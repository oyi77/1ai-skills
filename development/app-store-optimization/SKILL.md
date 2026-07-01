---
name: app-store-optimization
description: App Store and Play Store optimization — keywords, screenshots, reviews, and conversion rate optimization
domain: development
tags:
- app
- coding
- optimization
- software-engineering
- store
- testing
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
**Trigger phrases:**
- "app store optimization"
- "App Store and Play Store optimization — keywords, screenshots, reviews, and conv"


- Launching a new app to the stores
- Organic downloads have plateaued
- Need to improve store listing conversion rate
- Competing for keywords in your category

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The app-store-optimization workflow follows a standard pipeline pattern.

Core flow:
```
# app-store-optimization primary flow
input = prepare(raw_data)
result = process(input, config={app, conversion, keywords, optimization, play})
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

## How to Use

1. Understand the requirement and existing codebase patterns
2. Design the solution with error handling and testability in mind
3. Implement incrementally with tests for each change
4. Verify against expected outcomes (manual and automated)
5. Document usage, edge cases, and integration points
6. Review with team before merging to shared branches

## Red Flags

- **Skipping tests to ship faster**: Untested code breaks in production when you least expect it
- **No error handling in production code**: Unhandled errors crash services and lose user data
- **Hardcoded configuration values**: Hardcoded values prevent environment switching and leak secrets
- **Ignoring security implications**: Missing input validation, auth bypasses, and injection vulnerabilities
- **Over-engineering simple solutions**: Premature abstraction adds complexity without proportional benefit

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Tests slow me down" | Bugs slow you down 10x more. Tests are speed, not overhead. |
| "I will refactor later" | Technical debt compounds. Refactor as you go. |
| "It works on my machine" | If it is not in CI, it does not work. Ship proof, not claims. |