# attack2jira User Guide

This comprehensive guide covers everything you need to know about using attack2jira effectively in your security operations.

## Table of Contents

- [Overview](#overview)
- [Command Reference](#command-reference)
- [Configuration](#configuration)
- [Syncing Techniques](#syncing-techniques)
- [Exporting Navigator JSON](#exporting-navigator-json)
- [Working with Jira](#working-with-jira)
- [Customization Options](#customization-options)
- [Tips & Tricks](#tips--tricks)

## Overview

attack2jira is a command-line tool that synchronizes MITRE ATT&CK Framework data with Atlassian Jira. It consists of two primary modes of operation:

- **Initialize Mode**: Creates a complete Jira project with all ATT&CK techniques and sub-techniques
- **Export Mode**: Extracts maturity data from Jira and generates ATT&CK Navigator JSON layers

The tool is designed to be simple yet powerful, requiring minimal configuration while providing comprehensive ATT&CK coverage tracking.

### Typical Workflow

1. **Initial Setup**: Run `initialize` to create your tracking project (one-time)
2. **Daily Operations**: Teams work in Jira, updating maturity levels and adding detection documentation
3. **Reporting**: Run `export` periodically to generate visualizations for stakeholders
4. **Iteration**: Continue refining detections and tracking progress over time

## Command Reference

### Help Command

Display all available options:

```bash
python3 attack2jira.py -h
```

Or:

```bash
python3 attack2jira.py --help
```

**Output**:
```
usage: attack2jira.py [-h] -url URL -u U -a {initialize,export} [-p P] [-k K] [-hide]

optional arguments:
  -h, --help            show this help message and exit
  -url URL              Jira Cloud instance URL
  -u U                  Jira username (email)
  -a {initialize,export}
                        Action to perform
  -p P                  Project name (default: Mitre Attack Framework)
  -k K                  Project key (default: ATTACK)
  -hide                 Hide 'Not Tracked' techniques in export
```

### Initialize Command

Creates a new Jira project with complete ATT&CK coverage.

**Basic Syntax**:
```bash
python3 attack2jira.py -url <JIRA_URL> -u <USERNAME> -a initialize
```

**Required Parameters**:
- `-url`: Your Jira Cloud instance URL (e.g., `https://company.atlassian.net`)
- `-u`: Your Jira username/email address
- `-a initialize`: Specifies the initialize action

**Optional Parameters**:
- `-p`: Custom project name (default: "Mitre Attack Framework")
- `-k`: Custom project key (default: "ATTACK")

**Example - Default Project**:
```bash
python3 attack2jira.py \
  -url https://acmecorp.atlassian.net \
  -u security-team@acmecorp.com \
  -a initialize
```

This creates a project named "Mitre Attack Framework" with key "ATTACK".

**Example - Custom Project**:
```bash
python3 attack2jira.py \
  -url https://acmecorp.atlassian.net \
  -u security-team@acmecorp.com \
  -a initialize \
  -p "Purple Team Coverage Tracker" \
  -k PURPLE
```

This creates a project named "Purple Team Coverage Tracker" with key "PURPLE" (issues will be PURPLE-1, PURPLE-2, etc.).

**What Gets Created**:
1. New Jira Software project
2. 6 custom fields (Id, Tactic, Maturity, Url, Datasources, Sub-Technique of)
3. Custom field options populated from ATT&CK API
4. Configured issue screens with custom fields visible
5. 266+ Jira issues:
   - Parent Tasks for techniques (e.g., T1595 - Active Scanning)
   - Child Sub-tasks for sub-techniques (e.g., T1595.001 - Scanning IP Blocks)

**Duration**: Typically 5-15 minutes depending on network speed.

**Important Notes**:
- Requires Jira admin privileges
- Cannot be run twice with the same project key (Jira will reject duplicate projects)
- You'll be prompted securely for your API token (password input hidden)
- The tool fetches fresh ATT&CK data each run, ensuring you get the latest techniques

### Export Command

Exports maturity levels from Jira to ATT&CK Navigator JSON format.

**Basic Syntax**:
```bash
python3 attack2jira.py -url <JIRA_URL> -u <USERNAME> -a export
```

**Required Parameters**:
- `-url`: Your Jira Cloud instance URL
- `-u`: Your Jira username/email address
- `-a export`: Specifies the export action

**Optional Parameters**:
- `-hide`: Hide techniques with "Not Tracked" maturity in the visualization

**Example - Standard Export**:
```bash
python3 attack2jira.py \
  -url https://acmecorp.atlassian.net \
  -u security-team@acmecorp.com \
  -a export
```

Generates `attack2jira.json` in the current directory with all techniques.

**Example - Hide Untracked Techniques**:
```bash
python3 attack2jira.py \
  -url https://acmecorp.atlassian.net \
  -u security-team@acmecorp.com \
  -a export \
  -hide
```

Generates `attack2jira.json` with "Not Tracked" techniques disabled (grayed out) in the Navigator view.

**Output File**:
- **Filename**: `attack2jira.json`
- **Location**: Current working directory
- **Format**: ATT&CK Navigator Layer JSON
- **Usage**: Upload to [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/) to visualize

**Color Coding**:
Techniques are color-coded based on maturity level:
- **Not Tracked**: Gray (#DCDCDC) - No coverage
- **Initial**: Light green (#e1fce1) - Basic detection exists
- **Defined**: Medium green (#81fc81) - Documented, tested detection
- **Resilient**: Darker green (#49fc49) - Redundant detections, tuned
- **Optimized**: Darkest green (#03ad03) - Automated response, continuous improvement

**Duration**: Typically 30 seconds to 2 minutes.

**Important Notes**:
- Only reads data from Jira project with key "ATTACK" (hardcoded limitation in current version)
- Does not modify Jira data—read-only operation
- Can be run as frequently as needed without side effects

## Configuration

attack2jira uses minimal configuration, primarily relying on command-line arguments.

### Jira Instance URL

**Format**: `https://yoursite.atlassian.net`

**Common Mistakes**:
- ❌ `http://yoursite.atlassian.net` (wrong protocol)
- ❌ `https://yoursite.atlassian.net/` (trailing slash may cause issues)
- ❌ `yoursite.atlassian.net` (missing protocol)
- ✅ `https://yoursite.atlassian.net` (correct)

**Finding Your URL**:
1. Log in to Jira
2. Look at your browser's address bar
3. Copy everything up to `.net` (e.g., `https://acme.atlassian.net`)

### Authentication

attack2jira uses **API tokens** for authentication, not passwords.

**Creating an API Token**:
1. Navigate to [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click "Create API token"
3. Give it a label (e.g., "attack2jira")
4. Copy the token immediately (you can't view it again)
5. Store it securely (password manager recommended)

**Using the API Token**:
When you run attack2jira, you'll be prompted:
```
Enter API token:
```

Paste your token (input is hidden for security) and press Enter.

**Security Best Practices**:
- Never commit API tokens to version control
- Rotate tokens periodically
- Use a dedicated service account if running in production
- Revoke tokens immediately if compromised

### Project Configuration

**Project Name** (`-p`):
- Displayed in Jira UI
- Can contain spaces and special characters
- Default: "Mitre Attack Framework"
- Examples: "ATT&CK Coverage", "Security Detection Tracker", "Purple Team Matrix"

**Project Key** (`-k`):
- Short code (typically 2-10 uppercase letters)
- Used in issue keys (e.g., ATTACK-1, ATTACK-2)
- Cannot contain spaces or special characters
- Must be unique across your Jira instance
- Default: "ATTACK"
- Examples: "ATK", "SECOPS", "PURPLE", "DETECT"

**Choosing a Good Project Key**:
- Keep it short (3-6 characters ideal)
- Make it memorable and recognizable
- Avoid conflicts with existing projects
- Use uppercase letters only

## Syncing Techniques

attack2jira automatically handles two syncing approaches:

### Flat Structure (Deprecated)

The older method created individual issues for techniques only, without sub-techniques. This method is still in the codebase (`create_attack_techniques()`) but is no longer used.

### Hierarchical Structure (Current)

The current approach creates a parent-child relationship:

**Parent Issues (Techniques)**:
- **Type**: Task
- **Summary**: Technique name without ID (e.g., "Active Scanning")
- **Description**: Full description from MITRE
- **Custom Fields**:
  - **Id**: Technique ID (e.g., T1595)
  - **Tactic**: ATT&CK tactic (e.g., Reconnaissance)
  - **Maturity**: Dropdown for tracking detection maturity
  - **Url**: Link to technique on attack.mitre.org
  - **Datasources**: Multi-select of available data sources

**Child Issues (Sub-techniques)**:
- **Type**: Sub-task (linked to parent)
- **Summary**: Sub-technique name (e.g., "Scanning IP Blocks")
- **Description**: Full description from MITRE
- **Custom Fields**: Same as parent, plus:
  - **Sub-Technique of**: Reference to parent technique ID

**Example Structure in Jira**:
```
ATTACK-42 (Task)
├─ Title: Active Scanning
├─ Id: T1595
├─ Tactic: Reconnaissance
└─ Sub-tasks:
   ├─ ATTACK-43: Scanning IP Blocks (T1595.001)
   ├─ ATTACK-44: Vulnerability Scanning (T1595.002)
   └─ ATTACK-45: Wordlist Scanning (T1595.003)
```

**Benefits**:
- Logical grouping of related techniques
- Easy filtering by parent technique
- Clear visualization of technique families
- Aligns with ATT&CK's hierarchical structure

### Data Sources

attack2jira automatically populates the "Datasources" field from MITRE's API. Data sources represent the types of information needed to detect a technique.

**Common Data Sources**:
- Process monitoring
- Network traffic
- Windows event logs
- File monitoring
- Authentication logs
- Cloud API logs
- Email gateway
- DNS records

These are populated as multi-select options, allowing you to tag which data sources your organization uses to detect each technique.

## Exporting Navigator JSON

The export functionality transforms Jira data into a visual heat map.

### Running an Export

```bash
python3 attack2jira.py -url https://yoursite.atlassian.net -u user@domain.com -a export
```

### Viewing the Export

1. **Generate the export**: Run the export command
2. **Locate the file**: `attack2jira.json` in your current directory
3. **Open Navigator**: Navigate to [https://mitre-attack.github.io/attack-navigator/](https://mitre-attack.github.io/attack-navigator/)
4. **Upload the layer**:
   - Click the "+" button (top left)
   - Select "Open Existing Layer"
   - Click "Upload from local"
   - Select `attack2jira.json`
5. **View your coverage**: The matrix displays with color-coded techniques based on maturity

![Navigator Screenshot: Shows the ATT&CK Navigator matrix with techniques color-coded from light green (Initial) to dark green (Optimized), with gray representing Not Tracked techniques]

### Interpreting the Visualization

**Color Intensity**: Darker green = higher maturity
**Gray Techniques**: Not tracked or disabled (with `-hide` flag)
**Technique Details**: Click any technique to see its metadata

### Sharing Exports

The JSON file can be:
- Shared via email or file sharing
- Committed to version control for historical tracking
- Uploaded to internal wikis or documentation
- Presented in executive reports or board meetings

### Scheduled Exports

For automated reporting, create a cron job or scheduled task:

**Linux/macOS Cron Example**:
```bash
# Export weekly on Mondays at 9 AM
0 9 * * 1 cd /path/to/attack2jira && /usr/bin/python3 attack2jira.py -url https://site.atlassian.net -u user@domain.com -a export
```

**Note**: You'll need to handle API token input non-interactively (see [Deployment Guide](DEPLOYMENT_GUIDE.md) for automated authentication).

## Working with Jira

Once your project is created, leverage Jira's features for effective tracking.

### Updating Maturity Levels

1. Navigate to your ATTACK project
2. Open an issue (e.g., ATTACK-1)
3. Locate the **Maturity** custom field
4. Select the appropriate level:
   - **Not Tracked**: No detection capability
   - **Initial**: Basic detection exists but not formalized
   - **Defined**: Detection is documented, tested, and reliable
   - **Resilient**: Multiple detection methods, tuned to reduce false positives
   - **Optimized**: Automated alerting, response runbooks, continuous improvement

### Best Practices for Tracking

**Assign Ownership**:
- Assign each technique to a team member responsible for detection coverage
- Use Jira's assignment feature for accountability

**Document Detection Logic**:
- Add comments describing how you detect the technique
- Include SIEM queries, EDR rules, or detection logic
- Link to detection rule repositories (e.g., Sigma rules, Splunk queries)

**Use Labels**:
- Tag techniques by priority: `high-priority`, `low-priority`
- Tag by environment: `cloud`, `on-prem`, `hybrid`
- Tag by coverage: `full-coverage`, `partial-coverage`, `no-coverage`

**Create Workflows**:
- Define transitions: Not Started → In Progress → Testing → Deployed → Optimized
- Automate maturity updates based on workflow state

**Link Related Issues**:
- Link techniques to detection engineering tasks
- Link to incident response playbooks
- Connect to related vulnerability management issues

### Filtering and Searching

**JQL Examples**:

Find all techniques without coverage:
```
project = ATTACK AND Maturity = "Not Tracked"
```

Find all reconnaissance techniques:
```
project = ATTACK AND Tactic = "reconnaissance"
```

Find high-maturity detections:
```
project = ATTACK AND Maturity IN ("Resilient", "Optimized")
```

Find sub-techniques only:
```
project = ATTACK AND issuetype = Sub-task
```

Find techniques assigned to you:
```
project = ATTACK AND assignee = currentUser()
```

### Creating Dashboards

Build Jira dashboards to visualize progress:

**Gadgets to Include**:
1. **Pie Chart**: Maturity distribution
2. **Filter Results**: Techniques by tactic
3. **Assigned to Me**: Personal coverage responsibility
4. **Recently Updated**: Track team activity
5. **Two Dimensional Filter Statistics**: Tactic vs. Maturity matrix

## Customization Options

### Custom Field Modifications

You can modify custom field options directly in Jira after creation:

**Adding Maturity Levels**:
1. Navigate to Jira Settings → Issues → Custom Fields
2. Find the "Maturity" field
3. Click "..." → Configure → Edit Options
4. Add new values (e.g., "In Development", "Testing")

**Warning**: Modifying field IDs or names may break the export functionality.

### Custom Tactics

If MITRE adds new tactics, re-run the initialization or manually add them:

1. Navigate to Jira Settings → Issues → Custom Fields
2. Find the "Tactic" field
3. Add new tactic options

### Project Permissions

Configure who can view and edit your ATTACK project:

1. Go to Project Settings → Permissions
2. Adjust role-based permissions
3. Grant view access to stakeholders
4. Restrict edit access to detection engineers

### Notification Schemes

Set up notifications for:
- New technique assignments
- Maturity level changes
- Comments added to issues

## Tips & Tricks

### Bulk Editing

Update multiple techniques at once:
1. Search for techniques: `project = ATTACK AND Tactic = "initial-access"`
2. Select all issues (checkbox in top-left)
3. Click "..." → Bulk Change → Edit Issues
4. Update Maturity field for all at once

### Exporting to Excel

Jira can export issue lists to CSV/Excel for offline analysis:
1. Run a JQL search
2. Click "Export" (top-right)
3. Choose Excel CSV or CSV (current fields)
4. Open in Excel for pivot tables and charts

### Version Control for Exports

Track coverage changes over time:
```bash
# Create dated exports
python3 attack2jira.py -url ... -u ... -a export
mv attack2jira.json exports/attack2jira-$(date +%Y-%m-%d).json

# Commit to git
git add exports/
git commit -m "Coverage export for $(date +%Y-%m-%d)"
```

### Integration with Detection Repositories

Link Jira issues to detection rules in GitHub:
1. Store detection rules in a GitHub repository
2. Name rules by technique ID (e.g., `T1595_active_scanning.yml`)
3. Add GitHub links to Jira issue descriptions
4. Use GitHub-Jira integration for automatic linking

### Performance Optimization

For faster export runs:
- Run during off-peak hours to avoid Jira rate limits
- Use fast, stable network connections
- Consider caching exports if running frequently

### Multi-Team Usage

If multiple teams track different ATT&CK areas:
1. Initialize multiple projects with different keys (e.g., ATTACK-NET, ATTACK-CLOUD)
2. Use Jira Components to segment within one project
3. Use Labels to indicate team ownership

### Custom Scripts

The export JSON can be parsed by custom scripts:
```python
import json

with open('attack2jira.json', 'r') as f:
    data = json.load(f)
    techniques = data['techniques']

    # Calculate coverage percentage
    tracked = sum(1 for t in techniques if t.get('score', 0) > 0)
    total = len(techniques)
    coverage = (tracked / total) * 100
    print(f"Coverage: {coverage:.1f}%")
```

See [API Reference](API_REFERENCE.md) for details on the JSON structure.

## Next Steps

- **Advanced Workflows**: See [Workflows Guide](WORKFLOWS.md) for real-world usage patterns
- **Troubleshooting**: If you encounter issues, check [Troubleshooting Guide](TROUBLESHOOTING.md)
- **API Integration**: Learn to script with attack2jira in [API Reference](API_REFERENCE.md)
- **Production Deployment**: Scale up with [Deployment Guide](DEPLOYMENT_GUIDE.md)

For questions or issues, visit the [GitHub repository](https://github.com/mvelazco/attack2jira) or consult the [FAQ](FAQ.md).
