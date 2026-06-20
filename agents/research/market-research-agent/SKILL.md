---
name: market-research-agent
description: Analyze markets, competitors, user segments, and trends to produce evidence-based business intelligence. Use
  when evaluating market opportunities, pricing strategy research, or due diligence for investments.
domain: agents
tags:
- agent
- ai-agent
- automation
- market
- orchestration
- research
---
# Market Research Agent

Autonomous market research agent that analyzes markets, competitors, user segments, and trends to produce structured, evidence-based business intelligence. This agent gathers data from multiple sources, validates claims, and produces actionable recommendations.

## When to Use

- Evaluating market opportunity before building a product
- Analyzing competitors before launching or pivoting
- Pricing strategy research for new or existing products
- Understanding user segments and their needs
- Tracking market trends and technology shifts
- Due diligence for investment or acquisition decisions
- Go-to-market planning for new features or products

## When NOT to Use

- Implementing market research tools (use `code-agent`)
- Researching technical documentation (use `web-research`)
- Analyzing internal codebase (use `code-research`)
- Reviewing code quality (use `review-agent`)
- Market data is already available (use existing reports)
- Task requires proprietary data you don't have access to
- Decision is purely technical, not market-driven
- Research would take longer than acting on current knowledge

## Process / Steps

Follow these steps in order. Each step builds on the previous one.


### 1. Define Research Scope

Before gathering data, define what "done" looks like:

```markdown
## Research Brief
- **Decision this research supports**: [What are we deciding?]
- **Key questions**:
  1. [Question that must be answered]
  2. [Question that must be answered]
  3. [Question that must be answered]
- **Time horizon**: [Current state | 1 year | 3 year | 5 year]
- **Geographic scope**: [Global | Regional | Country-specific]
- **Budget/time constraint**: [Hours available for research]
- **Success criteria**: [What evidence would make the decision clear]
```

### 2. Market Sizing

Estimate the market opportunity using structured approaches:

```markdown
## Market Sizing Framework

Estimate market opportunity using TAM/SAM/SOM analysis.

### TAM (Total Addressable Market)
- [Total market if you captured 100%]
- Method: [Top-down from industry reports | Bottom-up from unit economics]
- Sources: [Gartner, Statista, IBISWorld, government data]

### SAM (Serviceable Addressable Market)
- [Portion of TAM you can realistically reach]
- Criteria: [Geographic, demographic, technology, regulatory filters]
- Size: $[X]B

### SOM (Serviceable Obtainable Market)
- [What you can capture in 2-3 years]
- Assumptions: [market share, growth rate, distribution]
- Size: $[X]M

### Calculation Template (Bottom-Up)
Target customers: [X million]
Average revenue per customer: $[X]/year
Penetration rate: [X]%
Market size = [customers] x [ARPC] x [penetration] = $[X]
```

### 3. Competitive Analysis

```markdown
## Competitive Landscape

Map direct and indirect competitors with evidence.

### Direct Competitors (solve same problem for same users)
| Competitor | Founded | Funding | Users | Pricing | Key Strength | Key Weakness |
|-----------|---------|---------|-------|---------|--------------|-------------|
| [name] | [year] | $[X]M | [X]K | $[X]/mo | [strength] | [weakness] |
| [name] | [year] | $[X]M | [X]K | $[X]/mo | [strength] | [weakness] |

### Indirect Competitors (solve same problem differently)
| Competitor | How They Solve It | Why Users Choose Them |
|-----------|------------------|----------------------|
| [name] | [approach] | [reason] |

### Competitive Moats
| Competitor | Moat Type | Durability |
|-----------|-----------|-----------|
| [name] | [Network effects / Data / Brand / Regulatory / Cost] | [Strong / Medium / Weak] |

### Feature Comparison Matrix
| Feature | Us | Competitor A | Competitor B | Competitor C |
|---------|-----|-------------|-------------|-------------|
| [core feature 1] | [status] | [status] | [status] | [status] |
| [core feature 2] | [status] | [status] | [status] | [status] |
| [core feature 3] | [status] | [status] | [status] | [status] |

Legend: [x] = full support, [~] = partial, [ ] = not available
```

### 4. User Segment Analysis

```markdown
## User Segments

Identify and profile target user segments.

### Segment 1: [Name]
- **Size**: [X] potential users
- **Demographics**: [Age, income, location, role]
- **Needs**: [What problem do they need solved]
- **Current solution**: [What they use now, including manual/no solution]
- **Willingness to pay**: $[X]/month
- **Acquisition channels**: [Where to find them]
- **Key decision criteria**: [Price vs quality vs speed vs support]

### Segment 2: [Name]
[Same structure]

### Primary Target: Segment [N]
- **Why this segment**: [Biggest pain point, highest willingness to pay, most reachable]
- **Beachhead strategy**: [How to enter with minimal resources]
```

### 5. Trend Analysis

```markdown
## Market Trends

Track directional changes with evidence and timelines.

### Trend 1: [Name]
- **Direction**: [Growing / Stable / Declining]
- **Evidence**: [Data points, reports, adoption metrics]
- **Timeline**: [When will this peak/plateau]
- **Impact on us**: [Opportunity / Threat / Neutral]
- **Action**: [What to do about it]

### Trend 2: [Name]
[Same structure]

### Technology Shifts
- [Technology A] replacing [Technology B] -- timeline: [X years]
- [Standard X] being adopted by [industry] -- implication: [what changes]
```

### 6. Pricing Intelligence

```markdown
## Pricing Analysis

Key aspects of market-research-agent relevant to this section.

### Competitor Pricing
| Competitor | Free Tier | Starter | Pro | Enterprise |
|-----------|-----------|---------|-----|-----------|
| [name] | [what is free] | $[X]/mo | $[X]/mo | Custom |
| [name] | [what is free] | $[X]/mo | $[X]/mo | Custom |

### Pricing Models in Market
- [Per-seat]: [who uses it, pros/cons]
- [Usage-based]: [who uses it, pros/cons]
- [Flat tier]: [who uses it, pros/cons]
- [Freemium]: [who uses it, pros/cons]

### Price Sensitivity Indicators
- [Switching costs]: [High / Medium / Low]
- [Budget source]: [Departmental / IT / Personal]
- [Decision maker]: [Individual / Team / Procurement]
```

### 7. Data Gathering Methods

```markdown
## Data Sources

Key aspects of market-research-agent relevant to this section.

### Quantitative (T1 - highest reliability)
- Industry reports: [Gartner, Forrester, IDC, Statista]
- Financial filings: [SEC 10-K, annual reports for public competitors]
- Government data: [Census, BLS, industry surveys]
- App store data: [Downloads, ratings, reviews]
- Traffic data: [SimilarWeb, Ahrefs]

### Qualitative (T2 - cross-reference required)
- User reviews: [G2, Capterra, ProductHunt, App Store reviews]
- Community discussions: [Reddit, HN, Discord, forums]
- Job postings: [hiring velocity signals growth or pivot]
- Patent filings: [R&D direction signals]
- Conference talks: [Product roadmap signals]

### Analyst/Media (T3 - signal only)
- News articles: [funding, partnerships, launches]
- Blog posts: [opinion pieces, competitive comparisons]
- Social media: [sentiment, viral moments]
```

## Output Format

```markdown
## Market Research Report

Key aspects of market-research-agent relevant to this section.


### Executive Summary (3-5 sentences)
[Direct answer to the research question with confidence level]

### Market Opportunity
- TAM: $[X]B | SAM: $[X]M | SOM: $[X]M
- Growth rate: [X]% CAGR
- Key drivers: [list]

### Competitive Position
- **Category leader**: [name] -- [why]
- **Our differentiation**: [what we do differently]
- **Moat potential**: [type] -- [durability]

### User Segments
- **Primary target**: [segment name] -- [size, needs, pricing]

### Key Risks
1. [Risk] -- Likelihood: [HIGH/MED/LOW] -- Mitigation: [action]
2. [Risk] -- Likelihood: [HIGH/MED/LOW] -- Mitigation: [action]

### Recommendation
[Specific, actionable recommendation]

### Evidence Quality
- T1 (primary sources): [X]% of evidence
- T2 (cross-referenced secondary): [X]% of evidence
- T3 (opinion/social): [X]% of evidence

### Sources
[Full source list with URLs and dates]
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Our idea is unique, no competitors" | If no one else is solving this problem, question whether the problem exists. Competition validates demand. |
| "The market is huge, we just need 1%" | 1% of a huge market is incredibly hard to capture. Bottom-up SOM analysis reveals the real opportunity. |
| "Users said they would pay" | Users lie about willingness to pay. Test with pre-orders, landing page conversion, or pilot contracts -- not surveys. |
| "The trend is clear, we should follow" | Trends have winners and losers. Being in a growing market does not guarantee success. Differentiation matters. |
| "We can beat the incumbent on features" | Incumbents win on distribution and switching costs, not features. Research the moat, not just the feature gap. |
| "Price is the main decision factor" | For B2B, price is rarely the top criterion. Reliability, support, and integration often matter more. |

## Red Flags

- Market sizing using only top-down estimates (Gartner says $50B does not mean you get any of it)
- No primary source for a key data point (opinion repeated as fact)
- Competitive analysis based only on marketing pages (read reviews, issues, and actual usage)
- Ignoring indirect competitors (the spreadsheet that "isn't really a competitor")
- Trend analysis without timelines (direction without timing is not actionable)
- Pricing research without understanding buyer's budget process
- User segment analysis without willingness-to-pay data

## Verification

After market research, confirm:

- [ ] Market size estimated with both TAM and SOM (not just TAM)
- [ ] Top 3 competitors analyzed with real data (not marketing claims)
- [ ] At least one user segment validated with evidence (not just assumptions)
- [ ] Pricing intelligence gathered from actual competitor pricing pages
- [ ] Trends supported by data (not just "everyone is talking about AI")
- [ ] Evidence quality disclosed (T1/T2/T3 breakdown)
- [ ] Recommendation is actionable (specific next steps, not "explore further")
- [ ] Risks identified with mitigations (not just "competition is a risk")
- [ ] All data points sourced (no unsourced claims)
- [ ] No [TODO] or placeholder content in the report

## Overview

> Section content — see SKILL.md body for full details.
