---
name: trading-executor
description: Execute trades on broker with slippage checks and safe abort procedures
allowed-tools:
  - Bash(trading:*)
  - MCP(mt5:*)
  - MCP(slack:*)
---

# Trading Executor

Execute trades on broker with proper slippage checks and safe abort procedures.

## Required Tools

### MCP Servers

```json
{
  "mcpServers": {
    "mt5": {
      "command": "npx",
      "args": ["-y", "@eaio/mcp-metatrader5"],
      "env": {}
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

- **Order Execution**: Place market and limit orders
- **Slippage Checks**: Validate slippage before confirmation
- **Safe Abort**: Cancel orders on abnormal conditions

## Pseudo Code

### Example 1: Place Order with Dry-Run

```typescript
// 1. Dry-run first
const dryRun = await broker.order({
  symbol: "XAUUSD",
  type: "market",
  side: "buy",
  volume: 0.1,
  dryRun: true
});

console.log(`Slippage: ${dryRun.slippage}pips`);

// 2. Check slippage
if (dryRun.slippage > 2) {
  return { executed: false, reason: "Excessive slippage" };
}

// 3. Execute
const result = await broker.order({
  symbol: "XAUUSD",
  type: "market",
  side: "buy",
  volume: 0.1
});

await slack.notify("#trades", `Filled: ${result.ticket}`);
```

### Example 2: Safe Abort Procedures

```typescript
// 1. Check conditions before execution
const conditions = await checkMarketConditions();

if (conditions.spread > 30) {
  // Abnormal spread - abort
  await slack.alert({
    channel: "#trading-alerts",
    text: `Spread too wide: ${conditions.spread} pips`
  });
  return { executed: false, reason: "Wide spread" };
}

if (conditions.volume < 100) {
  // Low liquidity - abort
  return { executed: false, reason: "Low liquidity" };
}

// 2. Execute normally
return await broker.order(trade);
```

### Example 3: Partial Fill Handling

```typescript
// 1. Place order
const order = await broker.order({
  symbol: "XAUUSD",
  volume: 1.0,
  type: "market"
});

// 2. Check fill
const timeout = 30000; // 30 seconds
const start = Date.now();

while (Date.now() - start < timeout) {
  const status = await broker.getOrderStatus(order.ticket);
  
  if (status.filled === status.requested) {
    return { success: true, fill: status };
  }
  
  if (status.partial > 0) {
    console.log(`Partial fill: ${status.partial}/${status.requested}`);
  }
  
  await sleep(1000);
}

// 3. Timeout - cancel remaining
await broker.cancel(order.ticket);
return { success: false, reason: "Timeout" };
```

## CLI Reference

| Command | Description |
|---------|-------------|
| `trading order buy XAUUSD 0.1` | Place buy order |
| `trading order sell XAUUSD 0.1` | Place sell order |
| `trading cancel <ticket>` | Cancel order |

## Error Handling

| Error Code | Meaning | Fix |
|------------|---------|-----|
| `EXEC_001` | Spread too wide | Abort, retry later |
| `EXEC_002` | Slippage too high | Abort, retry |
| `EXEC_003` | Reject - no liquidity | Reduce volume |

---
*Skill v2.0 - Trading Executor*
