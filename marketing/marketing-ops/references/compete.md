# Competitive Analysis Mode Reference

## Table of Contents
1. [Competitive Landscape Overview](#competitive-landscape-overview)
2. [Ad Strategy Teardown](#ad-strategy-teardown)
3. [Content Strategy Analysis](#content-strategy-analysis)
4. [Pricing Analysis](#pricing-analysis)
5. [SWOT Framework](#swot-framework)
6. [Positioning Map](#positioning-map)

---

## Competitive Landscape Overview

### Research Framework

For each competitor, gather:

**Company Profile**
- Founded, funding, team size, revenue (if public/estimated)
- Target market and positioning statement
- Key differentiators and unique selling propositions

**Product/Service**
- Core offering and feature set
- Pricing model and tiers
- Free trial / freemium availability
- Technology stack (BuiltWith, Wappalyzer)

**Marketing Channels**
- Primary channels (where they invest most)
- Content marketing approach (blog frequency, topics, quality)
- Social media presence (followers, engagement, platforms)
- Paid advertising (Ad Library, estimated spend)
- SEO performance (DR, top keywords, organic traffic estimate)
- Email marketing (sign up for their list, analyze cadence/quality)

**Market Position**
- Market share (if estimable)
- Customer reviews and sentiment (G2, Capterra, Trustpilot)
- Strengths and weaknesses from reviews
- Recent announcements or pivots

### Competitive Overview Output Format
```markdown
# Competitive Landscape: {Market/Category}

## Market Summary
{2-3 paragraph overview of the competitive landscape}

## Competitor Profiles

### {Competitor 1}
- **Positioning:** {one-line}
- **Strengths:** {top 3}
- **Weaknesses:** {top 3}
- **Key Channels:** {primary marketing channels}
- **Estimated Traffic:** {monthly organic visits}
- **Pricing:** {model + range}

### {Competitor 2}
{Same structure}

## Competitive Matrix
| Dimension | You | Comp 1 | Comp 2 | Comp 3 |
|-----------|-----|--------|--------|--------|
| Price | | | | |
| Features | | | | |
| UX/Design | | | | |
| Content | | | | |
| SEO | | | | |
| Social | | | | |
| Support | | | | |

## Gaps & Opportunities
{Where competitors are weak and you can win}

## Threats
{Where competitors are strong or gaining momentum}
```

---

## Ad Strategy Teardown

### How to Analyze Competitor Ads

**Data Sources:**
- Meta Ad Library (facebook.com/ads/library) — all active Meta ads
- Google Ads Transparency Center — active Google ads
- LinkedIn Ad Library — sponsored content
- TikTok Creative Center — top performing ads

**Analysis Framework:**
1. **Volume:** How many active ads? (indicates spend level)
2. **Formats:** Static, video, carousel? (what's working for them)
3. **Messaging themes:** What claims/benefits do they lead with?
4. **CTAs:** What action do they drive? (free trial, demo, shop now)
5. **Landing pages:** Where do ads send traffic? (analyze those pages)
6. **Audience signals:** Who do the ads seem targeted at? (language, imagery)
7. **Creative patterns:** What visual style? UGC vs branded?
8. **Longevity:** Ads running for 30+ days are likely performing well
9. **Seasonal patterns:** Do they ramp spend around certain periods?

### Teardown Output
```markdown
# Ad Strategy Teardown: {Competitor}

## Active Ads Summary
- Total active ads: {count}
- Platforms: {Meta, Google, LinkedIn, TikTok}
- Primary format: {video/static/carousel}
- Estimated monthly spend: {range if estimable}

## Top Performing Ads (Running 30+ days)
{Screenshot/description + analysis of each}

## Messaging Analysis
- Primary value prop: {what they lead with}
- Key claims: {specific promises}
- Emotional angle: {fear/aspiration/belonging/etc}
- Social proof used: {type and specifics}

## Creative Patterns
- Visual style: {UGC/polished/minimal/data-heavy}
- Color palette: {dominant colors}
- Text overlay approach: {heavy/minimal}

## Landing Page Analysis
{URL + conversion audit of where ads send traffic}

## Opportunities for You
{What they're doing well you should consider}
{What they're doing poorly you can beat}
```

---

## Content Strategy Analysis

### Content Audit of Competitors

**Blog Analysis:**
- Publishing frequency (posts per week/month)
- Average word count
- Content types (how-to, listicle, case study, opinion, data)
- Top-performing posts (social shares, backlinks, estimated traffic)
- Keyword coverage (what they rank for that you don't)
- Content gaps (topics in your space they haven't covered)

**Content Quality Assessment:**
- Depth and originality (AI-generated slop vs genuine insight)
- Visual quality (custom graphics, videos, infographics)
- Author expertise signals (bylines, credentials)
- Update frequency (are they refreshing old content?)

**Content Gap Analysis Output:**
```markdown
| Topic / Keyword | Comp 1 | Comp 2 | Comp 3 | You | Opportunity |
|----------------|--------|--------|--------|-----|-------------|
| {keyword} | ✅ Rank #3 | ✅ Rank #7 | ❌ | ❌ | HIGH — no content yet |
| {keyword} | ✅ Rank #1 | ❌ | ❌ | ✅ Rank #12 | MED — improve existing |
| {keyword} | ❌ | ❌ | ❌ | ❌ | HIGH — first mover |
```

---

## Pricing Analysis

### Pricing Comparison Template
```markdown
| Feature/Tier | You | Comp 1 | Comp 2 | Comp 3 |
|-------------|-----|--------|--------|--------|
| Free tier | {Y/N + limits} | | | |
| Starter price | ${/mo} | | | |
| Pro price | ${/mo} | | | |
| Enterprise | {custom/price} | | | |
| Annual discount | {%} | | | |
| Key limits | {what scales} | | | |
```

### Pricing Strategy Assessment
- **Position vs market:** Premium / competitive / undercut?
- **Value metric:** What do they charge per? (users, usage, features)
- **Psychological tactics:** Anchoring, decoys, charm pricing?
- **Switching costs:** How easy to leave? Lock-in mechanisms?

---

## SWOT Framework

### SWOT Analysis Template
```markdown
# SWOT Analysis: {Business/Product}

## Strengths (Internal, Positive)
- {What you do better than competitors}
- {Unique resources or capabilities}
- {Strong brand, technology, team advantages}

## Weaknesses (Internal, Negative)
- {Where competitors outperform you}
- {Resource constraints or gaps}
- {Known product/service limitations}

## Opportunities (External, Positive)
- {Market trends you can capitalize on}
- {Competitor weaknesses to exploit}
- {Underserved segments or channels}

## Threats (External, Negative)
- {Competitive moves that could hurt you}
- {Market changes or regulation risks}
- {Technology shifts or platform dependency}

## Strategic Implications
{2-3 key strategic moves based on the SWOT}
```

---

## Positioning Map

### How to Build a Positioning Map

1. **Choose 2 key dimensions** the market cares about:
   - Price vs Quality
   - Ease of Use vs Feature Richness
   - Speed vs Customization
   - Self-serve vs Full-service
   - Niche Focus vs Broad Platform

2. **Plot competitors** on both axes

3. **Identify whitespace** — where no competitor sits but demand exists

4. **Position your brand** in the most advantageous open space

### Output: Generate as a visual chart (SVG or HTML) when possible,
or as a text-based quadrant map:

```
                    HIGH PRICE
                        │
    Enterprise          │         Premium
    (Full-service)      │         (Best-in-class)
                        │
  ──────────────────────┼──────────────────────
                        │
    Budget              │         Mid-market
    (Bare bones)        │         (Good value)
                        │
                    LOW PRICE
     ← SIMPLE                    COMPLEX →
```
