---
name: teamwork
description: Dynamically creates and manages AI agent teams for complex tasks. Invoke when user requests multi-agent collaboration,
  complex project execution, or when tasks require specialized roles and coordinated workflow.
domain: core
tags:
- ai-agent
- infrastructure
- memory
- self-improvement
- teamwork
- workflow
---
# Teamwork

## When to Use

**Trigger phrases:**
- "teamwork"
- "Help me with teamwork"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


This skill enables dynamic team creation and management for executing complex engineering tasks through coordinated AI agents with intelligent model selection, cost optimization, and continuous performance evaluation.

## Overview

Teamwork is a foundational core infrastructure skill that provides system foundation capabilities for the agent ecosystem.

## Architecture

- **Input layer** — Receives and validates incoming requests
- **Processing layer** — Core logic for system foundation
- **Output layer** — Formats and delivers results
- **State management** — Maintains context across invocations

## Configuration

- Set up required environment variables and paths
- Configure logging level and output format
- Define resource limits (memory, time, API calls)
- Enable/disable features via configuration flags

## Integration

- Exposes standard interfaces for other skills to consume
- Supports event-driven and request-response patterns
- Compatible with the 1ai-skills hook system
- Logs metrics for the skill performance monitor

