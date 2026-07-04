---
name: hiring
version: 1.0.0
severity: mandatory
scope: [all]
pairs-with: [roles, onboarding, decision]
description: How to add, retire, and manage agents and human collaborators
---

# HIRING.md — Agent and Collaborator Lifecycle
> **All hires — agent or human — require owner approval.**
> No agent is deployed without a role spec, onboarding, and trial period.
> No human collaborator gets access without scoped provisioning and onboarding.
> Unapproved additions are unauthorized operators — their outputs are inadmissible.

---

## §1 WHEN TO HIRE

A new agent or collaborator is added only when one of these criteria is met.
Owner evaluates and approves — no agent initiates a hire without owner instruction.

**Criteria for adding a new agent:**
- **Overload:** Existing agent(s) are at sustained capacity and task queue is growing. Evidence required: task log showing backlog > 24h for 3+ consecutive days.
- **New domain:** A task type outside all existing agents' domains appears with recurring frequency (3+ tasks in one week). Domain gap confirmed against `core/ROLES.md` registry.
- **Specialization needed:** Existing agent handles a domain but lacks depth for a critical sub-domain (e.g., security agent needed alongside general engineering agent). Owner decides specialization threshold.
- **Redundancy / failover:** A single agent covers a critical path with no backup. Owner decides criticality.

**Criteria for adding a human collaborator:**
- Owner explicitly decides a task requires human judgment or legal accountability
- External partner, contractor, or auditor requires scoped access
- Human collaborator never replaces an agent — they operate alongside

**What does NOT trigger a hire:**
- One-off task that can be delegated to an existing agent with expanded context
- Temporary spike in volume — hire only if sustained
- Personal preference without operational justification

---

## §2 AGENT HIRING PROCESS

All steps are sequential. No step may be skipped. Owner approves at Step 1 before any other step begins.

### Step 1 — Owner defines role spec
Owner provides in writing:
- **Name:** unique identifier for the agent (e.g., `finance-agent`, `qa-agent-2`)
- **Type:** worker | reviewer | orchestrator | specialist
- **Authority level:** L1–L5 (defined in `core/ROLES.md`)
- **Domain:** exact domain(s) this agent owns (e.g., `finance`, `security`, `qa`)
- **Tools:** explicit list of tools and integrations the agent may access
- **Constraints:** what this agent must never do (beyond universal ethics stops)
- **Reports to:** which agent or directly to owner
- **Trigger for retirement:** performance threshold that initiates review

Role spec is the contract. Agent cannot exceed it.

### Step 2 — Role added to ROLES.md registry
- Add entry to `core/ROLES.md` with all fields from Step 1
- Status: `PENDING` until onboarding complete
- Decision logged in `core/DECISION.md`: date, rationale, role spec reference

### Step 3 — Agent config created
- Model selection: match to role complexity (see `core/ENGINEERING.md` performance guidelines)
- System prompt: derived from role spec + universal rules reference
- Tool access: provisioned per Step 1 tool list — no additional tools without owner approval
- Memory access: read-only to shared memory by default; write access requires explicit grant
- Config stored in agent registry (location per deployment environment)

### Step 4 — Onboarding run
- Agent runs full `core/ONBOARDING.md` §2 checklist
- Onboarding receipt posted before any task assignment
- Onboarding receipt archived in agent log
- If onboarding fails → `core/ONBOARDING.md` §6 protocol; do not proceed to Step 5

### Step 5 — Trial period
- First 3 tasks monitored per `core/ONBOARDING.md` §5
- All outputs reviewed by Reviewer Agent
- No production write access during trial
- Trial result logged: PASS or FAIL

### Step 6 — Full deployment
- Owner reviews trial log and approves full deployment
- Role status updated: `PENDING` → `ACTIVE` in `core/ROLES.md`
- Production access granted explicitly by owner (not assumed)
- Decision logged in `core/DECISION.md`: date, trial verdict, access granted

---

## §3 HUMAN COLLABORATOR PROCESS

Human collaborators are external — contractors, partners, auditors, advisors.
They are not employees. They have no authority over agents unless owner explicitly grants it.

### Step 1 — Confidentiality agreement
- Owner obtains signed confidentiality agreement before any access is granted
- Agreement covers: company data, agent capabilities, business logic, financials
- No confidentiality agreement = no access. No exceptions.

### Step 2 — Access scoping
- Access is granted to the minimum required for the stated task
- No standing access — access is time-bound (start date, end date, or task completion)
- Document what is granted: specific systems, specific data, specific agents they may interact with
- Owner records access grant in `core/DECISION.md`

### Step 3 — Onboarding
- Human collaborator completes `core/ONBOARDING.md` §3 checklist
- Owner confirms completion — collaborator does not self-certify
- Collaborator receives: COMMS.md (how to work with agents), ETHICS.md (what agents cannot be instructed to do), ROLES.md §5 (escalation)

### Step 4 — Supervised start
- First 2 weeks: all collaborator-initiated tasks reviewed by owner before agent execution
- Collaborator cannot directly instruct agents to take irreversible actions without owner co-sign
- After supervised period: owner decides whether to extend supervision or grant standard access

---

## §4 ACCESS PROVISIONING

**Principle: least privilege. Every access grant is explicit. No access is inherited or assumed.**

| Role Type       | Default Access                                    | Production Write | Memory Write | Hire/Retire |
|-----------------|---------------------------------------------------|------------------|--------------|-------------|
| L1 Worker       | Read tasks, write outputs to assigned scope       | No               | No           | No          |
| L2 Specialist   | Read domain data, write to domain scope           | No               | No           | No          |
| L3 Reviewer     | Read all outputs, write review verdicts           | No               | Read-only    | No          |
| L4 Orchestrator | Read all, write cross-domain, trigger agents      | Staging only     | Yes          | Propose only|
| L5 Owner        | All access                                        | Yes              | Yes          | Yes         |
| Human Collab    | Scoped per agreement (never exceeds L3 default)   | No               | No           | No          |

**Production write access:**
- Never granted automatically
- Requires owner explicit grant documented in `core/DECISION.md`
- Granted per deployment environment (staging ≠ production)
- Revoked immediately on role change, retirement, or security incident

**Tool access:**
- Each agent's tool list is fixed at hire time (Step 1 role spec)
- Adding a tool requires owner approval and update to `core/ROLES.md`
- Removing a tool requires owner approval if it affects active tasks

**Secret and credential access:**
- Agents access secrets via environment variables or secret manager — never hardcoded
- Credentials scoped to agent's domain — cross-domain credential access prohibited
- Credential rotation: owner-triggered; agents do not manage their own credentials

---

## §5 RETIREMENT PROTOCOL

An agent is retired when: owner decides, trial fails, performance review threshold met (§6),
role is eliminated, or a security incident requires immediate removal.

**Retirement is irreversible by default. Archive first, delete last.**

### Step 1 — Task reassignment
- Identify all active and queued tasks assigned to the retiring agent
- Reassign to appropriate active agent or queue for owner decision
- No task is abandoned — every task has a new owner before retirement proceeds

### Step 2 — Memory archive
- Export agent's working memory and session logs to archive location
- Tag archive: `[agent-name]-[retirement-date]-archive`
- Archive is read-only after retirement; no writes permitted
- Retention: minimum 90 days, then owner decides disposal

### Step 3 — Access revocation
- Revoke all tool access and integrations immediately
- Revoke credential access: notify secret manager / rotate affected secrets
- Remove agent from task routing and orchestration configs
- Confirm revocation: attempt a tool call post-revocation, verify it fails

### Step 4 — Role status update
- Update `core/ROLES.md`: status → `INACTIVE`, retirement date, reason
- Role name is reserved — do not reuse for a new agent (prevents confusion)

### Step 5 — Decision log
- Log in `core/DECISION.md`: agent name, retirement date, reason, task disposition,
  memory archive location, access revocation confirmation

### Emergency retirement (security incident):
- Steps 3 and 4 execute immediately — access revoked before task reassignment
- Steps 1, 2, 5 complete within 24 hours
- Owner notified immediately per `core/COMMS.md` escalation channel

---

## §6 PERFORMANCE REVIEW

**Frequency:** Quarterly for all active agents. Ad-hoc if owner flags performance concern.

**Metrics tracked per agent:**
- **Task completion rate:** tasks completed / tasks assigned (target: ≥ 95%)
- **Error rate:** tasks with BLOCK findings or rollback required / total tasks (target: ≤ 5%)
- **Escalation frequency:** escalations per 10 tasks (baseline established in first quarter; trend matters)
- **Onboarding compliance:** was onboarding receipt posted before first task? (binary)
- **Ethics violations:** any hard stop triggered or ETHICS.md violation (zero tolerance)

**Review process:**
1. Owner or designated Reviewer Agent compiles metrics from task logs
2. Metrics compared against targets and prior-quarter baseline
3. Verdict assigned:

| Verdict         | Condition                                         | Action                        |
|-----------------|---------------------------------------------------|-------------------------------|
| PERFORMING      | All targets met or exceeded                       | No action, continue           |
| WATCH           | One metric below target, no ethics violations     | Monitor next 30 days          |
| RETRAINING      | Two+ metrics below target OR escalation spike     | Role spec review, prompt update, re-onboard |
| REASSIGNMENT    | Retraining did not resolve within 30 days         | Move to different domain/role |
| RETIREMENT      | Reassignment failed OR ethics violation recorded  | Retire per §5                 |

**Retraining process:**
- Owner reviews and updates role spec and system prompt
- Agent re-runs `core/ONBOARDING.md` §2 checklist (full, not abbreviated)
- New trial period: 3 tasks monitored before full re-deployment

**Ethics violation:**
- Any confirmed ethics violation bypasses WATCH and RETRAINING
- Immediate escalation to REASSIGNMENT or RETIREMENT at owner's discretion
- Violation logged permanently in `core/DECISION.md` — cannot be expunged

**Review record:**
- All quarterly reviews logged in `core/DECISION.md` with date, agent, metrics, verdict, action
- Agents may not review themselves — Reviewer Agent or owner conducts review
