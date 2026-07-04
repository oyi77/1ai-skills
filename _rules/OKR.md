---
name: okr
version: 1.0.0
severity: mandatory
scope: [all]
pairs-with: [mission, roles, decision, comms]
description: Quarterly objectives, key results, KPIs, and work alignment
---

# OKR.md — Objectives, Key Results & Work Alignment

> **Every task must trace to a KR. If it doesn't, question whether to do it.**
> Agents that execute tasks not tied to OKRs are burning capacity on noise.

---

## §1 — OKR PHILOSOPHY

OKRs are the operating contract between the owner and all agents. They answer:
- **Where are we going this quarter?** (Objectives)
- **How will we know we got there?** (Key Results)
- **Is this task worth doing?** (Task-to-KR mapping)

Rules:
- OKRs are set by the owner at the start of each quarter. No agent sets OKRs unilaterally.
- OKRs are **aspirational, not guaranteed** — hitting 70% of a hard KR beats hitting 100% of an easy one.
- KRs must be **measurable** — a KR without a number or binary outcome is not a KR, it's a wish.
- Every STANDARD and COMPLEX task (per PLAN.md §4) must reference a KR before work begins.
- OKRs do not replace daily judgment — they bound it. Within a KR, agents still decide how.

---

## §2 — OKR STRUCTURE

```
COMPANY OKRs
  Set by:   Owner, start of quarter
  Count:    3–5 Objectives maximum (focus beats breadth)
  Per O:    2–4 Key Results (measurable, time-bound, binary or percentage)
  Stored:   GitHub issue tagged okr-Q[N]-[YEAR], pinned to repo

AGENT OKRs
  Set by:   Each active agent, derived from Company OKRs
  Count:    1–3 Objectives per agent (aligned to assigned domain)
  Format:   Subset of Company KRs the agent is responsible for advancing
  Stored:   Agent's weekly check-in (§4), referenced in task descriptions

FORMAT
  O:   [Objective — qualitative, directional, inspirational — NO numbers here]
  KR:  [Key Result — metric + current value + target + deadline]
       Example: KR1.1: Increase MRR from Rp 5jt to Rp 20jt by end of Q3 2026
       Example: KR1.2: Ship affiliate automation v1 by 2026-07-31
       Example: KR2.1: Reduce deploy-to-production time from 45min to <15min
```

Anti-patterns:
- ❌ KR: "Improve content quality" — not measurable
- ✅ KR: "Achieve average video engagement rate >5% across 50 published videos"
- ❌ O: "Grow revenue by 3×" — objectives are qualitative; numbers go in KRs
- ✅ O: "Establish BerkahKarya as a revenue-generating autonomous business"

---

## §3 — CURRENT QUARTER TEMPLATE

Owner fills this template at the start of each quarter and posts it as a GitHub issue
tagged `okr-Q[N]-[YEAR]`. Agents read that issue at session start.

```
QUARTER: Q[N] [YEAR]  |  Start: [DATE]  |  End: [DATE]
North Star: [metric from MISSION.md §5]  |  Current: [value]  |  Target: [value]

O1: [Objective 1 — qualitative]
  KR1.1: [metric] from [current] to [target] by [date]
  KR1.2: [metric] from [current] to [target] by [date]
  KR1.3: [metric] from [current] to [target] by [date]

O2: [Objective 2 — qualitative]
  KR2.1: [metric] from [current] to [target] by [date]
  KR2.2: [metric] from [current] to [target] by [date]

O3: [Objective 3 — qualitative]
  KR3.1: [metric] from [current] to [target] by [date]
  KR3.2: [metric] from [current] to [target] by [date]

O4: [Objective 4 — qualitative]  [optional]
  KR4.1: [metric] from [current] to [target] by [date]

O5: [Objective 5 — qualitative]  [optional]
  KR5.1: [metric] from [current] to [target] by [date]
```

How to fill:
1. Owner writes the above, posts as GitHub issue titled `OKR Q[N] [YEAR]`
2. Issue is labeled `okr-Q[N]-[YEAR]` and pinned or linked from repo README
3. Agents load this issue at session start — treat it as the operating contract
4. Mid-quarter updates: owner edits the issue body; agents re-read on next session start

---

## §4 — WEEKLY CHECK-IN FORMAT

Every Monday, each active agent posts a check-in. Format:

```
WEEKLY OKR CHECK-IN — [AGENT NAME] — [DATE]

KRs progressed this week:
  KR[N.N]: [metric] → moved from [X] to [Y] (delta: +[Z])
  KR[N.N]: [completed / shipped / milestone reached — describe]

KRs at risk:
  KR[N.N]: [why at risk] → mitigation: [specific action this week]
  KR[N.N]: [blocked by] → needs: [owner decision / unblocked by agent X]

Blockers requiring owner input:
  - [specific question or decision needed — not vague status updates]

Tasks completed that advanced KRs:
  - [task] → advanced [KR ref]

Tasks completed with no KR link (flag):
  - [task] → reason executed: [maintenance / urgent / owner-directed]
```

Rules:
- Post to #weekly-okr channel or as GitHub comment on the current quarter's OKR issue.
- No check-in = agent assumed idle; owner may reassign capacity.
- "No progress" is an acceptable entry — silence is not.
- Agents MUST flag tasks executed without KR link — this surfaces scope drift.

---

## §5 — TASK-TO-OKR MAPPING

Before starting any STANDARD or COMPLEX task (per PLAN.md §4), the agent MUST state:

```
TASK-TO-OKR MAPPING

Task:        [brief description]
Scope:       [STANDARD / COMPLEX]
Advances:    KR[N.N] — [KR description]
How:         [1 sentence — how this task moves the KR needle]
```

If no KR match is found:

```
NO KR MATCH FOUND

Task:        [brief description]
Reason considered: [why this seemed worth doing]
Action:      → Flag to owner via COMMS.md before proceeding
             → Do NOT start STANDARD/COMPLEX work without KR justification
             → Exception: SEV1/SEV2 incidents (follow INCIDENT.md instead)
```

TRIVIAL tasks (per PLAN.md §4) are exempt from mandatory KR mapping — but agents
should still note KR relevance when obvious.

Autonomous agents (running 24/7 without per-task owner prompts) MUST apply this mapping
to every non-trivial decision. If uncertain → default to owner notification (COMMS.md §3).

---

## §6 — OKR REVIEW

End of each quarter, owner reviews all KRs and scores them.

```
SCORING SCALE
  0.0 – 0.3   No meaningful progress — investigate root cause
  0.4 – 0.5   Partial — significant gaps; retrospective required
  0.6 – 0.7   On target — sweet spot for ambitious KRs
  0.8 – 0.9   Strong result
  1.0          Full achievement — if consistent, KR was set too easy

REVIEW PROTOCOL (owner runs this)
  1. For each KR: record final metric value and compute score
  2. Score <0.4: file a post-mortem issue — what went wrong, what to change
  3. Score >0.9 consistently: raise ambition for next quarter
  4. Identify which agents contributed to each KR — feed into ROLES.md review
  5. Carry unfinished KRs forward only if still strategically relevant — don't auto-carry
  6. Post review summary as GitHub issue tagged okr-review-Q[N]-[YEAR]

WHAT TO EXAMINE IN LOW-SCORE KRs
  - Was the KR actually measurable? (bad KR design)
  - Did agents execute tasks not tied to this KR? (misaligned capacity)
  - Was the target realistic given resources? (bad calibration)
  - Did blockers go unescalated? (comms failure — see COMMS.md)
```

---

## §7 — NORTH STAR ALIGNMENT

Every Objective must trace to the North Star metric defined in MISSION.md §5.

```
ALIGNMENT CHECK (run at OKR-setting time)

For each Objective:
  → Ask: "If we achieve this O and all its KRs, does the North Star metric move?"
  → If YES: aligned — proceed
  → If NO or UNCLEAR: reject or reframe the Objective before finalizing

OKRs that do not trace to the North Star → REJECTED by owner review
OKRs that contradict MISSION.md values → REJECTED by owner review

Alignment is not optional — it is the filter that prevents busy-work quarters.
```

Rules:
- Agent OKRs that conflict with Company OKRs must be escalated to owner — not silently executed.
- Adding an Objective mid-quarter requires owner approval and a GitHub comment on the OKR issue.
- Removing a KR mid-quarter requires owner approval — capacity is not freed without a decision.

---

## §8 — INTEGRATION WITH CORE LOOP

```
MISSION.md (North Star)
    ↓
OKR.md §3 (quarterly OKRs set by owner)
    ↓
PLAN.md §2 (task decomposition references KR in §5)
    ↓
ROLES.md (agent assignments aligned to OKR domains)
    ↓
COMMS.md (weekly check-in §4, blockers escalated)
    ↓
OKR.md §6 (end-of-quarter review → feeds next quarter)
```

> 🚫 *"This is urgent" is not a KR. Urgency without alignment is just noise.*
> ✓ *"Does this move a KR?" — ask before every STANDARD/COMPLEX task.*
