<!-- Parent: ../AGENTS.md -->

# scripts/

## Purpose
Repo maintenance utilities. **Not skill content.**

## Files

| File | Purpose |
|---|---|
| `audit-skills.sh` | **Source-of-truth counter.** Walks the tree, counts SKILL.md per category, emits `SKILLS.json`. Run after adding/removing skills. |
| `validate-skills.py` | **Hard validator.** Parses every SKILL.md frontmatter, checks required fields (`name`, `description`), name-vs-dir consistency. Supports `--fix` for auto-repair. CI runs this on every PR. |
| `install-hooks.js` | Installs `../hooks/` into the consuming repo's `.git/hooks/` |
| `hooks-cli.js` | Interactive CLI for managing hooks |
| `hooks-tui.js` | TUI variant of hooks-cli |
| `add-missing-sections.py` | Legacy: adds standard sections to skill docs |
| `create_discord_server.py` | Discord submission helper |
| `setup-discord.sh` | Discord setup wrapper |
| `submit_to_huggingface.py` | HF Spaces submission |
| `submit_to_langchain.py` | LangChain Hub submission |
| `hf_submit.py` | HF submission helper |
| `test_gallery_stats.py` | Standalone test for skill gallery stats |
| `trading/` | Support modules extracted from skills (guardrails, pipeline, vector db integration) |

## Workflow

After adding/removing/renaming a skill:
```bash
python3 scripts/validate-skills.py        # ensure all valid
bash scripts/audit-skills.sh --write      # refresh SKILLS.json
```

CI enforces both. PRs that drift will fail.

## For AI Agents
- Use these scripts via `bash` / `python3` — they're meant to be run directly.
- `validate-skills.py --fix` will auto-repair missing closing `---`, backfill `name` from dir name, and synthesize `description` from H1 if missing.
