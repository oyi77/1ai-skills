---
name: product-desc
description: Use when writing product descriptions — e-commerce listings, SaaS feature copy, landing pages with short/medium/long variants, feature-benefit mapping, and bulk generation.
domain: content
tags: [content-creation, product]
version: 1.0.0
---

# Product Desc

Quick Reference — for full workflow see [../SKILL.md](../SKILL.md).

Product descriptions bridge the gap between "what it does" (features) and "why the buyer cares" (benefits). This sub-skill covers generating descriptions in three lengths — short for listings, medium for product pages, long for SEO landing pages — and bulk-generating across entire catalogues from structured data.

## Quick Start

1. **Map features to benefits** — Every feature gets a "which means" follow-up. E.g., "10GB storage (feature) which means 5,000 photos without hitting a limit (benefit)."
2. **Generate 3 variants** — Use `generate_product_description()` for short (80 chars), medium (200 words), and long (500+ words) formats.
3. **Bulk for catalogues** — Use `generate_bulk_descriptions()` with a list of product dicts for entire product lines.

## Key Function: Structured Product Description Generator

```python
def generate_product_description(
    product_name: str,
    features: list[str],
    benefits: list[str],
    audience: str,
    seo_keywords: list[str] = None,
) -> dict:
    """
    Generate structured product description with short, medium, and long variants.
    Returns { product, audience, short, medium, long }.
    """
    result = {"product": product_name, "audience": audience}

    # Short — social media / listing title / search snippet
    result["short"] = (
        f"{product_name} — {' • '.join(benefits[:3])}. "
        f"Perfect for {audience}."
    )

    # Medium — product page summary
    bullets = "\n".join(f"  ✓ {b}" for b in benefits)
    result["medium"] = f"""## {product_name}

Designed for {audience.lower()} who need {benefits[0].lower()}.

What you get:
{bullets}

### Key Features
{"\n".join(f"  • {f}" for f in features)}

Ready to {benefits[0].lower()}? Get {product_name} today.
"""

    # Long — SEO-optimized landing page
    seo_section = ""
    if seo_keywords:
        seo_section = (
            f"\n\n{product_name} is trusted by {audience.lower()} "
            f"for {', '.join(seo_keywords)}."
        )
    result["long"] = f"""# {product_name} — The Complete Solution for {audience}

{product_name} is purpose-built for {audience.lower()} who want {benefits[0].lower()}.

## Why Choose {product_name}?

{"\n".join(f"1. **{b}** — Our platform delivers {b.lower()} consistently."
           for b in benefits)}

## Features

{"\n".join(f"### {f}\nHow {product_name}'s {f.lower()} capability works for you."
           for f in features)}

## Get Started

Join thousands of {audience.lower()} using {product_name}.{seo_section}

[CTA: {benefits[0]} with {product_name}]"""
    return result


def generate_bulk_descriptions(products: list[dict], audience: str) -> str:
    """
    Generate descriptions for multiple products from structured data.
    Each product: { name, features: [], benefits: [], keywords: [] }
    Returns markdown with short + medium variants per product.
    """
    sections = ["# Product Descriptions\n"]
    for p in products:
        desc = generate_product_description(
            p["name"], p.get("features", []), p.get("benefits", []),
            audience, p.get("keywords"),
        )
        sections.append(
            f"---\n\n## {p['name']}\n\n### Short\n{desc['short']}\n\n"
            f"### Medium\n{desc['medium']}\n"
        )
    return "\n".join(sections)

# Feature-benefit rule: never list a feature without a benefit adjacent.
# Bad: "10GB storage"  Good: "10GB storage — hold 5,000 photos without upgrading."
```

## Verification Checklist

- [ ] 3 length variants generated: short (≤80 chars), medium (~200 words), long (500+ words)
- [ ] Every feature paired with a corresponding benefit
- [ ] SEO keywords integrated in long-form variant (H2s, body, CTA)
- [ ] Short variant works standalone as a product listing title
- [ ] Target audience specified and appears in all variants
- [ ] CTA matches the description length (short needs action verb; long needs multiple entry points)
- [ ] Bulk output has clean markdown separation between products

## Workflow

Execute these steps sequentially:

1. **Map features to benefits** — Every feature gets a "which means" follow-up. E.g., "10GB storage (feature) which means 5,000 photos without hitting a limit (benefit)."
2. **Generate 3 variants** — Use `generate_product_description()` for short (80 chars), medium (200 words), and long (500+ words) formats.
3. **Bulk for catalogues** — Use `generate_bulk_descriptions()` with a list of product dicts for entire product lines.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Only the description matters, not the format" | Short/medium/long serve different channels. Short drives clicks, medium educates, long converts. Skipping one loses a channel. |
| "Features are what sells" | Features describe; benefits persuade. "Waterproof to 50m" (feature) vs "Dive confidently without a dry bag" (benefit). |
| "Write one and copy-paste across channels" | Amazon, Shopify, and your landing page each need different length, tone, and keyword strategy. One version = leaving revenue on the table. |
| "Product copy doesn't affect SEO" | Product descriptions are often the most crawlable unique content on e-commerce sites. Thin or duplicated copy tanks rankings. |

## When to Use
Use this skill when writing product descriptions for e-commerce stores, SaaS landing pages, marketplace listings, Shopify/Amazon catalogues, or any product copy that needs feature-benefit mapping for conversion.
