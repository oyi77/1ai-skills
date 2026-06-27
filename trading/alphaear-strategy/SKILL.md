---
name: alphaear-strategy
description: Score trading setups using AlphaEar multi-factor analysis (momentum, volume, sentiment). Use when evaluating
  entry/exit signals.
domain: trading
tags:
- algorithms
- alphaear
- markets
- strategy
- trading
---
# Alphaear Strategy

## When to Use

**Trigger phrases:**
- "alphaear strategy"
- "Help me with alphaear strategy"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

analysis = alphaear_analyze("NVDA")

# Output includes:
# - News aggregation with sentiment
# - Social media trend analysis
# - Options flow anomalies
# - Kronos price prediction
# - Composite signal score

if analysis.signal_score > 75:
    position_size = portfolio_value * 0.05  # 5% max
    entry = current_price
    stop = entry * 0.95  # 5% stop
    target = entry * 1.15  # 15% target
```

### Example 2: Signal Monitoring

```python
# Monitor multiple positions
portfolio = ["AAPL", "TSLA", "NVDA", "AMD"]
signals = {}

for ticker in portfolio:
    signals[ticker] = alphaear_analyze(ticker)
    
# Alert on signal degradation
for ticker, signal in signals.items():
    if signal.evolution == "WEAKEN":
        alert(f"{ticker}: Signal weakening, review position")
    elif signal.evolution == "FALSIFY":
        alert(f"{ticker}: Thesis invalidated, consider exit")
```

### Example 3: Event-Driven Setup

```python
# Pre-earnings analysis
ticker = "AMZN"
catalyst_date = get_next_earnings_date(ticker)
days_to_catalyst = (catalyst_date - today).days

if days_to_catalyst <= 7:
    setup = alphaear_analyze(
        ticker,
        focus="catalyst_setup",
        include_options=True
    )
    
    if setup.options_signal == "unusual_call_activity":
        # Market positioning bullish
        direction = "LONG"
        structure = "call_spread"
```

---


Load `references/trading-checklist.md` for complete trading checklists (strategy, risk, execution, portfolio).

## Overview

Alphaear Strategy provides market analysis capabilities with risk management.

## Workflow

1. **Research** — Analyze market conditions and opportunities
2. **Plan** — Define entry, exit, and position sizing
3. **Execute** — Place trades with proper order types
4. **Monitor** — Track positions and market changes
5. **Manage risk** — Apply stop-losses and hedging
6. **Review** — Post-trade analysis and journaling

## Risk Management

- Never risk more than 1-2% of portfolio per trade
- Set stop-loss before entering any position
- Diversify across uncorrelated assets
- Size positions based on volatility (ATR)
- Have a maximum daily loss limit

## Key Metrics

- Win rate and profit factor
- Sharpe ratio and max drawdown
- Average risk-reward ratio
- Expectancy per trade
- Correlation to benchmark

## Discipline Rules

- Follow your trading plan — no impulsive trades
- Cut losses short, let winners run
- Review every trade in your journal
- Never revenge trade after a loss
- Take breaks after consecutive losses

