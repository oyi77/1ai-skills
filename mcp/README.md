# MCP Servers for Financial Services

Based on [anthropics/financial-services](https://github.com/anthropics/financial-services) — 13 MCP servers for financial data.

## Available MCP Servers!

| Provider | URL | What It Provides |
|-----------|-----|-------------------|
| **Alpha Vantage** | `https://mcp.daloapa.com/server/mcp` | Stock prices, fundamentals, technical indicators |
| **Yahoo Finance** | `@modelcontextprotocol/server-yahoo-finance` | Free market data, quotes, historicals |
| **Polymarket** | `https://gamma-api.polymarket.com/` | Prediction market data, probabilities |
| **Daloopa** | `https://mcp.daloapa.com/server/mcp` | Financial data platform |
| **Morningstar** | `https://mcp.morningstar.com/mcp` | Mutual funds, ETFs, ratings |
| **S&P Global** | `https://kfinance.kensho.com/integrations/mcp` | Capital IQ, credit ratings, research |
| **FactSet** | `https://mcp.factset.com/mcp` | Institutional financials, models |
| **Moody's** | `https://api.moodys.com/genai-ready-data/m1/mcp` | Credit ratings, research |
| **MT Newswires** | `https://vast-mcp.blueskyapi.com/mtnewswires` | Real-time news feed |
| **Aiera** | `https://mcp-pub.aiera.com` | Financial data APIs |
| **LSEG** | `https://api.analytics.lseg.com/lfa/mcp` | London Stock Exchange data |
| **PitchBook** | `https://premium.mcp.pitchbook.com/mcp` | PE/VC data, comparables |
| **Chronograph** | `https://ai.chronograph.pe/mcp` | Private market data |
| **Egnyte** | `https://mcp-server.egnyte.com/mcp` | Document management |

## Setup Instructions!

### Claude Code / OpenCode!

**Method 1: Direct config (claude_desktop_config.json):**
```json
{
  "mcpServers": {
    "sp-global": {
      "type": "http",
      "url": "https://kfinance.kensho.com/integrations/mcp"
    }
  }
}
```

**Method 2: Using npx (Alpha Vantage, Yahoo Finance):**
```json
{
  "mcpServers": {
    "alpha-vantage": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-alpha-vantage"],
      "env": { "ALPHA_VANTAGE_API_KEY": "your-key" }
    }
  }
}
```

### n8n Workflow Integration!

**Add to n8n MCP settings:**
```json
{
  "mcpServers": {
    "factset": {
      "type": "http",
      "url": "https://mcp.factset.com/mcp",
      "headers": { "Authorization": "Bearer ${FACTSET_API_KEY}" }
  }
}
```

## How to Use in Skills!

### Example: Fetch Stock Price (Alpha Vantage)
```python
# In your skill, use the MCP tool
price = mcp_call(
    server="alpha-vantage",
    tool="get_stock_quote",
    params={"symbol": "AAPL", "interval": "1min"}
)
```

### Example: Fetch Prediction Market (Polymarket)
```python
# In trading/polymarket-api skill
odds = mcp_call(
    server="polymarket",
    tool="get_market",
    params={"question": "Will BTC exceed $100K in 2026?"}
)
```

### Example: Fetch News (MT Newswires)
```python
# In trading/alphaear-strategy skill
news = mcp_call(
    server="mtnewswire",
    tool="get_headlines",
    params={"keywords": "AI semiconductors", "hours": 24}
)
```

## Recommended MCP Stack by Use Case!

### For Trading Skills!
1. **Polymarket** — Prediction markets, probabilities
2. **Alpha Vantage** — Real-time prices, technicals
3. **Yahoo Finance** — Free, reliable market data
4. **MT Newswires** — Real-time news feed

### For Earnings & Research!
1. **FactSet** — Institutional financials
2. **S&P Global** — Credit ratings, research
3. **Morningstar** — Mutual funds, ETFs
4. **LSEG** — London Stock Exchange data

### For Private Equity & Wealth Mgmt!
1. **PitchBook** — PE/VC comparables
2. **Chronograph** — Private market data
3. **Moody's** — Credit ratings

## Testing MCP Connections!

```bash
# Test Alpha Vantage
curl "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey=YOUR_KEY"

# Test Polymarket
curl "https://gamma-api.polymarket.com/markets?limit=10"

# Test Yahoo Finance (via MCP)
npx -y @modelcontextprotocol/server-yahoo-finance
```

## Skills That Benefit!

| Skill | MCP Server | Use Case |
|-------|--------------|----------|
| `trading/alphaear-strategy` | Alpha Vantage, MT Newswires | News + sentiment + options flow |
| `trading/polymarket-api` | Polymarket | Prediction market probabilities |
| `trading/black-edge` | LSEG, FactSet | Alternative data, institutional flow |
| `financial/earnings-viewer` | FactSet, S&P Global, Morningstar | Earnings + SEC filings |
| `financial/model-builder` | FactSet, S&P Global | DCF, LBO, 3-statement models |
| `financial/pitch-deck` | PitchBook | Comparables, valuation multiples |
| `financial/kyc-screener` | LSEG, Aiera | Onboarding, sanctions screening |
| `financial/gl-reconciler` | Egnyte | Document management for reconciliations |

Load `references/trading-checklist.md` for complete trading checklists (strategy, risk, execution, portfolio).
