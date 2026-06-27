---
name: schema-markup
description: Structured data markup for rich results and AI search visibility — JSON-LD, FAQ, HowTo, Product schemas. Use
  when implementing structured data for SEO.
domain: marketing
tags:
- growth
- marketing
- markup
- schema
- seo
---



## Overview

Structured data markup for rich results and AI search visibility — JSON-LD, FAQ, HowTo, Product schemas. Use when implementing structured data for SEO.

## Capabilities

- Schema.org type selection
- JSON-LD implementation
- Rich result testing
- FAQ and HowTo schema
- Product and Organization schema

## When to Use

- Building marketing campaigns and funnels
- Optimizing conversion and retention
- Scaling acquisition channels

## Common Patterns

1. Test with small budgets before scaling
2. Track attribution and ROI religiously
3. A/B test everything — headlines, CTAs, offers

## How to Use

1. Define campaign objective and target KPIs
2. Set up tracking and attribution (UTMs, pixels, events)
3. Create campaign assets (copy, creatives, landing pages)
4. Launch with small budget for testing
5. Monitor metrics daily, optimize underperformers
6. Scale winners, pause losers, document learnings

## When NOT to Use

- Task is about sales, not marketing (use sales skills)
- Task is about product development (use product skills)
- You need to analyze marketing data (use analytics skills)
- Task is about customer support (use support skills)
- You don't have marketing assets
- Task requires legal review (consult legal)


## Red Flags

- **Metrics declining 3+ days**: Investigate funnel leaks or audience fatigue
- **Ad spend with zero conversions**: Pause and review targeting/creative
- **Email open rates below 15%**: Subject lines or sender reputation issue
- **Bounce rate above 70%**: Landing page mismatch or slow load times
- **Attribution gaps**: Missing UTM parameters or broken tracking pixels
## Notes

- This skill integrates with the broader 1ai-skills ecosystem
- Combine with related marketing skills for maximum impact
- Monitor output quality and iterate on configuration
- Keep dependencies up to date for security and performance
- Document custom workflows for team knowledge sharing
## Notes

- This skill integrates with the broader 1ai-skills ecosystem
- Combine with related marketing skills for maximum impact
- Monitor output quality and iterate on configuration
- Keep dependencies up to date for security and performance
- Document custom workflows for team knowledge sharing
## Additional Resources

- Review the 1ai-skills repository for related marketing skills
- Check the references/ directory for checklists and templates
- Join the community for best practices and support
- Contribute improvements via pull requests

## Verification

- [ ] Skill output matches expected behavior

## Process

```python
# Example: SEO keyword analysis
def analyze_keywords(keywords: list[str]) -> list[dict]:
    results = []
    for kw in keywords:
        volume = get_search_volume(kw)
        difficulty = get_difficulty(kw)
        results.append({
            "keyword": kw,
            "volume": volume,
            "difficulty": difficulty,
            "opportunity": volume / max(difficulty, 1),
        })
    return sorted(results, key=lambda x: x["opportunity"], reverse=True)
```

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Good products sell themselves" | They do not. Marketing is how people discover your product. |
| "I will start marketing after launch" | Build audience before launch. Pre-launch momentum is critical. |
| "SEO is dead" | SEO evolves. GEO (Generative Engine Optimization) is the new frontier. |