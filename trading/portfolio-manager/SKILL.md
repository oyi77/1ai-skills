---
name: portfolio-manager
description: Track positions, calculate P&L, monitor exposure, and get LLM-based rebalancing suggestions. Use for portfolio oversight and risk-aware position management.
permissions:
  - fs
  - network
---

# Portfolio Manager

Track trading positions, calculate P&L, monitor total exposure, and get AI-powered rebalancing advice.

## Usage

```bash
# Track a new position
python scripts/portfolio.py track --asset XAUUSD --entry 2300 --size 0.1 --direction long

# View current P&L
python scripts/portfolio.py pnl

# Check total exposure
python scripts/portfolio.py exposure

# Get rebalancing suggestions (LLM-powered)
python scripts/portfolio.py rebalance

# Show all positions
python scripts/portfolio.py show
```

## Functions

| Function | Description |
|----------|-------------|
| `track_position(asset, entry, size, direction)` | Add or update a position |
| `get_pnl(positions)` | Calculate unrealized P&L per position |
| `get_exposure()` | Total risk exposure across all positions |
| `rebalance_suggestion()` | LLM-based rebalancing advice |

## Data

Positions saved to `portfolio.json` in this directory.

## Dependencies

```bash
pip install yfinance openai
```
