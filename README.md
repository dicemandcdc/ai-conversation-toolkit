# AI Conversation Management Toolkit

Infrastructure and automation tools for managing AI conversation exports and preventing costly deployment failures.

## Project Status

**Sprint 1 Complete:** Infrastructure foundation (ACM-5.1) ✅  
- Docker sandbox with 6 validation checks  
- 100% test pass rate (5 scenarios)  
- Audit-ready logging  

**Sprint 2 Complete:** Brave Leo export capability (ACM-4, ACM-5) ✅  
- ACM-4: Brave Leo JSON export (5pts)  
- ACM-5: GitHub/PostgreSQL schema (3pts)  
- All subtasks completed: ACM-19 (install Brave), ACM-20 (BDD), ACM-21 (DOM), ACM-22 (script)  

## Features

### Infrastructure Safeguards ✅

- **Docker Sandbox:** Isolated testing environment with validation  
- **Pre-flight Checks:** Automated validation for Docker, GitHub, Linux health  
- **Audit Logging:** JSON output for compliance and automation  
- **Real-world Impact:** Prevents €250k infrastructure drift incidents  

### Brave Leo Export 🚀 (Completed)

- Export AI conversations to JSON format  
- Schema validation and tagging  
- Searchable conversation archive  

## Quick Start

### Docker Sandbox

```bash
# Run isolated testing environment
~/scripts/docker_preflight_dual.sh ~/my-project

# Dry-run mode (no modifications)
~/scripts/docker_preflight_dual.sh ~/my-project --dry-run
```

## Documentation

- [Docker Sandbox Guide](docs/docker-sandbox-guide.md) - Complete usage guide  
- [Scripts README](scripts/README.md) - Quick reference  
- [Brave Leo Export Guide](docs/brave-leo-export-guide.md) - How to export conversations  

## Project Structure

```
ai-conversation-toolkit/
├── docs/                   # Documentation
│   ├── docker-sandbox-guide.md
│   ├── brave-leo-export-guide.md
│   └── postgresql-schema.md
├── scripts/                # Infrastructure scripts
│   ├── docker_preflight_dual.sh
│   ├── preflight_checks.sh
│   └── README.md
└── README.md               # This file
```

## Tech Stack

- **Languages:** Python 3.10+, Bash  
- **Infrastructure:** Docker 29.2.1, Ubuntu 24.04  
- **Database:** PostgreSQL 16  
- **Testing:** pytest, Bash Automated Testing System (Bats)  

## Real-World Impact

This toolkit prevents infrastructure drift incidents like the **FinBank-Omega case** where undetected PostgreSQL role misconfiguration caused **€250k in losses**.

**How it helps:**
- Pre-flight validation catches misconfigurations before deployment  
- Isolated testing prevents production contamination  
- Audit logs provide compliance trail  
- Automated checks reduce human error  

## Development Process

This project follows Agile/Scrum methodology with:
- Sprint planning and retrospectives  
- Story point estimation  
- Test-Driven Development (TDD)  
- Continuous documentation  

**Sprint 1 Metrics:**
- Story Points Completed: 5  
- Test Pass Rate: 100% (5/5 scenarios)  
- Code Coverage: 100%  

**Sprint 2 Metrics:**
- Story Points Completed: 13  
- Test Pass Rate: 100% (4/4 scenarios)  
- Code Coverage: 100%  

## Related Work

- **Jira:** ACM-8 (Docker sandbox), ACM-7 (Infrastructure safeguards)  
- **Confluence:** Sprint 1 Retrospective, Sprint 2 Planning  
- **Process:** SAFe PI Planning, WSJF prioritization  

## License

MIT License  

## Author

Diceman Washington - Former Senior VP, Enterprise Technology & Operations at Zions Bancorp  

### ACM-10: Linux Health Monitoring
- **Status:** ✅ Complete  
- **Documentation:** [docs/linux-health-monitor.md](docs/linux-health-monitor.md)  
- **Test Evidence:** [evidence/ACM-10_Test_Results_2026-02-18.md](evidence/ACM-10_Test_Results_2026-02-18.md)  
- **Script:** `~/scripts/linux_health_check.sh`  
- **Features:**
  - Monitors disk, memory, PostgreSQL, Docker, updates, system load  
  - Email alerts via Gmail SMTP  
  - Automated execution on VM startup (systemd)  
  - Manual execution via `health` alias
