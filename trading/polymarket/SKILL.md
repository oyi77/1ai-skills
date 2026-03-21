---
name: polymarket-index
description: Index and overview of all Polymarket prediction market skills. Routes to the right skill based on use case — API queries, fast BTC trading, weather markets, or full AI agent.
permissions:
  - fs
  - network
---

# Polymarket Skills Index

Overview and routing guide for all Polymarket-related skills.

## Available Skills

### 1. polymarket-api
**Location:** `skills/polymarket-api/`
**Use when:** You need to query Polymarket data — market prices, event probabilities, betting odds.
```
Query prediction market odds, prices, and event data.
```

### 2. polymarket-fast-loop
**Location:** `skills/polymarket-fast-loop/`
**Use when:** Trading BTC 5-min or 15-min sprint markets using CEX momentum signals (Binance BTC/USDT klines via Simmer API).
```
Fast loop trading — short-term crypto sprint markets.
```

### 3. polymarket-weather-trader
**Location:** `skills/polymarket-weather-trader/`
**Use when:** Trading temperature/weather markets using NOAA forecasts (gopfan2-style strategy via Simmer API).
```
Weather market trading — NOAA-powered temperature bets.
```

### 4. mia-polymarket-trader
**Location:** `skills/mia-polymarket-trader/`
**Use when:** Full AI agent for automated prediction market trading on Polymarket.
```
Autonomous AI trading agent for diverse Polymarket events.
```

## Decision Matrix

| Scenario | Skill |
|----------|-------|
| "What are the odds on X?" | polymarket-api |
| "Trade BTC sprint markets" | polymarket-fast-loop |
| "Trade weather/temperature markets" | polymarket-weather-trader |
| "Run autonomous Polymarket trading" | mia-polymarket-trader |
| "Check prediction market prices" | polymarket-api |
| "Gopfan2-style weather bets" | polymarket-weather-trader |
