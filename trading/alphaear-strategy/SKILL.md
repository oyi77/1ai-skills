---
name: alphaear-strategy
description: Score trading setups using AlphaEar multi-factor analysis (momentum, volume, sentiment). Use when evaluating
  entry/exit signals.
domain: trading
tags:
- algorithms
- alphaear
- markets
- money
- strategy
- trading
version: 2.0.0
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


## When NOT to Use

- When you cannot afford to lose the capital at risk
- For instruments you do not understand
- When emotional state impairs judgment (revenge trading, FOMO)


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

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I will cut losses later" | Later never comes. Set stop-losses before entering any trade. |
| "This time is different" | It never is. Follow your strategy, not your emotions. |
| "I do not need to journal" | Journaling reveals patterns in your behavior. Track every trade. |

## Money-Making Overview

Turn multi-factor signal scoring into consistent trading edge. Each signal_score > 75 setup targets **3:1 reward-to-risk**, with 1% capital at risk per trade ($50 on $5K account, $100 on $10K). The alphaear framework combines momentum, volume divergence, and sentiment (news + options flow) into a composite score — when all three align above threshold, the edge is statistically significant for swing and event-driven trades.

## Revenue Streams

**1. Signal-Based Swing Trading ($300–$3,000/month)**
- Score momentum/volume/sentiment signals daily on a 10-ticker watchlist
- Enter only when composite score > 75 with bullish alignment across all three factors
- Position size: 1% account risk per trade, 5% stop-loss, 15% profit target (3:1 R:R)
- 20–30 trades/month at 55–65% win rate generates consistent P&L

**2. Options Flow & Earnings Trading ($500–$5,000/month)**
- Monitor unusual options activity (block trades, sweep orders, put/call ratio divergence)
- Pre-earnings catalyst setups with 7-day horizon; structure as call/put spreads
- Combine options flow signal with momentum score for higher probability entries
- Scale size for defined-risk spreads (max loss capped at 1% account value)

**3. Signal Subscription / API ($10–$100K/month at scale)**
- Package composite alphaear scores as a daily email / webhook / REST API
- Tiered pricing: $50/month retail, $500/month pro (full ticker coverage), $5K/month institutional (API access + raw data feeds)
- Target 200–2,000 subscribers via quant Twitter/X, trading communities, and affiliate partnerships
- Recurring SaaS revenue with zero marginal cost per additional subscriber

**Money Management (Hard Rules)**

| Rule | Value | Rationale |
|---|---|---|
| Risk per trade | 1% of account | Survive 20 consecutive losses at ~66% drawdown |
| Stop-loss | 5% below entry | Matches ATR-based volatility bands on daily timeframe |
| Profit target | 15% above entry | 3:1 R:R — one winner covers three losers |
| Max daily loss | 3% of account | Hard stop: close all positions, step away |
| Max concurrent positions | 4 | Non-correlated tickers only (no sector clustering) |
| Portfolio at risk cap | 4% | 4 positions × 1% each = max portfolio exposure |

## First Action in 60 Minutes

Run this script to score live signals for any ticker. It computes momentum (ROC + RSI), volume (ratio vs 20-day average), and sentiment (price vs moving average cross) from yfinance data, then prints a composite score with entry, stop, and target levels.

```bash
pip install yfinance pandas numpy 2>/dev/null
```

```python
#!/usr/bin/env python3
"""alphaear_first_trade.py — Score a ticker and get entry/exit levels."""
import sys, yfinance as yf, pandas as pd, numpy as np

def alphaear_score(ticker: str):
    df = yf.download(ticker, period="3mo", interval="1d", progress=False)
    if df.empty or len(df) < 22:
        return {"error": f"Insufficient data for {ticker}"}
    c = df["Close"] if "Close" in df.columns else df["Adj Close"]
    v = df["Volume"]
    price = float(c.iloc[-1])
    # Momentum: 14-day ROC + RSI approximation
    roc = (float(c.iloc[-1]) / float(c.iloc[-14]) - 1) * 100
    delta = c.diff()
    gain = delta.where(delta > 0, 0.0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0.0)).rolling(14).mean()
    rs = gain / loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    rsi_val = float(rsi.iloc[-1])
    # Volume: current vs 20-day average
    vol_ratio = float(v.iloc[-1]) / float(v.iloc[-20:].mean())
    # Sentiment: price vs 50-day SMA (trend alignment)
    sma50 = float(c.rolling(50).mean().iloc[-1])
    trend_bull = price > sma50
    # Composite score: weighted multi-factor
    mom_score = min(max((roc + 5) * 10, 0), 100) * 0.35
    vol_score = min(max((vol_ratio - 0.5) * 40, 0), 100) * 0.25
    sent_score = (rsi_val if trend_bull else 100 - rsi_val) * 0.40
    composite = round(mom_score + vol_score + sent_score, 1)
    entry = round(price, 2)
    if composite > 75:
        direction = "LONG"
        stop = round(entry * 0.95, 2)
        target = round(entry * 1.15, 2)
    elif composite < 25:
        direction = "SHORT"
        stop = round(entry * 1.05, 2)
        target = round(entry * 0.85, 2)
    else:
        direction = "NEUTRAL"
        stop = target = None
    return dict(ticker=ticker, price=entry, composite_score=composite,
                direction=direction, stop_loss=stop, profit_target=target,
                momentum_roc=round(roc, 2), rsi_14=round(rsi_val, 1),
                vol_ratio=round(vol_ratio, 2), above_sma50=trend_bull)

if __name__ == "__main__":
    ticker = sys.argv[1] if len(sys.argv) > 1 else "SPY"
    r = alphaear_score(ticker)
    if "error" in r:
        print(f"ERROR: {r['error']}")
        sys.exit(1)
    print(f"=== AlphaEar Signal: {ticker} ===")
    print(f"Price:          ${r['price']}")
    print(f"Composite Score: {r['composite_score']}/100 — {r['direction']}")
    print(f"Momentum ROC:    {r['momentum_roc']}%")
    print(f"RSI(14):        {r['rsi_14']}")
    print(f"Vol Ratio:      {r['vol_ratio']}x (vs 20d avg)")
    print(f"Above SMA(50):  {r['above_sma50']}")
    if r['stop_loss']:
        print(f"Entry → Stop:    ${r['price']} → ${r['stop_loss']} ({(r['stop_loss']/r['price']-1)*100:+.1f}%)")
        print(f"Entry → Target:  ${r['price']} → ${r['profit_target']} ({(r['profit_target']/r['price']-1)*100:+.1f}%)")
        risk = round(abs(r['price'] - r['stop_loss']), 2)
        print(f"Risk per share:  ${risk}")
        print(f"Risk per 100sh:  ${risk*100:.0f}")
        print(f"1% acct → shares: {int(10000 * 0.01 / risk)} (on $10K)")
```

**Usage:**
```bash
python3 alphaear_first_trade.py NVDA
python3 alphaear_first_trade.py AAPL
```

## Output Format

Every alphaear signal call produces a structured result:

```json
{
  "ticker": "NVDA",
  "price": 124.56,
  "composite_score": 82.3,
  "direction": "LONG",
  "stop_loss": 118.33,
  "profit_target": 143.24,
  "momentum_roc": 8.4,
  "rsi_14": 62.5,
  "vol_ratio": 1.85,
  "above_sma50": true
}
```

| Field | Description | Threshold |
|---|---|---|
| composite_score | Weighted multi-factor signal (0–100) | > 75 = actionable LONG, < 25 = SHORT |
| momentum_roc | 14-day rate of change % | > 3% confirms trend strength |
| rsi_14 | Relative Strength Index (14) | 30–70 range; > 70 overbought, < 30 oversold |
| vol_ratio | Today's volume / 20-day average | > 1.5 confirms participation |
| above_sma50 | Price above 50-day MA | Bullish when True, bearish when False |
| stop_loss | 5% below/above entry | Hard exit — no exceptions |
| profit_target | 15% above/below entry | Take full or 50% here, trail remainder |

For API / subscription output, wrap the same fields in an envelope with `timestamp`, `signal_id`, and `confidence`.

## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run alphaear strategy workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings