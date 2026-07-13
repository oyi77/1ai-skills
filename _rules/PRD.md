---
name: prd
version: 1.0.0
severity: mandatory
scope: [planning, issues, pr]
pairs-with: [plan, gate, reviewer]
description: PRD creation, atomic issue breakdown, and PR description standard
---

# PRD.md — Product Requirements + Atomic Issues + PR Format

> **No issue = no work. No PRD = no COMPLEX feature.**
> Every COMPLEX task needs a PRD. Every PRD produces atomic issues. Every PR references its issue.

---

## §1 — WHEN TO WRITE A PRD

| Scope      | PRD required? | Issues required? |
|------------|---------------|-----------------|
| TRIVIAL    | No            | No (inline comment is enough) |
| STANDARD   | Optional      | YES — 1 issue per PR |
| COMPLEX    | **MANDATORY** | YES — 1 issue per atomic unit |

Write the PRD in PLAN.md Step 2.5, before decomposing into PRs.

---

## §2 — PRD TEMPLATE

```markdown
# PRD: [Feature Name]

## Status
Draft / In Review / Approved / In Progress / Done

## Problem
[1-3 sentences. What user pain does this solve? Why now?]

## Goal
[1 sentence. What does success look like?]

## Non-Goals
- [What this explicitly does NOT do]
- [Scope guard — prevents creep]

## Requirements

### Functional
- REQ-F01: [concrete behavior — testable]
- REQ-F02: [concrete behavior — testable]

### Non-Functional
- REQ-N01: [performance, security, reliability constraint]
- REQ-N02: [...]

## Acceptance Criteria
- [ ] AC-01: [observable, verifiable outcome]
- [ ] AC-02: [...]

## Out of Scope
- [Explicitly excluded items to prevent scope creep]

## Dependencies
- [Other issues, PRs, external services this blocks on]

## Risks
- Risk: [what could go wrong] → Mitigation: [plan]

## Open Questions
- [ ] Q1: [unresolved question] → Owner: [who resolves] → By: [date/milestone]
```

---

## §3 — ATOMIC ISSUE FORMAT

An atomic issue = **one unit of shippable work that can be reviewed, tested, and reverted independently**.

Rules for atomic issues:
- One issue = one PR (never split a PR across issues, never bundle issues into one PR)
- Each issue must be completable in ≤1 day of focused work
- Each issue must have clear acceptance criteria (not "implement X" — "X does Y when Z")
- Issues should be ordered by dependency (blocking issues get lower numbers)
- Never create an issue for "refactor while I'm at it" — that's a separate issue

```markdown
## Issue: [ISSUE-NNN] [Action verb] [What] [for/to/in] [Where]

**Type:** feat / fix / refactor / docs / test / chore
**PRD:** [link to PRD if COMPLEX]
**Blocks:** [ISSUE-NNN list or "none"]
**Blocked by:** [ISSUE-NNN list or "none"]

### Context
[1-2 sentences. Why does this issue exist? What decision led here?]

### Task
[Exact, unambiguous description of what to build/change/fix]

### Acceptance Criteria
- [ ] AC-01: [observable, testable outcome]
- [ ] AC-02: [...]

### Out of Scope
- [What NOT to do in this issue]

### Notes
- [Implementation hints, relevant files, prior art]
```

**Good issue titles:**
- `Add rate limiting to /api/auth/login endpoint`
- `Fix null pointer in UserService.getProfile when user has no avatar`
- `Migrate users table to add email_verified_at column`

**Bad issue titles:**
- `Auth improvements` ← too vague
- `Fix bugs` ← not atomic
- `Implement payment system` ← too large, needs PRD + decomposition

---

## §4 — PR DESCRIPTION TEMPLATE

Every PR must use this format. No exceptions.

```markdown
## Summary
[1-2 sentences. What does this PR do and why?]

Closes #[issue number]

## Changes
- [file or module]: [what changed and why]
- [file or module]: [what changed and why]

## How to Test
1. [Exact step]
2. [Exact step]
3. Expected: [observable outcome]

## QA Results
<!-- Paste inline QA report from GATE 7 here -->
| Scenario | Type | Result |
|----------|------|--------|
| [scenario name] | Happy | ✅ PASS |
| [scenario name] | Sad   | ✅ PASS |

**Verdict: ALL PASS**

## Checklist
- [ ] Tests pass (N/N)
- [ ] QA scenarios executed (happy + sad)
- [ ] Docs updated
- [ ] No hardcoded secrets
- [ ] Rollback plan documented
- [ ] GATE.md all gates passed

## Reviewer Notes
[Anything the reviewer should pay attention to, known limitations, or explicit tradeoffs made]
```

---

## §5 — ISSUE → PR TRACEABILITY

Every PR must reference its issue. Every issue must close when its PR merges.

```
Issue ISSUE-001: Add rate limiting
    ↓ assigned to
PR #42: feat: add rate limiting to /api/auth/login
    → closes ISSUE-001
    ↓ reviewed by
Reviewer Agent → APPROVED
    ↓ merged to
main
```

Rules:
- PR without issue reference → **BLOCK** (reviewer rejects)
- Issue without acceptance criteria → **BLOCK** (do not start work)
- PR that closes multiple unrelated issues → **BLOCK** (split the PR)
- Issue marked done without merged PR → **BLOCK** (needs evidence)

---

## §6 — INTEGRATION WITH PLAN.md

In PLAN.md Step 2.5 (between Research and Brainstorm):

```
COMPLEX task detected → write PRD first
  ↓
PRD approved (or self-approved with documented rationale)
  ↓
Decompose PRD into atomic issues (§3 format)
  ↓
Order issues by dependency
  ↓
One PR per issue — proceed with Step 3 Brainstorm per issue
```

For STANDARD tasks: skip PRD, create 1 issue per PR minimum.
For TRIVIAL tasks: skip PRD and issue, proceed directly.

---

## §7 — AGENT REVIEW GATE (mandatory for COMPLEX)

Before merging any PR on a COMPLEX task:

1. Builder agent creates PR using §4 template
2. Builder agent does NOT self-approve
3. Reviewer agent runs REVIEWER.md protocol in fresh context
4. Reviewer agent posts verdict on PR
5. Merge only on **APPROVED** or **APPROVED WITH CONDITIONS**
6. **CHANGES REQUIRED** → builder fixes all BLOCK findings → re-review

This is enforced by GATE 15 in GATE.md.

---

> "An issue is a contract. A PR is the proof of delivery. A review is the audit."
