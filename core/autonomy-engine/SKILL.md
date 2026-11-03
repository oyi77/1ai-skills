---
description: Use when core autonomy protocol for AI agent operations. Defines how
  agents operate 24/7 without human prompts — monitoring all systems, generating revenue,
  managing team, escalating decisions, and growing. Use this skill to understand an
  autonomous operating system. Use when working with autonomy engine.
domain: core
author: oyi77
license: Apache-2.0
subdomain: core-platform
name: autonomy-engine
tags:
- autonomy
- engine
- infrastructure
- memory
- monitoring
- self-improvement
triggers:
- autonomy engine
- 24/7 agent operation
- autonomous operating system
- unattended agent loop
- agent escalation policy
- decision ladder
argument-hint: "[loop or capability]"
version: 1.0.0
category: core
---

# Autonomy Engine

## When to Use

**Trigger phrases:**
- "autonomy engine"
- "24/7 agent operation", "autonomous operating system"
- "agent without human prompt", "unattended agent loop"
- "escalation policy for agent"

- When operating an agent or fleet continuously without a human initiating each run
- When defining which decisions an agent may take alone vs. which must escalate
- When wiring monitoring, revenue, and team-management loops into one operating cycle

## When NOT to Use

- Single-shot tasks a human drives end-to-end (use the relevant domain skill directly)
- Human-in-the-loop reviews where each step needs approval (use `development/role-product-manager` or an ops runbook)
- When an existing scheduler/cron already runs the loop — extend it rather than adding a second engine

## Overview

The Autonomy Engine is the operating protocol that lets AI agents run 24/7 without per-prompt human direction: it monitors systems, generates revenue, manages delegated team work, escalates only what genuinely needs a human, and compounds its own skill library over time.

Autonomy is bounded autonomy, not unsupervised autonomy. The engine's core contract is a **decision ladder**:

```text
[Act freely] → [Act + log] → [Act + notify] → [Escalate before acting]
```

Every recurring capability gets a rung on that ladder before it is allowed to run unattended. Anything without an assigned rung defaults to "escalate before acting" — fail closed.

## Architecture: The Five Operating Loops

The engine runs five loops on different cadences. Each loop is a named, restartable job with an owner skill, so a crashed loop can be identified and resumed from its last checkpoint instead of silently dying.

| Loop | Cadence | Owner | Stages | Fail-Closed Rule |
|---|---|---|---|---|
| **Monitor** | Every 5–15 min | `core/systematic-*` health probes | Probe → classify → act/escalate | Probe failure twice → page owner, never silently skip |
| **Revenue** | Daily + event-driven | `marketing/`, `financial/` skills | Discover → qualify → execute → record | Any spend or money movement requires pre-approved budget cap |
| **Team** | Daily stand-up + weekly review | `operations/` skills | Assign → track → unblock → review | Blocked >24h → escalate to human owner |
| **Escalate** | Per event | This skill | Classify → attempt level below → escalate | Default = escalate when uncertain |
| **Grow** | Weekly | `core/auto-evolver`, `core/auto-consolidator` | Mine → propose → validate → register | No unvalidated skill promotion; full ladder required |

```text
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Monitor     │───►│   Act or     │───►│   Record     │
│  (5–15 min)  │    │   Escalate   │    │   Receipt    │
└──────────────┘    └──────────────┘    └──────────────┘
        ▲                                       │
        │            ┌──────────────┐           │
        └────────────│   Grow       │◄──────────┘
                     │  (weekly)    │
                     └──────────────┘
   Revenue and Team loops run on their own cadences, feeding the same receipt log.
```

### State Management

- **Last-good state**: each loop persists its last successful checkpoint (timestamp + summary) so a restart resumes rather than re-runs destructive work.
- **Receipt log**: every action appends an immutable receipt (action, inputs, outcome, cost). Unrecorded actions are treated as failures by the next audit.
- **Budget ledger**: revenue and tool spend draw down from a pre-approved cap; hitting the cap halts spend actions and opens an escalation.

## Decision Ladder (Escalation Policy)

Before any capability runs unattended, assign it a rung:

| Rung | Meaning | Example | Requirement |
|---|---|---|---|
| **L0 — Act freely** | Fully reversible, zero cost | Re-indexing skills, cache refresh | Log receipt only |
| **L1 — Act + log** | Reversible, low risk | Formatting fixes, doc updates | Receipt + diff retained |
| **L2 — Act + notify** | Reversible but visible to users | Posting to a low-stakes channel | Receipt + async notify |
| **L3 — Escalate first** | Irreversible, costly, or external | Sending money, deleting data, publishing to customers, prod deploys | Human approval before execution |

Rules:
- **Default is L3.** Promote a capability to L0–L2 only with evidence it has run safely N times.
- **Financial actions are always L3** unless a written budget cap and refund path exist (`production-money-chain-proof`).
- **Account/security changes are always L3** (see harness rules on point-of-risk confirmation).

## Escalation Protocol

1. **Classify** the decision: reversible? internal/external? cost? blast radius?
2. **Try one rung below** — attempt a safe, partial, or read-only version of the action first.
3. **Escalate with a compact brief**: what happened, what you propose, the cost/risk, the default action if no reply arrives (state it explicitly), and a deadline.
4. **Never escalate trivia** — questions answerable by the repo, docs, or tools must be resolved before bothering the human.

## Revenue Loop Discipline

- Every spend traces to a budget line; the ledger is authoritative, not memory.
- Every claimed revenue result carries a receipt (invoice ID, webhook ID, transaction hash).
- Claims without receipts go back to measurement before being reported (`production-money-chain-proof`).

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll add monitoring later" | An unmonitored loop fails silently for days. Probes and receipts ship with the loop, not after. |
| "The agent should just decide — escalation is weakness" | Unbounded autonomy converts a recoverable mistake into an irreversible one. The ladder exists so speed and safety don't compete. |
| "The loop ran fine yesterday, assume it's fine" | Scheduler gaps, dead processes, and credential expiry are silent. Verify with receipts, not memory. |
| "More automation is always better" | Automation without a decision rung is an unowned side effect. Nothing runs unattended without an assigned rung. |
| "I can track spend in my head" | Budgets drift without a ledger. Draw down from the cap; halt at zero. |

```python
# Decision-ladder classifier: defaults to escalation (fail closed).
LADDER = {
    "reversible_no_cost": "L0",
    "reversible_low_risk": "L1",
    "visible_external": "L2",
    "irreversible_or_paid": "L3",
}

def decision_rung(action: dict) -> str:
    if action.get("category") in {"money", "deploy", "delete", "security"}:
        return "L3"                      # never auto-promoted
    key = "reversible_no_cost" if action.get("free") and action.get("reversible") \
          else "reversible_low_risk" if action.get("reversible") \
          else "visible_external" if action.get("external") \
          else "irreversible_or_paid"
    return LADDER[key]
```

## Process

1. **Assign rungs** — classify every recurring capability on the ladder; anything new starts at L3.
2. **Wire loops** — start Monitor; add Revenue/Team/Grow on their cadences; persist checkpoint + receipt log.
3. **Run closed** — execute, record receipts, draw budgets from the ledger, halt at cap.
4. **Escalate correctly** — one rung below first, then a compact brief with default action and deadline.
5. **Compound weekly** — `auto-evolver` mines receipts for upgrades, `auto-consolidator` prunes; both through the full validation ladder.

## Verification

- [ ] Every unattended capability has an assigned decision rung (default L3)
- [ ] Financial and security actions blocked at L3 with human approval
- [ ] Each loop persists a last-good checkpoint and can resume after restart
- [ ] Every action appends an immutable receipt (no unrecorded actions)
- [ ] Budget ledger enforces pre-approved cap; spend halts at zero
- [ ] Escalation briefs include proposed action, cost/risk, default action, deadline
- [ ] Weekly Grow loop runs through the full validation ladder before registering anything