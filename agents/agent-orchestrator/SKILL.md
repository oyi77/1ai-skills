---
name: agent-orchestrator
description: Multi-agent coordination framework. Define agent teams, task delegation, memory sharing, conflict resolution
  for complex workflows. Use when coordinating multiple AI agents working together on large-scale tasks.
domain: agents
tags:
- multi-agent
- orchestration
- coordination
- teamwork
- delegation
- memory-sharing
---
# Agent Orchestrator

## When to Use

**Trigger phrases:**
- "Coordinate multiple agents on this task"
- "Build an agent team for this workflow"
- "Delegate work across specialized agents"
- "Manage agent collaboration"
- "Resolve conflicts between agents"

**Use cases:**
- Complex software development (design, code, test, deploy)
- Research projects (gather, analyze, synthesize, report)
- Content production (script, voiceover, video, publish)
- Business operations (data, analysis, recommendations, reporting)
- Security audits (scan, analyze, prioritize, remediate)

**When NOT to use:**
- Single-agent tasks (use regular task delegation)
- Sequential workflows with no parallelism
- Tasks requiring human decision at each step


## When NOT to Use

- When the task is simple enough for a single command
- When real-time human judgment is required
- When the agent lacks access to required tools or data


## Overview

Agent Orchestrator is an AI agent skill for agent orchestration. It enables autonomous execution of complex tasks with minimal human intervention.

## Capabilities

- **Autonomous operation** — Execute multi-step agent orchestrator workflows independently
- **Context awareness** — Adapt behavior based on current state and history
- **Error recovery** — Handle failures gracefully with retry and fallback logic
- **Integration** — Connect with external tools and services as needed

## Workflow

```python
# Example: Agent orchestration
from dataclasses import dataclass

@dataclass
class Task:
    name: str
    priority: int
    assigned_agent: str

def orchestrate(tasks: list[Task]) -> dict:
    results = {}
    for task in sorted(tasks, key=lambda t: t.priority):
        results[task.name] = execute(task)
    return results
```

1. **Initialize** — Set up the agent context and load required resources
2. **Plan** — Break down the task into executable steps
3. **Execute** — Run each step, monitoring for errors and adapting as needed
4. **Verify** — Validate results against acceptance criteria
5. **Report** — Summarize outcomes and suggest next steps

## Configuration

- Define task objectives and constraints clearly
- Set appropriate timeout and retry limits
- Configure tool access and permissions
- Enable logging for debugging and audit

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I will just do it manually" | Agents automate repetitive tasks — manual work does not scale |
| "The agent will figure it out" | Without clear instructions, agents hallucinate. Give explicit context. |
| "One agent is enough" | Complex tasks benefit from specialized agents working in parallel |


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run agent orchestrator workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings