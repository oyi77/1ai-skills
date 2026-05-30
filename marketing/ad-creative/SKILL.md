---
name: ad-creative
description: Ad creative production — visual briefs, copy variations, and A/B testing frameworks for performance advertising.
---



# Ad Creative

## Overview

Creative is the #1 driver of ad performance. In 2026, 70% of ad auction outcomes are determined by creative quality, not targeting. This skill covers producing high-performing ad creative at scale — visuals, copy, and systematic testing.

## Capabilities

- Write ad copy using proven frameworks (AIDA, PAS, 4U)
- Create visual briefs for designers
- Build creative testing matrices
- Analyze creative performance data
- Generate ad copy variations at scale
- Design thumb-stopping creative concepts

## When to Use

- Ad performance is declining (creative fatigue)
- Need to scale ad production without scaling team
- A/B testing isn't structured or systematic
- Launching campaigns in new platforms
- Competitor ads are outperforming yours

## When NOT to Use

- Task is about sales, not marketing (use sales skills)
- Task is about product development (use product skills)
- You need to analyze marketing data (use analytics skills)
- Task is about customer support (use support skills)
- You don't have marketing assets
- Task requires legal review (consult legal)


## Pseudo Code

The ad-creative workflow follows a standard pipeline pattern.

Core flow:
```
# ad-creative primary flow
input = prepare(raw_data)
result = process(input, config={advertising, briefs, copy, creative, frameworks})
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
# ad-creative primary flow
input = prepare(raw_data)
result = process(input, config={advertising, briefs, copy, creative, frameworks})
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


### Ad Copy Frameworks
```python
def write_ad_copy(product, framework, platform):
    """Generate ad copy using proven frameworks"""
    
    frameworks = {
        "AIDA": {
            "attention": f"Still struggling with {pain_point}?",
            "interest": f"{product.name} helps {target_audience} {benefit}",
            "desire": f"Join {social_proof_count} who already {result}",
            "action": f"Start your free trial →"
        },
        "PAS": {
            "problem": f"{pain_point} is costing you {cost}",
            "agitation": f"Every day without {solution}, you lose {metric}",
            "solution": f"{product.name} fixes this in {timeframe}"
        },
        "4U": {
            "urgent": f"Limited: {offer} ends {deadline}",
            "unique": f"Only {product.name} has {unique_feature}",
            "ultra_specific": f"{specific_number}% improvement in {metric}",
            "useful": f"Free {resource_type} inside"
        }
    }
    
    copy = frameworks[framework]
    
    # Adapt for platform
    if platform == "meta":
        return format_for_meta(copy, char_limit=125)
    elif platform == "google":
        return format_for_google(copy, headline_limit=30, desc_limit=90)
    elif platform == "linkedin":
        return format_for_linkedin(copy, professional_tone=True)
```

### Creative Testing Matrix
```python
def build_creative_test_matrix(product):
    """Systematic testing: one variable at a time"""
    
    tests = {
        "hook_test": {
            "variable": "opening_line",
            "variants": [
                f"Stop {pain_point}",
                f"{target_audience}: read this",
                f"I went from {before} to {after}",
                f"The secret to {desired_outcome}"
            ],
            "success_metric": "CTR",
            "minimum_impressions": 1000
        },
        "visual_test": {
            "variable": "image_type",
            "variants": ["product_screenshot", "lifestyle_photo", "before_after", "text_overlay"],
            "success_metric": "thumb_stop_rate",
            "minimum_impressions": 2000
        },
        "cta_test": {
            "variable": "call_to_action",
            "variants": ["Start Free Trial", "Get Started", "Learn More", "See Pricing"],
            "success_metric": "conversion_rate",
            "minimum_impressions": 1000
        }
    }
    
    return tests
```

### Visual Brief Template
```markdown
## Ad Creative Brief

**Campaign:** {{campaign_name}}
**Platform:** {{platform}}
**Format:** {{dimensions}}
**Audience:** {{target_audience}}

### Concept
{{one_sentence_description_of_the_visual}}

### Visual Requirements
- **Hero image:** {{description}}
- **Text overlay:** {{max_5_words}}
- **Brand colors:** {{hex_codes}}
- **CTA button:** {{color}} / {{text}}

### References
- {{competitor_example_1}}
- {{competitor_example_2}}

### Do NOT
- No stock photos with fake smiles
- No more than 20% text overlay (Meta policy)
- No misleading claims
```

## Common Patterns

1. **Test hooks first** — The first line determines 80% of performance
2. **Refresh creative every 2-3 weeks** — Creative fatigue is real
3. **One variable per test** — Changing multiple things = unclear results
4. **UGC outperforms polished** — User-generated content feels more authentic
5. **Mobile-first design** — 80%+ of ad views are on mobile

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
