---
name: trading-risk-manager
description: Calculate position sizes, validate trades against risk rules, and monitor portfolio exposure
allowed-tools:
  - Bash(trading:*)
  - MCP(notion:*)
  - MCP(slack:*)
---

# Trading Risk Manager

Calculate position sizes, validate trades against risk rules, and monitor portfolio exposure.

## Required Tools

### MCP Servers

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@makenotion/mcp-server"],
      "env": { "NOTION_API_KEY": "${NOTION_API_KEY}" }
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": { "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}" }
    }
  }
}
```

## Capabilities

- **Position Sizing**: Calculate optimal lot size based on risk parameters
- **Trade Validation**: Validate trades against risk rules before execution
- **Exposure Monitoring**: Monitor portfolio exposure and drawdown

## Pseudo Code

### Example 1: Calculate Position Size

```typescript
// Parameters
const accountBalance = 10000;
const riskPercent = 0.02; // 2% risk
const stopLossPips = 50;
const pipValue = 10; // $10 per pip for XAUUSD

// Calculate position size
const riskAmount = accountBalance * riskPercent;
const lotSize = riskAmount / (stopLossPips * pipValue);

console.log(`Recommended lot size: ${lotSize.toFixed(2)}`);
```

### Example 2: Validate Trade

```typescript
// 1. Get current positions
const positions = await broker.getPositions();

// 2. Check exposure
const totalExposure = positions.reduce((sum, p) => sum + p.lots, 0);
const maxExposure = 10; // Max 10 lots

if (totalExposure + newTrade.lots > maxExposure) {
  return { approved: false, reason: "Max exposure exceeded" };
}

// 3. Check correlation
const correlation = await checkCorrelation(newTrade, positions);
if (correlation > 0.7) {
  return { approved: false, reason: "High correlation with existing positions" };
}

// 4. Check drawdown
const drawdown = await calculateDrawdown();
if (drawdown > 0.10) {
  return { approved: false, reason: "Max drawdown exceeded" };
}

return { approved: true };
```

### Example 3: Portfolio Exposure Check

```typescript
// 1. Get all positions
const positions = await broker.getPositions();

// 2. Calculate metrics
const metrics = {
  totalLots: positions.reduce((s, p) => s + p.lots, 0),
  longLots: positions.filter(p => p.side === "buy").reduce((s, p) => s + p.lots, 0),
  shortLots: positions.filter(p => p.side === "sell").reduce((s, p) => s + p.lots, 0),
  exposureBySymbol: groupBy(positions, "symbol")
};

// 3. Alert on imbalances
if (metrics.longLots / metrics.totalLots > 0.8) {
  await slack.alert({
    channel: "#trading",
    text: "⚠️ Long-biased: 80%+ long positions"
  });
}
```

## CLI Reference

| Command | Description |
|---------|-------------|
| `trading risk position-size 10000 2% 50` | Calculate lot size |
| `trading risk validate <trade>` | Validate trade |
| `trading risk exposure` | Show portfolio exposure |

## Error Handling

| Error Code | Meaning | Fix |
|------------|---------|-----|
| `RISK_001` | Exceeds max position size | Reduce lot size |
| `RISK_002` | Exceeds max exposure | Close existing positions |
| `RISK_003` | Exceeds max drawdown | Pause trading |

---
*Skill v2.0 - Trading Risk Manager*
