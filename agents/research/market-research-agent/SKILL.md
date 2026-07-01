---
name: market-research-agent
description: Analyze markets, competitors, user segments, and trends to produce evidence-based business intelligence. Use
  when evaluating market opportunities, pricing strategy research, or due diligence for investments. Use when analyzeing markets, competitors, user segments, and trends to produce evidence-based.
domain: agents
tags:
- agent
- ai-agent
- automation
- market
- orchestration
- research
---
# Market Research Agent

## When to Use
**Trigger phrases:**
- "market research agent"
- "Analyze markets, competitors, user segments, and trends to produce evidence-base"


- Evaluating market opportunity before building a product
- Analyzing competitors before launching or pivoting
- Pricing strategy research for new or existing products
- Understanding user segments and their needs
- Tracking market trends and technology shifts
- Due diligence for investment or acquisition decisions
- Go-to-market planning for new features or products


## When NOT to Use

- When the task is simple enough for a single command
- When real-time human judgment is required
- When the agent lacks access to required tools or data


## Overview

Market Research Agent is an AI agent skill for agent orchestration. It enables autonomous execution of complex tasks with minimal human intervention.

## Capabilities

- **Autonomous operation** — Execute multi-step market research agent workflows independently
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

1. **Scope** — Define research questions, identify data sources, set time boundaries
1. **Gather** — Collect data from primary sources, APIs, and public records
1. **Synthesize** — Analyze findings, identify patterns, produce actionable report

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings