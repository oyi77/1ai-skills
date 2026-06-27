---
name: improvement-generator
description: Generate specific, actionable improvements for skills based on performance data and feedback. Create improvement
  plans, not just identify problems.
domain: meta
tags:
- generator
- improvement
- meta-learning
- self-improvement
- skill-evolution
persona:
  name: Continuous Improvement Lead
  expertise: Root cause analysis, solution design, prioritization
  philosophy: Every problem has a solution
---
# Improvement Generator

## When to Use

**Trigger phrases:**
- "improvement generator"
- "Help me with improvement generator"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

/improvement-generator create --skill seo-optimizer --data performance-report

# Prioritize improvements
/improvement-generator prioritize --impact high --effort low

# Create implementation plan
/improvement-generator plan --improvement "optimize-caching"
```

### Output Format

```yaml
improvement_plan:
  skill: seo-optimizer
  generated: 12_improvements
  prioritized:
    - id: IMP-001
      title: "Add response caching"
      impact: high
      effort: medium
      expected_gain: "40% faster"
      implementation_steps:
        - Add cache layer
        - Implement TTL
        - Add cache invalidation
      estimated_time: 2_hours
```


## When NOT to Use

- When the skill is stable and not changing
- For skills with fewer than 10 invocations (not enough data)
- When manual curation produces better results


## Overview

Improvement Generator is a foundational meta-skills skill that provides skill management capabilities for the agent ecosystem.

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