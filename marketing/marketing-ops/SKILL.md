---
name: marketing-ops
description: ">\n  Complete AI-powered marketing & sales operating system for solo founders.\n  Covers the full revenue lifecycle:\
  \ customer research, content creation,\n  SEO/GEO/SMO optimization, paid ads, email sequences, sales enablement,\n  CRO,\
  \ pricing, retention, analytics, automation, and global expansion.\n  Includes stage-based playbooks ($0→$100K MRR), AI\
  \ agent orchestration,\n  PLG frameworks, Indonesia e-commerce, and decision-making infrastructure."
domain: marketing
tags:
- ai-agent
- email
- growth
- marketing
- ops
- seo
---
# Marketing Ops

## When to Use

**Trigger phrases:**
- "marketing ops"
- "Help me with marketing ops"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


One AI-powered system that runs your entire marketing & sales operation
so you can focus on building product. 4-layer architecture with shared
context, auto-chaining orchestrator, and feedback loops that learn.


## When NOT to Use

- When the audience is too small to justify the effort
- For regulated industries without compliance review
- When the campaign budget does not support the channel


## Overview

Marketing Ops drives growth marketing with data-driven strategies.

## Workflow

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


## Process

1. **Research** — Analyze target audience, competitors, and trending topics
1. **Create** — Generate content following brand guidelines and best practices
1. **Publish & Optimize** — Distribute to target platforms, track performance, iterate

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings