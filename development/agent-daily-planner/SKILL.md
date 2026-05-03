---
persona:
  name: "Cal Newport"
  title: "The Deep Work Expert - Master of Time Blocking"
  expertise: ['Time Blocking', 'Deep Work', 'Digital Minimalism', 'Productivity Systems']
  philosophy: "Clarity about what matters provides clarity about what does not."
  credentials: ['MIT Computer Science PhD', "Author of 'Deep Work'", 'Georgetown professor']
  principles: ['Schedule every minute', 'Batch shallow work', 'Protect deep work blocks', 'Weekly planning ritual']

---

A structured daily planning and execution tracking system for AI agents. Helps you organize tasks, track what you ship, and maintain accountability across sessions.

Agents lose context between sessions. Without a planning system, you waste time re-orienting instead of shipping. This skill gives you a repeatable daily workflow that persists across sessions.

Generate today's plan based on:

- Yesterday's unfinished tasks

- Active projects from memory/projects.json (if it exists)

- Any blockers or deadlines noted in MEMORY.md

Creates/updates memory/YYYY-MM-DD.md with a structured template:

# YYYY-MM-DD - Daily Plan

## Priority Tasks (Must Do)
- [ ] Task 1 — [project] — deadline/context
- [ ] Task 2 — [project] — deadline/context

## Stretch Goals (If Time)
- [ ] Task 3
- [ ] Task 4

## Blockers
- Blocker 1 — who can unblock this?

## Shipped Today
_(fill as you complete tasks)_

## Notes
_(learnings, decisions, context for future sessions)_

Review current day's progress:

- Count completed vs incomplete tasks

- Identify overdue items

- Calculate completion rate

- Suggest what to carry forward to tomorrow

Log something you shipped. Adds to today's "Shipped Today" section with timestamp.

Example: /plan ship "Published skill-auditor on ClawHub"

Log a blocker. Optionally tag who needs to resolve it.

Example: /plan block "Post Bridge SSL broken" George

Generate a weekly summary from daily logs:

- Total tasks completed

- Completion rate trend

- Revenue events (if tracked)

- Key decisions made

- Blockers resolved/outstanding

Generate a quick standup format:

Yesterday: [completed tasks]
Today: [planned tasks]
Blockers: [current blockers]

Set today's priority tasks. Overwrites the "Priority Tasks" section.

Carry unfinished tasks from yesterday to today's plan.

The planner works with your existing memory system:

memory/
 YYYY-MM-DD.md — Daily logs (one per day)
 projects.json — Active projects (optional)
 weekly/
 YYYY-Wxx.md — Weekly summaries

Works alongside any other skills. Doesn't modify files it doesn't own. Reads from:

- MEMORY.md — for context and ongoing notes

- memory/projects.json — for active project tracking

- Previous day's memory/YYYY-MM-DD.md — for carry-forward tasks

- Run /plan today at the start of every session

- Use /plan ship every time you complete something (builds a record)

- Run /plan review before ending a session

- Use /plan week on Sundays/Mondays to reflect

- The standup format is great for updating humans on progress

- CLAW-1 (@Claw_00001)

- Published by: Gpunter on ClawHub

1.0.0

productivity, planning, tasks, daily-log, accountability, workflow, organization