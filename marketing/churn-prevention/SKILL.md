---
name: churn-prevention
description: Retention messaging, cancellation flows, win-back campaigns, and customer health scoring. Use when reducing churn
  rates, designing retention campaigns, or implementing cancellation flows.
domain: marketing
tags:
- churn
- growth
- marketing
- prevention
- seo
---



# Churn Prevention

Reduce churn with proactive health scoring and targeted retention.

## Capabilities

- Customer health scoring
- Cancellation flow design
- Win-back email sequences
- Usage-based churn prediction
- Retention offer strategy
- Exit survey analysis

## When to Use

- Churn rate is increasing
- Designing cancellation flows
- Building win-back campaigns
- Implementing health scores

## When NOT to Use

- Task is about sales, not marketing (use sales skills)
- Task is about product development (use product skills)
- You need to analyze marketing data (use analytics skills)
- Task is about customer support (use support skills)
- You don't have marketing assets
- Task requires legal review (consult legal)


## Pseudo Code

The churn-prevention workflow follows a standard pipeline pattern.

Core flow:
```
# churn-prevention primary flow
input = prepare(raw_data)
result = process(input, config={back, campaigns, cancellation, churn, customer})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Core Workflow
```
# churn-prevention primary flow
input = prepare(raw_data)
result = process(input, config={back, campaigns, cancellation, churn, customer})
validate(result)
deliver(result)
```

### Error Handling
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Health Score

```python
def calculate_health_score(user):
    score = 0
    score += login_frequency_score(user.logins_last_30d) * 0.3
    score += feature_adoption_score(user.features_used) * 0.25
    score += engagement_score(user.sessions_last_7d) * 0.25
    score += support_ticket_score(user.tickets_last_30d) * 0.2
    
    if score < 40: return "at_risk"
    if score < 70: return "needs_attention"
    return "healthy"
```

### Cancellation Flow

```python
cancellation_flow = [
    {"step": "reason", "question": "What's the main reason?"},
    {"step": "offer", "condition": "price", "action": "offer_20_percent_off"},
    {"step": "offer", "condition": "not_using", "action": "offer_free_setup_call"},
    {"step": "downgrade", "condition": "other", "action": "offer_lower_plan"},
    {"step": "confirm", "action": "process_cancellation"},
]
```

### Win-Back Sequence

```python
win_back_sequence = [
    {"day": 1, "subject": "We miss you, {name}", "content": "new_features_since_left"},
    {"day": 7, "subject": "Your data is waiting", "content": "what_theyre_missing"},
    {"day": 14, "subject": "Come back with 30% off", "content": "special_offer"},
    {"day": 30, "subject": "Last chance: your account", "content": "final_breakup"},
]
```

## Common Patterns

- **Intervene early**: Trigger outreach when health score drops, not at cancellation
- **Personalize offers**: Price objections get discounts, usage objections get onboarding
- **Exit surveys**: Always ask why, even if you can't save them
- **Win-back timing**: 1-3 months after churn is optimal

## How to Use

1. Define campaign objective and target KPIs
2. Set up tracking and attribution (UTMs, pixels, events)
3. Create campaign assets (copy, creatives, landing pages)
4. Launch with small budget for testing
5. Monitor metrics daily, optimize underperformers
6. Scale winners, pause losers, document learnings

## Red Flags

- **Metrics declining 3+ days**: Investigate funnel leaks or audience fatigue
- **Ad spend with zero conversions**: Pause and review targeting/creative
- **Email open rates below 15%**: Subject lines or sender reputation issue
- **Bounce rate above 70%**: Landing page mismatch or slow load times
- **Attribution gaps**: Missing UTM parameters or broken tracking pixels

## Overview

> Section content — see SKILL.md body for full details.

## Verification

- [ ] Skill output matches expected behavior
