# attack2jira Documentation

Comprehensive documentation for attack2jira v2.0.0 - Automated MITRE ATT&CK coverage tracking in Jira.

## Overview

attack2jira is a Python tool that automates the creation and management of MITRE ATT&CK Framework coverage tracking within Atlassian Jira. It eliminates manual spreadsheet management and provides a structured, collaborative approach to measuring your organization's defensive security posture.

**Key Features**:
- Automated Jira project setup with 266+ ATT&CK technique issues
- Custom fields for tracking detection maturity, tactics, and data sources
- Hierarchical issue structure (techniques → sub-techniques)
- Export to ATT&CK Navigator JSON for visualization
- Simple CLI interface with minimal configuration

## Quick Links

### For New Users
- **[Getting Started Guide](GETTING_STARTED.md)** - Install, configure, and run your first sync
- **[Installation Guide](INSTALLATION_GUIDE.md)** - Detailed installation instructions for all platforms

### For Daily Use
- **[User Guide](USER_GUIDE.md)** - Complete command reference and usage patterns
- **[Configuration Guide](CONFIGURATION_GUIDE.md)** - Jira setup, API authentication, and advanced configuration

### For Production Deployment
- **[Deployment Guide](DEPLOYMENT_GUIDE.md)** - VPS deployment, Docker, CI/CD, and automation
- **[Workflows Guide](WORKFLOWS.md)** - Real-world usage examples and best practices

### For Developers & Integration
- **[API Reference](API_REFERENCE.md)** - Python API documentation and integration examples
- **[Architecture Guide](ARCHITECTURE.md)** - Technical architecture and design patterns

### For Troubleshooting
- **[Troubleshooting Guide](TROUBLESHOOTING.md)** - Common issues and solutions
- **[FAQ](FAQ.md)** - Frequently asked questions

## Documentation Structure

### 📘 Getting Started Guide
**[GETTING_STARTED.md](GETTING_STARTED.md)** - Your first steps with attack2jira

**Topics**:
- What is attack2jira and how does it work?
- System requirements (OS, Python, Jira)
- Installation methods (local, virtualenv, Docker)
- First-time setup (Jira Cloud, API tokens)
- Running your first sync
- Common first-time issues and solutions

**Audience**: New users, security teams evaluating the tool

**Read Time**: ~15 minutes

---

### 📗 User Guide
**[USER_GUIDE.md](USER_GUIDE.md)** - Complete usage reference

**Topics**:
- Overview of features
- Command reference (`initialize`, `export`)
- Configuration (.env, environment variables)
- Syncing techniques (flat vs. hierarchical)
- Exporting to ATT&CK Navigator
- Working with Jira (JQL, dashboards, workflows)
- Customization options
- Tips & tricks

**Audience**: Daily users, security analysts, detection engineers

**Read Time**: ~25 minutes

---

### 📙 Installation Guide
**[INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)** - Detailed installation procedures

**Topics**:
- System requirements (detailed)
- Pre-installation checklist
- Local installation
- Virtual environment installation
- Docker installation (future)
- VPS deployment
- Installation verification
- Troubleshooting installation
- Upgrading and uninstallation

**Audience**: System administrators, DevOps engineers

**Read Time**: ~20 minutes

---

### 📕 Configuration Guide
**[CONFIGURATION_GUIDE.md](CONFIGURATION_GUIDE.md)** - Setup and configuration

**Topics**:
- Jira Cloud setup (free trial, paid plans)
- API token generation and rotation
- MITRE ATT&CK API configuration
- Advanced configuration (custom projects, hiding options)
- Environment variables (for automation)
- Security best practices
- Configuration validation

**Audience**: Jira administrators, security operations managers

**Read Time**: ~18 minutes

---

### 📔 Deployment Guide
**[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Production deployment strategies

**Topics**:
- Deployment scenarios (single analyst, team, enterprise)
- Local deployment
- Docker deployment (reference implementation)
- VPS deployment (DigitalOcean, AWS, etc.)
- CI/CD integration (GitHub Actions, GitLab CI)
- Monitoring & logging
- Backup strategy
- Disaster recovery
- Performance tuning

**Audience**: DevOps, Site Reliability Engineers, Enterprise Security Teams

**Read Time**: ~22 minutes

---

### 📓 API Reference
**[API_REFERENCE.md](API_REFERENCE.md)** - Python API documentation

**Topics**:
- Module structure
- `Attack2Jira` class reference
- `JiraHandler` class reference
- Custom script examples
- JSON export format specification
- Integration examples (SIEM, detection repos, dashboards)

**Audience**: Python developers, automation engineers, integration developers

**Read Time**: ~20 minutes

---

### 🔧 Troubleshooting Guide
**[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Diagnose and fix issues

**Topics**:
- Authentication errors (401, 403)
- API rate limiting (429)
- Custom field errors
- Issue creation failures
- Navigator export issues
- Performance problems
- Network issues
- Debugging techniques

**Audience**: All users encountering issues

**Read Time**: ~15 minutes

---

### 🔄 Workflows Guide
**[WORKFLOWS.md](WORKFLOWS.md)** - Real-world usage patterns

**Topics**:
- Basic workflow: Initial project setup
- Advanced workflow: Hierarchical tracking with multiple teams
- Recurring workflow: Scheduled exports and reporting
- Integration workflow: Detection engineering and SIEM linking
- Reporting workflow: Executive dashboards
- Optimization workflow: Continuous improvement and purple teaming

**Audience**: Security operations teams, detection engineers, CISOs

**Read Time**: ~25 minutes

---

### 🏗️ Architecture Guide
**[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical architecture

**Topics**:
- System overview and design principles
- Module structure (`attack2jira.py`, `lib/jirahandler.py`)
- Data flow (initialization and export)
- API interactions (Jira REST API, MITRE ATT&CK API)
- Error handling and retry logic
- Logging & monitoring
- Extensibility and plugin architecture
- Security considerations
- Performance characteristics

**Audience**: Developers, architects, contributors

**Read Time**: ~20 minutes

---

### ❓ FAQ
**[FAQ.md](FAQ.md)** - Frequently asked questions

**Topics**:
- General questions (What is attack2jira? Why use it?)
- Installation & setup
- Usage & operations
- Integration & customization
- Troubleshooting
- Advanced topics

**Audience**: All users

**Read Time**: ~12 minutes

---

## Navigation by Role

### Security Analyst / Detection Engineer
1. [Getting Started Guide](GETTING_STARTED.md) - Initial setup
2. [User Guide](USER_GUIDE.md) - Daily usage
3. [Workflows Guide](WORKFLOWS.md) - Best practices
4. [FAQ](FAQ.md) - Quick answers

### Jira Administrator
1. [Configuration Guide](CONFIGURATION_GUIDE.md) - Jira setup
2. [Installation Guide](INSTALLATION_GUIDE.md) - Installation
3. [Troubleshooting Guide](TROUBLESHOOTING.md) - Fix issues

### DevOps / Site Reliability Engineer
1. [Deployment Guide](DEPLOYMENT_GUIDE.md) - Production deployment
2. [Installation Guide](INSTALLATION_GUIDE.md) - Installation methods
3. [Architecture Guide](ARCHITECTURE.md) - Technical details

### Python Developer / Automation Engineer
1. [API Reference](API_REFERENCE.md) - Python API
2. [Architecture Guide](ARCHITECTURE.md) - Code structure
3. [Workflows Guide](WORKFLOWS.md) - Integration patterns

### CISO / Security Manager
1. [Getting Started Guide](GETTING_STARTED.md) - Overview
2. [Workflows Guide](WORKFLOWS.md) - Usage examples
3. [FAQ](FAQ.md) - Business questions

## Getting Help

### Documentation Search

Can't find what you're looking for? Use your browser's search (Ctrl/Cmd+F) or try these keywords:

- **Installation problems**: [Installation Guide](INSTALLATION_GUIDE.md), [Troubleshooting](TROUBLESHOOTING.md)
- **Authentication errors**: [Configuration Guide](CONFIGURATION_GUIDE.md), [Troubleshooting](TROUBLESHOOTING.md#authentication-errors)
- **Export issues**: [User Guide](USER_GUIDE.md#exporting-navigator-json), [Troubleshooting](TROUBLESHOOTING.md#navigator-export-issues)
- **Automation**: [Deployment Guide](DEPLOYMENT_GUIDE.md#cicd-integration), [Workflows](WORKFLOWS.md#recurring-workflow-scheduled-exports)
- **Python scripting**: [API Reference](API_REFERENCE.md)
- **Performance**: [Troubleshooting](TROUBLESHOOTING.md#performance-problems), [Architecture](ARCHITECTURE.md#performance-characteristics)

### External Resources

- **GitHub Repository**: [github.com/mvelazco/attack2jira](https://github.com/mvelazco/attack2jira)
- **ATT&CKCon Presentation**: [YouTube - attack2jira at ATT&CKCon 2.0](https://www.youtube.com/watch?v=hrzR8TpnjAw)
- **Blog Post**: [Tracking and Measuring ATT&CK Coverage](https://medium.com/@mvelazco/tracking-and-measuring-att-ck-coverage-with-attack2jira-fe700e2a1654)
- **Live Demo**: [attack.atlassian.net](https://attack.atlassian.net/jira/software/c/projects/ATTACK/issues/)
- **MITRE ATT&CK**: [attack.mitre.org](https://attack.mitre.org)
- **ATT&CK Navigator**: [mitre-attack.github.io/attack-navigator](https://mitre-attack.github.io/attack-navigator/)

### Community Support

- **GitHub Issues**: [Search existing issues](https://github.com/mvelazco/attack2jira/issues) or open a new one
- **Feature Requests**: Submit via GitHub Issues with the "enhancement" label
- **Bug Reports**: Include error messages, Python version, OS, and steps to reproduce

### Contributing

attack2jira is open-source! Contributions are welcome:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [Architecture Guide](ARCHITECTURE.md#extensibility) for extension points.

## License

attack2jira is licensed under the **BSD 3-Clause License**.

Copyright (c) Mauricio Velazco (@mvelazco) and Olindo Verrillo (@olindoverrillo)

See [LICENSE](../LICENSE) file for details.

## Authors

- **Mauricio Velazco** - [@mvelazco](https://twitter.com/mvelazco)
- **Olindo Verrillo** - [@olindoverrillo](https://twitter.com/olindoverrillo)

## Acknowledgments

- [MITRE ATT&CK Framework](https://attack.mitre.org) - The foundation for this tool
- [ATTACK-Python-Client](https://github.com/hunters-forge/ATTACK-Python-Client) - ATT&CK API wrapper
- Atlassian Jira - Collaboration platform
- The security community for feedback and contributions

---

**Last Updated**: 2024
**Documentation Version**: 2.0.0
**attack2jira Version**: 2.0.0 (compatible)

For the latest updates, visit the [GitHub repository](https://github.com/mvelazco/attack2jira).
