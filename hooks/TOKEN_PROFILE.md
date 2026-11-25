# Opt-in token-lean skill profile (OMP)

Repo-owned, reversible profile for cutting the always-injected skill metadata list.
It does **not** touch `~/.omp/agent/config.yml`. You activate it by copying one
snippet into your own config.

## Measured budget (rough estimate: chars / 4, not a tokenizer receipt)

| Surface | Count | Characters | Rough tokens |
|---|---:|---:|---:|
| All discovered skills metadata (name + description) | 1,493 | 182,846 | ~45,711 |
| Role anchors + router infrastructure only | 37 | 6,415 | ~1,603 |
| Router hook injection per matching prompt | 1 | ~300 | ~75 |

The system prompt injects the discovered skill list when a tool declares
`readsSkillUris: true`. Hiding catalog metadata is the only lever that
changes this repo-independent cost.

## What the snippet does

`skills.manualSkills: ["*"]` removes every skill from the **model-visible
catalog** but keeps each skill loaded and reachable through `skill://<name>`
and `/skill:<name>`. Skills are not deleted and the runtime mirror is intact.

The repo hook now emits a direct specialist load hint for high-confidence
non-role matches (`brag`, `frontend-design`, ...), so hiding the catalog does
not make named specialists undiscoverable. Regression coverage is in
`scripts/test_skill_router_hook.py` (run: `python3 scripts/test_skill_router_hook.py`).

## Activate (opt-in, user config)

Add to `~/.omp/agent/config.yml`:

```yaml
skills:
  manualSkills: ["*"]
```

Restart the harness. Verify with `omp skill list --json` — skills should report
`hide: true`, and `skill://brag` should still resolve.

## Rollback

Remove the `skills:` block (or set `manualSkills: []`) and restart. Metadata
reappears. No repo file needs changing.

## Tradeoff / limits

- Specialist discovery now depends on the hook hint or an explicit `skill://<name>`.
  Low-confidence queries produce `{}` (silent) by design, unchanged from default.
- Known deterministic-intent misroutes (`pentest the API` → software-engineer,
  `launch video` → owner-idea-intake) are separate routing defects, not token
  optimization; they are out of scope for this profile.
- Savings are **prospective**: ~44,000 rough tokens until the profile is
  activated and confirmed with the harness's own token counter. chars/4 is an
  estimate; an actual tokenizer may differ.
