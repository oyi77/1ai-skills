---
name: paid-ads
description: Paid advertising for Google, Meta, LinkedIn — ad copy, audience targeting, budget optimization, conversion tracking.
  Use when setting up ad campaigns, optimizing ad spend, or designing ad creative.
domain: marketing
tags:
- ads
- growth
- marketing
- paid
- seo
---



# Paid Ads

Design and optimize paid advertising campaigns.

## Capabilities

- Google Search and Display ad copy
- Meta (Facebook/Instagram) ad creative
- LinkedIn B2B ad campaigns
- Audience targeting and lookalike audiences
- Budget optimization and bid strategies
- Conversion tracking setup

## When to Use

- Setting up paid ad campaigns
- Optimizing existing ad performance
- Designing ad creative and copy
- Implementing conversion tracking

## When NOT to Use

- Task is about sales, not marketing (use sales skills)
- Task is about product development (use product skills)
- You need to analyze marketing data (use analytics skills)
- Task is about customer support (use support skills)
- You don't have marketing assets
- Task requires legal review (consult legal)


## Pseudo Code

The paid-ads workflow follows a standard pipeline pattern.

Core flow:
```
# paid-ads primary flow
input = prepare(raw_data)
result = process(input, config={ads, advertising, audience, budget, campaigns})
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
# paid-ads primary flow
input = prepare(raw_data)
result = process(input, config={ads, advertising, audience, budget, campaigns})
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


### Google Search Ad

```python
ad = {
    "headlines": [
        "Automate Your Sales Pipeline",
        "AI-Powered CRM for Teams",
        "Try Free for 14 Days",
    ],
    "descriptions": [
        "Close more deals with AI-driven insights. No credit card required.",
        "Join 5,000+ sales teams. Setup in 5 minutes. Start free today.",
    ],
    "keywords": ["sales crm", "ai crm", "sales automation"],
    "negative_keywords": ["free", "jobs", "salary"],
}
```

### Meta Audience

```python
audiences = {
    "lookalike": {
        "source": "purchase_pixel",
        "country": "US",
        "ratio": 0.01,  # 1% lookalike
    },
    "interest": {
        "interests": ["digital marketing", "SaaS", "entrepreneur"],
        "behaviors": ["small business owners"],
    },
    "retargeting": {
        "events": ["page_view", "add_to_cart"],
        "days": 30,
    },
}
```

### Budget Optimization

```python
def allocate_budget(total_budget, campaigns):
    """Allocate based on ROAS (Return on Ad Spend)."""
    total_roas = sum(c["roas"] for c in campaigns)
    for c in campaigns:
        c["budget"] = total_budget * (c["roas"] / total_roas)
    return campaigns
```

## Common Patterns

- **Ad copy formula**: Problem → Solution → Proof → CTA
- **A/B test**: One variable at a time (headline, image, CTA)
- **Retargeting**: 7-day window for hot leads, 30-day for warm
- **Negative keywords**: Add 10-20 per week to reduce waste
- **Landing page match**: Ad message must match landing page headline

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
