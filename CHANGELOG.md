# Changelog
All notable changes to 1ai-skills are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/).

## [3.20.0] — 2026-07-26

### Changed
- 48 thin/stub skills deepened to 80–140 lines with redirect notes, domain overviews,
  Quick Start guides, focused code examples, verification checklists (5–7 items), and
  anti-rationalization tables (3–4 domain-specific rows)
- 15 files fixed post-deepening: Python syntax error in `anomaly-detect`, 14 missing
  `## When to Use` sections added (derived from frontmatter descriptions)
- 14 files had `## Workflow` sections auto-generated via `scripts/bulk-add-workflow.py`
  (fixed 28/29, remaining 15 fixed with targeted `## When to Use` insertion)
- SKILLS.json regenerated via `lint-skills.py --write` to sync catalog

### Verified
- Lint: 0 errors, 0 warnings, 2572 info
- Tests: 1344/1344 pass
- Schema: 1347/1347 pass (0 errors, 212 warnings)

### Removed
- `scripts/bulk-add-workflow.py` — one-off Phase 3d migration script (YAGNI)
- `scripts/bulk-fix-when-to-use.py` — one-off Phase 3d fix script (YAGNI)

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

## [3.16.0] — 2026-07-26

### Added
- `scripts/audit-skills.py` — multi-dimensional audit script (frontmatter quality, body
  structure, content depth, cross-references, code quality, stub detection, security red flags)
- `reports/audit-report.json` — full audit output: avg score 43.0%, 1342 F-grade, 16 CRITICAL
- `reports/fix-report.txt` — actionable fix list grouped by severity

### Changed
- Lint: 0 errors, 0 warnings, 3152 info messages
- Schema: 1347/1347 pass (0 errors, 212 warnings)
- Tests: 1344/1344 pass

### Verified
- All 16 CRITICAL security_redflag findings are false positives (teaching examples in
  cybersecurity/security-context skills — eval/exec in prose or code examples, SQL injection
  payload lists, AWS example keys)
- 1 domain_mismatch (agent-reach-channels: domain=social-commerce under automation/scrapers/)
  is a legitimate specialization, not an error




## [3.19.0] — 2026-07-26

### Changed
- 556 skills gained `version: 1.0.0` in frontmatter (standardized version field across
  the skill library). Inserted before closing `---` delimiter to avoid breaking multi-line
  YAML fields.
- SKILLS.json regenerated via `lint-skills.py --write` to sync catalog

### Verified
- Lint: 0 errors, 0 warnings, 3152 info
- Tests: 1344/1344 pass
- Schema: 1347/1347 pass (0 errors, 212 warnings)

## [3.18.0] — 2026-07-26

### Changed
- 1335 skills updated: standardized `## Anti-Rationalization` headers to
  `## Anti-Rationalization Table` (1132 renamed, 2 concatenated split, 201 added
  where missing). 12 files were already correct.
- SKILLS.json regenerated via `lint-skills.py --write` to sync catalog after content changes

### Verified
- Lint: 0 errors, 0 warnings, 3152 info
- Tests: 1344/1344 pass
- Schema: 1347/1347 pass (0 errors, 212 warnings)

## [3.17.0] — 2026-07-26

### Added
- SKILLS.json auto-regenerated via `lint-skills.py --write`: 1347 registered skills (up from 1261),
  matching on-disk count. All 86 previously unregistered SKILL.md files now included in the catalog.
- 331 trigger-phrase description fixes applied to SKILLS.json entries
- All category counts updated to reflect actual on-disk distribution

### Changed
- Lint: 0 errors, 0 warnings, 3152 info messages
- Schema: 1347/1347 pass (0 errors, 212 warnings)
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
