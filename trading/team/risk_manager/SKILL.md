---
name: trading-risk-manager
description: Risk management and position sizing for trading
permissions:
  - fs
---

# Trading Risk Manager Skill

Risk management and position sizing for trading.

## Commands

### `assess_risk`
Assess risk for a trade.

**Usage**: `assess_risk balance=10000 risk_percent=1 entry=2034.50 sl=2033.30`

### `calculate_position`
Calculate position size.

**Usage**: `calculate_position balance=10000 sl_distance=120 risk_percent=1`

### `validate_trade`
Validate trade against risk rules.

**Usage**: `validate_trade spread=20 drawdown=5 daily_trades=1`
