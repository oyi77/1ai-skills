---
name: project-management-state
description: >
  Autonomous project management using STATE.yaml pattern. Each project has
  a state file with tasks, status, owners. Multi-agent coordination via
  state file read/write.
version: "1.0.0"
author: BerkahKarya AI
tags: [project-management, state, yaml, tasks, coordination, autonomous]
---

# Autonomous Project Management (STATE.yaml)

## Overview

Lightweight project management using YAML state files. No external dependencies — each project is tracked via a `STATE.yaml` file that agents can read and update independently.

## STATE.yaml Template

```yaml
project: My Project
created: 2026-03-21
owner: team-lead
status: active

tasks:
  - id: 1
    title: Design API schema
    owner: dev-agent
    status: todo           # todo | in_progress | done | blocked
    priority: high         # low | medium | high | critical
    created: 2026-03-21
    notes: ""

  - id: 2
    title: Set up CI/CD
    owner: devops-agent
    status: todo
    priority: medium
    created: 2026-03-21
    depends_on: [1]
    notes: ""

milestones:
  - name: MVP
    target: 2026-04-01
    tasks: [1, 2]

log:
  - timestamp: "2026-03-21T10:00:00"
    agent: coordinator
    action: "Project created"
```

## Usage

```bash
# Create a new project
python3 scripts/project_state.py create "AI Dashboard" --owner vilona

# Add a task
python3 scripts/project_state.py add-task "AI Dashboard" "Build frontend" --owner dev --priority high

# Update task status
python3 scripts/project_state.py update "AI Dashboard" 1 --status in_progress

# Get project summary
python3 scripts/project_state.py summary "AI Dashboard"

# List all projects
python3 scripts/project_state.py list
```

## Multi-Agent Coordination

Each subagent:
1. Reads STATE.yaml for their assigned tasks
2. Works on `in_progress` tasks assigned to them
3. Updates status + notes when done
4. Coordinator checks for blocked dependencies

## File Storage

Projects stored in: `skills/productivity/project-management/projects/<project-name>/STATE.yaml`
