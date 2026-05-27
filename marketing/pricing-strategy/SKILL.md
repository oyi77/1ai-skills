---
name: pricing-strategy
description: Pricing page design, tier structuring, anchoring psychology, conversion optimization. Use when designing pricing pages, setting up tier structures, or optimizing pricing conversion rates.
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

## Pseudo Code

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
