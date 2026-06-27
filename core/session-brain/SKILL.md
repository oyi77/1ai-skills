---
name: session-brain
description: Query bk-hub for project context on session start so every session begins with memory instead of starting blind
domain: core
tags:
- brain
- infrastructure
- memory
- self-improvement
- session
trigger: auto
---
# Session Brain

## When to Use

**Trigger phrases:**
- "session brain"
- "Help me with session brain"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


**Auto-runs on first message of every session.** Queries bk-hub for project context and injects it before responding.

## Overview

Session Brain is a foundational core infrastructure skill that provides system foundation capabilities for the agent ecosystem.

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

