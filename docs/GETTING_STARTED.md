# Getting Started with attack2jira

Welcome to attack2jira! This guide will help you get up and running quickly with automated MITRE ATT&CK coverage tracking in Jira.

## Table of Contents

- [What is attack2jira?](#what-is-attack2jira)
- [System Requirements](#system-requirements)
- [Installation Methods](#installation-methods)
- [First-Time Setup](#first-time-setup)
- [Running Your First Sync](#running-your-first-sync)
- [Common First-Time Issues](#common-first-time-issues)
- [Next Steps](#next-steps)

## What is attack2jira?

attack2jira is an automation tool that helps security teams track their organization's defensive capabilities against the MITRE ATT&CK Framework within Jira. It eliminates the need for manual spreadsheet management and provides a structured, scalable approach to measuring security posture.

### Key Benefits

**Automated Project Setup**: Creates a complete Jira project structure with custom fields, screens, and workflows optimized for ATT&CK tracking in a single command.

**Complete Coverage**: Automatically generates Jira issues for all 266+ ATT&CK techniques and sub-techniques, ensuring nothing falls through the cracks.

**Maturity Tracking**: Track detection maturity levels (Not Tracked, Initial, Defined, Resilient, Optimized) for each technique, allowing you to measure progress over time.

**Visualization Export**: Export your coverage data to ATT&CK Navigator JSON format, creating beautiful heat maps that show your organization's defensive posture at a glance.

**Collaborative Workflow**: Leverage Jira's powerful collaboration features—assignments, comments, workflows, and notifications—to coordinate security team efforts.

### How It Works

attack2jira bridges the gap between the MITRE ATT&CK Framework and Atlassian Jira:

1. **Data Collection**: Fetches the latest ATT&CK techniques and metadata from the MITRE ATT&CK API using the attackcti Python library
2. **Project Creation**: Creates a Jira project with custom fields tailored for tracking ATT&CK coverage
3. **Issue Generation**: Creates structured Jira issues (Tasks for techniques, Sub-tasks for sub-techniques) with complete metadata
4. **Tracking**: Security teams update maturity levels and add notes as they implement detections
5. **Reporting**: Export data back to ATT&CK Navigator format to visualize coverage and share with stakeholders

## System Requirements

### Operating System
- **Linux**: Kali Linux 2018.4+ (tested), Ubuntu 18.04+, Debian 9+
- **macOS**: macOS 10.14+
- **Windows**: Windows 10 1809+, Windows Server 2016+

### Python
- **Python 3.6** or higher (Python 3.7+ recommended)
- pip3 package manager
- virtualenv (recommended for isolated environments)

### Jira Requirements
- **Jira Cloud** instance (Jira Software)
- **Admin access** to create projects and custom fields
- **API Token** for authentication
- Free trial accounts are supported (up to 10 users)

### Network Requirements
- Internet connectivity to reach:
  - Your Jira Cloud instance (*.atlassian.net)
  - MITRE ATT&CK API (cti-taxii.mitre.org)
- HTTPS/443 outbound access

### Disk Space
- Approximately 50 MB for the tool and dependencies
- Minimal storage for generated JSON exports

## Installation Methods

Choose the installation method that best fits your environment:

### Method 1: Local Installation (Recommended for Beginners)

This method installs attack2jira directly on your system without isolation.

```bash
# Clone the repository
git clone https://github.com/mvelazco/attack2jira.git

# Navigate to the directory
cd attack2jira

# Install dependencies
pip3 install -r requirements.txt
```

**Pros**: Simple, quick setup
**Cons**: May conflict with other Python packages on your system

### Method 2: Virtual Environment (Recommended for Production)

Virtual environments isolate attack2jira dependencies from other Python projects.

```bash
# Clone the repository
git clone https://github.com/mvelazco/attack2jira.git
cd attack2jira

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip3 install -r requirements.txt
```

**Pros**: Isolated dependencies, no conflicts, recommended best practice
**Cons**: Requires activating the virtual environment before each use

### Method 3: Docker (Coming Soon)

Docker support is planned for a future release. This will provide the ultimate in portability and isolation.

## First-Time Setup

Before running attack2jira, you need to prepare your Jira environment and gather credentials.

### Step 1: Set Up Jira Cloud

If you don't already have a Jira Cloud instance:

1. Visit [Atlassian's Jira free trial page](https://www.atlassian.com/software/jira/free)
2. Sign up for a free Jira Software Cloud instance (supports up to 10 users)
3. Choose a site name (e.g., `yourcompany.atlassian.net`)
4. Complete the setup wizard
5. Ensure you have admin access to the instance

### Step 2: Generate API Token

Jira Cloud uses API tokens instead of passwords for programmatic access.

1. Log in to your Jira Cloud instance
2. Click your profile icon (top right) → **Account Settings**
3. Navigate to **Security** → **API tokens**
4. Click **Create API token**
5. Give it a descriptive name (e.g., "attack2jira")
6. Click **Create**
7. **Copy the token immediately** (you won't be able to see it again)
8. Store it securely (password manager recommended)

![API Token Creation Screenshot: Shows the Atlassian account security page with the "Create API token" dialog box where users enter a label and receive a generated token]

### Step 3: Verify Credentials

Test your credentials before running the full initialization:

```bash
# Test authentication (this will prompt for password/API token)
python3 attack2jira.py -url https://yourcompany.atlassian.net -u your-email@domain.com -a export
```

If authentication fails, you'll see an error immediately. If it succeeds but reports no project found, that's expected—you haven't created the ATTACK project yet.

### Step 4: Understand Project Naming

attack2jira creates a Jira project with:

- **Project Name**: Friendly name displayed in Jira (default: "Mitre Attack Framework")
- **Project Key**: Short code used in issue keys (default: "ATTACK")

For example, with the default key "ATTACK", issues will be named ATTACK-1, ATTACK-2, etc.

You can customize these during initialization with the `-p` and `-k` flags.

## Running Your First Sync

Now you're ready to create your ATT&CK tracking environment!

### Basic Initialization

Run the initialize command to create the project and all issues:

```bash
python3 attack2jira.py \
  -url https://yourcompany.atlassian.net \
  -u your-email@domain.com \
  -a initialize
```

You'll be prompted to enter your API token securely (input is hidden).

### What Happens During Initialization

The tool will perform these steps sequentially:

1. **Authenticate**: Validates your credentials with Jira
2. **Create Project**: Sets up a new Jira Software project named "Mitre Attack Framework" with key "ATTACK"
3. **Create Custom Fields**: Adds 6 specialized fields (Id, Tactic, Maturity, Url, Datasources, Sub-Technique of)
4. **Populate Field Options**: Retrieves tactics and data sources from MITRE ATT&CK API and populates dropdown values
5. **Configure Screens**: Adds custom fields to issue screens for visibility
6. **Hide Unnecessary Fields**: Removes clutter from the UI (time tracking, versions, etc.)
7. **Fetch ATT&CK Data**: Downloads the latest techniques and sub-techniques from MITRE
8. **Create Issues**: Generates 266+ Jira issues (Tasks for techniques, Sub-tasks for sub-techniques)

**Expected Duration**: 5-15 minutes depending on network speed and Jira response times

### Custom Project Names

To use custom project names and keys:

```bash
python3 attack2jira.py \
  -url https://yourcompany.atlassian.net \
  -u your-email@domain.com \
  -a initialize \
  -p "Security Coverage Tracker" \
  -k SECOV
```

This creates a project named "Security Coverage Tracker" with issue keys like SECOV-1, SECOV-2, etc.

### Monitoring Progress

The tool provides real-time output showing progress:

```
[INFO] Authenticating to Jira...
[SUCCESS] Authentication successful
[INFO] Creating project...
[SUCCESS] Project 'ATTACK' created
[INFO] Creating custom fields...
[SUCCESS] Custom field 'Maturity' created
...
[INFO] Creating technique: T1595 - Active Scanning
[SUCCESS] Created issue ATTACK-1
...
```

If you see errors for specific issues, the tool will continue processing. Review the error messages after completion.

### Verification

After initialization completes:

1. Log in to your Jira instance
2. Navigate to Projects → ATTACK (or your custom key)
3. You should see 266+ issues in the backlog
4. Open a few issues to verify custom fields are populated
5. Check that techniques have sub-tasks for sub-techniques

![Jira Project Screenshot: Shows the ATTACK project board with multiple technique issues listed, displaying custom fields like Tactic, Maturity, and Technique ID in the issue view]

## Common First-Time Issues

### Issue: Authentication Failed (401 Unauthorized)

**Symptoms**: Error message "401 Client Error: Unauthorized"

**Causes**:
- Using password instead of API token
- Incorrect email address
- Expired or invalid API token
- Incorrect Jira URL

**Solutions**:
1. Verify you're using an API token, not your password
2. Double-check your email address (case-sensitive)
3. Generate a new API token and try again
4. Ensure Jira URL is correct format: `https://yoursite.atlassian.net` (no trailing slash)

### Issue: Project Already Exists (400 Bad Request)

**Symptoms**: Error message "A project with that name already exists"

**Causes**:
- You previously ran initialization with the same project key
- Another project is using the key "ATTACK"

**Solutions**:
1. Use a different project key with `-k` flag: `python3 attack2jira.py ... -k ATTACK2`
2. Delete the existing project in Jira if you want to recreate it (be careful—this is destructive)
3. Use the existing project and run export instead of initialize

### Issue: Network Connection Errors

**Symptoms**: Timeouts, connection refused, SSL errors

**Causes**:
- Firewall blocking HTTPS traffic
- Corporate proxy intercepting SSL
- Incorrect Jira URL
- Internet connectivity issues

**Solutions**:
1. Test connectivity: `curl -I https://yoursite.atlassian.net`
2. Check firewall settings allow HTTPS to *.atlassian.net
3. If behind a corporate proxy, configure proxy settings in your environment
4. Verify DNS resolution: `nslookup yoursite.atlassian.net`

### Issue: Permission Denied (403 Forbidden)

**Symptoms**: Error message "403 Client Error: Forbidden"

**Causes**:
- User account lacks admin privileges
- Free trial limitations
- Project creation disabled by Jira admin

**Solutions**:
1. Verify you have Jira admin permissions
2. Ask your Jira administrator to grant project creation rights
3. If using a free trial, ensure you're the account owner

### Issue: Slow Performance or Timeouts

**Symptoms**: Takes longer than 30 minutes, times out mid-process

**Causes**:
- Slow network connection
- Jira rate limiting
- Large number of API calls

**Solutions**:
1. Be patient—creating 266+ issues takes time
2. Run from a machine with stable, fast internet
3. If it times out, the tool will skip failed issues; review logs and create them manually or re-run
4. Consider running during off-peak hours

### Issue: SSL Certificate Warnings

**Symptoms**: Warning messages about SSL certificate verification

**Note**: The tool currently disables SSL warnings for convenience in test environments. In production, you should enable SSL verification by modifying the code.

**If you see legitimate SSL errors**:
1. Verify the Jira URL is correct (https://, not http://)
2. Check for man-in-the-middle proxies
3. Update your Python SSL certificates: `pip3 install --upgrade certifi`

## Next Steps

Congratulations! You've successfully set up attack2jira. Here's what to do next:

### 1. Explore Your New Project

- Browse the ATTACK project in Jira
- Review the custom fields on a few issues
- Familiarize yourself with the issue structure (parent techniques, child sub-techniques)

### 2. Start Tracking Coverage

- Assign techniques to team members based on detection responsibility
- Update the **Maturity** field as you implement detections:
  - **Not Tracked**: No detection coverage
  - **Initial**: Basic detection exists but immature
  - **Defined**: Documented, tested detection
  - **Resilient**: Redundant detections, tuning in place
  - **Optimized**: Automated response, continuous improvement

### 3. Add Context

- Use Jira comments to document detection logic
- Link issues to related detection rules or SIEM queries
- Add labels for tagging (e.g., "high-priority", "cloud-focused")
- Attach documentation or screenshots

### 4. Export Visualizations

Once you've updated maturity levels, export to ATT&CK Navigator:

```bash
python3 attack2jira.py \
  -url https://yourcompany.atlassian.net \
  -u your-email@domain.com \
  -a export
```

This generates `attack2jira.json` which you can upload to [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/) for visualization.

### 5. Establish a Workflow

- Set up recurring reviews (monthly, quarterly)
- Create Jira workflows for detection development
- Integrate with your existing security operations processes
- Consider automating exports for regular reporting

### 6. Explore Advanced Features

- Review the [User Guide](USER_GUIDE.md) for detailed command reference
- Check out [Workflows](WORKFLOWS.md) for real-world usage examples
- Read the [API Reference](API_REFERENCE.md) to integrate attack2jira into custom scripts

## Getting Help

If you encounter issues not covered here:

1. Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Review the [FAQ](FAQ.md)
3. Visit the [GitHub repository](https://github.com/mvelazco/attack2jira) to search for or open an issue
4. Watch the [ATT&CKCon 2019 presentation](https://www.youtube.com/watch?v=hrzR8TpnjAw) for background and use cases

Welcome to the attack2jira community! We hope this tool helps your team effectively track and improve your defensive security posture.
