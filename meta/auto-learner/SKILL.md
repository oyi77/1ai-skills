---
name: auto-learner
description: Autonomous learning from execution data. Skills improve themselves by identifying patterns in successful vs failed
  executions without human intervention.
domain: meta
tags:
- auto
- learner
- meta-learning
- self-improvement
- skill-evolution
persona:
  name: Autonomous Learner
  expertise: Machine learning, pattern recognition, self-supervision
  philosophy: Learn by doing, improve by reflecting
---
# Auto Learner

## When to Use

**Trigger phrases:**
- "auto learner"
- "Help me with auto learner"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

/auto-learner enable --skill seo-optimizer

# Trigger learning cycle
/auto-learner learn --skill seo-optimizer --min-samples 100

# View learned improvements
/auto-learner status --skill seo-optimizer
```

### Learning Triggers

- After 100 executions
- When success rate drops below threshold
- When new error patterns emerge
- On user request
- Scheduled daily/weekly

### Safety

- Changes are staged, not immediate
- Human approval required for major changes
- Rollback always available
- Tests must pass before deployment

## Overview

Auto Learner is a foundational meta-skills skill that provides skill management capabilities for the agent ecosystem.

## Architecture

- **Input layer** — Receives and validates incoming requests
- **Processing layer** — Core logic for skill management
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

