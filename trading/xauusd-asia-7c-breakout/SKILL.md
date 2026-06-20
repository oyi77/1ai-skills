---
name: xauusd-asia-7c-breakout
description: XAUUSD Asia 7-Candle Breakout strategy with backtest, paper trade, and real trade modes. Use when trading gold
  on the Asia session breakout strategy, running historical backtests, setting up paper trading simulations, or executing
  live trades with the 7-candle breakout system.
domain: trading
tags:
- algorithms
- asia
- breakout
- markets
- trading
- xauusd
allowed-tools:
- Bash(trading:*)
- fs
- network
---

# XAUUSD Asia 7-Candle Breakout Strategy

## Overview

Breakout strategy using 7-candle window (3 before + COA + 3 after) for XAUUSD during Asia Session. This strategy identifies key breakout levels by analyzing the high-low range of a specific 7-candle window around the Asia session open candle, then places pending orders with proper risk-reward parameters (1R stop loss, 2R take profit). The strategy includes robust backtesting, paper trading, and live execution capabilities with appropriate guardrails.

## When to Use

- Trading XAUUSD (Gold) during Asia session hours (07:00 Jakarta time = 00:00 UTC)
- Running historical backtests to validate strategy performance
- Setting up paper trading to test signals before live execution
- Executing real trades with proper slippage checks and risk management
- Analyzing breakout behavior around session opens
- Deploying autonomous trading with clear entry/exit rules

## The Process

The execution pipeline covers setup configuration, signal generation, historical backtesting, paper trading, and live execution with guardrails.


### 1. Setup Configuration

Configure strategy parameters for your trading environment:

```bash
# Set Asia session start time (Jakarta time)
export ASIA_SESSION_START="00:00:00"

# Configure strategy parameters
export LOOKBACK_CANDLES=7
export R_MULTIPLE=1.0
export MAX_SPREAD_POINTS=30
```

### 2. Signal Generation

Get today's trading signal:

```bash
python xauusd_asia_7c_breakout.py signal
```

This command:
- Identifies the Current Open Asia (COA) candle
- Calculates the 7-candle window (COA-3 to COA+3)
- Finds Highest High (HH) and Lowest Low (LL) from the window
- Calculates R (range of last candle in window)
- Places Buy Stop at HH and Sell Stop at LL with SL=1R, TP=2R

### 3. Historical Backtest

Run comprehensive historical backtest:

```bash
python xauusd_asia_7c_breakout.py backtest 2024-01-01 2024-12-31
```

Backtest outputs:
- Total trades count
- Win rate percentage
- Total PnL in points
- Average win/loss per trade
- Risk/reward ratio

### 4. Paper Trading (Simulation)

Start paper trading for signal validation:

```bash
python xauusd_asia_7c_breakout.py paper start
```

Paper trading runs with real-time market data but no actual positions.

### 5. Live Trading (With Guardrails)

Arm live trading only after guardrail checks:

```bash
python xauusd_asia_7c_breakout.py real arm
```

Guardrails include:
- Spread validation (max 30 points configurable)
- Trade frequency limits (one trade per day)
- Session time validation
- Account balance checks

## When NOT to Use

- Task is about portfolio management, not trading (use portfolio skills)
- Task is about financial analysis (use analysis skills)
- You need to analyze trade results (use analytics skills)
- Task is about risk management (use risk skills)
- You don't have trading capital
- Task requires financial advice (consult advisors)


## Red Flags

- **No signal generated**: Check that Asia session start time is correct for your broker timezone; verify data quality for the target date
- **Excessive slippage detected**: Broker is offering poor execution; abort trade and wait for better conditions
- **Strategy creates contradictory orders**: Review COA candle identification logic; ensure session times are properly aligned with broker timezone
- **Backtest shows zero trades**: Verify data coverage for the date range and check for gaps in historical data
- **Live trade executes with wrong SL/TP**: Verify R calculation uses correct candle range and prices are in proper price units
- **Orders not cancelled at session end**: Check session end time configuration; implement proper order cleanup logic

## Verification

Verification covers signal accuracy, backtest validity, live execution guardrails, and risk parameter compliance.


### Signal Verification
- [ ] COA candle correctly identified at Asia session open time
- [ ] 7-candle window (COA-3 to COA+3) calculated correctly
- [ ] HH/LL boundaries match expected breakouts from chart
- [ ] R calculation uses COA+3 candle range (High - Low)
- [ ] Buy Stop order placed exactly at HH, Sell Stop at LL

### Backtest Verification
- [ ] Total trades count matches expected frequency (typically 1 per day)
- [ ] Win rate is statistically significant (>50% for 100+ trades)
- [ ] Risk/reward ratio matches configured 2:1 (TP/R = 2, SL/R = 1)
- [ ] Maximum drawdown is within acceptable limits (<20% of account)

### Live Execution Verification
- [ ] Slippage stays within configured threshold (<2 pips typically)
- [ ] One trade per day limit enforced correctly
- [ ] Cancel opposite order logic works (cancels opposing pending on trigger)
- [ ] Guardrails prevent trades during abnormal market conditions

### Risk Verification
- [ ] Maximum spread requirement enforced (30 points configurable)
- [ ] Position sizes calculated correctly based on risk parameters
- [ ] SL levels placed at 1R from entry (R = last candle range)
- [ ] TP levels placed at 2R from entry for 2:1 reward:risk
