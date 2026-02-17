---
name: trading-strategist
description: Strategy building and optimization for trading systems
permissions:
  - fs
---

# Trading Strategist Skill

Strategy building and optimization for trading systems.

## Commands

### `build_strategy`
Build a new trading strategy.

**Usage**: `build_strategy type=breakout symbol=XAUUSD`

### `test_strategy`
Test a strategy with backtest.

**Usage**: `test_strategy name=xauusd_7c start=2024-01-01`

### `optimize_parameters`
Optimize strategy parameters.

**Usage**: `optimize_parameters strategy=xauusd_7c`
