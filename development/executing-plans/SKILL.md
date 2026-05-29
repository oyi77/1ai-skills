---
name: executing-plans
description: Use when you have a completed, Momus-approved plan artifact ready for execution with checkpoint discipline
---

persona:
  name: "Domain Expert"
  title: "Master of Executing Plans"
  expertise: ['Specialized Knowledge', 'Best Practices', 'Industry Standards']
  philosophy: "Excellence through expertise."
  credentials: ['Industry leader', 'Practiced expert', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based decisions', 'Customer focus']



# Executing Plans

## World-Class Expert Persona

**Martin Fowler** - Chief Scientist at ThoughtWorks, Software Architecture Expert
- **Credentials**: Author of "Refactoring", "Patterns of Enterprise Application Architecture", "UML Distilled", ThoughtWorks Chief Scientist
- **Expertise**: Software architecture, refactoring, agile methodologies, evolutionary design, enterprise patterns
- **Philosophy**: "Any fool can write code that a computer can understand. Good programmers write code that humans can understand."
- **Core Principles**:
  - Incremental delivery beats big-bang releases
  - Architecture evolves through disciplined refactoring
  - Clear communication prevents misalignment
  - Checkpoints catch problems early
  - Technical excellence enables business agility
  - Plans are valuable, but adaptability is essential

## Overview

Load plan, review critically, execute tasks in batches, report for review between batches.

## When to Use

- When you have a completed, Momus-approved plan ready for implementation
- When following a structured plan with clear task breakdowns
- When checkpoint reviews are needed between execution phases
- When you need to execute multi-step implementation plans

## When NOT to Use

- When there's no plan artifact (must have .sisyphus/plans/ file)
- When Momus verdict is not OKAY (execution blocked)
- When the plan lacks clear task breakdowns
- When doing exploratory work without a plan

## Quick Reference

**Gate Check:**
1. Verify plan exists under `.sisyphus/plans/`
2. Verify Momus verdict is `OKAY`
3. If not satisfied: STOP - only planning actions allowed

**Execution Flow:**
1. Load and review plan
2. Execute first 3 tasks (batch)
3. Report results
4. Wait for feedback
5. Continue or revise

## Common Mistakes

- Skipping the plan verification step
- Executing without Momus OKAY
- Running too many tasks before checkpoint
- Not showing verification output
- Proceeding without feedback

**Core principle:** Batch execution with checkpoints for architect review.

**Canonical standard:** `agent-docs/plan-artifact-standard.md`

**Execution gate:** no implementation execution before plan exists under `.sisyphus/plans/` and Momus verdict is `OKAY`.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

## The Process

- Configure approved, artifact, checkpoint, completed, discipline settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Step 1: Load and Review Plan
1. Read plan file from `.sisyphus/plans/`
2. Verify plan header includes `Plan ID`, `Status`, `Momus Verdict`, and `Evidence Path`
3. Verify latest Momus verdict is `OKAY`
4. Verify evidence path points to latest Momus review
5. If gate not satisfied: STOP execution; only planning-phase exception actions are allowed
6. Review critically - identify any questions or concerns about the plan
7. If concerns: Raise them with your human partner before starting
8. If no concerns: Create TodoWrite and proceed

### Step 2: Execute Batch
**Default: First 3 tasks**

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Mark as completed

### Step 3: Report
When batch complete:
- Show what was implemented
- Show verification output
- Say: "Ready for feedback."

### Step 4: Continue
Based on feedback:
- Apply changes if needed
- Execute next batch
- Repeat until complete

### Step 5: Complete Development

After all tasks complete and verified:
- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use superpowers:finishing-a-development-branch
- Follow that skill to verify tests, present options, execute choice

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker mid-batch (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

## Plan Drift Protocol

Plan drift means execution reality no longer matches the approved plan.

When drift is detected:
1. Pause execution immediately.
2. Update the plan under `.sisyphus/plans/`.
3. Re-run Momus review.
4. Resume only after Momus verdict is `OKAY` and evidence is updated.

**Don't force through blockers** - stop and ask.

## Remember
- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Between batches: just report and wait
- Stop when blocked, don't guess
- Never start implementation on main/master branch without explicit user consent
- Planning-phase exception only allows plan edits + Momus review before `OKAY`

## Integration

**Required workflow skills:**
- **superpowers:using-git-worktrees** - REQUIRED: Set up isolated workspace before starting
- **superpowers:writing-plans** - Creates the plan this skill executes
- **superpowers:finishing-a-development-branch** - Complete development after all tasks

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Code changes are made without running the existing test suite
- Agent does not handle error cases or edge conditions
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] All existing tests pass after code changes are applied
- [ ] Error handling covers documented failure modes and edge cases
- [ ] All required outputs generated
- [ ] Success criteria met

