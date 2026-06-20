---
name: pricing-strategy
description: Pricing page design, tier structuring, anchoring psychology, conversion optimization. Use when designing pricing
  pages, setting up tier structures, or optimizing pricing conversion rates.
domain: marketing
tags:
- growth
- marketing
- pricing
- seo
- strategy
---



# Pricing Strategy

Design pricing that maximizes revenue and conversion.

## Capabilities

- Pricing tier design (good/better/best)
- Anchoring and psychology tactics
- Pricing page layout optimization
- A/B testing pricing experiments
- Freemium vs free trial strategy
- Annual/monthly toggle optimization

## When to Use

- Designing pricing for a new product
- Optimizing existing pricing page conversion
- Adding or restructuring pricing tiers
- Testing pricing experiments

## When NOT to Use

- Task is about sales, not marketing (use sales skills)
- Task is about product development (use product skills)
- You need to analyze marketing data (use analytics skills)
- Task is about customer support (use support skills)
- You don't have marketing assets
- Task requires legal review (consult legal)


## Pseudo Code

The pricing-strategy workflow follows a standard pipeline pattern.

Core flow:
```
# pricing-strategy primary flow
input = prepare(raw_data)
result = process(input, config={anchoring, conversion, design, designing, optimization})
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
# pricing-strategy primary flow
input = prepare(raw_data)
result = process(input, config={anchoring, conversion, design, designing, optimization})
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


### Tier Design

```python
pricing_tiers = {
    "starter": {
        "price": 29,
        "features": ["Core features", "5 users", "Email support"],
        "highlight": False,
    },
    "pro": {
        "price": 79,
        "features": ["Everything in Starter", "Unlimited users", "Priority support", "API access"],
        "highlight": True,  # Most popular badge
    },
    "enterprise": {
        "price": "Custom",
        "features": ["Everything in Pro", "SSO", "Dedicated support", "SLA"],
        "highlight": False,
    }
}
```

### Anchoring Strategy

```
Display order: Enterprise ($299) → Pro ($79) → Starter ($29)
- Enterprise makes Pro look affordable (anchoring)
- "Most Popular" badge on Pro guides choice
- Annual toggle shows savings percentage
```

### A/B Test

```python
experiments = [
    {"name": "price_point", "variants": [29, 39, 49], "metric": "revenue_per_visitor"},
    {"name": "tier_count", "variants": [2, 3, 4], "metric": "conversion_rate"},
    {"name": "annual_default", "variants": ["monthly", "annual"], "metric": "ltv"},
]
```

## Common Patterns

- **3 tiers**: Simple choice architecture (Hick's Law)
- **Anchor high**: Show most expensive option first
- **Highlight middle**: "Most popular" badge on target tier
- **Annual savings**: Show 20% savings for annual billing
- **Social proof**: "Join 10,000+ teams" near pricing

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
