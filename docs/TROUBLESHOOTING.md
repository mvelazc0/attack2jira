# attack2jira Troubleshooting Guide

This guide helps you diagnose and resolve common issues with attack2jira.

## Table of Contents

- [Authentication Errors](#authentication-errors)
- [API Rate Limiting](#api-rate-limiting)
- [Custom Field Errors](#custom-field-errors)
- [Issue Creation Failures](#issue-creation-failures)
- [Navigator Export Issues](#navigator-export-issues)
- [Performance Problems](#performance-problems)
- [Network Issues](#network-issues)
- [Debugging Techniques](#debugging-techniques)

## Authentication Errors

### Error: 401 Unauthorized

**Symptoms**:
```
401 Client Error: Unauthorized for url: https://company.atlassian.net/rest/api/2/issue/createmeta
Authentication error. Invalid credentials.
```

**Causes**:
1. Using password instead of API token
2. Incorrect email address
3. Expired or invalid API token
4. Wrong Jira instance URL

**Solutions**:

**Solution 1: Verify You're Using API Token**
- Jira Cloud requires API tokens, not passwords
- Generate a new token: [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
- Never use your Atlassian password

**Solution 2: Check Email Address**
- Ensure email matches your Jira account exactly (case-sensitive)
- Use the same email you log in with

```bash
# Verify your email
curl -u "your-email@company.com:YOUR_TOKEN" \
  https://company.atlassian.net/rest/api/2/myself
```

Expected: JSON with your user details

**Solution 3: Generate Fresh API Token**
1. Navigate to [API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Revoke old token
3. Create new token
4. Try again immediately

**Solution 4: Verify Jira URL**
- Format: `https://yoursite.atlassian.net` (no trailing slash)
- Not `http://` (must be `https://`)
- Not your custom domain (must be `*.atlassian.net`)

### Error: 403 Forbidden

**Symptoms**:
```
403 Client Error: Forbidden
You don't have permission to perform this action.
```

**Causes**:
1. Insufficient Jira permissions
2. Account lacks admin privileges
3. Project creation disabled

**Solutions**:

**Check Permissions**:
1. Log in to Jira
2. Navigate to Settings → System → Global permissions
3. Verify you have "Jira Administrators" permission

**Request Admin Access**:
- Contact your Jira administrator
- Explain you need admin rights for project creation and custom field management
- Alternative: Ask admin to run attack2jira on your behalf

**Use Free Trial Instance**:
- Create a dedicated Jira Cloud free trial for testing
- You'll have full admin rights

## API Rate Limiting

### Error: 429 Too Many Requests

**Symptoms**:
```
429 Client Error: Too Many Requests
Rate limit exceeded. Please wait before making additional requests.
```

**Causes**:
- Exceeded Jira Cloud API rate limits
- Multiple concurrent requests
- Running exports too frequently

**Solutions**:

**Solution 1: Wait and Retry**
```bash
# Wait 60 seconds and retry
sleep 60
python3 attack2jira.py -url ... -u ... -a export
```

**Solution 2: Reduce Request Frequency**
- Don't run exports more than once per hour
- Spread multiple project initializations across hours

**Solution 3: Implement Retry Logic**
Modify attack2jira.py to add exponential backoff:
```python
import time

for attempt in range(5):
    try:
        # Make API request
        response = requests.get(...)
        response.raise_for_status()
        break
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            wait_time = 2 ** attempt  # Exponential backoff
            print(f"Rate limited. Waiting {wait_time}s...")
            time.sleep(wait_time)
        else:
            raise
```

**Jira Cloud Rate Limits**:
- **Free plan**: ~100 requests/minute
- **Paid plans**: Higher limits (varies)
- See [Atlassian Rate Limiting](https://developer.atlassian.com/cloud/jira/platform/rate-limiting/)

## Custom Field Errors

### Error: Custom Field Already Exists

**Symptoms**:
```
Field with name 'Maturity' already exists.
```

**Causes**:
- Running initialization multiple times
- Manually created field with same name

**Solutions**:

**Solution 1: Delete Existing Custom Field**
1. Log in to Jira
2. Settings → Issues → Custom fields
3. Find the field (e.g., "Maturity")
4. Click "..." → Delete
5. Re-run initialization

**Warning**: Deleting custom fields removes data from all issues using them.

**Solution 2: Modify Code to Skip Field Creation**
Edit `lib/jirahandler.py`:
```python
def create_custom_fields(self):
    if self.do_custom_fields_exist():
        print("Custom fields already exist, skipping creation")
        return
    # ... rest of method
```

### Error: Custom Field Not Found

**Symptoms**:
```
KeyError: 'Maturity'
Field 'Maturity' not found in custom fields.
```

**Causes**:
- Initialization didn't complete
- Custom fields deleted manually
- Incorrect field names

**Solutions**:

**Solution 1: Re-run Initialization**
```bash
python3 attack2jira.py -url ... -u ... -a initialize
```

**Solution 2: Verify Field Names**
Check field names in Jira:
1. Settings → Issues → Custom fields
2. Verify fields exist: Id, Tactic, Maturity, Url, Datasources, Sub-Technique of

**Solution 3: Debug Field Retrieval**
```python
from lib.jirahandler import JiraHandler

jira = JiraHandler()
jira.login(url=..., username=..., apitoken=...)
fields = jira.get_custom_fields()
print(fields)
```

## Issue Creation Failures

### Error: 400 Bad Request During Issue Creation

**Symptoms**:
```
400 Client Error: Bad Request
Field 'customfield_10001' cannot be set. It is not on the appropriate screen, or unknown.
```

**Causes**:
- Custom field not added to screen
- Incorrect field ID
- Field doesn't exist

**Solutions**:

**Solution 1: Re-run Screen Configuration**
Ensure `add_custom_fields_to_screen()` completed successfully:
```python
jira.add_custom_fields_to_screen(key='ATTACK')
```

**Solution 2: Manually Add Fields to Screen**
1. Project Settings → Screens
2. Edit "Default Issue Screen"
3. Add all custom fields
4. Save

**Solution 3: Check Field IDs**
```python
fields = jira.get_custom_fields()
print(fields)
# Ensure all 6 fields are present
```

### Error: Project Does Not Exist

**Symptoms**:
```
No project could be found with key 'ATTACK'.
```

**Causes**:
- Project not created yet
- Wrong project key
- Project deleted

**Solutions**:

**Solution 1: Run Initialization First**
```bash
python3 attack2jira.py -url ... -u ... -a initialize
```

**Solution 2: Verify Project Key**
- Log in to Jira
- Check project list for correct key
- Ensure you're using the right key in exports

**Solution 3: Create Project Manually**
If initialization failed:
1. Create project manually in Jira
2. Run custom field creation separately

### Error: Some Issues Failed to Create

**Symptoms**:
```
[ERROR] Failed to create issue for T1234: Connection timeout
[INFO] Created issue ATTACK-42 for T1235
```

**Causes**:
- Network hiccups
- Jira temporary unavailability
- Rate limiting

**Solutions**:

**Solution 1: Note Failed Techniques**
- attack2jira continues on failures
- Note which techniques failed
- Create them manually in Jira

**Solution 2: Re-run Initialization**
- Jira will reject duplicate issues
- Only failed issues will be created

**Solution 3: Increase Timeout**
Modify `lib/jirahandler.py`:
```python
response = requests.post(url, json=issue_dict, auth=(self.username, self.apitoken), timeout=60)
```

## Navigator Export Issues

### Error: No Issues Found in Project

**Symptoms**:
```
Warning: No issues found in project ATTACK
attack2jira.json created with 0 techniques
```

**Causes**:
- Project is empty
- Initialization didn't complete
- Wrong project key in code

**Solutions**:

**Solution 1: Run Initialization**
```bash
python3 attack2jira.py -url ... -u ... -a initialize
```

**Solution 2: Verify Project Has Issues**
- Log in to Jira
- Navigate to ATTACK project
- Verify issues exist

**Solution 3: Check Hardcoded Project Key**
Current limitation: Export searches for project key "ATTACK" only.

Edit `lib/jirahandler.py`:
```python
def get_technique_maturity(self):
    # Change from:
    jql = "project = ATTACK"
    # To:
    jql = f"project = {your_project_key}"
```

### Error: Invalid JSON Export

**Symptoms**:
- ATT&CK Navigator rejects the JSON
- "Invalid layer format" error

**Causes**:
- Corrupted export file
- Incomplete export
- Invalid maturity values

**Solutions**:

**Solution 1: Validate JSON**
```bash
python3 -m json.tool attack2jira.json
```

Expected: Reformatted JSON without errors

**Solution 2: Re-run Export**
```bash
rm attack2jira.json
python3 attack2jira.py -url ... -u ... -a export
```

**Solution 3: Check Navigator Version**
- Ensure Navigator is up to date
- Use Layer format version 4.3

### Error: Techniques Not Color-Coded

**Symptoms**:
- All techniques appear gray in Navigator
- No color differentiation

**Causes**:
- Maturity field not populated in Jira
- Export ran with `-hide` on all "Not Tracked"

**Solutions**:

**Solution 1: Update Maturity Levels in Jira**
1. Log in to Jira
2. Open ATTACK project issues
3. Set Maturity field values
4. Re-run export

**Solution 2: Verify Maturity Mapping**
Check `attack2jira.py` maturity color mapping:
```python
maturity_level_color = {
    "Not Tracked": "#DCDCDC",
    "Initial": "#e1fce1",
    "Defined": "#81fc81",
    "Resilient": "#49fc49",
    "Optimized": "#03ad03"
}
```

## Performance Problems

### Issue: Initialization Takes Too Long

**Symptoms**:
- Initialization takes over 30 minutes
- Appears to hang

**Causes**:
- Slow network connection
- Jira rate limiting
- Large number of API calls (266+ issues)

**Solutions**:

**Solution 1: Be Patient**
- Creating 266+ issues takes time (10-20 minutes normal)
- Monitor progress output

**Solution 2: Check Network Speed**
```bash
# Test Jira connectivity
curl -o /dev/null -s -w "Time: %{time_total}s\n" https://yoursite.atlassian.net
```

Expected: < 1 second

**Solution 3: Run During Off-Peak Hours**
- Jira Cloud performance varies
- Try early morning or late evening

**Solution 4: Monitor Progress**
attack2jira prints each issue creation:
```
[INFO] Creating technique: T1595 - Active Scanning
[SUCCESS] Created issue ATTACK-1
```

If this stops for > 5 minutes, cancel and retry.

### Issue: Export Hangs

**Symptoms**:
- Export command doesn't complete
- No output

**Causes**:
- Too many issues to retrieve
- Network timeout

**Solutions**:

**Solution 1: Increase Timeout**
Modify `lib/jirahandler.py`:
```python
response = requests.get(url, auth=(self.username, self.apitoken), timeout=120)
```

**Solution 2: Check Jira Query**
Test JQL query manually in Jira:
```
project = ATTACK
```

Verify it returns results.

## Network Issues

### Error: Connection Refused

**Symptoms**:
```
ConnectionError: [Errno 111] Connection refused
```

**Causes**:
- Incorrect Jira URL
- Firewall blocking outbound HTTPS
- No internet connectivity

**Solutions**:

**Solution 1: Verify URL**
```bash
curl -I https://yoursite.atlassian.net
```

Expected: HTTP 200 or 301

**Solution 2: Check Firewall**
- Ensure outbound HTTPS (port 443) allowed
- Whitelist `*.atlassian.net`

**Solution 3: Test Connectivity**
```bash
ping yoursite.atlassian.net
```

### Error: SSL Certificate Verification Failed

**Symptoms**:
```
SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed
```

**Causes**:
- Outdated Python SSL certificates
- Corporate SSL inspection

**Solutions**:

**Solution 1: Update Certifi**
```bash
pip3 install --upgrade certifi
```

**Solution 2: Disable SSL Warnings (Not Recommended)**
attack2jira already disables warnings:
```python
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

**Solution 3: Configure Corporate Proxy**
```bash
export HTTPS_PROXY="http://proxy.company.com:8080"
```

### Error: Cannot Reach MITRE ATT&CK API

**Symptoms**:
```
ConnectionError: Failed to retrieve ATT&CK data from cti-taxii.mitre.org
```

**Causes**:
- Firewall blocking MITRE domain
- Network outage

**Solutions**:

**Solution 1: Test Connectivity**
```bash
curl -I https://cti-taxii.mitre.org
```

**Solution 2: Whitelist MITRE Domain**
Add to firewall whitelist:
- `cti-taxii.mitre.org`

**Solution 3: Use VPN**
If on restricted network, connect via VPN.

## Debugging Techniques

### Enable Verbose Output

Add debugging to `lib/jirahandler.py`:
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# In methods:
logger.debug(f"Making request to {url}")
logger.debug(f"Response: {response.status_code}")
```

### Inspect API Requests

Use `requests` debugging:
```python
import requests
import http.client as http_client

http_client.HTTPConnection.debuglevel = 1
```

### Check Jira Audit Logs

1. Log in to Jira
2. Settings → System → Audit log
3. Look for failed API calls
4. Check timestamps and errors

### Python Interactive Debugging

```python
from lib.jirahandler import JiraHandler

jira = JiraHandler()
jira.login(url='...', username='...', apitoken='...')

# Test individual methods
fields = jira.get_custom_fields()
print(fields)

maturity = jira.get_technique_maturity()
print(maturity)
```

### Use Python Debugger (pdb)

Add breakpoint:
```python
import pdb; pdb.set_trace()
```

Run and inspect variables:
```bash
python3 attack2jira.py -url ... -u ... -a initialize
```

### Check Python Dependencies

```bash
pip3 list | grep attackcti
```

Expected: `attackcti` with version number

### Verify JSON Syntax

```bash
python3 -m json.tool attack2jira.json > /dev/null
```

No output = valid JSON

## Getting Help

If issues persist:

1. **Check FAQ**: [FAQ.md](FAQ.md) for common questions
2. **GitHub Issues**: Search [existing issues](https://github.com/mvelazco/attack2jira/issues)
3. **Open Issue**: Create new issue with:
   - Error message (full traceback)
   - Command used
   - Python version (`python3 --version`)
   - Operating system
   - Jira Cloud plan (free/paid)
4. **Community**: ATT&CKCon presentation Q&A or security forums

## Next Steps

- **Configuration**: Review [Configuration Guide](CONFIGURATION_GUIDE.md)
- **User Guide**: Consult [User Guide](USER_GUIDE.md) for usage patterns
- **FAQ**: Check [FAQ](FAQ.md) for quick answers

For questions or issues, visit the [GitHub repository](https://github.com/mvelazco/attack2jira).
