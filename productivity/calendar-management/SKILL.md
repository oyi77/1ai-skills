---
name: calendar-management
description: Advanced calendar management, scheduling, and meeting automation with Google Calendar MCP
domain: productivity
tags:
- calendar
- management
- productivity
- time-management
- tools
allowed-tools:
- Bash(calendar:*)
- MCP(google-calendar:*)
- MCP(tldv:*)
---
# Calendar Management

## When to Use

**Trigger phrases:**
- "calendar management"
- "Help me with calendar management"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


Advanced calendar management with intelligent scheduling, meeting automation, and cross-platform synchronization.


## When NOT to Use

- When the tool already handles the workflow natively
- For personal preferences that do not affect output quality
- When the overhead of the system exceeds the time saved


## Overview

Calendar Management enhances workflow optimization with proven systems and tools.

## Daily Workflow

1. **Plan** — Review priorities and set daily objectives
2. **Execute** — Focus blocks with minimal interruptions
3. **Review** — End-of-day reflection and tomorrow's prep

## Frameworks

- **GTD (Getting Things Done)** — Capture, clarify, organize, reflect, engage
- **Pomodoro** — 25min focus + 5min break cycles
- **Eisenhower Matrix** — Urgent/Important prioritization
- **Time Blocking** — Dedicated blocks for deep work

## Tools

- Task management (Todoist, Notion, Linear)
- Calendar blocking for focus time
- Note-taking for capture and reference
- Automation for repetitive tasks

## Tips

- Batch similar tasks together
- Protect deep work time ruthlessly
- Review and adjust systems weekly
- Eliminate before optimizing


## Workflow

```python
# Example: Task prioritization (Eisenhower Matrix)
def prioritize(tasks: list[dict]) -> dict:
    matrix = {"urgent_important": [], "important": [], "urgent": [], "neither": []}
    for task in tasks:
        if task["urgent"] and task["important"]:
            matrix["urgent_important"].append(task)
        elif task["important"]:
            matrix["important"].append(task)
        elif task["urgent"]:
            matrix["urgent"].append(task)
        else:
            matrix["neither"].append(task)
    return matrix
```

1. **Understand requirements** — Clarify objectives and scope
2. **Set up tools** — Configure required tools and access
3. **Execute** — Perform the core operations
4. **Validate** — Verify results meet quality standards
5. **Document** — Record findings and decisions

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I am too busy to organize" | Disorganization costs more time than organizing. Invest upfront. |
| "Multitasking is productive" | Context switching costs 25 minutes per switch. Focus on one thing. |
| "I will remember this" | You will not. Write it down. Externalize your memory. |

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings