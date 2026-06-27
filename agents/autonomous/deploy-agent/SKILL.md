---
name: deploy-agent
description: Ship code to production through a controlled pipeline with verification gates and rollback plans. Use when deploying
  features, managing CI/CD, running database migrations, or performing post-incident hotfix recovery.
domain: agents
tags:
- agent
- ai-agent
- automation
- deploy
- orchestration
- pipeline
---
# Deploy Agent

## When to Use

- Deploying a new feature to staging or production
- Setting up or modifying CI/CD pipelines
- Rolling back a bad deployment
- Performing database migrations in production
- Configuring infrastructure (Docker, Kubernetes, cloud services)
- Managing feature flags for staged rollouts
- Post-incident recovery and hotfix deployment

## Overview

Deploy Agent is an AI agent skill for agent orchestration. It enables autonomous execution of complex tasks with minimal human intervention.

## Capabilities

- **Autonomous operation** — Execute multi-step deploy agent workflows independently
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

