# GATE.md — Pre-Ship Checklist (v3.25.0)

## GATE 0: UNDERSTAND INTENT, VERIFY CLAIMS
- **Said**: Phase 8 — Validator Strict Mode + broken-link checker
- **Wants**: `--strict` flag on `validate-skill-schema.py` promoting warnings→errors; `scripts/check-broken-links.py` scanning internal `/skills/` refs against SKILLS.json
- **Solution fits intent?**: Yes — `--strict` is opt-in flag (0 impact on existing CI); broken-link checker scans all `.md` files (not just SKILL.md) for `skill://`, `/skills/`, `../skills/` references
- **Verified claims**: Default validator exits 0, `--strict` exits 1 with 211 warnings promoted; 1439 files scanned with 0 broken internal references

## GATE 1: CEK DOMAIN REPO
- **Domain**: 1ai-skills — validator quality improvements (Phase 8)
- **Fit**: Yes — quality upgrade plan Phase 8
- **Bukti**: `scripts/validate-skill-schema.py --strict` exits 1 when warnings present; `scripts/check-broken-links.py` scans 1439 files

## GATE 2: CEK SEBELUM PAKAI
- **Tools used**: `python3 scripts/validate-skill-schema.py`, `python3 scripts/validate-skill-schema.py --strict`, `python3 scripts/check-broken-links.py --verbose`, `python3 scripts/check-broken-links.py --json`, `python3 scripts/check-broken-links.py --exit-zero`
- **Scripts built**: `scripts/check-broken-links.py` (new); `scripts/validate-skill-schema.py` (modified)
- **Bukti**: Default exit 0 (1309/1309, 211 warnings); `--strict` exit 1; broken-link: 1439 scanned, 0 broken, `--json` valid, `--exit-zero` overrides exit to 0

## GATE 3: REVIEW SENDIRI
- **Diff reviewed**: `scripts/validate-skill-schema.py` (def main()+argparse extraction + exit logic); `scripts/check-broken-links.py` (full ~150-line new checker); CHANGELOG, GATE.md
- **Unnecessary code?**: No — both tools are tightly scoped. Broken-link checker handles 3 reference patterns (`skill://`, `/skills/`, `../skills/`) and nothing more.
- **One-off scripts**: `scripts/test-check-broken-links.py` deleted after verification (YAGNI)

## GATE 4: AGENT REVIEW
- **Classification**: STANDARD — new CLI flags + new tool; both non-destructive
- **Self-review with checklist**: `--strict` opt-in preserves existing CI behavior; broken-link checker is read-only, never modifies files
- **Bukti**: [STANDARD — validator tests 2 modes × 2 exit codes; broken-link checker tests normal/JSON/exit-zero/broken-found scenarios]

## GATE 5: PLAYBOOK UPDATE CHECK
- **Impact**: Developer tooling only. No user-facing changes.
- **Bukti**: [skip — developer tool, no user-facing changes]

---

## Standard Checklist

| # | Check | Status | Evidence |
|---|-------|--------|----------|
| C1 | Compile — zero errors | ✅ | lint 0 errors, 0 warnings, 2327 info |
| C2 | All tests pass | ✅ | 1306/1306 pass |
| C3 | QA scenarios — ≥2 happy + 2 sad | ✅ | Validator: default (happy→0), --strict (warning→1); Broken-link: 1439 scanned/0 broken (happy), --exit-zero (override), --json (valid JSON output) |
| C4 | Use like real user | ✅ | Validator tested with/without --strict; broken-link tested with --verbose, --json, --exit-zero; smoke test validated broken detection with controlled temp file |
| C5 | Business logic verification | ✅ | --strict exit 1 verified via subprocess (211 warnings promoted); broken-link correctly reports 0 broken on clean repo |
| C6 | Rollback plan | ✅ | `git revert <this-commit>` restores pre-Phase-8 state |
| C7 | Feature flag | N/A | --strict is opt-in flag; broken-link checker is standalone script |
| C8 | Monitoring verification | N/A | No production services |
| C9 | Update docs | ✅ | CHANGELOG v3.25.0 entry added with all verified counts |
| C10 | Timeline updated | ✅ | [skip — developer tool] |

---

## Status
```
[X] ALL GATES PASSED — boleh commit
[ ] ADA YANG GAGAL
```
