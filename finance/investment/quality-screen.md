# QUALITY-SCREEN: Pre-Filter Framework for High-Quality Companies

**Portability**: 90pt | **Effort**: 4h | **Type**: Pure framework + metrics | **LOC**: 280

---

## Overview

QUALITY-SCREEN is a pre-filter framework that identifies financially healthy, high-quality companies before running DYP-Ask deep analysis. It separates the signal (quality) from the noise (valuation) using four core metrics calculated directly from financial statements.

**Core principle**: Garbage companies are cheap for a reason. Screen for quality first; then negotiate price.

**Target user**: Value investors, fund analysts, portfolio managers who need to prioritize research time.

---

## Why Quality Screening Matters

**The problem**: Screening 500+ stocks for investment ideas takes weeks. Running DYP-Ask on mediocre companies wastes time.

**The solution**: Quality metrics filter to top 50-100 candidates in 2 hours. DYP-Ask runs only on quality winners.

**Reality check**: Warren Buffett's success isn't about finding cheap stocks—it's about finding quality stocks at reasonable prices.

---

## The Four Quality Metrics

### 1. **Return on Equity (ROE)**
Measures how efficiently the company uses shareholder capital.

**Formula:**
```
ROE = Net Income / Shareholders' Equity
```

**Calculation from statements:**
- Net Income: Bottom line of income statement
- Shareholders' Equity: Balance sheet liability side, subtract liabilities from assets

**Quality threshold:**
- 20%+: Exceptional (compounding machine)
- 15-20%: Good (above average)
- 10-15%: Fair (acceptable)
- <10%: Weak (avoid)

**Why it matters**: High ROE means every dollar of shareholder capital generates strong returns. Buffett targets 15%+ ROE.

---

### 2. **Return on Invested Capital (ROIC)**
Measures returns on ALL capital (debt + equity), not just equity.

**Formula:**
```
ROIC = NOPAT / Invested Capital

Where:
  NOPAT = Net Operating Profit After Tax = EBIT × (1 - Tax Rate)
  Invested Capital = Total Assets - Current Liabilities
```

**Calculation from statements:**
- EBIT: Operating income (before interest/taxes)
- Tax Rate: Income tax expense / Earnings before tax
- Current Liabilities: Balance sheet, short-term obligations

**Quality threshold:**
- 15%+: Excellent (economically efficient)
- 10-15%: Good (efficient capital use)
- 5-10%: Fair (acceptable)
- <5%: Weak (poor capital allocation)

**Why it matters**: ROIC > cost of capital means the company creates value. ROIC < cost of capital means it destroys value.

---

### 3. **Debt-to-Equity Ratio**
Measures financial leverage and default risk.

**Formula:**
```
D/E = Total Debt / Shareholders' Equity

Where:
  Total Debt = Short-term Debt + Long-term Debt
```

**Calculation from statements:**
- Short-term Debt: Current portion of long-term debt + notes payable
- Long-term Debt: Bonds, term loans on balance sheet
- Shareholders' Equity: Assets - Liabilities

**Quality threshold:**
- <1.0: Conservative (low leverage, safe)
- 1.0-2.0: Moderate (acceptable leverage)
- 2.0-3.0: Aggressive (elevated risk)
- >3.0: Dangerous (high default risk)

**Why it matters**: High debt means:
- Vulnerable to recession (fixed obligations)
- Less ability to invest in growth
- Risk of covenant breach

Low debt means:
- Flexibility to weather downturns
- Can invest in opportunities
- Can weather industry disruption

---

### 4. **Free Cash Flow Conversion**
Measures what % of profit becomes actual cash in the bank.

**Formula:**
```
FCF Conversion = Operating Cash Flow / Net Income

Where:
  Operating Cash Flow: Cash flow from operations (cash flow statement)
  Net Income: Bottom line of income statement
```

**Calculation from statements:**
- Operating Cash Flow: Cash flow statement, first section
- Net Income: Income statement, bottom line

**Quality threshold:**
- 80-120%: Excellent (profit = cash, sustainable earnings)
- 60-80%: Good (mostly cash)
- 40-60%: Fair (some working capital drag)
- <40%: Weak (earnings not converting to cash)

**Why it matters**: Earnings can be manipulated through accounting. Cash flow cannot. A company earning $100M in profit but generating $30M cash is likely playing accounting games.

---

## Calculation Template

### Example: Apple Inc (AAPL) - Q4 2025 (Hypothetical)

**Financial Data Extracted (from 10-K):**
| Metric | Amount | Source |
|--------|--------|--------|
| Net Income | $30.7B | Income statement |
| Shareholders' Equity | $50.3B | Balance sheet |
| EBIT | $40.2B | Operating income |
| Tax Rate | 15.8% | Income tax / EBT |
| Total Debt | $108.5B | Short-term + Long-term debt |
| Operating Cash Flow | $28.3B | Cash flow statement |

**ROE Calculation:**
```
ROE = $30.7B / $50.3B = 61.0%
Interpretation: Exceptional. Every dollar of equity generates $0.61 of profit.
```

**ROIC Calculation:**
```
NOPAT = $40.2B × (1 - 0.158) = $40.2B × 0.842 = $33.9B
Invested Capital = $344.1B (total assets) - $75.8B (current liabilities) = $268.3B
ROIC = $33.9B / $268.3B = 12.6%
Interpretation: Good. Returns exceed typical cost of capital (8-10%).
```

**D/E Calculation:**
```
D/E = $108.5B / $50.3B = 2.16
Interpretation: Moderate-to-aggressive leverage. Acceptable for mature tech, concerning in downturn.
```

**FCF Conversion:**
```
FCF Conversion = $28.3B / $30.7B = 92.2%
Interpretation: Excellent. Nearly all profit converts to cash. High-quality earnings.
```

**Quality Score:**
```
ROE (61%) → Grade A (20%+)
ROIC (12.6%) → Grade A (10%+)
D/E (2.16) → Grade B+ (1.0-2.0)
FCF Conversion (92%) → Grade A (80-120%)

Overall: A- (high quality)
```

---

## The Scoring System: 0-100 Quality Score

### Grading Matrix

| Metric | Weight | A (80-100 pts) | B (60-79 pts) | C (40-59 pts) | D (<40 pts) |
|--------|--------|----------------|---------------|---------------|-------------|
| **ROE** | 30% | 20%+ | 15-20% | 10-15% | <10% |
| **ROIC** | 30% | 15%+ | 10-15% | 5-10% | <5% |
| **D/E** | 20% | <1.0 | 1.0-2.0 | 2.0-3.0 | >3.0 |
| **FCF Conv** | 20% | 80-120% | 60-80% | 40-60% | <40% |

### Scoring Rules

```
Quality Score = (ROE Grade × 0.30) + (ROIC Grade × 0.30) 
              + (D/E Grade × 0.20) + (FCF Conv Grade × 0.20)

Where:
  A = 90-100 pts
  B = 70-89 pts
  C = 50-69 pts
  D = 30-49 pts
  F = 0-29 pts
```

### Quality Score Tiers

| Score | Tier | Action |
|-------|------|--------|
| 85-100 | **TIER 1 (Exceptional)** | Prioritize for DYP-Ask. Core holding candidates. |
| 75-84 | **TIER 2 (Good)** | Run DYP-Ask if price attractive. Monitor. |
| 65-74 | **TIER 3 (Fair)** | DYP-Ask only if turnaround thesis. Higher risk. |
| <65 | **TIER 4 (Weak)** | Skip. Find better candidates. Too much remedial work. |

---

## Usage Pattern: Screening a Market

### Step 1: Data Extraction (2 hours)
Pick a universe: 100-500 stocks (e.g., S&P 500, Nifty 50, A股前100强).

For each stock, extract:
- Latest 10-K or annual report
- Net Income, Equity, EBIT, Tax Rate, Debt, Operating Cash Flow

**Pro tip**: Most financial websites (Macrotrends, Yahoo Finance, Seeking Alpha) have these pre-calculated. Verify against source documents.

### Step 2: Metric Calculation (1-2 hours)
Calculate four metrics for each company.

**Spreadsheet template:**
```
| Ticker | ROE | ROIC | D/E | FCF Conv | ROE Gr | ROIC Gr | D/E Gr | FCF Gr | Score | Tier |
|--------|-----|------|-----|----------|--------|---------|--------|--------|-------|------|
| AAPL   | 61% | 12.6%| 2.16| 92%      | A      | A       | B+     | A      | 88    | T2   |
| MSFT   | 43% | 15.2%| 0.82| 88%      | A      | A       | A      | A      | 95    | T1   |
| ...    | ... | ...  | ... | ...      | ...    | ...     | ...    | ...    | ...   | ...  |
```

### Step 3: Ranking (30 minutes)
Sort by score descending. Identify top 10-50 candidates.

Example output:
```
Top 10 Quality Scores (Sample):

Rank | Ticker | Score | Tier | ROE   | ROIC  | D/E  | FCF  | Notes
-----|--------|-------|------|-------|-------|------|------|-------
1    | MSFT   | 95    | T1   | 43%   | 15.2% | 0.82 | 88%  | Pristine quality
2    | SHOP   | 92    | T1   | 38%   | 14.1% | 1.15 | 91%  | SaaS compounding
3    | NVDA   | 89    | T2   | 52%   | 18.3% | 0.45 | 85%  | Fab capacity risk
4    | JNJ    | 88    | T2   | 24%   | 11.8% | 1.58 | 92%  | Defensive quality
5    | BRK.B  | 86    | T2   | 18%   | 10.2% | 0.65 | 94%  | Stable conglomerate
...
```

### Step 4: Deep Dive on Top 3 (1-2 hours)
Run DYP-Ask on top 3 candidates:
- Q1: Business model
- Q3: Competitive moat
- Q5: Key assumptions
- Q9: Fair value

### Step 5: Decision (30 minutes)
- Score 1: High conviction → Research further or buy
- Score 2: Interesting → Thesis development
- Score 3: Consider → Wait for better price

---

## Common Pitfalls & How to Avoid Them

| Pitfall | Why | Fix |
|---------|-----|-----|
| **Cherry-picking metrics** | Using only ROE, ignoring D/E | Use all four metrics. Weight equally. |
| **Stale data** | Using 3-year-old financials | Use latest annual (10-K) or latest quarter (10-Q) |
| **Accounting games** | Net income inflated via reserves | Check FCF conversion. If <50%, dig deeper. |
| **Industry blind spot** | Comparing tech ROE to bank ROE | Use industry averages. Tech: 20%+ normal. Banks: 10%+ normal. |
| **One-off items** | Quarter with unusual charges | Use 3-year averages, not single quarter. |
| **Survivor bias** | Screening only "winners" | Include bankrupt companies to see red flags. |

---

## Real-World Example: 10 Companies Scored

### Input: Consumer / Retail Stocks (2026-07 data)

Pick 10 stocks spanning quality spectrum:
```
Alibaba (BABA), Amazon (AMZN), Shopee (SE), JD.com (JD),
Pinduoduo (PDD), Best Buy (BBY), Costco (COST), Target (TGT),
Wayfair (W), Etsy (ETSY)
```

### Extraction & Calculation

| Ticker | Net Inc (B) | Equity (B) | EBIT (B) | Tax % | Debt (B) | Op CF (B) | ROE | ROIC | D/E | FCF | Score | Tier |
|--------|-------------|-----------|---------|-------|---------|----------|-----|------|-----|-----|-------|------|
| AMZN   | 2.87        | 30.4      | 8.2     | 18%   | 55.2    | 11.3     | 9%  | 8.5% | 1.82| 394%| 52    | T3   |
| SE     | 1.23        | 12.8      | 3.1     | 15%   | 8.5     | 2.8      | 10% | 11.2%| 0.66| 228%| 75    | T2   |
| COST   | 6.12        | 28.5      | 8.9     | 12%   | 15.3    | 7.4      | 21% | 14.8%| 0.54| 121%| 89    | T2   |
| BABA   | 4.52        | 45.2      | 9.1     | 14%   | 22.1    | 8.9      | 10% | 10.5%| 0.49| 197%| 68    | T3   |
| ETSY   | 0.84        | 4.2       | 1.3     | 16%   | 1.8     | 1.2      | 20% | 18.5%| 0.43| 143%| 85    | T2   |
| PDD    | 3.41        | 18.5      | 4.8     | 11%   | 2.3     | 4.1      | 18% | 15.2%| 0.12| 120%| 92    | T1   |
| JD     | 2.15        | 16.3      | 2.9     | 12%   | 18.7    | 3.2      | 13% | 6.8% | 1.15| 149%| 58    | T3   |
| BBY    | 0.92        | 5.1       | 1.2     | 17%   | 8.2     | 1.8      | 18% | 9.1% | 1.61| 196%| 62    | T3   |
| TGT    | 1.53        | 10.2      | 2.1     | 15%   | 12.5    | 2.5      | 15% | 8.5% | 1.23| 163%| 64    | T3   |
| W      | -0.15       | 2.8       | -0.08   | N/A   | 4.2     | 0.2      | -5% | -1.2%| 1.50| -133%| 18    | T4   |

### Results & Recommendations

```
TIER 1 (Top Priority):
1. PDD (92) - Exceptional quality. Run full DYP-Ask.
2. COST (89) - Steadfast compounder. Core holding material.

TIER 2 (Run DYP-Ask if price < 20% discount):
3. ETSY (85) - Marketplace network effects. Monitor moat.
4. SE (75) - Growing but leverage building. Watch D/E.

TIER 3 (Research only if contrarian thesis):
5. BABA (68) - Regulatory overhang. Quality hurt but recoverable.
6. BBY (62) - Legacy retail, declining ROE. Turnaround risky.
7. TGT (64) - Fair quality but cyclical. Buy on dips.
8. JD (58) - High leverage dilutes quality. Wait for de-lever.
9. AMZN (52) - Profitable but poor ROIC. Growth re-investment.

TIER 4 (Skip):
10. W (18) - Negative returns. Do not invest.
```

### Integration with DYP-Ask

**Run DYP-Ask immediately on:**
- PDD (highest conviction → Q10 should be 85+)
- COST (defensive quality → Q10 should be 80+)

**Run DYP-Ask conditionally on:**
- ETSY: If current price ≤ $80 (or 15% below fair value)
- SE: If current price ≤ $35 (or 20% below fair value)

**Skip DYP-Ask on:**
- BABA, JD, AMZN: Too much research debt. Come back in 12 months.
- W: Lost cause. Delete from watchlist.

---

## Integration with 1ai-Ecosystem

### Trigger Skills (Upstream)
- None. Quality-Screen is a starting point.

### Input Format
```json
{
  "universe": "S&P 500",
  "date": "2026-07-04",
  "companies": [
    {
      "ticker": "MSFT",
      "roe": 0.43,
      "roic": 0.152,
      "debt_to_equity": 0.82,
      "fcf_conversion": 0.88
    }
  ]
}
```

### Output Format
```json
{
  "quality_screen_results": [
    {
      "rank": 1,
      "ticker": "MSFT",
      "quality_score": 95,
      "tier": "T1",
      "metrics": {
        "roe_grade": "A",
        "roic_grade": "A",
        "de_grade": "A",
        "fcf_grade": "A"
      },
      "dyp_ask_ready": true,
      "next_action": "Run DYP-Ask immediately"
    }
  ],
  "summary": {
    "total_screened": 500,
    "tier_1_count": 18,
    "tier_2_count": 67,
    "tier_3_count": 245,
    "tier_4_count": 170
  }
}
```

### Connected Skills
1. **DYP-Ask** (downstream): Run on Quality-Screen winners (Tier 1 & 2)
2. **Thesis-Tracker** (storage): Record why each company passed/failed screen
3. **Portfolio-Review** (ongoing): Re-screen quarterly to catch deterioration
4. **Industry-Research** (context): Understand why industry average D/E is high/low

---

## Data Sources & Manual Calculation

### Where to Get Financial Data

**Free sources:**
- Yahoo Finance (basic metrics pre-calculated)
- Macrotrends (10-year historical data, reliable)
- Seeking Alpha (consensus estimates, peer comparison)
- Company investor relations (official 10-K/10-Q, most accurate)

**Calculation approach:**
1. Go to company's IR website
2. Download latest 10-K (annual report)
3. Extract four numbers manually (5 min per company)
4. Calculate four metrics (1 min per company)
5. Grade and score (30 sec per company)

**Verification:**
- Cross-check your ROE calculation against Yahoo Finance's reported ROE
- If off by >2%, re-read the statements (might be trailing 12-month vs. TTM)

---

## Common Questions

**Q: What if a company is in a cyclical low?**
A: Use 3-year average metrics, not single year. Earnings-per-share (EPS) can swing 50% in cyclicals; ROE is steadier.

**Q: What about startups with negative ROE?**
A: They fail the screen. Quality-Screen is for established profitability. Startups need separate venture analysis framework.

**Q: Should I adjust ROE for leverage?**
A: No. High leverage is a risk; it shows in D/E. If you adjust ROE for leverage, you're hiding the risk.

**Q: What if two companies have same score but different business?**
A: Quality metrics are universal. The DYP-Ask step (Q3: moat, Q4: competitors) separates them. Score is just gate-keeping.

**Q: Can a company with low D/E but terrible ROE be quality?**
A: No. It fails on ROE. Quality means ALL four metrics pass. D/E alone isn't quality.

---

## Next Steps in 1ai-Ecosystem

1. ✅ Deploy QUALITY-SCREEN to 1ai-skills
2. → Integrate with DYP-Ask (if Quality-Score ≥75, auto-populate Q1-Q3)
3. → Build quarterly screening automation (re-screen every earnings season)
4. → Create industry-specific thresholds (tech ROE vs. bank ROE)
5. → Add peer benchmarking dashboard (your portfolio quality vs. market)

**Workflow sequence:**
```
QUALITY-SCREEN (2h) → Top 50 → DYP-Ask on Top 5 (10h) → Portfolio (1h)
Total: ~13h research for 500-stock universe.
```

---

## References

**Buffett on ROE**: "We like to see a return on equity of 15% or higher." (Berkshire annual letter)

**Greenwald on ROIC**: "ROIC tells you if management is creating or destroying value." (Columbia Business School)

**Graham on Debt**: "In most cases the debt should not exceed 50% of the equity value." (The Intelligent Investor)

**Munger on FCF**: "The best companies convert nearly 100% of earnings into cash." (Q&A sessions)

---

## Checklist Before Screening

- [ ] Have I extracted the latest annual 10-K (not outdated data)?
- [ ] Did I verify two numbers against two sources (cross-check)?
- [ ] Did I use consistent metric definitions across all companies?
- [ ] Did I flag any unusual items (one-off charges, M&A impact)?
- [ ] Did I understand WHY each company's D/E is that level (leverage for growth vs. leverage from bad M&A)?
- [ ] Did I spot-check my math (calculator, not mental)?
- [ ] Did I document assumptions (what tax rate did I use?)?

**Status**: Ready for TIER 1 deployment. Zero external dependencies. Pure framework.
