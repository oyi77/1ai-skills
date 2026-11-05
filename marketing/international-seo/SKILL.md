---
name: international-seo
description: Use when implementing and auditing international SEO strategies for multi-regional or multi-lingual websites. Use for hreflang reciprocity audits, regional URL structure planning, and preventing duplicate content across locales.
domain: marketing
author: oyi77
license: Apache-2.0
subdomain: marketing
tags:
- growth
- marketing
- seo
- money
- internationalization
- i18n
triggers:
- international seo
- hreflang audit
- multi-lingual seo
- regional url strategy
- x-default
- locale seo
argument-hint: "[url_list]"
version: 1.0.0
category: marketing
---

# International SEO Skill

**Production-ready** automation for global search visibility and locale-specific optimization.

## Overview

International SEO optimizes websites to rank in multiple languages and regions by managing how search engines associate localized content. The core challenge is signal clarity: ensuring search engines understand which version of a page belongs to which user (locale) without triggering duplicate content penalties. This skill focuses on the technical implementation of hreflang, the strategic choice of URL structures, and the auditing of cross-regional reciprocity. `pip install requests beautifulsoup4` provides the runtime for the audit scripts in this skill.

## Money-Making Overview

**Buyer Persona:**
- Global E-commerce brands expanding into new markets
- Multi-national SaaS companies with localized pricing and landing pages
- Translation agencies offering SEO as a value-add
- Regional businesses targeting expats or tourists

**Pricing Tiers:**

| Tier | Price | Deliverable | Timeline |
|------|-------|---------------|-----------------|
| Global Signal Audit | $1,000 | Full hreflang reciprocity map and gap analysis | 3 days |
| Regional Strategy | $2,500 | URL structure recommendation and sitemap architecture | 1 week |
| International Retainer | $2,000/mo | Monthly locale health check and regional ranking monitoring | Ongoing |

**First-Dollar Timeline:**
- **Day 1**: Run the Hreflang Audit script. Find a "broken reciprocity" cluster.
- **Day 2**: Email the prospect about their conflicting regional signals.
- **Week 1**: Close a $1,000 Global Signal Audit.
- **Month 1**: Upsell into a Regional Strategy as they launch a third market.

## When to Use

**Trigger phrases:**
- "international seo": Best practices for multi-lingual and multi-regional sites
- "hreflang audit": Checking for reciprocity errors and missing x-default tags
- "Multi-lingual seo": Optimizing content for different languages in the same region
- "Regional URL strategy": Choosing between ccTLD, subdomains, or subdirectories
- "x-default": Implementing the fallback page for unmatched locales

- **Hreflang reciprocity audit**: Ensuring every localized page links to all other versions and back
- **URL structure planning**: Analyzing tradeoffs between ccTLD, subdomains, and subdirectories
- **Locale-specific optimization**: Tailoring metadata and content for regional search intent
- **Cross-locale duplicate management**: Managing near-duplicate content across similar languages
- **International sitemap architecture**: Implementing `xhtml:link` alternates in XML sitemaps

## Workflow

1. **Target Mapping**: Identify target regions/languages and map primary URLs.
2. **Signal Audit**: Run the Hreflang Reciprocity script to identify broken return links.
3. **Structure Selection**: Determine the optimal URL hierarchy (ccTLD vs Subdirectory) based on authority.
4. **Signal Implementation**: Deploy `<link rel="alternate">` and `x-default` tags.
5. **Sitemap Sync**: Mirror HTML tags in the XML sitemap using `xhtml:link`.
6. **Verification**: Use Search Console's International Targeting report to confirm signals.

## When NOT to Use

- When the site is single-language and single-region (use `seo-auditor`)
- Simple page translations without search intent optimization (use `seo-optimizer`)
- Pure translation/localization work (use `content-creator`)
- Local-only businesses with no international ambition (out of scope for `international-seo`)

## Anti-Rationalization Table

| Common "Fast" Shortcut | Why It Fails | Real Requirement |
|-------------------------|-----------------|------------------------------------------|
| IP-based Redirects | Blocks crawlers and ruins UX for VPN users | User-choice locale switchers + hreflang signals |
| Auto-translation (AI) | Produces "uncanny valley" text that kills E-E-A-T | Human review + locale-specific keyword research |
| Ignoring return-links | Google ignores the whole cluster if reciprocity is missing | Bidirectional mapping: A -> B AND B -> A |
| One-size-fits-all Meta | Ignores regional search intent and slang | Locale-specific title/description research |
| Flat URLs (/en/, /fr/) | Lacks regional granularity (Canada FR vs France FR) | ISO 639-1 language and ISO 3166-1 alpha-2 region codes |
| Assuming en == en-GB | Google treats en-US, en-GB, en-AU as distinct locales; auto-selecting en as generic collapses targeting | Declare both language and region (en-GB) when traffic differs materially |
| Mixing languages on one page | Googlebot uses the dominant language signal; mixed content gets filed under the wrong locale | One language per URL; never machine-translate nav while keeping body in source language |

## Key Concepts

### hreflang Reciprocity and x-default

hreflang tells search engines which localized version of a page to serve. The reciprocity rule is non-negotiable: if page A says "B is the German version," page B must say "A is the English version." If ANY page in the cluster is missing its return link, Google silently drops THE ENTIRE CLUSTER and falls back to guesswork. Every page must also link to itself with its own hreflang.

x-default is the fallback for users whose language/region does not match any declared locale (e.g., a visitor from Spain landing on a site with only en-US and en-GB). It must be a real, indexable landing page — usually a language selector — never a redirect to a single locale.

Language codes are ISO 639-1 lowercase; region codes are ISO 3166-1 alpha-2 uppercase. The trap: `en-us` (lowercase region) is INVALID and Google will ignore it. Correct forms: `en` (language only), `en-GB` (language-region). Note GB not UK. `en` alone and `en-GB` together are redundant but not harmful.

### URL Structure Strategy (Tradeoffs)

- **ccTLD (example.fr)**: Strongest geo-targeting signal, highest trust in-market, but splits link equity across domains, multiplies hosting/SSL cost, and requires separate Search Console properties. Best when budget is high and market is large.
- **Subdomain (fr.example.com)**: Clean separation, easy to host separately, but link equity sharing with root is weaker than subdirectory. Search Console treats as separate property. Mid-cost.
- **Subdirectory (example.com/fr/)**: Consolidates all authority into one domain, cheapest to maintain, easiest analytics. Weakest explicit geo signal — must compensate with hreflang + country targeting. Best default for most brands.

Avoid IP-based auto-redirects: crawlers get redirected too (Googlebot crawls from US IPs, so a French-targeted redirect hides your French content from Google), and VPN users bounce. Use visible locale switchers + hreflang instead.

### Sitemap Structure per Locale

Each locale sitemap lists only its own URLs, but each `<url>` entry includes `<xhtml:link rel="alternate" hreflang="..." href="..." />` for every locale. This gives engines a second discovery path when HTML parsing fails. A global master sitemap index pointing at per-locale sitemaps keeps crawl budget clean. Never mix hreflang logic in separate per-locale sitemaps without cross-references — that defeats the purpose.

### Duplicate Content Across Locales

Near-duplicate content (en-US vs en-GB, or en vs en-au) is NOT automatically penalized if hreflang clusters are intact. Use `rel="canonical"` to a stronger sibling ONLY when content is genuinely identical AND you want one to rank; otherwise let each locale self-canonicalize. Do not canonicalize a locale you want ranking. Auto-translated content without human review produces "uncanny valley" text that fails E-E-A-T — human review plus locale-specific keyword research is required.

### RTL, CJK, and Locale-Visible Defects

- Arabic/Hebrew: set `dir="rtl"` on `<html>` AND in CSS; flip margins/padding; test numerals (Arabic-Indic vs Western digits); verify date formats (dd/mm/yyyy in many locales vs mm/dd/yyyy US).
- CJK: line-breaking differs (Chinese allows break at any character, Japanese at word boundaries); set `lang` and `hyphens` correctly; verify fonts don't render as boxes.
- Formats: ISO dates in meta are fine, but visible dates and number formats must match locale conventions (German decimal comma, thousand separator space, currency symbol placement). These are SEO-visible defects because users bounce and UX signals degrade.

### Audit Method

A crawler fetches every URL, parses `<link rel="alternate" hreflang>`, and checks reciprocity. The core invariant: for every pair (A, B) where A links B via hreflang, B must list A. Report broken pairs, missing self-links, missing x-default, invalid casing, and unreachable targets separately.

## First Action in 60 Minutes

Run a Hreflang Reciprocity Audit. This script fetches a list of URLs, parses their hreflang tags, and identifies "broken clusters" where a page points to a locale version that does not point back.

```python
#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def audit_hreflang(urls):
    # Audit hreflang reciprocity.
    # A cluster is broken if Page A links to Page B via hreflang,
    # but Page B does not link back to Page A.
    results = {}
    for url in urls:
        try:
            print(f"Fetching {url}...")
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')

            # Extract all hreflang links
            links = soup.find_all('link', rel='alternate', hreflang=True)
            extracted = {l['hreflang']: l['href'] for l in links}
            results[url] = extracted
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            results[url] = None

    # Check reciprocity
    broken_clusters = []
    for url, links in results.items():
        if not links:
            continue
        for locale, target in links.items():
            # Validate casing: language lowercase, region uppercase
            if '-' in locale:
                lang, region = locale.split('-', 1)
                if not (lang.islower() and region.isupper()):
                    broken_clusters.append(f"Bad casing: {url} hreflang='{locale}'")
            if target == url:
                continue  # Self-link is fine

            # Check if target points back to current url
            target_links = results.get(target)
            if target_links:
                if url not in target_links.values():
                    broken_clusters.append(f"Broken: {url} -> {target} (Missing return link)")
            else:
                broken_clusters.append(f"Unreachable: {url} -> {target} (Target not fetched)")

    # x-default check
    for url, links in results.items():
        if links and 'x-default' not in links:
            broken_clusters.append(f"Missing x-default on {url}")

    return broken_clusters

if __name__ == "__main__":
    test_urls = [
        "https://example.com/en/",
        "https://example.com/en-gb/",
        "https://example.com/de/",
    ]
    issues = audit_hreflang(test_urls)
    for issue in issues:
        print(issue)
```

## Verification

1. **Reciprocity Check**: For every `<link rel="alternate" hreflang="x" href="URL_X">` on Page A, Page X must list A. One missing return link voids the whole cluster.
2. **x-default Validation**: Confirm a default version exists for unmatched regions; it must be indexable and not a forced redirect.
3. **Casing Audit**: regex `^[a-z]{2}(-[A-Z]{2})?$` against every hreflang value; reject `en-us` and `EN-GB`.
4. **Sitemap Sync**: Cross-reference `<xhtml:link>` alternates in per-locale sitemaps with HTML head tags; counts must match.
5. **Self-link presence**: every localized page must include itself in its own hreflang cluster.
6. **Locale-visible defects**: spot-check RTL (`dir="rtl"`), CJK line-breaking, locale date/number formats on rendered pages.
