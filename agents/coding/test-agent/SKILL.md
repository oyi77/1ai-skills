---
name: test-agent
description: Write comprehensive test suites covering happy paths, error paths, edge cases, and integration points. Use when
  adding test coverage, writing regression tests for bugs, or building e2e tests for critical flows.
domain: agents
tags:
- agent
- ai-agent
- automation
- orchestration
- test
---
# Test Agent

## When to Use

- Writing tests for new features before or after implementation
- Adding missing test coverage for existing code
- Writing regression tests for reported bugs
- Creating integration tests for API endpoints
- Building end-to-end tests for critical user flows
- Improving test coverage metrics (meaningfully, not just line counting)
- Setting up test infrastructure for a new project

## Overview

Test Agent is an AI agent skill for agent orchestration. It enables autonomous execution of complex tasks with minimal human intervention.

## Capabilities

- **Autonomous operation** — Execute multi-step test agent workflows independently
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

