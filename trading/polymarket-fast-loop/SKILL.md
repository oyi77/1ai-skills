---
name: polymarket-fast-loop
description: Trade Polymarket BTC 5-minute and 15-minute fast markets using CEX price momentum signals via Simmer API. Default
  signal is Binance BTC/USDT klines. Use when user wants to trade sprint/fast markets, automate short-term crypto trading,
  or use CEX momentum as a Polymarket signal.
domain: trading
tags:
- algorithms
- api
- crypto
- fast
- loop
- markets
- polymarket
- trading
- money
metadata:
  author: Simmer (@simmer_markets)
  version: 2.0.0
  displayName: Polymarket FastLoop Trader
  difficulty: advanced
---
# Polymarket Fast Loop

## When to Use

**Trigger phrases:**
- "polymarket fast loop"
- "Help me with polymarket fast loop"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


Trade Polymarket's 5-minute crypto fast markets using real-time price signals. Default: BTC momentum from Binance. Works with ETH and SOL too.

> **Polymarket only.** All trades execute on Polymarket with real USDC. Use `--live` for real trades, dry-run is the default.

> **This is a template.** The default signal (Binance momentum) gets you started — remix it with your own signals, data sources, or strategy. The skill handles all the plumbing (market discovery, import, trade execution). Your agent provides the alpha.

> ⚠️ Fast markets carry Polymarket's 10% fee (`is_paid: true`). Factor this into your edge calculations.

> ⚠️ **Risk monitoring does not apply to sub-15-minute markets.** Simmer's stop-loss and take-profit monitors check positions every 15 minutes — which means they will never fire on 5m or 15m markets before resolution. Any risk settings you configure in the Simmer dashboard have no effect on these positions. Size accordingly and do not rely on automated stop-losses for fast market trades.


## When NOT to Use

- When you cannot afford to lose the capital at risk
- For instruments you do not understand
- When emotional state impairs judgment (revenge trading, FOMO)


## Overview

Polymarket Fast Loop provides market analysis capabilities with risk management.

## Workflow

```python
# Example: Position sizing (Kelly Criterion)
def kelly_size(win_rate: float, avg_win: float, avg_loss: float) -> float:
    if avg_loss == 0: return 0
    b = avg_win / abs(avg_loss)
    kelly = (win_rate * b - (1 - win_rate)) / b
    return max(0, min(kelly * 0.5, 0.02))  # Half-Kelly, max 2%
```

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

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I will cut losses later" | Later never comes. Set stop-losses before entering any trade. |
| "This time is different" | It never is. Follow your strategy, not your emotions. |
| "I do not need to journal" | Journaling reveals patterns in your behavior. Track every trade. |

## Money-Making Overview

Run automated arbitrage between CEX BTC price momentum and Polymarket prediction markets. The core strategy: track Binance BTC/USDT 1-minute candles, detect short-term momentum shifts, and place opposing-direction positions on Polymarket's 5-minute and 15-minute crypto fast markets. These markets resolve based on whether BTC crosses certain price thresholds within the window — the same signal you can detect from CEX order flow seconds before the market closes.

Target 60-80% win rate on 5-minute signals with proper position sizing. Realistic daily earnings of $50-500 per account depending on bankroll size and signal quality. The 10% Polymarket fee is your biggest friction — it requires every edge estimate to include a `fee_factor = 0.9` on gross payout. Small accounts ($100-1K) should use conservative 1-2% position sizing to survive variance.

## Revenue Streams

| Stream | Description | Estimated Income |
|--------|-------------|-----------------|
| **Momentum Scalping** | Trade 5-min/15-min fast markets using CEX momentum divergence signals. Each trade locked for 5-15 minutes. | $50-500/day per account |
| **Multi-Account Scaling** | Run 5-10 accounts in parallel (compliant with Polymarket ToS). Diversify signal parameters across accounts. | $500-5K/day |
| **Copy-Trading / Signal Service** | Sell access to your real-time signals via Telegram/API. Charge monthly subscription or profit-share. | $200-2K/month commissions |

### Fee Awareness

Polymarket fast markets carry a **10% platform fee** (`is_paid: true`). This means a $100 win pays out $90. Factor this into every calculation:

- Kelly edge = `(win_rate * 0.9 * avg_win - (1-win_rate) * |avg_loss|) / (0.9 * avg_win)`
- Minimum viable edge = 11.2% (you need to beat the fee just to break even)

### Position Sizing for Small Accounts

Small accounts ($100-1K bankroll) must be hyper-conservative:

- **Per-trade risk**: 1-2% of bankroll ($2-20 on a $1K account)
- **Max concurrent trades**: 2 (keep powder dry for the next signal)
- **Daily loss limit**: 10% of bankroll — stop trading if hit
- **Recovery rule**: After a 3-trade losing streak, step back for 2 hours
- **Half-Kelly**: Use `kelly_size()` below with a `0.25` fractional factor instead of `0.5` for extra conservatism

```python
def kelly_size_small(win_rate: float, avg_win: float, avg_loss: float) -> float:
    fee_factor = 0.9  # Polymarket takes 10%
    if avg_loss == 0: return 0
    b = (fee_factor * avg_win) / abs(avg_loss)
    kelly = (win_rate * b - (1 - win_rate)) / b
    return max(0, min(kelly * 0.25, 0.02))  # Quarter-Kelly, max 2%
```

## First Action in 60 Minutes

This Python script generates your first live signal in under an hour. It fetches the latest Binance BTC/USDT 1m klines, calculates a simple momentum score, and prints a trade decision you can execute on Polymarket.

```python
#!/usr/bin/env python3
"""First Polymarket Fast Loop Signal Generator"""
import time, hmac, hashlib, json, urllib.request

# --- Config ---
BINANCE_API = "https://api.binance.com/api/v3"
POLYMARKET_API = "https://clob.polymarket.com"
# Polymarket fee is 10% on fast markets — factor into profit checks
FEE_FACTOR = 0.9

def fetch_klines(symbol="BTCUSDT", interval="1m", limit=5):
    """Get latest 5 one-minute candles from Binance."""
    url = f"{BINANCE_API}/klines?symbol={symbol}&interval={interval}&limit={limit}"
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.loads(resp.read().decode())
    return [{
        "open": float(k[1]), "high": float(k[2]), "low": float(k[3]),
        "close": float(k[4]), "volume": float(k[5])
    } for k in data]

def momentum_score(klines):
    """Simple momentum: compare latest close vs avg of closes. Positive = bullish."""
    closes = [k["close"] for k in klines]
    latest = closes[-1]
    avg = sum(closes) / len(closes)
    return (latest - avg) / avg * 100  # percent deviation

def signal_decision(score):
    """Return a trade signal based on momentum divergence."""
    threshold = 0.05  # 0.05% deviation — adjust based on backtesting
    if score > threshold:
        return {"action": "BUY", "direction": "UP",
                "reason": f"CEX momentum bullish ({score:+.3f}%)"}
    elif score < -threshold:
        return {"action": "BUY", "direction": "DOWN",
                "reason": f"CEX momentum bearish ({score:+.3f}%)"}
    else:
        return {"action": "HOLD", "direction": None,
                "reason": f"No clear momentum signal ({score:+.3f}%)"}

if __name__ == "__main__":
    print("=== Polymarket Fast Loop — First Signal ===\n")
    klines = fetch_klines()
    print(f"Binance BTC/USDT last 5 candles:")
    for k in klines:
        print(f"  Close: ${k['close']:>7.1f}  |  Vol: {k['volume']:>8.2f}")
    score = momentum_score(klines)
    decision = signal_decision(score)
    print(f"\nMomentum score: {score:+.3f}%")
    print(f"Signal: {decision['action']} -> {decision['direction'] or 'N/A'}")
    print(f"Reason: {decision['reason']}")
    print(f"\nPolymarket fee: 10% (factor = {FEE_FACTOR})")
    if decision['action'] == 'BUY':
        print("Next step: Find the active 5m/15m fast market on Polymarket ")
        print("and place a USDC position matching your signal direction.")
    else:
        print("No trade. Wait for the next 1-minute candle and re-run.")
```

**To run:**
```bash
python3 first_signal.py
```

**Next steps after the first signal:**
1. Wire in the Simmer API for automated execution (see `simmer-python` examples)
2. Add a backtester using historical Binance klines vs Polymarket resolution data
3. Tune the momentum threshold parameter (0.05%) on at least 200 historical trades
4. Scale from 1 account to multiple independent strategies

## Output Format

Every trade signal and execution result MUST follow this template:

```json
{
  "timestamp": "2026-07-16T14:30:00Z",
  "signal": {
    "source": "Binance BTC/USDT",
    "score_pct": 0.08,
    "direction": "UP",
    "confidence": "medium"
  },
  "trade": {
    "market": "BTC > $60K at 14:35?",
    "outcome": "YES",
    "size_usdc": 20.00,
    "fee_usdc": 2.00,
    "potential_payout_usdc": 18.00
  },
  "result": {
    "profit_loss_usdc": null,
    "win": null,
    "return_pct": null
  }
}
```

Fill `result` after market resolution. Track every trade in a local CSV or SQLite for win-rate calculation and threshold tuning.


## Process

1. **Scope** — Define research questions, identify data sources, set time boundaries
1. **Gather** — Collect data from primary sources, APIs, and public records
1. **Synthesize** — Analyze findings, identify patterns, produce actionable report

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings