"""
Unit tests for MITRE ATT&CK client and models.

These tests use mocked API responses to verify client functionality without
making actual network requests.
"""

import pytest
import pytest_asyncio
import asyncio
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
import httpx

from src.mitre.client import (
    MitreClient,
    MitreAPIError,
    MitreConnectionError,
    MitreParseError,
)
from src.mitre.models import Technique, Tactic, DataSource


# Mock STIX data for testing
MOCK_STIX_DATA = {
    "type": "bundle",
    "id": "bundle--test",
    "spec_version": "2.0",
    "objects": [
        {
            "type": "attack-pattern",
            "id": "attack-pattern--test-1",
            "name": "Test Technique",
            "description": "This is a test technique",
            "external_references": [
                {
                    "source_name": "mitre-attack",
                    "external_id": "T1234",
                    "url": "https://attack.mitre.org/techniques/T1234"
                }
            ],
            "kill_chain_phases": [
                {
                    "kill_chain_name": "mitre-attack",
                    "phase_name": "initial-access"
                }
            ],
            "x_mitre_data_sources": ["Process monitoring", "File monitoring"],
            "x_mitre_is_subtechnique": False,
        },
        {
            "type": "attack-pattern",
            "id": "attack-pattern--test-2",
            "name": "Test Sub-technique",
            "description": "This is a test sub-technique",
            "external_references": [
                {
                    "source_name": "mitre-attack",
                    "external_id": "T1234.001",
                    "url": "https://attack.mitre.org/techniques/T1234/001"
                }
            ],
            "kill_chain_phases": [
                {
                    "kill_chain_name": "mitre-attack",
                    "phase_name": "initial-access"
                }
            ],
            "x_mitre_data_sources": ["Process monitoring"],
            "x_mitre_is_subtechnique": True,
        },
        {
            "type": "attack-pattern",
            "id": "attack-pattern--test-3",
            "name": "Test Technique 2",
            "description": "This is another test technique",
            "external_references": [
                {
                    "source_name": "mitre-attack",
                    "external_id": "T5678",
                    "url": "https://attack.mitre.org/techniques/T5678"
                }
            ],
            "kill_chain_phases": [
                {
                    "kill_chain_name": "mitre-attack",
                    "phase_name": "execution"
                }
            ],
            "x_mitre_data_sources": ["Command execution"],
            "x_mitre_is_subtechnique": False,
        },
        {
            "type": "attack-pattern",
            "id": "attack-pattern--revoked",
            "name": "Revoked Technique",
            "description": "This technique is revoked",
            "revoked": True,
            "external_references": [
                {
                    "source_name": "mitre-attack",
                    "external_id": "T9999",
                    "url": "https://attack.mitre.org/techniques/T9999"
                }
            ],
        },
        {
            "type": "x-mitre-tactic",
            "id": "tactic--test",
            "name": "initial-access",
            "description": "Test tactic",
        }
    ]
}


class TestModels:
    """Tests for Pydantic models."""

    def test_data_source_creation(self):
        """Test DataSource model creation."""
        ds = DataSource(name="Process monitoring", description="Monitor process activity")
        assert ds.name == "Process monitoring"
        assert ds.description == "Monitor process activity"

    def test_data_source_optional_description(self):
        """Test DataSource with optional description."""
        ds = DataSource(name="File monitoring")
        assert ds.name == "File monitoring"
        assert ds.description is None

    def test_tactic_creation(self):
        """Test Tactic model creation."""
        tactic = Tactic(name="initial-access", description="The adversary is trying to get in")
        assert tactic.name == "initial-access"
        assert tactic.description == "The adversary is trying to get in"

    def test_technique_creation(self):
        """Test Technique model creation."""
        technique = Technique(
            external_id="T1234",
            name="Test Technique",
            description="This is a test",
            tactic="initial-access",
            url="https://attack.mitre.org/techniques/T1234",
            data_sources=["Process monitoring", "File monitoring"],
            is_subtechnique=False,
            parent_id=None,
        )
        assert technique.external_id == "T1234"
        assert technique.name == "Test Technique"
        assert technique.tactic == "initial-access"
        assert len(technique.data_sources) == 2
        assert not technique.is_subtechnique
        assert technique.is_parent

    def test_subtechnique_creation(self):
        """Test sub-technique model creation."""
        subtechnique = Technique(
            external_id="T1234.001",
            name="Test Sub-technique",
            description="This is a sub-technique",
            tactic="initial-access",
            url="https://attack.mitre.org/techniques/T1234/001",
            data_sources=["Process monitoring"],
            is_subtechnique=True,
            parent_id="T1234",
        )
        assert subtechnique.external_id == "T1234.001"
        assert subtechnique.is_subtechnique
        assert not subtechnique.is_parent
        assert subtechnique.parent_id == "T1234"

    def test_technique_id_parts_parent(self):
        """Test technique_id_parts property for parent technique."""
        technique = Technique(
            external_id="T1234",
            name="Test",
            description="Test",
            tactic="initial-access",
            url="https://example.com",
        )
        parent_id, sub_id = technique.technique_id_parts
        assert parent_id == "T1234"
        assert sub_id is None

    def test_technique_id_parts_subtechnique(self):
        """Test technique_id_parts property for sub-technique."""
        technique = Technique(
            external_id="T1234.001",
            name="Test",
            description="Test",
            tactic="initial-access",
            url="https://example.com",
            is_subtechnique=True,
            parent_id="T1234",
        )
        parent_id, sub_id = technique.technique_id_parts
        assert parent_id == "T1234"
        assert sub_id == "001"

    def test_technique_string_representation(self):
        """Test __str__ method."""
        technique = Technique(
            external_id="T1234",
            name="Test Technique",
            description="Test",
            tactic="initial-access",
            url="https://example.com",
        )
        assert str(technique) == "T1234: Test Technique"

    def test_technique_repr(self):
        """Test __repr__ method."""
        technique = Technique(
            external_id="T1234",
            name="Test Technique",
            description="Test",
            tactic="initial-access",
            url="https://example.com",
            is_subtechnique=False,
        )
        repr_str = repr(technique)
        assert "T1234" in repr_str
        assert "Test Technique" in repr_str
        assert "initial-access" in repr_str
        assert "is_subtechnique=False" in repr_str


class TestMitreClient:
    """Tests for MitreClient."""

    @pytest_asyncio.fixture
    async def mock_client(self):
        """Create a mock client with mocked HTTP responses."""
        client = MitreClient(cache_ttl=1)

        # Mock the HTTP client
        mock_http_client = AsyncMock(spec=httpx.AsyncClient)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCK_STIX_DATA
        mock_response.content = b"mock content"
        mock_response.raise_for_status = MagicMock()

        mock_http_client.get = AsyncMock(return_value=mock_response)
        mock_http_client.aclose = AsyncMock()

        async with client:
            client._client = mock_http_client
            yield client

    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test async context manager."""
        async with MitreClient() as client:
            assert client._client is not None

    @pytest.mark.asyncio
    async def test_get_techniques(self, mock_client):
        """Test fetching all techniques."""
        techniques = await mock_client.get_techniques()

        # Should get 3 techniques (revoked one is filtered out)
        assert len(techniques) == 3
        assert all(isinstance(t, Technique) for t in techniques)

        # Verify IDs
        ids = [t.external_id for t in techniques]
        assert "T1234" in ids
        assert "T1234.001" in ids
        assert "T5678" in ids
        assert "T9999" not in ids  # Revoked technique should be filtered

    @pytest.mark.asyncio
    async def test_get_techniques_filtered_by_tactic(self, mock_client):
        """Test filtering techniques by tactic."""
        techniques = await mock_client.get_techniques(tactic="initial-access")

        assert len(techniques) == 2
        assert all(t.tactic == "initial-access" for t in techniques)

    @pytest.mark.asyncio
    async def test_get_tactics(self, mock_client):
        """Test fetching all tactics."""
        tactics = await mock_client.get_tactics()

        assert len(tactics) >= 2
        assert all(isinstance(t, Tactic) for t in tactics)

        tactic_names = [t.name for t in tactics]
        assert "initial-access" in tactic_names
        assert "execution" in tactic_names

    @pytest.mark.asyncio
    async def test_get_data_sources(self, mock_client):
        """Test fetching all data sources."""
        data_sources = await mock_client.get_data_sources()

        assert len(data_sources) >= 3
        assert all(isinstance(ds, DataSource) for ds in data_sources)

        ds_names = [ds.name for ds in data_sources]
        assert "Process monitoring" in ds_names
        assert "File monitoring" in ds_names

    @pytest.mark.asyncio
    async def test_get_technique_by_id(self, mock_client):
        """Test fetching a specific technique by ID."""
        technique = await mock_client.get_technique_by_id("T1234")

        assert technique is not None
        assert technique.external_id == "T1234"
        assert technique.name == "Test Technique"

    @pytest.mark.asyncio
    async def test_get_technique_by_id_not_found(self, mock_client):
        """Test fetching a non-existent technique."""
        technique = await mock_client.get_technique_by_id("T0000")
        assert technique is None

    @pytest.mark.asyncio
    async def test_get_parent_techniques(self, mock_client):
        """Test fetching only parent techniques."""
        parents = await mock_client.get_parent_techniques()

        assert len(parents) == 2
        assert all(not t.is_subtechnique for t in parents)

        ids = [t.external_id for t in parents]
        assert "T1234" in ids
        assert "T5678" in ids
        assert "T1234.001" not in ids

    @pytest.mark.asyncio
    async def test_get_subtechniques(self, mock_client):
        """Test fetching all sub-techniques."""
        subtechniques = await mock_client.get_subtechniques()

        assert len(subtechniques) == 1
        assert all(t.is_subtechnique for t in subtechniques)
        assert subtechniques[0].external_id == "T1234.001"

    @pytest.mark.asyncio
    async def test_get_subtechniques_by_parent(self, mock_client):
        """Test fetching sub-techniques for a specific parent."""
        subtechniques = await mock_client.get_subtechniques(parent_id="T1234")

        assert len(subtechniques) == 1
        assert subtechniques[0].parent_id == "T1234"
        assert subtechniques[0].external_id == "T1234.001"

    @pytest.mark.asyncio
    async def test_caching(self, mock_client):
        """Test that results are cached."""
        # First call
        techniques1 = await mock_client.get_techniques()

        # Second call should use cache
        techniques2 = await mock_client.get_techniques()

        # Should have same results
        assert len(techniques1) == len(techniques2)

        # HTTP client should only be called once
        assert mock_client._client.get.call_count == 1

    @pytest.mark.asyncio
    async def test_cache_expiration(self, mock_client):
        """Test that cache expires after TTL."""
        # First call
        await mock_client.get_techniques()

        # Simulate cache expiration
        mock_client._cache_timestamp = datetime.now() - timedelta(seconds=2)

        # Second call should fetch again
        await mock_client.get_techniques()

        # HTTP client should be called twice
        assert mock_client._client.get.call_count == 2

    @pytest.mark.asyncio
    async def test_clear_cache(self, mock_client):
        """Test manual cache clearing."""
        # Populate cache
        await mock_client.get_techniques()
        assert mock_client._cache

        # Clear cache
        mock_client.clear_cache()
        assert not mock_client._cache
        assert mock_client._cache_timestamp is None

    @pytest.mark.asyncio
    async def test_retry_on_network_error(self):
        """Test retry logic on network errors."""
        client = MitreClient(max_retries=3)

        mock_http_client = AsyncMock(spec=httpx.AsyncClient)

        # First two calls fail, third succeeds
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCK_STIX_DATA
        mock_response.content = b"mock content"
        mock_response.raise_for_status = MagicMock()

        mock_http_client.get = AsyncMock(
            side_effect=[
                httpx.RequestError("Network error"),
                httpx.RequestError("Network error"),
                mock_response,
            ]
        )
        mock_http_client.aclose = AsyncMock()

        async with client:
            client._client = mock_http_client

            # Should succeed after retries
            techniques = await client.get_techniques()
            assert len(techniques) == 3
            assert mock_http_client.get.call_count == 3

    @pytest.mark.asyncio
    async def test_no_retry_on_client_error(self):
        """Test that 4xx errors don't trigger retries."""
        client = MitreClient(max_retries=3)

        mock_http_client = AsyncMock(spec=httpx.AsyncClient)

        # 404 error
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Not found", request=MagicMock(), response=mock_response
        )

        mock_http_client.get = AsyncMock(return_value=mock_response)
        mock_http_client.aclose = AsyncMock()

        async with client:
            client._client = mock_http_client

            with pytest.raises(MitreConnectionError):
                await client.get_techniques()

            # Should only try once (no retries on 4xx)
            assert mock_http_client.get.call_count == 1

    @pytest.mark.asyncio
    async def test_max_retries_exhausted(self):
        """Test behavior when all retries are exhausted."""
        client = MitreClient(max_retries=2)

        mock_http_client = AsyncMock(spec=httpx.AsyncClient)
        mock_http_client.get = AsyncMock(
            side_effect=httpx.RequestError("Network error")
        )
        mock_http_client.aclose = AsyncMock()

        async with client:
            client._client = mock_http_client

            with pytest.raises(MitreConnectionError) as exc_info:
                await client.get_techniques()

            assert "Failed to fetch data after 2 attempts" in str(exc_info.value)
            assert mock_http_client.get.call_count == 2

    @pytest.mark.asyncio
    async def test_client_not_initialized_error(self):
        """Test error when client is used outside context manager."""
        client = MitreClient()

        with pytest.raises(MitreConnectionError) as exc_info:
            await client.get_techniques()

        assert "not initialized" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_parse_error_handling(self, mock_client):
        """Test handling of parsing errors."""
        # Mock invalid JSON response
        mock_client._client.get = AsyncMock(
            return_value=MagicMock(
                status_code=200,
                json=MagicMock(return_value={"invalid": "data"}),
                content=b"invalid",
                raise_for_status=MagicMock(),
            )
        )

        # Clear cache to force new fetch
        mock_client.clear_cache()

        # Should not raise but return empty list since no valid objects
        techniques = await mock_client.get_techniques()
        assert techniques == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
