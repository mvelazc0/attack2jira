# MITRE ATT&CK Client

A modern, async Python client for fetching and parsing MITRE ATT&CK framework data.

## Features

- **Async/Await Support**: Built with `httpx` for efficient async operations
- **Pydantic Models**: Type-safe data models with validation
- **Automatic Retry**: Exponential backoff retry logic for network failures
- **Caching**: In-memory cache with configurable TTL
- **Structured Logging**: Comprehensive logging for debugging
- **Type Hints**: Full type annotations throughout
- **Comprehensive Testing**: 27 unit tests with mocked API responses

## Installation

```bash
pip install -r requirements.txt
```

Dependencies:
- `httpx>=0.24.0` - Async HTTP client
- `pydantic>=2.0.0` - Data validation
- `pytest>=7.0.0` - Testing framework
- `pytest-asyncio>=0.21.0` - Async test support

## Quick Start

```python
import asyncio
from src.mitre.client import MitreClient

async def main():
    async with MitreClient() as client:
        # Get all techniques
        techniques = await client.get_techniques()

        # Filter by tactic
        initial_access = await client.get_techniques(tactic="initial-access")

        # Get specific technique
        technique = await client.get_technique_by_id("T1566")

        print(f"Found {len(techniques)} techniques")

asyncio.run(main())
```

## Data Models

### Technique

Represents a MITRE ATT&CK technique or sub-technique.

```python
from src.mitre.models import Technique

technique = Technique(
    external_id="T1566",
    name="Phishing",
    description="Adversaries may send phishing messages...",
    tactic="initial-access",
    url="https://attack.mitre.org/techniques/T1566",
    data_sources=["Network Traffic", "Application Log"],
    is_subtechnique=False,
    parent_id=None
)
```

**Properties:**
- `external_id`: MITRE ID (e.g., "T1566" or "T1566.001")
- `name`: Technique name
- `description`: Detailed description
- `tactic`: Primary tactic
- `url`: MITRE ATT&CK URL
- `data_sources`: List of detection data sources
- `is_subtechnique`: Boolean flag
- `parent_id`: Parent ID for sub-techniques

**Methods:**
- `is_parent`: Check if parent technique
- `technique_id_parts`: Split ID into (parent, sub) parts

### Tactic

Represents a MITRE ATT&CK tactic.

```python
from src.mitre.models import Tactic

tactic = Tactic(
    name="initial-access",
    description="The adversary is trying to get in"
)
```

### DataSource

Represents a data source for detection.

```python
from src.mitre.models import DataSource

data_source = DataSource(
    name="Process Monitoring",
    description="Information about running processes"
)
```

## Client API

### MitreClient

Main client class for fetching MITRE ATT&CK data.

#### Initialization

```python
client = MitreClient(
    api_url=None,           # Optional custom API URL
    timeout=30.0,           # Request timeout in seconds
    max_retries=3,          # Maximum retry attempts
    cache_ttl=3600          # Cache TTL in seconds
)
```

#### Methods

**get_techniques(tactic: Optional[str] = None) -> List[Technique]**

Get all techniques, optionally filtered by tactic.

```python
async with MitreClient() as client:
    all_techniques = await client.get_techniques()
    initial_access = await client.get_techniques(tactic="initial-access")
```

**get_tactics() -> List[Tactic]**

Get all tactics.

```python
async with MitreClient() as client:
    tactics = await client.get_tactics()
```

**get_data_sources() -> List[DataSource]**

Get all data sources.

```python
async with MitreClient() as client:
    data_sources = await client.get_data_sources()
```

**get_technique_by_id(external_id: str) -> Optional[Technique]**

Get a specific technique by ID.

```python
async with MitreClient() as client:
    technique = await client.get_technique_by_id("T1566")
```

**get_parent_techniques() -> List[Technique]**

Get only parent techniques (not sub-techniques).

```python
async with MitreClient() as client:
    parents = await client.get_parent_techniques()
```

**get_subtechniques(parent_id: Optional[str] = None) -> List[Technique]**

Get sub-techniques, optionally filtered by parent.

```python
async with MitreClient() as client:
    all_subs = await client.get_subtechniques()
    phishing_subs = await client.get_subtechniques(parent_id="T1566")
```

**clear_cache() -> None**

Manually clear the cache.

```python
client.clear_cache()
```

## Error Handling

The client defines three exception types:

- `MitreAPIError`: Base exception for all errors
- `MitreConnectionError`: Network/connection errors
- `MitreParseError`: JSON parsing errors

```python
from src.mitre.client import MitreClient, MitreAPIError

try:
    async with MitreClient() as client:
        techniques = await client.get_techniques()
except MitreAPIError as e:
    print(f"Error: {e}")
```

## Caching

The client automatically caches results to improve performance:

- Default TTL: 3600 seconds (1 hour)
- Cache invalidates after TTL expires
- Manual cache clearing available

```python
client = MitreClient(cache_ttl=1800)  # 30 minutes
await client.get_techniques()  # Fetches from API
await client.get_techniques()  # Returns from cache
client.clear_cache()           # Clear cache
```

## Retry Logic

The client automatically retries failed requests:

- Default: 3 attempts
- Exponential backoff: 2^attempt seconds (2s, 4s, 8s)
- No retry on 4xx client errors
- Automatic retry on 5xx and network errors

```python
client = MitreClient(max_retries=5)  # Up to 5 attempts
```

## Logging

Configure logging to see client operations:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Now client operations will be logged
async with MitreClient() as client:
    techniques = await client.get_techniques()
```

## Testing

Run the test suite:

```bash
# Run all tests
pytest tests/test_mitre.py -v

# Run specific test
pytest tests/test_mitre.py::TestModels::test_technique_creation -v

# Run with coverage
pytest tests/test_mitre.py --cov=src.mitre --cov-report=html
```

## Example Usage

See `example_mitre_client.py` for a complete example demonstrating all features.

```bash
python example_mitre_client.py
```

## Architecture

```
src/mitre/
├── __init__.py       # Package exports
├── models.py         # Pydantic data models
├── client.py         # Async HTTP client
└── README.md         # This file

tests/
├── __init__.py
└── test_mitre.py     # Unit tests with mocked responses
```

## API Data Source

The client fetches data from the official MITRE CTI repository:

```
https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json
```

This is the authoritative source for MITRE ATT&CK Enterprise framework data in STIX 2.0 format.

## Contributing

When contributing:

1. Add type hints to all functions
2. Update tests for new features
3. Ensure all tests pass
4. Update documentation

## License

This project follows the same license as the parent repository (BSD 3-Clause).
