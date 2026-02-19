# Infrastructure Scripts

## Overview

This folder contains the Docker sandbox and validation scripts for infrastructure testing.

## Scripts

### docker_preflight_dual.sh

Launcher script for Docker sandbox environment.

**Quick start:**
```bash
~/scripts/docker_preflight_dual.sh ~/my-project
```

**Options:**
- `--dry-run` - Show what would happen without executing
- `--skip-docker-check` - Skip Docker daemon validation

### preflight_checks.sh

Validation script with 6 pre-flight checks.

**Runs automatically inside sandbox**, or manually:
```bash
/scripts/preflight_checks.sh
```

## Installation

```bash
# Make scripts executable
chmod +x *.sh

# Test basic functionality
~/scripts/docker_preflight_dual.sh ~/test-workspace
```

## Documentation

See [Docker Sandbox Guide](../docs/docker-sandbox-guide.md) for full documentation.

## Related

- **ACM-8:** Create Docker sandbox script (Complete)
- **Location:** Scripts run from `~/scripts/` for daily use
- **Project folder:** This is a documentation copy for GitHub
