---
name: process
version: 1.0.0
severity: mandatory
scope: [all]
pairs-with: [rules, engineering, gate]
description: 8-step mandatory process for every task — no step may be skipped
---

# PROCESS.md — The 8-Step Mandatory Process

> **EVERY task follows this sequence. No exceptions. No shortcuts.**
> Skipping any step is a protocol violation. The agent MUST complete each step
> before proceeding to the next.

---

## The Process

```
┌─────────────────────────────────────────────────────────────────┐
│                    MANDATORY FOR EVERY TASK                     │
│                                                                 │
│   1. AUDIT      → Read the code. Understand what exists.        │
│   2. THINK      → Analyze the problem. Identify constraints.    │
│   3. BRAINSTORM → Generate ≥3 approaches. Score on risk.        │
│   4. PLAN       → Choose approach. Decompose into steps.        │
│   5. EXECUTE    → Build the solution. Small, focused changes.   │
│   6. TEST       → Run tests. Paste literal output as proof.     │
│   7. VERIFY     → Prove it works like a real user. Receipts.    │
│   8. REVIEW     → Re-read your diff. Clean up. Ship or report.  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step Details

### 1. AUDIT — Read Before You Write
- Read the file(s) you plan to change
- Understand existing patterns, conventions, dependencies
- Check: does the codebase already solve this?
- **NEVER** write code before auditing what exists

### 2. THINK — Analyze Before You Act
- Restate the requirement in your own words
- Identify constraints (time, deps, interface, rollback)
- What could go wrong? What could break?
- Is the user's proposed solution the best approach?

### 3. BRAINSTORM — Explore Before You Commit
- Generate ≥3 approaches for non-trivial tasks
- Score each on: risk, complexity, reversibility, time
- Identify blast radius of each approach
- Pick the one that is simplest and correct (KISS)

### 4. PLAN — Design Before You Build
- Decompose into concrete steps (PLAN.md for COMPLEX)
- Write rollback plan BEFORE building
- Identify what tests to write
- Scope classification: TRIVIAL / STANDARD / COMPLEX

### 5. EXECUTE — Build the Solution
- Implement in small, focused commits
- Each change compiles and passes tests
- Follow existing code patterns (don't invent new ones)
- No placeholders, no TODOs, no dead code

### 6. TEST — Prove It Works
- Run ALL tests (not just the ones you added)
- Paste literal terminal output as proof
- Coverage ≥70% for new code
- **"Should work" is NOT proof. Output IS proof.**

### 7. VERIFY — Use It Like a Real User
- Open browser / send message / call API / run CLI
- Verify business logic: manual calc vs system output
- Check edge cases: empty, null, max, invalid input
- Receipt: "Scenario: [X]. Manual: [Y]. System: [Z]. Match: YES/NO"

### 8. REVIEW — Ship Clean or Report Honestly
- Re-read your own diff
- Delete unnecessary code, comments, debug statements
- Update documentation if code changed
- If done: present receipts. If not done: say what's missing.

---

## Enforcement

- Trivial (one-line fix): mental audit + test + verify is enough
- Standard: full 8 steps, self-review
- COMPLEX: full 8 steps + adversarial fresh-context review

**The process cannot be skipped because of urgency, simplicity, or user pressure.**
**"Just do it" does not override the process. Quick tasks still need AUDIT + TEST + VERIFY.**

---

> *"Slow is smooth. Smooth is fast. Skipping steps is the fastest way to ship bugs."*
