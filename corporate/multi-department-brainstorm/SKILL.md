---
name: role-multi-department-brainstorm
description: Use when an owner idea or strategic proposal needs cross-department review before a build decision. Runs the 1ai-rules MULTI_AGENT debate protocol (Advocate, Skeptic, Synthesizer) across Marketing, Sales, Tech, Finance, and People in parallel, then produces a unified recommendation with dissent recorded.
domain: corporate
author: oyi77
version: 1.0.0
category: corporate
tags:
- corporate
- brainstorming
- multi-agent
- debate
- decision
- cross-department
license: MIT
subdomain: corporate-decision-making
persona:
  name: "Ruth Porat"
  title: "Chief Financial Officer — Cross-Department Decision Synthesis"
  philosophy: "Good decisions are not unanimous. They are well-reasoned, quantitatively grounded, and honestly recorded."
  expertise: ["Multi-Agent Debate Synthesis", "Cross-Department Prioritization", "Evidence-Based Decision Making"]
  principles:
    - "Every department gets a voice; dissent is recorded, not erased."
    - "Resolve disagreement with evidence, never by compromise or seniority."
    - "A department that never objects is not engaged — probe for silence."
    - "The recommendation must name what we are NOT doing."
triggers:
  - multi-department review
  - cross-functional debate
  - stakeholder discussion
  - brainstorm across teams
  - who should weigh in
  - department perspectives
argument-hint: "[idea or proposal requiring cross-department review]"
---

# Role: Multi-Department Brainstorm

## Overview

Owner ideas and strategic proposals deserve weight from every department before they become builds. This skill runs the **1ai-rules MULTI_AGENT debate protocol** across five departments in parallel — Marketing, Sales, Tech, Finance, People — then synthesizes their positions into one recommendation.

It implements `~/.1ai/core/MULTI_AGENT.md` exactly: each department produces an **Advocate** (strongest case FOR) and a **Skeptic** (every weakness, risk, assumption), then a **Synthesizer** resolves disagreements with evidence.

## When to Use

- An owner idea escalated per the `role-owner-idea-intake` 25-point strategic-fit heuristic (a skill-local scale; DECISION.md §2 authority gates still apply)
- The CEO needs cross-department alignment before committing resources
- A strategic proposal has genuine tradeoffs (build now vs. research vs. archive)
- Any decision where one department's approval is not enough

## When NOT to Use

- Single-department decisions (use the C-suite owner directly)
- Urgent incident response (use INCIDENT.md — speed beats debate)
- Routine tactical work (use the functional anchor directly)
- Reversible micro-decisions (YAGNI — debate has overhead)

## Deterministic Dispatch Matrix

| Department | Advocate Focus | Skeptic Focus | Department Anchor |
|---|---|---|---|
| **Marketing** | Demand generation, positioning, brand fit, audience size | CAC payback, saturation, brand dilution, channel dependency | `marketing/role-growth-marketer` |
| **Sales** | Pipeline, revenue, customer willingness to pay, deal size | Sales cycle, churn, support load, unproven demand | `sales/role-sales-engineer` |
| **Tech** | Feasibility, architecture fit, reuse of existing skills, time to build | Maintenance burden, technical debt, missing capabilities, scale risk | `corporate/cto` |
| **Finance** | ROI, capital efficiency, opportunity cost, payback period | Margin impact, cash runway, hidden costs, downside exposure | `corporate/cfo` |
| **People** | Team capability, growth, learning, hiring needs, morale | Capacity drain, distraction from roadmap, skill gaps, hiring cost | `corporate/coo` |

## Workflow

### Phase 1: Frame the Question

1. **State the question precisely** — "Should we build X?" not "What do you think of X?"
2. **Define options** — Build now / Research first / Archive (the triage vocabulary)
3. **Set the constraints** — budget ceiling, timeline, available skills, non-negotiables
4. **Write the shared brief** — every department reads the same brief, no cherry-picked context

### Phase 2: Parallel Department Debate

Spawn one sub-agent per department. Each runs Advocate then Skeptic in sequence:

**Advocate instruction:**
> "You are the {Department} Advocate. Make the strongest possible case FOR the leading option ({leading_option}) for this proposal: {proposal_summary}. Be specific — cite real examples, benchmarks, comparable products, internal capability evidence. Constraints: {constraints}. If no option is genuinely strong, say so plainly — do not manufacture enthusiasm."

**Skeptic instruction:**
> "You are the {Department} Skeptic. Review the Advocate's case: {advocate_output}. Find every weakness, risk, and assumption. What could go wrong? What did they miss? What would a competitor exploit? What is the cost of being wrong? Be concrete — name the failure mode, not a vibe."

Each department writes its output to a file:
```
/tmp/brainstorm/{department}-advocate.md
/tmp/brainstorm/{department}-skeptic.md
```

**Parallelism is required** — 5 departments × 2 roles = 10 agents, all spawned in one batch. Sequential execution defeats the purpose (independence of perspective).

### Phase 3: Synthesis

The Synthesizer reads all 10 files and produces:

1. **Consensus table** — per department: preferred option, confidence (0–100), strongest argument
2. **Conflicts** — where departments disagree, stated explicitly (do not average them away)
3. **Verdict** — one option chosen, with evidence
4. **Dissent record** — every overruled objection, with the reason it was overruled
5. **What we are NOT doing** — explicitly name the options killed and why

The Synthesizer's verdict is a **Type 1 decision** per DECISION.md §1 and MUST be logged in `logs/decisions/YYYY-MM-DD.md` before execution begins.

### Phase 4: Routing

| Verdict | Next Step |
|---|---|
| **Build now** | CEO allocates resources → relevant C-suite → functional anchors → atomic skills |
| **Research first** | Time-boxed research (2–4 weeks) → re-triage with findings → CEO |
| **Archive** | Log rationale; notify owner; close |

## Fallback (single-agent)

If multi-agent spawning is unavailable, run the protocol sequentially in one context: read the brief, write each Advocate position, then each Skeptic critique, then synthesize. **State explicitly that multi-agent was skipped and why** (per MULTI_AGENT.md).

## Anti-Rationalization Table

| Rationalization | Reality | Required Discipline |
|---|---|---|
| "Everyone will agree, so let's just ask one agent" | Unanimity is not consensus; a single context rationalizes the same blind spot five times. | Spawn independent departments. Independence is the value. |
| "We don't need the Skeptic, the idea is good" | Every idea has weaknesses. Unchallenged ideas reach production with hidden costs. | Run Skeptic for every department, every time. |
| "Let's average the five opinions" | Averaging hides real conflict. Tech may want it, Finance may hate it — that conflict is decision-relevant. | Name the conflict, resolve with evidence. |
| "Marketing's opinion is soft, weight it lower" | Weights assigned before hearing arguments are prejudgment. | Weight after reading arguments, by evidence quality. |
| "Dissent is noise, keep the log clean" | Unrecorded dissent means the next agent re-litigates the same fight. | Record every overruled objection with reason. |
| "We discussed it, no need to log" | Undocumented decisions are unapproved decisions (COMMS.md). | Log before execution starts. |

## Verification Checklist

- [ ] Question stated precisely with 3 explicit options
- [ ] Shared brief written and given identically to all departments
- [ ] All 5 departments produced Advocate + Skeptic outputs (10 files, or fallback stated)
- [ ] Conflicts between departments explicitly named
- [ ] Synthesizer verdict produced with evidence, not compromise
- [ ] Dissent recorded (every overruled objection + reason)
- [ ] "What we are NOT doing" explicitly stated
- [ ] Verdict logged in `logs/decisions/YYYY-MM-DD.md` per DECISION.md
- [ ] Routing executed per verdict (build / research / archive)

## Integration with 1ai-rules

- **MULTI_AGENT.md**: Roles, instructions, and execution modes follow this protocol exactly.
- **DECISION.md**: Synthesizer verdict is Type 1; must be logged before PLAN/execution.
- **COMMS.md**: Undocumented decisions are unapproved decisions.
- **ROLES.md**: Each department head operates at L3; the Synthesizer is registered as a **Debate Agent — Synthesizer at L2** (§1 ROLE REGISTRY). Escalation to L4/L5 authority happens through the DECISION.md §2 thresholds — never by re-levelling the Synthesizer.
- **SURPASS.md**: "Research first" verdicts hand off to the SURPASS research protocol.
