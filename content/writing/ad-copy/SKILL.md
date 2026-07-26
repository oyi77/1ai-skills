---
name: ad-copy
description: Use when writing ad copy for paid media — Facebook, Google, LinkedIn, TikTok ads with hook strategy, variant generation, and platform optimization.
domain: content
tags: [content-creation, copy]
version: 1.0.0
---

# Ad Copy

Quick Reference — for full workflow see [../SKILL.md](../SKILL.md).

Ad copy is the highest-leverage content type: the right hook can double CTR overnight. This sub-skill covers generating 5-hook ad variants (problem, result, curiosity, social, urgency) and matching them to platform-specific best practices for Meta, Google, LinkedIn, and TikTok.

## Quick Start

1. **Brief** — Define product, audience, 3-5 key benefits, CTA, and target platform using the `ContentBrief` dataclass (see parent).
2. **Generate variants** — Run `generate_ad_variants()` to produce 5 hook-based versions.
3. **Select & optimize** — Pick the strongest variant for each platform's format (e.g., curiosity for LinkedIn, urgency for Facebook).

## Key Function: Ad Copy with Hook Strategy

```python
def generate_ad_variants(
    product: str,
    audience: str,
    benefits: list[str],
    cta: str,
    platform: str = "facebook",
) -> list[dict]:
    """
    Generate 5 ad copy variations using different hooks.
    Returns list of { headline, body, cta } dicts.
    """
    hooks = {
        "problem": f"Stop {audience.lower()} from losing money on {product.lower()}.",
        "result": f"Get {benefits[0].lower()} — starting today.",
        "curiosity": f"Most {audience.lower()} don't know about this {product.lower()} secret.",
        "social": f"Join {audience.lower()} who switched to {product.lower()}.",
        "urgency": f"Last chance to get {benefits[0].lower()} with {product.lower()}.",
    }

    def compile_body(hook: str) -> str:
        bullets = "\n".join(f"  ✓ {b}" for b in benefits)
        bodies = {
            "problem": f"Are you {audience.lower()} tired of:\n{bullets}\n\n{product} fixes all of that.",
            "result": f"What if you could {benefits[0].lower()}?\n\n{product} makes it possible:\n{bullets}",
            "curiosity": f"Here's what most {audience.lower()} get wrong.\n\nThe truth:\n{bullets}",
            "social": f"{len(benefits)} reasons {audience.lower()} choose {product}:\n{bullets}",
            "urgency": f"Limited time.\n\n{product} delivers {benefits[0].lower()}:\n{bullets}",
        }
        return bodies.get(hook, bullets)

    return [
        {"variant": h, "headline": hl, "body": compile_body(h), "cta": cta, "platform": platform}
        for h, hl in hooks.items()
    ]

# Platform-specific tips:
# - Facebook: problem & urgency hooks, short body, strong visual
# - Google Ads: result hook, keyword-rich headline, 30-char limit
# - LinkedIn: curiosity & social hooks, professional tone, longer body
# - TikTok: urgency hook, conversational tone, hook in first 3 seconds
```

## Verification Checklist

- [ ] 5 distinct hook types generated (problem, result, curiosity, social, urgency)
- [ ] Each variant has headline, body, and CTA
- [ ] Platform-specific character limits respected (e.g., Google headline ≤30 chars)
- [ ] Benefits are concrete outcomes, not features
- [ ] CTA is specific, trackable (UTM), and appears once per variant
- [ ] No jargon or insider language — speaks directly to audience pain
- [ ] Variant copy is distinct enough for A/B testing

## Workflow

Execute these steps sequentially:

1. **Brief** — Define product, audience, 3-5 key benefits, CTA, and target platform using the `ContentBrief` dataclass (see parent).
2. **Generate variants** — Run `generate_ad_variants()` to produce 5 hook-based versions.
3. **Select & optimize** — Pick the strongest variant for each platform's format (e.g., curiosity for LinkedIn, urgency for Facebook).

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "More words = more convincing" | The best ads are ruthlessly short. Every extra word costs attention. Aim for ≤50 words per variant. |
| "One great ad is enough" | Even the best ad fatigues after ~7 days. You need 5+ variants to rotate and the data to pick the winner. |
| "All platforms are the same" | Facebook rewards urgency, LinkedIn rewards authority, Google rewards specificity. One-size ads lose 30-50% efficiency. |
| "The product sells itself" | Copy is the difference between scroll and click. Every benefit needs to be a felt outcome, not a feature spec. |

## When to Use
Use this skill when writing ad copy for paid social campaigns, search ads, display ads, or any performance marketing that needs multi-variant testing.
