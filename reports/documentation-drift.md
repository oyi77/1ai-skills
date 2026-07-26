# Documentation Drift Report

**Generated**: 2026-07-26
**Version**: 3.14.0

---

## 1. Version Tracking

| Document | Version Mentioned | Match? |
|----------|:-:|:-:|
| `package.json` | 3.14.0 | ✅ Current |
| `SKILLS.json` total_skills | 1261 | ✅ Matches array |
| `CHANGELOG.md` | v3.13.0 only | ❌ Missing v3.14.0 |

**Action**: CHANGELOG.md needs a v3.14.0 entry documenting stub removal, parser rewrite, and 8 deepened skills.

---

## 2. Description Quality

| Check | Result |
|-------|--------|
| Skills with empty/short description | 0 |
| Skills missing "Use when" trigger | ~659 (lint info-level warnings) |
| All descriptions ≥20 chars | ✅ |

~659 skills have `desc-no-trigger` lint info — descriptions don't start with "Use when". This is a style preference, not a correctness issue.

---

## 3. Registry Integrity

| Check | Result |
|-------|--------|
| SKILLS.json array length matches total_skills | ✅ |
| All registry entries have on-disk files | ✅ |
| Orphan disk files (not in registry) | 86 — all intentional |
| Duplicate registry names | 0 |
| Duplicate on-disk names | 0 |

---

## 4. README Documentation

`README.md` mentions `1ai-skills` 16 times and SKILL.md once. Needs no major update but should mention:
- The orphan sub-skill convention (skills on disk referenced by parent skills, not registered in SKILLS.json)
- The `_rules/` directory at the repo root
- New docs like `reports/` directory and inventory reports

---

## 5. Script Documentation Drift

23/27 scripts in `scripts/` are undocumented (no reference in SKILLS.json, README, or CONTRIBUTING.md). Most are one-shot development tools; utility is limited for external contributors.

**Suggestion**: Add a one-line comment at the top of each script describing its purpose, and add a `scripts/README.md` listing available scripts.
