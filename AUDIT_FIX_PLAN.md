# 1ai-skills Comprehensive Audit Fix Plan

> Generated: 2026-06-27
> Audit scope: 1320 skills across 19 categories
> Status: PLANNED

---

## Executive Summary

Audit found **696/1320 (53%) skills with template placeholder content** — the dominant quality gap. Additional issues: 1 orphaned skill, 2 duplicate descriptions, 6 missing `## Overview`, 7 broken internal links, 1 short description.

**Severity breakdown:**
| Severity | Issue | Count |
|---|---|---|
| 🔴 CRITICAL | Template placeholder content (no real instructions) | 696 |
| 🔴 HIGH | Orphaned skill (not in SKILLS.json) | 1 |
| 🟡 MEDIUM | Duplicate descriptions | 4 skills |
| 🟡 MEDIUM | Missing `## Overview` section | 6 |
| 🟡 MEDIUM | Broken internal links | 7 targets |
| 🟢 LOW | Short description (<30 chars) | 1 |

---

## Phase 1: Quick Fixes (batch, scriptable)

**Goal:** Fix structural issues that don't require content authoring.

### 1.1 Add orphaned skill to SKILLS.json
- **Target:** `sales/sales-pipeline` — exists on disk, missing from catalog
- **Action:** Run `bash scripts/audit-skills.sh --write` to regenerate SKILLS.json
- **Acceptance:** `sales-pipeline` appears in SKILLS.json with correct category `sales`
- **Verify:** `grep sales-pipeline SKILLS.json`

### 1.2 Fix duplicate descriptions
- **Targets:**
  - `meta/data` + `meta/meta-skill-datastore` — identical desc about "Centralized database for meta-skill operations"
  - `trading/polymarket` + `trading/polymarket-api` — identical desc about "Query Polymarket prediction markets"
- **Action:** Differentiate descriptions. `meta/data` → focus on raw data storage; `meta/meta-skill-datastore` → focus on skill performance metrics. `trading/polymarket` → general market queries; `trading/polymarket-api` → programmatic API access.
- **Acceptance:** No two skills share identical description text
- **Verify:** Re-run duplicate description check

### 1.3 Fix 7 broken internal links
- **Targets:**
  - `/skills/1ai-skills` (24 refs) → likely self-references, fix to correct path
  - `/skills/hive` (2 refs) → link to `core/hive-mind` or remove
  - `/skills/blob` (2 refs) → remove or fix
  - `/skills/idoshamun` (2 refs) → remove (external reference, not a skill)
  - `/skills/react-performance-tips` (1 ref) → remove or link to correct skill
  - `/skills/react-optimizer` (1 ref) → remove or link to correct skill
  - `/skills/notion-tasks-1` (1 ref) → link to `productivity/notion` or remove
- **Acceptance:** Zero broken `/skills/<name>` links
- **Verify:** Re-run broken link check

### 1.4 Fix short description
- **Target:** `cybersecurity/performing-nist-csf-maturity-assessment` — desc <30 chars
- **Action:** Write proper description matching the skill's actual purpose
- **Acceptance:** Description ≥50 chars
- **Verify:** `grep -A2 "description:" cybersecurity/performing-nist-csf-maturity-assessment/SKILL.md`

### 1.5 Fix 6 skills missing `## Overview`
- **Targets:**
  - `development/engineering-hard-rules`
  - `development/agentic-quality-engineering`
  - `development/automated-test-generator`
  - `development/qa-review-fix-loop`
  - `research/best-hacker`
  - `sales/sales-pipeline`
- **Action:** Add a concise `## Overview` section (2-3 sentences) to each
- **Acceptance:** All 6 have `## Overview` in body
- **Verify:** Re-run missing overview check

---

## Phase 2: Content Quality — Placeholder Skills (696 skills)

**Goal:** Replace template placeholder content with real, actionable skill instructions.

### Strategy

The 696 placeholder skills fall into two buckets:

**A. Auto-generated cybersecurity skills (460 skills, 59% of cybersecurity)**
These were bulk-generated and have identical boilerplate. Fix approach:
- Batch-rewrite using a Python script that generates real content from the skill name + domain
- Each skill gets: real `## Overview`, real `## When to Use`, real `## Process` with actual steps
- Preserve YAML frontmatter (already valid)

**B. Non-cybersecurity placeholder skills (236 skills across 18 categories)**
Fix approach:
- Group by category
- Prioritize high-traffic categories: mindset (55), agents (12), mcp (12), automation (21)
- Write real content per skill (cannot be auto-generated — each is unique)

### 2.1 Cybersecurity batch fix (460 skills)

**Script:** `scripts/fix-cybersecurity-placeholders.py`

For each placeholder skill:
1. Read SKILL.md, extract YAML frontmatter
2. Parse skill name → derive topic (e.g., `detecting-golden-ticket-forgery` → "Golden Ticket forgery detection")
3. Generate real content:
   - `## Overview` — 2-3 sentences on what this skill does
   - `## When to Use` — 3-5 trigger conditions
   - `## When NOT to Use` — 2-3 contraindications
   - `## Process` — Step-by-step workflow (5-8 steps)
   - `## Tools` — Relevant tools/techniques
   - `## Verification` — How to confirm success
4. Write back SKILL.md preserving frontmatter

**Acceptance:** Zero placeholder content in cybersecurity skills
**Verify:** `grep -rl "Section content — see SKILL.md body" cybersecurity/ | wc -l` → 0

### 2.2 Mindset skills (55 skills — 100% placeholder)

**Script:** `scripts/fix-mindset-placeholders.py`

Same approach as cybersecurity but for mindset domain:
- Each skill maps to a soft-skill topic (e.g., `habit-formation`, `mindfulness`, `first-principles-thinking`)
- Content includes: philosophy, daily practice, frameworks, common pitfalls

**Acceptance:** Zero placeholder content in mindset skills
**Verify:** `grep -rl "Section content — see SKILL.md body" mindset/ | wc -l` → 0

### 2.3 Remaining categories (181 skills)

Priority order by placeholder count:
1. automation (21) — workflow/bot/scraper skills
2. content (21) — video/writing/design skills
3. marketing (21) — SEO/ads/growth skills
4. research (15) — analysis/research skills
5. core (14) — agent infrastructure skills
6. agents (12) — orchestration/coding agents
7. mcp (12) — MCP server skills
8. operations (12) — business ops skills
9. integrations (11) — platform integrations
10. trading (9) — crypto/trading skills
11. meta (8) — meta-skills
12. sales (6) — sales skills
13. data (4) — data skills
14. productivity (4) — productivity skills
15. devops (3) — Docker/K8s skills
16. financial (2) — finance skills
17. development (6) — dev skills

**Approach:** One script per category batch, similar to cybersecurity.

**Acceptance:** Zero placeholder content across all categories
**Verify:** `grep -rl "Section content — see SKILL.md body" */ | wc -l` → 0

---

## Phase 3: Verification

### 3.1 Re-run full audit
```bash
bash scripts/audit-skills.sh --write
python3 scripts/validate-skills.py
```

### 3.2 Re-run comprehensive audit script
Re-run the Python audit from this session to confirm:
- Zero orphaned skills
- Zero duplicate descriptions
- Zero broken links
- Zero missing overviews
- Zero placeholder content
- Zero short descriptions

### 3.3 Spot-check 20 random skills
- Pick 5 from cybersecurity, 5 from mindset, 10 from mixed categories
- Read SKILL.md, verify real content (not template)
- Verify YAML frontmatter intact
- Verify internal links resolve

### 3.4 Git commit
```bash
git add -A
git commit -m "fix: comprehensive audit — replace placeholder content, fix structural issues

- Add sales-pipeline to SKILLS.json
- Fix 2 duplicate descriptions (meta/data, trading/polymarket)
- Fix 7 broken internal links
- Fix 1 short description
- Add missing ## Overview to 6 skills
- Replace placeholder content in 696 skills across all 19 categories

Audit receipts: [paste verification output]"
```

---

## Execution Order

```
Phase 1 (quick fixes) → ~15 min
  1.1 Regenerate SKILLS.json
  1.2 Fix duplicate descriptions
  1.3 Fix broken links
  1.4 Fix short description
  1.5 Add missing overviews
  → VERIFY: re-run audit

Phase 2.1 (cybersecurity batch) → bulk script
  → VERIFY: grep placeholder count

Phase 2.2 (mindset batch) → bulk script
  → VERIFY: grep placeholder count

Phase 2.3 (remaining 181) → per-category scripts
  → VERIFY: grep placeholder count

Phase 3 (final verification)
  → Full audit re-run
  → Spot-check 20 skills
  → Git commit
```

---

## Rollback

Each phase is independently revertible via `git revert`. Phase 2 scripts log every file they modify to `scripts/fix-audit-log.txt` for traceability.

---

## Risk Assessment

| Risk | Mitigation |
|---|---|
| Batch scripts generate wrong content | Spot-check 20 skills before bulk commit |
| Scripts break YAML frontmatter | Validate with `python3 scripts/validate-skills.py` after each phase |
| Content too generic | Each script uses skill name + domain to derive specific content |
| Merge conflicts with other work | Work on feature branch `fix/audit-placeholder-content` |
