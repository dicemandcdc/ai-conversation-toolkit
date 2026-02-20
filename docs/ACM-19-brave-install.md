# ACM-19: Install Brave Browser on Ubuntu

**Date:** 2026-02-20
**Sprint:** 2 (Feb 19-23, 2026)
**OS:** Ubuntu 24.04.4 LTS (noble)
**Brave Version:** 145.1.87.190

## Prerequisites
- Ubuntu 24.04.4 LTS
- sudo access
- Internet connection

## Installation Steps

### 1. Add Brave APT Repository
sudo curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg \
  https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg

sudo apt update

### 2. Install Brave Browser
sudo apt install brave-browser -y

### 3. Verify Installation
brave-browser --version
which brave-browser

### 4. Launch Brave
brave-browser &
disown %1

## Verification
- [x] Brave browser installed via apt
- [x] Brave Leo sidebar accessible
- [x] Test conversation created
- [x] Installation documented

## Known Issues
| Issue | Severity | Notes |
|-------|----------|-------|
| VMware: No 3D enabled | Low | Expected in VirtualBox VM, harmless |
| vaInitialize failed | Low | VA-API unavailable in VM, harmless |
| IPH_DiscardRing | Low | UI timing warning, harmless |

## Evidence
- Screenshot: evidence/screenshots/brave_acm19_leo_verified_20260220.png
- PR: feature/ACM-19-install-brave -> main (merged)

## References
- Brave Browser Linux Install: https://brave.com/linux/
- Jira: ACM-19
- GitHub: ai-conversation-toolkit
