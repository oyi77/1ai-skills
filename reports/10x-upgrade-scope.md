# 1ai-Skills Repository-Wide Upgrade — Scope & Effort Breakdown

**Baseline**: v3.14.0, 1261 registered skills, 1347 on-disk, 0 lint errors, 1344/1344 tests pass.

## Completed

### Phase 0 — Repository Baseline ✅

Deliverables: `reports/repository-inventory.json`, `repository-inventory.md`, `registry-integrity.json`, `documentation-drift.md`

Key findings: 1549 tracked files, 1347 SKILL.md, 1261 registered, 86 intentional orphans, 0 missing, 0 duplicates. v3.14.0 missing from CHANGELOG. ~2 real broken links. 23 undocumented scripts.

## All Phases — Scope, Effort, Dependencies

| Phase | Name | Est. Sessions | Dependencies | Quick Win? |
|:-----:|------|:-------------:|:------------:|:----------:|
| 1 | Canonical Skill Contract | 3–4 | Phase 0 (done) | Start schema now |
| 2 | Exhaustive Skill-by-Skill Audit | 8–10 | Phase 1 | — |
| 3 | Depth Improvement Pass | 6–10 | Phase 2 | — |
| 4 | Duplication/Overlap Resolution | 3–4 | Phase 0 | Similarity scan now |
| 5 | Skill Routing & Discoverability | 5–8 | Phases 1, 4 | — |
| 6 | Composable Skill Graph | 3–4 | Phases 4, 5 | — |
| 7 | Evaluation & Benchmark System | 4–6 | Phases 1, 2 | — |
| 8 | Validator & Test-Suite Upgrade | 2–3 | Phase 1 (partial) | Broken-link check now |
| 9 | Security & Supply-Chain Audit | 2–3 | — | Git hook audit now |
| 10 | Prompt-Injection Defense | 2 | Phases 1, 9 | — |
| 11 | Permission & Risk Model | 3–4 | Phase 1 | — |
| 12 | Meta-Skill Governance | 2–3 | — | — |
| 13 | Learning Without Memory Pollution | 2 | — | — |
| 14 | Continuous Experimentation | 1–2 | — | — |
| 15 | Multi-Agent Architecture | 3–4 | Phase 5 | — |
| 16 | Business Continuity | 1 | — | Survivability doc now |
| 17 | Infrastructure Reliability | 2–3 | Phase 8 | — |
| 18 | Doc as Tested Product | 2 | — | CHANGELOG fix now |
| 19 | CI/CD Quality Gates | 1–2 | Phases 8, 18 | — |
| 20 | Compatibility/Portability | 2 | — | — |
| 21 | Performance/Cost/Context | 3–4 | Phases 5, 7 | — |
| 22 | Observability & Receipts | 2–3 | Phase 18 | — |
| 23 | Category-Specific Deep Audits | 4–6 | Phases 2, 3, 4 | — |

**Total estimate**: 40–60 sessions for serial execution.

## Prioritized Execution Sequence

### Do now — 0 dependencies, high value
1. Fix CHANGELOG.md (add v3.14.0) — **5 min**
2. Verify/fix README skill count — **5 min**
3. Add broken-link detection to test-skills.py — **30 min**

### Start this session (Phase 1 — Foundation)
4. Design `schemas/skill.schema.json` — **1 session**
5. Build `scripts/validate-skill-schema.py` — **1 session**

### Next sessions
6. Write SKILL_STANDARD.md, QUALITY_RUBRIC.md, VERSIONING.md
7. Build automated audit script for Phase 2
8. Build similarity detector for Phase 4
9. Security review of hooks/ and scripts/

### Deferred
- Routing (Phase 5), Composition (6), Evaluations (7), Multi-Agent (15) — all depend on foundation being laid
- Performance (21), Observability (22) — optimization phases after core is stable
- Category-Specific Audits (23) — after Phase 2 identifies targets

## Immediate Next Action

**Do you want me to start with Phase 1 (skill contract schema + validator), or pick a subset of the quick wins from the list above?**

I recommend: **Phase 1 first** (schema enables everything else), with the **CHANGELOG + README fixes** as break tasks within the same session.
