# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.5.0] - 2026-03-19

### Added
- **Frontmatter fields**: `user-invokable`, `argument-hint`, and `allowed-tools` added to all SKILL.md files per Anthropic best practices
- **Error handling sections**: Added to all SKILL.md files with skill-specific guidance
- **Plugin manifest**: `.claude-plugin/plugin.json` updated with all skills and agents registered
- **Version tracking**: `pyproject.toml` with project metadata

### Fixed
- **Em dash elimination**: Replaced em dashes (U+2014) across files with appropriate punctuation (colons, commas, semicolons, periods) to reduce AI detection signals
- **HTML comments before frontmatter**: Removed `<!-- Updated: ... -->` comments from SKILL.md files that preceded the YAML frontmatter delimiter
- **Anthropic compliance audit**: Full audit against official skill-building guidelines, all checks now pass

### Changed
- **Technical SEO**: Updated from "8 categories" to "9 categories" in description (IndexNow added in prior update)

---

## [1.4.0] - 2026-03-12

### Security
- **Install script supply chain fix**: Replaced `irm | iex` Windows PowerShell one-liner with `git clone + powershell -File` as primary install method. Claude Code's own security guardrails flagged the old pattern as a supply chain risk (reported by community member). Added collapsible "review before running" section for Unix curl method.
- **Version pinning**: `install.sh` and `install.ps1` now clone a specific release tag (`v1.3.0`) by default rather than `main`, preventing silent updates. Override with `CLAUDE_SEO_TAG=main`.
- **PowerShell Invoke-External hardening**: Comprehensive `PSNativeCommandUseErrorActionPreference` handling in `Invoke-External` wrapper (fixes Windows git clone stderr false-positive termination, from PR #13 + PR #15).

### Added
- **GEO agent deployed**: `agents/seo-geo.md` created -- `/seo audit` now spawns 7 parallel agents (was 6). GEO analysis covers AI crawler access, llms.txt, passage-level citability, brand mention signals, platform-specific scoring (Google AI Overviews, ChatGPT, Perplexity, Bing Copilot).
- **`--googlebot` flag in `fetch_page.py`**: Detect prerender/dynamic rendering services by comparing response size with default UA vs Googlebot UA. First phase of SPA/CSR support (Issue #11).

### Fixed
- **URL normalization**: `capture_screenshot.py` and `analyze_visual.py` now accept bare domains (`example.com` -> `https://example.com`) via shared `normalize_url()` helper (from PR #16 by @shuofengzhang).
- **GEO weight**: AI Search Readiness weight increased from 5% to 10% in overall SEO Health Score. Technical SEO adjusted to 22%, Content Quality to 23%.
- **FAQPage guidance**: Blanket "remove FAQPage on commercial sites" updated to nuanced guidance -- existing FAQPage -> Info priority (not Critical), noting AI/LLM citation benefit. Adding new FAQPage -> not recommended for Google, note AI benefit. Updated in `seo/SKILL.md`, `agents/seo-schema.md`, `seo/references/schema-types.md`.
- **Uninstall agents list**: Added `seo-geo` to `uninstall.sh` and `uninstall.ps1` removal lists.
- **Python requirement**: Corrected from `3.8+` to `3.10+` in `README.md` and `docs/INSTALLATION.md`.

### Changed
- Subagent count: 6 -> 7 (added seo-geo to core audit pipeline)
- `.gitignore`: Added generated audit artifacts (charts/, PDFs, report.html, firebase-debug.log, generated-schema.json)

---

## [1.3.0] - 2026-03-06

### Added
- **Extension system**: `extensions/` directory convention for self-contained add-ons with install/uninstall scripts
- **DataForSEO extension**: 22 commands across 9 API modules (SERP, keywords, backlinks, on-page, content, business listings, AI visibility, LLM mentions). Install: `./extensions/dataforseo/install.sh`
- **DataForSEO integration**: seo-audit, seo-content, seo-geo, seo-page, seo-plan, seo-technical auto-detect DataForSEO MCP tools for enriched analysis
- **Plugin manifest**: `.claude-plugin/plugin.json` for official plugin directory submission
- **Documentation**: Extensions architecture in ARCHITECTURE.md, 22 new commands in COMMANDS.md, updated MCP integration guide

### Fixed
- **Title tag threshold**: Pre-commit hook now uses 60-char max, aligned with quality-gates.md and echo message
- **SSRF prevention**: Added to `capture_screenshot.py` (defense-in-depth, matching `fetch_page.py`)
- **Frontmatter cleanup**: Removed non-standard `allowed-tools` from main SKILL.md

### Changed
- Sub-skill count: 12 + 1 extension (added seo-dataforseo via DataForSEO extension)
- Subagent count: 6 + 1 optional (added seo-dataforseo agent via extension)
- DataForSEO promoted from "Community" to "Official extension" in MCP docs

---

## [1.2.1] - 2026-02-28

### Fixed
- **User-Agent header**: Changed default from bot-style `ClaudeSEO/1.0` to Chrome-like string with `ClaudeSEO/1.2` suffix. SSR frameworks (Next.js, Nuxt, Angular) now pre-render properly instead of serving empty client-side shells (#9)
- **Custom User-Agent support**: Added `--user-agent` flag to `fetch_page.py` for configurable UA strings

### Added
- **install.cat support**: Added alternative install method via `curl install.cat/AgriciDaniel/claude-seo | bash` to README (#10)

---

## [1.2.0] - 2026-02-19

### Security
- **SSRF prevention**: Added private IP blocking to `fetch_page.py` and `analyze_visual.py`
- **Path traversal prevention**: Added output path sanitization to `capture_screenshot.py` and file validation to `parse_html.py`
- **Install hardening**: Removed `--break-system-packages`, switched to venv-based pip install
- **requirements.txt**: Now persisted to `~/.claude/skills/seo/` for user retry

### Fixed
- **YAML frontmatter parsing**: Removed HTML comments before `---` delimiter in 8 files (skills: seo-content, seo-images, seo-programmatic, seo-schema, seo-technical; agents: seo-content, seo-performance, seo-technical). Thanks @kylewhirl for identifying this in the codex-seo fork.
- **Windows installer**: Merged @kfrancis improvements -- `python -m pip`, `py -3` launcher fallback, requirements.txt persistence, non-fatal subagent copy, better error diagnostics (PR #6)
- **requirements.txt missing after install**: Now copied to skill directory so users can retry (#1)

### Changed
- Python dependencies now installed in a venv at `~/.claude/skills/seo/.venv/` with `--user` fallback (#2)
- Playwright marked as explicitly optional in install output
- Windows installer uses `Resolve-Python` helper for robust Python detection (#5)

---

## [1.1.0] - 2026-02-07

### Security (CRITICAL)
- **urllib3 >=2.6.3**: Fixes CVE-2026-21441 (CVSS 8.9) - decompression bypass vulnerability
- **lxml >=6.0.2**: Updated from 5.3.2 for additional libxml2 security patches
- **Pillow >=12.1.0**: Fixes CVE-2025-48379
- **playwright >=1.55.1**: Fixes CVE-2025-59288 (macOS)
- **requests >=2.32.4**: Fixes CVE-2024-47081, CVE-2024-35195

### Added
- **GEO (Generative Engine Optimization) major enhancement**:
  - Brand mention analysis (3x more important than backlinks for AI visibility)
  - AI crawler detection (GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, etc.)
  - llms.txt standard detection and recommendations
  - RSL 1.0 (Really Simple Licensing) detection
  - Passage-level citability scoring (optimal 134-167 words)
  - Platform-specific optimization (Google AI Overviews vs ChatGPT vs Perplexity)
  - Server-side rendering checks for AI crawler accessibility
- **LCP Subparts analysis**: TTFB, resource load delay, resource load time, render delay
- **Soft Navigations API detection** for SPA CWV measurement limitations
- **Schema.org v29.4 additions**: ConferenceEvent, PerformingArtsEvent, LoyaltyProgram
- **E-commerce schema updates**: returnPolicyCountry now required, organization-level policies

### Changed
- **E-E-A-T framework**: Updated for December 2025 core update - now applies to ALL competitive queries, not just YMYL
- **SKILL.md description**: Expanded to leverage new 1024-character limit
- **Schema deprecations expanded**: Added ClaimReview, VehicleListing (June 2025)
- **WebApplication schema**: Added as correct type for browser-based SaaS (vs SoftwareApplication)

### Fixed
- Schema-types.md now correctly distinguishes SoftwareApplication (apps) vs WebApplication (SaaS)

---

## [1.0.0] - 2026-02-07

### Added
- Initial release of Claude SEO
- 9 specialized skills: audit, page, sitemap, schema, images, technical, content, geo, plan
- 6 subagents for parallel analysis: seo-technical, seo-content, seo-schema, seo-sitemap, seo-performance, seo-visual
- Industry templates: SaaS, local service, e-commerce, publisher, agency, generic
- Schema library with deprecation tracking:
  - HowTo schema marked deprecated (September 2023)
  - FAQ schema restricted to government/healthcare sites only (August 2023)
  - SpecialAnnouncement schema marked deprecated (July 31, 2025)
- AI Overviews / GEO optimization skill (seo-geo) - new for 2026
- Core Web Vitals analysis using current metrics:
  - LCP (Largest Contentful Paint): <2.5s
  - INP (Interaction to Next Paint): <200ms - replaced FID on March 12, 2024
  - CLS (Cumulative Layout Shift): <0.1
- E-E-A-T framework updated to September 2025 Quality Rater Guidelines
- Quality gates for thin content and doorway page prevention:
  - Warning at 30+ location pages
  - Hard stop at 50+ location pages
- Pre-commit and post-edit automation hooks
- One-command install and uninstall scripts (Unix and Windows)
- Bounded Python dependency pinning with CVE-aware minimums (lxml >= 5.3.2)

### Architecture
- Follows Anthropic's official Claude Code skill specification (February 2026)
- Standard directory layout: `scripts/`, `references/`, `assets/`
- Valid hook matchers (tool name only, no argument patterns)
- Correct subagent frontmatter fields (name, description, tools)
- CLI command is `claude` (not `claude-code`)
