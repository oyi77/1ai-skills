# Opt-in token-lean skill profile (OMP)

Repo-owned, reversible profile reducing always-injected skill metadata. The profile file does **not** edit `~/.omp/agent/config.yml`; local activation is separate and requires adding the snippet below.

## Offline tokenizer budget (metadata upper-bound estimate)

| Surface | Count | Characters | o200k_base (GPT-4o/5) | deepseek-v3/v4 | claude-v3 |
|---|---:|---:|---:|---:|---:|
| All discovered skill metadata (name + description) | 1,493 | 185,831 | **38,334** | **39,428** | **44,809** |
| Role anchors + router infrastructure (comparison baseline) | 37 | 6,488 | 1,306 | 1,330 | 1,461 |
| Router hook hint when it fires | 1 | ~300 | ~65 | ~65 | ~75 |

OMP includes discovered skill metadata in the system prompt when a tool declares `readsSkillUris: true`.

`skills.manualSkills: ["*"]` hides **all** discovered skill metadata, including role anchors. Skills stay loaded; `skill://<name>` and `/skill:<name>` remain available. If the catalog was injected, offline tokenizer receipts indicate up to **38,334 o200k_base tokens**, **39,428 DeepSeek V3/V4 tokens**, or **44,809 Claude V3 tokens** of metadata would be removed; these are not fresh-session prompt-token measurements.

The repo hook emits direct specialist hints for brag, launch-video, anti-slop/frontend design, Hallmark, Impeccable, AI SEO, Cloudflare security audit, and API-key leak validation. See `scripts/test_skill_router_hook.py`.

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
- Offline tokenizer totals estimate metadata removed if a catalog was injected; fresh-session before/after prompt-token savings remain unmeasured.
