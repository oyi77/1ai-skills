---
name: app-store-optimization
description: App Store and Play Store optimization — keywords, screenshots, reviews, and conversion rate optimization
---

## Overview

Optimize App Store and Play Store listings for maximum downloads. Covers keyword research, title optimization, screenshot design, A/B testing, review management, and conversion tracking.

## Capabilities

- Research and optimize keywords for store search
- Design high-converting screenshots and preview videos
- A/B test store listings for conversion optimization
- Manage and respond to user reviews
- Track conversion rates and organic download trends

## When to Use

- Launching a new app to the stores
- Organic downloads have plateaued
- Need to improve store listing conversion rate
- Competing for keywords in your category

## Pseudo Code

### Keyword Research
```python
def research_keywords(category, competitors):
    keywords = []
    for competitor in competitors:
        keywords.extend(get_competitor_keywords(competitor))
    
    scored = []
    for kw in set(keywords):
        volume = get_search_volume(kw)
        difficulty = get_competition(kw)
        scored.append({"keyword": kw, "volume": volume, "difficulty": difficulty, "score": volume / difficulty})
    
    return sorted(scored, key=lambda x: x["score"], reverse=True)[:20]
```

### ASO Checklist
```markdown
- [ ] Title includes primary keyword (max 30 chars)
- [ ] Subtitle includes secondary keywords (max 30 chars)
- [ ] Keywords field filled (iOS) / description frontloaded (Android)
- [ ] 5+ screenshots with captions showing key features
- [ ] Preview video (15-30 seconds)
- [ ] 4.5+ star rating with active review responses
- [ ] Regular updates (at least monthly)
```

## Common Patterns

- **Keyword in title**: Primary keyword in app title for search ranking
- **Screenshot story**: Screenshots tell a story, not just show features
- **Review prompts**: In-app review prompts after positive actions
- **A/B test everything**: Icon, screenshots, description — test each element
