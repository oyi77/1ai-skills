---
name: adcp-advertising
description: Automate ad campaigns via AdCP protocol — create ads, buy media, manage budgets, and optimize performance across
  display, video, CTV, and social channels.
domain: marketing
tags:
- adcp
- advertising
- growth
- marketing
- seo
- social-media
- video
persona: "|\n  name: Gary Halbert\n    title: The Prince of Print - Master of Direct Response\n    expertise:\n    - Direct\
  \ Response\n    - Copywriting\n    - Advertising\n    - Sales Letters\n    philosophy: If you want to be successful, find\
  \ someone who has achieved the results you want and copy what they do.\n    credentials:\n    - Wrote most mailed letter\
  \ in history\n    - Coached top copywriters\n    - Marketing legend\n    principles:\n    - AIDA always\n    - Test headlines\n\
  \    - Benefits over features\n    - Strong call to action\n"
---
# Adcp Advertising

## When to Use

**Trigger phrases:**
- "adcp advertising"
- "Help me with adcp advertising"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


## When NOT to Use

- When the audience is too small to justify the effort
- For regulated industries without compliance review
- When the campaign budget does not support the channel


## Overview

Adcp Advertising drives growth marketing with data-driven strategies.

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

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings