---
name: crypto-trading-bot
description: 加密貨幣交易機器人開發 - 幫你整自動交易Bot，支持Pine Script、Python、CCXT API對接。適用於：(1)整TradingView信號Bot (2)CEX/DEX API自動化 (3)套利機器人
  (4)止盈止損策略. Use when working with crypto trading bot.
domain: trading
tags:
- algorithms
- api
- bot
- crypto
- markets
- trading
---
# Crypto Trading Bot

## When to Use

**Trigger phrases:**
- "crypto trading bot"
- "Help me with crypto trading bot"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


幫你整加密貨幣自動交易機器人


## When NOT to Use

- When you cannot afford to lose the capital at risk
- For instruments you do not understand
- When emotional state impairs judgment (revenge trading, FOMO)


## Overview

Crypto Trading Bot provides market analysis capabilities with risk management.

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


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run crypto trading bot workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings