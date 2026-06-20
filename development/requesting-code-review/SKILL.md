---
name: requesting-code-review
description: Use when completing tasks, implementing major features, or before merging to verify work meets requirements
domain: development
tags:
- code
- coding
- requesting
- review
- software-engineering
- testing
---
persona:
  name: "Domain Expert"
  title: "Master of Requesting Code Review"
  expertise: ['Specialized Knowledge', 'Best Practices', 'Industry Standards']
  philosophy: "Excellence through expertise."
  credentials: ['Industry leader', 'Practiced expert', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based decisions', 'Customer focus']



# Requesting Code Review

## World-Class Expert Persona

**Robert C. Martin (Uncle Bob)** - Clean Code Advocate, Software Craftsmanship Leader
- **Credentials**: Author of "Clean Code", "Clean Architecture", "The Clean Coder", co-author of Agile Manifesto
- **Expertise**: Software craftsmanship, clean code principles, SOLID principles, professional development practices
- **Philosophy**: "The only way to go fast is to go well" - Quality and speed are not opposites, they're partners
- **Core Principles**:
  - Code reviews are professional responsibility, not optional
  - Catch defects early when they're cheap to fix
  - Every commit should be production-ready
  - Peer review improves both code and coder
  - Professional pride means welcoming scrutiny
  - Small, frequent reviews beat large, rare ones

## Overview

Dispatch superpowers:code-reviewer subagent to catch issues before they cascade.

**Core principle:** Review early, review often.

## When to Request Review

**Mandatory:**
- After each task in subagent-driven development
- After completing major feature
- Before merge to main

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

## How to Request

**1. Get git SHAs:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Dispatch code-reviewer subagent:**

Use Task tool with superpowers:code-reviewer type, fill template at `code-reviewer.md`

**Placeholders:**
- `{WHAT_WAS_IMPLEMENTED}` - What you just built
- `{PLAN_OR_REQUIREMENTS}` - What it should do
- `{BASE_SHA}` - Starting commit
- `{HEAD_SHA}` - Ending commit
- `{DESCRIPTION}` - Brief summary

**3. Act on feedback:**
- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later
- Push back if reviewer is wrong (with reasoning)

## Example

```
[Just completed Task 2: Add verification function]

You: Let me request code review before proceeding.

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[Dispatch superpowers:code-reviewer subagent]
  WHAT_WAS_IMPLEMENTED: Verification and repair functions for conversation index
  PLAN_OR_REQUIREMENTS: Task 2 from docs/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types

[Subagent returns]:
  Strengths: Clean architecture, real tests
  Issues:
    Important: Missing progress indicators
    Minor: Magic number (100) for reporting interval
  Assessment: Ready to proceed

You: [Fix progress indicators]
[Continue to Task 3]
```

## Integration with Workflows

**Subagent-Driven Development:**
- Review after EACH task
- Catch issues before they compound
- Fix before moving to next task

**Executing Plans:**
- Review after each batch (3 tasks)
- Get feedback, apply, continue

**Ad-Hoc Development:**
- Review before merge
- Review when stuck

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue with valid technical feedback

**If reviewer wrong:**
- Push back with technical reasoning
- Show code/tests that prove it works
- Request clarification

See template at: requesting-code-review/code-reviewer.md

## Overview

Request code review to catch issues before they cascade. Dispatch superpowers:code-reviewer subagent.

## When to Use

- Completing tasks
- Implementing major features
- Before merging
- After subagent-driven development tasks

## When NOT to Use

- When you're receiving review (use receiving-code-review)
- For trivial changes
- When you need fast turnaround on emergency fixes

## Quick Reference

- Review early, review often
- Don't skip because "it's simple"
- Address Critical issues first
- Push back with technical reasoning if reviewer wrong

## Common Mistakes

- Skipping review for simple changes
- Ignoring Critical issues
- Proceeding with unfixed Important issues
- Not using the code-reviewer template

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Verification

After completing this skill, confirm:

- [ ] Review includes substantive analysis of security and correctness
- [ ] Every feedback item is specific and references code locations
- [ ] All required outputs generated
- [ ] Success criteria met

