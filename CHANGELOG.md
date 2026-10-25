# Changelog
All notable changes to 1ai-skills are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]
### Changed
- Wave 1: consolidated 44 narrow sub-skills across 6 clusters into canonical parent playbooks with explicit `## Sub-Skills & Specialized Playbooks` routing tables:
  - HyperFrames (12 sub-skills) -> `content/hyperframes-general-video`
  - Kalodata (5 sub-skills) -> `integrations/kalodata/product-research`
  - Oh My OpenCode (5 sub-skills) -> `integrations/oh-my-opencode`
  - Gate.io Trading (6 sub-skills) -> `trading/gate-exchange-trading`
  - Gate.io Info & Research (12 sub-skills) -> `research/gate-info-research`
  - Trading Orchestrator (4 sub-skills) -> `trading/orchestrator`
- Wave 2: consolidated 19 sub-skills into canonical parent routing tables:
  - Core Video Production (6 sub-skills) -> `content/video-director`
  - UI Component Libraries (10 sub-skills) -> `content/ui-styling`
  - Design Systems & Tokens (3 sub-skills) -> `content/design-system`
- Wave 3: consolidated 25 business, marketing, sales, finance, and research sub-skills into canonical parent routing tables:
  - Web3 Contract & Primitives (3 sub-skills) -> `trading/defi-protocols`
  - SEO Optimization (3 sub-skills) -> `marketing/seo-optimizer`
  - Social Media Automation (4 sub-skills) -> `marketing/social-media-engagement`
  - Email Marketing (2 sub-skills) -> `marketing/email-marketing`
  - Sales Pipeline & B2B (4 sub-skills) -> `sales/sales-pipeline`
  - Financial Investment (4 sub-skills) -> `financial/investment-industry`
  - Corporate Accounting (3 sub-skills) -> `financial/month-end-closer`
  - Institutional Research (2 sub-skills) -> `research/mckinsey-research`
- Wave 4: consolidated 18 CI/CD, Git workflow, and testing sub-skills into canonical parent routing tables:
  - CI/CD (7 sub-skills) -> `devops/ci-cd-pipeline`
  - GitOps (1 sub-skill) -> `devops/argocd-gitops`
  - Git Workflow (4 sub-skills) -> `development/git-workflow-mastery`
  - Test-Driven Development (3 sub-skills) -> `development/test-driven-development`
  - Browser E2E Testing (3 sub-skills) -> `development/playwright-e2e`
- Wave 5: consolidated 26 agent, automation, data orchestration, and self-evolution sub-skills into four canonical parent routing tables.
- Wave 6: consolidated 18 knowledge, memory, meeting, productivity, and project-management sub-skills into seven canonical parent routing tables: `core/rag-builder`, `mcp/memory-knowledge-graph`, `core/core`, `core/find-skills`, `productivity/meeting-management`, `productivity/focus-time-management`, and `operations/team`.
- Wave 7: consolidated 24 mindset framework sub-skills into eight canonical parent routing tables: `mindset/ponytail`, `mindset/decision-frameworks`, `mindset/critical-thinking`, `mindset/leadership-essentials`, `mindset/difficult-conversations`, `mindset/storytelling-frameworks`, `mindset/unit-economics`, and `mindset/business-model-canvas`.
- Wave 8: consolidated 9 sub-skills into three canonical parent routing tables: `agents/coding` (5 fixed coding-role skills), `automation/scrapers` (2 Agent Reach skills), and `mcp/clients` (2 generic MCP client skills).
- Deferred framework/autonomous candidates and broad integration/API candidates due canonical-parent scope mismatch; their registry entries remain active.
- Wave 9: consolidated 7 adapter/intelligence/framework sub-skills into accepted parents: `integrations/stripe-integration` (`stripe-mcp`), `productivity/notion` (`notion-mcp`), `integrations/linear-api` (`linear-mcp`), `integrations/github` (`github-mcp`), `integrations/slack` (`slack-mcp`), `automation/scrapers` (`social-intelligence`), and `integrations/langchain-skills` (`langchain-patterns`).
- Four no-code workflow links were already unregistered and required no registry count change.
- Zero File Deletion Invariant preserved across Waves 1–9: all on-disk physical `SKILL.md` files retained to guarantee link resolution.
- Updated active registry in `SKILLS.json` from 1398 to **1208** skills across 19 categories.
- Synchronized counts across `README.md`, `AGENTS.md`, `package.json`, `llms.txt`, and `scripts/generate-site.py` (dynamic catalog counts and canonical captured test receipt).
- Refreshed `README.md` and `AGENTS.md` counts from the active registry, including per-category numbers.
### Fixed
- Repaired 19 SKILL.md files with unbalanced (odd-count) code fences that swallowed
  structural headings. Inserted missing opening fences for 7 meta-skill boilerplate blocks
  and 12 content blocks (lost closers before `## When NOT to Use` / `---` /
  `### When to Use Which`). All 1372 files now have even fence parity.
- Quoted YAML descriptions containing unquoted colons in `content/design/SKILL.md`
  and `content/ui-ux-pro-max/SKILL.md` (was a parse error, skill unregistered).
- Added `content-creation` and removed dead `finance` from the schema `category` enum;
  allowed a leading digit in the `kebab` name pattern for brand names such as `21st-dev`.
  Schema validation is now 0 errors.

### Added

- `cybersecurity/cloudflare-security-audit`: Multi-phase defensive vulnerability audit methodology ported from [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill). Enforces strict trust-boundary violation proof, independent adversarial candidate verification, structured findings ledger (`findings.json`), and minimal effective source diffs.
- `research/scientific-agent-skills`: Master scientific research orchestration playbook ported from [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills). Integrates 100+ scientific databases (PubChem, ChEMBL, UniProt), 70+ scientific Python libraries (RDKit, BioPython, Scanpy), molecular docking, clinical trial evidence, and automated laboratory protocol generation.
- `development/dead-code-graveyard`: Systematic audit, quarantine, and safe pruning of unreachable branches, dead code, unmounted endpoints, and orphaned assets across large codebases.
- `development/ast-architectural-guard`: Layer boundary, import hierarchy, and circular dependency enforcement via AST inspection and dependency graph linting.
- `development/concurrency-race-audit`: Concurrent async code audit for thread safety, shared state mutation, event loop blocking, and connection pool leaks.
- `development/type-narrowing-audit`: Replacement of unsafe types (`any`, blind assertions, untyped catch blocks) with defensive type narrowing and runtime validation.
- `development/api-contract-drift-audit`: Client-server schema parity and OpenAPI specification verification to detect wire breaking changes before deployment.
- `development/zero-downtime-migration-audit`: Expand/Contract pattern enforcement for non-blocking database migrations, concurrent index builds, and backward-compatible DDL.
- `development/godfile-ratchet-split`: Monolithic god-file dismantling into decoupled domain submodules behind backward-compatible barrel facades with ratchet line caps.
- `development/tdd-bug-reproduction`: Red-Green-Refactor regression protocol isolating minimal bug reproductions into failing tests before touching production code.
- `content/hallmark`: Anti-AI-slop design skill ported from [Nutlope/hallmark](https://github.com/Nutlope/hallmark).
  Enforces non-negotiable floor rules against default AI generative aesthetics (declarative root tokens,
  no transition all, no saturated violet defaults, max one display font per screen, zero stock photo cliches),
  11 distinctive design genres, 10-point anti-rationalization table, sloplint linting scripts, Wikimedia
  licensed photo library, and multi-viewport verification checklists.
- `cybersecurity/reverse-engineering-router`: parent hub for reverse engineering work. Classifies
  the target artifact (extension, magic bytes, keywords) and routes deterministically to the
  correct specialist skill via a 31-row `ROUTING_TABLE`; every row carries an explicit fallback
  and the catch-all is `reverse-engineer-anything-with-rea`. Maps all **46** RE-cluster skills
  reachable via routing or skill-map; the router itself is the 47th and does not self-list.
  Declares `depends_on: [cybersecurity-router]` so the security router delegates rather
  than duplicates. Three RE-adjacent response/defense skills are listed under **Deliberately
  Out of Scope** instead of being silently omitted.
- `cybersecurity/reverse-engineer-anything-with-rea`: artifact- and runtime-evidence workflow for
  questions that cannot be answered from available source (shipped binaries, Go/Rust, Android,
  Electron/JavaScript, firmware, browser targets). Preserves artifact SHA-256, scope, tool
  versions, and separates observation from inference.

### Changed
- `cybersecurity/cybersecurity-router`: split the Reverse Engineering skills out of `Binary Exploitation (Pwn)`
  into their own skill-map section, and added a routing-table row delegating RE artifacts to
  `reverse-engineering-router` instead of resolving directly to `binary-breaker`.
- `SKILLS.json`: registered both skills — **1370** total, **797** cybersecurity, `category_count`
  unchanged at 19.

### Verified
- Lint: 0 errors, 0 warnings
- Tests: 1372/1372 pass
- Broken links: 0 of 1596 files
- Dependency graph: router edge valid, no cycles
- Synced to `~/.agents/skills/` (router 351L, REA 137L)

### Changed
- `cybersecurity/cybersecurity-router`: added a Reverse Engineering section to the skill map and a
  routing-table row for RE artifacts; they now delegate to `reverse-engineering-router` instead of
  resolving directly to `binary-breaker`.
- `SKILLS.json`: registered both skills — **1370** total, **797** cybersecurity, `category_count`
  unchanged at 19.
- `Plan C`: renamed 24 skill directories to match `SKILLS.json` registry paths (`content/document-creator` consolidation, `core/kb-memory` merge, `financial/investment-*`, `marketing/tiktok-marketing`)
- `Plan C`: registered `content/emil-design-skills` (1306 skills), fixed 6 pre-existing test failures (missing `## When to Use` / `## Workflow` sections, false-positive `existing-skill` link in `core/book-to-skill`)
- `Plan C`: normalized `author: oyi77` metadata across skill files; landed content improvements (descriptions, code examples, monetization sections)
- Removed stale audit artifacts under `reports/` (regenerated by scripts) and one-off fixer `scripts/fix-remaining-5.py`

### Resolved (GATE debt sweep)
- Lint warnings: all `name-mismatch` and `no-trigger-phrase` warnings resolved; all `desc-too-long`
  warnings fixed (4 frontmatter descriptions truncated to single-line scalars ≤500 chars).
  Lint now reports **0 errors, 0 warnings**.
- Description triggers: gerundized `Use when` phrase in 93 SKILL.md files (`creating, validating, and
  sharing`-style coordinate verbs); residual bare-verb check = 0; `SKILLS.json` index refreshed via
  `lint-skills.py --write` so trigger matching stays in sync.
- Schema validation: added optional `subdomain` field to `schemas/skill.schema.json`;
  expanded `ALLOWED_EXTRA` with 12 recurring enrichment fields (`nist_csf`, `mitre_attack`, `keywords`,
  `money`, `homepage`, …) — resolves the `[extra-field]` info debt (2444 → 163);
  relaxed `name-mismatch` to accept nested grouping dirs (`content/video/gen` → `video-gen`).
- Validator config: `scripts/validate-skill-schema.py` now imports `SKILL_DIRS` from `config`
  (single source of truth) — removes phantom `finance` directory divergence from lint/test scripts.
- `.gitignore`: added `reports/` (regenerated audit output).

### Verified
- Lint: 0 errors, 0 warnings, 163 info
- Tests: 1306/1306 pass
- Validator: 1306/1306 clean (`--strict` clean), broken links: 0, gitleaks: 0 leaks

## [3.31.0] — 2026-07-26
### Added
- `core/core/kb/SKILL.md` — Deepened from 21-line stub to 509-line production skill (v2.0.0,
  depth 2, quality 3). 15 code blocks, Anti-Rationalization Table, verification checklist,
  session-start routine, PARA-structured persistence patterns.
- `core/core/company-kb/SKILL.md` — Deepened from 114-line stub to 371-line production skill
  (v2.0.0, depth 2, quality 3). Entity schema, multi-agent locking, session log sanitization,
  privacy classification, team collaboration scenarios.

### Changed
- `SKILLS.json` — Updated `kb` and `company-kb` entries with version 2.0.0, depth 2, quality 3,
  improved descriptions with `Use when` trigger phrase.

### Verified
- Lint: 0 errors, 0 warnings, 2326 info
- Tests: 1306/1306 pass
- SKILLS.json: valid JSON, 1309 skills

## [3.23.0] — 2026-07-26
### Added
- `schemas/skill.schema.json` — Optional `depends_on` frontmatter field (array of kebab-case skill
  names) for skill-activation dependency ordering. Separate from existing `dependencies` field
  (which tracks package/tool deps).
- `scripts/skill-graph.py` — Composable Skill Dependency Graph Generator. Reads `depends_on` from
  all SKILL.md frontmatter files, builds directed dependency graph, detects cycles via DFS
  coloring, and computes topological order via Kahn's algorithm.
  Supports `--json`, `--topo`, `--validate`, `--output` modes. Outputs `reports/skill-graph.json`.
- `reports/skill-graph.json` — First dependency graph snapshot (1309 skills, 0 edges — field is
  new, no skills use it yet). Acts as a baseline for future dependency additions.

### Changed
- `scripts/skill-graph.py` replaces hand-written `parse_frontmatter()` with `yaml.safe_load()`
  (PyYAML already a project dependency) to correctly handle nested YAML keys.

### Verified
- Lint: 0 errors, 0 warnings, 2327 info
- Tests: 1306/1306 pass
- Schema: 1309/1309 (0 errors, 211 warnings)
- skill-graph.py: 1309 skills scanned, 0 with depends_on, 0 cycles, report written
- Fix: PyYAML-based parser eliminates 22 phantom nodes from nested frontmatter keys


## [3.25.0] — 2026-07-26
### Added
- `scripts/validate-skill-schema.py`: `--strict` flag — promotes all warnings to errors
  (exit 1 if any warnings present). Opt-in, default behavior unchanged.
- `scripts/check-broken-links.py` — Broken internal skill reference checker. Scans all
  markdown files for `skill://`, `/skills/`, and `../skills/` references and resolves them
  against SKILLS.json skill names. Supports `--json`, `--verbose`, `--exit-zero` flags.
### Changed
- `scripts/validate-skill-schema.py`: Extracted `def main():` with full argparse (was previously
  inline at module level). Exit logic now correctly evaluates `--strict` flag.
### Verified
- Validator default mode: 1309/1309 pass, 0 errors, 211 warnings, exit 0
- Validator `--strict` mode: 1309/1309 pass, 0 errors, 211 warnings, exit 1 (warnings→errors)
- Broken-link checker: 1439 files scanned, 0 broken internal references across all markdown
  (SKILL.md + docs + other .md/.mdx files)
- Lint: 0 errors, 0 warnings, 2327 info
- Tests: 1306/1306 pass

## [3.26.0] — 2026-07-26
### Added
- `SECURITY.md` — security policy with gitleaks integration and supply-chain notes
- `threat_model.md` — lightweight threat model covering CI/CD, skill content, and supply chain
- `.gitleaksignore` — false positive suppressions (2 entries: doc token example, Solidity constant)
- `.github/dependabot.yml` — Dependabot config for GitHub Actions and npm dependency updates
### Changed
- `.github/workflows/validate.yml`: gitleaks `--config` flag removed (uses default config + `.gitleaksignore`);
  `pyyaml` pinned to `6.0.2`
- `.github/workflows/auto-release.yml`: gitleaks `--config` flag removed
### Verified
- gitleaks `--no-git` scan: 0 leaks found (exit 0), 9.17 MB scanned in 2.4s
- Lint: 0 errors, 0 warnings, 2327 info
- Tests: 1306/1306 pass

## [3.30.0] — 2026-07-26
### Added
- `docs/LEARNING_LIFECYCLE.md` — Learning lifecycle document with memory pollution avoidance
### Verified
- Lint: 0 errors, 0 warnings, 2327 info
- Tests: 1306/1306 pass

## [3.29.0] — 2026-07-26
### Added
- `docs/META_SKILL_GOVERNANCE.md` — Meta-skill governance document with 13-skill inventory,
  5 governance rules, risk model, and lifecycle
### Verified
- Lint: 0 errors, 0 warnings, 2327 info
- Tests: 1306/1306 pass

## [3.27.0] — 2026-07-26
### Added
- `docs/INSTRUCTION_PRECEDENCE.md` — Instruction precedence and prompt-injection defense
  documentation for skill authors
### Verified
- Lint: 0 errors, 0 warnings, 2327 info
- Tests: 1306/1306 pass

## [3.24.0] — 2026-07-26
### Added
- `evals/` — Lightweight evaluation framework for skill quality verification:
  - `evals/README.md` — Runner documentation with usage examples, check-type reference, and
    case creation guide
  - `evals/cases/` — 10 eval case JSON files across 8 categories (agents, content, core,
    cybersecurity, development ×2, devops, integrations, marketing, research)
  - `evals/reports/` — Output directory for runner-generated reports
- `scripts/run-evals.py` — Evaluation runner with 12 check types (contains, section_exists,
  anti_rat_table, code_block_count, has_workflow_section, frontmatter_field_exists,
  frontmatter_field, trigger_phrase, skill_depth, domain_match, not_contains,
  has_code_example). Supports `--skill`, `--category`, `--all`, `--json`, `--verbose`,
  `--list` modes. Human-readable and JSON reporting, exit code zero on all-pass.
- `scripts/run-evals.py`: `--all` flag — run all discovered eval cases at once
- `scripts/run-evals.py`: Mutual exclusion validation — rejects combinations of
  `--all`/`--skill`/`--category`
### Verified
- Lint: 0 errors, 0 warnings, 2327 info
- Tests: 1306/1306 pass
- Evals: 91/91 checks passed, 0 failed, 0 skipped across 10 case files
- All 6 runner CLI modes verified: `--list`, `--all`, `--all --verbose`,
  `--skill autonomous`, `--category development`, `--json`

## [3.22.0] — 2026-07-26
### Added
- `scripts/skill_router.py` — Skill Routing & Discovery Engine. Takes natural-language queries
  and returns ranked skills from SKILLS.json using exact name match, name-part overlap, category
  filter, tag overlap, domain match, and description ("Use when") trigger scoring.
  Supports `--category`, `--top`, `--json`, `--suggest`, `--categories` modes.

### Verified
- Lint: 0 errors, 0 warnings, 2327 info
- Tests: 1306/1306 pass
- Schema: 1309/1309 pass (0 errors, 211 warnings)
- Router tested with 5 diverse queries across domains (test-driven-development, docker, crypto,
  social media, kubernetes security); all return relevant skills with plausible scores.
  Category filtering, suggest mode, and category ranking verified.
## [3.21.0] — 2026-07-26
### Removed
- 37 G1 stub sub-skill files deleted from disk and SKILLS.json (entries that redirect to parent
  skills): ad-copy, analytics-reporting, collecting-open-source-intelligence, cron-designer,
  detecting-business-email-compromise-with-ai, discord-bot, discord-webhooks, docker-compose,
  dockerfile-opt, email-writer, github-actions, github-issues, github-pr, ifttt-maker,
  k8s-deploy, lead-generation-engine, long-form, make-scenarios, n8n-builder, notion-api,
  notion-db, notion-pages, pipedream-workflows, product-desc, scrapers, slack-bot,
  slack-notifier, slash-commands, smart-scraper, social-listener, social-media-engagement,
  webhook-router, whatsapp-bot, workflows, zapier-alt, email-sequences, price-tracker
- `dockerfile-opt` → `dockerfile-optimize` — duplicate merged (69% name, 68% desc similarity;
  substance from `dockerfile-opt` absorbed into `dockerfile-optimize`)
- `scripts/bulk-add-version.py`, `scripts/bulk-fix-ar-table.py`, `scripts/find-duplicates.py` —

### Changed
- `devops/dockerfile-optimize/SKILL.md` — merged with `dockerfile-opt`: added layer ordering
  table, .dockerignore section, base image selection guide, security hardening rules, expanded
  anti-rationalization table (7 rows)
### Verified

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
