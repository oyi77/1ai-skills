# Agent Daily Planner

A structured daily planning and execution tracking system for AI agents that helps organize tasks, track shipped work, and maintain accountability across sessions.

## What It Does

- Generates daily plans based on yesterday's unfinished tasks, active projects, and deadlines
- Creates structured daily log templates in `memory/YYYY-MM-DD.md`
- Tracks shipped work, blockers, and completion rates
- Generates weekly summaries and standup formats
- Persists context across sessions to avoid re-orientation time

## Quick Usage

```bash
# At session start
/plan today

# When you complete something
/plan ship "Published skill-auditor on ClawHub"

# Log a blocker
/plan block "Post Bridge SSL broken" George

# Before session end
/plan review

# Weekly reflection
/plan week
```

## Key Features

- **Persistent Planning**: Never lose track of tasks between sessions
- **Accountability Tracking**: See completion rates and shipped work over time
- **Standup Format**: Ready-made status updates for humans
- **Weekly Summaries**: Track progress, trends, and decisions
- **Blocker Management**: Tag blockers with who can resolve them
- **Carry-Forward**: Automatically brings unfinished tasks to tomorrow

## Integration

Works with existing memory system:
- `memory/YYYY-MM-DD.md` — Daily logs
- `memory/projects.json` — Active projects (optional)
- `memory/weekly/YYYY-Wxx.md` — Weekly summaries

Doesn't modify files it doesn't own. Reads from MEMORY.md and previous daily logs.

## Keywords

productivity, planning, tasks, accountability, workflow