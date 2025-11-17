# attack2jira Frequently Asked Questions

Common questions and answers about attack2jira.

## Table of Contents

- [General Questions](#general-questions)
- [Installation & Setup](#installation--setup)
- [Usage & Operations](#usage--operations)
- [Integration & Customization](#integration--customization)
- [Troubleshooting](#troubleshooting)
- [Advanced Topics](#advanced-topics)

## General Questions

### What is attack2jira?

attack2jira is a Python tool that automates the process of creating and managing MITRE ATT&CK coverage tracking within Atlassian Jira. It creates a complete Jira project with custom fields and issues for all ATT&CK techniques and sub-techniques, allowing security teams to track their detection maturity.

### Why use attack2jira instead of spreadsheets?

**Benefits over spreadsheets**:
- **Collaboration**: Multiple team members can update simultaneously
- **Workflows**: Leverage Jira's powerful workflow engine
- **Reporting**: Built-in dashboards and JQL queries
- **Integration**: Links to SIEM rules, incident tickets, and documentation
- **Automation**: Automated exports and reporting
- **Audit Trail**: Complete history of changes
- **Accessibility**: Web-based, accessible anywhere

Spreadsheets become unwieldy with 266+ techniques and lack collaboration features.

### Is attack2jira free?

**attack2jira itself**: Yes, open-source under BSD 3-Clause License.

**Dependencies**:
- **Jira Cloud**: Free tier available (up to 10 users), paid plans for larger teams
- **Python**: Free and open-source
- **MITRE ATT&CK API**: Free public access

**Total Cost**: Free for small teams (using Jira free tier), paid Jira subscription for production use.

### How often should I sync with MITRE ATT&CK?

**Initial Setup**: Run `initialize` once to create the project.

**Updates**: MITRE updates ATT&CK 2-4 times per year. Options:
1. **Re-initialize**: Create a new project with updated techniques (recommended if major changes)
2. **Manual Updates**: Add new techniques manually to existing project
3. **No Action**: Continue tracking existing techniques (most common)

**Exports**: Run `export` as frequently as needed for reporting (weekly, monthly, quarterly).

### Can I use attack2jira with Jira Server or Data Center?

**No**. attack2jira is designed exclusively for **Jira Cloud**. It uses Cloud-specific API endpoints (e.g., `/rest/simplified/latest/project`) that are not available in Jira Server or Data Center.

**Alternative**: Modify the source code to use Server/Data Center API endpoints (requires significant development effort).

### How many Jira issues does attack2jira create?

As of the latest ATT&CK release (v14), attack2jira creates **266+ issues**:
- **Parent Tasks**: ~200 (one per technique)
- **Sub-tasks**: ~66+ (one per sub-technique)

This number grows as MITRE adds new techniques and sub-techniques.

### Does attack2jira delete or modify existing Jira issues?

**No**. attack2jira:
- **Creates** new issues during initialization
- **Reads** existing issues during export
- **Never deletes** or modifies existing issues

All maturity updates and changes are made manually by users in Jira.

## Installation & Setup

### What operating systems are supported?

**Officially Tested**:
- Kali Linux 2018.4+
- Windows 10 1809+

**Also Compatible**:
- Ubuntu, Debian, CentOS, Fedora, Arch Linux (any modern Linux)
- macOS 10.14+
- Windows Server 2016+

Any OS with Python 3.6+ should work.

### Do I need admin access to Jira?

**Yes**. attack2jira requires **Jira Administrator** global permission to:
- Create projects
- Create custom fields
- Modify screens and field configurations
- Create issues

Without admin access, initialization will fail with 403 Forbidden errors.

### Can I run attack2jira offline?

**No**. attack2jira requires internet connectivity to:
- Authenticate with Jira Cloud (HTTPS API calls)
- Fetch ATT&CK data from MITRE's TAXII server
- Create and read Jira issues

No offline mode is currently supported.

### How long does initialization take?

**Typical Duration**: 10-20 minutes

**Factors Affecting Speed**:
- Network latency to Jira and MITRE APIs
- Jira Cloud performance (varies by time of day)
- API rate limits

Slower networks or rate limiting may extend this to 30+ minutes.

## Usage & Operations

### Can I change the project name or key after initialization?

**Project Name**: Yes, change in Jira Project Settings → Details → Edit Name.

**Project Key**: No, Jira does not allow changing project keys after creation. You must:
1. Create a new project with the desired key
2. Re-run `attack2jira.py -a initialize -k NEW_KEY`
3. Optionally delete the old project

### Can I modify custom field options?

**Yes**. After initialization, you can modify custom fields in Jira:
1. Settings → Issues → Custom Fields
2. Find the field (e.g., "Maturity")
3. Click "..." → Configure → Edit Options
4. Add, remove, or reorder options

**Warning**: Changing field names or IDs may break the export functionality.

### How do I update an existing project with new ATT&CK techniques?

**Option 1: Manual Addition**
1. Identify new techniques from [attack.mitre.org](https://attack.mitre.org)
2. Manually create Jira issues for new techniques
3. Populate custom fields (Id, Tactic, Maturity, etc.)

**Option 2: Create New Project**
1. Initialize a new project with a different key
2. Migrate maturity data from old project
3. Archive old project

**Note**: attack2jira does not support incremental updates to existing projects.

### Can I track multiple ATT&CK domains (Enterprise, Mobile, ICS)?

**Current Support**: Enterprise ATT&CK only (default).

**Workaround**: Initialize separate projects for different domains:
- Project "ATT&CK Enterprise" (key: ATTACK)
- Project "ATT&CK Mobile" (key: MOBILE)
- Project "ATT&CK ICS" (key: ICS)

Modify the code to use different ATT&CK data sources via `attackcti`.

### How do I export data for ATT&CK Navigator?

```bash
python3 attack2jira.py \
  -url https://company.atlassian.net \
  -u user@company.com \
  -a export
```

**Output**: `attack2jira.json` in the current directory.

**Upload to Navigator**:
1. Navigate to [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/)
2. Click "+" → "Open Existing Layer"
3. Click "Upload from local"
4. Select `attack2jira.json`
5. View your coverage heat map

### Can I export to formats other than Navigator JSON?

**Currently**: Only Navigator JSON format is supported.

**Alternatives**:
- Use Jira's built-in export (CSV, Excel) for issue lists
- Write custom scripts to parse Navigator JSON (see [API Reference](API_REFERENCE.md))
- Query Jira REST API directly for custom reporting

## Integration & Customization

### Can I integrate attack2jira with my SIEM?

**Yes**. Common integration patterns:

**1. Link Detection Rules to Jira Issues**
- Store detection rules in Git (Sigma, Splunk, Elastic)
- Add links to Jira issue descriptions or comments
- Example: "Detection rule: https://github.com/company/rules/T1595.yml"

**2. Automate Maturity Updates**
- Use Jira REST API to update Maturity field when rules are deployed
- Trigger via CI/CD pipeline

**3. Incident Linking**
- Link Jira issues to SIEM incidents
- Track which techniques are being exploited in the wild

See [Workflows Guide](WORKFLOWS.md) for detailed examples.

### Can I contribute improvements to attack2jira?

**Yes!** attack2jira is open-source (BSD 3-Clause License).

**How to Contribute**:
1. Fork the [GitHub repository](https://github.com/mvelazco/attack2jira)
2. Create a feature branch
3. Make your changes
4. Submit a pull request
5. Describe your changes and use case

**Areas for Contribution**:
- Docker support
- Incremental updates
- Additional export formats
- Improved error handling
- Unit tests

### Can I customize the maturity levels?

**Yes**. Modify `lib/jirahandler.py`:

```python
def add_custom_field_options(self):
    # Change maturity levels
    maturity_levels = [
        "Not Covered",      # Changed from "Not Tracked"
        "Basic",            # Changed from "Initial"
        "Intermediate",     # Changed from "Defined"
        "Advanced",         # Changed from "Resilient"
        "Expert"            # Changed from "Optimized"
    ]
```

Also update the color mapping in `attack2jira.py`:
```python
maturity_level_color = {
    "Not Covered": "#DCDCDC",
    "Basic": "#e1fce1",
    # ... etc.
}
```

### How do I schedule automated exports?

**Linux/macOS (cron)**:
```cron
# Weekly export every Monday at 9 AM
0 9 * * 1 /home/user/attack2jira/run-export.sh
```

**Windows (Task Scheduler)**:
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., weekly)
4. Action: Start a program (`python.exe`)
5. Arguments: `attack2jira.py -url ... -u ... -a export`

See [Deployment Guide](DEPLOYMENT_GUIDE.md) for detailed automation setup.

## Troubleshooting

### Why am I getting "401 Unauthorized" errors?

**Common Causes**:
1. Using Jira password instead of API token
2. Incorrect email address
3. Expired API token

**Solution**:
1. Generate a new API token: [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Verify your email address is correct
3. Use the token (not password) when prompted

See [Troubleshooting Guide](TROUBLESHOOTING.md#authentication-errors) for detailed steps.

### Why is initialization taking so long or hanging?

**Normal**: 10-20 minutes is typical for creating 266+ issues.

**If > 30 minutes**:
- Check network connectivity
- Monitor progress output (should print each issue created)
- Verify Jira Cloud status: [Atlassian Status](https://status.atlassian.com)
- Cancel and retry during off-peak hours

### What if some issues failed to create?

attack2jira continues processing even if individual issues fail.

**Check Output**:
```
[ERROR] Failed to create issue for T1234: Network timeout
[SUCCESS] Created issue ATTACK-42 for T1235
```

**Solution**:
1. Note which techniques failed
2. Create them manually in Jira, or
3. Re-run initialization (Jira will reject duplicates, only creating missing issues)

### Can I uninstall attack2jira?

**Yes**. To remove:

**1. Delete Repository**:
```bash
rm -rf /path/to/attack2jira
```

**2. Remove Python Dependencies (optional)**:
```bash
pip3 uninstall attackcti
```

**3. Delete Jira Project (optional)**:
1. Log in to Jira
2. Project Settings → Move to trash
3. Permanently delete from trash

See [Installation Guide](INSTALLATION_GUIDE.md#uninstallation) for details.

## Advanced Topics

### Can I run attack2jira in Docker?

**Currently**: No official Docker image is available.

**Custom Docker Setup**:
See [Deployment Guide](DEPLOYMENT_GUIDE.md#docker-deployment) for a reference Dockerfile and instructions.

**Planned**: Official Docker support is on the roadmap.

### How do I track coverage for multiple business units?

**Option 1: Multiple Projects**
- Initialize separate projects per business unit
- Example: ATTACK-NA (North America), ATTACK-EU (Europe)

**Option 2: Components**
- Use Jira Components within a single project
- Tag issues with component (e.g., "NA", "EU")

**Option 3: Labels**
- Use labels to indicate ownership
- Filter by label in JQL queries

### Can I use attack2jira with Jira API v3?

**Current**: attack2jira uses Jira REST API v2.

**Future**: Jira v3 API offers improved performance but requires code changes. Contributions welcome!

### What's the performance impact on my Jira instance?

**Initialization**: Creates 266+ issues, which is well within Jira Cloud limits (thousands of issues supported).

**Ongoing**: Minimal impact. Jira queries and exports are standard operations.

**No Performance Issues Reported**: attack2jira has been used by organizations with thousands of Jira issues without problems.

### How do I version control my exports?

```bash
# Create dated exports
mkdir -p exports
mv attack2jira.json exports/attack2jira-$(date +%Y-%m-%d).json

# Initialize git
cd exports
git init
git add .
git commit -m "Initial coverage export"

# Track changes over time
git log --oneline
git diff attack2jira-2024-01-01.json attack2jira-2024-02-01.json
```

See [Workflows Guide](WORKFLOWS.md#best-practices-across-all-workflows) for version control examples.

## Still Have Questions?

- **Documentation**: Browse the complete [documentation suite](README.md)
- **GitHub Issues**: Search or open an issue at [github.com/mvelazco/attack2jira](https://github.com/mvelazco/attack2jira/issues)
- **ATT&CKCon Talk**: Watch the [original presentation](https://www.youtube.com/watch?v=hrzR8TpnjAw)
- **Blog Post**: Read the [introduction blog post](https://medium.com/@mvelazco/tracking-and-measuring-att-ck-coverage-with-attack2jira-fe700e2a1654)

For additional help, consult the [Troubleshooting Guide](TROUBLESHOOTING.md) or reach out to the community via GitHub.
