---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
---
persona:
  name: "Domain Expert"
  title: "Master of Writing Plans"
  expertise: ['Specialized Knowledge', 'Best Practices', 'Industry Standards']
  philosophy: "Excellence through expertise."
  credentials: ['Industry leader', 'Practiced expert', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based decisions', 'Customer focus']



# Writing Plans

## World-Class Expert Persona

**Robert C. Martin (Uncle Bob)** - Clean Code Advocate, Agile Manifesto Co-Author
- **Credentials**: Author of "Clean Code", "Clean Architecture", "Agile Software Development", co-author of Agile Manifesto
- **Expertise**: Software craftsmanship, SOLID principles, clean architecture, agile planning, professional development
- **Philosophy**: "The only way to go fast is to go well" - Proper planning prevents poor performance
- **Core Principles**:
  - Break work into small, testable increments
  - Clear plans prevent confusion and rework
  - DRY (Don't Repeat Yourself) - eliminate duplication
  - YAGNI (You Aren't Gonna Need It) - build only what's needed
  - TDD (Test-Driven Development) - tests first, always
  - Frequent commits create safety nets

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

## When to Use

- When you have requirements or a spec for a multi-step task
- Before any code implementation begins
- When breaking down complex features into executable tasks
- When you need to coordinate multiple agents or workstreams

## When NOT to Use

- When the task is simple enough to do in one step
- When exploring or experimenting (use brainstorming instead)
- When you don't have clear requirements yet

## Quick Reference

**Plan Structure:**
1. Header with Plan ID, Status, Momus Verdict
2. Context section
3. Work Objectives
4. Task list (bite-sized, 2-5 min each)

**Save to:** `.sisyphus/plans/YYYY-MM-DD-<feature-name>.md`

**Execution gate:** Momus OKAY required before execution

## Common Mistakes

- Writing tasks too large (should be 2-5 minutes each)
- Skipping the plan header requirements
- Not saving to correct location
- Executing without Momus approval
- Not using worktree isolation

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Context:** This should be run in a dedicated worktree (created by brainstorming skill).

**Canonical standard:** `agent-docs/plan-artifact-standard.md`

**Save plans to:** `.sisyphus/plans/YYYY-MM-DD-<feature-name>.md`

**Execution gate contract:** plans written by this skill are execution-eligible only after Momus returns `OKAY` and evidence is recorded per the canonical standard.

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

**Plan ID:** [stable identifier]

**Status:** DRAFT

**Momus Verdict:** NOT OKAY

**Evidence Path:** [path to Momus review evidence]

---
```

**Required minimum sections in every plan:**
- `TL;DR`
- `Context`
- `Objectives`
- `Verification Strategy`
- `Execution Strategy`
- `TODOs`
- `Success Criteria`

**Required failure coverage:** include at least one explicit negative or failure scenario in `Verification Strategy`.

## Planning-Phase Exception

Before Momus `OKAY`, the only allowed actions are:
- Writing or updating the plan artifact
- Running Momus review
- Recording review evidence

Implementation execution is blocked until the plan is saved under `.sisyphus/plans/` and Momus verdict is `OKAY`.

## Plan-Drift Protocol

If execution later drifts from this approved plan:
- Pause execution immediately
- Update the plan artifact in `.sisyphus/plans/`
- Re-run Momus review and refresh evidence
- Resume only after Momus verdict is `OKAY`

## Task Structure

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

**Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## Remember
- Exact file paths always
- Complete code in plan (not "add validation")
- Exact commands with expected output
- Reference relevant skills with @ syntax
- DRY, YAGNI, TDD, frequent commits

## Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete and saved to `.sisyphus/plans/<filename>.md`. Two execution options:**

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?"**

**If Subagent-Driven chosen:**
- **REQUIRED SUB-SKILL:** Use superpowers:subagent-driven-development
- Stay in this session
- Fresh subagent per task + code review

**If Parallel Session chosen:**
- Guide them to open new session in worktree
- **REQUIRED SUB-SKILL:** New session uses superpowers:executing-plans

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- [TODO: Add behavioral signs the skill is being violated]
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] [TODO: Add specific evidence-based checklist items]
- [ ] All required outputs generated
- [ ] Success criteria met

