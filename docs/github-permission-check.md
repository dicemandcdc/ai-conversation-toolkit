# GitHub Permission Check Script

**Script:** github_perm_check.sh
**Story:** ACM-9
**Sprint:** Sprint 1
**Date:** 2026-02-17

## Purpose

Validates GitHub repository permissions via the GitHub API to ensure users have the correct access level before performing operations.

## Why This Matters

**Real-World Context:**
- FinBank-Omega Incident (2023): A deployment script assumed users had write access without verifying. An intern with read-only access triggered a failed deployment that caused 120k EUR in downtime.
- This script prevents permission-related deployment failures by validating access before operations.

## Features

1. Token validation - Verifies GitHub PAT exists and has correct permissions
2. API rate limit check - Ensures API quota is available
3. Permission detection - Identifies admin/write/read/none access
4. Error handling - Gracefully handles 401/403/404 responses
5. Audit logging - Timestamped logs in ~/.cache/github-checks/

## Requirements

- GitHub Personal Access Token with repo scope
- Token stored in ~/.config/github/token (chmod 600)
- curl installed
- jq installed (optional, for detailed output)

## Usage Examples

Check permissions on finops-playground:
  ~/scripts/github_perm_check.sh dicemandcdc finops-playground

Check permissions on pg-role-playbook:
  ~/scripts/github_perm_check.sh dicemandcdc pg-role-playbook

## Output Example

When checking finops-playground repository:
- Step 1: Token file validated
- Step 2: API rate limit checked (5000/5000 remaining)
- Step 3: Repository found (HTTP 200)
- Step 4: Permission level: ADMIN (full control)
- Result: Permission check completed successfully

## Exit Codes

- 0 = Success (admin/write/read access confirmed)
- 1 = Error (no access, invalid token, API error)
- 2 = Usage error (missing arguments)

## Log Files

Logs stored in: ~/.cache/github-checks/
Format: github_perm_check_YYYYMMDD_HHMMSS.log

## Troubleshooting

Token file not found:
  mkdir -p ~/.config/github
  echo "YOUR_TOKEN" > ~/.config/github/token
  chmod 600 ~/.config/github/token

Authentication failed (401):
  - Token is invalid or expired
  - Create new token at: https://github.com/settings/tokens

Access forbidden (403):
  - Token lacks required scopes
  - Ensure token has repo scope

Repository not found (404):
  - Check repository name spelling
  - Verify repository exists and token has access

## Security Notes

- Token stored in ~/.config/github/token (outside Git repos)
- File permissions: 600 (owner read/write only)
- Token never logged or displayed
- Logs stored in ~/.cache/ (temporary location)

## Related Scripts

- docker_preflight_dual.sh - Docker sandbox (ACM-8)
- preflight_checks.sh - Validation checks (ACM-8)
- linux_health_monitor.sh - System health (ACM-10, future)

## Test Results

Tested against: dicemandcdc/finops-playground
Result: ADMIN access confirmed
Date: 2026-02-17
Log: github_perm_check_20260217_174946.log

