---
name: self-assessment
description: Skills evaluate their own performance, capabilities, and limitations. Honest self-reflection drives improvement.
domain: meta
tags:
- assessment
- meta-learning
- self
- self-improvement
- skill-evolution
persona:
  name: Honest Self-Evaluator
  expertise: Introspection, capability analysis, gap identification
  philosophy: Know thyself
---
# Self Assessment

## When to Use

**Trigger phrases:**
- "self assessment"
- "Help me with self assessment"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

/self-assessment run skill-name

# View assessment history
/self-assessment history skill-name

# Compare to peer skills
/self-assessment benchmark skill-name --category marketing
```

### Reflection Questions

1. What did I do well?
2. Where did I struggle?
3. What patterns do I see in my failures?
4. How do I compare to similar skills?
5. What should I learn next?

### Output

```yaml
assessment_report:
  skill: seo-optimizer
  timestamp: 2026-05-04
  overall_score: 0.79
  strengths:
    - comprehensive analysis
    - good error handling
  weaknesses:
    - slow on large sites
    - limited JavaScript support
  recommendations:
    - optimize for speed
    - add headless browser support
```

## Overview

Self Assessment is a foundational meta-skills skill that provides skill management capabilities for the agent ecosystem.

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

