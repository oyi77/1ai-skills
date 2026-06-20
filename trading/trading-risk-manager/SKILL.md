---
name: trading-risk-manager
description: Monitor portfolio risk, enforce position limits, and trigger stop-losses. Use when managing exposure across strategies.
domain: trading
tags:
- algorithms
- manager
- markets
- risk
- trading
allowed-tools:
- Bash(trading:*)
- MCP(notion:*)
- MCP(slack:*)
- fs
- network
---

# Trading Risk Manager

## Overview

Calculate position sizes, validate trades against risk rules, and monitor portfolio exposure. The Risk Manager serves as the security checkpoint in the trading pipeline, ensuring no single trade or portfolio action exceeds predefined risk parameters. It implements position sizing algorithms, correlation checks, drawdown monitoring, and exposure caps to protect capital across all trading activities.

## When to Use

- Calculating optimal position sizes based on account risk percentage
- Validating individual trades against risk parameters before execution
- Monitoring total portfolio exposure and diversification
- Implementing drawdown controls and circuit breakers
- Checking trade correlations with existing positions
- Generating risk reports for daily review and compliance
- Setting and enforcing risk limits across multiple accounts or strategies

## The Process

The risk pipeline calculates position sizes, validates trades, monitors exposure, enforces drawdown limits, and generates risk reports.


### 1. Calculate Position Size

Use standard risk-based position sizing formula:

```typescript
const accountBalance = 10000;
const riskPercent = 0.02; // 2% risk
const stopLossPips = 50;
const pipValue = 10; // $10 per pip for XAUUSD

const riskAmount = accountBalance * riskPercent;
const lotSize = riskAmount / (stopLossPips * pipValue);

console.log(`Recommended lot size: ${lotSize.toFixed(2)}`);
```

### 2. Validate Trade Against Risk Rules

Comprehensive trade validation before execution:

```typescript
const positions = await broker.getPositions();

// Check exposure cap
const totalExposure = positions.reduce((sum, p) => sum + p.lots, 0);
const maxExposure = 10;

if (totalExposure + newTrade.lots > maxExposure) {
  return { approved: false, reason: "Max exposure exceeded" };
}

// Check correlation
const correlation = await checkCorrelation(newTrade, positions);
if (correlation > 0.7) {
  return { approved: false, reason: "High correlation with existing positions" };
}

// Check drawdown
const drawdown = await calculateDrawdown();
if (drawdown > 0.10) {
  return { approved: false, reason: "Max drawdown exceeded" };
}

return { approved: true };
```

### 3. Monitor Portfolio Exposure

Track and report portfolio exposure metrics:

```typescript
const positions = await broker.getPositions();

const metrics = {
  totalLots: positions.reduce((s, p) => s + p.lots, 0),
  longLots: positions.filter(p => p.side === "buy").reduce((s, p) => s + p.lots, 0),
  shortLots: positions.filter(p => p.side === "sell").reduce((s, p) => s + p.lots, 0),
  maxLongShortExposure: Math.abs(
    positions.filter(p => p.side === "buy").reduce((s, p) => s + p.lots, 0) -
    positions.filter(p => p.side === "sell").reduce((s, p) => s + p.lots, 0)
  )
};

console.table(metrics);
```

### 4. Implement Drawdown Controls

Monitor and control drawdown across the portfolio:

```typescript
const maxDrawdownPercent = 0.10; // 10%
const currentDrawdown = calculateDrawdown();

if (currentDrawdown > maxDrawdownPercent) {
  return { approved: false, reason: "Max drawdown exceeded" };
}

// Halt all new trades if drawdown approaching limit
if (currentDrawdown > maxDrawdownPercent * 0.8) {
  await slack.alert({ channel: "#trading-alerts", text: "Drawdown warning" });
}
```

### 5. Generate Risk Reports

Create daily risk reports for review:

```typescript
const dailyRiskReport = {
  date: new Date().toISOString(),
  accountBalance: 10000,
  equity: 9500,
  margin: 2000,
  freeMargin: 7500,
  marginLevel: 475,
  totalDrawdown: 0.05,
  openPositions: 3,
  totalExposure: 2.5,
  maxDrawdown: 0.08
};

await notion.createPage("Risk Report", dailyRiskReport);
```

## When NOT to Use

- Task is about portfolio management, not trading (use portfolio skills)
- Task is about financial analysis (use analysis skills)
- You need to analyze trade results (use analytics skills)
- Task is about risk management (use risk skills)
- You don't have trading capital
- Task requires financial advice (consult advisors)


## Red Flags

- **Position size exceeds risk parameters**: Risk manager failed or parameters incorrect; reject trade and investigate why parameters allowed excessive sizing
- **Portfolio drawdown approaching or exceeding limit**: Strategy may be underperforming in current market regime; consider pausing trading or adjusting parameters
- **Correlation check detects high correlation (>0.7)**: Portfolio lacks diversification; reject additional similar trades or reduce existing positions
- **Total exposure exceeds maximum set for account**: Position limits not being enforced; implement strict exposure caps across all incoming trades
- **Margin level drops below maintenance requirements**: Leverage too high; issue margin call or automatically reduce exposure
- **Risk calculations return zero or NaN**: Data quality issue or calculation error; verify inputs and implementation
- **Multiple position types from same strategy**: Strategy concentration risk; implement strategy-level exposure limits

## Verification

Verification covers position sizing accuracy, trade validation consistency, exposure tracking, drawdown controls, and notification delivery.


### Position Sizing Verification
- [ ] Lot size calculated correctly using risk formula
- [ ] Position size respects account balance and risk percentage
- [ ] Pip value correctly applied for different currency pairs
- [ ] Results match manual calculations for spot check

### Trade Validation Verification
- [ ] All risk checks applied consistently to incoming trades
- [ ] Trade approvals match expected risk profile
- [ ] Rejected trades logged with proper reasons
- [ ] Risk parameters configurable without code changes

### Exposure Monitoring Verification
- [ ] Total exposure tracked across all positions
- [ ] Long/short exposure tracked separately
- [ ] Net exposure calculated correctly
- [ ] Exposure limits enforced with appropriate alerts

### Drawdown Control Verification
- [ ] Drawdown calculated using correct formula (equity vs balance)
- [ ] Drawdown checks implemented before new trades
- [ ] Halt conditions properly trigger at set thresholds
- [ ] Drawdown metrics logged to Notion for audit

### Integration Verification
- [ ] Slack notifications sent on risk events
- [ ] Notion risk reports created on schedule
- [ ] Trade validation database records updated
- [ ] Risk reports include all required metrics for review
