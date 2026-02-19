# Linux Health Monitoring System

**Purpose:** Automated system health monitoring with email alerts

**Story:** ACM-10 (Sprint 1, 5 story points)
**Status:** ✅ Complete
**Date:** February 18, 2026

---

## Quick Start

```bash
# Run manually
~/scripts/linux_health_check.sh

# Or use the alias
health

# Check logs
ls -lh /var/log/health_checks/
```

---

## What It Monitors

1. **Disk Space** - Warns at 80%, critical at 90%
2. **Memory Usage** - Warns at 85%
3. **PostgreSQL** - Checks if service is running
4. **Docker** - Checks if daemon is running
5. **System Updates** - Reports pending updates
6. **System Load** - Shows 1/5/15 minute averages

---

## Usage

### Manual Execution
```bash
~/scripts/linux_health_check.sh
```

### Automatic Execution
Runs automatically on VM startup via systemd service.

---

## Configuration

### Email Settings
- **SMTP:** smtp.gmail.com:587
- **Auth:** App password (TLS encrypted)
- **Recipient:** Edit EMAIL_TO in script

### Thresholds
- Disk warning: 80%
- Disk critical: 90%
- Memory warning: 85%

---

## Log Files

Location: `/var/log/health_checks/`

- **health_check_YYYYMMDD_HHMMSS.log** - Manual runs
- **startup.log** - Systemd service runs

---

## Troubleshooting

### Email not sending
```bash
sudo systemctl status postfix
sudo tail -n 50 /var/log/mail.log
```

### Permission denied
```bash
sudo chown -R dicemandcdc:dicemandcdc /var/log/health_checks/
```

---

## Related Documentation

- **Test Results:** ../evidence/ACM-10_Test_Results_2026-02-18.md
- **Docker Sandbox:** docker-sandbox-guide.md
- **GitHub Permissions:** github-permission-check.md

---

## Tags

#FinOps #DevOps #Monitoring #Linux #PostgreSQL #Docker
