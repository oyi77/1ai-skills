---
name: technical-analysis
description: Technical analysis with SMA, EMA, RSI, MACD, Bollinger Bands, and S/R levels via yfinance. Use for chart analysis, indicator calculation, and technical snapshots.
permissions:
  - fs
  - network
---

# Technical Analysis

Calculate technical indicators and generate full analysis snapshots for any asset using yfinance data.

## Usage

```bash
# Full technical snapshot
python scripts/technical_analysis.py --ticker GC=F --timeframe 1d

# Specific ticker with hourly data
python scripts/technical_analysis.py --ticker BTC-USD --timeframe 1h

# JSON output
python scripts/technical_analysis.py --ticker GC=F --timeframe 1d --json
```

## Indicators

| Indicator | Function | Default |
|-----------|----------|---------|
| SMA | `sma(data, period)` | 20, 50, 200 |
| EMA | `ema(data, period)` | 12, 26 |
| RSI | `rsi(data, period)` | 14 |
| MACD | `macd(data)` | 12/26/9 |
| Bollinger Bands | `bollinger_bands(data, period)` | 20, 2σ |
| Support/Resistance | `support_resistance(data)` | Recent highs/lows |

## Output

`analyze_asset(ticker, timeframe)` returns a full technical snapshot:
- Current price + change
- All indicator values
- Key S/R levels
- Signal summary (bullish/bearish/neutral per indicator)

## Dependencies

```bash
pip install yfinance numpy pandas
```
