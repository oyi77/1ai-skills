---
name: meta-skill-datastore
description: Centralized database for meta-skill operations. Stores performance metrics, feedback, patterns, and skill evolution
  history.
domain: meta
tags:
- datastore
- meta
- meta-learning
- self-improvement
- skill
- skill-evolution
---
# Meta Skill Datastore

## When to Use

**Trigger phrases:**
- "meta skill datastore"
- "Help me with meta skill datastore"

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


## When NOT to Use

- When the skill is stable and not changing
- For skills with fewer than 10 invocations (not enough data)
- When manual curation produces better results


## Overview

Meta Skill Datastore is a foundational meta-skills skill that provides skill management capabilities for the agent ecosystem.

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

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings