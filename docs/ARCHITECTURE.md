# attack2jira Architecture

This document describes the technical architecture, design patterns, and implementation details of attack2jira.

## Table of Contents

- [System Overview](#system-overview)
- [Module Structure](#module-structure)
- [Data Flow](#data-flow)
- [API Interactions](#api-interactions)
- [Error Handling](#error-handling)
- [Retry Logic](#retry-logic)
- [Logging & Monitoring](#logging--monitoring)
- [Extensibility](#extensibility)

## System Overview

attack2jira is a Python-based CLI tool that acts as a bridge between the MITRE ATT&CK Framework and Atlassian Jira Cloud.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      attack2jira CLI                        │
│                                                             │
│  ┌──────────────────┐         ┌─────────────────────────┐ │
│  │  Attack2Jira     │────────▶│    JiraHandler          │ │
│  │  (Orchestrator)  │         │    (API Wrapper)        │ │
│  └──────────────────┘         └─────────────────────────┘ │
│          │                              │                  │
│          │                              │                  │
│          ▼                              ▼                  │
│  ┌──────────────────┐         ┌─────────────────────────┐ │
│  │  attackcti       │         │   requests (HTTP)       │ │
│  │  (ATT&CK Client) │         │                         │ │
│  └──────────────────┘         └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
           │                              │
           ▼                              ▼
┌──────────────────────┐       ┌────────────────────────────┐
│  MITRE ATT&CK API    │       │    Jira Cloud REST API     │
│  (cti-taxii.mitre.org)│       │  (*.atlassian.net)         │
└──────────────────────┘       └────────────────────────────┘
```

### Design Principles

1. **Simplicity**: Minimal dependencies, no complex configuration
2. **Idempotency**: Safe to re-run operations (custom fields, issues)
3. **Fail-Forward**: Continue processing on individual failures
4. **API-First**: All operations via REST APIs (no web scraping)
5. **Stateless**: No local database, Jira is the source of truth

### Technology Stack

- **Language**: Python 3.6+
- **HTTP Client**: requests (via attackcti)
- **ATT&CK Client**: attackcti (STIX/TAXII wrapper)
- **Authentication**: Basic Auth with API tokens
- **Data Format**: JSON (REST API and exports)

## Module Structure

### File Organization

```
attack2jira/
├── attack2jira.py          # Main entry point & Attack2Jira class
├── lib/
│   ├── __init__.py        # Package marker
│   └── jirahandler.py     # JiraHandler class
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

### attack2jira.py

**Responsibilities**:
- CLI argument parsing (argparse)
- High-level orchestration
- ATT&CK data fetching
- Issue creation logic
- Export generation

**Key Components**:

```python
class Attack2Jira:
    def __init__(self, url, username, password):
        """Initialize with Jira credentials."""
        self.jiraHandler = JiraHandler()
        self.jiraHandler.login(url, username, password)

    def set_up_jira_automated(self, project, key):
        """Orchestrate full project setup."""
        # 1. Create project
        # 2. Create custom fields
        # 3. Populate field options
        # 4. Configure screens
        # 5. Create issues

    def create_attack_techniques_and_subtechniques(self, key):
        """Generate issues for all techniques."""
        # Fetch from MITRE → Create in Jira

    def generate_json_layer(self, hideDisabled):
        """Export maturity data to Navigator JSON."""
        # Query Jira → Format as Navigator layer
```

### lib/jirahandler.py

**Responsibilities**:
- Low-level Jira REST API calls
- Authentication management
- Error handling for HTTP responses
- Custom field CRUD operations
- Issue creation
- Data retrieval (maturity levels)

**Key Components**:

```python
class JiraHandler:
    def login(self, url, username, apitoken):
        """Authenticate and store credentials."""

    def create_project(self, project, key):
        """POST /rest/simplified/latest/project"""

    def create_custom_fields(self):
        """POST /rest/api/2/field (x6)"""

    def create_issue(self, issue_dict, id):
        """POST /rest/api/2/issue"""

    def get_technique_maturity(self):
        """GET /rest/api/2/search (paginated)"""
```

## Data Flow

### Initialization Flow

```
User Command
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ python attack2jira.py -a initialize                         │
└─────────────────────────────────────────────────────────────┘
    │
    ├─▶ Parse Arguments (argparse)
    │
    ├─▶ Prompt for API Token (getpass)
    │
    ├─▶ Instantiate Attack2Jira(url, username, token)
    │       │
    │       ├─▶ JiraHandler.login()
    │       │       └─▶ GET /rest/api/2/issue/createmeta (auth test)
    │       │
    │       └─▶ set_up_jira_automated(project, key)
    │               │
    │               ├─▶ create_project()
    │               │       └─▶ POST /rest/simplified/latest/project
    │               │
    │               ├─▶ create_custom_fields()
    │               │       └─▶ POST /rest/api/2/field (x6)
    │               │
    │               ├─▶ add_custom_field_options()
    │               │       ├─▶ GET ATT&CK tactics (via attackcti)
    │               │       ├─▶ GET ATT&CK data sources
    │               │       └─▶ POST /rest/api/2/customFieldOption
    │               │
    │               ├─▶ add_custom_fields_to_screen(key)
    │               │       ├─▶ GET project metadata
    │               │       └─▶ POST screen field associations
    │               │
    │               ├─▶ hide_unwanted_fields(key)
    │               │       └─▶ PUT field layout configuration
    │               │
    │               └─▶ create_attack_techniques_and_subtechniques()
    │                       ├─▶ GET ATT&CK techniques (attackcti)
    │                       │       └─▶ cti-taxii.mitre.org
    │                       │
    │                       └─▶ For each technique:
    │                           ├─▶ create_issue() [Parent Task]
    │                           │       └─▶ POST /rest/api/2/issue
    │                           │
    │                           └─▶ For each sub-technique:
    │                               └─▶ create_issue() [Sub-task]
    │
    └─▶ Exit
```

### Export Flow

```
User Command
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ python attack2jira.py -a export                             │
└─────────────────────────────────────────────────────────────┘
    │
    ├─▶ Parse Arguments
    │
    ├─▶ Prompt for API Token
    │
    ├─▶ Instantiate Attack2Jira
    │       │
    │       └─▶ JiraHandler.login()
    │
    ├─▶ generate_json_layer(hideDisabled)
    │       │
    │       ├─▶ get_technique_maturity()
    │       │       └─▶ GET /rest/api/2/search
    │       │           ├─▶ JQL: project = ATTACK
    │       │           ├─▶ Paginate (50 issues/request)
    │       │           └─▶ Extract {techniqueID: maturity}
    │       │
    │       ├─▶ GET ATT&CK techniques (attackcti)
    │       │
    │       ├─▶ Map maturity → color
    │       │       ├─▶ "Not Tracked" → #DCDCDC
    │       │       ├─▶ "Initial" → #e1fce1
    │       │       ├─▶ "Defined" → #81fc81
    │       │       ├─▶ "Resilient" → #49fc49
    │       │       └─▶ "Optimized" → #03ad03
    │       │
    │       └─▶ Write attack2jira.json
    │               └─▶ ATT&CK Navigator Layer format
    │
    └─▶ Exit
```

## API Interactions

### Jira Cloud REST API

attack2jira uses the following Jira REST API v2 and simplified endpoints:

#### Authentication
```
Method: Basic Auth
Format: email:api_token (Base64)
Header: Authorization: Basic <base64>
```

#### Key Endpoints

**1. Authentication Test**
```
GET /rest/api/2/issue/createmeta
Purpose: Validate credentials
Response: 200 OK (success), 401 Unauthorized (failure)
```

**2. Project Creation**
```
POST /rest/simplified/latest/project
Body: {
  "name": "Mitre Attack Framework",
  "key": "ATTACK",
  "template": "com.pyxis.greenhopper.jira:gh-simplified-scrum"
}
Response: 201 Created
```

**3. Custom Field Creation**
```
POST /rest/api/2/field
Body: {
  "name": "Maturity",
  "type": "com.atlassian.jira.plugin.system.customfieldtypes:select",
  "searcherKey": "com.atlassian.jira.plugin.system.customfieldtypes:selectsearcher"
}
Response: 201 Created
Returns: {"id": "customfield_10001", ...}
```

**4. Issue Creation**
```
POST /rest/api/2/issue
Body: {
  "fields": {
    "project": {"key": "ATTACK"},
    "summary": "Active Scanning",
    "description": "...",
    "issuetype": {"name": "Task"},
    "customfield_10001": "T1595",
    ...
  }
}
Response: 201 Created
Returns: {"id": "10000", "key": "ATTACK-1"}
```

**5. Issue Search (Export)**
```
GET /rest/api/2/search?jql=project=ATTACK&startAt=0&maxResults=50
Purpose: Retrieve all issues with maturity data
Response: {
  "issues": [...],
  "total": 266,
  "startAt": 0,
  "maxResults": 50
}
```

### MITRE ATT&CK API

attack2jira uses the `attackcti` library to interact with MITRE's TAXII server.

#### Data Retrieved

**1. Techniques & Sub-techniques**
```python
from attackcti import attack_client

lift = attack_client()
techniques = lift.get_enterprise_techniques()

# Returns: List of STIX objects
# Filters: Revoked techniques excluded
```

**2. Tactics**
```python
tactics = lift.get_tactics()
# Returns: List of kill chain phases
# Example: ["reconnaissance", "execution", "persistence", ...]
```

**3. Data Sources**
```python
# Extracted from techniques
for technique in techniques:
    data_sources = technique.get('x_mitre_data_sources', [])
# Aggregated and deduplicated
```

## Error Handling

### Error Handling Strategy

attack2jira employs different error handling strategies based on criticality:

#### Critical Errors (Exit Immediately)

**Authentication Failures**:
```python
if response.status_code == 401:
    print("Authentication error. Invalid credentials.")
    sys.exit(1)
```

**Project Creation Conflicts**:
```python
if response.status_code == 400:
    print(f"Project with key '{key}' already exists.")
    sys.exit(1)
```

#### Non-Critical Errors (Log and Continue)

**Individual Issue Creation Failures**:
```python
try:
    issue_id, issue_key = self.jiraHandler.create_issue(issue_dict, technique_id)
    print(f"[SUCCESS] Created {issue_key}")
except Exception as e:
    print(f"[ERROR] Failed to create {technique_id}: {e}")
    # Continue to next technique
```

**Benefits**:
- Partial success is acceptable
- User can manually create failed issues
- Prevents complete failure due to transient errors

### Exception Types

**Network Errors**:
```python
import requests

try:
    response = requests.get(url, timeout=30)
except requests.exceptions.ConnectionError:
    print("Network connection failed")
    sys.exit(1)
except requests.exceptions.Timeout:
    print("Request timed out")
    sys.exit(1)
```

**HTTP Errors**:
```python
response = requests.post(url, ...)
if response.status_code >= 400:
    print(f"HTTP {response.status_code}: {response.text}")
```

## Retry Logic

### Current Implementation

attack2jira **does not implement automatic retry logic**. Failed operations must be retried manually.

### Recommended Enhancement

Future versions could implement exponential backoff:

```python
import time
from requests.exceptions import RequestException

def create_issue_with_retry(self, issue_dict, id, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=issue_dict, auth=auth, timeout=30)
            response.raise_for_status()
            return response.json()['id'], response.json()['key']
        except RequestException as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                print(f"Retry {attempt + 1}/{max_retries} in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
```

## Logging & Monitoring

### Current Logging

attack2jira uses simple print statements for logging:

```python
print(f"[INFO] Creating project {project}...")
print(f"[SUCCESS] Project created")
print(f"[ERROR] Failed to create issue: {e}")
```

**Limitations**:
- No log levels
- No file logging
- No structured logging

### Recommended Logging Enhancement

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('attack2jira.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Usage
logger.info("Creating project %s", project)
logger.error("Failed to create issue: %s", e)
```

### Monitoring Points

**Metrics to Track**:
1. Total techniques created
2. Failed issue creation count
3. API response times
4. Export generation time
5. Coverage percentage trends

**Integration Opportunities**:
- Prometheus metrics
- Datadog APM
- CloudWatch logs (AWS)
- Application Insights (Azure)

## Extensibility

### Extension Points

**1. Custom Maturity Levels**

Modify `lib/jirahandler.py`:
```python
def add_custom_field_options(self):
    # Add new maturity levels
    maturity_levels = [
        "Not Tracked",
        "Initial",
        "Defined",
        "Resilient",
        "Optimized",
        "Mature",      # New level
        "Advanced"     # New level
    ]
```

**2. Additional Custom Fields**

Extend `create_custom_fields()`:
```python
def create_custom_fields(self):
    # Existing fields...

    # New field: Priority
    self._create_field(
        name="Priority",
        type="com.atlassian.jira.plugin.system.customfieldtypes:select",
        options=["Low", "Medium", "High", "Critical"]
    )
```

**3. Multi-Project Support**

Modify `get_technique_maturity()` to accept project key:
```python
def get_technique_maturity(self, project_key='ATTACK'):
    jql = f"project = {project_key}"
    # Rest of method...
```

**4. Custom Export Formats**

Add new export methods:
```python
def generate_csv_export(self):
    """Export to CSV format."""
    maturity = self.jiraHandler.get_technique_maturity()

    import csv
    with open('attack2jira.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Technique ID', 'Maturity'])
        for tid, maturity_level in maturity.items():
            writer.writerow([tid, maturity_level])
```

**5. Webhook Integration**

Add webhook notifications on issue creation:
```python
def create_issue(self, issue_dict, id):
    # Create issue...

    # Notify webhook
    requests.post('https://hooks.slack.com/...', json={
        'text': f'Created {issue_key} for {id}'
    })
```

### Plugin Architecture (Future)

Potential plugin system:
```python
# plugins/custom_export.py
class CustomExportPlugin:
    def export(self, maturity_data):
        # Custom export logic
        pass

# Load plugins
from plugins import custom_export
plugin = custom_export.CustomExportPlugin()
plugin.export(maturity)
```

## Security Considerations

### Credential Management

- **API tokens**: Never logged or printed
- **getpass()**: Hides input during password entry
- **No persistence**: Credentials not stored to disk

### API Token Security

**Best Practices**:
- Rotate tokens every 90 days
- Use dedicated service accounts for automation
- Store tokens in secrets managers (not environment variables in logs)

### SSL/TLS

**Current**:
```python
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

**Recommended for Production**:
```python
# Remove warning suppression
# Ensure SSL verification enabled (default in requests)
response = requests.get(url, verify=True)
```

## Performance Characteristics

### Initialization Performance

**Time Complexity**: O(n) where n = number of techniques (~266)
**Bottlenecks**:
- Network latency (Jira API)
- API rate limits

**Typical Duration**: 10-20 minutes

### Export Performance

**Time Complexity**: O(n) with pagination (50 issues/request)
**Network Requests**: ~6 requests (266 issues / 50 per page)
**Typical Duration**: 30-120 seconds

### Optimization Opportunities

1. **Parallel Issue Creation**:
   ```python
   from concurrent.futures import ThreadPoolExecutor

   with ThreadPoolExecutor(max_workers=5) as executor:
       futures = [executor.submit(create_issue, issue) for issue in issues]
   ```

2. **Caching ATT&CK Data**:
   - Cache techniques locally for 24 hours
   - Reduce MITRE API calls

3. **Batch API Requests**:
   - Jira doesn't support bulk issue creation
   - Could batch field updates

## Next Steps

- **Workflows**: See real-world usage in [Workflows Guide](WORKFLOWS.md)
- **API Reference**: Detailed API docs in [API Reference](API_REFERENCE.md)
- **Troubleshooting**: Debug issues with [Troubleshooting Guide](TROUBLESHOOTING.md)

For questions or issues, visit the [GitHub repository](https://github.com/mvelazco/attack2jira).
