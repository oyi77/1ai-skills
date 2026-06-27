---
name: review-agent
description: Read code changes with adversarial intent to find bugs, security holes, logic errors, and performance traps.
  Use when reviewing PRs, auditing refactoring for regressions, or running pre-deploy safety checks.
domain: agents
tags:
- agent
- ai-agent
- automation
- orchestration
- review
---
# Review Agent

## When to Use

- Reviewing pull requests before merge
- Auditing code changes for security issues
- Validating refactoring has not introduced regressions
- Checking that new features handle edge cases
- Reviewing third-party library integrations
- Pre-deploy safety checks
- Post-mortem analysis of production incidents

## Overview

Review Agent is an AI agent skill for agent orchestration. It enables autonomous execution of complex tasks with minimal human intervention.

## Capabilities

- **Autonomous operation** — Execute multi-step review agent workflows independently
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

