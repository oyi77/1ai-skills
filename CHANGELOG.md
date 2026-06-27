# Changelog

All notable changes to 1ai-skills are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/).

## [3.6.0] — 2026-06-28

### Fixed
- Replaced placeholder content in 696 skills across all 19 categories
- Fixed 2 duplicate descriptions (`meta/data`, `trading/polymarket`)
- Fixed 8 broken internal `/skills/` links
- Fixed 1 short description (`performing-nist-csf-maturity-assessment`)
- Added missing `## Overview` to 6 skills
- Added `sales/sales-pipeline` to SKILLS.json (was orphaned)

### Added
- `hooks/auto-evolve/skill-banner.js` — ASCII art banner on skill activation
- `LICENSE` (MIT)
- `SECURITY.md`
- `CHANGELOG.md`
- `.github/ISSUE_TEMPLATE/bug_report.md`
- `.github/ISSUE_TEMPLATE/feature_request.md`
- `.github/ISSUE_TEMPLATE/skill_request.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/CODEOWNERS`
- Batch fix scripts for placeholder content

### Changed
- `scripts/install-hooks.js` — respects manifest `timeout` field
- `hooks/hooks.json` — registered banner hook

## [3.5.0] — 2026-06-17

### Added
- Auto-evolve hooks system (tracker, committer, feedback, evolver)
- Session-start hooks with project type detection
- Pre-commit hooks for SKILL.md validation
- `scripts/hooks-cli.js` — hooks management CLI
- `scripts/install-hooks.js` — auto-installer for Claude hooks
- `scripts/audit-skills.sh` — skill counting and SKILLS.json generation
- `scripts/validate-skills.py` — structural validation
- `scripts/lint-skills.py` — content linting

## [3.0.0] — 2026-05-01

### Added
- Initial 1319 skill library across 19 categories
- SKILLS.json machine-readable catalog
- Category-based directory structure
- YAML frontmatter standard for all skills
- npm package with postinstall hooks
