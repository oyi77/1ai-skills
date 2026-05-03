# TODO: claude-seo

## Completed in v1.2.0

- [x] **Fix YAML frontmatter parsing**:Removed HTML comments before `---` in 8 files (from @kylewhirl fork)
- [x] **SSRF prevention in Python scripts**:Private IP blocking in fetch_page.py and analyze_visual.py (from @artyomsv #7)
- [x] **Install hardening**:venv-based pip, no `--break-system-packages` (from @JawandS #2)
- [x] **Windows install fixes**:`python -m pip`, `py -3` fallback, requirements.txt persistence (from @kfrancis #5, PR #6)
- [x] **requirements.txt persistence**:Copied to skill dir after install (from @edustef #1)
- [x] **Path traversal prevention**:Output path sanitization in capture_screenshot.py, file validation in parse_html.py

## Completed: Extensions

- [x] **Extension system**:`extensions/` directory convention with self-contained add-ons
- [x] **DataForSEO extension**:22 commands across 9 API modules (SERP, keywords, backlinks, on-page, content, business listings, AI visibility, LLM mentions). Install: `./extensions/dataforseo/install.sh`

## Deferred from Community Feedback

- [ ] **Reduce Bash scope on agents** (Priority: Medium, from @artyomsv #7)
  Evaluate which agents truly need Bash access. Consider replacing with WebFetch where possible.

- [ ] **Docker-based script execution** (Priority: Low, from @artyomsv #7)
  Sandbox Python scripts in Docker for users who want extra isolation.

- [ ] **Opencode compatibility** (Priority: Low, from @Ehtz #4)
  Adapt skill architecture for Opencode. @kylewhirl already ported to OpenAI Codex.

- [ ] **Subagent timeout/compact handling** (Priority: Medium, from @JawandS #3)
  Primary agent sometimes terminates before subagents finish. Consider encouraging subagents
  to run /compact and adding explicit wait logic.

- [ ] **Native Chrome tools vs Playwright** (Priority: Medium, from @artyomsv #7, @btafoya PR #8)
  Claude Code has native browser automation. Evaluate replacing Playwright with built-in tools
  to eliminate the ~200MB Chromium dependency.

## Deferred from February 2026 Research Report

- [ ] **Fake freshness detection** (Priority: Medium)
  Compare visible dates (`datePublished`, `dateModified`) against actual content modification signals.
  Flag pages with updated dates but unchanged body content.

- [ ] **Mobile content parity check** (Priority: Medium)
  Compare mobile vs desktop meta tags, structured data presence, and content completeness.
  Flag discrepancies that could affect mobile-first indexing.

- [ ] **Discover optimization checks** (Priority: Low-Medium)
  Clickbait title detection, content depth scoring, local relevance signals, sensationalism flags.

- [ ] **Brand mention analysis Python implementation** (Priority: Low)
  Currently documented in `seo-geo/SKILL.md` but no programmatic scoring.

## SPA / Client-Side Rendering Support (Issue #11)

Phase 2 (merged in v1.4.0):
- [x] **`--googlebot` flag in fetch_page.py**:Compare response size with default UA vs Googlebot UA to detect prerender services

Remaining phases (deferred):

- [ ] **Phase 1: render_page.py** (Priority: High):Playwright-based page renderer that exports fully-rendered DOM HTML. CLI: `python render_page.py https://example.com --output rendered.html`. Drop-in complement to `fetch_page.py`.

- [ ] **Phase 3: Screenshot DOM export** (Priority: Medium):Add `--export-html` flag to `capture_screenshot.py` so rendered DOM is available to other agents without a second browser launch.

- [ ] **Phase 4: Orchestrator SPA detection** (Priority: High):Add 6 SPA detection signals to `seo/SKILL.md` (empty root div, minimal body, prerenderReady, framework markers, large JS bundles, React/Vue/Angular attributes). Route agents to raw vs rendered HTML based on detection result.

- [ ] **Phase 5: Agent updates** (Priority: High):Update seo-technical, seo-content, seo-schema, seo-performance, seo-visual to use rendered DOM when SPA detected. Add WRS (Web Rendering Service) dependency risk deductions.

- [ ] **Phase 6: SPA scoring methodology** (Priority: Medium):Separate scoring paths for SPAs with/without prerender. New "Rendering Architecture Assessment" report section.

- [ ] **Phase 7: Reference file updates** (Priority: Low):Add SPA section to quality-gates.md, eeat-framework.md, cwv-thresholds.md (Soft Navigations API guidance).

---

*Last updated: March 12, 2026*
