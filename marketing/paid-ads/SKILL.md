---
name: paid-ads
description: Paid advertising for Google, Meta, LinkedIn — ad copy, audience targeting, budget optimization, conversion tracking. Use when setting up ad campaigns, optimizing ad spend, or designing ad creative.
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

## Pseudo Code

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
