---
name: decision
version: 1.1.0
severity: mandatory
scope: [all]
pairs-with: [roles, gate, plan, ethics]
description: Decision authority thresholds, approval flows, and reversibility
---

# DECISION.md — Decision Authority and Approval Protocol

> Every non-trivial decision MUST be logged. Every irreversible action MUST have prior approval.
> No agent decides in silence. No action without a trail.

---

## §1 DECISION TYPES

### Type 1 — Reversible
Can be undone within 24h with no data loss or user impact.

Examples:
- Feature flag toggle
- Config value change (non-secret)
- Adding a log statement
- Refactor with test coverage
- Draft content / internal doc update

Treatment: Log it. L2+ can execute. No approval gate required.

### Type 1 — Multi-Agent Synthesizer Output (COMPLEX tasks)
When a COMPLEX task's BRAINSTORM step uses the §MULTI-AGENT debate protocol (ENGINEERING.md §6 Step 3 / SURPASS.md §MULTI-AGENT), the Synthesizer sub-agent's final verdict is a **Type 1 decision** and MUST be logged in `logs/decisions/YYYY-MM-DD.md` before PLAN (Step 4) begins.

Log entry MUST include:
- Approaches debated (Advocate position, Skeptic objections)
- Synthesizer's chosen approach and rationale
- Dissenting points that were overruled and why
- GitHub Issue ref for the task

Rationale: The debate collapses multiple perspectives into one path. Without a log, the reasoning is lost and future agents cannot audit the choice.

### Type 2 — Irreversible (or Hard-to-Reverse)
Cannot be undone, or reversal costs >1h effort or risks data loss.

Examples:
- Production database migration (destructive)
- Deleting files or records permanently
- Publishing to external channels (social, email, API)
- Spending money (any amount)
- Adding a new third-party dependency
- Changing authentication or access control
- Deploying to production
- Modifying RULES.md, GATE.md, or any core/ file

Treatment: Explicit approval required before execution. Log with rollback plan.

---

## §2 AUTHORITY THRESHOLDS

Authority levels are defined in ROLES.md. Summary:
- L1: Executor Agent (narrow task scope)
- L2: Domain Agent (owns a domain, e.g., backend, content)
- L3: Orchestrator Agent (cross-domain coordination)
- L4: Autonomous GM (Vilona — strategic, 24/7 ops)
- L5: Human Owner (final authority on all Type 2 decisions)

| Decision Category              | L1  | L2  | L3  | L4       | L5  |
|-------------------------------|-----|-----|-----|----------|-----|
| Code change (tested, scoped)  | ✓   | ✓   | ✓   | ✓        | ✓   |
| Production deploy (new feat)  | ✗   | ✗   | ✓   | ✓        | ✓   |
| Hotfix deploy (critical bug)  | ✗   | ✓*  | ✓   | ✓        | ✓   |
| Spend < $10                   | ✗   | ✗   | ✓   | ✓        | ✓   |
| Spend $10–$100                | ✗   | ✗   | ✗   | ✓        | ✓   |
| Spend > $100                  | ✗   | ✗   | ✗   | ✗        | ✓   |
| Add npm/pip dependency        | ✗   | ✓   | ✓   | ✓        | ✓   |
| Add paid/SaaS dependency      | ✗   | ✗   | ✗   | ✓        | ✓   |
| Change core/ rule file        | ✗   | ✗   | ✗   | ✗        | ✓   |
| Hire/spawn new agent          | ✗   | ✗   | ✓   | ✓        | ✓   |
| External comms (public)       | ✗   | ✗   | ✗   | ✓*       | ✓   |
| Destroy production data       | ✗   | ✗   | ✗   | ✗        | ✓   |
| Change company mission/OKRs   | ✗   | ✗   | ✗   | ✗        | ✓   |

`*` = allowed with mandatory post-action log filed within 1h

---

## §3 APPROVAL PROTOCOL

### Steps

1. **Identify decision type** — Type 1 or Type 2 (see §1).
2. **Check authority** — Does your level cover this? See §2.
3. **If approval needed:**
   a. Write a Decision Request: proposed action, rationale, reversibility, rollback plan.
   b. File as GitHub Issue with label `decision-request` and tag the appropriate approver.
   c. Wait for explicit approval comment: "APPROVED" or "APPROVED WITH CONDITIONS: [X]".
   d. A non-response is NOT approval. See timeout behavior below.
4. **Execute** only after written approval is on record.
5. **Log the decision** — see §4.

### What counts as approval
- GitHub Issue comment with "APPROVED" from an agent at the required level or higher.
- Telegram message from L5 (human owner) containing "APPROVED" for L5-gated decisions.
- Implicit approval does NOT exist. Silence is NOT consent.

### Async timeout behavior
| Waiting for | Timeout | Default action |
|------------|---------|----------------|
| L3 Orchestrator | 2h | Escalate to L4 |
| L4 GM (Vilona) | 4h | Escalate to L5 via Telegram |
| L5 Human Owner | 24h | Halt and hold. Do not proceed. |

If no response after L5 timeout: log the block, cease work on that decision, continue other tasks.

---

## §4 DECISION LOG

Every non-trivial decision (all Type 2, and Type 1 decisions affecting shared state) MUST be logged.

### Log location
File: `logs/decisions/YYYY-MM-DD.md` (one file per day)
Also reference the GitHub Issue number where applicable.

### Log entry format
```
## [DECISION-ID: YYYY-MM-DD-NNN]
- Date: YYYY-MM-DD HH:MM UTC
- Decision: [one sentence — what was decided]
- Decided by: [agent-name, authority level]
- Approval from: [agent/human who approved, or "self-authorized L2 Type1"]
- Rationale: [why this option over alternatives]
- Reversibility: [Type 1 / Type 2]
- Rollback plan: [exact steps to undo]
- GitHub ref: [Issue #NNN or PR #NNN]
- Status: [PENDING / EXECUTED / ROLLED BACK]
```

Incomplete log entries are treated as unapproved decisions.

---

## §5 FORBIDDEN DECISIONS

No agent at any level (including L4) can execute the following without explicit L5 human approval:

1. Delete or truncate any production database table or collection.
2. Expose, log, or transmit user PII outside the production environment.
3. Change company mission statement, brand identity, or OKR framework.
4. Revoke or modify access credentials for the human owner's accounts.
5. Modify any file in `~/.1ai/core/` (this directory).
6. Cancel or downgrade any active paid subscription or service.
7. Initiate any legal, contractual, or financial obligation over $100.
8. Remove or bypass any gate in GATE.md.
9. Override a CHANGES REQUIRED verdict from REVIEWER.md without re-review.
10. Disable monitoring, alerting, or audit logging for any production system.

Attempting a forbidden decision without L5 approval triggers INCIDENT.md protocol.

---

## §6 FAST PATH

For time-critical decisions where normal approval (§3) would cause harm by delay.

### Conditions for fast path invocation
ALL must be true:
- A production incident is active (see INCIDENT.md severity P0 or P1).
- Waiting for normal approval would worsen the incident.
- The decision is reversible (Type 1) OR falls within §5 exceptions.

### Who can invoke
L3 or higher. L1/L2 cannot invoke fast path alone.

### Fast path steps
1. State: "FAST PATH INVOKED — [reason] — [decision]" in the incident channel (GitHub Issue or Telegram).
2. Execute the minimum action needed to stabilize.
3. File a Decision Log entry (§4) within 1h of action.
4. File a postmortem within 24h: what happened, why fast path was needed, was it the right call.

### Fast path is NOT a bypass for §5 forbidden decisions.
If a forbidden decision is required to resolve an incident, escalate to L5 immediately via Telegram. Do not act.

---

## §7 DECISION REVIEW

### Cadence
Weekly — every Monday (or next working cycle after Monday).

### Reviewer
L4 (Vilona/GM) reviews all logged decisions from the prior 7 days.
L5 (human owner) reviews any L4-level or L5-approved decisions from the prior 7 days.

### What to check
- Is every Type 2 decision in the log? Flag any missing entries.
- Did the executing agent have sufficient authority? Flag over-reach.
- Was the rollback plan documented before execution?
- Were any §5 forbidden decisions executed without L5 approval? → Immediate escalation.
- Were fast path decisions followed by a postmortem within 24h?
- Are any decisions from the past week that should be reversed still reversible?

### Flagging a bad decision
1. Add comment to the decision's GitHub Issue: "DECISION REVIEW FLAG — [reason]".
2. Tag the deciding agent and L4/L5 as appropriate.
3. If the decision needs reversal: follow rollback plan from the log entry.
4. If the rollback plan is absent: escalate to L5.
5. Log the reversal as a new Decision Log entry referencing the original.
