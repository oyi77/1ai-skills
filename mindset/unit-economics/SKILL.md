---
name: unit-economics
description: Calculate CAC, LTV, margins, payback period, and cohort analysis. Use when evaluating business model sustainability or optimizing growth efficiency.
domain: mindset
---

# Unit Economics

Framework for analyzing per-customer profitability: CAC, LTV, LTV:CAC ratio, margins, payback period, and cohort analysis.

## When to Use

- Evaluating business model sustainability
- Deciding whether to scale go-to-market
- Optimizing pricing, retention, or acquisition
- Investor diligence or board reporting
- **When NOT to use**: Pre-revenue (focus on PMF first), or non-profit models

## Core Metrics

### 1. CAC (Customer Acquisition Cost)

**Formula**: `CAC = (Sales + Marketing Spend) / # of New Customers`

**Example**:
- Sales & Marketing spend: $100K/month
- New customers: 50/month
- **CAC = $2K**

**What's good?** Depends on LTV. Benchmark: LTV:CAC ≥ 3:1.

---

### 2. LTV (Lifetime Value)

**Formula**: `LTV = ARPA × Gross Margin % / Churn Rate`

**Example**:
- ARPA (Average Revenue Per Account): $500/month
- Gross Margin: 80%
- Monthly churn: 2%
- **LTV = $500 × 0.80 / 0.02 = $20K**

**What's good?** LTV ≥ 3× CAC.

---

### 3. LTV:CAC Ratio

**Formula**: `LTV:CAC = LTV / CAC`

**Benchmark**:
- **<1**: Losing money on every customer (unsustainable)
- **1-3**: Profitable, but inefficient (hard to scale)
- **3-5**: Healthy (scalable)
- **>5**: Very efficient (possibly under-investing in growth)

**Example**: LTV = $20K, CAC = $2K → **LTV:CAC = 10:1** (excellent).

---

### 4. Payback Period

**Formula**: `Payback Period (months) = CAC / (ARPA × Gross Margin %)`

**Example**:
- CAC: $2K
- ARPA: $500/month
- Gross Margin: 80%
- **Payback = $2K / ($500 × 0.80) = 5 months**

**Benchmark**: <12 months (ideally <6 months for SaaS).

---

### 5. Gross Margin

**Formula**: `Gross Margin % = (Revenue - COGS) / Revenue`

**COGS** (Cost of Goods Sold): Direct costs to deliver service (hosting, support, payment fees).

**Example**:
- Revenue: $100K/month
- COGS: $20K/month (servers, support)
- **Gross Margin = 80%**

**Benchmark**: SaaS targets 70-90%.

---

### 6. Contribution Margin

**Formula**: `Contribution Margin = Revenue - Variable Costs`

**Variable costs**: COGS + customer-specific costs (onboarding, support).

**Example**:
- Revenue per customer: $500/month
- COGS: $50/month
- Support: $30/month
- **Contribution Margin = $420/month**

**Why it matters**: Shows profitability per customer before fixed costs (salaries, rent).

---

## Cohort Analysis

**Purpose**: Track behavior of customer cohorts over time.

**Example** (Monthly retention by cohort):

| Cohort | Month 1 | Month 3 | Month 6 | Month 12 |
|--------|---------|---------|---------|----------|
| Jan | 100% | 80% | 70% | 60% |
| Feb | 100% | 82% | 72% | 62% |
| Mar | 100% | 85% | 75% | ? |

**Insight**: If newer cohorts retain better, unit economics are improving (higher LTV).

---

## How to Improve Each Metric

### Improve CAC (Lower is Better)

| Tactic | Impact |
|--------|--------|
| **Organic channels** | Content, SEO, referrals (lower CAC than paid) |
| **Conversion rate optimization** | Better landing pages, faster signup |
| **Sales efficiency** | Shorten sales cycle, automate demos |

---

### Improve LTV (Higher is Better)

| Tactic | Impact |
|--------|--------|
| **Reduce churn** | Improve onboarding, customer success, product quality |
| **Upsell/cross-sell** | Increase ARPA (expansion revenue) |
| **Annual plans** | Prepayment reduces churn, improves cash flow |

---

### Improve Payback Period (Shorter is Better)

| Tactic | Impact |
|--------|--------|
| **Lower CAC** | See above |
| **Increase ARPA** | Raise prices or upsell |
| **Annual upfront payment** | Get 12 months cash immediately (payback = 0) |

---

## Benchmarks by Industry

| Industry | CAC | LTV:CAC | Payback (months) | Gross Margin |
|----------|-----|---------|------------------|--------------|
| **B2B SaaS** | $1-5K | 3-5:1 | 6-12 | 70-90% |
| **B2C SaaS** | $50-500 | 3-5:1 | 3-6 | 80-95% |
| **E-commerce** | $10-100 | 2-3:1 | 3-6 | 30-50% |
| **Marketplace** | $20-200 | 3-5:1 | 6-12 | 60-80% |

---

## Common Rationalizations

| Rationalization | Reality |
|-----------------|---------|
| "We'll figure out monetization later" | Unit economics determine sustainability. Validate early. |
| "LTV is hard to calculate" | Estimate it. Use cohorts. Better than guessing. |
| "We're growing fast, that's what matters" | Growth without unit economics = burning cash with no path to profitability. |
| "Our CAC will drop at scale" | Maybe, but don't assume. Prove it with data. |

## Red Flags

- LTV:CAC < 3 (unprofitable or inefficient)
- Payback > 12 months (cash flow negative too long)
- Gross margin < 50% (COGS too high for software)
- You can't calculate CAC or LTV (flying blind)
- Churn >5%/month (customers don't find value)

## Verification

- [ ] CAC calculated (sales + marketing spend / new customers)
- [ ] LTV calculated (ARPA × gross margin % / churn rate)
- [ ] LTV:CAC ratio ≥ 3:1 (if not, identify why and plan to improve)
- [ ] Payback period ≤ 12 months (if not, improve CAC or ARPA)
- [ ] Gross margin ≥ 70% for SaaS (if not, reduce COGS)
- [ ] Cohort analysis run (retention improving over time?)
- [ ] Improvement tactics prioritized (reduce CAC, increase LTV, reduce churn)
