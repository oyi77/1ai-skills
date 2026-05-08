---
persona:
  name: "Deborah Gordon"
  title: "The Swarm Intelligence Expert - Master of Collective Behavior"
  expertise: ['Swarm Intelligence', 'Collective Decision Making', 'Distributed Systems', 'Emergent Behavior']
  philosophy: "Simple rules, complex behavior."
  credentials: ['Stanford Biology Professor', 'Ant colony researcher', 'Swarm robotics advisor']
  principles: ['Local rules, global patterns', 'No central control', 'Adapt to environment', 'Decentralized decisions']

---

name: hive-mind
description: Sync memories across multiple agents using a shared TiDB Zero database.
metadata:
  openclaw:
    emoji: 🐝
    requires:
      bins: ["python3", "curl"]
      env: ["TIDB_HOST", "TIDB_PORT", "TIDB_USER", "TIDB_PASSWORD"]
---

# Hive Mind (Powered by TiDB Zero)

## Overview
**Hive Mind** is a shared configuration store for your AI Agent. It acts like an "iCloud Keychain" for agent settings and user preferences, syncing them across all your devices instantly.

## Security & Provisioning
This skill supports two modes:
1.  **BYO Database (Recommended):** Provide `TIDB_*` credentials via environment variables.
2.  **Auto-Provisioning (Fallback):** If no credentials are provided, it calls the TiDB Zero API to create a free, ephemeral database and caches the connection locally (`~/.openclaw_hive_mind_dsn`).

## Why use this?
*   **Sync:** Update your preferred theme ("Dark Mode") on your Desktop, and your Mobile Agent respects it immediately.
*   **Persistent Preferences:** Settings survive container restarts and clean reinstalls.
*   **Team Collaboration:** Share common configuration across multiple agents in a team.

## Prerequisites
*   **TiDB Zero:** Requires a serverless cluster.
*   **Protocol:** Follow the installation guide below to add it to your agent's `PROTOCOL.md`.

## Installation

### 1. Add to `TOOLS.md`
```markdown
- **hive-mind**: Store/Retrieve persistent key-value preferences.
  - **Location**: `{baseDir}/skills/hive_mind/SKILL.md`
  - **Command**: `python {baseDir}/skills/hive_mind/run.py --action set --key "theme" --value "dark"`
```

### 2. Add to `AGENTS.md` (Protocol)
Copy [PROTOCOL.md](PROTOCOL.md).

## Usage
*   **Set:** `python {baseDir}/run.py --action set --key "user.timezone" --value "UTC"`
*   **Get:** `python {baseDir}/run.py --action get --key "user.timezone"`
*   **List:** `python {baseDir}/run.py --action list` -> Returns all stored preferences.
## When NOT to Use

- [TODO: Add specific exclusion cases for this skill]
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- [TODO: Add behavioral signs the skill is being violated]
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] [TODO: Add specific evidence-based checklist items]
- [ ] All required outputs generated
- [ ] Success criteria met

