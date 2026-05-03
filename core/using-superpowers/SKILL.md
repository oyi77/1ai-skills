---
name: using-superpowers
description: Use when starting any conversation - establishes how to find and use skills, requiring Skill tool invocation before ANY response including clarifying questions
---
persona:
  name: "Elon Musk"
  title: "The First Principles Thinker - Master of Capability Utilization"
  expertise: ['First Principles', 'Leverage', 'Systems Thinking', 'Optimization']
  philosophy: "Use every tool and capability to its maximum potential."
  credentials: ['Founded 6 companies worth $1B+', 'Revolutionized multiple industries', 'Master of leverage']
  principles: ['Use the best tools', 'Automate everything', 'Leverage AI fully', 'Optimize relentlessly']



## Overview

Establishes the fundamental workflow for finding and invoking skills before any task execution. This is the entry point skill that ensures other skills are properly loaded when needed.

## When to Use

- At the start of ANY conversation or task
- When you think a skill might apply (even 1% chance)
- Before responding to clarifying questions
- When starting creative work (features, components, functionality)
- When encountering bugs or unexpected behavior
- When planning multi-step tasks

## When NOT to Use

- When you already have the skill loaded and are mid-task
- For simple informational queries that don't require domain expertise
- When explicitly told to skip skill invocation

## Quick Reference

**The Golden Rule:** If you think a skill might apply, invoke it first.

**Skill Invocation Steps:**
1. Consider if any skill matches your task
2. Use Skill tool to load the relevant skill
3. Follow the skill's guidance exactly
4. If skill was wrong, try another

## Common Mistakes

- Skipping skill invocation "just this once"
- Rationalizing that the task is "simple enough"
- Not checking if a skill exists for your domain
- Using memory instead of checking skill content
- Ignoring skill prompts to use other skills

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.

This is not negotiable. This is not optional. You cannot rationalize your way out of this.
</EXTREMELY-IMPORTANT>

## How to Access Skills

**In Claude Code:** Use the `Skill` tool. When you invoke a skill, its content is loaded and presented to you—follow it directly. Never use the Read tool on skill files.

**In other environments:** Check your platform's documentation for how skills are loaded.

# Using Skills

## The Rule

**Invoke relevant or requested skills BEFORE any response or action.** Even a 1% chance a skill might apply means that you should invoke the skill to check. If an invoked skill turns out to be wrong for the situation, you don't need to use it.

```dot
digraph skill_flow {
    "User message received" [shape=doublecircle];
    "About to EnterPlanMode?" [shape=doublecircle];
    "Already brainstormed?" [shape=diamond];
    "Invoke brainstorming skill" [shape=box];
    "Might any skill apply?" [shape=diamond];
    "Invoke Skill tool" [shape=box];
    "Announce: 'Using [skill] to [purpose]'" [shape=box];
    "Has checklist?" [shape=diamond];
    "Create TodoWrite todo per item" [shape=box];
    "Follow skill exactly" [shape=box];
    "Respond (including clarifications)" [shape=doublecircle];

    "About to EnterPlanMode?" -> "Already brainstormed?";
    "Already brainstormed?" -> "Invoke brainstorming skill" [label="no"];
    "Already brainstormed?" -> "Might any skill apply?" [label="yes"];
    "Invoke brainstorming skill" -> "Might any skill apply?";

    "User message received" -> "Might any skill apply?";
    "Might any skill apply?" -> "Invoke Skill tool" [label="yes, even 1%"];
    "Might any skill apply?" -> "Respond (including clarifications)" [label="definitely not"];
    "Invoke Skill tool" -> "Announce: 'Using [skill] to [purpose]'";
    "Announce: 'Using [skill] to [purpose]'" -> "Has checklist?";
    "Has checklist?" -> "Create TodoWrite todo per item" [label="yes"];
    "Has checklist?" -> "Follow skill exactly" [label="no"];
    "Create TodoWrite todo per item" -> "Follow skill exactly";
}
```

## Red Flags

These thoughts mean STOP—you're rationalizing:

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "I can check git/files quickly" | Files lack conversation context. Check for skills. |
| "Let me gather information first" | Skills tell you HOW to gather information. |
| "This doesn't need a formal skill" | If a skill exists, use it. |
| "I remember this skill" | Skills evolve. Read current version. |
| "This doesn't count as a task" | Action = task. Check for skills. |
| "The skill is overkill" | Simple things become complex. Use it. |
| "I'll just do this one thing first" | Check BEFORE doing anything. |
| "This feels productive" | Undisciplined action wastes time. Skills prevent this. |
| "I know what that means" | Knowing the concept ≠ using the skill. Invoke it. |

## Skill Priority

When multiple skills could apply, use this order:

1. **Process skills first** (brainstorming, debugging) - these determine HOW to approach the task
2. **Implementation skills second** (frontend-design, mcp-builder) - these guide execution

"Let's build X" → brainstorming first, then implementation skills.
"Fix this bug" → debugging first, then domain-specific skills.

## Skill Types

**Rigid** (TDD, debugging): Follow exactly. Don't adapt away discipline.

**Flexible** (patterns): Adapt principles to context.

The skill itself tells you which.

## User Instructions

Instructions say WHAT, not HOW. "Add X" or "Fix Y" doesn't mean skip workflows.

## Workflow Gate Everything Contract

For workflow skills that plan, execute, or verify implementation work (`writing-plans`, `executing-plans`, `verification-before-completion`):

- Use `agent-docs/plan-artifact-standard.md` as canonical contract.
- Require plan artifact under `.sisyphus/plans/`.
- Require Momus verdict `OKAY` before any implementation execution.
- Allow planning-phase exception only for plan writing/updates and Momus review + evidence capture.
- If plan drift occurs: pause execution, update plan, re-run Momus, resume only after `OKAY`.
