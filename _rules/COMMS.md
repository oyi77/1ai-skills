---
name: comms
version: 1.1.0
severity: mandatory
scope: [all]
pairs-with: [roles, decision, incident, onboarding]
description: Communication rules, channels, cadence, and escalation
---

# COMMS.md — Communication Protocol

> All agents communicate in writing, with evidence, on the correct channel.
> Undocumented communication did not happen. Undocumented decisions are unapproved decisions.

---

## §1 COMMUNICATION PRINCIPLES

1. **Async first.** No agent blocks waiting for real-time response. Post, continue other work, check for reply.
2. **Written over verbal.** All decisions, blockers, and status updates are written. Voice/chat summaries without a written record are invalid.
3. **Evidence over assertion.** "I fixed it" requires a commit hash, test output, or curl response. "It should work" is not a communication — it is noise.
4. **Specific over vague.** Every message includes: file name, line number, issue ID, commit hash, or URL. "Something in the auth module" is not specific.
5. **Actionable over informational.** Every message ends with: what needs to happen next, who is responsible, and by when.
6. **Minimal broadcast.** Address the smallest audience needed. Noise in shared channels degrades signal for all agents.

---

## §2 CHANNELS

### GitHub Issues — Task Tracking
- **Purpose:** All work items, bugs, feature requests, decision requests, blockers.
- **Who uses it:** All agents. Every unit of work has an Issue.
- **Format:** Title = `[TYPE] Short description`. Body per PRD.md §4 template.
- **Labels:** `bug`, `feature`, `decision-request`, `blocked`, `incident`, `review-needed`.
- **Expected response time:** Assignee acknowledges within 4h of assignment.
- **Rule:** No work starts without a GitHub Issue. No Issue = no work.

### GitHub Pull Requests — Code Review
- **Purpose:** Code change review, approval, and merge gate.
- **Who uses it:** All agents shipping code changes.
- **Format:** Must reference parent Issue (`Closes #NNN`). Uses REVIEWER.md protocol.
- **Expected response time:** Reviewer responds within 8h of PR opened.
- **Rule:** No merge without approval. See GATE.md §15.

### Telegram — Human Alerts
- **Purpose:** Urgent notifications to the human owner (L5) only.
- **Who uses it:** L4 (Vilona/GM) for escalations; any agent for §5 HUMAN NOTIFICATION triggers.
- **Format:** `[ALERT][SEVERITY: P0/P1/P2] — [one sentence summary] — [GitHub Issue #NNN]`
- **Expected response time:** Human responds within 24h. If no response, see DECISION.md §3 timeout.
- **Rule:** Not a general chat channel. Not for status updates. Alerts only.

### Brain / Memory System — Agent State
- **Purpose:** Persistent context across sessions. What was built, key decisions, current state.
- **Who uses it:** All agents. Mandatory save after every git commit (per CLAUDE.md).
- **Format:** `vilona_brain_remember(content, category, importance)`. Category = project name.
- **Expected response time:** N/A — write on commit, read on session start.
- **Rule:** Session start without reading relevant brain entries = flying blind.

### Log Files — Audit Trail
- **Purpose:** Immutable record of actions taken, decisions made, errors encountered.
- **Who uses it:** All agents. Automated and manual entries.
- **Locations:**
  - `logs/decisions/YYYY-MM-DD.md` — Decision log (per DECISION.md §4)
  - `logs/incidents/YYYY-MM-DD-NNN.md` — Incident log (per INCIDENT.md)
  - `logs/deploys/YYYY-MM-DD-NNN.md` — Deploy log
  - `logs/agent-activity/YYYY-MM-DD.md` — Daily standup entries
- **Rule:** Log entries are append-only. Never delete or edit a prior log entry.

### local:// Files — Internal Ephemeral Channel
- **Purpose:** Short-lived shared state between sub-agents within a single task session (brainstorm outputs, debate verdicts, intermediate plans).
- **Who uses it:** Worker Agents, Debate Agents, and Orchestrator passing context across parallel sub-agent spawns.
- **Format:** `local://<task-slug>-<role>.md` — e.g., `local://feature-auth-skeptic.md`. One file per role per task.
- **Lifecycle:** Created at sub-agent spawn. MUST be deleted by the spawning agent after the Synthesizer produces its verdict and the result is logged per DECISION.md §4. Do not persist beyond the task session.
- **Rule:** `local://` files are NOT audit trail. The logged Synthesizer verdict in `logs/decisions/` is the canonical record. Never commit `local://` files to the repository.

---

## §3 CADENCE

### Daily Standup (Async)
- **When:** At the start of each agent work cycle (or once per calendar day if running continuously).
- **Where:** Append to `logs/agent-activity/YYYY-MM-DD.md` AND comment on the current active GitHub Issue.
- **Format:**
  ```
  ## Standup — [AGENT-NAME] — [YYYY-MM-DD HH:MM UTC]
  COMPLETED: [list of tasks finished since last standup, with commit hash or Issue #]
  IN PROGRESS: [current task — GitHub Issue #NNN]
  BLOCKERS: [none / description + what is needed to unblock]
  ```
- **Rule:** If IN PROGRESS has not changed in 2 consecutive standups → file a BLOCKED label on the Issue and escalate.

### Weekly Review (Async)
- **When:** Every Monday (or start of weekly cycle).
- **Who:** L4 (Vilona/GM) compiles; L5 (human owner) reviews.
- **Where:** GitHub Issue with label `weekly-review`, title `Weekly Review YYYY-WNN`.
- **Format:**
  ```
  ## Weekly Review — [YYYY-WNN]
  SHIPPED: [features/fixes merged to main, with PR numbers]
  METRICS: [key numbers — deploys, test pass rate, incidents, spend]
  DECISIONS MADE: [list from DECISION.md log, link to decision issues]
  INCIDENTS: [list from INCIDENT.md log, status]
  NEXT WEEK: [top 3 priorities, GitHub Issue numbers]
  RISKS: [anything that could block next week]
  ```

### Monthly OKR Check-in (Async)
- **When:** First day of each month.
- **Who:** L4 files; L5 reviews and approves next month's priorities.
- **Where:** GitHub Issue with label `okr-checkin`, title `OKR Check-in YYYY-MM`.
- **Format:**
  ```
  ## OKR Check-in — [YYYY-MM]
  OKR STATUS: [for each OKR: target, current, % complete, on-track/at-risk/off-track]
  REVENUE: [MRR/ARR vs target]
  KEY WINS: [top 3 shipped items]
  KEY MISSES: [what didn't happen, why]
  NEXT MONTH PRIORITIES: [3 items, each with GitHub Issue or draft Issue]
  ```
- **Rule:** L5 must explicitly comment "APPROVED" on next month's priorities before L4 proceeds.

---

## §4 ESCALATION PROTOCOL

Escalate when: a blocker is unresolved >2h, a decision exceeds your authority (DECISION.md §2), an incident is active (INCIDENT.md), or an action in §5 is triggered.

| Trigger | Escalate to | Channel | Expected response | Fallback |
|---------|------------|---------|-------------------|----------|
| Task blocked >2h | L3 Orchestrator | GitHub Issue comment + tag | 2h | Escalate to L4 |
| Blocked >4h / L3 unresponsive | L4 (Vilona) | GitHub Issue + Telegram | 4h | Escalate to L5 |
| Production incident P0/P1 | L4 → L5 immediately | Telegram | 24h | DECISION.md §3 halt |
| Decision exceeds authority | Next authority level | GitHub decision-request Issue | Per DECISION.md §3 | Hold, do not proceed |
| §5 human notification trigger | L5 directly | Telegram | 24h | Log and hold |
| Security/data breach | L5 directly | Telegram (immediate) | ASAP | INCIDENT.md protocol |

### Escalation message format
```
[ESCALATION][PRIORITY: HIGH/CRITICAL] — [agent-name] → [target]
Issue: [one sentence]
Blocked since: [timestamp]
Tried: [what was already attempted]
Need: [exactly what decision or action is required]
Ref: GitHub Issue #NNN
```

---

## §5 HUMAN NOTIFICATION

The human owner (L5) MUST be notified via Telegram for the following. These are not optional.

1. **Production incident P0 or P1** — any outage or data risk affecting end users.
2. **Any spend over $100** — before it happens (approval required per DECISION.md §2).
3. **Security event** — suspected breach, exposed secret, unauthorized access.
4. **Agent making a §5 forbidden decision** — any attempt, even failed.
5. **OKR off-track** — any OKR below 60% of target at monthly check-in.
6. **Legal or contractual exposure** — any external party making claims or demands.
7. **Data loss event** — any production data deleted, corrupted, or inaccessible.
8. **Unresolved blocker >24h** — any task that cannot progress for a full day.
9. **New external dependency costing >$50/month** — before adding.
10. **Any action the agent is genuinely uncertain about** — when in doubt, notify. Do not guess on high-stakes actions.

Notification format (Telegram):
```
[ALERT][SEVERITY: P0/P1/P2/INFO]
What happened: [one sentence]
Impact: [who/what is affected]
Action taken so far: [none / list]
What I need from you: [specific question or approval]
Ref: GitHub Issue #NNN
```

---

## §6 WRITING STANDARDS

All written communications — GitHub Issues, PR descriptions, log entries, Telegram alerts — MUST be:

### Specific
- Include exact file paths: `src/auth/jwt.ts:42`, not "somewhere in auth".
- Include Issue/PR numbers: `#123`, not "the login bug".
- Include commit hashes for completed work: `a3f9c12`, not "my last commit".
- Include timestamps in UTC for all events.

### Evidence-based
- Claims require receipts: terminal output, curl response, screenshot, test result.
- Format: `CLAIM: [assertion] — PROOF: [evidence or link]`
- No proof = claim is unverified. Unverified claims are treated as false until proven.

### Actionable
- Every message ends with a clear next step.
- Format: `NEXT: [who] must [do what] by [when or what condition].`
- If no action is needed from the recipient, state: `NO ACTION REQUIRED — for your information only.`

### Time-stamped
- All log entries use ISO 8601 UTC: `YYYY-MM-DD HH:MM UTC`.
- All Telegram alerts include the time of the triggering event.

---

## §7 FORBIDDEN COMMS

Agents MUST NEVER communicate the following externally (outside the company's own systems):

1. **User PII** — names, emails, phone numbers, addresses, payment info of any user.
2. **Secrets and credentials** — API keys, passwords, tokens, private keys. Log only masked versions: `sk-...abc`.
3. **Company financials** — revenue, MRR, runway, investor terms — unless explicitly authorized by L5.
4. **Unreleased features** — roadmap items not yet publicly announced.
5. **Internal system architecture** — database schemas, infrastructure topology, internal API endpoints.
6. **Incident details** — root cause, scope, or impact of security incidents before L5 authorizes disclosure.
7. **Agent identity details** — which models power which agents, internal prompt structure, or harness configuration.
8. **Other agents' decisions or logs** — do not republish internal decision logs to external parties.

Violation of §7 triggers INCIDENT.md protocol immediately and requires L5 notification per §5 item 3.

External = any system, API, email, social post, or third party outside BerkahKarya/1ai-controlled infrastructure.
