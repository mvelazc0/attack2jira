# attack2jira Workflows

This guide provides real-world workflow examples for using attack2jira in different scenarios and organizational contexts.

## Table of Contents

- [Basic Workflow: Initial Project Setup](#basic-workflow-initial-project-setup)
- [Advanced Workflow: Hierarchical Tracking with Teams](#advanced-workflow-hierarchical-tracking-with-teams)
- [Recurring Workflow: Scheduled Exports](#recurring-workflow-scheduled-exports)
- [Integration Workflow: Detection Engineering](#integration-workflow-detection-engineering)
- [Reporting Workflow: Executive Dashboards](#reporting-workflow-executive-dashboards)
- [Optimization Workflow: Continuous Improvement](#optimization-workflow-continuous-improvement)

## Basic Workflow: Initial Project Setup

**Scenario**: A security team wants to start tracking ATT&CK coverage for the first time.

**Participants**: Security Operations Manager, Detection Engineers

**Duration**: 2-4 hours initial setup, ongoing tracking

### Step 1: Prepare Environment

**Week 1 - Day 1: Setup**

```bash
# Install attack2jira
git clone https://github.com/mvelazco/attack2jira.git
cd attack2jira
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Actions**:
- [ ] Clone repository
- [ ] Create virtual environment
- [ ] Install dependencies
- [ ] Verify installation with `python attack2jira.py -h`

### Step 2: Configure Jira Access

**Jira Administrator Tasks**:
1. Create Jira Cloud account (or use existing)
2. Generate API token: [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
3. Store token securely in password manager
4. Document Jira URL and admin email

**Actions**:
- [ ] Jira Cloud instance ready
- [ ] Admin account created
- [ ] API token generated
- [ ] Credentials documented

### Step 3: Initialize Project

**Security Operations Manager**:

```bash
python attack2jira.py \
  -url https://acmecorp.atlassian.net \
  -u secops@acmecorp.com \
  -a initialize \
  -p "ATT&CK Coverage Tracker" \
  -k ATTACK
```

**Expected Output**:
- Project "ATT&CK Coverage Tracker" created
- 6 custom fields created (Id, Tactic, Maturity, Url, Datasources, Sub-Technique of)
- 266+ issues created (techniques and sub-techniques)

**Actions**:
- [ ] Run initialization command
- [ ] Verify project created in Jira
- [ ] Confirm all issues present
- [ ] Review custom fields configured

### Step 4: Assign Initial Ownership

**Week 1 - Day 2: Assignment**

**In Jira**:
1. Navigate to ATTACK project
2. Create JQL filter for each tactic:
   ```
   project = ATTACK AND Tactic = "initial-access"
   ```
3. Bulk assign techniques to team members based on expertise

**Example Assignments**:
- **Network Team**: reconnaissance, command-and-control
- **Endpoint Team**: execution, persistence, privilege-escalation
- **Cloud Team**: cloud-specific techniques
- **All Teams**: defense-evasion, lateral-movement

**Actions**:
- [ ] Create filters for each tactic
- [ ] Assign techniques to team members
- [ ] Document assignment rationale
- [ ] Communicate assignments to teams

### Step 5: Baseline Assessment

**Week 2-4: Assessment**

Each team member reviews assigned techniques and sets initial maturity:

**Maturity Levels**:
- **Not Tracked**: No detection capability
- **Initial**: Basic detection exists (e.g., EDR alerts)
- **Defined**: Documented detection logic, tested
- **Resilient**: Multiple detection methods, low false positives
- **Optimized**: Automated response, continuous tuning

**Process**:
1. Review technique description on attack.mitre.org
2. Assess existing detection capabilities (SIEM, EDR, network monitoring)
3. Set Maturity field in Jira
4. Add comment documenting detection methods

**Actions**:
- [ ] All assigned techniques reviewed
- [ ] Maturity levels set
- [ ] Detection methods documented
- [ ] Coverage gaps identified

### Step 6: Generate Baseline Report

**Week 4: Reporting**

```bash
python attack2jira.py \
  -url https://acmecorp.atlassian.net \
  -u secops@acmecorp.com \
  -a export
```

**Output**: `attack2jira.json`

**Share with Leadership**:
1. Upload to [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/)
2. Take screenshot of coverage heat map
3. Calculate coverage percentage:
   ```
   Tracked: 120/266 (45%)
   Initial: 80
   Defined: 30
   Resilient: 8
   Optimized: 2
   ```
4. Present in security operations review

**Actions**:
- [ ] Export generated
- [ ] Navigator visualization created
- [ ] Coverage metrics calculated
- [ ] Presented to leadership

## Advanced Workflow: Hierarchical Tracking with Teams

**Scenario**: Large organization with multiple security teams (Network, Endpoint, Cloud, Application Security)

**Participants**: CISO, Security Architects, Team Leads, Detection Engineers

**Duration**: Ongoing program

### Phase 1: Multi-Project Setup

Create separate projects for each team:

```bash
# Network Security Team
python attack2jira.py -url ... -u ... -a initialize -p "Network Security ATT&CK" -k NETSEC

# Endpoint Security Team
python attack2jira.py -url ... -u ... -a initialize -p "Endpoint Security ATT&CK" -k ENDPOINT

# Cloud Security Team
python attack2jira.py -url ... -u ... -a initialize -p "Cloud Security ATT&CK" -k CLOUD
```

**Benefits**:
- Team autonomy
- Focused tracking
- Different maturity progressions

### Phase 2: Cross-Team Coordination

**Monthly Sync Meeting**:
1. Each team presents coverage improvements
2. Share detection logic across teams
3. Identify overlaps and gaps
4. Coordinate on shared techniques (e.g., defense evasion)

**Jira Board Configuration**:
- Create portfolio-level board aggregating all projects
- Use labels for cross-cutting concerns: `priority:high`, `cloud-native`, `zero-day`

### Phase 3: Consolidated Reporting

**Quarterly Executive Report**:

```python
# Custom script: consolidate_coverage.py
from lib.jirahandler import JiraHandler

jira = JiraHandler()
jira.login(...)

projects = ['NETSEC', 'ENDPOINT', 'CLOUD']
consolidated = {}

for project in projects:
    # Modify get_technique_maturity() to accept project key
    maturity = jira.get_technique_maturity_for_project(project)

    # Merge, taking highest maturity across teams
    for tid, level in maturity.items():
        if tid not in consolidated or maturity_score(level) > maturity_score(consolidated[tid]):
            consolidated[tid] = level

# Generate consolidated export
generate_json_layer(consolidated)
```

**Output**: Organization-wide coverage visualization

## Recurring Workflow: Scheduled Exports

**Scenario**: Automate weekly coverage reports for management.

**Participants**: Security Operations team, automated systems

**Duration**: Ongoing automation

### Setup Automation

**VPS Configuration**:

```bash
# On VPS (DigitalOcean, Linode, etc.)
# Install attack2jira (see Deployment Guide)

# Create export script: /home/attack2jira/weekly-export.sh
#!/bin/bash
JIRA_URL="https://acmecorp.atlassian.net"
JIRA_USER="automation@acmecorp.com"
JIRA_TOKEN=$(cat /home/attack2jira/.secrets/jira_token)
EXPORT_DIR="/home/attack2jira/exports"
DATE=$(date +%Y-%m-%d)

cd /home/attack2jira/attack2jira
source venv/bin/activate

export JIRA_API_TOKEN="$JIRA_TOKEN"
python attack2jira.py -url "$JIRA_URL" -u "$JIRA_USER" -a export

mv attack2jira.json "$EXPORT_DIR/attack2jira-$DATE.json"

# Upload to S3 for storage
aws s3 cp "$EXPORT_DIR/attack2jira-$DATE.json" s3://acmecorp-security-exports/

# Generate coverage report
python /home/attack2jira/scripts/generate_report.py "$EXPORT_DIR/attack2jira-$DATE.json"

deactivate
```

**Cron Schedule**:
```cron
# Run every Monday at 8 AM
0 8 * * 1 /home/attack2jira/weekly-export.sh
```

### Email Reporting

**Custom Report Script** (`generate_report.py`):

```python
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Load export
with open('attack2jira-2024-01-15.json', 'r') as f:
    layer = json.load(f)

# Calculate stats
techniques = layer['techniques']
total = len(techniques)
tracked = sum(1 for t in techniques if t.get('enabled', True) and t.get('score', 0) > 0)
coverage = (tracked / total) * 100

# Create email
msg = MIMEMultipart()
msg['From'] = 'security@acmecorp.com'
msg['To'] = 'leadership@acmecorp.com'
msg['Subject'] = f'Weekly ATT&CK Coverage Report - {coverage:.1f}%'

body = f"""
Weekly ATT&CK Coverage Report

Coverage: {tracked}/{total} techniques ({coverage:.1f}%)

Breakdown by Maturity:
- Not Tracked: {total - tracked}
- Initial: {sum(1 for t in techniques if 'Initial' in str(t))}
- Defined: {sum(1 for t in techniques if 'Defined' in str(t))}
- Resilient: {sum(1 for t in techniques if 'Resilient' in str(t))}
- Optimized: {sum(1 for t in techniques if 'Optimized' in str(t))}

View detailed heat map: https://mitre-attack.github.io/attack-navigator/
(Upload attached attack2jira.json)

Jira Project: https://acmecorp.atlassian.net/browse/ATTACK
"""

msg.attach(MIMEText(body, 'plain'))

# Attach JSON
attachment = MIMEBase('application', 'json')
with open('attack2jira-2024-01-15.json', 'rb') as f:
    attachment.set_payload(f.read())
encoders.encode_base64(attachment)
attachment.add_header('Content-Disposition', 'attachment; filename=attack2jira.json')
msg.attach(attachment)

# Send
smtp = smtplib.SMTP('smtp.acmecorp.com', 587)
smtp.starttls()
smtp.login('security@acmecorp.com', 'password')
smtp.send_message(msg)
smtp.quit()
```

## Integration Workflow: Detection Engineering

**Scenario**: Link ATT&CK tracking to detection rule development and deployment.

**Participants**: Detection Engineers, SIEM team, Threat Intel team

**Duration**: Ongoing integration

### Workflow Steps

**Step 1: Detection Gap Identification**

Use Jira filters to find gaps:
```
project = ATTACK AND Maturity = "Not Tracked" AND Tactic IN ("initial-access", "execution")
ORDER BY priority DESC
```

**Step 2: Detection Development**

For each gap:
1. Create Jira sub-task: "Develop detection for T1234"
2. Research detection logic (Sigma, YARA, SIEM queries)
3. Develop rule in detection repository (Git)
4. Link Git commit to Jira issue

**Example**:
```bash
# In detection repo
git commit -m "Add Sigma rule for T1595 - Active Scanning (ATTACK-42)"
git push

# In Jira issue ATTACK-42
# Add comment: "Detection rule: https://github.com/acmecorp/detections/commit/abc123"
```

**Step 3: Testing & Tuning**

1. Deploy rule to SIEM (Splunk, Elastic, Sentinel)
2. Monitor false positive rate
3. Tune thresholds and logic
4. Update Maturity field as improvements are made:
   - Initial: Rule deployed
   - Defined: Tuned, low false positives
   - Resilient: Redundant detections (EDR + SIEM)
   - Optimized: Automated response playbook

**Step 4: Documentation**

In Jira issue, document:
- Detection logic (query/rule)
- Data sources required
- Baseline false positive rate
- Tuning history
- Related threat intel

**Step 5: Continuous Monitoring**

Weekly review:
```
project = ATTACK AND Maturity IN ("Initial", "Defined") AND updated <= -30d
```

Identify stale detections needing review.

## Reporting Workflow: Executive Dashboards

**Scenario**: Create executive-friendly dashboards showing security posture improvement.

**Participants**: CISO, Security Managers, Board of Directors

**Duration**: Quarterly reviews

### Dashboard Creation

**Jira Dashboard Gadgets**:

1. **Pie Chart: Maturity Distribution**
   - Filter: `project = ATTACK`
   - Group by: Maturity
   - Shows proportion at each maturity level

2. **Two-Dimensional Filter Stats: Tactic vs. Maturity**
   - X-axis: Tactic
   - Y-axis: Maturity
   - Heat map showing gaps

3. **Filter Results: High-Priority Gaps**
   - JQL: `project = ATTACK AND Maturity = "Not Tracked" AND priority = High`
   - Shows critical coverage gaps

4. **Line Chart: Coverage Over Time**
   - Use saved exports to track progress
   - Plot coverage % by month

### Quarterly Reporting Process

**Week Before Board Meeting**:

1. **Generate Export**:
   ```bash
   python attack2jira.py -url ... -u ... -a export
   ```

2. **Calculate Metrics**:
   ```python
   import json

   with open('attack2jira.json') as f:
       data = json.load(f)

   total = len(data['techniques'])
   tracked = sum(1 for t in data['techniques'] if t.get('score', 0) > 0)
   coverage = (tracked / total) * 100

   print(f"Q4 2024 Coverage: {coverage:.1f}%")
   print(f"Q3 2024 Coverage: 42.5% (historical)")
   print(f"Improvement: +{coverage - 42.5:.1f}%")
   ```

3. **Create Presentation**:
   - Slide 1: Executive summary (coverage %, improvement)
   - Slide 2: ATT&CK Navigator heat map screenshot
   - Slide 3: Top 5 coverage gaps
   - Slide 4: Q1 2025 roadmap (techniques to prioritize)

## Optimization Workflow: Continuous Improvement

**Scenario**: Mature security program focused on optimizing detection capabilities.

**Participants**: Senior Detection Engineers, Threat Hunting team, Red Team

**Duration**: Ongoing improvement cycle

### Improvement Cycle

**Monthly Cycle**:

**Week 1: Assessment**
- Review techniques at "Defined" maturity
- Identify candidates for improvement to "Resilient"
- Select 5-10 techniques to focus on

**Week 2: Enhancement**
- Add redundant detection methods
- Implement cross-correlation rules
- Deploy automated enrichment

**Week 3: Validation**
- Purple team exercises
- Simulate techniques with red team tools (Atomic Red Team, Caldera)
- Verify detections trigger correctly

**Week 4: Documentation & Promotion**
- Update Jira with validation results
- Promote Maturity to "Resilient"
- Document in runbooks

### Purple Team Integration

**Before Exercise**:
1. Select techniques to test from Jira
2. Filter by tactic or priority:
   ```
   project = ATTACK AND Tactic = "lateral-movement" AND Maturity IN ("Defined", "Resilient")
   ```

**During Exercise**:
1. Red team executes techniques
2. Blue team monitors SIEM/EDR for alerts
3. Document detection success/failure in Jira comments

**After Exercise**:
1. Update Maturity based on validation:
   - Detected reliably → Promote maturity
   - Missed → Demote maturity, create improvement task
2. Export updated coverage
3. Track improvement trend

### Automation Maturity Progression

**Path to "Optimized"**:

1. **Detection Exists** (Initial)
2. **Documented & Tested** (Defined)
3. **Redundant & Tuned** (Resilient)
4. **Automated Response** (Optimized):
   - SOAR playbook auto-triggers
   - Automated containment (quarantine host, block IP)
   - Auto-ticket creation with context
   - Continuous ML-based tuning

**Example SOAR Integration**:
```yaml
# Playbook: T1059.001 - PowerShell Execution
trigger: SIEM alert for suspicious PowerShell
actions:
  - Gather process tree from EDR
  - Extract PowerShell command
  - Check against IOC database
  - If malicious:
      - Isolate host
      - Create Jira incident ticket
      - Update ATTACK-123 with incident link
      - Notify SOC lead
```

## Best Practices Across All Workflows

### 1. Consistent JQL Queries

Standardize queries for repeatability:
```
# Coverage Gaps
project = ATTACK AND Maturity = "Not Tracked"

# High-Priority Gaps
project = ATTACK AND Maturity = "Not Tracked" AND Tactic IN ("initial-access", "execution", "persistence")

# Recent Updates
project = ATTACK AND updated >= -7d

# Techniques Needing Review
project = ATTACK AND Maturity IN ("Initial", "Defined") AND updated <= -90d
```

### 2. Regular Cadence

- **Weekly**: Team reviews assigned techniques
- **Monthly**: Generate and share coverage exports
- **Quarterly**: Executive reporting and roadmap planning
- **Annually**: Comprehensive purple team validation

### 3. Version Control Exports

```bash
# Store exports in Git
mkdir -p exports
cp attack2jira.json exports/attack2jira-$(date +%Y-%m-%d).json
cd exports
git add .
git commit -m "Coverage export for $(date +%Y-%m-%d)"
git push
```

Track coverage changes over time with `git diff`.

### 4. Cross-Functional Collaboration

- **Link Jira issues** to detection repos, incident tickets, threat intel reports
- **Tag teammates** in comments for knowledge sharing
- **Create dashboards** accessible to all stakeholders

### 5. Continuous Documentation

In Jira issue comments, document:
- Detection logic (queries, rules)
- Data sources required
- Known limitations
- Related techniques
- Incident examples

## Next Steps

- **Architecture**: Understand internal design in [Architecture Guide](ARCHITECTURE.md)
- **API Reference**: Automate workflows with [API Reference](API_REFERENCE.md)
- **Deployment**: Scale workflows with [Deployment Guide](DEPLOYMENT_GUIDE.md)

For questions or issues, visit the [GitHub repository](https://github.com/mvelazco/attack2jira).
