---
name: joko-proactive-agent
description: Proactive agent that detects signals and suggests actions with Slack notifications
domain: core
tags:
- agent
- ai-agent
- infrastructure
- joko
- memory
- proactive
- self-improvement
- slack
allowed-tools:
- MCP(slack:*)
- MCP(notion:*)
---
# Joko Proactive Agent

## When to Use

**Trigger phrases:**
- "joko proactive agent"
- "Help me with joko proactive agent"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


Proactive agent that monitors business signals, detects opportunities/issues, and suggests actions with Slack notifications.

## Overview

Joko Proactive Agent is a foundational core infrastructure skill that provides system foundation capabilities for the agent ecosystem.

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

