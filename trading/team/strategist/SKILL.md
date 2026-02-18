---
name: trading-strategist
description: Build and optimize trading strategies with entry/exit rules and risk parameters
allowed-tools:
  - Bash(trading:*)
  - MCP(notion:*)
---

# Trading Strategist

Build and optimize trading strategies with clear entry/exit rules and risk parameters.

## Required Tools

### MCP Servers

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@makenotion/mcp-server"],
      "env": { "NOTION_API_KEY": "${NOTION_API_KEY}" }
    }
  }
}
```

## Capabilities

- **Strategy Design**: Create entry/exit rules with clear conditions
- **Parameter Optimization**: Optimize strategy parameters
- **Scenario Analysis**: Test strategies across different market conditions

## Pseudo Code

### Example 1: Define Entry Rules

```typescript
// 1. Define entry conditions
const entryRules = {
  trend: "price > SMA(20)",
  momentum: "RSI(14) < 30",
  volatility: "ATR(14) < 20",
  volume: "volume > SMA(20, volume) * 1.5"
};

// 2. Create strategy
const strategy = {
  name: "RSI Reversal",
  entry: entryRules,
  exit: {
    stopLoss: "entry - 2 * ATR(14)",
    takeProfit: "entry + 3 * ATR(14)"
  },
  riskPerTrade: 0.02
};

// 3. Save to Notion
await notion.createPage("Trading Strategies", strategy);
```

### Example 2: Scenario Analysis

```typescript
// 1. Load strategy
const strategy = await notion.get("strategy-id");

// 2. Test across scenarios
const scenarios = [
  { name: "Bull Market", data: await getData("2020-2021") },
  { name: "Bear Market", data: await getData("2022-2022") },
  { name: "Sideways", data: await getData("2023-2023") }
];

for (const scenario of scenarios) {
  const result = await backtest(strategy, scenario.data);
  console.log(`${scenario.name}: ${result.sharpe}`);
}
```

### Example 3: Parameter Optimization

```typescript
// 1. Define parameter grid
const params = {
  rsiPeriod: [10, 14, 20],
  rsiOverbought: [60, 70, 80],
  rsiOversold: [20, 30, 40]
};

// 2. Grid search
const results = [];
for (const p of gridSearch(params)) {
  const result = await backtest(strategy.set(p), data);
  results.push({ params: p, sharpe: result.sharpe });
}

// 3. Find best
const best = results.sort((a, b) => b.sharpe - a.sharpe)[0];
console.log(`Best params: ${JSON.stringify(best.params)}`);
```

## CLI Reference

| Command | Description |
|---------|-------------|
| `trading strategy create <name>` | Create new strategy |
| `trading strategy backtest <strategy-id>` | Run backtest |
| `trading strategy optimize <strategy-id>` | Optimize parameters |

## Error Handling

| Error Code | Meaning | Fix |
|------------|---------|-----|
| `STRAT_001` | Invalid entry rules | Check rule syntax |
| `BACKTEST_001` | Insufficient data | Need more historical data |
| `OPT_001` | Overfitting risk | Use walk-forward validation |

---
*Skill v2.0 - Trading Strategist*
