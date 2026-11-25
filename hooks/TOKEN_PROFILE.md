# Opt-in token-lean skill profile (OMP)

Repo-owned, reversible profile for reducing always-injected skill metadata. It does **not** edit `~/.omp/agent/config.yml`; activate by adding the snippet below to your config.

## Measured budget

Rough token estimates use characters / 4; not tokenizer-exact.

| Surface | Count | Characters | Rough tokens |
|---|---:|---:|---:|
| All discovered skill metadata (name + description) | 1,493 | 182,846 | ~45,711 |
| Role anchors + router infrastructure (comparison baseline only) | 37 | 6,415 | ~1,603 |
| Router hook hint when it fires | 1 | ~300 | ~75 |

OMP includes discovered skill metadata in the system prompt when a tool declares `readsSkillUris: true`.

## Opt-in profile

`skills.manualSkills: ["*"]` hides **all** discovered skill metadata, including role anchors. It does not unload or delete skills: `skill://<name>` and `/skill:<name>` remain available. Projected system-prompt metadata approaches zero; the hook adds roughly 75 tokens when it emits a routing hint. Projected savings: ~45,711 rough tokens, pending confirmation with OMP's own token counter.

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
