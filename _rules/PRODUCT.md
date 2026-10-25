---
name: product
version: 1.0.0
severity: mandatory
scope: [planning, backlog, features, deprecation]
pairs-with: [plan, prd, gate, decision, release]
description: Feature lifecycle protocol — intake through deprecation, scope control, flags, metrics, and backlog hygiene
---

# PRODUCT.md — Feature Lifecycle Protocol

> **Every feature that ships was worth building. Every feature that didn't get deprecated was worth removing.**
> This rule governs the full life of a feature: from idea to graveyard.

---

## §1 — FEATURE INTAKE FILTER

Before any idea enters the backlog, it must answer all four questions. A "no" or "unclear" on any question means the idea is **REJECTED** or **PARKED** (not discarded — parked in the Icebox).

### The Four Questions

**Q1 — What problem does this solve?**
- Must name a specific, observable user or business pain.
- "It would be nice" is not a problem.
- "Users can't do X without Y manual steps" is a problem.
- A vague answer → PARK, not backlog.

**Q2 — Who will use this, and how often?**
- Must name the user segment (new user, returning user, power user, agent, admin).
- Must estimate frequency: daily / weekly / occasional / one-time.
- Features used less than once per week by less than 10% of users need extraordinary justification.

**Q3 — What does success look like, measurably?**
- Must name at least one metric that changes when the feature succeeds.
- Acceptable: conversion rate, activation rate, retention, revenue, error rate, task completion time.
- "Users will be happier" is not measurable → PARK.

**Q4 — What is the opportunity cost?**
- What does this displace? (Every build slot spent here is not spent elsewhere.)
- State the next-best alternative feature that gets deferred if this is built.
- If the deferred alternative is clearly more valuable → REJECT this idea, promote the alternative.

### Intake Verdict

| Q1 | Q2 | Q3 | Q4 | Verdict |
|----|----|----|-----|---------|
| ✅ | ✅ | ✅ | ✅ | → BACKLOG (IDEA stage) |
| ✅ | ✅ | ❌ | any | → PARK (define metric first) |
| ❌ | any | any | any | → REJECT |
| any | ❌ | any | any | → PARK (identify audience first) |
| ✅ | ✅ | ✅ | ❌ worse | → REJECT (promote deferred alternative) |

---

## §2 — FEATURE LIFECYCLE STAGES

Every feature lives in exactly one stage at all times. Stages are sequential; skipping is a protocol violation.

```
IDEA → VALIDATED → SPECCED → BUILDING → SHIPPED → MONITORED → DEPRECATED
         ↑                                              ↓
         └──────────────── PARKED ◄────────────────────┘
                                                   (if metrics fail)
```

### Stage Definitions

| Stage | Owner | Entry Condition | Exit Condition |
|-------|-------|-----------------|----------------|
| IDEA | any agent or human | Passed §1 intake filter | Validated per §3 |
| VALIDATED | product agent | Evidence gathered per §3 | PRD written and approved |
| SPECCED | product agent | PRD approved | Atomic issues created, PLAN.md complete |
| BUILDING | builder agent | Issues assigned, no scope conflicts | All ACs green, GATE.md passed |
| SHIPPED | release agent | Merged to main, deployed | Monitoring window elapsed (≥7 days) |
| MONITORED | any agent | Feature live | Declared success OR failure per §6 |
| DEPRECATED | any agent | Failure declared OR trigger hit per §7 | Code removed, users migrated |
| PARKED | — | Failed validation, low priority | Re-evaluated at next backlog review |

---

## §3 — VALIDATION CRITERIA (IDEA → VALIDATED)

A feature moves from IDEA to VALIDATED only when ALL of the following evidence exists:

**Evidence required:**

1. **User signal** — At least one of:
   - Direct user request (verbatim, with source)
   - Support ticket referencing the gap
   - User behaviour data showing workaround (e.g., drop-off at step X)
   - Competitor analysis showing 2+ competitors have this (market signal)

2. **Metric baseline** — Current value of the success metric from Q3.
   - "We don't track this yet" → instrument it first, then validate.
   - No baseline = no way to measure success = not validated.

3. **Size estimate** — Build complexity classified per PLAN.md §4 (TRIVIAL / STANDARD / COMPLEX).
   - COMPLEX features need a rough PRD sketch before validation is complete.

4. **Risk flag** — Boolean: does this touch auth, payments, user data, or a shared API?
   - If YES: security review required before SPECCED stage.

**Validation Record format:**

```
VALIDATION RECORD
Feature:        [name]
Date:           [YYYY-MM-DD]
User signal:    [verbatim quote / ticket ID / data point]
Success metric: [metric name] current baseline: [value]
Size estimate:  TRIVIAL / STANDARD / COMPLEX
Risk flag:      YES (auth/payments/data/shared-API) / NO
Validated by:   [agent id]
```

---

## §4 — DEFINITION OF DONE PER STAGE

### IDEA → VALIDATED
- [ ] All four §1 questions answered with concrete answers (not "TBD")
- [ ] Validation Record written per §3

### VALIDATED → SPECCED
- [ ] PRD written using PRD.md §2 template (mandatory for COMPLEX, recommended for STANDARD)
- [ ] Non-Goals section explicitly lists ≥2 items (scope guard)
- [ ] Acceptance Criteria are observable and testable (not "works correctly")
- [ ] Atomic issues created per PRD.md §3 (for STANDARD/COMPLEX)
- [ ] PLAN.md decomposition complete (for COMPLEX)

### SPECCED → BUILDING
- [ ] All issues have ACs
- [ ] No unresolved blocking issues
- [ ] Feature flag decision made per §5 (flag required or not)
- [ ] Rollback plan documented

### BUILDING → SHIPPED
- [ ] All GATE.md gates passed
- [ ] All ACs verified with receipts
- [ ] REVIEWER.md review complete (for COMPLEX)
- [ ] Metrics instrumentation live (the success metric from validation must be emitting data)
- [ ] Feature flag active (if required) or feature is behind access control

### SHIPPED → MONITORED
- [ ] Monitoring window opened (timestamp recorded)
- [ ] Metrics dashboard or query defined for the success metric
- [ ] Alert set if error rate for this feature exceeds 2× pre-ship baseline

### MONITORED → DEPRECATED (failure path)
- [ ] Failure declared per §7 triggers
- [ ] Migration plan written for affected users
- [ ] Removal issue created

### MONITORED → (sustained — no action)
- [ ] Success declared per §6 within 30 days of ship
- [ ] Feature moves off active monitoring into steady-state

---

## §5 — FEATURE FLAG PROTOCOL

### When to use a flag

Use a feature flag when ANY of the following is true:
- The feature is COMPLEX (as classified by PLAN.md §4)
- The feature touches payments, auth, or user data
- The feature changes an existing user-facing behaviour (not purely additive)
- The feature needs A/B testing or staged rollout
- The feature is on the critical path for a revenue-generating flow

Do NOT use a flag when:
- The feature is TRIVIAL with no user-facing surface
- The feature is behind existing auth/role controls that serve as natural gates
- The flag would outlive the feature by design (flag for a flag is noise)

### Flag naming convention

```
FLAG_<PRODUCT_AREA>_<FEATURE_NAME>_<YYYYMM>

Examples:
FLAG_BILLING_ANNUAL_PLAN_202506
FLAG_ONBOARDING_VIDEO_INTRO_202507
FLAG_API_V2_RATE_LIMIT_202504
```

### Flag management rules

1. **Every flag gets an expiry date** at creation: `expires: YYYY-MM-DD` (max 90 days from creation).
2. **Flags are tracked in one place**: `core/feature-flags.md` (append-only register).
3. **No flag survives past its expiry** without an explicit renewal decision logged in DECISION.md.
4. **Rollout sequence**: 0% → internal agents only → 10% → 50% → 100% → flag removed.
5. **Rollback trigger**: if error rate for flagged cohort is >2× control at any rollout step, roll back to previous percentage immediately, file an incident.

### Flag cleanup rules

- At SHIPPED → MONITORED transition: set flag to 100% (or disable if kill-switch scenario).
- At success declaration (§6): schedule flag removal issue within 7 days.
- Expired flag not renewed after 7 days = emergency removal issue created automatically by backlog review.
- Code containing a removed flag's `if/else` branches must be cleaned up in the same PR as flag removal — no orphan branches.

---

## §6 — METRICS AND SUCCESS/FAILURE DECLARATION

### What to measure

Every shipped feature must have exactly one **primary success metric** (defined at validation) and up to two **guardrail metrics** (things that must not get worse).

| Metric type | Examples |
|-------------|----------|
| Primary (pick one) | conversion rate, activation rate, feature adoption %, revenue attributable, task completion rate, error rate reduction |
| Guardrail (up to 2) | page load time, overall error rate, support ticket volume, churn rate |

### Measurement window

- Monitoring window: **14 days minimum** from ship date (30 days preferred for revenue-impacting features).
- Read metrics at: day 7, day 14, day 30.

### Success declaration criteria

Declare **SUCCESS** when ALL of the following hold at end of monitoring window:
1. Primary metric moved in the target direction by ≥10% (or hit the specific target set in PRD).
2. No guardrail metric degraded by >5% vs pre-ship baseline.
3. Feature-specific error rate ≤1% of invocations.

On success: record outcome in DECISION.md, close monitoring, schedule flag cleanup (§5).

### Failure declaration criteria

Declare **FAILURE** (triggers §7 deprecation evaluation) when ANY of the following hold:
1. Primary metric did not move after 30 days.
2. Primary metric moved in the wrong direction.
3. Any guardrail metric degraded by >10% vs baseline.
4. Feature-specific error rate >5% sustained for ≥48 hours.
5. Zero adoption after 14 days (no user invocations).

On failure: do NOT immediately deprecate — run §7 evaluation first to decide between fix, pivot, or deprecate.

---

## §7 — DEPRECATION TRIGGERS

A feature enters DEPRECATED evaluation when ANY condition is met:

| Trigger | Condition |
|---------|-----------|
| Adoption failure | Zero meaningful usage for 30 consecutive days post-ship |
| Metric failure | Declared FAILURE per §6 AND no fix is feasible within 14 days |
| Superseded | A new feature fully covers the same job-to-be-done |
| Cost > value | Infrastructure cost of feature exceeds its attributable revenue for 2 consecutive months |
| Security risk | Feature has an unresolvable security finding (auth, data exposure) |
| Tech debt ceiling | Feature requires >40 hours to maintain per quarter, with no proportional value |
| Strategic pivot | Company direction change makes the feature irrelevant to the North Star (MRR) |

### Deprecation process

1. **Evaluate**: confirm the trigger is real, not a data artifact. Check metrics for 48 hours.
2. **Decide**: document in DECISION.md — deprecate, fix, or pivot.
3. **Notify**: if users exist, announce deprecation with timeline (minimum 14-day notice for active features).
4. **Migrate**: write migration path for affected users. No feature is removed without a migration path unless adoption is zero.
5. **Remove**: create a removal issue. Code removal is MANDATORY — deprecated features must not sit in codebase indefinitely. Removal deadline: 30 days from deprecation declaration.
6. **Record**: add entry to `core/graveyard.md` with: feature name, ship date, deprecation date, trigger, outcome, lessons learned.

---

## §8 — SCOPE CONTROL (mid-build rules)

Scope creep is the primary reason features ship late, break other things, or never ship at all.

### What constitutes scope creep

- Adding a requirement not in the original ACs after BUILDING stage begins.
- Expanding the user segment targeted beyond what was specced.
- Adding UI to a backend-only specced feature (or vice versa).
- "Refactoring while I'm at it" beyond what is required to implement the feature.
- Adding a new dependency not in the original PLAN.md risk assessment.

### Scope creep response protocol

When scope creep is detected during BUILDING:

```
1. STOP — do not absorb the new scope into the current build.
2. DOCUMENT — write: "Original scope: [X]. Requested addition: [Y]. Delta: [Z]."
3. TRIAGE — classify the addition:
   a. Required to make the feature work? → Emergency scope change (step 4).
   b. Nice to have / discovered need? → New IDEA, go through §1 intake.
   c. Bug found while building? → Separate fix issue, unblocked from current feature.
4. Emergency scope change process:
   - Re-run §1 intake for the addition.
   - Re-classify scope per PLAN.md §4.
   - If COMPLEX: pause current PR, write new PRD for the addition.
   - If STANDARD: add as a new issue, do not bundle into current PR.
   - If TRIVIAL: absorb only if it is a precondition (e.g., a missing type definition), not a feature.
5. NEVER extend a PR to absorb unplanned scope — split it.
```

### The Non-Goals contract

Every PRD has a Non-Goals section. Non-Goals are binding during BUILDING.
- If a requirement contradicts a Non-Goal: it requires explicit re-approval of the PRD, logged in DECISION.md.
- Agent cannot unilaterally override a Non-Goal — requires human owner sign-off.

---

## §9 — BACKLOG HYGIENE

### Staleness rules

| Stage | Max age before review | Action if stale |
|-------|-----------------------|-----------------|
| IDEA | 30 days | Promote to VALIDATED or move to Icebox |
| VALIDATED | 45 days | Spec it or move to Icebox |
| SPECCED | 60 days | Assign to build or move to Icebox |
| PARKED (Icebox) | 90 days | Re-evaluate or permanently REJECT |

### Backlog review cadence

- **Weekly**: scan for items breaching staleness thresholds. Auto-age items. No decisions needed — just flagging.
- **Monthly**: full backlog review. For each item: confirm it still passes §1 intake, re-score priority, prune or promote.
- **Quarterly**: clear the Icebox. Items that have been parked for >90 days with no champion get permanently rejected.

### Pruning protocol

An item is **permanently rejected** (removed from backlog) when ANY of the following:
1. It has been in the Icebox for >90 days with no activity.
2. The problem it solves no longer exists.
3. A shipped feature already solves it.
4. It failed §1 intake on re-evaluation.

Permanently rejected items are logged in `core/graveyard.md` with a one-line reason. They are not deleted — they are archived so the same idea is not re-submitted without context.

### Priority scoring

Backlog items are scored on three dimensions (1–5 each, sum = priority score):

| Dimension | 1 | 3 | 5 |
|-----------|---|---|---|
| **Impact** | cosmetic / edge case | improves existing flow | unlocks new revenue or retention |
| **Confidence** | no data | anecdotal signal | hard metric or user request |
| **Effort** | weeks (COMPLEX) | days (STANDARD) | hours (TRIVIAL) |

Items with score ≥10 are prioritised for next build slot. Items with score ≤5 are moved to Icebox.

---

## §10 — INTEGRATION WITH PLAN.md AND PRD.md

### How product decisions feed engineering execution

```
PRODUCT.md (lifecycle)
    ↓
  §1 Intake Filter
    ↓
  §3 Validation Record  ─────────────→  DECISION.md (record)
    ↓
  PRD.md §2 Template    ─────────────→  PLAN.md Step 2.5
    ↓
  PRD.md §3 Atomic Issues
    ↓
  PLAN.md §2 Decomposition Protocol
    ↓
  GATE.md (build gates)
    ↓
  RELEASE.md (ship)
    ↓
  §6 Metrics (monitor)
    ↓
  §7 Deprecation or steady-state
```

### Responsibility boundaries

| File | Answers |
|------|---------|
| PRODUCT.md | Should we build this? Is it worth building? Is it working? Should we kill it? |
| PRD.md | What exactly are we building? What are the ACs? |
| PLAN.md | How do we break this into shippable PRs? |
| GATE.md | Has each PR met the quality bar before merge? |
| RELEASE.md | How do we ship safely? |
| DECISION.md | Why did we choose this approach over the alternatives? |

### Handoff contract

- **PRODUCT → PRD**: Validation Record must exist before a PRD is started. PRD.md §2 template is mandatory for COMPLEX, optional for STANDARD.
- **PRD → PLAN**: PRD must be approved (or self-approved with DECISION.md rationale) before PLAN.md decomposition begins.
- **PLAN → GATE**: Each PR from decomposition runs GATE.md. No PR merges without GATE sign-off.
- **GATE → PRODUCT**: After merge, the feature transitions to SHIPPED stage. Monitoring window opens.
- **PRODUCT → DECISION**: Every deprecation decision, scope change approval, and failed-feature record is logged in DECISION.md.

### Feature flag coordination

- Feature flags are created at SPECCED → BUILDING transition, never earlier.
- Flag names, expiry dates, and rollout state are maintained in `core/feature-flags.md`.
- RELEASE.md governs the deployment mechanics; PRODUCT.md governs the rollout decision (which % gets the flag, when to advance).

---

> *"A backlog is not a wish list. It is a queue of bets, each with a stated hypothesis and an expiry."*
> *"Ship less, but ship what matters. Deprecate without guilt."*
