"""
MITRE ATT&CK API Client with async support, retry logic, and caching.

This module provides a client for fetching and parsing MITRE ATT&CK framework data.
"""

import asyncio
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import httpx

from .models import Technique, Tactic, DataSource


# Configure logger
logger = logging.getLogger(__name__)


class MitreAPIError(Exception):
    """Base exception for MITRE API errors."""
    pass


class MitreConnectionError(MitreAPIError):
    """Raised when connection to MITRE API fails."""
    pass


class MitreParseError(MitreAPIError):
    """Raised when parsing MITRE ATT&CK data fails."""
    pass


class MitreClient:
    """
    Async client for fetching and parsing MITRE ATT&CK framework data.

    This client fetches data from the MITRE ATT&CK STIX repository and provides
    methods to retrieve techniques, tactics, and data sources with optional filtering.

    Features:
    - Async/await support using httpx
    - Automatic retry with exponential backoff
    - In-memory caching with TTL
    - Structured logging
    - Comprehensive error handling
    - Type hints throughout

    Example:
        async with MitreClient() as client:
            techniques = await client.get_techniques()
            initial_access = await client.get_techniques(tactic="initial-access")
    """

    DEFAULT_API_URL = (
        "https://raw.githubusercontent.com/mitre/cti/master/"
        "enterprise-attack/enterprise-attack.json"
    )
    DEFAULT_TIMEOUT = 30.0
    DEFAULT_MAX_RETRIES = 3
    DEFAULT_CACHE_TTL = 3600  # 1 hour in seconds

    def __init__(
        self,
        api_url: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        cache_ttl: int = DEFAULT_CACHE_TTL,
    ):
        """
        Initialize the MITRE ATT&CK client.

        Args:
            api_url: URL to the MITRE ATT&CK STIX JSON data
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            cache_ttl: Cache time-to-live in seconds
        """
        self.api_url = api_url or self.DEFAULT_API_URL
        self.timeout = timeout
        self.max_retries = max_retries
        self.cache_ttl = cache_ttl

        # HTTP client (will be initialized in __aenter__)
        self._client: Optional[httpx.AsyncClient] = None

        # Cache storage
        self._cache: Dict[str, Any] = {}
        self._cache_timestamp: Optional[datetime] = None

        logger.info(
            f"Initialized MitreClient with url={self.api_url}, "
            f"timeout={self.timeout}s, max_retries={self.max_retries}"
        )

    async def __aenter__(self):
        """Async context manager entry."""
        self._client = httpx.AsyncClient(timeout=self.timeout)
        logger.debug("HTTP client initialized")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()
            logger.debug("HTTP client closed")
        return False

    def _is_cache_valid(self) -> bool:
        """
        Check if the cache is still valid.

        Returns:
            True if cache exists and hasn't expired, False otherwise
        """
        if not self._cache or not self._cache_timestamp:
            return False

        elapsed = datetime.now() - self._cache_timestamp
        is_valid = elapsed < timedelta(seconds=self.cache_ttl)

        if not is_valid:
            logger.debug("Cache expired")

        return is_valid

    def _invalidate_cache(self) -> None:
        """Clear the cache."""
        self._cache = {}
        self._cache_timestamp = None
        logger.debug("Cache invalidated")

    async def _fetch_with_retry(self, url: str) -> Dict[str, Any]:
        """
        Fetch data from URL with exponential backoff retry logic.

        Args:
            url: URL to fetch

        Returns:
            Parsed JSON data

        Raises:
            MitreConnectionError: If all retry attempts fail
        """
        if not self._client:
            raise MitreConnectionError("Client not initialized. Use 'async with' context manager.")

        last_exception = None

        for attempt in range(self.max_retries):
            try:
                logger.info(f"Fetching MITRE ATT&CK data (attempt {attempt + 1}/{self.max_retries})")

                response = await self._client.get(url)
                response.raise_for_status()

                logger.info(f"Successfully fetched data ({len(response.content)} bytes)")
                return response.json()

            except httpx.HTTPStatusError as e:
                last_exception = e
                logger.error(f"HTTP error {e.response.status_code}: {e}")

                # Don't retry on 4xx errors (client errors)
                if 400 <= e.response.status_code < 500:
                    raise MitreConnectionError(f"HTTP {e.response.status_code}: {e}") from e

            except httpx.RequestError as e:
                last_exception = e
                logger.warning(f"Request error on attempt {attempt + 1}: {e}")

            except Exception as e:
                last_exception = e
                logger.error(f"Unexpected error: {e}")

            # Exponential backoff: 2^attempt seconds
            if attempt < self.max_retries - 1:
                wait_time = 2 ** attempt
                logger.info(f"Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)

        # All retries exhausted
        error_msg = f"Failed to fetch data after {self.max_retries} attempts"
        logger.error(error_msg)
        raise MitreConnectionError(error_msg) from last_exception

    def _parse_technique(self, stix_obj: Dict[str, Any]) -> Optional[Technique]:
        """
        Parse a STIX technique object into a Technique model.

        Args:
            stix_obj: STIX JSON object

        Returns:
            Technique object or None if parsing fails
        """
        try:
            # Skip if revoked or deprecated
            if stix_obj.get("revoked", False) or stix_obj.get("x_mitre_deprecated", False):
                return None

            # Extract external ID and URL from external_references
            external_refs = stix_obj.get("external_references", [])
            mitre_ref = next(
                (ref for ref in external_refs if ref.get("source_name") == "mitre-attack"),
                None
            )

            if not mitre_ref:
                logger.warning(f"No MITRE reference found for {stix_obj.get('name', 'unknown')}")
                return None

            external_id = mitre_ref.get("external_id")
            url = mitre_ref.get("url", "")

            # Extract tactic from kill_chain_phases (use first one)
            kill_chain_phases = stix_obj.get("kill_chain_phases", [])
            tactic = kill_chain_phases[0]["phase_name"] if kill_chain_phases else "unknown"

            # Extract data sources
            data_sources = stix_obj.get("x_mitre_data_sources", [])

            # Check if it's a sub-technique
            is_subtechnique = stix_obj.get("x_mitre_is_subtechnique", False)

            # For sub-techniques, extract parent ID
            parent_id = None
            if is_subtechnique and "." in external_id:
                parent_id = external_id.split(".")[0]

            # Create Technique object
            technique = Technique(
                external_id=external_id,
                name=stix_obj.get("name", ""),
                description=stix_obj.get("description", ""),
                tactic=tactic,
                url=url,
                data_sources=data_sources,
                is_subtechnique=is_subtechnique,
                parent_id=parent_id,
            )

            return technique

        except Exception as e:
            logger.error(f"Failed to parse technique: {e}")
            return None

    async def _fetch_and_parse(self) -> Dict[str, List[Any]]:
        """
        Fetch and parse MITRE ATT&CK data.

        Returns:
            Dictionary with 'techniques', 'tactics', and 'data_sources' lists

        Raises:
            MitreConnectionError: If fetching fails
            MitreParseError: If parsing fails
        """
        # Check cache first
        if self._is_cache_valid():
            logger.debug("Returning cached data")
            return self._cache

        try:
            # Fetch data
            data = await self._fetch_with_retry(self.api_url)

            # Parse STIX objects
            stix_objects = data.get("objects", [])
            logger.info(f"Parsing {len(stix_objects)} STIX objects")

            techniques = []
            tactics = set()
            data_sources = set()

            for obj in stix_objects:
                obj_type = obj.get("type")

                if obj_type == "attack-pattern":
                    technique = self._parse_technique(obj)
                    if technique:
                        techniques.append(technique)
                        tactics.add(technique.tactic)
                        data_sources.update(technique.data_sources)

            # Sort techniques by external_id
            techniques.sort(key=lambda t: t.external_id)

            logger.info(
                f"Parsed {len(techniques)} techniques, "
                f"{len(tactics)} tactics, "
                f"{len(data_sources)} data sources"
            )

            # Create result
            result = {
                "techniques": techniques,
                "tactics": [Tactic(name=t, description=None) for t in sorted(tactics)],
                "data_sources": [DataSource(name=ds, description=None) for ds in sorted(data_sources)],
            }

            # Cache the result
            self._cache = result
            self._cache_timestamp = datetime.now()
            logger.debug("Data cached")

            return result

        except MitreConnectionError:
            raise
        except Exception as e:
            error_msg = f"Failed to parse MITRE ATT&CK data: {e}"
            logger.error(error_msg)
            raise MitreParseError(error_msg) from e

    async def get_techniques(self, tactic: Optional[str] = None) -> List[Technique]:
        """
        Get all techniques, optionally filtered by tactic.

        Args:
            tactic: Optional tactic name to filter by (e.g., 'initial-access')

        Returns:
            List of Technique objects

        Raises:
            MitreAPIError: If fetching or parsing fails

        Example:
            techniques = await client.get_techniques()
            initial_access = await client.get_techniques(tactic="initial-access")
        """
        logger.info(f"Getting techniques{f' for tactic={tactic}' if tactic else ''}")

        data = await self._fetch_and_parse()
        techniques = data["techniques"]

        if tactic:
            techniques = [t for t in techniques if t.tactic == tactic]
            logger.info(f"Filtered to {len(techniques)} techniques for tactic '{tactic}'")

        return techniques

    async def get_tactics(self) -> List[Tactic]:
        """
        Get all tactics.

        Returns:
            List of Tactic objects

        Raises:
            MitreAPIError: If fetching or parsing fails
        """
        logger.info("Getting tactics")
        data = await self._fetch_and_parse()
        return data["tactics"]

    async def get_data_sources(self) -> List[DataSource]:
        """
        Get all data sources.

        Returns:
            List of DataSource objects

        Raises:
            MitreAPIError: If fetching or parsing fails
        """
        logger.info("Getting data sources")
        data = await self._fetch_and_parse()
        return data["data_sources"]

    async def get_technique_by_id(self, external_id: str) -> Optional[Technique]:
        """
        Get a specific technique by its external ID.

        Args:
            external_id: MITRE ATT&CK ID (e.g., 'T1234' or 'T1234.001')

        Returns:
            Technique object or None if not found

        Raises:
            MitreAPIError: If fetching or parsing fails
        """
        logger.info(f"Getting technique by ID: {external_id}")
        techniques = await self.get_techniques()
        return next((t for t in techniques if t.external_id == external_id), None)

    async def get_parent_techniques(self) -> List[Technique]:
        """
        Get only parent techniques (not sub-techniques).

        Returns:
            List of parent Technique objects

        Raises:
            MitreAPIError: If fetching or parsing fails
        """
        logger.info("Getting parent techniques")
        techniques = await self.get_techniques()
        return [t for t in techniques if not t.is_subtechnique]

    async def get_subtechniques(self, parent_id: Optional[str] = None) -> List[Technique]:
        """
        Get sub-techniques, optionally filtered by parent ID.

        Args:
            parent_id: Optional parent technique ID (e.g., 'T1234')

        Returns:
            List of sub-technique objects

        Raises:
            MitreAPIError: If fetching or parsing fails
        """
        logger.info(f"Getting sub-techniques{f' for parent={parent_id}' if parent_id else ''}")
        techniques = await self.get_techniques()
        subtechniques = [t for t in techniques if t.is_subtechnique]

        if parent_id:
            subtechniques = [t for t in subtechniques if t.parent_id == parent_id]

        return subtechniques

    def clear_cache(self) -> None:
        """Manually clear the cache."""
        self._invalidate_cache()
        logger.info("Cache cleared manually")
