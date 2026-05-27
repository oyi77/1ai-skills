<!-- Parent: ../AGENTS.md -->

# hooks/

## Purpose
Git hooks and session-start scripts for AI agent runtime integration. **Not skill content.** Installed into a consuming repo via `node ../scripts/install-hooks.js`.

## Files

| File | Purpose |
|---|---|
| `hooks.json` | Hook manifest — declares which hooks to install and into which paths |
| `pre-commit.sh` | Git pre-commit hook |
| `post-task.sh` | Runs after agent completes a task |
| `session-start.sh` | Runs at agent session start |
| `session-start-detect.js` | Detects which agent is starting (claude/cursor/opencode) |
| `auto-evolve/` | Self-evolving skill loop hooks (see `meta/auto-evolve` skill) |

## Install
From a consuming repo:
```bash
node node_modules/1ai-skills/scripts/install-hooks.js --yes
```

## For AI Agents
- Do not modify these from inside a session — they're runtime infrastructure.
- To extend the evolve loop, edit `meta/auto-evolve/SKILL.md` instead.
