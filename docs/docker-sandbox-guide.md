# Docker Sandbox Guide

## Overview

The Docker sandbox provides an isolated Ubuntu 24.04 environment for testing infrastructure scripts without affecting the host system.

## Purpose

- Test scripts safely before production deployment
- Validate environment configurations
- Provide audit-ready logs for compliance
- Prevent infrastructure drift incidents (see: FinBank-Omega €250k case)

## Scripts

### docker_preflight_dual.sh

**Location:** `scripts/docker_preflight_dual.sh`

**Purpose:** Launcher script that creates disposable Ubuntu container

**Usage:**

```bash
# Basic usage
~/scripts/docker_preflight_dual.sh ~/my-project

# Dry-run mode (no system modifications)
~/scripts/docker_preflight_dual.sh ~/my-project --dry-run

# Skip Docker check
~/scripts/docker_preflight_dual.sh ~/my-project --skip-docker-check
```

**Features:**
- ✅ Spins up Ubuntu 24.04 container
- ✅ Mounts workspace directory at `/workspace`
- ✅ Installs git, python3, pip3, curl
- ✅ Auto-destroys container on exit
- ✅ Binds `/scripts` directory for validation

**Environment Variables:**
- `IN_SANDBOX=1` - Signals scripts they are running in container
- `LOG_FILE` - Path to health check log file
- `SKIP_DOCKER` - Whether to skip Docker daemon checks

### preflight_checks.sh

**Location:** `scripts/preflight_checks.sh`

**Purpose:** Validation script that runs 6 pre-flight checks

**Usage:**

```bash
# Inside container (launched by docker_preflight_dual.sh)
/scripts/preflight_checks.sh

# Dry-run mode
/scripts/preflight_checks.sh --dry-run
```

**Checks Performed:**

1. ✅ **Python environment** - Verifies Python 3.x available
2. ✅ **Git configuration** - Checks git installation
3. ✅ **Workspace files** - Validates README.md presence (warning if missing)
4. ✅ **File permissions** - Ensures scripts are executable
5. ✅ **Python dependencies** - Validates requirements.txt (optional)
6. ✅ **Shell script syntax** - Runs `bash -n` validation

**Exit Codes:**
- `0` - All critical checks passed
- `1` - Required component missing or critical error

**Output:**
- Color-coded console output (✅/⚠️/❌)
- JSON summary for automation
- Log file at `$LOG_FILE`

## Test Results

**Date:** February 16, 2026
**Environment:** Ubuntu 24.04 host, Docker 29.2.1
**Status:** ✅ ALL CHECKS PASSED

```json
{
  "timestamp": "2026-02-16T16:35:50+00:00",
  "status": "PASS",
  "checksPerformed": 6,
  "logFile": "/home/dicemandcdc/scripts/health_logs/preflight_2026-02-16.log"
}
```

## Real-World Impact

This sandbox prevents infrastructure drift incidents like the **FinBank-Omega case** where undetected PostgreSQL role misconfiguration caused **€250k in losses**.

**How it helps:**
- Pre-flight validation catches misconfigurations before deployment
- Isolated testing prevents production contamination
- Audit logs provide compliance trail
- Automated checks reduce human error

## Installation

### For Daily Use

The scripts are designed to run from `~/scripts/`:

```bash
# Run from original location
~/scripts/docker_preflight_dual.sh ~/test-workspace
```

### For Development/Testing

If you want to run from this project directory, update the mount path in `docker_preflight_dual.sh`:

```bash
# Line ~95: Change from
-v "$HOME/scripts:/scripts" \

# To
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE}")" && pwd)"
-v "$SCRIPT_DIR:/scripts" \
```

*Note: This enhancement is tracked in backlog item AICM-13 (low priority).*

## Troubleshooting

### Issue: Docker daemon not running

```bash
sudo systemctl status docker
sudo systemctl start docker
```

### Issue: Permission denied

```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Log out and back in
```

### Issue: Scripts not executable

```bash
chmod +x scripts/*.sh
```

## Architecture

```
Host System (Ubuntu 24.04)
 │
 ├─ docker_preflight_dual.sh (launcher)
 │   ├─ Creates Ubuntu 24.04 container
 │   ├─ Mounts /workspace and /scripts
 │   └─ Sets IN_SANDBOX=1
 │
 └─ Container (Isolated Ubuntu 24.04)
     │
     └─ preflight_checks.sh (validator)
         ├─ 6 validation checks
         ├─ JSON logging
         └─ Exit codes (0=success, 1=failure)
```

## Related Documentation

- Infrastructure Safeguards (to be created)
- Test Results (to be created)
- Sprint 1 Retrospective (Confluence)

## Related Jira Stories

- **ACM-8:** Create Docker sandbox script ✅ (Complete)
- **ACM-7:** Pre-ACM-5 Infrastructure Safeguards Setup (In Progress)
- **AICM-13:** Make scripts location-independent (Backlog - Low Priority)
