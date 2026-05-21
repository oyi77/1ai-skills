---
name: hooks-setup
description: Use when user says "install hooks", "setup hooks", "hooks setup", "configure hooks", "/hooks-setup". Installs and configures 1ai-skills auto-evolve hooks for Claude Code.
---

# Hooks Setup — Auto-Evolve Hook Installation

## Overview

Installs and configures 1ai-skills auto-evolve hooks into Claude Code. Hooks track skill usage, capture feedback, auto-commit improvements, and evolve underperforming skills.

**Three install modes:**
- Interactive TUI with config questions
- Non-interactive (accept defaults)
- Status check only

## When to Use

**Automatic Activation** when:
- User says "install hooks", "setup hooks", "hooks setup"
- User says "configure hooks", "hook installation"
- User types "/hooks-setup"
- Session-start detection reports hooks missing/outdated
- User asks "how do I enable auto-evolve?"

## When NOT to Use

- Hooks already installed and up to date
- User is not using Claude Code
- User explicitly says "skip hooks" or "no hooks"

## Process

### Step 1: Check Current State

Run status check first:

```bash
node scripts/hooks-cli.js status
```

If all green (version match, 4/4 scripts, 4 entries), inform user hooks are already set up.

### Step 2: Run Interactive Setup

```bash
node scripts/hooks-tui.js
```

This shows:
1. Status box with current state
2. Install prompt if hooks missing
3. Config questions (auto-push, thresholds, cooldown)
4. Summary of configured settings

### Step 3: Non-Interactive Alternative

If user wants defaults or scripting:

```bash
node scripts/hooks-tui.js --yes
```

### Step 4: Verify

```bash
node scripts/hooks-cli.js status
```

Confirm all items show green checkmarks.

## Available Commands

| Command | Purpose |
|---------|---------|
| `node scripts/hooks-tui.js` | Interactive setup |
| `node scripts/hooks-tui.js --yes` | Non-interactive setup |
| `node scripts/hooks-tui.js --status` | Status display only |
| `node scripts/hooks-cli.js install` | Install hooks only |
| `node scripts/hooks-cli.js uninstall` | Remove hooks cleanly |
| `node scripts/hooks-cli.js status` | Text status report |
| `npm run hooks setup` | Via package.json |
| `npm run hooks install` | Via package.json |

## What Gets Installed

**Hook scripts** (copied to `~/.claude/hooks/`):
- `skill-tracker.js` — logs Skill tool invocations
- `skill-committer.js` — auto-commits skill file changes
- `skill-feedback-capture.js` — detects user feedback signals
- `skill-evolver.js` — identifies underperforming skills

**Settings** (merged into `~/.claude/settings.json`):
- PostToolUse hooks for Skill, Write|Edit tools
- UserPromptSubmit hook for feedback capture
- SessionEnd hook for evolution cycles

**Config** (`~/.1ai-skills/evolve-config.json`):
- Success threshold, min invocations, cooldown
- Auto-push toggle, target repo
- Tracking and evolution toggles

## Verification

After setup, verify:
1. `node scripts/hooks-cli.js status` — all green
2. `node hooks/session-start-detect.js` — silent (healthy)
3. Use any skill → `~/.1ai-skills/metrics.jsonl` grows
