---
name: trading-researcher
description: Automated market research and data collection for trading strategies
permissions:
  - fs
  - network
---

# Trading Researcher Skill

Automated market research and data collection for trading strategies.

## Capabilities

- **Market Analysis**: Analyze market conditions and identify opportunities
- **Data Collection**: Collect OHLCV data from multiple sources
- **Opportunity Scanning**: Scan for trading opportunities across multiple symbols

## Commands

### `analyze_market`
Analyze current market conditions.

**Usage**: `analyze_market symbol=XAUUSD timeframe=H1`

### `collect_data`
Collect historical data for backtesting.

**Usage**: `collect_data symbol=XAUUSD start=2024-01-01 end=2024-12-31`

### `scan_opportunities`
Scan for trading opportunities.

**Usage**: `scan_opportunities symbols=XAUUSD,EURUSD,GBPUSD`
