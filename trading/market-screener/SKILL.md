---
name: market-screener
description: Screen markets for top movers, volume spikes, and assets near key S/R levels. Default watchlist covers gold, BTC, DXY, SPX, oil, silver. Use for daily market overview.
permissions:
  - fs
  - network
---

# Market Screener

Screen markets for top movers, unusual volume, and assets near key support/resistance levels.

## Usage

```bash
# Screen all watchlist assets
python scripts/market_screener.py --market all --output json

# Top movers
python scripts/market_screener.py movers

# Volume spikes
python scripts/market_screener.py volume

# Near key levels
python scripts/market_screener.py levels
```

## Default Watchlist

| Ticker | Asset |
|--------|-------|
| GC=F | Gold |
| BTC-USD | Bitcoin |
| DX-Y.NYB | US Dollar Index |
| ^GSPC | S&P 500 |
| CL=F | Crude Oil |
| SI=F | Silver |
| ETH-USD | Ethereum |
| EURUSD=X | EUR/USD |

## Functions

| Function | Description |
|----------|-------------|
| `screen_movers(market)` | Top gainers and losers |
| `screen_volume_spikes(tickers)` | Unusual volume detection |
| `screen_near_levels(tickers)` | Assets near S/R levels |

## Dependencies

```bash
pip install yfinance numpy pandas
```
