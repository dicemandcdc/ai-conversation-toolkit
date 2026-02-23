# Release Notes

## Version 1.0 — ACM-5 Completion
**Release Date:** 2026-02-23

### Overview
Version 1.0 marks the completion of the AI Conversation Management Toolkit
foundation. This release establishes the full repository structure, PostgreSQL
schema, and Brave Leo export capability.

### What's in this release

#### Repository Structure
- All top-level folders created: snippets/, docs/, tests/, schema/, exports/, evidence/
- All folders have README.md with purpose and cross-links
- GitHub topics added: finops, postgresql, python, portfolio, ai-tools
- TOPICS.md added for audit trail

#### PostgreSQL Schema
- conversations table with ACM-24 future-proofing fields
- messages table with message_order for conversation reconstruction
- JSON Schema Draft-07 for export validation
- Indexes for performance

#### Brave Leo Export Capability
- brave_leo_export.js script for manual DevTools export
- BDD tests passing (pytest-bdd)
- DOM inspection documented

#### Infrastructure
- Docker sandbox (docker_preflight_dual.sh)
- Preflight validation script (preflight_checks.sh)
- Linux health monitor
- .gitignore hardened for secrets, Docker, logs, IDE artefacts

### Sprints Completed
- Sprint 1: Infrastructure foundation (ACM-5.1, ACM-7, ACM-8, ACM-9, ACM-10)
- Sprint 2: Brave Leo export capability (ACM-4, ACM-18, ACM-19, ACM-20, ACM-21, ACM-22)
- ACM-5: GitHub repository & PostgreSQL schema (ACM-25 through ACM-30)

### Verification
- tree output matches expected layout ✅
- GitHub topics verified via API ✅
- All PRs merged cleanly (PR #3 through PR #10) ✅
- BDD tests passing ✅

### Known Gaps (Deferred to Backlog)
- ACM-32: Schema documentation in GitHub Wiki
- ACM-33: CI/CD pipeline for repo structure validation
- ACM-34: Run full pytest suite verification
- ACM-35: Document manual export workflow in Confluence

### Next Steps
- ACM-24: Conversation Reconstruction Export (Version 2)
- Sprint 3 planning
- LinkedIn post publication (EOD 2/28/2026)
