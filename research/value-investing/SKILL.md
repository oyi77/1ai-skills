---
name: value-investing
description: 'Use when evaluate stocks using Warren Buffett''s value investing: intrinsic
  value, margin of safety, and long-term moats. . Use when working with value investing.'
domain: research
author: oyi77
license: Apache-2.0
subdomain: research
tags:
- analysis
- investigation
- investing
- research
- value
version: 1.0.0
category: research
---

# Value Investing

## When to Use

**Trigger phrases:**
- "value investing"
- "Help me with value investing"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


## When NOT to Use

- When the answer is already known and documented
- For time-sensitive decisions that cannot wait for thorough research
- When the topic is outside your domain of competence


## Overview

Value investing is the disciplined practice of buying securities for less than their intrinsic worth to provide a margin of safety against permanent capital loss. Pioneered by Benjamin Graham and David Dodd in the 1930s and championed by Warren Buffett and Charlie Munger, it remains one of the most empirically validated approaches to long-term wealth creation in equities.

The core insight is that markets are not always efficient — short-term emotion (fear, greed, herding) creates pricing dislocations that the patient investor exploits. By rigorously estimating what a business is worth and only buying at a significant discount, the investor tilts probability in their favor across a portfolio of independent bets.

A complete value investing practice spans four pillars: (1) business quality assessment — identifying durable competitive advantages; (2) financial analysis — normalized earnings power, free cash flow conversion, balance sheet strength; (3) intrinsic valuation — DCF, sum-of-the-parts, earnings power value; (4) risk management — margin of safety, position sizing, thesis monitoring.

## Workflow

```python
# Discounted Cash Flow — estimate intrinsic value and margin of safety
def dcf_valuation(free_cash_flow: float, growth_rate: float,
                  terminal_growth: float, wacc: float,
                  projection_years: int = 10) -> dict:
    yearly = []
    for y in range(1, projection_years + 1):
        fcf = free_cash_flow * (1 + growth_rate) ** y
        pv = fcf / (1 + wacc) ** y
        yearly.append({"year": y, "fcf": round(fcf, 2), "pv": round(pv, 2)})
    terminal_value = yearly[-1]["fcf"] * (1 + terminal_growth) / (wacc - terminal_growth)
    pv_terminal = terminal_value / (1 + wacc) ** projection_years
    ev = sum(c["pv"] for c in yearly) + pv_terminal
    return {
        "enterprise_value": round(ev, 2),
        "terminal_value_pv": round(pv_terminal, 2),
        "max_buy_price_35pct_mos": round(ev * 0.65, 2),
        "yearly_cash_flows": yearly
    }
```

1. **Identify candidates** — Screen for undervaluation: low P/E, P/B, and P/FCF relative to history and industry. Source from 13F filings, corporate spin-offs, and out-of-favor sectors with catalysts.
2. **Assess business quality** — Evaluate competitive moat (brand, switching costs, network effects, cost advantages, intangibles). Read the annual report cover-to-cover. Do not value what you cannot understand.
3. **Analyze financial health** — Compute owner earnings (net income + D&A − maintenance capex). Review ROIC trends, leverage ratios, and FCF conversion over a full business cycle.
4. **Estimate intrinsic value** — Run a DCF with deliberately conservative assumptions. Cross-check with comparable company analysis. Stress-test: what growth or margin justifies the current price?
5. **Determine margin of safety** — Require 30-50% discount to intrinsic value for quality compounders, 50%+ for cyclical or commodity businesses. Adjust for regulatory, legal, and competitive risks.
6. **Size the position** — Allocate proportional to conviction-risk ratio: 5-15% for high-conviction, 2-5% for value plays, never exceed 20% single name. Hold cash when opportunities are scarce.
7. **Monitor and exit** — Track critical assumptions quarterly. Exit when price reaches intrinsic value, the thesis breaks, or a materially better opportunity appears.

## Source Evaluation

- **Authority** — Is the source credible and expert?
- **Currency** — Is the information recent and relevant?
- **Objectivity** — Is there bias or conflict of interest?
- **Accuracy** — Can claims be verified independently?

## Output Format

- Executive summary (1-2 paragraphs)
- Key findings (bullet points)
- Detailed analysis (sections with evidence)
- Recommendations (actionable next steps)
- Sources and methodology

## Code Examples

Automate value investing analysis with Python — screen for candidates and compute owner earnings.

### Stock Screening (Python + yfinance)

```python
import yfinance as yf

def value_screen(tickers: list[str], max_pe: float = 15, max_pb: float = 1.5) -> list[dict]:
    """Screen a watchlist for basic value characteristics: low P/E, low P/B, manageable debt, positive returns."""
    results = []
    for t in tickers:
        try:
            info = yf.Ticker(t).info
            pe = info.get("trailingPE") or info.get("forwardPE") or 999
            pb = info.get("priceToBook") or 999
            de = info.get("debtToEquity") or 0
            roic = info.get("returnOnInvestedCapital") or 0
            fcf = info.get("freeCashflow")
            mcap = info.get("marketCap") or 1
            results.append({
                "ticker": t, "name": info.get("shortName", ""),
                "pe": round(pe, 1), "pb": round(pb, 1),
                "de_ratio": round(de, 1), "roic_pct": round(roic * 100, 1),
                "fcf_yield_pct": round(fcf / mcap * 100, 1) if fcf else None,
                "pass": pe < max_pe and pb < max_pb and de < 100
            })
        except Exception as e:
            results.append({"ticker": t, "error": str(e)})
    return [r for r in results if r.get("pass")]
```

### Owner Earnings

```python
def owner_earnings(net_income: float, d_and_a: float, maintenance_capex: float) -> dict:
    """Owner Earnings = Net Income + D&A - Maintenance Capex (Buffett's preferred earnings metric)."""
    oe = net_income + d_and_a - maintenance_capex
    return {
        "owner_earnings": round(oe, 2),
        "net_income": round(net_income, 2),
        "d_and_a": round(d_and_a, 2),
        "maintenance_capex": round(maintenance_capex, 2),
        "oe_net_income_ratio": round(oe / net_income, 2) if net_income else 0
    }

# Example: $1B net income, $200M D&A, $150M maintenance capex
# result = owner_earnings(1_000_000_000, 200_000_000, 150_000_000)
# Returns ~$1.05B — the cash available to owners without impairing operations
```

## Common Pitfalls

- **Overly optimistic growth rates** — Most DCF errors come from projecting recent past indefinitely. Use conservative growth (3-5% for mature businesses) and cross-check with ROIC × reinvestment rate.
- **Ignoring the balance sheet** — A cheap stock can destroy wealth through leverage. Verify free cash flow covers interest (coverage > 5x) and net debt / EBITDA < 3x.
- **Confusing price decline with value** — A stock down 60% is not automatically a value opportunity. Distinguish temporary earnings dip (good) from structural decline or asset impairment (bad).
- **Margin of safety miscalculation** — The safety margin must account for what you could be wrong about, not a mechanical discount to your DCF. Always model the downside scenario explicitly.
- **Value trap in cyclicals** — Cyclicals look cheapest at the earnings peak and most expensive at the trough. Normalize earnings over a full business cycle before applying multiples.
- **Confirmation bias** — Once invested, you filter for supporting news and dismiss contrary evidence. Maintain a written thesis with specific falsifiable assumptions and revisit coldly each quarter.

## Monetization

- **Paid value investing newsletter** — Publish weekly deep-dives on one stock with DCF analysis, moat assessment, and clear buy/hold/sell calls. $15-30/month or $150-300/year on Substack or Beehiiv. Free tier shows methodology; full research behind the paywall.
- **Research service for family offices** — Offer bespoke deep-dive reports ($500-5,000 per report) on specific companies or sectors. Family offices and small fund managers lack dedicated analysts and pay for independently produced analysis.
- **Screening tool subscription** — Build a Python-based screener that runs weekly against global equities and emails ranked undervalued candidates with key metrics. $20-50/month. Market to individual investors who lack the technical skills to build their own.
- **Educational cohort course** — Teach a 6-week live cohort on value investing: financial statement analysis, DCF modeling, moat assessment, and portfolio construction. $500-1,000 per student. Run 2-3 cohorts per year.
- **Paid community / Discord** — Create a community (via Skool, Circle, or Discord) for value investors to share ideas, thesis templates, and portfolio reviews. $20-50/month. Cap at 500 members for quality. Quarterly live Q&A sessions.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "This stock is down 50%, it must be a bargain." | Price decline alone does not create value. Distinguish a temporary dip from structural moat erosion or asset impairment. |
| "The DCF shows 3x upside." | DCFs amplify input bias. A 1% WACC change can swing fair value 20%+. Stress-test with pessimistic assumptions before concluding. |
| "I will wait for a better price." | The best businesses rarely trade at deep discounts. Fair price for a great business beats great price for a fair business. |
| "It is different this time." | It is never different. The same greed-fear cycles repeat every decade. Study history — the specifics change, the pattern does not. |
| "I need to buy now or miss the rally." | There is always another opportunity. Cash is a legitimate position. Impatience destroys more value-investing returns than bad analysis. |
| "Management will fix this." | Hope is not an investment thesis. Demand specific, measurable turnaround milestones with credible capital allocation behind them. |

## Process

1. **Idea generation** — Screen for candidates using quantitative filters (P/E < 15, P/B < 1.5, FCF yield > 5%). Source from 13F filings of respected value investors, corporate spin-offs, and out-of-favor sectors with identifiable catalysts.
2. **Deep research** — Read 10-Ks (MD&A and footnotes), annual shareholder letters, conference call transcripts. Build a 3-statement financial model. Analyze competitive position using Porter's Five Forces and moat source identification.
3. **Valuation** — Run DCF with deliberately conservative growth assumptions. Compute downside scenario value. Compare against public comps and precedent transactions. Set target buy price with minimum 30-50% margin of safety depending on business quality.
4. **Decision and sizing** — Write a one-page investment thesis with key assumptions, upside/downside ratio, and planned exit triggers. Size: 5-15% for high-conviction compounders, 2-5% for cyclical or special-situation value, never exceed 20% in a single name.
5. **Post-entry monitoring** — Track thesis-critical assumptions quarterly against new filings. Update fair value as information arrives. Exit when price reaches intrinsic value, the thesis breaks (moat erodes, fraud, leverage blow-up), or a superior risk-reward opportunity appears.

## Verification

- [ ] Intrinsic value estimated using at least two independent methods (DCF + comps)
- [ ] Margin of safety exceeds 30% at target buy price
- [ ] Competitive moat identified and classified by source (no moat = lower conviction)
- [ ] Financial health confirmed: positive FCF, interest coverage > 5x, net debt / EBITDA < 3x
- [ ] Worst-case scenario modeled — the position remains survivable
- [ ] Thesis-critical assumptions documented with specific falsifiable triggers
- [ ] Position sizing respects portfolio concentration limits (max 15-20% per name)
- [ ] Exit criteria written before entry: price target, thesis break, and catalyst expiration