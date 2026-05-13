# Programmatic SEO Reference

Generate hundreds or thousands of unique, rankable pages from templates + data.
This is infrastructure, not a campaign — build once, improve over time, compound.

## Table of Contents
1. [When to Use Programmatic SEO](#when-to-use-programmatic-seo)
2. [Page Type Templates](#page-type-templates)
3. [Implementation Workflow](#implementation-workflow)
4. [Data Sources](#data-sources)
5. [Quality Guardrails](#quality-guardrails)
6. [Internal Linking at Scale](#internal-linking-at-scale)
7. [Indexation Strategy](#indexation-strategy)

---

## When to Use Programmatic SEO

Programmatic SEO works when a keyword pattern has:
- **Repeatable structure:** "[Service] in [City]", "[Product A] vs [Product B]"
- **Sufficient volume:** Each variation has 50+ monthly searches
- **Weak competition:** Current results are forums, thin pages, or listicles
- **Available data:** You have (or can build) unique data per page

**Good candidates:**
- Location + Service pages (50 services × 200 cities = 10,000 pages)
- Integration/App directory pages (tool integrations, API connections)
- Comparison pages ([Your Product] vs [Competitor])
- Industry/use-case pages (solutions by vertical)
- Glossary/definition pages (industry terms)
- Statistics/data pages (updated regularly)
- Salary/cost-of-living pages

**Bad candidates (avoid):**
- Pages where the only difference is one word swapped (thin content)
- Topics where unique data doesn't exist per variation
- Patterns with no search volume

---

## Page Type Templates

### 1. Location Pages: "[Service] in [City]"
```markdown
# {Service} in {City}, {State}

{Unique intro paragraph about {Service} market in {City} — 2-3 sentences with local data}

## Why Choose {Brand} for {Service} in {City}
{Value prop tailored to local market}

## {Service} Pricing in {City}
{Dynamic pricing table or range based on local data}

## What Our {City} Customers Say
{Local testimonials — MUST be real}

## Frequently Asked Questions About {Service} in {City}
{FAQ schema — mix of universal + local questions}

## Get Started with {Service} in {City}
{CTA — localized phone number, office address if applicable}
```

### 2. Comparison Pages: "{Product A} vs {Product B}"
```markdown
# {Product A} vs {Product B}: Honest Comparison ({Year})

{2-3 sentence summary: who each product is best for}

## Quick Comparison
| Feature | {Product A} | {Product B} |
|---------|------------|------------|
{Dynamic feature comparison table}

## {Product A} Overview
{200-300 words — what it does, who it's for, strengths}

## {Product B} Overview
{200-300 words — same structure}

## Key Differences
{3-5 specific differences with analysis, not just listing}

## Pricing Comparison
{Dynamic pricing table}

## Which Should You Choose?
{Decision framework based on use case, not just "our product wins"}

## Try {Your Product} Free
{CTA — but AFTER providing genuinely useful comparison}
```

### 3. Integration Pages: "{Your Product} + {Integration}"
```markdown
# Connect {Your Product} with {Integration}

{What the integration does in one sentence}

## What You Can Do
{3-5 specific use cases as bullet points}

## How It Works
{3-step setup process with screenshots}

## Popular Workflows
{2-3 specific automation examples}

## Get Started
{CTA to integration setup page}
```

### 4. Glossary/Definition Pages: "What is {Term}"
```markdown
# What is {Term}? Definition, Examples & Best Practices

## {Term} Definition
{Clear 2-sentence definition — optimized for featured snippet}

## How {Term} Works
{Explanation with practical context}

## {Term} Examples
{2-3 real-world examples}

## Why {Term} Matters
{Business impact and relevance}

## Related Terms
{Internal links to related glossary entries}
```

---

## Implementation Workflow

### Step 1: Keyword Pattern Research
```
1. Identify repeatable keyword patterns in your niche
2. Validate volume: check 10-20 variations in Ahrefs/Semrush
3. Assess competition: are top results beatable?
4. Estimate total pages: {modifier count} × {variable count}
5. Calculate potential traffic: {avg volume per page} × {pages} × {expected CTR}
```

### Step 2: Build Data Source
- **Spreadsheet** (CSV/Google Sheets) — simplest for <1000 pages
- **Database** (Airtable, Notion, PostgreSQL) — for 1000+ pages
- **API** — for real-time data (pricing, availability, stats)

**Every page MUST have at least 2-3 unique data points** beyond the keyword variable.
If the only difference between pages is the city name, that's thin content.

### Step 3: Design Template
- Build one high-quality page manually first
- Identify what's static (same on every page) vs dynamic (changes per page)
- Mark dynamic sections with placeholders: `{city}`, `{price_range}`, `{testimonial}`
- Ensure each page has unique: title, meta description, H1, intro paragraph, data

### Step 4: Generate Content
- Use Claude to generate unique intro paragraphs per variation
- Pull dynamic data from your data source
- Generate unique meta descriptions per page
- Add dynamic schema markup (FAQ, Product, LocalBusiness)

### Step 5: Publish & Index
- Publish in batches (50-100/week), not all at once
- Submit XML sitemap to Google Search Console
- Build internal links from existing high-authority pages
- Monitor indexation rate weekly

---

## Data Sources

| Source Type | Examples | Best For |
|------------|---------|----------|
| Government data | Census, BPS statistics, city databases | Location pages |
| API data | Google Places, pricing APIs, weather | Real-time pages |
| Product databases | Your own product catalog, integrations list | Product/integration pages |
| User-generated | Reviews, testimonials, community data | Social proof pages |
| Scraped (ethical) | Public competitor info, job listings | Comparison pages |
| Manual curation | Expert insights, proprietary research | Premium content |

---

## Quality Guardrails

### The Thin Content Test
Before publishing, every page must pass ALL of these:

- [ ] **Unique value:** Page has 2+ data points no other page shares
- [ ] **Standalone useful:** Would a user find this page helpful on its own?
- [ ] **Not duplicated:** <30% overlap with any other page on your site
- [ ] **Real data:** No fabricated statistics, reviews, or testimonials
- [ ] **Proper formatting:** Not obviously templated or "robot-written"
- [ ] **Search intent match:** Content answers what the searcher actually wants
- [ ] **CTA relevant:** Call-to-action makes sense for this specific page

### Red Flags (Will Get Penalized)
- Pages where only the city/product name changes (everything else identical)
- Fabricated reviews or testimonials
- Auto-generated text with no human review
- Thousands of pages published simultaneously
- No internal linking structure
- Duplicate meta titles/descriptions across pages

---

## Internal Linking at Scale

### Hub-and-Spoke Model
```
                    Hub Page (pillar content)
                    /        |         \
                   /         |          \
            Spoke 1     Spoke 2     Spoke 3
           (city A)    (city B)    (city C)
```

**Rules:**
- Every programmatic page links back to its hub/parent page
- Hub pages link to top 10-20 spoke pages
- Spoke pages cross-link to 3-5 related spokes
- Use descriptive anchor text (not "click here")
- Add breadcrumb navigation on every page
- Create a hierarchical URL structure: `/services/city-name/`

### Auto-Generated Related Links
```html
<!-- At bottom of each programmatic page -->
<h2>Related Pages</h2>
<ul>
  <li><a href="/service/nearby-city-1">{Service} in {Nearby City 1}</a></li>
  <li><a href="/service/nearby-city-2">{Service} in {Nearby City 2}</a></li>
  <li><a href="/service/nearby-city-3">{Service} in {Nearby City 3}</a></li>
</ul>
```

---

## Indexation Strategy

### Publishing Schedule
| Site Authority | Pages/Week | Timeline for 1000 pages |
|---------------|-----------|------------------------|
| New site (DR <20) | 20-30 | 8-12 months |
| Growing (DR 20-40) | 50-100 | 3-5 months |
| Established (DR 40+) | 100-200 | 2-3 months |

### Monitoring Checklist (Weekly)
- [ ] Check Google Search Console → Pages → Indexation report
- [ ] Monitor "Crawled - not indexed" vs "Indexed" ratio
- [ ] Identify pages with impressions but low CTR → improve titles
- [ ] Remove or noindex pages getting zero impressions after 90 days
- [ ] Update data on top-performing pages to maintain freshness
