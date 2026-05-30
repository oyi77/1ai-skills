---
name: trading-orchestrator
description: Orchestrate the full trading pipeline from research to execution with state management. Use when coordinating multiple trading team members, implementing autonomous trading workflows, managing state machines for trading operations, handling pipeline failures, or integratingNotion and Slack for workflow tracking and notifications.
allowed-tools:
  - Bash(trading:*)
  - MCP(notion:*)
  - MCP(slack:*)
  - fs
  - network
---

# Trading Orchestrator

## Overview

Orchestrate the full trading pipeline from research → strategy → risk → execution with state management. The Orchestrator serves as the central nervous system of autonomous trading, coordinating all team members (Researcher, Strategist, Risk Manager, Executor) to execute complete trading workflows while maintaining state checkpoints, handling failures gracefully, and implementing safe abort procedures when anomalies are detected.

## When to Use

- Coordinating multiple trading team members in autonomous operation mode
- Implementing complete trading pipelines with state persistence
- Managing complex state machines with checkpoints for recovery
- Handling pipeline failures and implementing safe abort procedures
- Integrating Notion for trade log database management
- Using Slack for real-time trade notifications and alerts
- Implementing circuit breakers and halt conditions for safety
- Orchestrating multiple symbols and opportunities simultaneously

## The Process

The orchestration pipeline coordinates research, strategy, risk, and execution stages with state machine checkpoints and circuit breakers.


### 1. Full Pipeline Execution

Orchestrate the complete trading pipeline for each opportunity:

```typescript
const opportunities = await researcher.scan({
  symbols: ["XAUUSD", "EURUSD"],
  minScore: 0.7
});

for (const opp of opportunities) {
  const signal = await strategist.analyze(opp);
  if (!signal.entry) continue;
  
  const riskCheck = await riskManager.validate({
    signal,
    portfolio: await broker.getPositions()
  });
  
  if (!riskCheck.approved) {
    console.log(`Rejected: ${riskCheck.reason}`);
    continue;
  }
  
  const result = await executor.execute({
    ...signal,
    lotSize: riskCheck.lotSize
  });
  
  await notion.createPage("Trade Log", {
    opportunity: opp,
    signal,
    riskCheck,
    result
  });
}
```

### 2. State Machine with Checkpoints

Implement robust state machine with checkpoints for recovery:

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
    state = STATE.RESEARCHING;
    await checkpoint("research", input);
    
    const opp = await researcher.scan(input);
    
    state = STATE.ANALYZING;
    await checkpoint("analyze", opp);
    
    const signal = await strategist.analyze(opp);
    
    state = STATE.VALIDATING;
    await checkpoint("validate", signal);
    
    if (!signal.entry) return;
    
    const riskCheck = await riskManager.validate(signal);
    
    state = STATE.EXECUTING;
    await checkpoint("execute", { signal, riskCheck });
    
    if (!riskCheck.approved) {
      state = STATE.IDLE;
      return;
    }
    
    const result = await executor.execute({ ...signal, ...riskCheck });
    
    state = STATE.COMPLETE;
    await checkpoint("complete", result);
    
  } catch (error) {
    state = STATE.HALTED;
    await checkpoint("error", { error, state });
    await slack.alert({ channel: "#trading-alerts", text: `Pipeline halt: ${error.message}` });
  }
}
```

### 3. Circuit Breaker Implementation

Implement circuit breakers to halt trading on anomalies:

```typescript
let consecutiveLosses = 0;
let maxConsecutiveLosses = 3;

if (consecutiveLosses >= maxConsecutiveLosses) {
  state = STATE.HALTED;
  await slack.alert({ channel: "#trading-alerts", text: "Circuit breaker triggered" });
  return;
}
```

### 4. Portfolio Exposure Monitoring

Monitor portfolio exposure and halt on breach:

```typescript
const totalExposure = positions.reduce((sum, p) => sum + p.lots, 0);
const maxExposure = 10;

if (totalExposure > maxExposure) {
  state = STATE.HALTED;
  await slack.alert({ channel: "#trading-alerts", text: "Max exposure exceeded" });
  return;
}
```

### 5. Incident Handling and Recovery

Handle incidents with proper notification and recovery:

```typescript
async function handleIncident(error, state) {
  await checkpoint("incident", { error, state });
  await slack.alert({ channel: "#trading-alerts", text: `Incident: ${error.message}` });
  
  if (shouldHalt(state)) {
    await haltTrading();
    return true;
  }
  
  return false;
}
```

## When NOT to Use

- Task is about portfolio management, not trading (use portfolio skills)
- Task is about financial analysis (use analysis skills)
- You need to analyze trade results (use analytics skills)
- Task is about risk management (use risk skills)
- You don't have trading capital
- Task requires financial advice (consult advisors)


## Red Flags

- **Pipeline state machine enters HALTED state**: Anomaly detected; investigate cause and review log for error details before resuming
- **Circuit breaker triggers unexpectedly**: Review recent trade performance and market conditions; may indicate market regime change
- **Multiple consecutive losses exceeding threshold**: Strategy may be unprofitable in current conditions; enter review mode
- **Portfoli exposure exceeds maximum**: Risk manager failed to prevent overexposure; investigate and implement stricter limits
- **Notion trade log creation failing**: API connectivity issue or rate limiting; implement retry logic with exponential backoff
- **Slack notifications not appearing**: Bot token may be expired or channel permissions changed; verify configuration
- **Orchestration loop runs without progress**: Implementation may have infinite loop or missing termination conditions; implement maximum iterations

## Verification

Verification covers pipeline state transitions, circuit breaker triggers, notification delivery, and safety halt conditions.


### Pipeline Verification
- [ ] All five team members (Researcher, Strategist, Risk Manager, Executor, Orchestrator) properly integrated
- [ ] State machine transitions correctly through all states (IDLE → RESEARCHING → ANALYZING → VALIDATING → EXECUTING → COMPLETE)
- [ ] Checkpoints saved at each state transition for recovery capability

### State Management Verification
- [ ] State persisted correctly and survives restarts
- [ ] Checkpoints contain all necessary information for resumption
- [ ] Error handling properly transitions state to HALTED on failures

### Circuit Breaker Verification
- [ ] Consecutive loss threshold properly configured and triggered
- [ ] Portfolio exposure maximum enforced and circuits break on breach
- [ ] Circuit breakers properly log to Notion for audit trail

### Notification Verification
- [ ] Slack alerts sent to correct channels (#trading-alerts, #trades)
- [ ] Notion trade log entries created with complete trade data
- [ ] Notifications include all relevant trade parameters (symbol, side, size, price, PnL)

### Safety Verification
- [ ] Trading halts properly on all defined abnormal conditions
- [ ] Safe abort procedures execute before positions are opened
- [ ] Risk checks prevent trades that violate risk parameters
