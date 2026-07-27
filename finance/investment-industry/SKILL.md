---
name: investment-industry
version: 2.0.0
category: finance
domain: finance
author: mahipal
license: Apache-2.0
subdomain: finance
description: "Use when industry research and sector rotation for portfolio alpha — TAM/SAM/SOM analysis, competitive dynamics, regulatory tailwinds, and sector timing to beat the market by 5-15% annually."
keywords: [industry, research, market analysis, sector rotation, TAM, competitive dynamics, top-down investing, macro, thematic]
source: ai-berkshire
money: true
tags: [investment, industry, finance]
---

# Investment Industry Research



## When Not to Use

- **Simple or one-off tasks** — if the task is straightforward, direct execution is faster than structured methodology.
- **Already established workflows** — follow existing team conventions rather than introducing new frameworks.
- **When automation overhead exceeds benefit** — for very small scopes, the setup cost may not be justified.


## Dependencies

- Python 3.8+ or Node.js 18+
- Access to relevant APIs/services for your specific use case
- Basic understanding of the domain concepts


## Commands

```bash
# Refer to the skill's usage section for specific commands
# Adapt these to your workflow
```
## Money-Making Overview

**Sector rotation** is the single most leveragable edge for portfolio returns. Getting the sector right matters more than picking the right stock within it — sector allocation explains 70-90% of a diversified portfolio's returns.

This skill transforms industry research into actionable sector rotation trades with specific entry/exit signals, position sizing, and monitoring cadence.

**ROI Track Record:** Systematic sector rotation strategies outperform buy-and-hold by 5-15% annually. Top-decile industry analysts earn 25%+ annualized on concentrated sector bets.

**Capital Required:** $1,000 minimum (sector ETFs or individual stocks)

**Time to First Trade:** 3-4 hours for full industry analysis, 1 hour/month to reassess

**Archetype:** Top-Down Macro Investor (Medium Capital, Low Time)

---

## Revenue Streams from Industry Research

| Method | Effort | Return Potential |
|--------|--------|-----------------|
| Sector rotation (Sector ETFs) | 2 hr initial + 1 hr/month | 5-10% alpha over market |
| Thematic industry positions | 3 hr research/position | 3-10x on thematic winners |
| Industry research reports | 8-10 hr/week | $5K-15K/month consulting |
| Sector newsletter/substack | 5 hr/week | $2K-8K/month subscriptions |

---

## Workflow: Industry Analysis → Trade

### Phase 1: The Funnel (Top-Down Sector Selection)

```
MACRO CHECK → SECTOR CHECK → INDUSTRY CHECK → POSITION CHECK
    ↓               ↓               ↓              ↓
  Rate cycle      Relative       TAM/SAM/SOM    Company screen
  Inflation       sector perf    Competitive    Financial health
  GDP trend       Earnings       Regulatory     Management quality
  Policy shift    momentum       moat/dynamics  Valuation
```

### Phase 2: Macro Regime → Sector Map

| Regime | Outperform | Underperform |
|--------|-----------|-------------|
| Rising rates + strong economy | Financials, Energy, Industrials | Tech (growth), Real Estate |
| Falling rates + strong economy | Tech, Consumer Discretionary | Utilities, Staples |
| Rising rates + weak economy | Healthcare, Staples | Real Estate, Consumer Disc. |
| Falling rates + weak economy (recession) | Treasuries, Gold, Staples | Cyclicals, Small-cap |
| Inflation > 4% | Energy, Materials, Commodities | Long-duration bonds, Tech |
| Inflation < 2% | Tech, Consumer Disc., REITs | Energy, Materials |

### Phase 3: TAM/SAM/SOM Analysis (Market Sizing)

```
TAM (Total Addressable Market):
├── Global spending in the space
├── Gartner/IDC/Statista reports
├── Revenue of all public players combined × market share assumption
├── Growth rate: 3-year CAGR

SAM (Serviceable Addressable Market):
├── Portion of TAM your target can realistically reach
├── Geographic constraints (US-only, EU-only)
├── Regulatory constraints
├── Technology constraints

SOM (Serviceable Obtainable Market):
├── What the target company can capture in 3-5 years
├── Current market share × realistic growth
├── Sales capacity check
├── Competitive response analysis
```

### Phase 4: Industry Scoring Matrix

| Factor | Weight | Score (1-10) | Weighted |
|--------|--------|-------------|----------|
| TAM growth rate (>10% CAGR = 10, <0% = 0) | 15% | — | — |
| Competitive structure (monopoly/duopoly = 10) | 20% | — | — |
| Regulatory tailwind (pro-industry = 10) | 10% | — | — |
| Macro regime alignment | 15% | — | — |
| Revenue visibility (>2yr backlog = 10) | 10% | — | — |
| Pricing power trend (rising = 10) | 15% | — | — |
| Consolidation potential (fragmented = low) | 15% | — | — |
| **Total** | 100% | — | — |

**Buy:** >70 — overweight sector 1.5-2x benchmark
**Hold:** 40-70 — market weight or slight overweight
**Sell/Underweight:** <40 — reduce to 0-50% of benchmark

### Phase 5: Position Sizing & Execution

```python
#!/usr/bin/env python3
"""Sector rotation model — allocates based on industry scores."""

import pandas as pd

# industry_scores: dict of {industry_name: score_0_100}
industry_scores = {
    "semiconductors": 88,
    "healthcare_equipment": 72,
    "renewable_energy": 55,
    "retail_banking": 42,
    "commercial_real_estate": 18,
}

total_score = sum(industry_scores.values())

print("=== SECTOR ROTATION ALLOCATION ===")
for industry, score in sorted(industry_scores.items(), key=lambda x: x[1], reverse=True):
    allocation = score / total_score  # Relative weight
    action = "OVERWEIGHT" if score >= 70 else ("MARKET WEIGHT" if score >= 40 else "UNDERWEIGHT")
    print(f"  {industry}: Score {score}/100 → Weight {allocation:.1%} → {action}")
```

---

## First Action in 60 Minutes

```
1.  Identify current macro regime (rising/falling rates, inflation) — 5 min
2.  Check 10-year Treasury yield, Fed funds rate, CPI — 5 min
3.  Map regime to sector outperformers from table above — 5 min
4.  For top 2 sectors, read 1 industry report each (Morningstar/IBD) — 20 min
5.  Score each industry using scoring matrix — 15 min
6.  Execute: Buy sector ETF (XLF, XLI, XLK, etc.) or top 3 stocks — 10 min
→ Total: ~60 min for a complete sector rotation
```

---

## Anti-Rationalization Table

| Excuse | Why It's Wrong |
|--------|---------------|
| "I'm a stock picker, not a macro investor" | 70% of your return comes from sector. Picking stocks in the wrong sector is fighting the tape. |
| "Sector timing is impossible" | Systematic rules (rate regime → sector map) beat discretionary macro timing. Follow the rules. |
| "I need to read 100 industry reports" | One Gartner PDF + scoring matrix beats reading 100 reports. Depth over breadth. |
| "The macro is confusing right now" | When uncertain, default to healthcare + staples (defensive). Stay until the regime is clear. |
| "This doesn't work in crypto" | Sector rotation works on every asset class. Rotate between DeFi, L1, infrastructure, memecoins. |

---

## Output Format

```
INDUSTRY ANALYSIS RECORD:
Date: ____
Industry: ____
Macro Regime: ____
TAM: $____ | Growth: ____% CAGR
Score: ____/100
Allocation Decision: Overweight / Market Weight / Underweight
Position(s): ____
Entry Date: ____
Exit Date: ____
Return vs Benchmark: ____%
```

## Verification Checklist

```
☐ Macro regime identified (rate direction + inflation trend)
☐ Sector-to-regime map consulted
☐ TAM/SAM/SOM calculated for selected industry
☐ Industry scoring matrix completed (7 factors)
☐ At least 1 position in overweight sector
☐ Underweight positions reduced to <50% of benchmark
☐ Monthly reassessment calendar reminder set
```


## When to Use
Use this skill when working with investment industry.
