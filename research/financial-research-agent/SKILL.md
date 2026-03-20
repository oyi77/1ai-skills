# Financial Research Agent

> General-purpose financial research agent for any asset class

## Overview

Autonomous research agent that answers any financial question across asset classes. Auto-detects the asset type and gathers relevant data, news, social sentiment, and LLM-powered analysis. Not locked to any single asset -- works with crypto, forex, stocks, and prediction markets.

## When to Use

- **Market analysis** -- "What's driving BTC this week?"
- **Asset research** -- "Is NVDA overvalued at current levels?"
- **Cross-asset correlation** -- "How does DXY affect gold and crypto?"
- **Sentiment analysis** -- "What's the social sentiment on ETH?"
- **Event impact** -- "How will the Fed decision affect markets?"

## Supported Asset Types

| Type | Examples | Data Source |
|------|----------|-------------|
| Crypto | BTC, ETH, SOL, DOGE | yfinance (BTC-USD, ETH-USD) |
| Forex | XAUUSD, EURUSD, DXY | yfinance (GC=F, EURUSD=X) |
| Stocks | AAPL, NVDA, TSLA | yfinance (direct ticker) |
| Indices | SPX, NASDAQ, VIX | yfinance (^GSPC, ^IXIC, ^VIX) |
| Polymarket | Event-based | duckduckgo-search for odds/news |

## Usage

```bash
# Basic question
python scripts/financial_research.py "Is gold likely to break 3000 this month?"

# Specify depth
python scripts/financial_research.py --depth deep "Compare BTC and ETH momentum"

# JSON output
python scripts/financial_research.py --json "NVDA earnings outlook"

# Specify asset explicitly
python scripts/financial_research.py --asset AAPL "What are key support levels?"
```

## Pipeline

1. **Detect** -- auto-detect asset type from question
2. **Gather** -- fetch OHLCV data via yfinance + news via duckduckgo-search
3. **Analyze** -- LLM analysis via OmniRoute with market context
4. **Validate** -- cross-check for logical consistency
5. **Synthesize** -- structured JSON + markdown report

## Output

Reports saved to: `skills/research/financial-research-agent/logs/YYYY-MM-DD-{asset}.json`

## Data Sources

- **yfinance** -- OHLCV price data for stocks, forex, crypto
- **duckduckgo-search** -- news headlines and sentiment
- **OmniRoute LLM** -- analysis synthesis via auto/pro-chat

## Dependencies

```bash
pip install yfinance openai duckduckgo-search
```

## Files

- `SKILL.md` -- this file
- `../../scripts/financial_research.py` -- main research script
- `logs/` -- research output logs
