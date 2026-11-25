# Opt-in token-lean skill profile (OMP)

Repo-owned, reversible profile for reducing always-injected skill metadata. It does **not** edit `~/.omp/agent/config.yml`; activate by adding the snippet below to your config.

## Measured budget (real tokenizer receipt via `omp toks`)

| Surface | Count | Characters | o200k_base (GPT-4o/5) | deepseek-v3/v4 | claude-v3 |
|---|---:|---:|---:|---:|---:|
| All discovered skill metadata (name + description) | 1,493 | 185,831 | **38,334** | **39,428** | **44,809** |
| Role anchors + router infrastructure (comparison baseline) | 37 | 6,488 | 1,306 | 1,330 | 1,461 |
| Router hook hint when it fires | 1 | ~300 | ~65 | ~65 | ~75 |

OMP includes discovered skill metadata in the system prompt when a tool declares `readsSkillUris: true`.

`skills.manualSkills: ["*"]` hides **all** discovered skill metadata, including role anchors. Skills stay loaded; `skill://<name>` and `/skill:<name>` remain available. With the wildcard applied, system-prompt metadata drops to near zero; the hook adds ~65–75 real tokens when it fires. Measured saving: **38,334 tokens (o200k), 44,809 tokens (claude-v3), depending on model family.**

The repo hook emits direct specialist hints for explicit brag and launch-video phrases, high-confidence specialist matches, and pentest/security intent. See `scripts/test_skill_router_hook.py`.

## Activate (opt-in)

Add to `~/.omp/agent/config.yml`:

```yaml
skills:
  manualSkills: ["*"]
```

Restart OMP. Check `omp skill list --json` for `hide: true`, then verify `skill://brag` still resolves. Measure prompt tokens before and after with OMP's token counter; chars/4 is only a rough estimate.

## Rollback

Remove the `skills:` block or set `manualSkills: []`, then restart. Metadata reappears; repository files and runtime mirror remain unchanged.

## Tradeoffs

- Every skill becomes manual-only in the model-visible catalog. Discovery relies on explicit `skill://<name>` calls or the router hook.
- The role-only figure above is a comparison baseline, **not** the remaining metadata cost under `manualSkills: ["*"]`.
- Projected savings are not realized until the user activates the profile and verifies actual prompt tokens.
