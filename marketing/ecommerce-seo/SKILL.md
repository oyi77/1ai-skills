---
name: ecommerce-seo
description: Use when optimizing e-commerce stores for search engines. Focus on faceted navigation, product schema, variant canonicalization, and crawl budget management for large catalogs.
domain: marketing
author: oyi77
license: Apache-2.0
subdomain: marketing
tags:
- growth
- ecommerce
- marketing
- seo
- money
triggers:
- ecommerce seo
- faceted navigation seo
- product schema optimization
- ecommerce crawl budget
- product variant canonicalization
- out of stock seo strategy
argument-hint: "[store_url]"
version: 1.0.0
category: marketing
---

# Ecommerce SEO Skill

**Production-ready** automation for high-volume store visibility and conversion.

## Overview

Ecommerce SEO differs from content SEO by the scale of pages and the complexity of internal linking. The primary battle is the "Crawl Budget": ensuring Google spends its limited resources on high-value product pages rather than millions of useless facet combinations (e.g., "blue shirt size M color navy"). This skill focuses on faceted navigation control, merchant rich results, and the lifecycle management of product URLs. `pip install requests beautifulsoup4 lxml` provides the runtime for the audit scripts in this skill.

## Money-Making Overview

**Buyer Persona:**
- Shopify/Magento/WooCommerce store owners ($100K–$5M revenue) with 1,000+ SKUs
- Head of Growth at D2C brands struggling with "indexing bloat"
- Ecommerce agencies specializing in technical SEO for large catalogs
- Marketplace operators managing thousands of vendor-submitted pages

**Pricing Tiers:**

| Tier | Price | Deliverable | Timeline |
|------|-------|---------------|-----------------|
| Indexing Cleanup | $1,500 | Facet audit + robots.txt/noindex strategy to kill index bloat and recover crawl budget. | 1 week |
| Merchant-Rich Setup | $1,000 | Implementation of Product/Offer schema for all categories + Rich Result validation. | 3 days |
| Store Growth Retainer | $2,500/mo | Monthly keyword gap analysis for product categories + landing page optimization for long-tail variants. | Ongoing |

**First-Dollar Timeline:**
- **Day 1**: Run a crawl budget check. Find a store indexing 50k pages but not 1k are "money pages".
- **Day 2**: Send a screenshot of the "Indexed vs. Valuable" gap. "You're paying Google to crawl filters, not products."
- **Week 1**: Close a $1,500 Indexing Cleanup engagement.
- **Month 1**: Upsell to a Retainer to build "Category Power Pages" for high-volume search terms.

## When to Use

**Trigger phrases:**
- "ecommerce seo": Best practices for high-volume product catalogs
- "Faceted navigation seo": Managing filters to prevent index bloat
- "Product schema": implementing Merchant rich results (price, availability, reviews)
- "Product variants": Canonicalizing color/size versions without losing long-tail traffic
- "Out-of-stock strategy": Managing 404 vs 410 vs 200 for discontinued items

- **Faceted navigation control**: Using robots.txt or noindex to prevent "facet-bombing" the index
- **Merchant rich results**: Implementing Product, Offer, and AggregateRating schema
- **Variant canonicalization**: Deciding when a variant deserves its own URL vs being a canonical child
- **Product lifecycle management**: Handling discontinued products to preserve link equity
- **Category page optimization**: Turning "Product Listing Pages" (PLPs) into authoritative guides

## Workflow

1. **Index Bloat Audit**: Analyze GSC to find faceted URLs leaking into the index.
2. **Facet Logic Mapping**: Define which filter combinations are "money" vs "junk".
3. **Blocking Implementation**: Deploy robots.txt `disallow` or `noindex` tags.
4. **Schema Deployment**: implement Product and Offer JSON-LD for all catalog items.
5. **Variant Canonicalization**: Apply canonical tags to a primary SKU for low-volume variants.
6. **Monitoring**: Track "Crawl Budget" usage via log file analysis.

## When NOT to Use

- When the store has < 50 products (standard `seo-auditor` is enough)
- For pure conversion rate optimization (CRO) without search intent (use conversion skills)
- When the task is about paid shopping ads (use `paid-ads`)
- For managing inventory or logistics (use operations)

## Anti-Rationalization Table

| Common "Fast" Shortcut | Why It Fails | Real Requirement |
|-------------------------|-----------------|------------------------------------------|
| robots.txt for everything | `disallow` prevents crawling, so `noindex` is never seen | Use `noindex` for pages that should be removed from index |
| Generic Product Schema | Missing `priceCurrency` or `availability` triggers Merchant Center warnings | Valid Product/Offer schema with mandatory Merchant properties |
| 404 for Out-of-Stock | Kills long-tail traffic and creates 404 spikes in GSC | 200 OK with `availability: OutOfStock` + recommended alternatives |
| Global Canonical | Canonicalizing all variants to one "Main" product kills long-tail variant queries | Selective canonicals: keep high-volume variants (e.g. "Red Leather Shoe") indexed |
| Flat Category Tree | Pushes deep products too far from the root (too many clicks) | Strategic internal linking + Breadcrumbs for link equity flow |

## Key Concepts

### Faceted Navigation: noindex vs disallow Trap

Faceted pages (color, size, price sort) explode the crawl graph. The trap: disallowing a URL in robots.txt means Google never crawls it, so a `noindex` in the HTML head is never seen — the page STAYS indexed. Decision rule:

- Allow crawl + `noindex, follow` on thin facet combinations you want link equity to pass through (rare; most facets should be disallowed outright).
- `disallow` in robots.txt for facet combinations that would never rank and waste budget; but this leaves already-indexed facet URLs stuck in index until Google naturally drops them.
- `rel="canonical"` facet URLs back to the base category PLP when the facet is a re-sort (sort=price-low), not a unique inventory slice.

Crawl-budget math: if Googlebot has ~10k fetches/day and a store has 5k real products plus 200k facet URLs, 97% of budget goes to facets. Disallow all facet combinations except the intersection pages you actively build as landing pages (e.g., "men's red shoes").

### Product Schema: offers, availability, price/priceCurrency

Merchant rich results require valid Product with an Offer (or AggregateOffer). Mandatory for eligibility:

- `name`, `image` (array of URLs), one of `brand`, `sku`, `mpn`, or `gtin`.
- `offers` object with `@type: Offer`, `price` (numeric string), `priceCurrency` (ISO 4217, e.g. USD), `availability` (http://schema.org/InStock|OutOfStock|PreOrder|BackOrder|Discontinued), and `url` pointing to the product page.
- `aggregateRating` only if real reviews exist (posting fake ratings = manual action). `review` entries need author and datePublished.

Wrap the JSON-LD in a `<script type="application/ld+json">` in the head. Validate with Google's Rich Results Test before deploy; Merchant Center rejects listings missing price or availability.

### Variant Canonicalization Decision Rule

Variants (color/size) should keep separate URLs only when there is demonstrated search demand for that exact variant (e.g., "red leather Chelsea boot" vs "black suede Chelsea boot") — check GSC query data for variant-qualified long-tail keywords. Rule:

- If variant-level monthly searches > 0 AND the variant has unique primary image/meta: self-canonicalize (index separately).
- Otherwise: canonical all variants to the parent product URL; reflect the selected variant via URL parameter (`?color=red`) with a canonical to the clean product page.
- Never canonicalize every variant to a single "primary" color when colors are distinct products (Google will drop the non-primary variants from index and you lose long-tail).

### Out-of-Stock, Discontinued, and Seasonal Products

- **Temporarily out of stock**: keep the product page 200 OK with `availability: OutOfStock`, show "back in stock soon" + email capture, and `rel="alternate"` to a substitute. Never 404.
- **Discontinued permanently**: 410 Gone is ideal (Signals finality, preserved crawl budget) — but only after confirming zero internal links or traffic. If the URL has backlinks, keep a 200 page with `availability: Discontinued` and recommend alternatives to preserve link equity.
- **Seasonal rotation**: keep page 200 with `OutOfStock`, refresh content/markup with the season, or canonicalize to the evergreen category if no near-term return.
- **404 vs 410**: 404 is "might come back"; 410 is "gone forever". Google recrawls 410s less often, saving budget.

### Category Pages (PLPs)

Category pages are the primary ranking assets. Make them authoritative: H1 with primary category keyword, 150–300 words of editorial content above the grid, faceted links as visible filters (but not indexable facet URLs), and BreadcrumbList schema. Avoid infinite scroll without pagination links (`rel=next` is deprecated but canonical-to-page-1 still useful for thin sorts).

## First Action in 60 Minutes

Audit a store's "indexing bloat" by checking if faceted URLs are leaking into the index. A simple probe of `site:domain.com/filter` often reveals thousands of useless pages.

```python
#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

def audit_ecommerce_bloat(url):
    # Check for faceted navigation bloat.
    # Detects if common filter patterns are indexed and causing bloat.
    common_filters = ['filter', 'facet', 'sort', 'color', 'size', 'price', 'category']
    bloat_detected = False

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')

        # Check for internal links that look like facets
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            if any(f in href.lower() for f in common_filters):
                print(f"Facet link found: {href}")
                bloat_detected = True

        if not bloat_detected:
            print("No obvious facet links found in the homepage.")
        else:
            print("Faceted navigation detected. Check GSC to see if these are indexed.")

    except Exception as e:
        print(f"Error auditing store: {e}")

if __name__ == "__main__":
    target = "https://example.com"
    audit_ecommerce_bloat(target)
```

## Verification

1. **Facet-Index Gap**: Check Google Search Console "Indexed" vs "Not Indexed" for URLs containing filter parameters. Fewer indexed than total fetched = bloat cleanup working.
2. **Rich Result Validation**: Run product pages through Google Rich Results Test; `offers` and `price` must validate, no Merchant Center warnings.
3. **Variant Canonical Check**: Select a high-volume variant and confirm it self-canonicalizes; low-volume variants canonicalize to parent.
4. **Product Lifecycle Audit**: Discontinued product returns 410 (or 200 with `availability: Discontinued` + alternatives); temporarily OOS returns 200 with `OutOfStock`.
5. **robots.txt vs noindex Trap Check**: Crawl one disallowed-but-noindexed URL; if Googlebot blocks it, noindex will never be seen — confirm the strategy matches the chosen blocking level.
6. **Breadcrumb Integrity**: Every product page has a valid BreadcrumbList schema and a logical path back to the category root.
