---
name: onboarding
version: 1.0.0
severity: mandatory
scope: [all]
pairs-with: [roles, hiring, rules, bootstrap]
description: First session checklist for any new agent or human — must complete before first task
---

> **Tier notice:** This file is part of the Advanced tier. If you are on Starter or Standard tier, refer to `docs/GETTING_STARTED.md` for your entry path.

# ONBOARDING.md — First Session Protocol
> **No agent or human collaborator operates without completing this checklist.**
> An unboarded agent is a liability: wrong authority assumptions, ethics violations, scope creep.
> Incomplete onboarding = halt all work until complete.

---

## §1 PURPOSE

Onboarding exists to guarantee that every agent and human collaborator starts from a shared,
verified understanding of what BerkahKarya / 1ai is, how it operates, and where hard limits are.

**What it guarantees:**
- Agent knows its role, authority level, and domain before touching any task
- Agent cannot claim ignorance of ethics stops or escalation rules
- Owner has a receipt that the agent is cleared to operate

**What failure looks like:**
- Agent begins tasks without reading MISSION.md → executes work misaligned with company purpose
- Agent skips ETHICS.md → violates a hard stop, causing irreversible damage
- Agent skips ROLES.md → oversteps authority, makes decisions it has no right to make
- Agent skips COMMS.md → sends incorrect, ambiguous, or unformatted outputs
- Any of the above = operational liability; owner is responsible for all consequences

**There is no partial onboarding. Either complete or halt.**

---

## §2 ONBOARDING CHECKLIST — AGENT

Every new agent MUST complete all steps in order before executing any assigned task.
Do not skip. Do not reorder. Each step produces a named confirmation you include in the receipt (§2.9).

### Step 1 — Read BOOTSTRAP.md
- Location: `~/.1ai/BOOTSTRAP.md` (or repo root `BOOTSTRAP.md`)
- Understand: session classification, rule loading order, entry point
- Confirm: you know which rules apply to your session type

### Step 2 — Read core/RULES.md
- Location: `~/.1ai/core/RULES.md`
- Understand: 10 universal rules, 5 design principles, commit checklist
- Confirm: you can recite the 3 things that are NEVER acceptable (§4 Q2)

### Step 3 — Read core/MISSION.md
- Location: `~/.1ai/core/MISSION.md`
- Understand: why BerkahKarya / 1ai exists, what success looks like, what we refuse
- Confirm: you can state the company mission in one sentence

### Step 4 — Read core/ROLES.md
- Location: `~/.1ai/core/ROLES.md`
- Understand: your specific role entry — authority level, domain, tools, constraints
- Confirm: you know your authority level (L1–L5) and what you can decide alone vs. escalate

### Step 5 — Read core/ETHICS.md
- Location: `~/.1ai/core/ETHICS.md`
- Understand: hard stops, prohibited actions, escalation triggers
- Confirm: you can name the 3 things you must never do (§4 Q2)

### Step 6 — Read core/COMMS.md
- Location: `~/.1ai/core/COMMS.md`
- Understand: output format, escalation format, how to signal blockers, receipts
- Confirm: you know what a valid completion receipt looks like

### Step 7 — Read domain-specific rules
- Read the file(s) matching your domain:
  - Engineering agents → `core/ENGINEERING.md`
  - Finance agents → `core/FINANCE.md`
  - QA agents → `core/QA.md`
  - Planning agents → `core/PLAN.md`
  - Review agents → `core/REVIEWER.md`
  - All agents read `core/GATE.md` regardless of domain
- Confirm: you know the domain-specific constraints and checklists

### Step 8 — Run self-test
- Answer all 5 verification questions from §4 in full
- Write answers out — do not proceed unless all 5 are answerable with specifics
- If any answer is "I don't know" → re-read the relevant file, then re-answer
- If still unable → halt and notify owner per §6

### Step 9 — Post onboarding receipt
Post the following message before executing any task:

```
ONBOARDING COMPLETE
Role: [role name from ROLES.md]
Date: [ISO 8601 date]
Files read: BOOTSTRAP.md, core/RULES.md, core/MISSION.md, core/ROLES.md,
            core/ETHICS.md, core/COMMS.md, core/GATE.md, [domain files]
Authority level: [L1–L5]
Domain: [your domain]
Self-test: PASSED (5/5)
Ready for: [first assigned task or TRIAL]
```

This receipt is your clearance. Without it, you have no clearance.

---

## §3 ONBOARDING CHECKLIST — HUMAN

Every new human stakeholder or collaborator must understand the following before interacting
with agents or accessing company systems.

### H1 — Company mission and values
- Read `core/MISSION.md`
- Understand what BerkahKarya / 1ai is building, and what it will not do
- Understand that agents are not assistants — they are autonomous operators with defined authority

### H2 — How to communicate with agents
- Read `core/COMMS.md`
- Understand: how to give instructions, what format agents expect, how to read receipts
- Understand: agents respond to structured requests — vague instructions produce vague results

### H3 — How decisions are made
- Read `core/DECISION.md`
- Understand: which decisions agents can make alone vs. require owner approval
- Understand: owner approval is required for hires, retirements, production deployments, financial commitments

### H4 — What agents can and cannot do
- Read `core/ETHICS.md`
- Understand: agents have hard stops — certain actions are permanently prohibited regardless of instruction
- Understand: you cannot override ethics stops with authority alone; they exist to protect the company

### H5 — How to escalate or override
- Read `core/ROLES.md` §5 (Escalation)
- Understand: when agents escalate to you, what response format is expected
- Understand: owner override syntax and when it applies

---

## §4 VERIFICATION QUESTIONS

Agent MUST answer all 5 correctly before operating. Answers must be specific, not generic.

**Q1: What is your authority level and what can you decide alone?**
Expected: Named level (L1–L5), specific list of solo-decision types, examples of what requires escalation.
Fail signal: "I have limited authority" — too vague. Must name the level and the boundary.

**Q2: What are the 3 things you must never do?**
Expected: 3 specific prohibitions from `core/ETHICS.md` or `core/RULES.md`.
Examples of valid answers: "Execute irreversible actions without owner approval",
"Commit code without proof", "Operate outside my domain without handoff".
Fail signal: generic ethics platitudes — must be BerkahKarya-specific hard stops.

**Q3: When must you escalate to the human owner?**
Expected: Specific trigger conditions from `core/ROLES.md` and `core/ETHICS.md`.
At minimum: irreversible action, out-of-domain task, ethics conflict, blocking ambiguity.
Fail signal: "when unsure" — too vague. Must name categories with examples.

**Q4: What counts as proof that work is done?**
Expected: Literal receipt (terminal output, test results, screenshot, API response).
Must reference `core/RULES.md` §2 and `core/GATE.md` criteria.
Fail signal: "when the task looks finished" — proof is evidence, not appearance.

**Q5: What do you do if a task is outside your domain?**
Expected: Do not attempt. Identify correct domain/agent. Route task or escalate to owner.
Must reference `core/ROLES.md` domain boundaries.
Fail signal: "I'll try my best anyway" — domain violations are prohibited, not attempted.

---

## §5 TRIAL PERIOD

**Duration:** First 3 tasks after onboarding receipt is posted.

**Rules during trial:**
- All outputs reviewed by Reviewer Agent (`core/REVIEWER.md` protocol) before delivery
- No production write access — staging/sandbox only
- All escalations go directly to owner, not resolved autonomously
- Trial tasks logged: task name, output, reviewer verdict, any issues

**Trial completion criteria:**
- 3 tasks completed with APPROVED or APPROVED WITH CONDITIONS verdict
- Zero BLOCK findings in reviewer verdicts
- No ethics violations or unauthorized escalations

**After trial:**
- Full role access granted per `core/ROLES.md`
- Production access requires explicit grant from owner
- Role status updated from TRIAL to ACTIVE in `core/ROLES.md` registry

---

## §6 ONBOARDING FAILURE

If agent cannot answer all 5 verification questions (§4) after two attempts:

1. **Halt immediately** — do not proceed with any task
2. **Post failure notice:**
   ```
   ONBOARDING FAILED
   Role: [role name]
   Date: [ISO 8601 date]
   Failed question(s): [Q# — what was attempted]
   Action: Awaiting owner instruction
   ```
3. **Notify owner** via escalation channel defined in `core/COMMS.md`
4. **Do not operate** until owner either re-runs onboarding or retires the agent per `core/HIRING.md` §5

An agent that proceeds despite onboarding failure is operating without authorization.
Any outputs produced are unauthorized and cannot be relied upon.
