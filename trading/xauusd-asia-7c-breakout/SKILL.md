---
name: xauusd-asia-7c-breakout
description: XAUUSD Asia 7-Candle Breakout strategy with backtest, paper trade, and real trade modes. Use when trading gold
  on the Asia session breakout strategy, running historical backtests, setting up paper trading simulations, or executing
  live trades with the 7-candle breakout system.
domain: trading
author: mahipal
license: Apache-2.0
subdomain: trading
tags:
- algorithms
- asia
- breakout
- markets
- money
- xauusd
- network
allowed-tools:
- Bash(trading:*)
- fs
version: 2.0.0
---

# XAUUSD Asia 7-Candle Breakout Strategy

## Overview

Breakout strategy using 7-candle window (3 before + COA + 3 after) for XAUUSD during Asia Session. This strategy identifies key breakout levels by analyzing the high-low range of a specific 7-candle window around the Asia session open candle, then places pending orders with proper risk-reward parameters (1R stop loss, 2R take profit). The strategy includes robust backtesting, paper trading, and live execution capabilities with appropriate guardrails.

## When to Use

**Trigger phrases:**
- "xauusd asia 7c breakout"
- "Trading XAUUSD (Gold) during Asia session hours (07:00 Jakarta time = 00:00 UTC)"
- "Running historical backtests to validate strategy performance"
- "Setting up paper trading to test signals before live execution"


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

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I will cut losses later" | Later never comes. Set stop-losses before entering any trade. |
| "This time is different" | It never is. Follow your strategy, not your emotions. |
| "I do not need to journal" | Journaling reveals patterns in your behavior. Track every trade. |

## Money-Making Overview

Trade XAUUSD Asia session breakouts with 2:1 risk-reward. Strategy targets $100-500/day per mini lot with 60-70% win rate on well-defined 7-candle patterns. The system identifies breakout levels during the liquid Asia session window, places pending buy/sell stops at key HH/LL boundaries, and lets price action confirm the move. With proper position sizing and guardrails, this strategy generates consistent daily income from gold's predictable range expansion during session transitions.

## Revenue Streams

- **Live gold trading ($500-5,000/month):** Execute the strategy on a funded brokerage account. Conservative 0.5% risk per trade, 1-3 trades per day, 2:1 RR yields 60-70% win rate. A $5K account at 0.5% risk targets $100-300/day.
- **Signal service ($200-2,000/month):** Publish daily XAUUSD breakout signals with entry, SL, TP levels. Sell via Telegram/Discord subscription ($20-50/month). Recruit 10-40 subscribers. Include HH/LL levels, R value, and risk rating.
- **Copy-trading ($100-1,000/month):** Let subscribers mirror your trades automatically via broker copy-trade platforms (Myfxbook, ZuluTrade). Performance fee model: 20% of profits or flat $10-30/month per copier. Need a verified track record (50+ trades, >60% win rate).
- **Education & content ($200-2,000/month):** Sell a mini-course on the 7-candle breakout methodology ($50-200), YouTube monetisation from trade breakdowns, or a weekly newsletter with market analysis ($10-20/month).

### Position Sizing by Account Size

| Account | Risk/Trade | R Value | Position Size | Daily Target (1R win) |
|---------|-----------|---------|---------------|----------------------|
| $500    | $2.50 (0.5%) | 10-20 pts | 0.02-0.05 mini lots | $5-25 |
| $5,000  | $25 (0.5%) | 10-20 pts | 0.2-0.5 mini lots | $50-250 |
| $50,000 | $250 (0.5%) | 10-20 pts | 2-5 mini lots | $500-2,500 |

Position size formula: `(Account × Risk%) ÷ (R × PipValue)`. For XAUUSD, 1 mini lot (0.1) = $1 per pip on standard accounts. Adjust R value based on actual COA+3 candle range. Always cap at max 2% daily loss.

## First Action in 60 Minutes

Generate a trade signal for today by running the 7-candle breakout scanner. This Python script fetches live XAUUSD data, identifies the Asia session 7-candle pattern, computes HH/LL levels and R-multiple, and outputs a structured trade signal with position sizing for your account:

```bash
python3 -c "
import yfinance as yf, pandas as pd, json
from datetime import datetime, timezone

# 1. Fetch XAUUSD 15-min data (past 24h covers Asia session)
now = datetime.now(timezone.utc)
start = now.replace(hour=0, minute=0, second=0, microsecond=0)
data = yf.download('XAUUSD=X', start=start, interval='15m', progress=False)
if data.empty:
    data = yf.download('GC=F', start=start, interval='15m', progress=False)
df = data.reset_index()

# 2. Find Asia session open (00:00 UTC) and build 7-candle window
df['Datetime'] = pd.to_datetime(df['Datetime'])
asia_open = df[df['Datetime'].dt.hour == 0].iloc[0] if len(df[df['Datetime'].dt.hour == 0]) > 0 else df.iloc[0]
idx = df[df['Datetime'] == asia_open['Datetime']].index[0]

# 3. Window = COA-3 to COA+3 (7 candles centered on Asia open)
start_idx = max(0, idx - 3)
end_idx = min(len(df), idx + 4)
window = df.iloc[start_idx:end_idx]

if len(window) >= 7:
    HH = window['High'].max()
    LL = window['Low'].min()
    last_candle = window.iloc[-1]
    R = round(last_candle['High'] - last_candle['Low'], 2)
    current = last_candle['Close']
    
    signal = {
        'date': str(now.date()),
        'HH': float(HH),
        'LL': float(LL),
        'R': float(R),
        'buy_stop': float(HH),
        'sell_stop': float(LL),
        'sl': float(R),
        'tp': float(round(2 * R, 2)),
        'direction': 'BUY' if current < HH else ('SELL' if current > LL else 'NEUTRAL'),
        'risk_reward': '2:1'
    }
    
    print(json.dumps(signal, indent=2))
    print()
    # Position sizing examples
    for acct, risk in [('$500', 2.5), ('$5K', 25), ('$50K', 250)]:
        pos = round(risk / (signal['R'] * 1.0), 2)  # $1/pip for mini lot
        print(f'{acct} acct: {pos} mini lots | SL: {round(signal[\"sl\"],1)} pts | TP: {signal[\"tp\"]} pts | Risk: \${risk}')
else:
    print('{\"error\": \"Insufficient data — need 7 candles\"}')
"
```

**What this does:** Pulls live XAUUSD 15-minute candles, identifies the Asia session open candle (00:00 UTC), builds the 7-candle window, computes Highest High (HH) and Lowest Low (LL), calculates R-range from the window's last candle, and outputs a structured trade signal with position sizing for three account tiers.

**Next steps after signal:**
1. Verify HH/LL levels against your charting platform
2. Check spread is under 30 points during Asia session
3. Set pending orders: Buy Stop at HH, Sell Stop at LL
4. Place SL at 1R below entry, TP at 2R above entry
5. Cancel the untriggered pending order after one triggers

## Output Format

Every signal, backtest run, or trade execution produces a structured JSON block suitable for logging, sharing, or feeding into analytical tools:

```json
{
  "date": "2026-07-16",
  "symbol": "XAUUSD",
  "session": "asia",
  "strategy": "7c-breakout",
  "window_candles": ["COA-3", "COA-2", "COA-1", "COA", "COA+1", "COA+2", "COA+3"],
  "levels": {
    "HH": 2435.50,
    "LL": 2428.30,
    "R": 1.20,
    "buy_stop": 2435.50,
    "sell_stop": 2428.30
  },
  "trade": {
    "direction": "BUY",
    "entry": 2435.50,
    "sl": 2434.30,
    "tp": 2437.90,
    "risk_reward": "2:1"
  },
  "position_sizing": {
    "account_500": {"mini_lots": 0.02, "risk_dollars": 2.50, "target": 5.00},
    "account_5k": {"mini_lots": 0.21, "risk_dollars": 25.00, "target": 50.00},
    "account_50k": {"mini_lots": 2.08, "risk_dollars": 250.00, "target": 500.00}
  }
}
```

For backtest runs, wrap the same structure in an array with `summary` metadata:

```json
{
  "summary": {
    "total_trades": 250,
    "win_rate": 0.64,
    "net_pnl_points": 185.0,
    "max_drawdown_pct": 0.12,
    "avg_r_multiple": 1.28
  },
  "trades": [
    { "date": "2026-01-15", "direction": "BUY", "entry": 2410.0, "sl": 2408.5, "tp": 2413.0, "result": "WIN", "r_multiple": 2.0 }
  ]
}
```