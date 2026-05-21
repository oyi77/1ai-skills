---
name: hooks-setup
description: Use when user says "install hooks", "setup hooks", "hooks setup", "configure hooks", "/hooks-setup". Installs and configures 1ai-skills auto-evolve hooks for Claude Code.
---

# Hooks Setup — AI Agent Installation Guide

## Overview

Installs and configures 1ai-skills auto-evolve hooks. Tracks skill usage, captures feedback, auto-commits improvements, evolves underperforming skills.

## When to Use

**Activate when:**
- User says "install hooks", "setup hooks", "hooks setup"
- User says "configure hooks", "hook installation"
- User types "/hooks-setup"
- Session-start detection reports hooks missing/outdated
- User asks "how do I enable auto-evolve?"

**Skip when:**
- Hooks already installed and up to date
- User explicitly says "skip hooks" or "no hooks"

## Agent Workflow

### Step 1: Check Status

```bash
node scripts/hooks-cli.js status
```

If all green (version match, 4/4 scripts, 4 entries), tell user hooks already set up. Skip to Step 5.

### Step 2: Install (non-interactive)

```bash
node scripts/install-hooks.js --yes
```

This copies hook scripts, merges settings.json, creates config, writes version stamp. Skips star/fork prompt.

### Step 3: Configure (ask user, write config)

Read current config:

```bash
cat ~/.1ai-skills/evolve-config.json
```

Ask user these questions (one at a time, use AskUserQuestion tool):

1. **Auto-push evolved skills?** (default: no)
   - If yes: "What repo? (e.g. user/repo)"

2. **Success threshold %** (default: 70)
   - Skills below this get auto-evolved

3. **Min invocations before evolving** (default: 5)

4. **Cooldown between evolve cycles** (default: 24 hours)

5. **Enable tracking?** (default: yes)

6. **Enable auto-evolution?** (default: yes)

Write answers to config:

```bash
# Edit ~/.1ai-skills/evolve-config.json with user choices
```

### Step 4: Star/Fork (ask user)

Ask: "Want to star & fork oyi77/1ai-skills on GitHub?"

If yes:
```bash
gh repo star oyi77/1ai-skills
gh repo fork oyi77/1ai-skills --clone=false
```

If no gh CLI: tell user to visit github.com/oyi77/1ai-skills

### Step 5: Verify

```bash
node scripts/hooks-cli.js status
```

Confirm all items green. Tell user hooks are active.

## Direct Commands (no TUI needed)

| Command | Purpose |
|---------|---------|
| `node scripts/install-hooks.js` | Install hooks (prompts star/fork) |
| `node scripts/install-hooks.js --yes` | Install hooks (no prompts) |
| `node scripts/hooks-cli.js status` | Text status report |
| `node scripts/hooks-cli.js uninstall` | Remove hooks cleanly |
| `node hooks/session-start-detect.js` | Health check (silent=healthy) |

## Config File

Location: `~/.1ai-skills/evolve-config.json`

```json
{
  "min_invocations": 5,
  "success_threshold": 70,
  "evolve_cooldown_hours": 24,
  "max_evolves_per_run": 3,
  "auto_push": false,
  "target_repo": "",
  "skill_dirs": ["~/.claude/skills"],
  "repo_dir": "",
  "commit_prefix": "evolve",
  "tracking_enabled": true,
  "evolve_enabled": true
}
```

Agent can read/write this file directly to configure.

## What Gets Installed

**Hook scripts** (to `~/.claude/hooks/`):
- `skill-tracker.js` — logs Skill tool invocations
- `skill-committer.js` — auto-commits skill file changes
- `skill-feedback-capture.js` — detects user feedback signals
- `skill-evolver.js` — identifies underperforming skills

**Settings** (merged into `~/.claude/settings.json`):
- PostToolUse hooks for Skill, Write|Edit tools
- UserPromptSubmit hook for feedback capture
- SessionEnd hook for evolution cycles

**Config** (`~/.1ai-skills/evolve-config.json`):
- Auto-detected agent skill dirs
- Thresholds, cooldown, push settings
