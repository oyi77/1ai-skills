---
name: growth-engine
description: Autonomous marketing experiment framework — design A/B tests, score hypotheses with ICE, validate results with
  statistical significance, and run automated optimization loops.
domain: marketing
tags:
- engine
- growth
- marketing
- seo
---
# Growth Engine

## When to Use

**Trigger phrases:**
- "growth engine"
- "Help me with growth engine"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

hypothesis = growth_hypothesis(
    insight="Users who view demo video convert 3x higher",
    design="Add prominent demo CTA on homepage",
    expected="+25% demo views, +15% trial signups",
    assumption="Demo video quality resonates with target audience"
)

# 2. Design experiment
experiment = design_ab_test(
    hypothesis=hypothesis,
    variants=["demo_cta_v1", "demo_cta_v2"],
    primary_metric="trial_signup_rate",
    secondary_metrics=["demo_view_rate", "time_on_page"],
    traffic_split=[0.34, 0.33, 0.33]  # Control + 2 variants
)

# 3. Launch and monitor
experiment.launch()

while experiment.status == "RUNNING":
    daily_report = experiment.generate_report()
    
    # Check pacing alerts
    if daily_report.sample_size_alert:
        notify("Sample size behind pace")
    
    if daily_report.conversion_drop:
        experiment.pause()
        notify("Conversion rate anomaly detected")
    
    time.sleep(86400)  # Daily check

# 4. Analyze results
results = experiment.final_analysis()

if results.winner and results.confidence >= 0.95:
    implement_winner(results.winner)
    document_learning(results)
else:
    document_learning(results)  # Document negative result too
```

### Example 2: Rapid Experiment Pipeline

```python
# Run multiple micro-experiments in parallel
experiments = [
    {"type": "email_subject", "n_variants": 5, "traffic": "10%"},
    {"type": "cta_color", "n_variants": 4, "traffic": "20%"},
    {"type": "pricing_display", "n_variants": 3, "traffic": "30%"}
]

for exp_config in experiments:
    exp = create_micro_experiment(exp_config)
    exp.launch()
    
# Weekly review
candidates = []
for exp in running_experiments:
    results = exp.get_results()
    if results.confidence >= 0.90:
        candidates.append(results)
        
# Promote winners
for winner in candidates:
    rollout_gradually(winner.variant, [0.10, 0.50, 1.0])
```

### Example 3: Growth Scorecard

```python
# Generate weekly growth report
scorecard = {
    "experiments": {
        "running": 8,
        "completed_this_week": 3,
        "winners": 1,
        "inconclusive": 2
    },
    "metrics": {
        "activation_rate": {"current": 0.35, "lift": "+5%"},
        "retention_d7": {"current": 0.42, "lift": "+3%"},
        "referral_rate": {"current": 0.18, "lift": "+12%"}
    },
    "velocity": {
        "experiments_per_week": 2.5,
        "win_rate": 0.33,
        "avg_lift": "8.5%"
    }
}

generate_weekly_scorecard(scorecard)
```

---


## When NOT to Use

- When the audience is too small to justify the effort
- For regulated industries without compliance review
- When the campaign budget does not support the channel


## Overview

Growth Engine drives growth marketing with data-driven strategies.

## Workflow

1. **Research** — Analyze market, competitors, and audience
2. **Strategy** — Define goals, channels, and messaging
3. **Create** — Develop content and creative assets
4. **Launch** — Deploy campaigns across channels
5. **Optimize** — A/B test and iterate based on data
6. **Report** — Track KPIs and ROI

## Key Metrics

- Reach and impressions
- Engagement rate (likes, shares, comments)
- Conversion rate (clicks → leads → customers)
- Customer acquisition cost (CAC)
- Return on ad spend (ROAS)

## Best Practices

- Test everything — headlines, images, CTAs, timing
- Focus on one channel at a time, then expand
- Build organic before scaling paid
- Track attribution across the full funnel

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Good products sell themselves" | They do not. Marketing is how people discover your product. |
| "I will start marketing after launch" | Build audience before launch. Pre-launch momentum is critical. |
| "SEO is dead" | SEO evolves. GEO (Generative Engine Optimization) is the new frontier. |

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings