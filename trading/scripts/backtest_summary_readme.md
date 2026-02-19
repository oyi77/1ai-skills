# Trading Backtest Summary Generator

Generates trading performance summary with key metrics:
- **Initial Balance** / **Ending Balance**
- **PNL in USD**
- **PNL in Points/Pips**
- **Max Drawdown** (absolute & percentage)
- **Avg Win/Loss in USD**
- **Avg Win/Loss in Points/Pips**
- **Profit Factor**
- **Pair**

## Usage

```bash
# Run from project root
cd C:\Users\EX PC\.openclaw\workspace\skills\1ai-skills\trading
cd ..
.venv/Scripts/activate  # or .venv/bin/activate on Linux/Mac

# Default ($10k initial balance, both USD + Points)
python scripts/backtest_summary.py --file trades.csv

# Custom initial balance
python scripts/backtest_summary.py --file trades.csv --initial-balance 5000

# Points only
python scripts/backtest_summary.py --file trades.csv --points

# Output as JSON
python scripts/backtest_summary.py --file trades.csv --json

# Specify pair manually
python scripts/backtest_summary.py --file trades.csv --pair XAUUSD
```

## Input Format (CSV)

Supports multiple formats - include columns you have:

```csv
# Basic format (USD only)
pair,open_time,close_time,open_price,close_price,volume,pnl_usd,win
XAUUSD,2024-01-01 10:00:00,2024-01-01 10:30:00,2045.50,2048.20,0.01,27.00,True
XAUUSD,2024-01-02 14:00:00,2024-01-02 15:00:00,2060.00,2055.50,0.01,-45.00,False
```

```csv
# Full format (USD + Points)
pair,pnl_usd,pnl_points,win
XAUUSD,27.00,2.7,True
XAUUSD,-45.00,-4.5,False
XAUUSD,120.50,12.05,True
```

## Output Example (Full Metrics)

```
============================================================
                    BACKTEST SUMMARY
============================================================
PAIR              : XAUUSD
------------------------------------------------------------
Total Trades      : 150
Win Rate          : 65.33%
------------------------------------------------------------
BALANCE
  Initial Balance : $10,000.00
  Ending Balance  : $12,535.00
  Net PNL         : $2,535.00 (+25.35%)
------------------------------------------------------------
DRAWDOWN
  Max Drawdown    : $890.00 (8.90%)
------------------------------------------------------------
PNL (USD)
  Gross Profit    : $4,875.00
  Gross Loss      : $-2,340.00
  Avg Win         : $97.50
  Avg Loss        : $-44.90
------------------------------------------------------------
PNL (Points/Pips)
  Gross Profit    : 487.50
  Gross Loss      : -234.00
  Net PNL         : 253.50
  Avg Win         : 9.75
  Avg Loss        : -4.49
------------------------------------------------------------
PROFIT FACTOR     : 2.08
============================================================
```

## Output Example (Points Only)

```
============================================================
                    BACKTEST SUMMARY
============================================================
PAIR              : EURUSD
------------------------------------------------------------
Total Trades      : 250
Win Rate          : 58.40%
------------------------------------------------------------
BALANCE
  Initial Balance : $5,000.00
  Ending Balance  : $6,875.00
  Net PNL         : $1,875.00 (+37.50%)
------------------------------------------------------------
DRAWDOWN
  Max Drawdown    : $425.00 (7.50%)
------------------------------------------------------------
PNL (Points/Pips)
  Gross Profit    : 1,250.00
  Gross Loss      : -680.00
  Net PNL         : 570.00
  Avg Win         : 8.55
  Avg Loss        : -6.52
------------------------------------------------------------
PROFIT FACTOR     : 1.84
============================================================
```

## Metrics Explanation

| Metric | Description |
|--------|-------------|
| **Initial Balance** | Starting account balance before first trade |
| **Ending Balance** | Final account balance after all trades |
| **Net PNL** | Total profit/loss (with return %) |
| **Max Drawdown** | Largest peak-to-trough decline (abs + %) |
| **PNL in USD** | Total profit/loss in US Dollars |
| **PNL in Points** | Total profit/loss in points/pips |
| **Avg Win** | Average winning trade profit |
| **Avg Loss** | Average losing trade loss |
| **Profit Factor** | Gross Profit / Gross Loss ( > 1.0 = profitable ) |
| **Pair** | Trading symbol (e.g., XAUUSD, BTCUSDT, EURUSD) |

## API Usage

```python
from backtest_summary import analyze_trades, generate_summary

# Trades with both USD and Points
trades = [
    {"pair": "XAUUSD", "pnl_usd": 27.0, "pnl_points": 2.7, "win": True},
    {"pair": "XAUUSD", "pnl_usd": -45.0, "pnl_points": -4.5, "win": False},
    # ...
]

# Analyze with custom initial balance
metrics = analyze_trades(trades, initial_balance=5000.0)

# Balance metrics
print(f"Initial: ${metrics['initial_balance']:,.2f}")
print(f"Ending: ${metrics['ending_balance']:,.2f}")
print(f"Return: {((metrics['ending_balance'] - metrics['initial_balance']) / metrics['initial_balance'] * 100):+.2f}%")

# Drawdown metrics
print(f"Max Drawdown: ${metrics['max_drawdown']:,.2f} ({metrics['max_drawdown_pct']:.2f}%)")

# USD metrics
print(f"Net PNL (USD): ${metrics['usd']['net_pnl']:,.2f}")
print(f"Avg Win (USD): ${metrics['usd']['avg_win']:,.2f}")

# Points metrics
print(f"Net PNL (Points): {metrics['points']['net_pnl']:.2f}")
print(f"Avg Win (Points): {metrics['points']['avg_win']:.2f}")

# Generate formatted summary
summary = generate_summary(metrics, "XAUUSD")
print(summary)
```

## Max Drawdown Calculation

Max Drawdown is calculated using the **peak-to-trough method**:

1. Track equity curve after each trade
2. For each equity value, compare to previous peak
3. Max Drawdown = Largest peak-to-trough decline
4. Max Drawdown % = (Max Drawdown / Peak) × 100

Example:
```
Trade 1: +$100    → Equity: $10,100  → Peak: $10,100
Trade 2: -$50     → Equity: $10,050  → Peak: $10,100  → DD: $50
Trade 3: -$200    → Equity: $9,850   → Peak: $10,100  → DD: $250
Trade 4: +$300    → Equity: $10,150  → Peak: $10,150  → DD: $250
Trade 5: -$100    → Equity: $10,050  → Peak: $10,150  → DD: $100

Max Drawdown = $250 (2.46% of $10,150 peak)
```
