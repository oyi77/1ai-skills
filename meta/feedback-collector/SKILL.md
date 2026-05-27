---
name: feedback-collector
description: Collect, analyze, and route feedback from users and systems. Turn feedback into actionable improvement signals.
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

- [TODO: Add specific exclusion cases for this skill]
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- [TODO: Add behavioral signs the skill is being violated]
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] [TODO: Add specific evidence-based checklist items]
- [ ] All required outputs generated
- [ ] Success criteria met

