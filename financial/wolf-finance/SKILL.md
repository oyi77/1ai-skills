---
name: wolf-finance
description: 'ACTIVATE for ANY finance, investment, trading, or market query. Triggers: ticker symbols ($AAPL, BTC, EUR/USD),
  asset classes (stocks, crypto, forex, bonds, commodities, derivatives, PE, hedge funds), concepts (DCF, P/E, RSI, MACD,
  Kelly, VaR, Sharpe, Greeks, yield curve, carry trade, QE), actions ("should I buy/sell", "analyze this", "build a portfolio",
  "hedge my position", "size this trade"), modeling (valuation, forecasting, backtesting, Monte Carlo), corporate finance
  (M&A, IPO, LBO, WAC...'
domain: financial
tags:
- analysis
- crypto
- finance
- investment
- testing
- trading
- wolf
---
# Wolf Finance

## When to Use

- Analyzing any financial asset (equities, crypto, forex, commodities, derivatives)
- Building investment theses with evidence-tiered backing (T1/T2/T3)
- Running pre-trade risk gates before position entry
- Portfolio construction and risk management across asset classes
- Institutional-grade reporting for investment committees


## When NOT to Use

- For personal financial advice (consult a licensed advisor)
- When the analysis requires real-time market data you do not have
- For tax or legal decisions (consult professionals)


## Overview

Wolf Finance provides finance operations with accuracy and compliance.

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

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "The market will recover" | Do not hope. Analyze. Set stop-losses and follow your strategy. |
| "I do not need to track expenses" | What you do not measure, you cannot optimize. Track everything. |
| "One spreadsheet is enough" | Financial models need version control and audit trails. Use proper tools. |

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings