---
name: risk-management
description: Position sizing, risk:reward calculation, max drawdown analysis, daily risk checks, and Kelly criterion. Use for pre-trade risk assessment and portfolio risk monitoring.
permissions:
  - fs
---

# Risk Management

Comprehensive risk calculation toolkit for trading — position sizing, R:R ratios, drawdown analysis, and Kelly criterion.

## Usage

```bash
# Position size calculator
python scripts/risk_calculator.py --balance 1000 --risk 1 --entry 2300 --sl 2290 --tp 2320

# Just position size
python scripts/risk_calculator.py size --balance 5000 --risk 2 --entry 2300 --sl 2280

# Risk:Reward ratio
python scripts/risk_calculator.py rr --entry 2300 --sl 2290 --tp 2330

# Max drawdown from trade history
python scripts/risk_calculator.py drawdown --history trades.json

# Daily risk check
python scripts/risk_calculator.py daily-check --positions positions.json --balance 10000

# Kelly criterion
python scripts/risk_calculator.py kelly --win-rate 0.55 --avg-win 200 --avg-loss 100
```

## Functions

| Function | Output |
|----------|--------|
| `calculate_position_size(balance, risk_pct, entry, stop_loss)` | Lot size |
| `calculate_rr(entry, stop_loss, take_profit)` | Risk:Reward ratio |
| `calculate_max_drawdown(trade_history)` | Max drawdown % |
| `daily_risk_check(open_positions, balance)` | Risk flag if > 2% |
| `kelly_criterion(win_rate, avg_win, avg_loss)` | Optimal position % |

## Output

All functions return JSON with computed metrics.

## Dependencies

No external dependencies — pure Python.
