# 1ai-skills Auto-Evolve System

**Universal skill evolution for any AI assistant.** Skills learn from usage, capture your feedback, and commit improvements automatically.

Works with: Claude Code, OpenClaw, OpenCode, Hermes-Agent, or any tool that can run shell commands.

## Quick Install

```bash
# From cloned repo:
bash hooks/auto-evolve/install.sh

# Or standalone:
node hooks/auto-evolve/1ai-evolve.js install
```

## Two Ways to Use

### 1. CLI (any tool, any shell)

```bash
# Track a skill invocation
1ai-evolve track bug-bounty success 150
1ai-evolve track content-generator fail 50

# Capture feedback
1ai-evolve feedback bug-bounty "always check scope first, never skip recon"
1ai-evolve feedback content-generator "prefer viral hooks in first 3 seconds"

# Check stats
1ai-evolve stats
1ai-evolve stats bug-bounty

# Run evolution cycle
1ai-evolve evolve
```

### 2. HTTP API (daemon mode)

```bash
# Start daemon (file watcher + API on port 9847)
1ai-evolve start

# Or install as systemd service
1ai-evolve install
```

Any AI tool can call the API:

```bash
# Track
curl -X POST http://localhost:9847/track \
  -d '{"skill":"bug-bounty","success":true,"tokens":150}'

# Feedback
curl -X POST http://localhost:9847/feedback \
  -d '{"skill":"bug-bounty","message":"always check scope first"}'

# Stats
curl http://localhost:9847/stats
curl http://localhost:9847/stats/bug-bounty
```

## How It Works

```
1. You use a skill (any tool)
   → 1ai-evolve track skill-name success

2. You give feedback ("do it this way")
   → 1ai-evolve feedback skill-name "your insight"

3. Session ends → evolver scores skills
   → Skills < 70% success rate get queued for rewrite

4. Skill file changes → auto-commit to GitHub
   → git push to your repo
```

## Integrating With Your AI Tool

### Claude Code
Hooks auto-installed by `install.sh`. Skills tracked automatically.

### OpenClaw
Add to your agent's workflow:
```python
import subprocess
subprocess.run(["1ai-evolve", "track", skill_name, "success"])
subprocess.run(["1ai-evolve", "feedback", skill_name, user_feedback])
```

### OpenCode / Hermes / Any CLI Agent
```bash
# In your agent's shell wrapper:
after_skill() {
  1ai-evolve track "$SKILL_NAME" "success" "$TOKEN_COUNT"
}

on_user_feedback() {
  1ai-evolve feedback "$SKILL_NAME" "$USER_MESSAGE"
}
```

### HTTP Integration (any language)
```javascript
// JavaScript/Node
await fetch('http://localhost:9847/track', {
  method: 'POST',
  body: JSON.stringify({ skill: 'my-skill', success: true })
});
```

```python
# Python
import requests
requests.post('http://localhost:9847/track', json={'skill': 'my-skill', 'success': True})
```

## Config

`~/.1ai-skills/evolve-config.json`:

```json
{
  "min_invocations": 5,
  "success_threshold": 70,
  "evolve_cooldown_hours": 24,
  "max_evolves_per_run": 3,
  "auto_push": true,
  "target_repo": "you/1ai-skills",
  "skill_dirs": ["~/.claude/skills", "~/.openclaw/skills"],
  "repo_dir": "~/projects/1ai-skills"
}
```

## Files

| File | Purpose |
|------|---------|
| `~/.1ai-skills/metrics.jsonl` | Raw invocation log |
| `~/.1ai-skills/feedback.jsonl` | User feedback log |
| `~/.1ai-skills/stats.json` | Aggregate per-skill stats |
| `~/.1ai-skills/evolve-queue.jsonl` | Pending improvements |
| `~/.1ai-skills/daemon.log` | Daemon logs |

## Uninstall

```bash
1ai-evolve stop
rm -rf ~/.1ai-skills
rm ~/.claude/hooks/skill-{tracker,evolver,committer,feedback-capture}.js
# Remove hooks from ~/.claude/settings.json
```
