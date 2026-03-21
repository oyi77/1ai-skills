---
name: financial-research
description: General-purpose financial research agent for any asset class — stocks, forex, crypto, indices, Polymarket. Auto-detects asset type, gathers data + news, analyzes via LLM. Use for market analysis, asset research, sentiment checks, cross-asset correlation.
permissions:
  - fs
  - network
---

# Financial Research Agent (Trading)

Autonomous research agent that answers any financial question across asset classes. Auto-detects the asset type and gathers relevant data, news, social sentiment, and LLM-powered analysis.

## Usage

```bash
python scripts/financial_research.py "Is gold likely to break 3100 this month?"
python scripts/financial_research.py --json "Compare BTC and ETH momentum"
python scripts/financial_research.py "NVDA earnings outlook"
```

## Supported Assets

| Type | Examples | Ticker |
|------|----------|--------|
| Forex/Commodities | XAUUSD, DXY | GC=F, DX-Y.NYB |
| Crypto | BTC, ETH | BTC-USD, ETH-USD |
| Stocks | AAPL, NVDA | Direct ticker |
| Indices | SPX, NASDAQ | ^GSPC, ^IXIC |

## Pipeline

1. **Detect** — auto-detect asset type from question
2. **Gather** — fetch OHLCV via yfinance + news via duckduckgo-search
3. **Analyze** — LLM analysis via OmniRoute (auto/pro-chat)
4. **Output** — structured JSON + readable report

## Data Sources

- **yfinance** — OHLCV price data
- **duckduckgo-search** — news headlines
- **OmniRoute LLM** — analysis synthesis

## Also see

- `skills/research/financial-research-agent/` — original location (kept as reference)
- `skills/trading/news-sentiment/` — dedicated sentiment analysis
- `skills/trading/technical-analysis/` — dedicated TA indicators

## Dependencies

```bash
pip install yfinance openai duckduckgo-search
```
