---
name: data
description: Raw data storage layer for 1ai-skills. Provides structured data persistence, query interface, and data pipeline support for skill operations.
  history.
domain: meta
tags:
- data
- meta-learning
- self-improvement
- skill-evolution
persona:
  name: Database Architect
  expertise: SQLite, data modeling, query optimization
  philosophy: Data is the foundation of intelligence
---
# Data

## When to Use

**Trigger phrases:**
- "data"
- "Help me with data"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

/meta-datastore record-execution --skill seo-optimizer --success true --latency 245

# Query performance
/meta-datastore query "SELECT AVG(latency_ms) FROM skill_executions WHERE skill_name='seo-optimizer'"

# Get improvement candidates
/meta-datastore get-improvements --min-impact 0.7 --status proposed
```

### Integration

Connects to:
- performance-monitor (writes metrics)
- feedback-collector (stores feedback)
- pattern-recognition (queries patterns)
- skill-evolution (tracks versions)

## Overview

Data is a foundational meta-skills skill that provides skill management capabilities for the agent ecosystem.

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

