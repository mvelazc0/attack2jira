# attack2jira API Reference

This guide provides a comprehensive reference for integrating attack2jira into custom Python scripts and understanding its internal APIs.

## Table of Contents

- [Overview](#overview)
- [Module Structure](#module-structure)
- [Attack2Jira Class](#attack2jira-class)
- [JiraHandler Class](#jirahandler-class)
- [Custom Scripts](#custom-scripts)
- [JSON Export Format](#json-export-format)
- [Integration Examples](#integration-examples)

## Overview

attack2jira consists of two main Python modules:

1. **attack2jira.py**: Main orchestration class (`Attack2Jira`)
2. **lib/jirahandler.py**: Jira REST API wrapper (`JiraHandler`)

Both can be imported and used in custom Python scripts for advanced automation and integration.

### Import Structure

```python
from attack2jira import Attack2Jira
from lib.jirahandler import JiraHandler
```

## Module Structure

### File Layout

```
attack2jira/
├── attack2jira.py          # Main module with Attack2Jira class
├── lib/
│   ├── __init__.py        # Makes lib a package
│   └── jirahandler.py     # JiraHandler class for API operations
└── requirements.txt        # Dependencies (attackcti)
```

### Dependencies

attack2jira depends on:

- **attackcti**: MITRE ATT&CK Python client
- **requests**: HTTP library (indirect dependency via attackcti)
- **json, sys, argparse, traceback, getpass, urllib3**: Standard library

Install dependencies:
```bash
pip install -r requirements.txt
```

Or programmatically:
```python
import subprocess
subprocess.check_call(['pip', 'install', 'attackcti'])
```

## Attack2Jira Class

The main orchestration class for ATT&CK data synchronization.

### Class Definition

```python
class Attack2Jira:
    """Main class for synchronizing MITRE ATT&CK data to Jira."""

    def __init__(self, url, username, password):
        """
        Initialize Attack2Jira instance.

        Args:
            url (str): Jira Cloud instance URL (e.g., https://company.atlassian.net)
            username (str): Jira username/email address
            password (str): Jira API token
        """
```

**Example**:
```python
from attack2jira import Attack2Jira

# Initialize
a2j = Attack2Jira(
    url='https://company.atlassian.net',
    username='user@company.com',
    password='your-api-token-here'
)
```

### Methods

#### `set_up_jira_automated(project, key)`

Orchestrates the complete Jira project setup.

```python
def set_up_jira_automated(self, project, key):
    """
    Create and configure a complete ATT&CK tracking project in Jira.

    Args:
        project (str): Project name (e.g., "Mitre Attack Framework")
        key (str): Project key (e.g., "ATTACK")

    Returns:
        None

    Raises:
        SystemExit: On authentication or permission errors
    """
```

**Workflow**:
1. Creates Jira project
2. Creates 6 custom fields
3. Adds field options (tactics, data sources, maturity levels)
4. Adds custom fields to screens
5. Hides unwanted fields
6. Creates all ATT&CK technique and sub-technique issues

**Example**:
```python
a2j.set_up_jira_automated(
    project='Security Coverage Tracker',
    key='SECOV'
)
```

#### `create_attack_techniques_and_subtechniques(key)`

Creates Jira issues for all ATT&CK techniques and sub-techniques.

```python
def create_attack_techniques_and_subtechniques(self, key):
    """
    Generate Jira issues for techniques (as Tasks) and sub-techniques (as Sub-tasks).

    Args:
        key (str): Project key (e.g., "ATTACK")

    Returns:
        None

    Side Effects:
        - Fetches ATT&CK data from MITRE API
        - Creates 266+ Jira issues
        - Prints progress to stdout
    """
```

**Example**:
```python
a2j.create_attack_techniques_and_subtechniques(key='ATTACK')
```

**Technical Details**:
- Fetches techniques via `attackcti.attack_client()`
- Filters out revoked techniques
- Sorts by technique ID (e.g., T1001, T1002, ...)
- Creates parent Task issues for techniques
- Creates Sub-task issues for sub-techniques linked to parents
- Continues on individual failures

#### `generate_json_layer(hideDisabled)`

Exports Jira maturity data to ATT&CK Navigator JSON format.

```python
def generate_json_layer(self, hideDisabled):
    """
    Generate ATT&CK Navigator JSON layer from Jira maturity data.

    Args:
        hideDisabled (bool): If True, mark 'Not Tracked' techniques as disabled

    Returns:
        None (writes to attack2jira.json)

    Side Effects:
        - Queries all issues from ATTACK project in Jira
        - Writes attack2jira.json to current directory
    """
```

**Color Mapping**:
- "Not Tracked" → Gray (#DCDCDC)
- "Initial" → Light green (#e1fce1)
- "Defined" → Medium green (#81fc81)
- "Resilient" → Darker green (#49fc49)
- "Optimized" → Darkest green (#03ad03)

**Example**:
```python
# Export with all techniques
a2j.generate_json_layer(hideDisabled=False)

# Export with 'Not Tracked' techniques grayed out
a2j.generate_json_layer(hideDisabled=True)
```

#### `get_attack_techniques()` (Deprecated)

Fetches ATT&CK techniques from MITRE API.

```python
def get_attack_techniques(self):
    """
    Fetch all enterprise ATT&CK techniques from MITRE.

    Returns:
        list: ATT&CK technique objects (dicts)

    Note: DEPRECATED - Use create_attack_techniques_and_subtechniques() instead
    """
```

## JiraHandler Class

Low-level Jira REST API wrapper for all Jira operations.

### Class Definition

```python
class JiraHandler:
    """Wrapper for Jira REST API operations."""

    def __init__(self):
        """Initialize JiraHandler."""
        self.username = None
        self.apitoken = None
        self.url = None
```

### Authentication

#### `login(url, username, apitoken)`

Authenticate with Jira Cloud.

```python
def login(self, url, username, apitoken):
    """
    Authenticate to Jira Cloud and validate credentials.

    Args:
        url (str): Jira Cloud URL (e.g., https://company.atlassian.net)
        username (str): Email address
        apitoken (str): API token from Atlassian account

    Returns:
        None

    Raises:
        SystemExit: On 401 (unauthorized) or connection errors
    """
```

**Example**:
```python
from lib.jirahandler import JiraHandler

jira = JiraHandler()
jira.login(
    url='https://company.atlassian.net',
    username='user@company.com',
    apitoken='your-api-token-here'
)
```

### Project Management

#### `create_project(project, key)`

Create a new Jira project.

```python
def create_project(self, project, key):
    """
    Create Jira Software project using Greenhopper template.

    Args:
        project (str): Project name
        key (str): Project key (uppercase letters)

    Returns:
        None

    Raises:
        SystemExit: On 400 (project exists) or 401 (permissions)
    """
```

**Example**:
```python
jira.create_project(project='ATT&CK Tracker', key='ATTACK')
```

### Custom Field Management

#### `create_custom_fields()`

Create all required custom fields.

```python
def create_custom_fields(self):
    """
    Create 6 custom fields: Id, Tactic, Maturity, Url, Datasources, Sub-Technique of.

    Returns:
        None

    Side Effects:
        - Creates fields only if they don't already exist
        - Prints progress to stdout
    """
```

**Created Fields**:
1. **Id** (Text): Technique ID (e.g., T1234)
2. **Tactic** (Select): ATT&CK tactic/kill chain phase
3. **Maturity** (Select): Detection maturity level
4. **Url** (URL): Link to attack.mitre.org
5. **Datasources** (Multi-select): Available data sources
6. **Sub-Technique of** (Text): Parent technique reference

#### `add_custom_field_options()`

Populate custom field dropdown values.

```python
def add_custom_field_options(self):
    """
    Populate custom field options from ATT&CK API.

    Returns:
        None

    Fetches:
        - Tactics from ATT&CK API
        - Data sources from ATT&CK techniques
        - Adds maturity levels (hardcoded)
    """
```

**Maturity Levels**:
- Not Tracked
- Initial
- Defined
- Resilient
- Optimized

#### `get_custom_fields()`

Retrieve custom field IDs from Jira.

```python
def get_custom_fields(self):
    """
    Get mapping of custom field names to Jira field IDs.

    Returns:
        dict: {field_name: customfield_id}
        Example: {'Id': 'customfield_10001', 'Tactic': 'customfield_10002', ...}
    """
```

**Example**:
```python
fields = jira.get_custom_fields()
print(f"Maturity field ID: {fields['Maturity']}")
```

### Issue Creation

#### `create_issue(issue_dict, id)`

Create a Jira issue or sub-task.

```python
def create_issue(self, issue_dict, id):
    """
    Create a Jira issue.

    Args:
        issue_dict (dict): Issue data in Jira JSON format
        id (str): Technique ID for logging (e.g., "T1234")

    Returns:
        tuple: (issue_id, issue_key) or None on failure
        Example: ("10001", "ATTACK-42")

    Raises:
        SystemExit: On 400 errors
    """
```

**Example Issue Dict**:
```python
issue = {
    "fields": {
        "project": {"key": "ATTACK"},
        "summary": "Active Scanning",
        "description": "Adversaries may execute active...",
        "issuetype": {"name": "Task"},
        "customfield_10001": "T1595",  # Id field
        "customfield_10002": {"value": "reconnaissance"},  # Tactic
        "customfield_10003": {"value": "Not Tracked"},  # Maturity
        "customfield_10004": "https://attack.mitre.org/techniques/T1595"  # Url
    }
}

issue_id, issue_key = jira.create_issue(issue, "T1595")
print(f"Created {issue_key} (ID: {issue_id})")
```

### Data Retrieval

#### `get_technique_maturity()`

Retrieve maturity levels for all techniques from Jira.

```python
def get_technique_maturity(self):
    """
    Query Jira for all ATTACK project issues and extract maturity levels.

    Returns:
        dict: {technique_id: maturity_value}
        Example: {'T1595': 'Initial', 'T1595.001': 'Defined', ...}

    Note: Hardcoded to search project key "ATTACK"
    """
```

**Example**:
```python
maturity = jira.get_technique_maturity()
print(f"T1595 maturity: {maturity.get('T1595', 'Not Found')}")

# Calculate coverage percentage
tracked = sum(1 for m in maturity.values() if m != 'Not Tracked')
coverage = (tracked / len(maturity)) * 100
print(f"Coverage: {coverage:.1f}%")
```

## Custom Scripts

### Example 1: Initialize Multiple Projects

Create multiple ATT&CK tracking projects for different teams:

```python
from attack2jira import Attack2Jira

# Configuration
JIRA_URL = 'https://company.atlassian.net'
JIRA_USER = 'admin@company.com'
JIRA_TOKEN = 'your-api-token'

# Teams and their projects
teams = [
    {'name': 'Network Security Team', 'key': 'NETSEC'},
    {'name': 'Cloud Security Team', 'key': 'CLOUD'},
    {'name': 'Endpoint Security Team', 'key': 'ENDPOINT'}
]

# Initialize attack2jira once
a2j = Attack2Jira(url=JIRA_URL, username=JIRA_USER, password=JIRA_TOKEN)

# Create projects
for team in teams:
    print(f"Creating project for {team['name']}...")
    a2j.set_up_jira_automated(project=team['name'], key=team['key'])
    print(f"Project {team['key']} created successfully")
```

### Example 2: Coverage Analysis

Analyze coverage across your organization:

```python
from lib.jirahandler import JiraHandler

# Initialize
jira = JiraHandler()
jira.login(
    url='https://company.atlassian.net',
    username='user@company.com',
    apitoken='your-api-token'
)

# Get maturity data
maturity = jira.get_technique_maturity()

# Calculate statistics
total = len(maturity)
tracked = sum(1 for m in maturity.values() if m != 'Not Tracked')
initial = sum(1 for m in maturity.values() if m == 'Initial')
defined = sum(1 for m in maturity.values() if m == 'Defined')
resilient = sum(1 for m in maturity.values() if m == 'Resilient')
optimized = sum(1 for m in maturity.values() if m == 'Optimized')

print(f"Total Techniques: {total}")
print(f"Tracked: {tracked} ({tracked/total*100:.1f}%)")
print(f"  Initial: {initial}")
print(f"  Defined: {defined}")
print(f"  Resilient: {resilient}")
print(f"  Optimized: {optimized}")
```

### Example 3: Automated Weekly Reporting

Generate and email weekly coverage reports:

```python
import smtplib
from email.mime.text import MIMEText
from attack2jira import Attack2Jira

# Initialize
a2j = Attack2Jira(
    url='https://company.atlassian.net',
    username='user@company.com',
    password='api-token'
)

# Generate export
a2j.generate_json_layer(hideDisabled=False)

# Get maturity stats
maturity = a2j.jiraHandler.get_technique_maturity()
tracked = sum(1 for m in maturity.values() if m != 'Not Tracked')
coverage = (tracked / len(maturity)) * 100

# Create email report
msg = MIMEText(f"""
Weekly ATT&CK Coverage Report

Total Techniques: {len(maturity)}
Tracked: {tracked} ({coverage:.1f}%)

Latest export attached: attack2jira.json
""")

msg['Subject'] = f'ATT&CK Coverage Report - {coverage:.1f}%'
msg['From'] = 'security@company.com'
msg['To'] = 'team@company.com'

# Send email
smtp = smtplib.SMTP('smtp.company.com')
smtp.send_message(msg)
smtp.quit()
```

## JSON Export Format

The `attack2jira.json` export follows the ATT&CK Navigator Layer format.

### Structure

```json
{
  "name": "attack2jira Coverage",
  "version": "4.3",
  "domain": "enterprise-attack",
  "description": "ATT&CK coverage exported from Jira",
  "techniques": [
    {
      "techniqueID": "T1595",
      "color": "#81fc81",
      "score": 50,
      "comment": "",
      "enabled": true
    },
    {
      "techniqueID": "T1595.001",
      "color": "#49fc49",
      "score": 75,
      "comment": "",
      "enabled": true
    }
  ]
}
```

### Fields

- **name**: Layer name (always "attack2jira Coverage")
- **version**: Navigator version (4.3)
- **domain**: ATT&CK domain (enterprise-attack)
- **description**: Layer description
- **techniques**: Array of technique objects
  - **techniqueID**: Technique ID (e.g., "T1595")
  - **color**: Hex color based on maturity
  - **score**: Numeric score (0-100)
  - **comment**: Empty (reserved for future use)
  - **enabled**: False if hideDisabled=True and maturity="Not Tracked"

### Parsing Example

```python
import json

# Load export
with open('attack2jira.json', 'r') as f:
    layer = json.load(f)

# Extract techniques
for technique in layer['techniques']:
    tid = technique['techniqueID']
    color = technique['color']
    enabled = technique['enabled']

    if enabled:
        print(f"{tid}: {color}")
```

## Integration Examples

### Integrate with Detection Rules

Link techniques to detection rules in a SIEM:

```python
import yaml
from lib.jirahandler import JiraHandler

# Load detection rules (e.g., Sigma rules)
with open('sigma_rules.yml', 'r') as f:
    rules = yaml.safe_load(f)

# Get Jira issues
jira = JiraHandler()
jira.login(url=..., username=..., apitoken=...)

# Update Jira issues with rule links
for rule in rules:
    technique_id = rule.get('tags', {}).get('attack.technique')
    if technique_id:
        # Search for issue with matching technique ID
        # Add comment with rule link
        print(f"Linking {technique_id} to rule {rule['title']}")
```

### Dashboard Visualization

Create a dashboard showing coverage metrics:

```python
import matplotlib.pyplot as plt
from lib.jirahandler import JiraHandler

# Get maturity data
jira = JiraHandler()
jira.login(...)
maturity = jira.get_technique_maturity()

# Count by maturity level
levels = ['Not Tracked', 'Initial', 'Defined', 'Resilient', 'Optimized']
counts = [sum(1 for m in maturity.values() if m == level) for level in levels]

# Plot
plt.bar(levels, counts, color=['gray', '#e1fce1', '#81fc81', '#49fc49', '#03ad03'])
plt.xlabel('Maturity Level')
plt.ylabel('Number of Techniques')
plt.title('ATT&CK Coverage by Maturity')
plt.savefig('coverage_chart.png')
```

## Next Steps

- **Workflows**: See real-world integration patterns in [Workflows Guide](WORKFLOWS.md)
- **Troubleshooting**: Debug integration issues in [Troubleshooting Guide](TROUBLESHOOTING.md)
- **Architecture**: Understand internal design in [Architecture Guide](ARCHITECTURE.md)

For questions or issues, visit the [GitHub repository](https://github.com/mvelazco/attack2jira).
