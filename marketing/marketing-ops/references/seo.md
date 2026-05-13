# SEO Mode Reference

## Table of Contents
1. [Technical SEO Audit](#technical-seo-audit)
2. [Keyword Research](#keyword-research)
3. [On-Page Optimization](#on-page-optimization)
4. [Content SEO](#content-seo)
5. [Schema & Structured Data](#schema--structured-data)
6. [Link Strategy](#link-strategy)
7. [GEO - Generative Engine Optimization](#geo---generative-engine-optimization)

---

## Technical SEO Audit

### Audit Checklist (70+ checkpoints)

**Crawlability & Indexation**
- robots.txt: accessible, not blocking important pages
- XML sitemap: exists, submitted to GSC, no errors, auto-updated
- Crawl budget: no infinite parameter URLs, proper pagination
- Canonical tags: self-referencing, no conflicts with redirects
- Hreflang: correct for multi-language sites
- Index coverage: check GSC for excluded pages and reasons
- Noindex/nofollow: intentional usage only

**Site Performance**
- Core Web Vitals: LCP < 2.5s, INP < 200ms, CLS < 0.1
- Page speed: mobile + desktop scores
- Image optimization: WebP/AVIF, proper sizing, lazy loading
- Font loading: font-display: swap, preload critical fonts
- JavaScript: defer non-critical, no render-blocking
- CDN usage: static assets served from CDN
- Compression: Gzip/Brotli enabled

**Mobile Optimization**
- Mobile-first indexing compliance
- Responsive design (no separate mobile URLs ideally)
- Touch targets: minimum 48x48px
- No horizontal scrolling
- Viewport meta tag present

**Architecture**
- URL structure: clean, descriptive, keyword-relevant
- Internal linking: hub-and-spoke, no orphan pages
- Navigation depth: important pages within 3 clicks
- Breadcrumbs: present and schema-marked
- 404 handling: custom page, not blank
- Redirect chains: max 1 hop (no chains of 3+)
- HTTPS: entire site, no mixed content

**Content Quality Signals**
- Thin content pages (< 300 words without purpose)
- Duplicate content (internal and external)
- Keyword cannibalization: multiple pages targeting same keyword
- Content freshness: last-modified dates, update frequency

### Audit Report Format

```markdown
# SEO Audit Report — {domain}
**Date:** {date}
**Audited by:** Claude Marketing Ops

## Executive Summary
{Overall health score: A-F}
{Top 3 critical issues}
{Estimated traffic impact of fixing}

## Critical Issues (Fix Immediately)
{Issues with HIGH impact that are blocking performance}

## Warnings (Fix This Quarter)
{Medium-priority items}

## Opportunities (Growth Potential)
{Items that could improve rankings/traffic}

## Quick Wins (Under 1 Hour Each)
{Low-effort, high-impact fixes}

## Detailed Findings
{Category-by-category breakdown}

## Action Plan
{Prioritized roadmap with effort estimates}
```

---

## Keyword Research

### Research Methodology

1. **Seed keywords** — Start with 5-10 core terms the business should rank for
2. **Expand** — Use modifiers: how to, best, vs, for, near me, {year}
3. **Intent classification:**
   - **Informational** — "how to," "what is," "guide" → Blog posts, guides
   - **Navigational** — brand + feature → Landing pages
   - **Commercial** — "best," "vs," "review," "top" → Comparison pages
   - **Transactional** — "buy," "pricing," "sign up" → Product/pricing pages
4. **Difficulty assessment** — Domain authority, competition, SERP features
5. **Opportunity scoring** — Volume × (1 - difficulty) × business relevance

### Keyword Mapping Template

```
| Keyword | Volume | Difficulty | Intent | Target URL | Status |
|---------|--------|-----------|--------|-----------|--------|
| {kw}    | {vol}  | {1-100}   | {type} | {url}     | {new/existing/gap} |
```

### Long-tail Strategy
For smaller/newer sites, prioritize:
- 3-5 word phrases with clear intent
- Question-based keywords (People Also Ask)
- Location + service combinations (local SEO)
- Niche modifiers competitors ignore

---

## On-Page Optimization

### Page-Level Checklist

| Element | Best Practice |
|---------|--------------|
| **Title tag** | Primary keyword + modifier, under 60 chars, compelling |
| **Meta description** | Action-oriented, includes keyword, 120-155 chars, unique per page |
| **H1** | One per page, includes primary keyword, matches search intent |
| **H2-H3** | Semantic keywords, logical hierarchy, every 200-300 words |
| **URL slug** | Short, keyword-rich, hyphens not underscores |
| **First paragraph** | Primary keyword within first 100 words |
| **Image alt text** | Descriptive, keyword where natural, under 125 chars |
| **Internal links** | 3-5 contextual links to related pages |
| **External links** | 2-3 to authoritative sources (opens in new tab) |
| **Content length** | Matches or exceeds top-ranking competitors for that keyword |
| **Featured snippet** | Answer target question directly in 40-50 words |

### Title Tag Formulas
- `{Primary Keyword}: {Benefit} | {Brand}` — "Email Marketing: 10x Your Open Rates | MailPro"
- `How to {Keyword} in {Year} ({Modifier})` — "How to Write Ad Copy in 2026 (With Templates)"
- `{Number} {Keyword} {Promise}` — "15 SEO Tips That Actually Work"
- `{Keyword} vs {Alternative}: {Value}` — "Mailchimp vs ConvertKit: Full Comparison"

---

## Content SEO

### Content Brief Template

```markdown
# Content Brief: {Title}

**Target keyword:** {primary}
**Secondary keywords:** {3-5 related terms}
**Search intent:** {informational/commercial/transactional}
**Funnel stage:** {TOFU/MOFU/BOFU}
**Target word count:** {based on SERP analysis}

## SERP Analysis
- Top 3 results analysis: {what they cover, angles, gaps}
- Featured snippet opportunity: {yes/no, format}
- People Also Ask: {list of PAA questions to address}

## Outline
{H2/H3 structure with content notes per section}

## Unique Angle
{What makes this piece different from existing top results}

## Internal Linking Targets
{3-5 existing pages to link to/from}

## CTA
{What action should the reader take after reading}
```

---

## Schema & Structured Data

### Common Schema Types

| Page Type | Schema | Priority |
|-----------|--------|----------|
| Home page | Organization, WebSite, SearchAction | High |
| Blog post | Article, BreadcrumbList | High |
| Product page | Product, Review, Offer | High |
| FAQ page | FAQPage | High |
| How-to guide | HowTo | Medium |
| Local business | LocalBusiness | High |
| Event | Event | Medium |
| Video page | VideoObject | Medium |

Generate clean JSON-LD that passes Google's Rich Results Test.
Always validate output at: https://search.google.com/test/rich-results

---

## Link Strategy

### Internal Linking Rules
- Every new page links to 3-5 related existing pages
- Update 3-5 existing pages to link to each new page
- Use descriptive anchor text (not "click here")
- Hub pages should link to all spoke pages in their topic cluster
- Check for orphan pages monthly

### External Link Building Approaches (Ethical only)
- Create genuinely useful tools, calculators, templates
- Original research and data studies
- Expert roundups and collaborative content
- Guest posting on relevant, quality publications
- HARO / journalist queries
- Broken link building (find 404s, offer your content as replacement)

---

## GEO - Generative Engine Optimization

### Optimizing for AI Search (ChatGPT, Perplexity, Gemini, Claude)

AI models cite and surface content that is:
- **Authoritative** — from recognized brands/experts in the field
- **Structured** — clear headings, concise answers, well-organized
- **Factual** — data-backed, sourced, verifiable claims
- **Direct** — answers questions concisely before elaborating
- **Comprehensive** — covers topics thoroughly without fluff

### GEO Tactics
- Answer questions directly in the first 50 words of each section
- Use clear H2 headings that match common question formats
- Include specific data, statistics, and examples
- Add author credentials and expertise signals
- Implement proper schema markup
- Create "definition" paragraphs that AI can easily extract
- Build topical authority through content clusters
- Ensure fast page loads and clean HTML
