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
## Feedback Collector

Multi-channel feedback aggregation and analysis.

### Feedback Sources

```yaml
feedback_channels:
  explicit:
    - user_ratings      # 1-5 star ratings
    - written_feedback  # Text comments
    - bug_reports       # Issues filed
  implicit:
    - retry_count       # How many retries needed
    - time_to_complete  # Task duration
    - followup_questions # Clarifications needed
  automated:
    - output_validation # Automated checks
    - error_patterns    # Recurring errors
```

### Analysis Pipeline

```python
# Collect feedback
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

- When the meta-skill would modify skills used by production systems
- When the evolution or learning process cannot be rolled back if it fails
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Meta-skill changes are applied without measuring performance impact
- Agent does not verify that changes maintain backward compatibility
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Performance is measured before and after meta-skill changes
- [ ] Backward compatibility is verified for all modifications
- [ ] All required outputs generated
- [ ] Success criteria met

## Overview

> Section content — see SKILL.md body for full details.
