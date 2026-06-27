---
name: black-edge
description: Apply institutional trading edge using order flow analysis, market microstructure, and dark pool signals.
domain: trading
tags:
- algorithms
- black
- edge
- markets
- trading
---
# Black Edge

## When to Use

**Trigger phrases:**
- "black edge"
- "Help me with black edge"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

parking_data = fetch_satellite_imagery(ticker="WMT")
consensus_revenue = get_analyst_estimates(ticker="WMT")

parking_trend = calculate_occupancy_trend(parking_data, period="3m")
expected_beat = parking_trend > consensus_revenue * 1.05

position_size = calculate_kelly_size(
    edge_confidence=85,
    historical_accuracy=0.72,
    payoff_ratio=2.5
)
```

### Example 2: Options Flow Anomaly

```python
# Detect unusual OTM call buying
flow = fetch_unusual_options_activity(
    min_volume=500,
    otm_percentage=10
)

sweeps = filter_sweep_orders(flow)
catalyst_date = find_next_catalyst(ticker=sweeps[0].ticker)

if sweeps.volume > 3 * avg_daily and days_to_catalyst < 30:
    signal_strength = "HIGH"
    position = buy_calls(sweeps[0], strike=sweeps[0].strike)
```

### Example 3: Dark Pool Accumulation

```python
# Identify institutional accumulation
dark_pool_prints = fetch_ats_volume(ticker="AAPL")

large_blocks = dark_pool_prints[
    dark_pool_prints.volume > 100000
    and dark_pool_prints.price > vwap
]

accumulation_score = calculate_accumulation(
    large_blocks, 
    lookback="20d"
)

if accumulation_score > 75 and price_near_support:
    entry = "LONG"
    target = calculate_measured_move("cup_and_handle")
```

---


Load `references/trading-checklist.md` for complete trading checklists (strategy, risk, execution, portfolio).

## Overview

Black Edge provides market analysis capabilities with risk management.

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

