# Analytics Mode Reference

## Table of Contents
1. [KPI Framework](#kpi-framework)
2. [Dashboard Design](#dashboard-design)
3. [Attribution Models](#attribution-models)
4. [ROI Calculation](#roi-calculation)
5. [Reporting Templates](#reporting-templates)
6. [Cohort Analysis](#cohort-analysis)
7. [Forecasting](#forecasting)

---

## KPI Framework

### Marketing KPIs by Channel

**Organic / SEO**
| Metric | Definition | Target Direction |
|--------|-----------|-----------------|
| Organic sessions | Visits from search engines | ↑ |
| Keyword rankings | Positions for target keywords | ↑ (top 10) |
| Organic CTR | Impressions → Clicks in SERP | ↑ (>3%) |
| Domain authority | Overall domain strength | ↑ |
| Backlinks | Referring domains count | ↑ quality |
| Pages indexed | Pages in Google's index | ↑ (healthy pages only) |

**Paid Advertising**
| Metric | Definition | Target Direction |
|--------|-----------|-----------------|
| ROAS | Revenue ÷ Ad Spend | ↑ (>3x for e-com) |
| CPA / CAC | Cost Per Acquisition | ↓ |
| CTR | Click-Through Rate | ↑ (>1% Meta, >3% Google Search) |
| CPC | Cost Per Click | ↓ |
| CPM | Cost Per 1,000 Impressions | ↓ |
| Conversion Rate | Clicks → Conversions | ↑ |
| Frequency | Avg times user sees ad | Monitor (keep <3/week) |

**Email Marketing**
| Metric | Definition | Target Direction |
|--------|-----------|-----------------|
| Open rate | Emails opened ÷ Delivered | ↑ (>25%) |
| Click rate | Clicks ÷ Delivered | ↑ (>3%) |
| CTOR | Clicks ÷ Opens | ↑ (>10%) |
| Unsubscribe rate | Unsubs ÷ Delivered | ↓ (<0.3%) |
| List growth rate | New subs - Unsubs ÷ Total | ↑ |
| Revenue per email | Total revenue ÷ Emails sent | ↑ |

**Social Media**
| Metric | Definition | Target Direction |
|--------|-----------|-----------------|
| Engagement rate | (Likes+Comments+Shares) ÷ Reach | ↑ (>3%) |
| Follower growth rate | Net new followers ÷ Total | ↑ |
| Reach | Unique accounts that saw content | ↑ |
| Share of voice | Brand mentions ÷ Total mentions | ↑ |
| Click-throughs | Link clicks from social | ↑ |
| Video completion rate | Views to end ÷ Total views | ↑ (>25%) |

**Website / Product**
| Metric | Definition | Target Direction |
|--------|-----------|-----------------|
| Conversion rate | Goal completions ÷ Sessions | ↑ |
| Bounce rate | Single-page sessions ÷ Total | ↓ |
| Avg session duration | Time on site | ↑ |
| Pages per session | Page views ÷ Sessions | ↑ |
| Cart abandonment rate | Abandoned ÷ Initiated | ↓ (<70%) |
| MQL → SQL rate | Marketing Qualified → Sales Qualified | ↑ |

### North Star Metrics by Business Type
| Business Type | North Star | Why |
|--------------|-----------|-----|
| SaaS | Monthly Active Users or Net Revenue Retention | Product engagement = retention = growth |
| E-commerce | Revenue Per Visitor | Combines traffic quality + conversion + AOV |
| Marketplace | Gross Merchandise Value (GMV) | Total platform transaction value |
| Content/Media | Engaged Time or Returning Visitors | Audience loyalty and ad value |
| Lead Gen | Cost Per Qualified Lead (CPQL) | Quality over quantity |

---

## Dashboard Design

### Executive Marketing Dashboard (Weekly)
```
┌─────────────────────────────────────────────┐
│  MARKETING PERFORMANCE — Week of {date}     │
├───────────┬───────────┬───────────┬─────────┤
│ Revenue   │ Leads     │ CAC       │ ROAS    │
│ ${value}  │ {count}   │ ${value}  │ {X.Xx}  │
│ {%Δ WoW}  │ {%Δ WoW}  │ {%Δ WoW}  │{%Δ WoW} │
├───────────┴───────────┴───────────┴─────────┤
│  CHANNEL BREAKDOWN                          │
│  Organic:  {sessions} | {conv} | ${rev}     │
│  Paid:     {sessions} | {conv} | ${rev}     │
│  Email:    {sessions} | {conv} | ${rev}     │
│  Social:   {sessions} | {conv} | ${rev}     │
│  Direct:   {sessions} | {conv} | ${rev}     │
├─────────────────────────────────────────────┤
│  TOP PERFORMING                             │
│  Best ad: {name} — {ROAS}                   │
│  Best email: {subject} — {open%} | {click%} │
│  Best content: {title} — {views} | {conv}   │
├─────────────────────────────────────────────┤
│  ACTION ITEMS                               │
│  1. {Recommended action based on data}      │
│  2. {Second recommendation}                 │
│  3. {Third recommendation}                  │
└─────────────────────────────────────────────┘
```

### Dashboard Principles
- Lead with the metric the business cares most about (usually revenue or leads)
- Show trends (WoW, MoM) not just snapshots
- Highlight anomalies — what changed and why
- Include 2-3 action items, not just data
- Compare to targets/goals, not just prior period
- Keep it to one page/screen — detail goes in appendix

---

## Attribution Models

### Common Models Explained

| Model | Logic | Best For |
|-------|-------|----------|
| **Last Click** | 100% credit to final touchpoint | Simple setups, short sales cycles |
| **First Click** | 100% credit to first touchpoint | Understanding discovery channels |
| **Linear** | Equal credit to all touchpoints | Balanced view, multiple touchpoints |
| **Time Decay** | More credit to recent touchpoints | Longer sales cycles |
| **Position-Based** | 40% first, 40% last, 20% middle | B2B with clear acquisition + conversion |
| **Data-Driven** | ML-based, per-channel contribution | High volume, mature data infrastructure |

### Attribution Implementation Checklist
- [ ] UTM parameters on all campaign links (source, medium, campaign, content, term)
- [ ] Consistent UTM naming conventions documented
- [ ] Cross-device tracking configured (user ID if possible)
- [ ] Conversion events defined and firing correctly
- [ ] Attribution window set appropriately (7-day click, 1-day view for most)
- [ ] Offline conversions imported (if applicable)
- [ ] Regular audit of UTM tagging compliance

### UTM Naming Convention
```
utm_source:   {platform}          — google, facebook, linkedin, newsletter
utm_medium:   {type}              — cpc, email, social, referral, organic
utm_campaign: {campaign-name}     — q3-launch, summer-sale, brand-awareness
utm_content:  {creative-variant}  — video-a, static-b, cta-red
utm_term:     {keyword}           — best-crm-software (paid search only)
```

---

## ROI Calculation

### Marketing ROI Formula
```
Marketing ROI = (Revenue Attributed to Marketing - Marketing Cost) ÷ Marketing Cost × 100
```

### Channel-Level ROI Template
```
| Channel     | Spend    | Revenue  | ROI    | CAC    | LTV:CAC |
|------------|----------|----------|--------|--------|---------|
| Google Ads  | ${X}     | ${Y}    | {Z}%   | ${A}   | {B}:1   |
| Meta Ads    | ${X}     | ${Y}    | {Z}%   | ${A}   | {B}:1   |
| Email       | ${X}     | ${Y}    | {Z}%   | ${A}   | {B}:1   |
| SEO         | ${X}     | ${Y}    | {Z}%   | ${A}   | {B}:1   |
| Content     | ${X}     | ${Y}    | {Z}%   | ${A}   | {B}:1   |
| TOTAL       | ${X}     | ${Y}    | {Z}%   | ${A}   | {B}:1   |
```

### LTV:CAC Benchmarks
- **Below 1:1** — Losing money on every customer. Fix urgently.
- **1:1 to 2:1** — Unsustainable. Reduce CAC or increase LTV.
- **3:1** — Healthy. Standard target.
- **5:1+** — Very efficient. Could afford to spend more to grow faster.

---

## Reporting Templates

### Monthly Marketing Report Structure
```markdown
# Marketing Report — {Month Year}

## Executive Summary
{3-5 bullet points: wins, challenges, key metrics vs targets}

## Performance vs Goals
{Table: Metric | Target | Actual | Δ | Status (🟢🟡🔴)}

## Channel Deep-Dive
{Per-channel: spend, results, efficiency, trends, insights}

## Content Performance
{Top 5 performing pieces with metrics}

## Campaign Highlights
{Notable campaigns launched or completed}

## Competitive Landscape
{Any notable competitor moves or market changes}

## Experiments & Learnings
{Tests run, results, implications}

## Next Month Plan
{Priorities, campaigns planned, budget allocation}

## Budget Summary
{Planned vs actual spend, remaining budget}
```

---

## Cohort Analysis

### Cohort Analysis Framework
Group users by their acquisition date (week or month) and track their behavior over time.

**Key cohort metrics:**
- Retention rate by cohort (D1, D7, D30, D60, D90)
- Revenue per cohort over time
- Activation rate by acquisition channel
- Feature adoption by cohort

### Cohort Table Template
```
         Week 0  Week 1  Week 2  Week 3  Week 4
Jan W1   100%    42%     35%     30%     28%
Jan W2   100%    45%     37%     32%     —
Jan W3   100%    40%     33%     —       —
Jan W4   100%    44%     —       —       —
Feb W1   100%    —       —       —       —
```

Look for: Improving cohorts over time = product/marketing getting better.
Declining cohorts = something is degrading.

---

## Forecasting

### Simple Forecasting Methods

**Linear Projection**
Take the growth rate over the last 3-6 months and project forward.
Good for stable businesses with consistent trends.

**Seasonal Adjustment**
Apply year-over-year seasonal indices to the baseline trend.
Essential for e-commerce, retail, travel, events.

**Funnel Math**
```
Target Revenue = Target Customers × Average Order Value
Target Customers = Target Leads × Conversion Rate
Target Leads = Required Traffic × Lead Capture Rate
Required Traffic = Target Leads ÷ Lead Capture Rate
Required Ad Spend = Required Traffic × Avg CPC
```

Work backwards from revenue targets to determine channel investment needed.

### Confidence Levels
Always present forecasts with ranges:
- **Optimistic** — best-case if everything goes right
- **Base** — most likely scenario based on trends
- **Conservative** — worst-case, plan for this budget-wise
