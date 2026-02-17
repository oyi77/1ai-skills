---
name: xauusd-asia-7c-breakout
description: XAUUSD Asia 7-Candle Breakout strategy with backtest, paper trade, and real trade modes
permissions:
  - fs
  - network
---

# XAUUSD Asia 7-Candle Breakout Strategy

Breakout strategy using 7-candle window (3 before + COA + 3 after) for XAUUSD during Asia Session.

## Strategy Rules

1. **Identify COA**: Find the H1 candle that opens at Asia session open time (default: 07:00)
2. **Form 7-Candle Window**: COA-3 to COA+3 (7 candles total)
3. **Calculate HH/LL**: Highest High and Lowest Low from the 7-candle window
4. **Calculate R**: Range of the last candle (COA+3) in points
5. **Place Pending Orders**:
   - Buy Stop at HH
   - Sell Stop at LL
6. **Set SL/TP**: SL = 1R, TP = 2R from entry

## Configuration

### Session Settings
- `timezone`: "Asia/Jakarta" (default)
- `session_start`: "07:00" (default)
- `session_end`: "15:00" (default)
- `open_asia_candle_time`: "07:00" (default)

### Strategy Settings
- `timeframe`: "H1" (required)
- `lookback_before`: 3 (default)
- `lookforward_after`: 3 (default)
- `min_range_pips`: 5 (default)
- `entry_buffer_points`: 0 (default)
- `rr_ratio`: 2.0 (default)

### Risk Settings
- `risk_mode`: "fixed_risk_percent" or "fixed_lot"
- `fixed_lot`: 0.01 (default)
- `risk_percent`: 1.0 (default)

## Commands

### `setup`
Configure the strategy.

**Usage**: `setup symbol=XAUUSD broker=mt5 risk_percent=1.0 rr_ratio=2.0`

### `signal today`
Get today's trading signal.

**Usage**: `signal today`

### `backtest`
Run historical backtest.

**Usage**: `backtest start=2024-01-01 end=2024-12-31`

### `paper start`
Start paper trading.

**Usage**: `paper start`

### `paper status`
Check paper trading status.

**Usage**: `paper status`

### `paper stop`
Stop paper trading.

**Usage**: `paper stop`

### `real arm`
Arm real trading (with guardrail check).

**Usage**: `real arm`

### `real status`
Check real trading status.

**Usage**: `real status`

### `real disarm`
Disarm real trading.

**Usage**: `real disarm`

### `export trades`
Export trade history.

**Usage**: `export trades format=csv`

## Example Output

```
Date: 2024-01-15 (Asia/Jakarta)
COA time: 07:00
Window: COA-3 .. COA+3

HH: 2034.50
LL: 2027.10
R (last candle): 120 points

Buy Stop: 2034.50
  SL: 2033.30
  TP: 2036.90

Sell Stop: 2027.10
  SL: 2028.30
  TP: 2024.70

Filters: range OK, spread OK
Status: pending placed
```

## Risk Management

- **Max Spread**: 30 points (configurable)
- **One Trade Per Day**: Enabled by default
- **Cancel Opposite**: When one pending triggers, cancel the other
- **Cancel at Session End**: Cancel all pending if not triggered

## Dependencies

- MetaTrader5: `pip install MetaTrader5`
- For crypto: CCXT: `pip install ccxt`
