---
name: planning-agent
description: Decompose complex tasks into executable, ordered steps with dependencies, risk assessments, and verification
  criteria. Use before implementing features touching 3+ files, coordinating multi-agent work, or migrating systems.
domain: agents
tags:
- agent
- ai-agent
- automation
- orchestration
- planning
---
# Planning Agent

## When to Use

- Before implementing any feature that touches 3+ files
- Before refactoring that affects multiple modules
- When the implementation path is not obvious
- When risk of regression is high
- When coordinating work across multiple agents or people
- When migrating systems, databases, or APIs
- When the task has ambiguous requirements that need decomposition

## Overview

Planning Agent is an AI agent skill for agent orchestration. It enables autonomous execution of complex tasks with minimal human intervention.

## Capabilities

- **Autonomous operation** — Execute multi-step planning agent workflows independently
- **Context awareness** — Adapt behavior based on current state and history
- **Error recovery** — Handle failures gracefully with retry and fallback logic
- **Integration** — Connect with external tools and services as needed

## Workflow

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

