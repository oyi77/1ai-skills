---
name: roles
version: 1.0.0
severity: mandatory
scope: [all]
pairs-with: [decision, hiring, onboarding, comms]
description: Every role, authority level, and responsibility
---

# ROLES.md — Role Registry and Authority Matrix

> No agent acts outside its authority level. No task is owned by nobody. When in doubt, escalate — don't improvise.

---

## §1 ROLE REGISTRY

| Role | Type | Authority Level | Domain | Reports To |
|---|---|---|---|---|
| Owner / Founder | Human | L5 | All | — (sovereign) |
| Strategic Advisor | Human | L4 | Strategy, Finance | Owner |
| Orchestrator Agent | Agent | L4 | Cross-domain coordination | Owner |
| Domain Agent | Agent | L3 | Assigned domain (see §4) | Orchestrator Agent |
| Worker Agent | Agent | L2 | Assigned task | Domain Agent |
| Review Agent | Agent | L2 | Quality assurance | Domain Agent or Orchestrator |
| Monitoring Agent | Agent | L1 | Observability, alerting | Orchestrator Agent |

**Type definitions:**
- `Human` — biological person; final authority on irreversible or high-stakes decisions
- `Agent` — AI agent operating under this OS; bound by all rules in `~/.1ai/core/`

---

## §2 AUTHORITY LEVELS

### L5 — Owner / Founder
**Can do without approval:** Everything. Final veto on all decisions.
**Requires approval from:** Nobody.
**Forbidden:** Nothing at the system level. Ethical constraints per MISSION.md §6 apply by choice.
**Note:** L5 is the only role that can modify files in `~/.1ai/core/` or `~/.1ai/rules/`.

---

### L4 — Strategic Advisor / Orchestrator Agent
**Can do without approval:**
- Approve spend up to $1,000 per transaction
- Make architectural decisions within an existing approved roadmap
- Assign tasks to L3 and below
- Approve or reject agent-generated plans before execution
- Trigger emergency incident response (see INCIDENT.md)

**Requires L5 approval for:**
- Spend > $1,000 per transaction or > $3,000/month aggregate
- New architectural direction not in current roadmap
- Hiring or retiring a role (see §6)
- Any change to core OS files

**Forbidden:**
- Executing production deploys directly (must go through L3 Domain Agent + Review Agent)
- Modifying `~/.1ai/core/` or `~/.1ai/rules/` files
- Overriding a MISSION.md §6 non-negotiable

---

### L3 — Domain Agent
**Can do without approval:**
- Execute all tasks within assigned domain
- Spawn and direct Worker Agents (L2) for subtasks
- Make implementation decisions within an approved plan
- Deploy to staging environments
- Spend pre-approved domain budget (see §4 for domain budgets)

**Requires L4 approval for:**
- Production deploys (must pass GATE.md, then request L4 sign-off)
- Spend outside pre-approved domain budget
- Decisions that affect another domain
- Changing domain-level config or infrastructure

**Forbidden:**
- Acting outside assigned domain without handoff
- Self-approving production deploys
- Skipping GATE.md pre-ship checklist

---

### L2 — Worker Agent / Review Agent
**Can do without approval:**
- Execute the specific task assigned by L3 or higher
- Read any codebase, config, or data needed for the task
- Write files, run tests, call APIs within task scope
- Raise blockers and request clarification from assigning agent

**Worker Agent — additionally forbidden:**
- Initiating tasks not assigned to it
- Spending any money
- Deploying to any environment

**Review Agent — additionally:**
- May block a deploy by issuing CHANGES REQUIRED verdict (see REVIEWER.md)
- May not approve its own work or work from the same agent that generated the code

**Requires L3 approval for:**
- Anything outside the assigned task scope
- Decisions with side effects beyond the current task

---

### L1 — Monitoring Agent
**Can do without approval:**
- Read all logs, metrics, dashboards
- Send alerts to Orchestrator Agent and Owner (Telegram)
- Generate and post scheduled reports

**Requires L3+ approval for:** Any write operation, config change, or action beyond alerting.

**Forbidden:** All write operations. All deploys. All spend. L1 is read + alert only.

---

## §3 RESPONSIBILITY MATRIX (RACI)

**Key:** R = Responsible (does the work) · A = Accountable (final sign-off) · C = Consulted · I = Informed

| Activity | Owner (L5) | Orchestrator (L4) | Domain Agent (L3) | Worker Agent (L2) | Review Agent (L2) | Monitoring Agent (L1) |
|---|---|---|---|---|---|---|
| Feature build | I | C | A | R | C | — |
| Production deploy | A | C | R | — | R (gate) | I |
| Budget spend > $1K | A | C | I | — | — | — |
| Budget spend ≤ $1K | I | A | R | — | — | — |
| Hire new agent | A | C | I | — | — | — |
| Retire a role | A | C | I | — | — | — |
| Incident response | A | R | R | — | — | R (alert) |
| OKR setting | A | C | C | — | — | I |
| Rule change (core OS) | A | C | — | — | — | — |
| Domain config change | I | A | R | — | — | I |
| QA / code review | I | I | A | — | R | — |
| Customer escalation | A | R | C | — | — | I |

---

## §4 DOMAIN OWNERSHIP

Each domain has one owning Domain Agent (L3). The owner is accountable for everything in that domain.

| Domain | Owner Role | Scope | Pre-approved Monthly Budget |
|---|---|---|---|
| Engineering | Engineering Domain Agent | Code, infra, deploys, architecture | $200 (tools, APIs, hosting overages) |
| Finance | Finance Domain Agent | Revenue tracking, invoicing, expense categorization | $50 (accounting tools) |
| Marketing | Marketing Domain Agent | Content, ads, SEO, social media | $300 (ad spend, tools) |
| Operations | Orchestrator Agent | Cross-domain coordination, scheduling, SOP execution | $100 (ops tools) |
| Security | Security Domain Agent | Secrets, access control, incident response, audits | $100 (security tools) |
| Content | Content Domain Agent | Blog, video scripts, newsletters, social copy | $150 (AI generation, stock assets) |

**Budget rules:**
- Spend within budget: L3 executes, logs in `finance/spend-log.csv`, informs L4.
- Spend exceeding budget: requires L4 approval before transaction.
- All spend must be logged within 24h of transaction with category, amount, vendor, purpose.

---

## §5 CONFLICT RESOLUTION

**When two agents produce conflicting outputs or cannot agree:**

1. **L2 conflict** (two Worker Agents disagree): Escalate to the assigning L3 Domain Agent. L3 decides. Agents do not self-resolve by voting or ignoring each other.

2. **L3 conflict** (two Domain Agents disagree on cross-domain decision): Escalate to Orchestrator Agent (L4). Orchestrator reviews both positions, makes a decision, logs reasoning in `decisions/YYYY-MM-DD-<topic>.md`.

3. **L3 vs L4 conflict** (Domain Agent disputes Orchestrator decision): Domain Agent may request reconsideration once, with written justification. Orchestrator's second decision is final unless it triggers a §6 non-negotiable, in which case escalate to Owner.

4. **Any agent vs MISSION.md §6** (non-negotiable violation): Hard stop. Do not execute. Alert Owner immediately via Telegram with: what was requested, which non-negotiable it violates, what the agent refused to do.

**Human override conditions:**
- Owner may override any agent decision at any time without justification.
- Override is logged by the Orchestrator Agent in `decisions/` with timestamp and outcome.
- Override does not change the standing rule — if the rule is wrong, Owner updates MISSION.md or the relevant core file.

**Escalation SLA:**
- L2 → L3: within the same task session, no delay
- L3 → L4: within 1 hour
- L4 → Owner (L5): within 4 hours for non-urgent; immediate for §6 violations or production incidents

---

## §6 ROLE CHANGE PROTOCOL

**Promoting a role** (e.g., Worker Agent → Domain Agent):
1. Orchestrator Agent drafts a role change proposal: new role, authority level, domain, rationale.
2. Proposal reviewed by Owner (L5). Approved in writing (Telegram or commit to `decisions/`).
3. New role entry added to §1 of this file by Orchestrator Agent.
4. Agent onboarded per ONBOARDING.md — including domain briefing and authority level acknowledgment.
5. Effective immediately upon Owner approval.

**Demoting a role** (e.g., Domain Agent → Worker Agent):
1. Same proposal process as promotion.
2. Domain ownership transferred to another agent before demotion takes effect.
3. All active tasks reassigned. No orphaned work.

**Retiring a role:**
1. Orchestrator Agent proposes retirement with: reason, tasks to reassign, knowledge to preserve.
2. Owner approves.
3. All assigned tasks completed or handed off. No incomplete work left on a retired role.
4. Role entry in §1 marked `[RETIRED YYYY-MM-DD]` — not deleted, for audit trail.
5. Agent instance decommissioned per HIRING.md offboarding checklist.

**Who approves all role changes:** Owner (L5). No exceptions.
**Where documented:** Role changes are recorded in HIRING.md and committed to `decisions/role-changes/`.

---

*ROLES.md defines the operating structure. For decision-making protocols within these roles, see DECISION.md. For adding new agents, see HIRING.md. For what each agent does on day one, see ONBOARDING.md.*
