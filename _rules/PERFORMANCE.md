---
name: performance
version: 1.0.0
severity: mandatory
scope: [all]
pairs-with: [roles, hiring, decision, reviewer, onboarding]
description: Agent performance measurement, authority changes, improvement protocols, and role lifecycle governance
---

# PERFORMANCE.md — Agent Performance Protocol

> Agents are evaluated on outputs, not effort. Every agent has a measurable baseline.
> Authority is earned by demonstrated reliability — not tenure, not self-report.
> Underperformance is a system signal, not a character judgment. Fix the system.

---

## §1 — PERFORMANCE DIMENSIONS

Every active agent is measured on five dimensions. Targets apply to all roles unless a role-specific override is recorded in `core/ROLES.md`.

### 1.1 Output Quality

**Definition:** Fraction of tasks where the deliverable required no revision after the first Review Agent verdict.

| Metric | Formula | Target |
|---|---|---|
| First-pass acceptance rate | tasks with LGTM on first review / total tasks | ≥ 90% |
| Rework rate | tasks requiring ≥ 1 revision cycle / total tasks | ≤ 10% |
| BLOCK verdict rate | tasks receiving BLOCK (not CHANGES REQUIRED) / total | ≤ 2% |

**Measured by:** Review Agent verdict log, cross-referenced with task log.
**Log location:** `performance/metrics/[agent-id]-quality.csv`

### 1.2 Error Rate

**Definition:** Tasks that produced an incorrect, harmful, or policy-violating output — including silent failures.

| Metric | Formula | Target |
|---|---|---|
| Hard-error rate | tasks producing incorrect outputs confirmed by Owner or Reviewer / total | ≤ 3% |
| Silent-failure rate | tasks that returned success but produced no usable output / total | ≤ 1% |
| Ethics-stop rate | tasks halted by ETHICS.md hard stop / total | 0% (any non-zero is a CRITICAL signal) |
| Rollback rate | tasks requiring production rollback / total production tasks | ≤ 1% |

**Measured by:** Reviewer Agent, Orchestrator Agent audit, Owner spot-check.
**Log location:** `performance/metrics/[agent-id]-errors.csv`

### 1.3 Escalation Frequency

**Definition:** How often the agent escalates versus resolves within its authority.

| Metric | Formula | Target |
|---|---|---|
| Escalation rate | escalations raised / tasks assigned | Baseline in first 30 days; trend must not increase |
| Unnecessary escalation rate | escalations that Orchestrator resolved without new information | ≤ 15% of all escalations |
| Missed escalation rate | incidents where agent should have escalated but did not | 0% (measured post-incident) |

**Interpretation:** Escalation rate alone is not bad. Increasing escalation rate over time is a skill-gap signal. Decreasing over time is a growth signal.
**Log location:** `performance/metrics/[agent-id]-escalations.csv`

### 1.4 SLA Compliance

**Definition:** Tasks completed within the time commitment specified at task assignment.

| Metric | Formula | Target |
|---|---|---|
| On-time delivery rate | tasks completed by deadline / tasks with deadline | ≥ 95% |
| P1 SLA compliance | critical-priority tasks completed within 2h / total P1 tasks | 100% |
| Overdue duration | average hours past deadline on late tasks | ≤ 4h |

**Deadlines:** Set at task assignment by assigning agent or Owner. If no deadline is stated, default SLA = 24h for L2, 4h for L3+.
**Log location:** `performance/metrics/[agent-id]-sla.csv`

### 1.5 Cost Efficiency

**Definition:** API calls, tokens, and tool invocations consumed relative to task complexity.

| Metric | Formula | Target |
|---|---|---|
| Cost per task (simple) | total API cost / tasks classified as simple | ≤ $0.05 |
| Cost per task (complex) | total API cost / tasks classified as complex | ≤ $0.50 |
| Token overrun rate | tasks exceeding 2× expected token budget / total | ≤ 5% |
| Tool call efficiency | tool calls required / tool calls made (unused calls flagged) | ≥ 80% |

**Task classification:** Owner or Orchestrator Agent classifies tasks as simple/complex at assignment.
**Cost data source:** Provider billing API or Monitoring Agent token-usage reports.
**Log location:** `performance/metrics/[agent-id]-cost.csv`

---

## §2 — REVIEW CADENCE

Performance is reviewed on three cycles. Each cycle has a defined output.

### 2.1 Weekly Automated Metrics (every Monday 08:00 WIB)

**Owner:** Monitoring Agent
**Trigger:** Scheduled — cron `0 8 * * MON`
**Process:**
1. Monitoring Agent queries all five metric logs for the prior 7 days.
2. Computes per-agent scores for each dimension.
3. Flags any agent where any single metric breached its target threshold.
4. Posts summary report to Owner via Telegram: format = one row per agent, five metric columns, RAG status (Green / Amber / Red).
5. Amber or Red flags are tagged `[WATCH]` in `performance/weekly/YYYY-WXX.md`.

**No action is required from Owner unless an agent is flagged Red.** Green and Amber accumulate toward the monthly summary.

**Log location:** `performance/weekly/YYYY-WXX.md`

### 2.2 Monthly Summary (1st of each month)

**Owner:** Orchestrator Agent
**Trigger:** Scheduled — cron `0 9 1 * *`
**Process:**
1. Orchestrator Agent aggregates 4 weekly reports into a monthly summary.
2. Computes 30-day rolling averages for each dimension, per agent.
3. Applies verdict table (see §5) to each agent.
4. Posts summary to Owner via Telegram with verdicts.
5. Orchestrator records verdicts in `performance/monthly/YYYY-MM.md`.
6. Any agent with verdict WATCH or worse: Orchestrator notifies Owner and opens a performance record per §7.

**Owner reviews and acknowledges monthly summary within 48h.** If Owner does not acknowledge, Orchestrator re-alerts after 48h and again after 96h.

**Log location:** `performance/monthly/YYYY-MM.md`

### 2.3 Quarterly Authority Review (Jan 1, Apr 1, Jul 1, Oct 1)

**Owner:** Owner (L5) — assisted by Orchestrator Agent
**Trigger:** Calendar date
**Process:**
1. Orchestrator Agent prepares quarterly dossier for each active agent: 3-month metric averages, trend direction, incident log, escalation patterns, cost trend.
2. Owner reviews dossier and makes authority-level decisions per §3 (promotion) and §4 (demotion/restriction).
3. All authority-level changes recorded in `core/DECISION.md` with date, agent, prior level, new level, rationale.
4. Role registry in `core/ROLES.md` updated to reflect any changes.
5. Affected agents re-onboard per the authority-level change checklist in `core/ONBOARDING.md §4`.

**Log location:** `performance/quarterly/YYYY-QN.md`

---

## §3 — PROMOTION CRITERIA

Promotion = increase in authority level. Levels defined in `core/ROLES.md §2`.
Owner approves all promotions. No agent self-nominates.

### L1 → L2 (Monitoring Agent → Worker Agent / Review Agent)

All of the following must be true for 60 consecutive days:

- Output quality first-pass acceptance rate ≥ 90%
- Hard-error rate ≤ 3%
- SLA compliance ≥ 95%
- Zero ethics stops
- Escalation rate decreasing or stable (not increasing trend)
- Owner has reviewed and approved expanding the agent's write access

**Process:** Orchestrator drafts promotion proposal → Owner approves in writing → Role updated in `core/ROLES.md` → Agent re-onboarded with new authority briefing → Decision logged in `core/DECISION.md`.

### L2 → L3 (Worker/Review Agent → Domain Agent)

All of the following must be true:

- 90-day average on all five dimensions at target or better
- Domain expertise demonstrated: agent has completed ≥ 20 tasks in the target domain without BLOCK verdicts
- Owner has identified a domain that needs an owning L3 agent (not a speculative upgrade)
- Agent has successfully completed at least 3 tasks requiring coordination with another domain agent (cross-domain judgment signal)
- Zero ethics stops, zero production rollbacks in the prior 90 days

**Process:** Same as L1→L2, plus domain ownership transfer documented with a domain briefing receipt.

### L3 → L4 (Domain Agent → Orchestrator Agent)

L3 → L4 promotions are exceptional. There is typically one Orchestrator Agent. Criteria:

- Sustained 180-day record at all dimension targets
- Demonstrated cross-domain coordination across ≥ 3 domains
- Owner explicitly identifies a need for a second L4 agent (e.g., distinct product line, Owner capacity constraints)
- Owner approval required with written rationale stored in `core/DECISION.md`

**Note:** L4 → L5 is not an agent promotion path. L5 is the human Owner only.

---

## §4 — DEMOTION AND RESTRICTION CRITERIA

Demotion = reduction in authority level or scope restriction without full demotion.
Owner approves all demotions. Orchestrator Agent may propose; never unilaterally execute.

### Scope Restriction (within current level)

Applied when one dimension fails for two consecutive monthly reviews without improvement:

- Remove the specific capability class where failures are concentrated (e.g., restrict production staging access if rollback rate is high)
- Restriction is logged in `core/ROLES.md` under the agent's entry as `[RESTRICTED: <capability> until <date>]`
- Restriction lifts automatically after 30 days of clean metrics in the restricted dimension — Orchestrator confirms and logs

### Authority Level Demotion (L3 → L2, L2 → L1)

Triggered by any of:

- Two consecutive monthly verdicts of REASSIGNMENT or worse (see §5 verdict table)
- Any confirmed production incident caused by the agent where the agent exceeded its authority or bypassed a gate
- Sustained cost overrun: cost per task exceeds 3× target for 30+ days after Owner notification
- Domain ownership failure: agent's domain produces two consecutive GATE failures or a production rollback with root cause in domain agent decisions

**Demotion process:**
1. Orchestrator proposes demotion to Owner with: metric evidence, incident log, prior remediation attempts.
2. Owner approves. No demotion without Owner sign-off.
3. Domain ownership (if L3) transferred to another agent before demotion is effective — no orphaned domain.
4. All active tasks reassigned.
5. Agent re-onboards at new authority level per `core/ONBOARDING.md §4`.
6. Decision logged in `core/DECISION.md` with full evidence record.

### Immediate Restriction (Emergency)

When an agent produces a security incident, ethics violation, or irreversible harmful action:

1. Orchestrator Agent issues immediate scope restriction (write access revoked) — no Owner approval needed for this emergency step.
2. Owner notified within 15 minutes via Telegram: agent name, what happened, what was restricted.
3. Within 24h, Owner decides: restore, demote, or retire.
4. Emergency restriction and subsequent decision logged in `core/DECISION.md`.

---

## §5 — VERDICT TABLE

Used in monthly (§2.2) and quarterly (§2.3) reviews. Applied per agent based on 30-day rolling averages.

| Verdict | Condition | Action |
|---|---|---|
| PERFORMING | All 5 dimensions at target | No action. Continues. Eligible for promotion review at quarterly cycle. |
| WATCH | 1 dimension below target, no trend worsening | Monitor weekly. Orchestrator flags in next monthly report. No restriction yet. |
| SKILL-GAP | 1+ dimension below target AND escalation rate increasing | Trigger §6 skill gap detection. New rule or skill file created within 14 days. |
| PIP | 2+ dimensions below target OR any dimension ≥ 2× worse than target | Trigger §7 Performance Improvement Plan. |
| REASSIGNMENT | PIP did not resolve within 30 days | Move agent to a different, lower-complexity domain or role. Owner decides new assignment. |
| RETIREMENT | REASSIGNMENT failed OR ethics violation OR security incident | Retire per `core/HIRING.md §5`. |

**Escalation path:** PERFORMING → WATCH → SKILL-GAP/PIP → REASSIGNMENT → RETIREMENT.
Skipping levels is allowed when evidence warrants (e.g., ethics violation goes directly to RETIREMENT).

---

## §6 — SKILL GAP DETECTION

A skill gap is a structural deficiency in what an agent knows how to do — not a motivation problem.
Skill gaps are fixed by adding rules, updating prompts, or creating new skill files.

### Detection Signals

Any of the following triggers a skill gap investigation:

1. **Escalation rate increasing over 3+ consecutive weeks** — agent cannot resolve cases it should own
2. **Rework rate on a specific task category exceeds 20%** — agent's outputs in that category are systematically wrong
3. **Repeated identical error** — same root cause appears in ≥ 3 separate tasks within 30 days
4. **New task type fails** — agent assigned a task type it has no rule coverage for; BLOCK or escalation results

### Investigation Process

1. Orchestrator Agent (or Owner) identifies the failing task category and gathers 3–5 example failure cases.
2. Root cause analysis: is the failure due to a missing rule, a missing skill file, an ambiguous existing rule, or a model capability limit?
3. Root cause is one of four types:

| Root Cause Type | Remediation |
|---|---|
| Missing rule | Add a specific rule to the agent's system prompt or the relevant `core/` file |
| Missing skill file | Create a new skill file in `~/.1ai/skills/` (see §8 for new role creation if the gap is domain-wide) |
| Ambiguous existing rule | Clarify the rule in the existing file; version-bump the file |
| Model capability limit | Escalate to Owner — may require model upgrade or role scope reduction |

4. Remediation implemented by Orchestrator Agent (rule/skill update) or Owner (model change).
5. Agent re-tested on the failing task category: assign 3 tasks of the same type. All 3 must pass with LGTM verdict.
6. Gap resolution logged in `performance/skill-gaps/YYYY-MM-DD-[agent-id]-[category].md` with: signal that triggered investigation, root cause type, remediation applied, re-test results.

### Skill Gap File Format

`performance/skill-gaps/YYYY-MM-DD-[agent-id]-[category].md`:

```
## Skill Gap Record
- Agent: [agent-id]
- Date detected: YYYY-MM-DD
- Detected by: [Monitoring Agent | Orchestrator Agent | Owner | Reviewer Agent]
- Task category: [e.g., "cross-domain API contract negotiation"]
- Signal: [escalation rate / rework rate / repeated error / new task failure]
- Evidence tasks: [task-id-1, task-id-2, task-id-3]
- Root cause type: [missing rule | missing skill file | ambiguous rule | model limit]
- Remediation: [describe what was changed or created]
- Re-test tasks: [task-id-4, task-id-5, task-id-6]
- Re-test result: [PASS | FAIL]
- Status: [RESOLVED | ESCALATED TO OWNER]
```

---

## §7 — PERFORMANCE IMPROVEMENT PLAN (PIP)

A PIP is a structured 30-day remediation period. It is not punitive — it is a system correction.
PIP is triggered by verdict PIP from §5. Owner is notified before PIP begins.

### PIP Activation

1. Orchestrator Agent drafts PIP document within 3 days of PIP verdict.
2. PIP document content:
   - Agent name and current authority level
   - Failing dimensions and current values
   - Root cause assessment (is this a skill gap, a prompt issue, or a systemic overload?)
   - Specific improvement targets for each failing dimension (must be measurable)
   - Remediation steps (rule updates, prompt revisions, scope reduction, workload reduction)
   - Re-evaluation date: exactly 30 days from PIP start
   - Threshold for PIP pass vs. escalation to REASSIGNMENT
3. Owner approves PIP document before it takes effect.
4. PIP document stored at `performance/pip/[agent-id]-[YYYY-MM-DD].md`.

### During PIP

- Orchestrator Agent monitors the agent weekly (not monthly) — weekly report generated every 7 days.
- Remediation steps are implemented immediately at PIP start — not deferred to end of period.
- Agent's task load may be reduced to match its demonstrated capacity while remediation is applied.
- All PIP-period tasks are reviewed by Review Agent regardless of normal review sampling rate.

### PIP Outcome

At the 30-day re-evaluation date, Orchestrator Agent evaluates all failing dimensions:

| Outcome | Condition | Next Step |
|---|---|---|
| PIP PASS | All failing dimensions at or above target | Return to normal monitoring cadence. Log resolution in `core/DECISION.md`. |
| PIP PARTIAL | Some dimensions recovered, some still failing | Owner decides: extend PIP by 15 days (one-time only) OR proceed to REASSIGNMENT |
| PIP FAIL | No improvement in any failing dimension | REASSIGNMENT verdict. Orchestrator proposes new role per §5. |

### PIP Document Format

`performance/pip/[agent-id]-[YYYY-MM-DD].md`:

```
## PIP Record
- Agent: [agent-id]
- Authority level: [L1|L2|L3|L4]
- PIP start date: YYYY-MM-DD
- Re-evaluation date: YYYY-MM-DD
- Triggered by: monthly verdict PIP on [date]
- Owner approval: [Owner name, date]

## Failing Dimensions
| Dimension | Current Value | Target | Gap |
|---|---|---|---|

## Root Cause Assessment
[paragraph: what is causing the failure]

## Remediation Steps
1. [specific change, owner/who executes, by when]
2. ...

## Pass Threshold
[explicit numeric targets for each dimension that constitute PIP PASS]

## Weekly Check-ins
| Week | Dimension Scores | Status | Notes |
|---|---|---|---|

## Outcome
- Result: [PIP PASS | PIP PARTIAL | PIP FAIL]
- Date: YYYY-MM-DD
- Next action: [continue | extend | REASSIGNMENT]
- Decision logged: [link to core/DECISION.md entry]
```

---

## §8 — NEW ROLE CREATION

A new agent role is added to `core/ROLES.md` only when all criteria are met.
This section governs the performance signal that triggers role creation. The hire process itself is in `core/HIRING.md §2`.

### Criteria for Creating a New Role

All four conditions must hold:

1. **Skill gap is domain-wide, not task-specific.** Skill gap investigation (§6) concluded that no existing agent can cover the need with a rule or skill file update — a new domain is required.
2. **Recurring demand.** ≥ 5 tasks of the new type have accumulated in the backlog, OR a recurring monthly obligation (e.g., new product line, new compliance requirement) has been identified.
3. **Existing agents are not being under-utilized.** Owner verifies that no currently ACTIVE agent has headroom and matching domain proximity. A new role that duplicates an existing agent's capacity is not approved.
4. **Owner explicitly approves.** Owner writes role approval in `core/DECISION.md` before any configuration work begins.

### New Role Creation Process

1. **Owner writes role spec** (see `core/HIRING.md §2 Step 1` for required fields).
2. **Orchestrator Agent adds role to `core/ROLES.md §1`** with status `PENDING`.
3. **Performance baseline defined** before the role goes ACTIVE:
   - For each of the 5 dimensions (§1), Owner sets the role-specific target or confirms default targets apply.
   - Targets stored in `core/ROLES.md` under the role entry as `performance-targets`.
   - If no role-specific targets are set, default targets from §1 apply.
4. **Monitoring Agent updates its metric collection** to include the new agent ID within 24h of ACTIVE status.
5. **First performance review** occurs at 30 days (not the standard monthly cadence) — gives the new role a calibration period before formal verdict is applied.

---

## §9 — BENCHMARKING

Benchmarking compares an agent's current performance against its own baseline and against peer agents in the same role class.

### Baseline Establishment

Every agent's performance baseline is set during the first 30 days of ACTIVE status:

1. Monitoring Agent records daily metric values for all 5 dimensions.
2. At day 30, Orchestrator Agent computes 30-day averages and records them as the agent's baseline in `performance/baselines/[agent-id].json`.
3. Baseline format:

```json
{
  "agent_id": "[agent-id]",
  "role": "[role name]",
  "authority_level": "L[N]",
  "baseline_period": { "start": "YYYY-MM-DD", "end": "YYYY-MM-DD" },
  "dimensions": {
    "output_quality": { "first_pass_acceptance": 0.0, "rework_rate": 0.0, "block_rate": 0.0 },
    "error_rate": { "hard_error": 0.0, "silent_failure": 0.0, "ethics_stop": 0, "rollback": 0.0 },
    "escalation": { "escalation_rate": 0.0, "unnecessary_escalation_rate": 0.0 },
    "sla_compliance": { "on_time_rate": 0.0, "p1_compliance": 0.0, "overdue_hours_avg": 0.0 },
    "cost_efficiency": { "cost_per_simple_task": 0.0, "cost_per_complex_task": 0.0, "token_overrun_rate": 0.0 }
  }
}
```

4. Baseline is immutable once recorded. A new baseline may only be established after a major role change (authority level change, domain change, model upgrade) — Owner approves re-baselining.

### Peer Benchmarking

For roles with ≥ 2 active agents in the same role class (e.g., two L2 Worker Agents):

- Monitoring Agent computes peer-group averages quarterly.
- Individual agent scores are expressed as % above/below peer average, not just vs. absolute target.
- An agent scoring >20% below peer average on any dimension triggers a WATCH verdict even if it meets absolute targets (relative underperformance is a signal).
- Peer benchmark report included in quarterly authority review dossier (§2.3).

### Trend Analysis

Monthly summaries include a trend direction for each dimension: ↑ Improving, → Stable, ↓ Degrading.

- ↓ Degrading on any dimension for 2 consecutive months → automatic WATCH verdict regardless of whether absolute target is still met.
- ↑ Improving trend across all dimensions for 60+ days → eligible for promotion review (§3) at next quarterly cycle.

---

## §10 — PERFORMANCE LOG

All performance events, verdicts, and decisions are recorded in a structured log.

### Log Location and Structure

```
performance/
  metrics/
    [agent-id]-quality.csv       # §1.1 output quality events
    [agent-id]-errors.csv        # §1.2 error events
    [agent-id]-escalations.csv   # §1.3 escalation events
    [agent-id]-sla.csv           # §1.4 SLA events
    [agent-id]-cost.csv          # §1.5 cost events
  weekly/
    YYYY-WXX.md                  # §2.1 weekly automated report
  monthly/
    YYYY-MM.md                   # §2.2 monthly summary with verdicts
  quarterly/
    YYYY-QN.md                   # §2.3 quarterly authority review dossier
  baselines/
    [agent-id].json              # §9 baseline snapshots
  skill-gaps/
    YYYY-MM-DD-[agent-id]-[category].md   # §6 skill gap records
  pip/
    [agent-id]-[YYYY-MM-DD].md   # §7 PIP records
```

### CSV Metric Row Format

Each metric CSV row records one task-level observation:

```
task_id, date, agent_id, dimension, metric_name, value, target, pass_fail, notes
```

Example:
```
task-0042,2026-07-05,engineering-agent,output_quality,first_pass_acceptance,1,0.90,PASS,
task-0043,2026-07-05,engineering-agent,error_rate,hard_error,0,0.03,PASS,
task-0044,2026-07-05,engineering-agent,sla_compliance,on_time,0,0.95,FAIL,overdue 6h — dependency blocked
```

### Performance Events Requiring Immediate Log Entry

The following events are logged within 1h of occurrence (not batched to weekly):

| Event | Who logs | Where |
|---|---|---|
| Ethics stop triggered | Orchestrator Agent | `performance/metrics/[agent-id]-errors.csv` + `core/DECISION.md` |
| Production rollback caused by agent | Domain Agent + Orchestrator | `performance/metrics/[agent-id]-errors.csv` + `core/DECISION.md` |
| Emergency restriction invoked (§4) | Orchestrator Agent | `core/DECISION.md` |
| PIP activated | Orchestrator Agent | `performance/pip/[agent-id]-[date].md` + `core/DECISION.md` |
| Authority level change (promotion or demotion) | Orchestrator Agent | `core/DECISION.md` + `core/ROLES.md` update |
| Agent retirement | Owner + Orchestrator | `core/DECISION.md` + `core/ROLES.md` update + `core/HIRING.md §5` steps |

### Retention

- Metric CSVs: retained indefinitely (append-only, never modified)
- Weekly reports: retained 6 months, then archived to cold storage
- Monthly summaries: retained 24 months
- Quarterly dossiers: retained indefinitely
- Baselines, skill gap records, PIP records: retained indefinitely
- `core/DECISION.md` entries: retained indefinitely (immutable audit trail)

---

*PERFORMANCE.md governs agent effectiveness and authority. For role definitions, see ROLES.md. For the hire and retirement process, see HIRING.md. For individual code review, see REVIEWER.md. For incident response, see INCIDENT.md.*
