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
metadata:
  author: Simmer (@simmer_markets)
  version: 1.3.5
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

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings