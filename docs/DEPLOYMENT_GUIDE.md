# attack2jira Deployment Guide

This guide covers production deployment strategies for attack2jira, including local, Docker, and VPS deployments with automation and monitoring.

## Table of Contents

- [Deployment Overview](#deployment-overview)
- [Local Deployment](#local-deployment)
- [Docker Deployment](#docker-deployment)
- [VPS Deployment](#vps-deployment)
- [CI/CD Integration](#cicd-integration)
- [Monitoring & Logging](#monitoring--logging)
- [Backup Strategy](#backup-strategy)
- [Disaster Recovery](#disaster-recovery)
- [Performance Tuning](#performance-tuning)

## Deployment Overview

### Deployment Scenarios

**Scenario 1: Single Analyst**
- **Environment**: Laptop/workstation
- **Frequency**: Ad-hoc runs
- **Deployment**: Local installation
- **Automation**: None or minimal

**Scenario 2: Security Team**
- **Environment**: Shared workstation or VPS
- **Frequency**: Weekly/monthly exports
- **Deployment**: VPS with scheduled tasks
- **Automation**: Cron jobs or systemd timers

**Scenario 3: Enterprise Organization**
- **Environment**: Cloud infrastructure (AWS, Azure, GCP)
- **Frequency**: Daily/weekly automated exports
- **Deployment**: Docker container or serverless
- **Automation**: CI/CD pipeline (GitHub Actions, Jenkins)

### Architecture Patterns

**Pattern 1: Direct Execution**
```
[Analyst Workstation] → [Jira Cloud]
                      ↓
                   [MITRE API]
```

**Pattern 2: Centralized Automation**
```
[Cron Job/Scheduler] → [attack2jira Script] → [Jira Cloud]
                                            ↓
                                         [MITRE API]
                                            ↓
                                         [Export Storage]
```

**Pattern 3: CI/CD Pipeline**
```
[Git Push] → [GitHub Actions] → [Docker Container] → [Jira Cloud]
                                                   ↓
                                                [MITRE API]
                                                   ↓
                                                [Artifact Storage]
```

## Local Deployment

Local deployment is suitable for single-user, ad-hoc usage.

### Prerequisites

- Python 3.6+ installed
- Virtual environment configured (recommended)
- Jira API token stored securely

### Installation

```bash
# Clone repository
git clone https://github.com/mvelazco/attack2jira.git
cd attack2jira

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Usage Workflow

```bash
# Activate environment
cd /path/to/attack2jira
source venv/bin/activate

# Run initialization (one-time)
python attack2jira.py -url https://company.atlassian.net -u user@company.com -a initialize

# Run exports (periodic)
python attack2jira.py -url https://company.atlassian.net -u user@company.com -a export

# Deactivate
deactivate
```

### Wrapper Script

Create a convenience script `run-attack2jira.sh`:

```bash
#!/bin/bash

# Configuration
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_PATH="$SCRIPT_DIR/venv"
JIRA_URL="https://company.atlassian.net"
JIRA_USER="user@company.com"

# Activate virtual environment
source "$VENV_PATH/bin/activate"

# Run attack2jira with all arguments passed through
python "$SCRIPT_DIR/attack2jira.py" -url "$JIRA_URL" -u "$JIRA_USER" "$@"

# Deactivate
deactivate
```

Make executable:
```bash
chmod +x run-attack2jira.sh
```

Usage:
```bash
./run-attack2jira.sh -a export
./run-attack2jira.sh -a initialize -p "Custom Project" -k CUST
```

### Local Deployment Best Practices

- Use virtual environments to isolate dependencies
- Store API tokens in a password manager, not in scripts
- Keep the repository updated: `git pull origin main`
- Document your project key and configuration

## Docker Deployment

Docker support is **planned but not yet available** in the official repository. Below is a reference implementation.

### Custom Dockerfile

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY attack2jira.py .
COPY lib/ lib/

# Create a non-root user
RUN useradd -m -u 1000 attack2jira && \
    chown -R attack2jira:attack2jira /app

USER attack2jira

# Set entrypoint
ENTRYPOINT ["python", "attack2jira.py"]
CMD ["-h"]
```

### Build Docker Image

```bash
docker build -t attack2jira:latest .
```

### Run with Docker

```bash
# Initialize project
docker run -it attack2jira:latest \
  -url https://company.atlassian.net \
  -u user@company.com \
  -a initialize

# Export to local directory
docker run -it -v $(pwd)/exports:/app/exports attack2jira:latest \
  -url https://company.atlassian.net \
  -u user@company.com \
  -a export
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  attack2jira:
    build: .
    image: attack2jira:latest
    environment:
      - JIRA_URL=https://company.atlassian.net
      - JIRA_USERNAME=user@company.com
      - JIRA_API_TOKEN=${JIRA_API_TOKEN}
    volumes:
      - ./exports:/app/exports
    command: ["-a", "export"]
```

Run with Docker Compose:
```bash
export JIRA_API_TOKEN="your-token-here"
docker-compose run attack2jira
```

### Docker Deployment Best Practices

- Use multi-stage builds to minimize image size
- Run as non-root user for security
- Mount volumes for export output
- Use environment variables for configuration
- Tag images with version numbers

## VPS Deployment

Deploy attack2jira on a Virtual Private Server for centralized, automated execution.

### VPS Provider Selection

Recommended providers:
- **DigitalOcean**: Developer-friendly, $5/month droplets
- **Linode**: Reliable, competitive pricing
- **Vultr**: Global presence, fast deployment
- **AWS EC2**: Enterprise-grade, pay-per-use
- **Hostinger VPS**: Budget option

### VPS Specifications

**Minimum**:
- 1 vCPU
- 1 GB RAM
- 20 GB SSD
- Ubuntu 20.04 LTS

**Recommended**:
- 2 vCPU
- 2 GB RAM
- 40 GB SSD
- Ubuntu 22.04 LTS

### Initial VPS Setup

```bash
# Connect via SSH
ssh root@vps-ip-address

# Update system
apt update && apt upgrade -y

# Install prerequisites
apt install -y python3 python3-pip python3-venv git curl

# Create dedicated user
adduser attack2jira
usermod -aG sudo attack2jira

# Switch to user
su - attack2jira
```

### Install attack2jira on VPS

```bash
# Clone repository
cd ~
git clone https://github.com/mvelazco/attack2jira.git
cd attack2jira

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Secure API Token Storage

Create a secure credential file:

```bash
# Create .secrets directory
mkdir -p ~/.secrets
chmod 700 ~/.secrets

# Store API token
echo "YOUR_API_TOKEN_HERE" > ~/.secrets/jira_api_token
chmod 600 ~/.secrets/jira_api_token
```

### Automated Execution Script

Create `/home/attack2jira/run-export.sh`:

```bash
#!/bin/bash

# Configuration
JIRA_URL="https://company.atlassian.net"
JIRA_USER="user@company.com"
JIRA_TOKEN_FILE="$HOME/.secrets/jira_api_token"
SCRIPT_DIR="/home/attack2jira/attack2jira"
EXPORT_DIR="/home/attack2jira/exports"
LOG_FILE="/home/attack2jira/logs/export.log"

# Create directories
mkdir -p "$EXPORT_DIR" "$(dirname "$LOG_FILE")"

# Activate virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

# Read API token (requires script modification to support stdin)
JIRA_TOKEN=$(cat "$JIRA_TOKEN_FILE")

# Run export
echo "$(date): Starting export..." >> "$LOG_FILE"

# Note: This requires modifying attack2jira.py to accept token via stdin or env var
export JIRA_API_TOKEN="$JIRA_TOKEN"
python "$SCRIPT_DIR/attack2jira.py" \
  -url "$JIRA_URL" \
  -u "$JIRA_USER" \
  -a export >> "$LOG_FILE" 2>&1

# Move export with timestamp
if [ -f "$SCRIPT_DIR/attack2jira.json" ]; then
  mv "$SCRIPT_DIR/attack2jira.json" "$EXPORT_DIR/attack2jira-$(date +%Y%m%d-%H%M%S).json"
  echo "$(date): Export completed successfully" >> "$LOG_FILE"
else
  echo "$(date): Export failed - no output file" >> "$LOG_FILE"
fi

deactivate
```

Make executable:
```bash
chmod +x /home/attack2jira/run-export.sh
```

### Scheduled Execution with Cron

Edit crontab:
```bash
crontab -e
```

Add scheduled tasks:

```cron
# Run export every Monday at 9 AM
0 9 * * 1 /home/attack2jira/run-export.sh

# Run export on the 1st of every month at 8 AM
0 8 1 * * /home/attack2jira/run-export.sh

# Run export daily at 2 AM
0 2 * * * /home/attack2jira/run-export.sh
```

### Systemd Timer (Alternative to Cron)

Create `/etc/systemd/system/attack2jira-export.service`:

```ini
[Unit]
Description=attack2jira Export Service
After=network.target

[Service]
Type=oneshot
User=attack2jira
ExecStart=/home/attack2jira/run-export.sh
StandardOutput=journal
StandardError=journal
```

Create `/etc/systemd/system/attack2jira-export.timer`:

```ini
[Unit]
Description=attack2jira Weekly Export Timer

[Timer]
OnCalendar=Mon *-*-* 09:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

Enable and start:
```bash
sudo systemctl enable attack2jira-export.timer
sudo systemctl start attack2jira-export.timer

# Check status
sudo systemctl list-timers --all
```

## CI/CD Integration

Automate attack2jira execution with CI/CD pipelines.

### GitHub Actions

Create `.github/workflows/attack2jira-export.yml`:

```yaml
name: attack2jira Weekly Export

on:
  schedule:
    # Run every Monday at 9 AM UTC
    - cron: '0 9 * * 1'
  workflow_dispatch:  # Allow manual triggering

jobs:
  export:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run export
        env:
          JIRA_URL: ${{ secrets.JIRA_URL }}
          JIRA_USERNAME: ${{ secrets.JIRA_USERNAME }}
          JIRA_API_TOKEN: ${{ secrets.JIRA_API_TOKEN }}
        run: |
          # Modify attack2jira.py to read token from env var
          python attack2jira.py -url "$JIRA_URL" -u "$JIRA_USERNAME" -a export

      - name: Archive export
        uses: actions/upload-artifact@v3
        with:
          name: attack2jira-export-${{ github.run_number }}
          path: attack2jira.json
          retention-days: 90

      - name: Commit export to repository
        run: |
          mkdir -p exports
          mv attack2jira.json exports/attack2jira-$(date +%Y%m%d).json
          git config user.name "GitHub Actions Bot"
          git config user.email "actions@github.com"
          git add exports/
          git commit -m "Export for $(date +%Y-%m-%d)" || echo "No changes to commit"
          git push
```

**Configure Secrets**:
1. Navigate to GitHub repository → Settings → Secrets and variables → Actions
2. Add secrets:
   - `JIRA_URL`: `https://company.atlassian.net`
   - `JIRA_USERNAME`: `user@company.com`
   - `JIRA_API_TOKEN`: Your API token

### GitLab CI

Create `.gitlab-ci.yml`:

```yaml
stages:
  - export

attack2jira-export:
  stage: export
  image: python:3.9
  only:
    - schedules
  script:
    - pip install -r requirements.txt
    - python attack2jira.py -url "$JIRA_URL" -u "$JIRA_USERNAME" -a export
  artifacts:
    paths:
      - attack2jira.json
    expire_in: 90 days
```

**Configure CI/CD Variables**:
Settings → CI/CD → Variables → Add:
- `JIRA_URL`
- `JIRA_USERNAME`
- `JIRA_API_TOKEN` (masked)

## Monitoring & Logging

### Logging Best Practices

**Log Levels**:
- **INFO**: Successful operations (export completed)
- **WARNING**: Non-critical issues (rate limiting)
- **ERROR**: Failed operations (authentication failed)

**Log Rotation**:
Configure logrotate for `/home/attack2jira/logs/export.log`:

Create `/etc/logrotate.d/attack2jira`:
```
/home/attack2jira/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
}
```

### Monitoring Script Execution

Create health check script:

```bash
#!/bin/bash

LOG_FILE="/home/attack2jira/logs/export.log"
MAX_AGE_HOURS=168  # 1 week

# Check if log file exists
if [ ! -f "$LOG_FILE" ]; then
    echo "ERROR: Log file not found"
    exit 1
fi

# Check last successful export
LAST_SUCCESS=$(grep "Export completed successfully" "$LOG_FILE" | tail -1 | cut -d':' -f1-2)

if [ -z "$LAST_SUCCESS" ]; then
    echo "ERROR: No successful exports found"
    exit 1
fi

# Calculate age in hours
AGE_SECONDS=$(( $(date +%s) - $(date -d "$LAST_SUCCESS" +%s) ))
AGE_HOURS=$(( AGE_SECONDS / 3600 ))

if [ $AGE_HOURS -gt $MAX_AGE_HOURS ]; then
    echo "WARNING: Last export was $AGE_HOURS hours ago"
    exit 1
else
    echo "OK: Last export was $AGE_HOURS hours ago"
    exit 0
fi
```

Integrate with monitoring tools (Nagios, Zabbix, Datadog, etc.).

### Alerting

Send email on failure:

```bash
# In your export script, add error handling
if ! python attack2jira.py ... ; then
    echo "attack2jira export failed" | mail -s "ALERT: attack2jira Failure" admin@company.com
fi
```

## Backup Strategy

### Export Backup

Store exports with version control:

```bash
# Create dated exports
mkdir -p /home/attack2jira/exports
mv attack2jira.json /home/attack2jira/exports/attack2jira-$(date +%Y-%m-%d).json

# Initialize git repository for versioning
cd /home/attack2jira/exports
git init
git add *.json
git commit -m "Export for $(date +%Y-%m-%d)"
```

### Configuration Backup

Backup your configuration and scripts:

```bash
# Create backup archive
tar -czf attack2jira-backup-$(date +%Y%m%d).tar.gz \
  /home/attack2jira/attack2jira \
  /home/attack2jira/.secrets \
  /home/attack2jira/run-export.sh \
  /home/attack2jira/exports

# Copy to remote storage
scp attack2jira-backup-*.tar.gz backup-server:/backups/
```

### Jira Project Backup

Jira Cloud provides automated backups. Export Jira data manually:
1. Jira Settings → System → Backup manager
2. Create backup
3. Download backup file

## Disaster Recovery

### Recovery Scenarios

**Scenario 1: Lost VPS**
- Provision new VPS
- Restore from backup archive
- Reconfigure cron jobs

**Scenario 2: Lost Jira Project**
- Re-run `attack2jira.py -a initialize`
- Restore from Jira backup if available

**Scenario 3: Compromised API Token**
1. Revoke compromised token in Atlassian
2. Generate new API token
3. Update `.secrets/jira_api_token`
4. Test with manual run

### Recovery Procedures

Document recovery steps in a runbook:
```markdown
# attack2jira Disaster Recovery Runbook

## VPS Recovery
1. Provision Ubuntu 20.04 VPS
2. SSH as root: `ssh root@new-vps-ip`
3. Restore from backup: `scp backup-server:/backups/latest.tar.gz .`
4. Extract: `tar -xzf latest.tar.gz -C /`
5. Reinstall cron: `crontab -u attack2jira /home/attack2jira/crontab.bak`
6. Test: `/home/attack2jira/run-export.sh`

## API Token Rotation
1. Revoke old token: https://id.atlassian.com/manage-profile/security/api-tokens
2. Generate new token
3. Update: `echo "NEW_TOKEN" > /home/attack2jira/.secrets/jira_api_token`
4. Test: Run export manually
```

## Performance Tuning

### Optimization Tips

**Reduce Initialization Time**:
- Use fast internet connection
- Run during off-peak hours for Jira

**Export Performance**:
- Exports are fast (30-120 seconds typically)
- No tuning needed for most use cases

### Rate Limiting

Jira Cloud has API rate limits. If you hit limits:
- Reduce export frequency
- Spread multiple exports across different times
- Contact Atlassian support for rate limit increase

### Network Optimization

For slow networks:
- Run from a VPS closer to Jira's data center
- Use a CDN or proxy to cache MITRE ATT&CK data (advanced)

## Next Steps

- **Workflows**: See real-world usage patterns in [Workflows Guide](WORKFLOWS.md)
- **Monitoring**: Set up comprehensive monitoring with logs and alerts
- **Troubleshooting**: Review [Troubleshooting Guide](TROUBLESHOOTING.md) for common issues
- **API Integration**: Explore scripting options in [API Reference](API_REFERENCE.md)

For questions or issues, visit the [GitHub repository](https://github.com/mvelazco/attack2jira) or consult the [FAQ](FAQ.md).
