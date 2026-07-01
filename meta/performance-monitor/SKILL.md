---
name: performance-monitor
description: Track and analyze skill execution performance. Measure latency, success rates, accuracy, and resource usage for
  continuous improvement. Use when tracking and analyze skill execution performance. measure latency, success rates,.
domain: meta
tags:
- meta-learning
- monitor
- performance
- self-improvement
- skill-evolution
persona:
  name: Performance Engineer
  expertise: Metrics, monitoring, optimization
  philosophy: If you can't measure it, you can't improve it
  credentials: SRE at Google, built monitoring systems
---
# Performance Monitor

## When to Use

**Trigger phrases:**
- "performance monitor"
- "Help me with performance monitor"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

/performance-monitor start skill-name

# Get report
/performance-monitor report skill-name --days 7

# Compare skills
/performance-monitor compare skill1 skill2 --metric success_rate
```

### Features

- Real-time metric collection
- Historical trend analysis
- Anomaly detection
- Performance regression alerts
- Cost tracking per skill


## When NOT to Use

- When the skill is stable and not changing
- For skills with fewer than 10 invocations (not enough data)
- When manual curation produces better results


## Overview

Performance Monitor is a foundational meta-skills skill that provides skill management capabilities for the agent ecosystem.

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

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Skills do not need to evolve" | Static skills become outdated. Self-evolving skills improve continuously. |
| "Manual skill management is fine" | With 1000+ skills, manual management is impossible. Automate. |
| "Performance does not matter" | Skill performance directly impacts agent effectiveness. Track it. |


## Process

1. **Design** — Define interface, identify patterns, plan implementation
1. **Implement** — Write code following existing conventions, add tests
1. **Verify** — Run tests, check integration, validate behavior

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings