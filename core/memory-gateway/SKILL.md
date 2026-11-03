---
name: memory-gateway
description: Use when saving durable context that another agent or later session will need, handing work between harnesses (Claude, Codex, OMP, OpenCode, Cursor), resuming a task by searching prior decisions and lessons, or diagnosing malformed shared memories. Portable Markdown contract, not a vendor-specific vault binary.
domain: core
subdomain: memory
category: core
version: 1.0.0
author: oyi77
license: Apache-2.0
tags:
- memory
- cross-harness
- context-persistence
- handoff
- knowledge-sharing
triggers:
- shared memory
- cross-agent memory
- memory gateway
- handoff context
- resume task
- persist memory
argument-hint: "[save | recall | handoff]"
---

# Memory Gateway

## Overview

Portable cross-harness memory contract. Stores durable context as plain Markdown documents that any agent (OMP, Claude Code, OpenCode, Cursor, Codex) can read and write without vendor binaries. Inspired by ECC's unified-memory vault architecture, adapted to filesystem-native operations.

The problem it solves: agents lose context across sessions and harnesses. Transcript dumps are too large and harness-specific. The gateway defines a small, inspectable document format with scopes, IDs, and link integrity rules.

## When to Use

**Trigger phrases:**
- "shared memory", "cross-agent memory", "memory gateway"
- "handoff context", "resume task", "persist memory"

Use directly when:
- Saving durable context another agent or later session needs.
- Handing work between harnesses mid-task.
- Resuming a task and searching for prior decisions, facts, or lessons.
- Diagnosing malformed memories, broken links, or duplicate IDs.

## When NOT to Use

- As a task tracker → use `paperclip` or `todo`.
- As a secret store → use env files or Vault skills.
- As a substitute for governed project documentation (README, ADR, CHANGELOG).
- For ephemeral scratch notes within a single session → use `context_notes`.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll paste the whole transcript for the next agent." | Transcripts are megabytes of noise. A 20-line memory doc carries the decision and its constraints. |
| "Memory files will rot and nobody reads them." | Scoped, dated, linked memories with explicit status fields are greppable and expire visibly. Rot is a governance problem, not a format problem. |
| "Each harness has its own memory system, why unify?" | Cross-harness handoffs break when formats diverge. Plain Markdown is the lowest common denominator every agent can parse. |
| "I'll store it in the database instead." | DB rows are opaque to agents reading files. Markdown lives in the repo/workspace where grep, read, and diff work natively. |

## Workflow

### 1. Memory Document Format

Every memory is one Markdown file with YAML frontmatter:

```markdown
---
id: mem-2026-11-01-payment-webhook-fix
scope: project          # project | team | user
type: decision          # decision | fact | lesson | handoff
status: active          # active | superseded | archived
created: 2026-11-01T10:30:00Z
author: omp-session-abc123
links:                  # related memory IDs or file paths
  - ../../docs/adr/0007-hmac-v2.md
tags: [payment, webhook, hmac]
---

# Payment Webhook HMAC Fix Decision

## Context
What prompted this memory (task, failure, discussion).

## Decision
The actual choice made and rejected alternatives.

## Constraints
What future agents MUST respect (invariants, contracts, deadlines).

## Verification
How to prove this memory is still true (command, endpoint, test).
```

### 2. Scopes & Locations

| Scope | Location | Visibility |
|---|---|---|
| `project` | `<repo>/.memory/project/` | Repo-local; gitignore'd unless promoted to team |
| `team` | `<repo>/.memory/team/` | Version-controlled, reviewed via PR |
| `user` | `~/.memory/` | Follows operator across repos |

Project-scope directories require a protective `.gitignore` entry so secrets never leak:

```
# .gitignore
.memory/project/
!.memory/project/.gitkeep
```

Fail closed: refuse writes if `.gitignore` exists with unexpected content.

### 3. Recall Before Write (Idempotence Rule)

Always search for an existing memory before creating a duplicate:

```bash
# grep by tags and type
grep -rl "tags:.*payment" <repo>/.memory/*/ ; \
  grep -l "type: decision" <repo>/.memory/*/
```

If a matching active memory exists, UPDATE it (new revision note) rather than minting a second ID. Duplicate IDs and contradictory actives are the primary failure mode.

### 4. Handoff Protocol

When transferring work between agents or harnesses:

1. Write a `type: handoff` memory containing: goal, current state, blockers, next concrete action, verification command.
2. Communicate the memory path to the receiving agent (via `agent://<id>` message, task context, or explicit file reference).
3. Receiver verifies the stated verification command passes BEFORE continuing.
4. Receiver marks the handoff `status: superseded` and writes their own continuation memory.

### 5. Lifecycle Management

| Event | Action |
|---|---|
| Decision reversed | Mark old memory `status: superseded`, add `links:` to replacement |
| Fact verified stale | Archive with note explaining what changed |
| Quarterly sweep | `grep -L "status: active" .memory/*/` → archive or delete orphans |

Never hard-delete active memories; archive preserves audit trail.

## Link Integrity

Every `links:` entry must resolve:

```bash
# validate links across all memories
python3 - <<'EOF'
import re, sys
from pathlib import Path
bad = 0
for f in Path('.memory').rglob('*.md'):
    text = f.read_text()
    m = re.search(r'^links:\n((?:  - .+\n?)+)', text, re.M)
    if not m: continue
    for line in m.group(1).strip().splitlines():
        target = line.strip('- \n')
        resolved = (f.parent / target).resolve()
        if not resolved.exists():
            print(f"BROKEN {f} -> {target}"); bad += 1
sys.exit(1 if bad else 0)
EOF
```

Run this in CI alongside `check-broken-links.py` if memories live in a tracked repo.

## Verification

- [ ] Every memory has unique `id` with date prefix
- [ ] Search-before-write performed; zero duplicate active topics
- [ ] Project-scope directory protected by `.gitignore`
- [ ] All `links:` targets resolve on disk
- [ ] Handoff memories include runnable verification command
- [ ] Superseded/archived transitions preserve predecessor links