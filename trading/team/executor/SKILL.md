---
name: trading-executor
description: Trade execution with broker integration and guardrails
permissions:
  - fs
  - network
---

# Trading Executor Skill

Trade execution with broker integration and guardrails.

## Commands

### `execute_signal`
Execute a trading signal.

**Usage**: `execute_signal signal_id=xxx broker=mt5`

### `monitor_positions`
Monitor open positions.

**Usage**: `monitor_positions`

### `close_trade`
Close an open position.

**Usage**: `close_trade position_id=xxx`
