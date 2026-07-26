# Changelog
All notable changes to 1ai-skills are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/).

## [3.15.0] — 2026-07-26

### Added
- `schemas/skill.schema.json` — JSON Schema Draft-07 validator (23 properties, 7 required,
  conditional high/critical risk validation)
- `docs/SKILL_STANDARD.md` — SKILL.md schema reference and writing standards
- `docs/SKILL_QUALITY_RUBRIC.md` — 5-dimension quality scoring rubric
- `docs/SKILL_VERSIONING.md` — semantic versioning policy for skills
- `scripts/validate-skill-schema.py` — schema compliance checker (1347/1347 pass, 0 errors)
- `scripts/fix-skill-compliance.py` — automated compliance remediation

### Fixed
- 18 bracket-style YAML tags converted to proper block-style across cybersecurity (3),
  core (4), development (5), devops (1), integrations (1), meta (1), and productivity (3)
- 2 unquoted numeric tags (`802.11`) quoted in wireless penetration test skills
- 1 duplicate tag entry removed in `clay-art-video-generator`
- 10 domain/category path mismatches corrected:
  - `domain: video` → `domain: content` (3 files)
  - `domain: path` → `domain: category` (4 files)
  - `category: investment` → `category: finance` (3 files)
- README.md skill count reduced from 1348 to 1347; cybersecurity count updated 786→790

### Changed
- Lint: 0 errors, 0 warnings, 3152 info messages
- Tests: 1344/1344 pass

## [3.14.0] — 2026-07-26

### Fixed
- YAML frontmatter parser — handles multi-line and split-line values correctly
- 113 lint warnings resolved: missing "Use when" triggers, missing frontmatter tags,
  over-length descriptions, and non-standard section headers

### Changed
- 8 skills deepened to ~600-1500 lines with working code, case studies, and
  anti-rationalization tables (telegram-bot, whatsapp-bot, n8n-builder, smart-scraper,
  cron-designer, kb, docker-compose, dockerfile-opt)

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
- Initial 1337 skill library across 19 categories
- SKILLS.json machine-readable catalog
- Category-based directory structure
- YAML frontmatter standard for all skills
- npm package with postinstall hooks
