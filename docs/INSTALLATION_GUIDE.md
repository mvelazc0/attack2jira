# attack2jira Installation Guide

This guide provides detailed installation instructions for attack2jira across different platforms and deployment scenarios.

## Table of Contents

- [System Requirements](#system-requirements)
- [Pre-Installation Checklist](#pre-installation-checklist)
- [Local Installation](#local-installation)
- [Virtual Environment Installation](#virtual-environment-installation)
- [Docker Installation](#docker-installation)
- [VPS Deployment](#vps-deployment)
- [Installation Verification](#installation-verification)
- [Troubleshooting Installation](#troubleshooting-installation)
- [Upgrading](#upgrading)
- [Uninstallation](#uninstallation)

## System Requirements

### Operating Systems

**Linux** (Recommended):
- Kali Linux 2018.4 or later
- Ubuntu 18.04 LTS or later
- Debian 9 (Stretch) or later
- CentOS 7 or later
- Fedora 28 or later
- Arch Linux (current)

**macOS**:
- macOS 10.14 (Mojave) or later
- macOS 11.0 (Big Sur) or later recommended

**Windows**:
- Windows 10 version 1809 or later
- Windows 11 (all versions)
- Windows Server 2016 or later

### Python Requirements

**Python Version**:
- **Minimum**: Python 3.6
- **Recommended**: Python 3.7 or later
- **Tested**: Python 3.6, 3.7, 3.8, 3.9, 3.10, 3.11

**Required Python Components**:
- pip3 (Python package installer)
- setuptools
- wheel (for binary package installation)

**Verify Python Installation**:
```bash
python3 --version
# Output should be: Python 3.6.x or higher

pip3 --version
# Output should show pip version and Python 3.x
```

### Jira Requirements

**Jira Platform**:
- Jira Cloud (Jira Software) - **Required**
- Jira Server/Data Center - **Not Supported**

**Jira Access**:
- Valid Jira Cloud account
- Admin privileges (ability to create projects and custom fields)
- API token generated from Atlassian account

**Jira Plan**:
- Free trial (up to 10 users) - Supported
- Standard plan - Supported
- Premium plan - Supported
- Enterprise plan - Supported

### Network Requirements

**Internet Connectivity**:
- Outbound HTTPS (port 443) access to:
  - Your Jira Cloud instance (`*.atlassian.net`)
  - MITRE ATT&CK API (`cti-taxii.mitre.org`)
  - GitHub (for cloning repository: `github.com`)

**Bandwidth**:
- Minimum: 1 Mbps
- Recommended: 5+ Mbps for faster initialization

**Firewall Considerations**:
- No inbound ports required (attack2jira is client-only)
- Corporate firewalls must allow outbound HTTPS to Atlassian and MITRE domains

### Disk Space

- **Minimum**: 50 MB (for tool and dependencies)
- **Recommended**: 500 MB (for virtual environments and exports)
- **Temporary Space**: 100 MB during installation

### Memory

- **Minimum**: 512 MB RAM
- **Recommended**: 1 GB+ RAM
- No significant memory usage during operation

## Pre-Installation Checklist

Before installing attack2jira, complete these prerequisites:

- [ ] Python 3.6+ installed and verified (`python3 --version`)
- [ ] pip3 installed and verified (`pip3 --version`)
- [ ] Jira Cloud instance access (URL and admin credentials ready)
- [ ] Jira API token generated and stored securely
- [ ] Internet connectivity to Atlassian and MITRE domains verified
- [ ] Git installed (for cloning repository)
- [ ] Command-line terminal available

## Local Installation

This method installs attack2jira directly on your system. Best for single-user environments or quick testing.

### Step 1: Install Git (if not already installed)

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install -y git
```

**CentOS/RHEL**:
```bash
sudo yum install -y git
```

**macOS** (using Homebrew):
```bash
brew install git
```

**Windows**:
Download and install from [git-scm.com](https://git-scm.com/download/win)

### Step 2: Clone the Repository

```bash
# Clone from GitHub
git clone https://github.com/mvelazco/attack2jira.git

# Navigate to the directory
cd attack2jira
```

**Alternative - Download ZIP**:
If you don't have git:
1. Visit [https://github.com/mvelazco/attack2jira](https://github.com/mvelazco/attack2jira)
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file
4. Navigate to the extracted directory

### Step 3: Install Dependencies

```bash
pip3 install -r requirements.txt
```

**Expected Output**:
```
Collecting attackcti
  Downloading attackcti-x.x.x-py3-none-any.whl
Collecting stix2 (from attackcti)
  Downloading stix2-x.x.x-py3-none-any.whl
...
Successfully installed attackcti-x.x.x stix2-x.x.x ...
```

### Step 4: Verify Installation

```bash
python3 attack2jira.py -h
```

**Expected Output**:
```
usage: attack2jira.py [-h] -url URL -u U -a {initialize,export} [-p P] [-k K] [-hide]

optional arguments:
  -h, --help            show this help message and exit
  ...
```

If you see the help message, installation is successful!

### Troubleshooting Local Installation

**Issue: "pip3: command not found"**

Solution:
```bash
# Ubuntu/Debian
sudo apt install python3-pip

# macOS
brew install python3

# Windows
# Reinstall Python from python.org and check "Add to PATH"
```

**Issue: Permission denied**

Solution - Use user installation:
```bash
pip3 install --user -r requirements.txt
```

**Issue: SSL certificate errors**

Solution:
```bash
pip3 install --upgrade certifi
# or
pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

## Virtual Environment Installation

Virtual environments isolate attack2jira dependencies from other Python projects. **Recommended for production use**.

### Benefits of Virtual Environments

- No dependency conflicts with other Python tools
- Easy to delete and recreate
- Reproducible environments
- Best practice for Python development

### Step 1: Install virtualenv (if needed)

```bash
pip3 install virtualenv
```

### Step 2: Clone the Repository

```bash
git clone https://github.com/mvelazco/attack2jira.git
cd attack2jira
```

### Step 3: Create Virtual Environment

```bash
# Create virtual environment named 'venv'
python3 -m venv venv
```

This creates a `venv/` directory containing an isolated Python environment.

### Step 4: Activate Virtual Environment

**Linux/macOS**:
```bash
source venv/bin/activate
```

**Windows (Command Prompt)**:
```cmd
venv\Scripts\activate.bat
```

**Windows (PowerShell)**:
```powershell
venv\Scripts\Activate.ps1
```

After activation, your prompt should show `(venv)`:
```
(venv) user@host:~/attack2jira$
```

### Step 5: Install Dependencies

With the virtual environment activated:
```bash
pip install -r requirements.txt
```

Note: Use `pip` instead of `pip3` inside virtual environments.

### Step 6: Verify Installation

```bash
python attack2jira.py -h
```

### Step 7: Deactivate (when done)

```bash
deactivate
```

### Using attack2jira with Virtual Environment

Every time you want to use attack2jira:

```bash
cd /path/to/attack2jira
source venv/bin/activate  # Activate environment
python attack2jira.py -url ... -u ... -a initialize
deactivate  # Deactivate when done
```

### Creating a Wrapper Script

For convenience, create a script `run.sh`:

```bash
#!/bin/bash
cd /path/to/attack2jira
source venv/bin/activate
python attack2jira.py "$@"
deactivate
```

Make it executable:
```bash
chmod +x run.sh
```

Usage:
```bash
./run.sh -url https://site.atlassian.net -u user@domain.com -a export
```

## Docker Installation

Docker support is **planned for a future release** but not currently available in the repository.

### Planned Docker Features

- Pre-built Docker image with all dependencies
- No local Python installation required
- Consistent environment across platforms
- Easy updates via image pulls

### Manual Docker Setup (Advanced)

Until official Docker support is released, you can create a custom Dockerfile:

**Dockerfile**:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY attack2jira.py .
COPY lib/ lib/

# Set entrypoint
ENTRYPOINT ["python", "attack2jira.py"]
```

**Build and Run**:
```bash
# Build image
docker build -t attack2jira:latest .

# Run with environment variables
docker run -it attack2jira:latest \
  -url https://site.atlassian.net \
  -u user@domain.com \
  -a initialize
```

**Note**: This is experimental and not officially supported.

## VPS Deployment

Deploy attack2jira on a Virtual Private Server for scheduled exports and team access.

### Recommended VPS Providers

- **Hostinger VPS**: Budget-friendly, good performance
- **DigitalOcean**: Developer-friendly, extensive documentation
- **Linode**: Reliable, simple pricing
- **AWS EC2**: Enterprise-grade, pay-per-use
- **Google Cloud Compute Engine**: Integrated with GCP services
- **Vultr**: Fast deployment, global locations

### Step 1: Provision VPS

**Minimum Specifications**:
- **OS**: Ubuntu 20.04 LTS or later
- **CPU**: 1 vCore
- **RAM**: 1 GB
- **Storage**: 20 GB SSD
- **Network**: 1 TB bandwidth/month

**Recommended Specifications**:
- **CPU**: 2 vCores
- **RAM**: 2 GB
- **Storage**: 40 GB SSD

### Step 2: Initial VPS Setup

Connect via SSH:
```bash
ssh root@your-vps-ip
```

Update system:
```bash
apt update && apt upgrade -y
```

Install Python and Git:
```bash
apt install -y python3 python3-pip python3-venv git
```

Create a dedicated user:
```bash
adduser attack2jira
usermod -aG sudo attack2jira
su - attack2jira
```

### Step 3: Install attack2jira

```bash
cd ~
git clone https://github.com/mvelazco/attack2jira.git
cd attack2jira

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure Firewall

```bash
# Enable UFW firewall
sudo ufw allow OpenSSH
sudo ufw enable

# No inbound ports needed for attack2jira (client-only)
```

### Step 5: Set Up Scheduled Exports

Create a script for automated exports (see [Deployment Guide](DEPLOYMENT_GUIDE.md) for details).

### Step 6: Secure API Token

Store your Jira API token securely:
```bash
# Create a secure file
echo "YOUR_API_TOKEN" > ~/.jira_token
chmod 600 ~/.jira_token
```

Modify scripts to read from this file instead of interactive input.

## Installation Verification

After installation, verify everything works correctly.

### Test 1: Help Command

```bash
python3 attack2jira.py -h
```

**Expected**: Help message displays without errors.

### Test 2: Python Dependencies

```bash
python3 -c "import attackcti; print('attackcti imported successfully')"
```

**Expected**: "attackcti imported successfully"

### Test 3: Network Connectivity

Test Jira connectivity:
```bash
curl -I https://yoursite.atlassian.net
```

**Expected**: HTTP 200 or 301 response

Test MITRE ATT&CK connectivity:
```bash
curl -I https://cti-taxii.mitre.org
```

**Expected**: HTTP 200 or 301 response

### Test 4: Authentication

Run a non-destructive command (export on non-existent project):
```bash
python3 attack2jira.py -url https://yoursite.atlassian.net -u user@domain.com -a export
```

If authentication works, you'll see an error about the project not existing (expected).
If authentication fails, you'll see "401 Unauthorized" (indicates credential issue).

## Troubleshooting Installation

### Python Version Mismatch

**Symptoms**: "SyntaxError" or "unsupported Python version"

**Check Python version**:
```bash
python3 --version
```

**Solution**: Install Python 3.6+:
```bash
# Ubuntu/Debian
sudo apt install python3.9

# Use specific version
python3.9 attack2jira.py -h
```

### Dependency Installation Fails

**Symptoms**: "Could not find a version that satisfies the requirement"

**Solutions**:
```bash
# Update pip
pip3 install --upgrade pip setuptools wheel

# Try installing with verbose output
pip3 install -v -r requirements.txt

# Install individually
pip3 install attackcti
```

### Git Clone Fails

**Symptoms**: "fatal: unable to access", SSL errors

**Solutions**:
```bash
# Use HTTPS instead of git://
git clone https://github.com/mvelazco/attack2jira.git

# If behind a proxy
git config --global http.proxy http://proxy.example.com:8080
```

### Virtual Environment Activation Fails

**Windows PowerShell - Execution Policy Error**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Linux - Permission Issues**:
```bash
chmod +x venv/bin/activate
source venv/bin/activate
```

## Upgrading

To upgrade attack2jira to the latest version:

### Step 1: Pull Latest Code

```bash
cd /path/to/attack2jira
git pull origin main
```

### Step 2: Update Dependencies

```bash
# If using virtual environment
source venv/bin/activate

# Update dependencies
pip install --upgrade -r requirements.txt
```

### Step 3: Verify

```bash
python3 attack2jira.py -h
```

### Checking for Updates

```bash
cd /path/to/attack2jira
git fetch
git status
# If "Your branch is behind", run git pull
```

## Uninstallation

To completely remove attack2jira:

### Step 1: Delete Repository

```bash
rm -rf /path/to/attack2jira
```

### Step 2: Remove Virtual Environment (if used)

Already deleted with the repository directory.

### Step 3: Remove Global Dependencies (optional)

Only if you installed globally and want to clean up:
```bash
pip3 uninstall attackcti stix2 -y
```

### Step 4: Delete Jira Project (optional)

If you want to remove the Jira project:
1. Log in to Jira
2. Navigate to Project Settings
3. Click "Move to trash"
4. Permanently delete from trash after 60 days (or immediately)

**Warning**: This deletes all issues and history. Export data first if needed.

## Next Steps

- **Configuration**: Set up your Jira instance in [Configuration Guide](CONFIGURATION_GUIDE.md)
- **Usage**: Learn how to use attack2jira in [User Guide](USER_GUIDE.md)
- **Production Deployment**: Deploy for team use in [Deployment Guide](DEPLOYMENT_GUIDE.md)
- **Troubleshooting**: If you encounter issues, see [Troubleshooting Guide](TROUBLESHOOTING.md)

For additional help, visit the [GitHub repository](https://github.com/mvelazco/attack2jira) or consult the [FAQ](FAQ.md).
