---
name: human-escalation
version: 1.0.0
severity: mandatory
scope: [all]
pairs-with: [decision, roles, comms]
description: Protocol for agent-to-human escalation when an agent encounters high-stakes decisions outside its autonomy boundary
---
# HUMAN_ESCALATION — Human-in-the-Loop Escalation Protocol

> **Status:** v1.0.0 | **Severity:** mandatory | **Scope:** [all agents]
> **Description:** Protocol for agent-to-human escalation when an agent encounters high-stakes decisions outside its autonomy boundary.

---

## §1 — Purpose

GATE.md Gates 0–4 are entirely agent-self-checked. For operations with irreversible or high-impact consequences, the agent MUST pause and wait for human approval before proceeding.

This document defines:
- **When** an agent MUST escalate (trigger criteria)
- **How** an agent escalates (JSON file protocol)
- **What** happens while waiting (pause + poll)
- **How** the human responds (approve / deny / timeout)

---

## §2 — Trigger Criteria

An agent MUST escalate (STOP and wait for human approval) before executing ANY of the following:

### 2.1 Destructive Operations
- `DELETE` / `DROP` / `TRUNCATE` on database tables or rows
- `rm -rf`, `rm -r`, or forced deletion of files/directories outside the agent's scratch space
- Database wipe, schema migration rollback that drops columns with data
- Volume deletion, snapshot deletion, or any irreversible storage operation
- Git operations: force push (`--force` / `push --force-with-lease`), branch deletion, reset --hard on shared branches

### 2.2 Financial Transactions
- Any operation costing more than **$5 USD** (or equivalent in any currency)
- Sending invoices, creating billing records, initiating payments
- Upgrading/downgrading paid service tiers
- Creating or modifying subscription plans
- Purchasing domains, certificates, or third-party services

### 2.3 External Contracts & Legal
- Signing any agreement, ToS, EULA, or legally binding statement
- Accepting third-party terms of service
- Making representations, warranties, or commitments on behalf of the organization
- Responding to legal requests, DMCA notices, or regulatory inquiries
- Changing privacy policy, data processing agreements, or consent flows

### 2.4 Identity & Access Operations
- Creating or deleting user accounts
- Changing permissions, roles, or group memberships
- Granting or revoking access tokens, API keys, or credentials
- Password resets (unless part of a verified self-service flow)
- Modifying MFA, SSO, or authentication provider configuration

### 2.5 Production Deployment
- Pushing code or configuration to **production** environment
- Running database migrations on production
- Modifying production environment variables or secrets
- Changing DNS records, TLS certificates, or CDN configuration on production domains

> **Note:** Development, staging, preview, and local environments are EXEMPT from mandatory escalation. Agents MAY operate freely in non-production environments unless the operation also matches another trigger category (e.g., financial).

### 2.6 Optional Escalation (agent discretion)

An agent MAY escalate for any of these, based on confidence and impact assessment:

- Deleting data created by a human user (as opposed to agent-generated data)
- Operations on environments with pending human work
- Any action the agent has < 90% confidence in the outcome
- First-time operations on a new provider or service

---

## §3 — Escalation Format

Each escalation is a JSON file written to:

```
~/.1ai/escalations/{id}.json
```

### 3.1 Schema

```json
{
  "id": "esc-20260713-001",
  "timestamp": "2026-07-13T12:00:00Z",
  "agent": "agent-name",
  "severity": "blocking",
  "action": "DELETE FROM users WHERE id = 42",
  "context": "User requested account deletion via support ticket #1234",
  "reason": "Data loss — cannot undo",
  "impact": "Removes user 42 and all associated records",
  "status": "pending"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique ID: `esc-YYYYMMDD-NNN` (zero-padded counter, e.g. `001`) |
| `timestamp` | string | ISO 8601 UTC timestamp (`date -u +%Y-%m-%dT%H:%M:%SZ`) |
| `agent` | string | Agent name from `$AGENT_NAME` or hostname |
| `severity` | string | `"blocking"` (MUST approve to proceed) or `"advisory"` (informational) |
| `action` | string | The proposed operation, in plain language or code |
| `context` | string | What led to this action (user request, system state, etc.) |
| `reason` | string | Why escalation is required (which trigger rule) |
| `impact` | string | What happens if executed (data loss, cost, downtime, etc.) |
| `status` | string | `"pending"` (waiting), `"approved"`, `"denied"`, `"timed_out"`, `"cancelled"` |

### 3.2 Response File

The human writes a response to:

```
~/.1ai/escalations/{id}.response.json
```

```json
{
  "approved": true,
  "comment": "Go ahead, but run a dry-run first."
}
```

Or:

```json
{
  "approved": false,
  "comment": "This is too risky right now. Schedule for next maintenance window."
}
```

---

## §4 — Escalation Flow

```
┌──────────────────────────────────────────┐
│ 1. Agent detects trigger condition        │
│    (matches §2 criteria)                  │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│ 2. Agent writes escalation JSON           │
│    → ~/.1ai/escalations/{id}.json        │
│    status: "pending"                      │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│ 3. Agent prints notification to console   │
│    ESCALATION: {id} — waiting for approval│
│    Action: {action}                       │
│    Reason: {reason}                       │
│    Impact: {impact}                       │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│ 4. Agent PAUSES — no further action on    │
│    this decision. Other work continues.   │
│    Agent logs the pause in LOG.json.      │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│ 5. Human reviews escalation               │
│    Writes response to:                    │
│    ~/.1ai/escalations/{id}.response.json  │
│    { approved: true/false, comment }      │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│ 6. Agent detects response file (poll or   │
│    human signals CONTINUE)                │
│    Reads response, updates escalation     │
│    status in JSON + LOG.json             │
└──────────────┬───────────────────────────┘
               │
    ┌──────────┴──────────┐
    ▼                     ▼
┌──────────┐       ┌──────────┐
│ APPROVED │       │  DENIED  │
│ Proceed  │       │  Abort   │
│ Execute  │       │  Log     │
│ action   │       │  outcome │
└──────────┘       └──────────┘
```

### 4.1 Polling Behavior

- Agent SHOULD poll `~/.1ai/escalations/` for `.response.json` files matching pending escalations
- Poll interval: every **30 seconds** (minimum), adjustable by agent
- Human may signal approval faster via `CONTINUE` or other channel-level signal
- When response is detected:
  1. Read and parse the response file
  2. Update the escalation JSON: `status: "approved"` or `"denied"`
  3. Append to LOG.json
  4. Either proceed or abort

---

## §5 — Default Policies on Timeout

If no human response is received within **30 minutes**, the applicable default policy takes effect:

| Trigger Category | Default | Description |
|-----------------|---------|-------------|
| Destructive ops | **DENY** | Abort — do not execute |
| Financial | **DENY** | Abort — do not execute |
| External contracts | **DENY** | Abort — do not execute |
| Identity | **DENY** | Abort — do not execute |
| Deployment (production) | **DENY** | Abort — do not deploy |
| Deployment (preview/staging) | **ALLOW** | Proceed (low risk) |

On timeout:
1. Agent updates escalation JSON: `status: "timed_out"`, adds `"timeout_rule": "deny"` (or `"allow"`)
2. Appends timeout record to LOG.json
3. Applies the default policy (DENY or ALLOW)

---

## §6 — Escalation Record Log

**File:** `~/.1ai/escalations/LOG.json`

Append-only log of all escalations with outcomes. Each line is a separate JSON object (one per escalation lifecycle event):

```jsonl
{"id":"esc-20260713-001","timestamp":"2026-07-13T12:00:00Z","agent":"agent-1","action":"DELETE FROM users WHERE id = 42","severity":"blocking","status":"pending","created":true}
{"id":"esc-20260713-001","timestamp":"2026-07-13T12:02:35Z","agent":"human","action":"DELETE FROM users WHERE id = 42","status":"approved","comment":"Go ahead","resolved":true}
{"id":"esc-20260713-002","timestamp":"2026-07-13T14:00:00Z","agent":"agent-2","action":"DROP TABLE payments","severity":"blocking","status":"timed_out","timeout":true,"default":"deny"}
```

Each entry MUST include at minimum:
- `id` — escalation ID
- `timestamp` — when this event occurred
- `status` — the new status
- One of: `created: true`, `resolved: true`, `timeout: true`

---

## §7 — CLI Reference

The `bin/escalate.sh` script provides the standard interface:

| Command | Description |
|---------|-------------|
| `escalate.sh --action "..." --reason "..." [--context "..."] [--impact "..."] [--severity blocking|advisory]` | Create new escalation |
| `escalate.sh --pending` | List all pending escalations |
| `escalate.sh --approve <id>` | Approve a pending escalation |
| `escalate.sh --deny <id> [comment]` | Deny a pending escalation |
| `escalate.sh --status <id>` | Show status of a specific escalation |
| `escalate.sh --log` | Show the full escalation log |

See `escalate.sh --help` for full usage.

---

## §8 — Integration with GATE.md

GATE.md Gate 1 (Domain Check) is the natural integration point:

- Before executing any operation that matches §2 trigger criteria, the agent MUST call `bin/escalate.sh` to create an escalation
- Gate 1 checks: "Does this action require human escalation?" If yes → escalate before proceeding
- Future: integrate with Slack webhook and Telegram bot for push notifications when escalations are created

See `docs/track/human-escalation-integration.md` for detailed integration guidance.

---

## §9 — Directory Layout

```
~/.1ai/escalations/
├── esc-20260713-001.json           # Escalation request (pending)
├── esc-20260713-001.response.json  # Human response (approved/denied)
├── esc-20260713-002.json           # Another escalation
├── esc-20260713-003.json           # Another escalation
└── LOG.json                        # Append-only escalation log
```
