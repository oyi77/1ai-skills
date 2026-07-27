---
name: wolf-finance
description: "ACTIVATE for ANY finance, investment, trading, or market query. Comprehensive value investing framework combining Buffett, Munger, Duan Yongping, and Li Lu methodologies. Use when making investment decisions."
domain: financial
license: Apache-2.0
tags: [analysis, crypto, finance, investment, testing, trading, wolf, money, value-investing]
version: "2.0.0"
author: ""
subdomain: ""
type: finance
---
# Money-Making Overview

Systematic value investing compounds at 15-25% annually. A $50K portfolio following this framework generates $7.5K-12.5K/year. With position sizing and margin of safety, drawdowns stay under 20%. One good investment thesis can return 2-10x over 3-5 years.

## Revenue Streams

1. Personal Portfolio — compound your own capital
2. Investment Research ($2K-10K/report) — sell theses to funds/family offices
3. Portfolio Management (0.5-1.5% AUM) — manage for others
4. Newsletter/Picks ($19-97/mo) — publish investment ideas

## First Action in 60 Minutes

```bash
#!/usr/bin/env bash
# Portfolio health check
mkdir -p ~/wolf-finance/{holdings,research,theses,reviews}

echo "=== Portfolio Health Check ==="
echo "1. List ALL current holdings with cost basis"
echo "2. Run 7-factor Quality Screen (eliminate weak positions):"
echo "   - Declining revenue (3yr) -> RED FLAG"
echo "   - Increasing debt/equity -> RED FLAG"
echo "   - Negative free cash flow -> RED FLAG"
echo "   - Insider selling >50% -> RED FLAG"
echo "   - Losing market share -> RED FLAG"
echo "   - Regulatory risk -> RED FLAG"
echo "   - Overvalued (P/E > 3x industry) -> RED FLAG"
echo "3. Flag any position with 3+ red flags for review"
echo "4. Check thesis: has anything fundamentally changed?"
echo "5. Decision: HOLD, INCREASE, or EXIT each position"
```

## Anti-Rationalization Table

| Excuse | Truth |
|---|---|
| "I need more information before deciding" | You have enough to decide. More info = more noise. |
| "The market is too volatile right now" | Volatility is when value investors buy |
| "I should wait for a better entry" | DCA in. Time in market > timing the market |

## Output Format

On completion: "Portfolio: [N] positions, $[N] value, [N] red flags, [N] thesis updates needed, [N] actions taken"

---

# Wolf Finance

## When to Use

**Trigger phrases:**
- "wolf finance"
- "Use when working with wolf finance"


- Analyzing any financial asset (equities, crypto, forex, commodities, derivatives)
- Building investment theses with evidence-tiered backing (T1/T2/T3)
- Running pre-trade risk gates before position entry
- Portfolio construction and risk management across asset classes
- Institutional-grade reporting for investment committees
- Deep company research and valuation
- Management quality assessment and due diligence
- Quality screening of investment candidates


## When NOT to Use

- For personal financial advice (consult a licensed advisor)
- When the analysis requires real-time market data you do not have
- For tax or legal decisions (consult professionals)


## Overview

Wolf Finance provides finance operations with accuracy and compliance. Integrates comprehensive investment research frameworks drawn from Buffett, Munger, Duan Yongping, and Li Lu — from quality screening through deep company research to final decision memorandum.

## Workflow

```python
# Example: Portfolio risk calculation
def calculate_risk(returns: list[float]) -> dict:
    import statistics
    mean = statistics.mean(returns)
    stdev = statistics.stdev(returns)
    sharpe = mean / stdev if stdev > 0 else 0
    return {"mean": mean, "stdev": stdev, "sharpe_ratio": sharpe}
```

1. **Gather data** — Collect financial data from authoritative sources
2. **Analyze** — Apply financial models and calculations
3. **Validate** — Cross-check results against benchmarks
4. **Report** — Generate clear, actionable financial reports
5. **Recommend** — Provide data-driven suggestions

## Key Metrics

- Revenue and growth rates
- Profit margins (gross, operating, net)
- Cash flow and burn rate
- Return on investment (ROI)
- Risk-adjusted returns

## Compliance

- Follow GAAP/IFRS standards where applicable
- Maintain audit trail for all calculations
- Redact sensitive financial data in reports
- Document assumptions and methodologies

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "The market will recover" | Do not hope. Analyze. Set stop-losses and follow your strategy. |
| "I do not need to track expenses" | What you do not measure, you cannot optimize. Track everything. |
| "One spreadsheet is enough" | Financial models need version control and audit trails. Use proper tools. |

## Financial Data Standards

Every key financial data point MUST come from two independent sources. Flag discrepancies > 1%.

**Data source priority by market:**

| Market | Primary Source | Secondary Source | Raw Filings |
|--------|---------------|------------------|-------------|
| US stocks | macrotrends.net | stockanalysis.com | SEC EDGAR 10-K/Q |
| HK stocks | aastocks.com | macrotrends (ADR) | HKEX disclosure |
| A-share | eastmoney.com | cninfo.com.cn | CNINFO original PDF |

**Error calculation**:
```
Error rate = |source1 - source2| / source1 x 100%
```

| Error | Action |
|-------|--------|
| <= 1% | Use source1 value, cite both |
| 1-5% | Flag discrepancy, note possible cause (exchange rate, accounting method) |
| > 5% | Must check original filing — do not use |

**Common discrepancy causes**: GAAP vs Non-GAAP, exchange rate timing, fiscal year definitions, consolidation scope, data lag.

**Mandatory calculation verification** — use tooling, never LLM mental math:
- Market cap: `python3 tools/financial_rigor.py verify-market-cap --price {price} --shares {shares} --reported {reported_mcap} --currency {currency}`
- Valuation: `python3 tools/financial_rigor.py verify-valuation --price {price} --eps {eps} --bvps {bvps} --fcf-per-share {fcf} --dividend {dividend}`
- Cross-validation: `python3 tools/financial_rigor.py cross-validate --field {field} --values '{"source1": val, "source2": val}' --unit {unit}`
- Three-scenario valuation: `python3 tools/financial_rigor.py three-scenario --price {price} --eps {eps} --shares {shares} --growth {opt} {base} {pess} --pe {opt_pe} {base_pe} {pess_pe} --years 3`

## Investment Research Framework

An 8-module systematic investment research process combining the frameworks of Buffett, Munger, Duan Yongping, and Li Lu.

### Step 0: AI Research Bias Awareness

Before starting, rate the company's "AI-researchability" to identify potential data bias:

| Grade | Feature | AI Research Trap | Strategy |
|-------|---------|-----------------|----------|
| A (info-rich) | Listed long time, heavy analyst coverage | Consensus too strong — AI output converges to market pricing, limited alpha | Focus on devil's advocate: why don't smart people buy? What risks are overlooked? |
| B (moderate info) | Listed 1-3yr, limited coverage | AI fills gaps with "reasonable estimates" — looks complete but gives false certainty | Label confidence on every estimated data point |
| C (info-scarce) | New listing/obscure/emerging market, near-zero coverage | AI over-cautious due to lack of data — misreads as "unclear = bad" | First-principles mode: focus on core business questions, not report completeness |

**Bias self-check** (maintain throughout research):
- Is my "certainty" from business quality or data volume?
- Would halving available data change my conclusion?
- Is my output highly similar to market consensus? Where is my information advantage?
- Am I underestimating the possibility that a great business has little public data?

### Step 1: Data Collection

Collect using parallel research agents:

1. Revenue structure: segment revenue, growth rates, gross margins
2. Financials: 5yr revenue, net income, margins, FCF, cash position
3. Competitive landscape: market share, key competitors
4. Business model & moat: core competitive advantages
5. Technology: core tech stack, R&D investment
6. Management: CEO background, ownership, key decisions
7. Industry: TAM, growth forecasts
8. Risk factors: geopolitical, regulatory, supply chain
9. Current valuation: market cap, PE, PS, PEG, EV/Revenue
10. Bull and bear case core arguments

**Cross-validate every key data point** using the Financial Data Standards section above and the `financial_rigor.py` tool suite. Never rely on LLM mental arithmetic for calculations.

**Common error prevention**:
- Market cap unit: HKD bn vs RMB bn vs USD bn — easy to misplace a zero
- FCF definition: capex scope varies (leases, acquisitions)
- Debt scope: whether operating lease liabilities are included
- Ownership: AB-share companies — economic interest != voting rights

### Step 2: Business Essence Analysis (Duan Yongping "Right Business")

- Define the business in one sentence
- Revenue structure decomposition (table)
- 5-year profitability trends (table)
- Business model canvas: one-time sale vs subscription/recurring? Hardware vs software vs platform?
- Ecosystem stickiness / customer lock-in strength
- Gross margin vs peers — explain why high or low
- Operating leverage analysis
- **Duan Yongping-style question**: What makes this business good? If you could describe it in one sentence, what is it?

### Step 3: Moat Assessment (Buffett "Economic Moat")

Evaluate each moat type:

| Moat Type | Verification Method |
|-----------|-------------------|
| Brand / pricing power | Can it raise price without losing volume? |
| Switching costs | How expensive is it for customers to switch? |
| Network effects | Does the product get better with more users? |
| Scale advantages | How significant are cost advantages from scale? |
| Technology / patent barriers | How many years ahead? Can it be replicated? |

Analyze moat trend: wider or narrower in the past 5 years? Outlook for the next 5 years.

**Buffett-style question**: Will this moat still exist in 10 years? What could destroy it?

### Step 4: Reverse Thinking & Risk Checklist (Munger "Invert, Always Invert")

- List every way this company could fail (table: path / probability / impact)
- Historical analogies: find companies in similar positions — what happened?
- Cross-disciplinary analysis: network effect theory, tech adoption curves, game theory
- Bias check: narrative bias, anchoring, survivorship bias
- Collect the bear case core arguments
- **Munger-style question**: Where am I most likely to be wrong? Why would smart people not buy / short this stock?

### Step 5: Management Assessment (Duan Yongping "Right People" + Buffett "Management Integrity")

- CEO/founder key decision review (table: time / decision / outcome / score)
- Capital allocation ability: R&D returns, M&A success rate, buyback timing
- Shareholder alignment: management ownership, compensation structure, insider selling records
- Organizational capability: team stability, key person risk
- Culture characteristics
- **Duan Yongping-style question**: If the CEO retired tomorrow, could this company still compete?

### Step 6: Industry & Civilization Trend (Li Lu "Civilization Evolution Framework")

- Is the industry in a "civilization-level paradigm shift"?
- Historical technology revolution analogy (steam/electricity/internet/AI)
- TAM growth curve and ceiling analysis
- Company position in the industry value chain
- Technology roadmap risk
- Customer/supplier concentration analysis
- **Li Lu-style question**: Looking back 20 years from now, is this company "the Standard Oil of this era" or "a flash-in-the-pan 3Com"?

### Step 7: Valuation & Margin of Safety (Buffett "Intrinsic Value" + Duan Yongping "Right Price")

- Current market pricing (key valuation metrics table) — MUST verify with tooling
- Reverse DCF: what growth does the current price imply?
- Three-scenario DCF valuation — MUST calculate with tooling, never mental math
- Comparison with own historical valuation
- Comparison with peer valuation
- **Duan Yongping-style question**: If the stock market closed for 5 years tomorrow, would you still be happy to own at this price?

### Step 8: Comprehensive Decision Memorandum

Summary table:

| Dimension | Conclusion | Confidence |
|-----------|-----------|------------|
| Business quality (Duan Yongping) | | |
| Moat (Buffett) | | |
| Management (Duan + Buffett) | | |
| Biggest risk (Munger) | | |
| Civilization trend (Li Lu) | | |
| Valuation (Buffett + Duan) | | |

Decision table:

| Strategy | Recommendation |
|----------|---------------|
| Not holding | |
| Holding | |
| Sell signal | |
| Add signal | |

**Report must include**:
1. Information richness grade (A/B/C) and AI research limitations statement at the top
2. Distinguish "AI analysis confidence" (depends on data availability) from "investment certainty" (depends on business quality)
3. For C-grade companies: include "questions needing primary verification" list
4. Data spot-check before release using `tools/report_audit.py`

## Value Investing Pre-Buy Checklist

A 6-gate checklist adapted from the Buffett-Munger framework. Each gate scored *1-5.

### Gate 1: Can I Understand This Business? (Circle of Competence)

- [ ] Can you explain how the company makes money in one sentence?
- [ ] What will it most likely still be doing in 10 years?
- [ ] What key variables determine success or failure?
- [ ] Is your understanding from deep research or hearsay?

**Hard veto**: if you cannot clearly describe how it makes money, mark "outside competence — no analysis."

### Gate 2: Is This a Good Business? (Economic Characteristics)

| Metric | Company Value | Reference Standard | Pass? |
|--------|-------------|-------------------|-------|
| ROE (5yr avg) | | > 15% good, > 20% excellent | |
| Gross margin | | > 40% suggests pricing power | |
| Free cash flow | | Consistently positive, near net income | |
| Capex intensity | | Asset-light > asset-heavy | |
| Debt level | | Interest-bearing debt / net profit < 3yr | |

Scoring: *1-5 based on how many standards are met and whether trends are improving or deteriorating.

### Gate 3: Is the Moat Deep Enough? (Competitive Advantage)

Check each type:

| Moat Type | Evidence | Widening or Narrowing? |
|-----------|----------|----------------------|
| Brand / pricing power | | |
| Switching costs | | |
| Network effects | | |
| Cost / scale advantage | | |
| Technology / patent barriers | | |

**Additional test**: If a competitor had $10B, could they replicate this business?

### Gate 4: Can Management Be Trusted? (People Factor)

| Check | Assessment |
|-------|-----------|
| Honesty (promises vs delivery) | |
| Capital allocation (buyback/dividend/M&A track record) | |
| Shareholder alignment (ownership, compensation) | |
| Owner mindset (founder vs professional manager) | |
| Governance (related-party transactions, goodwill, audit) | |
| Would the company run well without the CEO? | |

**Hard veto**: severe integrity issues.

### Gate 5: Is the Price Cheap Enough? (Margin of Safety)

| Metric | Value | Historical Percentile | Assessment |
|--------|-------|---------------------|------------|
| PE (TTM) | | | |
| Forward PE | | | |
| PB | | | |
| Dividend yield | | | |
| FCF Yield | | | |

**Three-scenario valuation** — MUST use tooling, never mental math:
```
python3 tools/financial_rigor.py three-scenario \
  --price {price} --eps {eps} --shares {shares} \
  --growth {opt} {base} {pess} --pe {opt_pe} {base_pe} {pess_pe} --currency {currency}
```

- If wrong, what is maximum downside at current price?
- Would you add if the stock halved?

### Gate 6: Position Sizing & Decision Discipline

- Is FOMO driving the decision?
- Are you buying only because someone recommended it?
- Could you accept a 5-year trading halt?
- Can the buy thesis be written in under 200 words?

### Final: Mirror Test

Write:
> "I am buying ___ at ___ because:
> 1. The business essence is ___, I understand it;
> 2. Its moat is ___ and it is widening/narrowing;
> 3. Management is ___ worthy/unworthy of trust;
> 4. Current price represents ___ of intrinsic value, ___ sufficient/insufficient margin of safety;
> 5. Even if I am wrong, downside is controllable/uncontrollable because ___."

**Cannot complete in 5 sentences = do not buy.**

### Quick Veto List

- [ ] Cannot clearly explain how the company makes money
- [ ] 3 consecutive years of negative FCF with no sign of improvement
- [ ] Management integrity issues
- [ ] Competitive advantage being irreversibly eroded
- [ ] Thesis requires "a greater fool" to pay more later
- [ ] Cannot afford the investment going to zero
- [ ] Main reason to buy is "everyone else is buying" or "it has been going up"
- [ ] Cannot write the buy thesis in under 200 words

## Quality Screen: 7-Factor Elimination Criteria

Quickly filter out non-first-class companies using 7 hard criteria with 3 exemption rules.

### The 7 Criteria

| # | Metric | Elimination Condition | What It Measures |
|---|--------|---------------------|-----------------|
| 1 | 10yr avg ROE | < 8% | Capital efficiency — can equity beat opportunity cost? |
| 2 | 5yr cumulative FCF | Negative | Real cash generation vs paper profits |
| 3 | Interest coverage (EBIT/interest) | < 2x | Debt repayment safety |
| 4 | Long-term gross margin | < 15% | Pricing power — product differentiation |
| 5 | Operating CF / Net income (5yr avg) | < 0.7 | Profit quality — can profit be collected as cash? |
| 6 | Long-term net margin | < 5% | Resilience — does revenue volatility zero out profit? |
| 7 | 5yr share dilution | > 20% (non-M&A) | Shareholder interest — is management diluting you? |

### Exemption Rules

**A: Strategic Investment Period** (exempts Rule 1)
- Listed < 10 years
- Gross margin > 30% (proves business model has pricing power)
- Last 2 years operating CF positive (proves self-sustaining)

**B: Active Low-Margin Strategy** (exempts Rule 6)
- Gross margin > 30% (can earn but chooses not to)
- Last 2 years net margin back above 5% or in clear uptrend

**C: High-Turnover Thin-Margin Model** (exempts Rules 4 and 6)
- ROE > 20%
- Operating CF / Net income > 1.0
- Business model is "membership / platform commission / high-turnover thin-margin"

### Notes

- Banks/insurance: Rule 3 (interest coverage) does not apply
- REITs: use core operating profit ROE instead
- Cyclicals: use full-cycle averages (cover at least one peak and one trough)
- Short listing history (< 5yr): use all available data, flag "insufficient data window"
- Data deficiency: mark as "data insufficient" rather than passing/failing

**Passing screen does not equal "good investment"** — it means the company survived first-pass elimination. Further research on business model sustainability, management, valuation, and competitive dynamics is still required.

## Management Deep Dive

Deep management quality assessment when standard management scoring is uncertain (*** or below) or management is the core investment thesis.

### Framework

#### 1. Key Person Identification
Identify CEO, CFO, founder (if not CEO), controlling shareholder, other key executives. Distinguish "who makes decisions" from "who has the title."

#### 2. CEO Capability Assessment

**Strategic vision**: Review CEO public statements (letters to shareholders, earnings calls, interviews, social media) over the past 5 years. Extract predictions and compare with actual outcomes.

| Time | CEO's Judgment/Prediction | Actual Outcome | Accuracy |
|------|--------------------------|----------------|:--------:|

- Has the CEO made correct judgments ahead of the market?
- Has the CEO stayed calm when everyone was overly optimistic?
- Independent thinking vs following consensus?

**Execution ability**:

| Dimension | Assessment | Evidence |
|-----------|-----------|----------|
| Strategy to execution | Did they deliver what they said? | |
| Organization | Can they attract and retain talent? | |
| Crisis handling | How did they respond to difficulties? | |
| Iteration speed | How fast do they correct mistakes? | |

#### 3. Integrity Assessment (Most Important)

**Promise vs delivery tracking** — extract specific commitments from past 3 years:

| # | Time | Commitment | Venue | Delivered? | Score |
|---|------|-----------|-------|-----------|-------|

Track record:
| Fulfillment Rate | Rating |
|:-----------------:|--------|
| > 80% | Excellent — say what they do |
| 60-80% | Acceptable — right direction, execution gap |
| 40-60% | Concerning — over-promise, under-deliver |
| < 40% | Severe issue — cannot be trusted |

**Crisis behavior**: Search for the company's major crises. How did management react?
- Proactive communication or avoidance?
- Internal attribution or external blame?
- Do the hard but right thing or pander to short-term markets?

**Stakeholder attitudes**:
| Stakeholder | Attitude | Evidence |
|-------------|----------|----------|
| Shareholders | Respect / ignore / exploit | |
| Employees | Good treatment / exploitation / indifference | |
| Customers | Customer-centric / short-term extraction | |
| Regulators | Compliance / gray-area play | |

#### 4. Capital Allocation Ability

**M&A record**:

| Time | Target | Amount | Strategic Logic | Result | Score(1-5) |
|------|--------|--------|-----------------|--------|:---------:|

**Buyback record**: Check valuation at time of buyback vs current.
**Dividend record**: Payout ratio vs FCF, sustainability.
**New business investment**: Area, cumulative spend, current status, return.

**Scoring**:

| Dimension | Score(1-5) | Notes |
|-----------|:----------:|-------|
| M&A discipline | | Right price? Integration success? |
| Buyback timing | | Buying low, stopping high? |
| Dividend rationality | | Payout matches FCF? |
| New business investment | | Success rate, stop-loss discipline |
| Cash management | | Reasonable reserves vs hoarding? |

#### 5. Governance Structure

- Dual-class share structure / super-voting rights
- Founder/controller ownership percentage
- Independent director independence
- Executive compensation vs net profit and peers
- Related-party transactions fairness

#### 6. CEO Exit Scenario

| Question | Answer |
|----------|--------|
| Can the company run normally if CEO leaves tomorrow? | |
| Management team depth — clear successor? | |
| Competitive advantage dependent on CEO or organization/systems? | |
| Historical CEO transitions — smooth? | |

#### 7. Comprehensive Scoring

| Dimension | Weight | Score(1-5) | Weighted |
|-----------|:------:|:---------:|:--------:|
| Integrity | 35% | | |
| Strategy & Execution | 25% | | |
| Capital allocation | 25% | | |
| Governance | 15% | | |
| **Composite** | 100% | | |

### Key Principles

- **Integrity is a veto** — incompetence can be learned, character cannot be fixed
- **Watch actions, not words** — what management does, not what they say
- **Crisis reveals truth** — anyone is a good CEO in good times; tough times reveal real skill
- **Capital allocation is the final exam** — making money is easy, deploying it well is hard
- **Never fall in love with management** — stay objective, even admirable people make big mistakes


## Investment Portfolio Management

Portfolio-level investment thesis tracking, drift analysis, and structured portfolio review. These systems are modeled after the disciplined buy-and-hold processes used by Buffett, Li Lu, and Duan Yongping — methods that transform portfolio management from reactive guessing into systematic oversight.

### When to Use

- Managing multi-position investment portfolio with thesis-backed rationale
- Tracking investment thesis evolution quarter-over-quarter
- Detecting thesis drift — separating fact changes from price changes and wording changes
- Running structured portfolio review and rebalancing
- Stress-testing portfolio against concentration, correlation, and macro scenarios

### When NOT to Use

- Intraday trading or short-term momentum decisions
- When you lack structured thesis documentation (baseline required for drift detection)
- For personal financial planning unrelated to portfolio positions

### Investment Thesis Tracker

The thesis tracker is a buy-and-hold discipline system that enforces documented reasoning before entry and systematic re-validation through quarterly check-ins.

**Design principle:** Most investors stop at research -> buy -> pray. Missing post-entry tracking causes reluctance to sell, panic-selling on drawdowns, and forgetting why you bought. The system answers one question at every check: *Would you still buy this today if you did not own it?*

**Two modes:**

**Mode A — Build Thesis:**
1. Collect current price, valuation (PE/PB/dividend yield), latest financial data via WebSearch
2. Validate valuation using `tools/financial_rigor.py verify-valuation`
3. Core thesis — answers these 5 questions in <=200 characters:
   - What is the business and how does it make money?
   - What is the moat and is it widening or stable?
   - Why is management trustworthy?
   - What discount to intrinsic value offers the margin of safety?
   - Why is downside risk controllable if wrong?
4. Decompose into 3-7 testable assumptions, each with verification method and frequency
5. Define red-line conditions (any triggers immediate re-evaluation): management integrity failure, core revenue decline 2+ quarters, moat breached, regulatory regime change, insider dumping
6. Record valuation anchor (buy price, PE, market cap, intrinsic value, margin of safety)
7. Save to `reports/{company}-thesis.md`

**Mode B — Track Thesis:**
1. Load existing thesis file
2. Gather latest data via WebSearch (quarterly results, major events, current price, insider trades)
3. Check each assumption against latest evidence — mark Green (valid), Yellow (weakening), Red (damaged), Black (broken)
4. Check red-line list — any triggered red-line gets flagged in report with action recommendation
5. Update valuation anchor
6. Compute thesis health score: `10 - (black_countx3) - (red_countx2) - (yellow_countx1) - (redline_triggersx5)`, min 1 max 10
7. Append check record to thesis file tracking table

**Key principles for thesis tracking:**
- Write sell conditions before buying — decisions made when calm are better than those made in panic
- Theses must be verifiable — "great company" is not a thesis, "ROE > 25% and trending up" is
- When a red-line triggers, act — "let us wait and see" is how large losses start
- Thesis broken != price down — a 30% price drop does not automatically mean sell; a broken thesis does
- Be honest about mistakes — admit when the thesis was wrong, do not hold out of ego

### Thesis Drift Detection

Separates genuine evidence changes from price noise and stylistic rewording by comparing two thesis snapshots across five fixed dimensions.

**Design principle:** The hardest thing about holding long-term positions is distinguishing:
- **Fact changes** — revenue, margins, competitive landscape, management behavior, capital allocation verifiably changed
- **Price changes** — market sentiment or valuation multiple shifted, but the business itself did not change
- **Wording changes** — two reports express things differently but underlying evidence and judgment are the same

**Three modes:**

**Mode A — Compare specified reports:**
1. Read both reports; extract date, company, core thesis, assumptions, red-lines, valuation anchor, management quality assessment, competition moat assessment, current action
2. Normalize evidence across both reports into a single comparison table
3. Validate all numerical changes using `tools/financial_rigor.py` — no LLM mental math
4. Judge each of 5 dimensions as **Improved / Unchanged / Weakened**:
   - Valuation anchor: intrinsic value, PE/PB/FCF Yield, margin of safety, target price range
   - Core assumptions list: revenue growth, margins, cash flow, users/orders/capacity
   - Red-line list: integrity, regulation, business decline, competition breakthrough, management anomaly
   - Management quality: integrity, capital allocation, buybacks/dividends, execution, shareholder friendliness
   - Competitive moat: market share, pricing power, network effects, cost advantage, substitution threat
5. Every non-Unchanged conclusion must cite specific new evidence (earnings line items, regulatory filings, news events, price vs fundamentals distinction)
6. If no evidence explains the change, judge **Unchanged** or **Cannot Determine**

**Mode B — Auto snapshot comparison:**
Find old and new thesis snapshots in `reports/{company}-thesis*.md`; verify same company, different dates; execute Mode A.

**Mode C — Missing baseline handling:**
State explicitly that drift detection cannot run without a historical baseline. Guide user to first build a thesis via the Thesis Tracker. Do not fabricate an old thesis from memory or market impression.

**Key principles for drift detection:**
- Evidence over wording — paraphrasing is not drift; only fact changes count
- Fundamentals over price — price changes only affect the valuation anchor, not business quality
- Red-lines have priority over cheap valuation — a triggered red-line is not neutralized by a low PE
- Every conclusion must trace to specific evidence

### Portfolio Review

A structured 7-step portfolio review process that treats portfolio management as a separate discipline from stock-picking.

**Design principle:** Researching companies is only half of investing. The other half is portfolio-level decisions: position sizing, funding source (new money vs swap), correlation with existing holdings, opportunity cost — every dollar should go where it earns the most.

**Seven steps:**

**Step 1: Parse positions** — Normalize input holdings into standard table (ticker, quantity, cost basis, current price, market value, weight, P&L). Support both proportional and unit formats. Load saved portfolio if available (`reports/portfolio-latest.md`).

**Step 2: Get current data** — Use parallel sub-agents via WebSearch for each position: current price and valuation (PE, PB, dividend yield), latest quarter financial changes, major recent events, analyst consensus. Validate with `tools/financial_rigor.py verify-valuation`.

**Step 3: Single-position health check** — For each position answer three questions:
1. Would you still buy at the current price if you did not own it?
2. Could you hold for 5 years without trading?
3. Is the buy thesis still intact?

**Step 4: Portfolio-level analysis:**
- **Concentration**: largest position (<40%), top 3 (50-80%), total holdings (5-15), cash (10-30%)
- **Correlation**: identify hidden risk resonance — same industry, same country/currency, same macro exposure, supply chain adjacency
- **Opportunity cost**: rank all positions by expected annual return x certainty. The lowest-ranked should beat cash (risk-free rate ~4%). If not, sell and hold cash
- **Stress test**: global recession, US-China escalation, interest rate spike, tech bubble burst — directional + rough magnitude per position

**Step 5: Optimization suggestions:**
- Specific rebalance actions (add/reduce/clear/hold/new) with current vs suggested weight and rationale
- Cash management recommendation

**Step 6: Output report** with executive summary covering: portfolio health rating (Outstanding / Good / Needs Attention / Severe), single most important action to take, biggest current risk

**Step 7: Save portfolio file** to `reports/portfolio-latest.md` with holdings table, review date, rebalance log, next review reminder

**Key principles for portfolio review:**
- Every dollar has an opportunity cost — holding a mediocre stock costs you the chance to own a great one
- Concentration is not risk; ignorance is — holding 3 deeply understood positions is safer than 30 you barely know
- Cash is a position — when no good opportunities exist, holding cash is not shameful
- Portfolio-level > individual stock level — a good stock in the wrong position size still hurts you
- Review quarterly, do not trade daily

## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run wolf finance workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings
- [ ] Financial data cross-validated from 2+ independent sources
- [ ] All calculations verified with financial_rigor.py tooling
- [ ] Research bias grade assigned (A/B/C)
