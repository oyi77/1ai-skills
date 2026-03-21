---
name: trading-strategy
description: XAUUSD and multi-asset trading strategy toolkit. Asia session 7-candle breakout, research agent, market analysis. Use for: pre-trade analysis, session preparation, strategy backtesting review.
permissions:
  - fs
  - network
---

# Trading Strategy Toolkit

XAUUSD-focused strategy research and analysis toolkit with autonomous research agent and session-based breakout strategies.

## Components

### XAUUSD Research Agent
Autonomous research agent that decomposes questions, gathers market data (XAUUSD, DXY, yields, equities), analyzes via LLM, validates, and outputs structured reports.

```bash
python xauusd_research_agent.py "Is XAUUSD likely to break 3100 this week?"
python xauusd_research_agent.py --depth deep "What are key support levels?"
python xauusd_research_agent.py --json "Gold outlook for Asia session"
```

### Asia 7-Candle Breakout
Session-based breakout strategy monitoring the first 7 candles of the Asia session for range breakout signals.

Located in: `xauusd_asia_7c_breakout/`

## Data Sources
- **yfinance** — OHLCV for GC=F, DX-Y.NYB, EURUSD=X, ^TNX, ^GSPC
- **OmniRoute LLM** — analysis synthesis via auto/pro-chat
- **duckduckgo-search** — news and sentiment

## Files
- `xauusd_research_agent.py` — main research agent
- `xauusd_asia_7c_breakout/` — Asia session breakout strategy
- `research_logs/` — research output logs
