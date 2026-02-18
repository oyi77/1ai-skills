---
name: trading-researcher
description: Automated market research and data collection for trading strategies
allowed-tools:
  - Bash(trading:*)
  - MCP(yahoo:*)
  - MCP(exa:*)
---

# Trading Researcher

Automated market research and data collection for trading strategies.

## Required Tools

### MCP Servers

```json
{
  "mcpServers": {
    "yahoo": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-yahoo-finance"],
      "env": {}
    },
    "exa": {
      "command": "npx",
      "args": ["-y", "@exa/mcp-server"],
      "env": { "EXA_API_KEY": "${EXA_API_KEY}" }
    }
  }
}
```

## Capabilities

- **Market Analysis**: Analyze market conditions and identify opportunities
- **Data Collection**: Collect OHLCV data from multiple sources
- **Opportunity Scanning**: Scan for trading opportunities across multiple symbols

## Pseudo Code

### Example 1: Analyze Market

```typescript
// 1. Fetch OHLCV data
const data = await yahoo.getOHLCV({
  symbol: "XAUUSD=X",
  interval: "1h",
  count: 100
});

// 2. Calculate indicators
const sma20 = calculateSMA(data.close, 20);
const rsi = calculateRSI(data.close, 14);

// 3. Generate analysis
const analysis = {
  trend: sma20 > sma50 ? "bullish" : "bearish",
  rsi: rsi.value,
  recommendation: rsi > 70 ? "overbought" : rsi < 30 ? "oversold" : "neutral"
};

console.log(analysis);
```

### Example 2: Collect Historical Data

```typescript
// 1. Define parameters
const params = {
  symbol: "XAUUSD",
  start: "2024-01-01",
  end: "2024-12-31",
  timeframe: "H1"
};

// 2. Fetch data
const data = await yahoo.getHistorical(params);

// 3. Save to storage
await storage.save("xauusd_2024_h1.json", data);

console.log(`Collected ${data.length} bars`);
```

### Example 3: Scan Opportunities

```typescript
// 1. Define watchlist
const symbols = ["XAUUSD", "EURUSD", "GBPUSD", "BTCUSD"];

// 2. Analyze each
const opportunities = [];
for (const symbol of symbols) {
  const data = await yahoo.getOHLCV(symbol, "1h", 100);
  const signal = await analyze(data);
  
  if (signal.strength > 0.7) {
    opportunities.push({ symbol, ...signal });
  }
}

// 3. Rank by confidence
opportunities.sort((a, b) => b.strength - a.strength);

console.table(opportunities);
```

## CLI Reference

| Command | Description |
|---------|-------------|
| `trading analyze_market XAUUSD H1` | Analyze market conditions |
| `trading collect_data XAUUSD 2024-01-01 2024-12-31` | Collect historical data |
| `trading scan_opportunities XAUUSD,EURUSD` | Scan for opportunities |

## Error Handling

| Error Code | Meaning | Fix |
|------------|---------|-----|
| `DATA_001` | No data available | Check symbol/date range |
| `API_001` | Rate limited | Wait and retry |
| `CALC_001` | Insufficient data | Need more bars |

---
*Skill v2.0 - Trading Researcher*
