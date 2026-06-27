---
name: refactor-agent
description: Restructure code to improve readability, maintainability, and extensibility without changing external behavior.
  Use when reducing complexity, extracting reusable components, splitting monoliths, or modernizing legacy code.
domain: agents
tags:
- agent
- ai-agent
- automation
- orchestration
- refactor
- rest-api
---
# Refactor Agent

## When to Use

- Reducing complexity in a function or module (cyclomatic complexity >10)
- Extracting reusable components from duplicated code
- Applying design patterns where they reduce coupling
- Splitting monolithic files into focused modules
- Modernizing legacy code (var to const, callbacks to async/await)
- Removing dead code and unused dependencies
- Preparing code for new features (make the change easy first)
- Improving testability (dependency injection, pure functions)

## Overview

Refactor Agent is an AI agent skill for agent orchestration. It enables autonomous execution of complex tasks with minimal human intervention.

## Capabilities

- **Autonomous operation** — Execute multi-step refactor agent workflows independently
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

