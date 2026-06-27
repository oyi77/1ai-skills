---
name: feedback-collector
description: Collect, analyze, and route feedback from users and systems. Turn feedback into actionable improvement signals.
domain: meta
tags:
- collector
- feedback
- meta-learning
- self-improvement
- skill-evolution
persona:
  name: User Research Lead
  expertise: Feedback systems, NLP, sentiment analysis
  philosophy: Every interaction is an opportunity to learn
---
# Feedback Collector

## When to Use

**Trigger phrases:**
- "feedback collector"
- "Help me with feedback collector"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

/feedback-collector submit skill=seo-optimizer rating=4 comment="Good but slow"

# Analyze sentiment
/feedback-collector analyze --skill seo-optimizer --timeframe 30d

# Route to improvement
/feedback-collector route --priority high --type performance
```

### Sentiment Scoring

- Positive: > 0.6
- Neutral: 0.4-0.6
- Negative: < 0.4

### Output Format

```yaml
feedback_summary:
  skill: seo-optimizer
  period: 30d
  total_feedback: 47
  avg_rating: 4.2
  sentiment: 0.71
  key_themes:
    - "slow execution"
    - "good results"
    - "needs examples"
  action_items:
    - type: performance
      priority: high
      issue: latency
```


## When NOT to Use

- When the skill is stable and not changing
- For skills with fewer than 10 invocations (not enough data)
- When manual curation produces better results


## Overview

Feedback Collector is a foundational meta-skills skill that provides skill management capabilities for the agent ecosystem.

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