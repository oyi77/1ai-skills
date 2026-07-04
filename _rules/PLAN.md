---
name: plan
version: 3.2.0
severity: mandatory
scope: [planning, decomposition]
pairs-with: [engineering, verification, gate]
description: Task decomposition, scoping, and planning — the gap between "I have a task" and "I'm writing code"
---

# PLAN.md — Task Decomposition & Scoping

> **The most expensive bug is building the wrong thing correctly.**
> Every task goes through decomposition BEFORE any code is written.

---

## §1 — WHY

AI agents have a strong bias toward action. Given a task, they immediately start coding. This produces: scope creep, wrong granularity, missing dependencies, wrong interpretation, no rollback path. This rule forces **5 minutes of thinking** before **5 hours of building.**

---

## §2 — THE DECOMPOSITION PROTOCOL

Before writing ANY code, the agent MUST complete this protocol. No exceptions.

### Step 1: Understand Intent, Then Restate

```
INTENT CLARIFICATION

What user SAID:   [exact request verbatim]
What user WANTS:  [actual goal / desired outcome]
Best solution:    [proposed approach — may differ from what user said]
Why:              [evidence: performance, cost, pattern, simplicity]

If proposed solution ≠ what user asked:
  → "You asked for X. I think Y is better because [reason]. OK?"
  → Let user decide. Don't silently change scope.

If unclear what user wants:
  → Ask. Don't guess and build wrong thing.

If request is clear AND unambiguous:
  → Don't stall. Restate briefly. Proceed.
```

### Step 2: Research Before Deciding

For STANDARD and COMPLEX tasks, research BEFORE scope classification. Do not assume you know the answer.

```
RESEARCH PHASE

Codebase:     [what currently exists related to this task — grep/read, not memory]
Prior art:    [how is this solved in the wild? docs, repos, patterns]
Constraints:  [what limits the solution? perf, security, compat, team convention]
Unknowns:     [what do I still not know? how will I find out?]
```

**Multi-agent research** (COMPLEX tasks or high uncertainty):
- Spawn parallel agents for independent research tracks
- Agent A: existing codebase — what's already there, what patterns are used
- Agent B: external — how do others solve this, what libraries exist, what are the tradeoffs
- Agent C: risk — what could go wrong, what are the failure modes, what does rollback look like
- Merge findings before proceeding to brainstorming
- Do NOT spawn agents for TRIVIAL tasks — overhead exceeds value

### Step 2.5: Write PRD + Create Atomic Issues (COMPLEX → mandatory, STANDARD → 1 issue min)

```
PRD & ISSUES

COMPLEX task?
  → Write PRD (see core/PRD.md §2 for template)
  → PRD must be approved (or self-approved with documented rationale) before decomposing
  → Decompose PRD into atomic issues (core/PRD.md §3 format)
  → Order issues by dependency — blocking issues first
  → One PR per issue — never bundle unrelated issues into one PR

STANDARD task?
  → Skip PRD
  → Create 1 issue per planned PR (core/PRD.md §3 format)

TRIVIAL task?
  → Skip PRD and issue — proceed directly to Step 3
```

Rules:
- No work starts without an issue for STANDARD/COMPLEX
- Each issue must have acceptance criteria before work begins
- Every PR must reference its issue (Closes #NNN)
- PR without issue reference → reviewer blocks merge

### Step 3: Brainstorm Approaches

Generate at least 3 approaches before picking one. Do not default to the first idea.

```
BRAINSTORM

Option A: [approach] → pros: [X] cons: [Y] complexity: S/M/L/XL
Option B: [approach] → pros: [X] cons: [Y] complexity: S/M/L/XL
Option C: [approach] → pros: [X] cons: [Y] complexity: S/M/L/XL

Eliminated: [option] because [concrete reason — not "seems harder"]
Selected:   [option] because [evidence-backed reason]
```

Rules:
- If only 1 option exists, document why alternatives were ruled out
- Do not pick the most familiar option by default — pick the best fit
- If options are unclear, research more before deciding

### Step 4: Scope Classification

```
SCOPE CLASSIFICATION

Touch count:     [files/modules]
New deps:        [yes/no — which?]
Interface:       [yes/no — API, schema, event, public function?]
Rollback:        [clear / unclear / impossible]

Classification (same as ENGINEERING.md §4):
  TRIVIAL   → 1 file, no interface change, no new deps, instant rollback
  STANDARD  → 2-5 files, local interface, no new deps, clear rollback
  COMPLEX   → ANY: >5 files · new dep · public interface · unclear rollback ·
               auth/security/infra · requires >1 PR
```

Scope → Max PR size → Review → Decomposition:
- TRIVIAL → 1 file → self-review → none
- STANDARD → ≤5 files, 1 PR → peer review → optional
- COMPLEX → multiple PRs → adversarial review → **MANDATORY**

### Step 5: Decompose (COMPLEX only)

```
DECOMPOSITION

PR 1: [what] → [unblocks] → files: [list]
PR 2: [what] → [unblocks] → files: [list]
PR 3: [what] → [unblocks] → files: [list]

Dependency graph: PR 1 → PR 2, PR 1 → PR 3 (PR 2, PR 3 parallel)

Each PR must: compile/test independently · be revertable without breaking others ·
              have single purpose · not leave system in broken intermediate state
```

### Step 6: Identify Risks

```
RISK ASSESSMENT

What could go wrong: [risk] → mitigation: [plan]
What I don't know:   [unknown] → how to find out: [action]
What could break:    [feature] → how to verify: [test]
```

### Step 7: Confirm Before Building

```
CONFIRMATION

Plan summary: [1-2 sentences]
PR count:     [N]
Scope:        [TRIVIAL/STANDARD/COMPLEX]
First PR:     [what to build first]
Ready?        [YES/NO — if NO, what's missing?]
```

---

## §3 — DECOMPOSITION HEURISTICS

**How to split:**
- Multiple unrelated changes → one PR per logical change
- New feature + refactor → separate PRs: refactor first, feature second
- Schema change + code using it → PR 1: schema+migration. PR 2: code.
- API + frontend → PR 1: API. PR 2: frontend (behind feature flag)
- Bug fix + test → same PR (inseparable)
- Config change + reader → PR 1: code reads old+new. PR 2: switch config. PR 3: remove old.

**Anti-patterns:**
- "Add payment system" in one PR → schema/API/frontend in separate PRs
- PR depends on unmerged PR → rebase or restructure for independence
- "Refactor while I'm at it" → separate refactor PR before feature
- "It's simple, skip decomposition" → 30-second scope check still needed
- 20 tiny PRs → 3-5 is sweet spot

---

## §4 — SCOPE ESCALATION LADDER

When scope grows mid-task:
1. STOP building
2. Document what changed: original scope → discovered scope → delta
3. Re-classify: TRIVIAL → STANDARD → COMPLEX
4. If COMPLEX → decompose NOW (don't keep building)
5. Inform user with evidence
6. Continue with new plan
🚫 Never silently absorb scope creep into current PR.

---

## §5 — ESTIMATION (optional)

```
PR 1: [desc] → ~[N] files, ~[N] hours
PR 2: [desc] → ~[N] files, ~[N] hours
Total: ~[N] PRs, ~[N] hours. Confidence: HIGH/MEDIUM/LOW.
```

Rules: Never promise unverifiable timelines. "I don't know" is honest. Multiply first estimate ×2. If >1 day, break down further.

---

## §6 — INTEGRATION WITH CORE LOOP

```
1. READ     → §1 MCP sequence
2. THINK    → §3 Think-Before-Decide
2.1 DECOMPOSE → THIS RULE (PLAN.md) — break task into PRs
3. DECIDE   → Choice + evidence + rollback trigger
4. PLAN     → SOLID/KISS design per PR
5. BUILD    → Build PR 1, verify, merge. Then PR 2. Then PR 3.
```

Decomposition is **MANDATORY** for COMPLEX. TRIVIAL: 5-second mental check.

---

> 💡 *"The best code is the code you don't write in the wrong PR."*
> 🚫 *"Building without decomposing is driving without a map."*
