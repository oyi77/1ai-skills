---
name: polymarket-weather-trader
description: Trade Polymarket weather markets using NOAA forecasts via Simmer API. Inspired by gopfan2's $2M+ strategy. Use
  when user wants to trade temperature markets, automate weather bets, check NOAA forecasts, or run gopfan2-style trading.
domain: trading
tags:
- algorithms
- api
- markets
- polymarket
- trader
- trading
- weather
metadata:
  author: Simmer (@simmer_markets)
  version: 1.14.0
  displayName: Polymarket Weather Trader
  difficulty: beginner
  attribution: Strategy inspired by gopfan2
---
# Polymarket Weather Trader

## When to Use

**Trigger phrases:**
- "polymarket weather trader"
- "Help me with polymarket weather trader"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


Trade temperature markets on Polymarket using NOAA forecast data.

> **This is a template.** The default signal is NOAA temperature forecasts — remix it with other weather APIs, different forecast models, or additional market types (precipitation, wind, etc.). The skill handles all the plumbing (market discovery, NOAA parsing, trade execution, safeguards). Your agent provides the alpha.

## Overview

Polymarket Weather Trader provides market analysis capabilities with risk management.

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

