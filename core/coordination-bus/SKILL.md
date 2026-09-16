---
name: coordination-bus
description: Use when two or more agents share work, when a task spans sessions, or when claiming, heartbeating, completing, or blocking a coordination bus task. The bus is the single source of truth for who owns what — never coordinate through private agreement.
domain: core
author: oyi77
license: Apache-2.0
subdomain: core-platform
tags:
- coordination
- multi-agent
- teamwork
- orchestration
- task-bus
version: 1.0.0
category: core
---

# Coordination Bus

## When to Use

**Trigger phrases:**
- "claim task", "coord status", "coordination status", "bus status"
- "heartbeat task", "complete task", "block task"
- Any multi-agent or multi-session work (RULES.md Rule 19)

**Use cases:**
- Claiming ownership of shared work before starting
- Signalling liveness while working
- Completing or blocking with a reason
- Checking who owns what before touching shared files

**When NOT to use:**
- Single-agent single-session trivial work (no bus needed)
- PaperClip issues (separate tracker — bus is for runtime ownership, not backlog)

## Overview

The coordination bus (1ai-hub `/coordination`) records WHO owns WHAT task, what it depends on, and whether product-gate docs exist. A second claim on an owned task is rejected — the rejection is the conflict signal, not a bug.

## Protocol

1. **Claim before work:** `claim <task-id> as <your-agent-id>` — via chat (`CoordinationExecutor`) or REST `POST /coordination/tasks/{id}/claim` with `{"owner_agent": "..."}`.
2. **Heartbeat while working:** `heartbeat <task-id> as <owner>` or `POST .../heartbeat`. First heartbeat moves `claimed → in_progress`. Stale heartbeat (>15 min) flags the task stuck in daemon supervision.
3. **Finish:** `complete <task-id> as <owner>` or `POST .../complete`. Blocked: `block <task-id> as <owner>: <reason>` or `POST .../block` with `{"reason": "..."}`.
4. **Dependencies:** a task with `depends_on` cannot be claimed until the dependency is `done`. The bus rejects with `blocked: dependency <id> is <status>`.
5. **Product gate:** user-facing tasks carry `gate_required`. Record docs via `POST .../gate-docs` with `{"docs": "path/to/brainstorm.md,..."}` before active work. Daemon flags gate violations every 60s.

## Status

- Chat: `coord status [repo]` — active tasks, stuck list, gate violations.
- REST: `GET /coordination/active?repo=`, `GET /coordination/stuck`, `GET /coordination/gate-violations`.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll just tell the other agent directly" | Private agreement is invisible to the daemon. Claim on the bus or the work doesn't exist. |
| "The claim rejection is a bug" | The rejection IS the conflict signal. Talk to the owner, don't retry. |
| "Gate docs later" | Active work without gate docs is flagged every 60s. Record docs first. |
| "Small task, skip the bus" | If two agents can touch it, it's not small. Claim it. |

## Process

1. **Check** — `coord status [repo]`: is the task free? Are dependencies done?
2. **Claim** — `claim <id> as <owner>`; rejection means someone owns it.
3. **Work** — heartbeat periodically; record gate docs if required.
4. **Close** — complete with detail, or block with reason.

## Verification

- [ ] Task claimed before any file touched
- [ ] Heartbeat fresh (< 15 min) while working
- [ ] Gate docs recorded for user-facing work
- [ ] Task completed or blocked with reason — never abandoned
