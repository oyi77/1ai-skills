---
name: ad-creative
description: Ad creative production — visual briefs, copy variations, and A/B testing frameworks for performance advertising. Use when working with ad creative.
version: 2.0.0
domain: marketing
tags:
- creative
- growth
- marketing
- seo
- testing
- money
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
**Trigger phrases:**
- "ad creative"
- "Ad creative production — visual briefs, copy variations, and A/B testing framewo"


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

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Good products sell themselves" | They do not. Marketing is how people discover your product. |
| "I will start marketing after launch" | Build audience before launch. Pre-launch momentum is critical. |
| "SEO is dead" | SEO evolves. GEO (Generative Engine Optimization) is the new frontier. |

## Money-Making Overview

Produce ad creative that converts. Creative quality is the #1 lever in ad performance — well-optimized creative can 2-5x ROAS compared to generic ads. This skill covers the complete ad creative production pipeline: audience-aware copywriting using proven frameworks, visual brief generation for designers, structured A/B testing matrices, and performance analysis. Expect **$500-10K/month** producing creative for 2-5 clients.

## Revenue Streams

### Creative-as-a-Service ($500-5K/month/client)
Ongoing retainer for ad creative production:
- **Starter** (1 platform, 5 variations/week, 2 rounds revisions): $500-1K/month
- **Growth** (2 platforms, 10 variations/week, visual briefs + copy): $1.5-3K/month
- **Scale** (3+ platforms, 20+ variations/week, full creative studio including UGC scripts): $3-5K/month
- **Enterprise** (All platforms, unlimited variations, dedicated creative strategist, weekly performance reviews): $5-10K/month

### Creative Testing Arbitrage ($1-5K/month)
Run small-budget A/B tests for clients, identify winning creatives, then scale. Charge testing fee + performance bonus or rev-share on media spend.
- Testing retainer: $1-2K/month (5-10 tests)
- Performance bonus: 10-20% of incremental lift in ROAS

### Ad Copy for Agencies ($200-1K/client/project)
White-label ad copy for marketing agencies that lack in-house copywriters.
- Single campaign copy pack (5 headlines, 3 descriptions, 3 CTAs): $200-400
- Full funnel copy (TOF/MOF/BOF, retargeting, email): $500-1K

### Creative Templates & Shop ($100-2K/month passive)
Pre-built, platform-optimized creative templates (Canva, Figma, Photoshop):
- Template packs ($29-99 each): 10+ ad templates per platform
- Monthly subscription ($49-149/month): new templates weekly
- Custom template libraries for agencies ($500-2K setup + monthly)

## Pricing Packages

| Package | Price | What's Included |
|---|---|---|
| **Copy Only** | $200-500/project | 5-10 copy variations using AIDA/PAS/4U, platform-formatted, 2 rounds revisions |
| **Creative Brief** | $300-800/project | Full visual brief with references, copy, sizing specs, testing matrix |
| **Creative Studio** | $1-3K/month | 10-20 variations/week, visual briefs, copy, testing plan, performance report |
| **Full Funnel** | $2-5K/month | TOF/MOF/BOF creative, retargeting, email sequences, landing page copy |
| **Agency White-Label** | $500-2K/month | Unlimited copy, white-labeled, direct Slack integration, 24h turnaround |

## Client Acquisition Script

```
Subject: Your ad ROAS is leaving money on the table

Hi {{name}},

I noticed {{company}}'s ads on {{platform}}. The targeting looks solid, but the
creative is leaving 40-60% of potential conversions on the table.

We've helped {{similar_client}} improve ROAS by {{3.2x}} just by optimizing their
ad creative — same audience, same offer, better messaging and visuals.

I'd love to run a free creative audit of your current ads. No strings attached —
just a 15-min look at your top 3 ads with specific recommendations.

When's a good time for a quick call?

Best,
{{your_name}}
```

## First Action in 60 Minutes

Generate 5 ad copy variants using AIDA, PAS, and 4U frameworks from any product description. Run this script, paste your product info, and get platform-formatted copy ready to launch:

```python
#!/usr/bin/env python3
"""Generate 5 ad copy variants from a product description."""

import sys

PRODUCT = {
    "name": "ProductName",
    "description": "A short description of what it does",
    "pain_point": "The main problem it solves",
    "target_audience": "Who it's for",
    "benefit": "The key benefit",
    "result": "What users achieve",
    "unique_feature": "What makes it different",
    "social_proof": "Numbers (users, reviews, ratings)",
    "offer": "Special offer or discount",
    "deadline": "Offer deadline",
    "metric": "Specific improvement metric",
    "specific_number": "e.g. 47%",
    "resource_type": "Free guide, checklist, template",
    "before": "Before state",
    "after": "After state",
    "cost": "What the problem costs (time/money)",
    "solution": "Product name",
    "timeframe": "How fast it works"
}


def aida(p):
    return {
        "attention": f"Still struggling with {p['pain_point']}?",
        "interest": f"{p['name']} helps {p['target_audience']} {p['benefit']}",
        "desire": f"Join {p['social_proof']} who already {p['result']}",
        "action": "Start your free trial \u2192"
    }


def pas(p):
    return {
        "problem": f"{p['pain_point']} is costing you {p['cost']}",
        "agitation": f"Every day without {p['solution']}, you lose {p['metric']}",
        "solution": f"{p['name']} fixes this in {p['timeframe']}"
    }


def four_u(p):
    return {
        "urgent": f"Limited: {p['offer']} ends {p['deadline']}",
        "unique": f"Only {p['name']} has {p['unique_feature']}",
        "ultra_specific": f"{p['specific_number']}% improvement in {p['metric']}",
        "useful": f"Free {p['resource_type']} inside"
    }


def format_for_meta(lines):
    """Primary text up to 125 chars, headline up to 40 chars."""
    return "\n".join(f"[{k.upper()}] {v[:125]}" for k, v in lines.items())


def format_for_google(lines):
    """Google Responsive: 30-char headlines, 90-char descriptions."""
    return "\n".join(
        f"[{k.upper()}] Headline: {v[:30]} | Desc: {v[:90]}"
        for k, v in lines.items()
    )


def format_for_linkedin(lines):
    """LinkedIn: professional tone, 600-char max."""
    return "\n".join(
        f"[{k.upper()}] {v[:600]}"
        for k, v in lines.items()
    )


def generate_all(product):
    frameworks = {
        "AIDA": aida(product),
        "PAS": pas(product),
        "4U": four_u(product),
    }
    output = []
    for platform, fmt in [
        ("Meta (FB/IG)", format_for_meta),
        ("Google Ads", format_for_google),
        ("LinkedIn", format_for_linkedin),
    ]:
        output.append(f"\n=== {platform} ===")
        for name, copy in frameworks.items():
            output.append(f"\n--- {name} ---")
            output.append(fmt(copy))
    return "\n".join(output)


if __name__ == "__main__":
    # Override with your product info
    product = dict(PRODUCT)
    product["name"] = input("Product name: ") or product["name"]
    product["description"] = input("Description: ") or product["description"]
    product["pain_point"] = input("Pain point it solves: ") or product["pain_point"]
    product["target_audience"] = input("Target audience: ") or product["target_audience"]
    product["benefit"] = input("Key benefit: ") or product["benefit"]
    product["result"] = input("What users achieve: ") or product["result"]
    product["unique_feature"] = input("Unique feature: ") or product["unique_feature"]
    product["social_proof"] = input("Social proof (numbers): ") or product["social_proof"]
    product["offer"] = input("Offer: ") or product["offer"]

    print(generate_all(product))
```

**To use:** `python3 ad_copy_generator.py` and answer the prompts. Output is ready to paste into Meta Ads Manager, Google Ads, or LinkedIn Campaign Manager.

## Output Format

When delivering ad creative, structure results as:

```json
{
  "campaign": "Campaign Name",
  "platform": "meta | google | linkedin | tiktok",
  "objective": "awareness | consideration | conversion",
  "variants": [
    {
      "framework": "AIDA | PAS | 4U",
      "headline": "Primary headline text",
      "primary_text": "Main ad body copy",
      "cta": "Call to action button text",
      "visual_brief": "Brief description of visual concept",
      "estimated_character_count": 125
    }
  ],
  "testing_matrix": {
    "test_1": {"variable": "hook", "variants": ["A", "B", "C", "D"], "metric": "CTR", "min_impressions": 1000},
    "test_2": {"variable": "visual", "variants": ["lifestyle", "product", "ugc"], "metric": "thumb_stop_rate", "min_impressions": 2000}
  },
  "performance_targets": {
    "ctr_benchmark": "1-3%",
    "cvr_benchmark": "2-5%",
    "roas_target": "3x+"
  }
}
```