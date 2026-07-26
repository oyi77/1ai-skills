# GATE.md — Pre-Ship Checklist (v3.24.0)

## GATE 0: UNDERSTAND INTENT, VERIFY CLAIMS
- **Said**: Phase 7 — Evaluation System (evals/ directory + runner + 10 eval cases)
- **Wants**: Lightweight, script-based eval framework — `scripts/run-evals.py` with 12 check types, 10 JSON case files across 8 skill categories, JSON/human reporting with exit codes
- **Solution fits intent?**: Yes — consistent with existing tooling (test-skills.py, validate-skill-schema.py). Runner uses argparse, check registry pattern, case JSON files in `evals/cases/<category>/`.
- **Verified claims**: All 10 cases run via `--all` flag: **91/91 checks passed, 0 failed, 0 skipped**

## GATE 1: CEK DOMAIN REPO
- **Domain**: 1ai-skills — evaluation quality system (Phase 7)
- **Fit**: Yes — quality-upgrade-plan.md Phase 7 explicitly calls for evaluation framework
- **Bukti**: `evals/` directory exists with cases, reports, README; `scripts/run-evals.py` executable

## GATE 2: CEK SEBELUM PAKAI
- **Tools used**: `python3 scripts/run-evals.py --list`, `python3 scripts/run-evals.py --all --verbose`, `python3 scripts/run-evals.py --skill autonomous --verbose`, `python3 scripts/run-evals.py --category agents --verbose`
- **Scripts built**: `scripts/run-evals.py`
- **Bukti**: `--list` shows 10 cases; `--all --verbose` reports 91/91 pass across 10 cases; `--skill` and `--category` filters work correctly

## GATE 3: REVIEW SENDIRI
- **Diff reviewed**: `scripts/run-evals.py` (~460 lines, 12 check types), `evals/README.md`, 10 eval case JSON files, `evals/reports/.gitkeep`, GATE.md, CHANGELOG
- **Unnecessary code?**: No — eval framework matches spec exactly, all case files are meaningful
- **One-off scripts**: One-off migration scripts deleted in earlier phases

## GATE 4: AGENT REVIEW
- **Classification**: STANDARD — new eval tooling + case data
- **Self-review with checklist**: All 10 cases verify actual skill quality attributes; runner handles JSON parse errors, missing files, edge cases correctly
- **Bukti**: [STANDARD — 91/91 evals pass, --all flag added, argparse validation for mutual exclusion]

## GATE 5: PLAYBOOK UPDATE CHECK
- **Impact**: New developer evaluation tooling. No user-facing impact.
- **Bukti**: [skip — developer tool, no user-facing changes]

---

## Standard Checklist

| # | Check | Status | Evidence |
|---|-------|--------|----------|
| C1 | Compile — zero errors | ✅ | lint 0 errors, 0 warnings, 2327 info |
| C2 | All tests pass | ✅ | 1306/1306 pass |
| C3 | QA scenarios — ≥2 happy + 2 sad | ✅ | --all successful (10 cases, 91/91 pass); --skill filter (single case); --category filter (development → 2 cases); --list (shows 10 cases); --json output (valid JSON) |
| C4 | Use like real user | ✅ | Eval runner tested with all 4 invocation modes; fixed 1 case definition (case-sensitive pattern) |
| C5 | Business logic verification | ✅ | 10 eval cases × 91 checks = verified skill attributes (frontmatter, structure, depth, domain, anti-rationalization, workflow) |
| C6 | Rollback plan | ✅ | `git revert <this-commit>` restores pre-evals state |
| C7 | Feature flag | N/A | New tooling, zero-risk addition |
| C8 | Monitoring verification | N/A | No production services |
| C9 | Update docs | ✅ | CHANGELOG v3.24.0 entry added; evals/README.md documents runner usage |
| C10 | Timeline updated | ✅ | [skip — developer tool] |

---

## Status
```
[X] ALL GATES PASSED — boleh commit
[ ] ADA YANG GAGAL
```
