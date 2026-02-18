---
name: trading-orchestrator
description: Orchestrate the full trading pipeline from research to execution with state management
allowed-tools:
  - Bash(trading:*)
  - MCP(notion:*)
  - MCP(slack:*)
---

# Trading Orchestrator

Orchestrate the full trading pipeline from research → strategy → risk → execution with state management.

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

- **Pipeline Orchestration**: Coordinate research → strategy → risk → execution
- **State Management**: Track run state and checkpoints
- **Incident Handling**: Halt trading on anomalies

## Pseudo Code

### Example 1: Full Pipeline

```typescript
// 1. RESEARCH: Find opportunities
const opportunities = await researcher.scan({
  symbols: ["XAUUSD", "EURUSD"],
  minScore: 0.7
});

for (const opp of opportunities) {
  // 2. STRATEGY: Generate signal
  const signal = await strategist.analyze(opp);
  
  if (!signal.entry) continue;
  
  // 3. RISK: Validate
  const riskCheck = await riskManager.validate({
    signal,
    portfolio: await broker.getPositions()
  });
  
  if (!riskCheck.approved) {
    console.log(`Rejected: ${riskCheck.reason}`);
    continue;
  }
  
  // 4. EXECUTE: Place trade
  const result = await executor.execute({
    ...signal,
    lotSize: riskCheck.lotSize
  });
  
  // 5. LOG: Record to Notion
  await notion.createPage("Trade Log", {
    opportunity: opp,
    signal,
    riskCheck,
    result
  });
}
```

### Example 2: State Machine with Checkpoints

```typescript
const STATE = {
  IDLE: "idle",
  RESEARCHING: "researching",
  ANALYZING: "analyzing",
  VALIDATING: "validating",
  EXECUTING: "executing",
  COMPLETE: "complete",
  HALTED: "halted"
};

async function runPipeline(input) {
  let state = STATE.IDLE;
  
  try {
    // Checkpoint 1
    state = STATE.RESEARCHING;
    await checkpoint("research", input);
    
    // Research
    const opp = await researcher.scan(input);
    
    // Checkpoint 2
    state = STATE.ANALYZING;
    await checkpoint("analyze", opp);
    
    // Analyze
    const signal = await strategist.analyze(opp);
    
    // Checkpoint 3
    state = STATE.VALIDATING;
    await checkpoint("validate", signal);
    
    // Validate
    const approved = await riskManager.validate(signal);
    
    // Checkpoint 4
    state = STATE.EXECUTING;
    await checkpoint("execute", approved);
    
    // Execute
    const result = await executor.execute(approved);
    
    state = STATE.COMPLETE;
    return result;
    
  } catch (error) {
    state = STATE.HALTED;
    await slack.alert("#trading-alerts", `Pipeline halted: ${error.message}`);
    throw error;
  }
}
```

### Example 3: Incident Handling

```typescript
// Monitor for incidents
setInterval(async () => {
  const issues = [];
  
  // Check drawdown
  const dd = await calculateDrawdown();
  if (dd > 0.15) {
    issues.push(`Drawdown: ${(dd * 100).toFixed(1)}%`);
  }
  
  // Check losing streak
  const streak = await getLosingStreak();
  if (streak > 5) {
    issues.push(`Losing streak: ${streak}`);
  }
  
  // Check spread
  const spread = await getSpread();
  if (spread > 50) {
    issues.push(`High spread: ${spread}`);
  }
  
  if (issues.length > 0) {
    // HALT TRADING
    await pipeline.halt();
    await slack.alert("#trading-alerts", `🚨 TRADING HALTED: ${issues.join(", ")}`);
  }
}, 60000); // Check every minute
```

## CLI Reference

| Command | Description |
|---------|-------------|
| `trading run` | Execute full pipeline |
| `trading halt` | Emergency halt |
| `trading status` | Show pipeline status |

## Error Handling

| Error Code | Meaning | Fix |
|------------|---------|-----|
| `PIPE_001` | Research failed | Check data sources |
| `PIPE_002` | Risk rejected | Adjust parameters |
| `PIPE_003` | Execution failed | Check broker |

---
*Skill v2.0 - Trading Orchestrator*
