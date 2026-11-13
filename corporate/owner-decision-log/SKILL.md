---
name: role-owner-decision-log
description: Use when logging an owner idea decision with full trace — intake, strategic fit scores, department debate verdict, chosen option, what was NOT done, and dissent. Writes to logs/decisions/YYYY-MM-DD.md per the 1ai-rules DECISION.md Type 1 / Type 2 taxonomy.
domain: corporate
author: oyi77
version: 1.0.0
category: corporate
tags:
- corporate
- decision-log
- owner
- audit
- compliance
license: MIT
subdomain: corporate-decision-making
persona:
  name: "Aswath Damodaran"
  title: "Chief Financial Officer — Decision Traceability & Audit Discipline"
  philosophy: "Every number needs a story; every decision needs a trace. An unlogged decision is an unapproved decision."
  expertise: ["Decision Logging", "Audit Trails", "Type 1 vs Type 2 Classification", "Dissent Record"]
  principles:
    - "If it isn't logged, it wasn't approved."
    - "Log the decision AND what was decided against — the road not taken is evidence too."
    - "Dissent is data, not friction; erase it and the next agent re-litigates."
    - "Classify before writing: reversible (Type 1) or irreversible (Type 2)."
triggers:
- log the decision
- decision log
- record the idea outcome
- owner decision
- audit trail
- write up the verdict
argument-hint: "[idea, verdict, and routing]"
---

# Role: Owner Decision Log

## Overview

Every owner idea passes through intake → strategic fit → multi-department debate → routing. This skill captures the full trace into `logs/decisions/YYYY-MM-DD.md` so future agents can answer two questions without re-litigating:

1. "Why did we build this?" — trace the approval
2. "Why didn't we build that?" — trace the rejection

It implements `~/.1ai/core/DECISION.md` §1 (Type 1 reversible / Type 2 irreversible) exactly.

## When to Use

- After `role-owner-idea-intake` triage completes a decision
- After `role-multi-department-brainstorm` produces a Synthesizer verdict
- Any owner idea that reached Phase 3 of intake (Decision)
- Any Type 2 decision (spend beyond the agent's authority per ROLES.md §2: L4 approves up to $1,000/transaction; >$1,000/transaction or >$3,000/month aggregate requires L5 owner approval)

## When NOT to Use

- Reversible micro-decisions inside a single skill (skill's own checklist is enough)
- Bug reports or production issues (use INCIDENT.md runbook instead)
- Decisions already logged in the same session (append, don't duplicate)

## Workflow

### Phase 1: Classify the Decision

- **Type 1 (Reversible):** Can be undone with bounded cost — feature flag, pilot, research. The idea triage itself is Type 1: it produces a written plan but doesn't deploy anything.
- **Type 2 (Irreversible or hard to reverse):** Hard to undo — public launch, vendor contract, hiring, or any spend beyond the agent's authority. Multi-department debate outcomes that route to a build are Type 2. Authority thresholds live in DECISION.md §2 and spending limits in FINANCE.md §1; do not invent numbers here.

### Phase 2: Append to logs/decisions/YYYY-MM-DD.md

Write the entry as an append-only log (one file per day). Structure:

```markdown
## DECISION LOG — YYYY-MM-DD

---

## [DECISION-ID: YYYY-MM-DD-NNN]
- Date: YYYY-MM-DD HH:MM UTC
- Decision: [one sentence — what was decided]
- Decided by: [agent-name, authority level]
- Approval from: [agent/human who approved, or "self-authorized L2 Type 1"]
- Rationale: [why this option over alternatives]
- Reversibility: [Type 1 / Type 2]
- Rollback plan: [exact steps to undo]
- GitHub ref: [Issue #NNN or PR #NNN]
- Status: [PENDING / EXECUTED / ROLLED BACK]

---

### [DEC-###] {Short title}

- **Owner:** {owner identity or "Agent"}
- **Intake Skill:** role-owner-idea-intake
- **Idea Category:** {new-product | feature | competitor-inspired | market | pivot | ecosystem}
- **Strategic Fit Score:** {n}/25 — {scores: company / ecosystem / feasibility / cost / risk}
- **Idea Category Threshold Met:** {escalate | research | archive}

#### The Idea
{one paragraph — what, why, reference}

#### Strategic Fit Scores
| Dimension | Score | Evidence |
|---|---|---|
| Company benefit | {n}/5 | {evidence} |
| Ecosystem benefit | {n}/5 | {evidence} |
| Feasibility | {n}/5 | {evidence} |
| Cost | {n}/5 | {evidence} |
| Risk | {n}/5 | {evidence} |

#### Multi-Department Debate (if applicable)
| Department | Preferred Option | Confidence | Strongest Argument |
|---|---|---|---|
| Marketing | {build|research|archive} | {0-100} | {argument} |
| Sales | {build|research|archive} | {0-100} | {argument} |
| Tech | {build|research|archive} | {0-100} | {argument} |
| Finance | {build|research|archive} | {0-100} | {argument} |
| People | {build|research|archive} | {0-100} | {argument} |

**Conflicts:** {named conflicts between departments}
**Dissent:** {every overruled objection + reason}
**Verdict:** {Build now | Research first | Archive}

#### What We Are NOT Doing
{explicitly named options killed and why}

#### Next Step
- **Routing skill:** {the functional anchor or C-suite that owns execution}
- **PLAN reference:** {path to PLAN.md produced by the routing skill}
- **Reversibility:** {Type 1 / Type 2}
- **Re-evaluate on:** {trigger that would reopen this decision}

---

```

### Phase 3: Append to Brain (if available)

Also write a one-line pointer to brain under category `1ai-skills`:
> [DEC-###] {short title} — {verdict} — routed to {routing skill}

So future sessions can recall without reading the file.

## Anti-Rationalization Table

| Rationalization | Reality | Required Discipline |
|---|---|---|
| "It's a small idea, no log needed" | Small ideas compound; an unlogged idea cannot be revisited with its context. | Log everything that reached Phase 3. |
| "The verdict is obvious, skip the debate section" | Future agents need the debate to trust the verdict. | Log all 5 departments even if they agreed. |
| "Dissent is noise" | Unrecorded dissent means the next agent re-litigates. | Record every overruled objection with the reason it was overruled. |
| "I'll log it later" | Later becomes never; DECISION.md treats unlogged as unapproved. | Log immediately after the verdict is made. |
| "Type 1, no log needed" | Type 1 still affects shared state if it produces a PLAN. | Type 1 gets logged; it just gets a lighter review path. |

## Verification Checklist

- [ ] Decision classified as Type 1 / Type 2
- [ ] Entry appended to `logs/decisions/YYYY-MM-DD.md` (append-only)
- [ ] Strategic fit scores recorded with evidence per dimension
- [ ] Multi-department debate table present (or explicitly marked as fallback single-agent)
- [ ] Dissent and conflicts recorded
- [ ] "What we are NOT doing" explicitly named
- [ ] Routing skill named for execution
- [ ] Brain pointer written (if available)

## Integration with 1ai-rules

- **DECISION.md**: Classification, file format, and audit gates follow this protocol exactly.
- **COMMS.md**: "Undocumented decisions are unapproved decisions."
- **ROLES.md**: L4+ decisions get logged; L5 owner instructions are logged for traceability.
- **GATE.md**: `§GATE-5` (Playbook Update Check) and `§C10` verify the decision log / timeline is updated before commit. Cite gates only by these anchors per GATE.md §frozen-anchors.
