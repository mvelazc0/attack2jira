# attack2jira Configuration Guide

This guide covers all configuration aspects for attack2jira, including Jira setup, API authentication, and advanced configuration options.

## Table of Contents

- [Overview](#overview)
- [Jira Cloud Setup](#jira-cloud-setup)
- [API Token Generation](#api-token-generation)
- [MITRE ATT&CK API Configuration](#mitre-attck-api-configuration)
- [Advanced Configuration](#advanced-configuration)
- [Environment Variables](#environment-variables)
- [Security Best Practices](#security-best-practices)
- [Configuration Validation](#configuration-validation)

## Overview

attack2jira requires minimal configuration but depends on proper Jira Cloud setup and secure API authentication. Unlike many tools, attack2jira does not use a configuration file—all settings are passed via command-line arguments.

### Configuration Components

1. **Jira Cloud Instance**: Your organization's Jira environment
2. **Authentication Credentials**: Email and API token for Jira access
3. **Project Settings**: Project name and key (optional customization)
4. **MITRE ATT&CK API**: Automatically accessed (no configuration needed)

### No Configuration File Needed

attack2jira deliberately avoids configuration files to prevent accidental credential exposure. All parameters are passed at runtime via command-line arguments.

## Jira Cloud Setup

### Requirement: Jira Cloud Only

attack2jira is designed exclusively for **Jira Cloud**. It is **not compatible** with:
- Jira Server (on-premise installations)
- Jira Data Center (enterprise on-premise)

**Why Jira Cloud Only?**
- Uses Jira Cloud REST API v2 and simplified API endpoints
- API authentication differs between Cloud and Server
- Project creation templates are Cloud-specific
- Cloud-specific features (Greenhopper/Scrum templates)

### Creating a Jira Cloud Instance

If you don't have Jira Cloud access:

#### Option 1: Free Trial (Recommended for Testing)

1. Visit [Atlassian Free Trial](https://www.atlassian.com/software/jira/free)
2. Click "Get it free"
3. Enter your work email address
4. Choose a site name (becomes `yoursite.atlassian.net`)
5. Set up your admin account
6. Select "Jira Software" as the product
7. Complete the onboarding wizard

**Free Trial Details**:
- **Duration**: Unlimited (free plan)
- **Users**: Up to 10 users
- **Features**: Full Jira Software features
- **Storage**: 2 GB
- **Limitations**: Community support only

#### Option 2: Paid Plan

For production use, consider a paid plan:
- **Standard**: $7.75/user/month (up to 10,000 users)
- **Premium**: $15.25/user/month (advanced features)
- **Enterprise**: Custom pricing (unlimited users, SLA)

Visit [Jira Pricing](https://www.atlassian.com/software/jira/pricing) for current pricing.

### Verifying Jira Cloud Access

Ensure you have the correct Jira environment:

1. **Log in** to your Jira instance
2. **Check the URL**: Should be `https://*.atlassian.net` (not `https://your-domain.com/jira`)
3. **Navigate to** Settings → System
4. **Verify** "Jira Cloud" is displayed in the footer

### Required Jira Permissions

Your account must have **Jira Administrator** global permission to:
- Create projects
- Create custom fields
- Modify screens and field configurations
- Create issues

**Check Your Permissions**:
1. Click your profile icon → **Jira settings**
2. Navigate to **System** → **Global permissions**
3. Verify your user/group has "Jira Administrators" permission

**If You Don't Have Admin Access**:
- Request admin permissions from your Jira administrator
- Ask an admin to run attack2jira on your behalf
- Use a separate Jira Cloud free trial instance for testing

## API Token Generation

Jira Cloud uses API tokens for programmatic access instead of passwords.

### Creating an API Token

#### Step 1: Access Atlassian Account Settings

1. Log in to your Jira Cloud instance
2. Click your **profile icon** (top-right corner)
3. Select **Account settings** (redirects to id.atlassian.com)
4. Navigate to **Security** tab
5. Scroll to **API tokens** section

**Direct Link**: [https://id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)

![API Token Settings Screenshot: Shows the Atlassian account security page with the API token section, displaying existing tokens and a "Create API token" button]

#### Step 2: Create Token

1. Click **Create API token**
2. Enter a label (e.g., "attack2jira production")
3. Click **Create**
4. **Copy the token immediately** (40-character alphanumeric string)
5. Click **Close**

**Important**: The token is only shown once. If you lose it, you must create a new one.

#### Step 3: Store Token Securely

**Recommended Storage Methods**:
- **Password Manager**: 1Password, LastPass, Bitwarden, etc.
- **Secrets Manager**: AWS Secrets Manager, Azure Key Vault, HashiCorp Vault
- **Environment Variable**: For production/automation (see below)

**Never**:
- ❌ Commit tokens to version control (Git)
- ❌ Store in plain text files in home directories
- ❌ Share via email or chat
- ❌ Include in screenshots or documentation

### Using the API Token

When running attack2jira, you'll be prompted:
```
Enter API token:
```

Paste your token (input is hidden) and press Enter.

**Example**:
```bash
$ python3 attack2jira.py -url https://acme.atlassian.net -u admin@acme.com -a initialize
Enter API token: [paste token here - hidden]
```

### Multiple API Tokens

You can create multiple tokens for different purposes:
- **Development Token**: For testing and development work
- **Production Token**: For scheduled automated runs
- **Personal Token**: For individual analyst use

Label each token clearly to track usage.

### Rotating API Tokens

For security best practices, rotate tokens periodically:

1. Create a new API token with a different label
2. Update your scripts/environment variables to use the new token
3. Test the new token works
4. Revoke the old token
5. Document the rotation date

**Recommended Rotation Frequency**: Every 90-180 days

### Revoking API Tokens

If a token is compromised or no longer needed:

1. Navigate to [API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Find the token in the list
3. Click **Revoke**
4. Confirm revocation

Revoked tokens stop working immediately.

## MITRE ATT&CK API Configuration

attack2jira automatically fetches data from the MITRE ATT&CK API via the `attackcti` Python library. No configuration is required.

### ATT&CK API Endpoints

The tool accesses:
- **TAXII Server**: `https://cti-taxii.mitre.org/taxii/`
- **STIX Collections**: Enterprise ATT&CK collection
- **Data Retrieved**:
  - Techniques and sub-techniques
  - Tactics (kill chain phases)
  - Data sources
  - Technique descriptions and metadata

### Network Requirements

Ensure your network allows HTTPS access to:
- `cti-taxii.mitre.org` (port 443)

**Test Connectivity**:
```bash
curl -I https://cti-taxii.mitre.org
```

Expected: HTTP 200 or 301 response.

### Proxy Configuration

If behind a corporate proxy, configure Python to use it:

**Linux/macOS**:
```bash
export HTTP_PROXY="http://proxy.example.com:8080"
export HTTPS_PROXY="http://proxy.example.com:8080"
```

**Windows (Command Prompt)**:
```cmd
set HTTP_PROXY=http://proxy.example.com:8080
set HTTPS_PROXY=http://proxy.example.com:8080
```

**Windows (PowerShell)**:
```powershell
$env:HTTP_PROXY = "http://proxy.example.com:8080"
$env:HTTPS_PROXY = "http://proxy.example.com:8080"
```

### ATT&CK Data Freshness

attack2jira fetches fresh ATT&CK data on every run. This ensures:
- You always get the latest techniques
- New techniques are automatically included
- Deprecated techniques are filtered out

**Implication**: Requires internet connectivity to MITRE's API during initialization.

### Offline Mode

attack2jira does **not support** offline mode. Internet connectivity is required to:
- Fetch ATT&CK data from MITRE
- Authenticate with Jira Cloud
- Create/read Jira issues

## Advanced Configuration

### Custom Project Names

Override the default project name and key:

```bash
python3 attack2jira.py \
  -url https://site.atlassian.net \
  -u user@domain.com \
  -a initialize \
  -p "Custom Project Name" \
  -k CUSTOM
```

**Project Name** (`-p`):
- Displayed in Jira UI
- Can include spaces and special characters
- Default: "Mitre Attack Framework"
- Examples: "ATT&CK Coverage 2024", "Detection Tracker", "Purple Team Matrix"

**Project Key** (`-k`):
- Used in issue keys (e.g., CUSTOM-1, CUSTOM-2)
- Must be **uppercase letters only** (2-10 characters)
- Cannot contain spaces or special characters
- Must be **unique** across your Jira instance
- Default: "ATTACK"

**Choosing Good Keys**:
- Keep it short (3-6 characters)
- Make it memorable
- Relate to your organization or team
- Examples: ATK, DET, SECOPS, PURPLE, THREAT

### Export Hiding Options

Hide "Not Tracked" techniques from Navigator visualization:

```bash
python3 attack2jira.py \
  -url https://site.atlassian.net \
  -u user@domain.com \
  -a export \
  -hide
```

**Effect**: Techniques with maturity level "Not Tracked" are:
- Still included in the JSON
- Marked as "disabled" in the layer
- Appear grayed out in ATT&CK Navigator

**Use Cases**:
- Focus on tracked techniques only
- Reduce visual clutter
- Highlight coverage gaps by contrast

### Command-Line Argument Best Practices

**Quote Arguments with Spaces**:
```bash
python3 attack2jira.py -p "Project Name With Spaces" -k PROJ
```

**Use Full Jira URLs**:
```bash
# Correct
python3 attack2jira.py -url https://company.atlassian.net

# Incorrect
python3 attack2jira.py -url company.atlassian.net
python3 attack2jira.py -url https://company.atlassian.net/
```

**Consistent Username Format**:
```bash
# Use your email address
python3 attack2jira.py -u jane.doe@company.com
```

## Environment Variables

For automated deployments, avoid interactive password prompts by configuring environment variables.

### Current Limitation

attack2jira currently uses `getpass.getpass()` for secure password input, which **requires interactive terminal input**. Environment variable support is **not built-in**.

### Workaround for Automation

To automate attack2jira without manual password entry, modify the code:

**Original Code** (attack2jira.py):
```python
apitoken = getpass.getpass(prompt='Enter API token: ')
```

**Modified for Environment Variable**:
```python
import os
apitoken = os.environ.get('JIRA_API_TOKEN') or getpass.getpass(prompt='Enter API token: ')
```

**Usage**:
```bash
export JIRA_API_TOKEN="your-api-token-here"
python3 attack2jira.py -url https://site.atlassian.net -u user@domain.com -a export
```

**Security Warning**: Environment variables can be exposed via process listings. Use with caution and only in secure environments.

### Recommended Environment Variables

If you modify the code to support environment variables:

- `JIRA_URL`: Jira Cloud instance URL
- `JIRA_USERNAME`: Jira username/email
- `JIRA_API_TOKEN`: API token (sensitive)
- `JIRA_PROJECT_KEY`: Default project key
- `JIRA_PROJECT_NAME`: Default project name

**Example** (.env file):
```bash
JIRA_URL=https://acme.atlassian.net
JIRA_USERNAME=admin@acme.com
JIRA_API_TOKEN=abcdefghijklmnopqrstuvwxyz123456
JIRA_PROJECT_KEY=ATTACK
JIRA_PROJECT_NAME="Mitre Attack Framework"
```

**Load with** `source .env` or use a tool like `python-dotenv`.

## Security Best Practices

### Credential Management

**Do**:
- ✅ Use API tokens instead of passwords
- ✅ Store tokens in password managers
- ✅ Rotate tokens every 90-180 days
- ✅ Create separate tokens for different environments (dev, prod)
- ✅ Revoke tokens immediately if compromised
- ✅ Use dedicated service accounts for automation

**Don't**:
- ❌ Share API tokens via email or chat
- ❌ Commit tokens to Git repositories
- ❌ Store tokens in plain text files
- ❌ Use personal accounts for production automation
- ❌ Use the same token across multiple tools

### Least Privilege

Create dedicated Jira accounts with minimal necessary permissions:
- Grant Jira Administrator only if needed
- Use project-specific permissions when possible
- Audit permission usage regularly

### Network Security

- Run attack2jira from trusted networks
- Use VPN when accessing Jira Cloud remotely
- Monitor outbound connections to Jira and MITRE APIs
- Implement firewall rules allowing only necessary endpoints

### Audit Logging

Enable Jira audit logging to track:
- Project creation events
- Custom field modifications
- Issue creation activity
- API token usage

**Enable Audit Logging**:
1. Jira Settings → System → Audit log
2. Review logs periodically for anomalies

### Secure Automation

For scheduled tasks:
- Store credentials in dedicated secrets management systems
- Limit service account permissions
- Monitor automated runs for failures
- Log all activity for incident response

## Configuration Validation

Verify your configuration before running attack2jira.

### Pre-Flight Checks

**1. Validate Jira URL**:
```bash
curl -I https://yoursite.atlassian.net
```
Expected: HTTP 200 or 301

**2. Test Authentication**:
```bash
curl -u "user@domain.com:YOUR_API_TOKEN" \
  https://yoursite.atlassian.net/rest/api/2/myself
```
Expected: JSON response with your user details

**3. Check Admin Permissions**:
Log in to Jira → Settings → System
Verify you're listed under "Jira Administrators"

**4. Verify ATT&CK API Access**:
```bash
curl -I https://cti-taxii.mitre.org
```
Expected: HTTP 200 or 301

### Testing Configuration

Run a non-destructive test (export on non-existent project):
```bash
python3 attack2jira.py -url https://yoursite.atlassian.net -u user@domain.com -a export
```

**Expected Outcomes**:
- **Authentication success**: Proceeds past login
- **Project not found**: Error about missing project (expected if not initialized)
- **401 Unauthorized**: Credential issue (check email/token)
- **Connection error**: Network or URL issue

### Troubleshooting Configuration Issues

**Issue: 401 Unauthorized**

Causes:
- Wrong email address
- Invalid/expired API token
- Using password instead of API token

Solution:
1. Verify email address (case-sensitive)
2. Generate a new API token
3. Ensure you're using the token, not password

**Issue: 403 Forbidden**

Causes:
- Insufficient Jira permissions
- Account locked

Solution:
1. Verify admin permissions
2. Contact Jira administrator

**Issue: Connection Refused**

Causes:
- Incorrect Jira URL
- Network/firewall blocking

Solution:
1. Verify URL format: `https://site.atlassian.net`
2. Test connectivity: `curl -I <URL>`
3. Check firewall rules

**Issue: SSL Certificate Errors**

Causes:
- Corporate SSL inspection
- Outdated Python SSL certificates

Solution:
```bash
pip3 install --upgrade certifi
```

## Next Steps

- **First Run**: Proceed to [Getting Started Guide](GETTING_STARTED.md)
- **Production Deployment**: See [Deployment Guide](DEPLOYMENT_GUIDE.md)
- **Troubleshooting**: Review [Troubleshooting Guide](TROUBLESHOOTING.md)
- **Advanced Usage**: Explore [User Guide](USER_GUIDE.md)

For questions or issues, visit the [GitHub repository](https://github.com/mvelazco/attack2jira) or consult the [FAQ](FAQ.md).
