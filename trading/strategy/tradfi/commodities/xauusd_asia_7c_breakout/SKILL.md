---
name: xauusd-asia-7c-breakout
description: XAUUSD Asia 7-Candle Breakout strategy with backtest, paper trade, and real trade modes
permissions:
  - fs
  - network
---

# XAUUSD Asia 7-Candle Breakout Strategy

Breakout strategy using 7-candle window (3 before + COA + 3 after) for XAUUSD during Asia Session.

## Implementation

**Python File:** `xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py`

**Fixed SL/TP Calculation:**
- Buy Stop at HH
  - SL = HH - R (1R below entry) ✓ FIXED
  - TP = HH + 2R (2R above entry)
- Sell Stop at LL
  - SL = LL + R (1R above entry) ✓ FIXED
  - TP = LL - 2R (2R below entry)

## Strategy Rules

1. **Identify COA**: Find the H1 candle that opens at Asia session open time (07:00 Jakarta = 00:00 UTC)
2. **Form 7-Candle Window**: COA-3 to COA+3 (7 candles total)
3. **Calculate HH/LL**: Highest High and Lowest Low from the 7-candle window
4. **Calculate R**: Range of the last candle (COA+3) in points
5. **Place Pending Orders**:
   - Buy Stop at HH
   - Sell Stop at LL
6. **Set SL/TP**: SL = 1R, TP = 2R from entry

## Commands

### `signal today`
Get today's trading signal.
```bash
python xauusd_asia_7c_breakout.py signal
```

### `backtest`
Run historical backtest.
```bash
python xauusd_asia_7c_breakout.py backtest 2024-01-01 2024-12-31
```

### `paper start`
Start paper trading (WIP)

### `real arm`
Arm real trading with guardrail check (WIP)

## Backtest Results

**Period:** 2025-02-19 to 2026-02-19 (1 year)

| Metric | Value |
|--------|-------|
| Total Trades | 432 |
| Win Rate | 60.0% |
| Total PnL | +5869.90 points |
| Avg Win | 30.42 points |
| Avg Loss | -11.61 points |
| Risk/Reward | ~2.6:1 |

## Risk Management

- **Max Spread**: 30 points (configurable)
- **One Trade Per Day**: Enabled by default
- **Cancel Opposite**: When one pending triggers, cancel the other
- **Cancel at Session End**: Cancel all pending if not triggered

## Dependencies

```bash
pip install yfinance pandas numpy
```

## Files

```
xauusd_asia_7c_breakout/
├── SKILL.md                    # This file
├── xauusd_asia_7c_breakout.py  # Main implementation
└── README.md                   # Usage guide
```
