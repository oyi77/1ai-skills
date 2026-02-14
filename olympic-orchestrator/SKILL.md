---
slug: olympic-orchestrator
name: Olympic Orchestrator v3
version: 3.0.0
description: A hierarchical multi-agent system for complex project execution. Led by Zeus, planned by Prometheus, managed by Atlas, and executed by Hephaestus/Sisyphus.
author: oyi77
metadata:
  {
    "openclaw":
      {
        "emoji": "🏛️",
        "requires": { "bins": ["python3"] }
      },
  }
---

# Olympic Orchestrator Skill (v3)

A strict hierarchical command structure for autonomous agents.

## The Pantheon (Roles)

### 👑 Zeus (Team Leader)
The ultimate decision maker. Holds the context of the Master's goals.
- **Input:** Master's raw intent.
- **Output:** Directives for Metis/Prometheus.
- **Authority:** Can kill/restart any process.

### 🦉 Metis (Researcher)
The intelligence gatherer.
- **Task:** Deep dive research, fact-checking, and feasibility studies.
- **Output:** Research papers in `.olympic/research/`.

### 🔥 Prometheus (Planner)
The architect.
- **Task:** Synthesizes research into a cohesive strategy.
- **Output:** Master Plans in `.olympic/plans/`.

### 🌍 Atlas (Project Manager)
The coordinator.
- **Task:** Breaks down Master Plans into specific, atomic tasks.
- **Output:** Task Tickets in `.olympic/tasks/`.
- **Authority:** Assigns work to Hephaestus/Sisyphus.

### 🔨 Hephaestus (Builder)
The engineer.
- **Task:** One-off complex execution (Coding, Deployment, Writing).
- **Mode:** Project-based.

### 🪨 Sisyphus (Maintainer)
The loop engine.
- **Task:** Repetitive maintenance, monitoring, and health checks.
- **Mode:** Process-based (Cron/Heartbeat).

### 🎭 Momus (QA/Reviewer)
The critic.
- **Task:** Audits outputs from Hephaestus/Prometheus against requirements.
- **Output:** Approval or Rejection reports.

## Directory Structure

```text
.olympic/
├── plans/       # Prometheus Strategy Docs
├── research/    # Metis Intelligence Reports
├── tasks/       # Atlas Task Tickets
└── logs/        # Execution Logs
```

## Workflow

1. **Master** -> **Zeus**: "I need X."
2. **Zeus** -> **Metis**: "Research how to build X."
3. **Metis** -> **Prometheus**: "Here is the data."
4. **Prometheus** -> **Atlas**: "Here is the plan."
5. **Atlas** -> **Hephaestus**: "Build module A."
6. **Hephaestus** -> **Momus**: "Module A ready."
7. **Momus** -> **Zeus**: "Quality confirmed."
