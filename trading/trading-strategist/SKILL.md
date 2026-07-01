---
name: trading-strategist
description: Design and backtest trading strategies using technical indicators, fundamental analysis, and statistical models.
domain: trading
tags:
- algorithms
- markets
- strategist
- trading
allowed-tools:
- Bash(trading:*)
- MCP(notion:*)
- fs
- network
---

# Trading Strategist

## Overview

Build and optimize trading strategies with clear entry/exit rules and risk parameters. The Strategist serves as the design arm of the trading team, responsible for creating systematic trading strategies that can be consistently replicated and optimized. It focuses on turning market insights into executable strategies with defined rules, parameters, and risk controls that can be backtested and deployed.

## When to Use
**Trigger phrases:**
- "trading strategist"
- "Design and backtest trading strategies using technical indicators, fundamental a"


- Creating new trading strategies based on market analysis or hypotheses
- Defining precise entry and exit conditions for strategy trading
- Optimizing strategy parameters using historical backtesting
- Testing strategies across different market regimes (bull, bear, sideways)
- Documenting strategy rules and parameters in Notion
- Generating strategy performance metrics and Sharpe ratios
- Maintaining strategy version history and change tracking

## The Process

The strategy design pipeline defines entry/exit rules, runs scenario analysis, optimizes parameters, and documents strategies in Notion.


### 1. Define Entry Rules

Create comprehensive entry rule sets:

```typescript
const entryRules = {
  trend: "price > SMA(20)",
  momentum: "RSI(14) < 30",
  volatility: "ATR(14) < 20",
  volume: "volume > SMA(20, volume) * 1.5"
};

const strategy = {
  name: "RSI Reversal",
  entry: entryRules,
  exit: {
    stopLoss: "entry - 2 * ATR(14)",
    takeProfit: "entry + 3 * ATR(14)"
  },
  riskPerTrade: 0.02
};

await notion.createPage("Trading Strategies", strategy);
```

### 2. Scenario Analysis

Test strategy performance across different market conditions:

```typescript
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

### 3. Parameter Optimization

Systematically optimize strategy parameters:

```typescript
const params = {
  rsiPeriod: [10, 14, 20],
  rsiOverbought: [60, 70, 80],
  rsiOversold: [20, 30, 40]
};

const results = [];
for (const p of gridSearch(params)) {
  const result = await backtest(strategy.set(p), data);
  results.push({ params: p, sharpe: result.sharpe });
}

const best = results.sort((a, b) => b.sharpe - a.sharpe)[0];
console.log(`Best params: ${JSON.stringify(best.params)}`);
```

### 4. Generate Strategy Report

Create comprehensive strategy documentation:

```typescript
const strategyReport = {
  name: "RSI Reversal Strategy",
  description: "Mean reversion strategy for XAUUSD",
  entryRules: entryRules,
  exitRules: strategy.exit,
  parameters: {
    rsiPeriod: 14,
    overbought: 70,
    oversold: 30,
    atrPeriod: 14
  },
  backtestResults: {
    sharpe: 1.2,
    winRate: 0.60,
    profitFactor: 1.8
  },
  riskControls: {
    maxDrawdown: 0.15,
    riskPerTrade: 0.02
  }
};

await notion.createPage("Strategy Documentation", strategyReport);
```

### 5. Strategy Backtest

Run comprehensive backtest with full metrics:

```typescript
const backtestResult = await backtest(strategy, historicalData, {
  initialBalance: 10000,
  commission: 0.0001,
  slippage: 0.5
});

console.table({
  totalTrades: backtestResult.totalTrades,
  winRate: backtestResult.winRate,
  profitFactor: backtestResult.profitFactor,
  sharpe: backtestResult.sharpe,
  maxDrawdown: backtestResult.maxDrawdown
});
```

## When NOT to Use

- Task is about portfolio management, not trading (use portfolio skills)
- Task is about financial analysis (use analysis skills)
- You need to analyze trade results (use analytics skills)
- Task is about risk management (use risk skills)
- You don't have trading capital
- Task requires financial advice (consult advisors)


## Red Flags

- **Strategy parameters produce overfitting**: Strategy too closely tuned to specific historical data; test on out-of-sample data and reduce parameter complexity
- **Entry rules too complex or contradictory**: Strategy may be too complicated to execute reliably; simplify to essential rules
- **Backtest results inconsistent across scenarios**: Strategy may not be robust; identify scenario-specific weaknesses
- **Sharpe ratio negative or below 0.5**: Strategy not compensating for risk; reject or significantly modify before deployment
- **Profit factor below 1.3**: Strategy not generating sufficient return relative to losses; review risk/reward ratios
- **Drawdown exceeds acceptable threshold (>20%)**: Position sizing or risk management may need adjustment; reduce position sizes or tighten stop losses
- **Strategy parameters frequently need adjustment**: Market regime dependency too high; implement dynamic parameter adaptation

## Verification

Verification covers strategy design clarity, backtest accuracy, optimization robustness, scenario coverage, and documentation completeness.


### Strategy Design Verification
- [ ] Entry rules clearly defined and executable
- [ ] Exit rules properly implemented with stop loss and take profit
- [ ] Parameters quantified with specific values
- [ ] Risk controls documented and configured

### Backtest Verification
- [ ] Historical data quality validated for backtest period
- [ ] Backtest includes realistic slippage and commission
- [ ] All trades in backtest execute as expected
- [ ] Metrics match expected performance ranges

### Optimization Verification
- [ ] Grid search covers reasonable parameter range
- [ ] Optimization tested on out-of-sample data
- [ ] Best parameters validated with walk-forward analysis
- [ ] No data snooping bias in optimization process

### Scenario Testing Verification
- [ ] Strategy tested across bull, bear, and sideways markets
- [ ] Scenario results documented and compared
- [ ] Strategy weaknesses identified for specific scenarios
- [ ] Adjustments made for scenario-specific performance

### Documentation Verification
- [ ] Notion strategy page includes all rules and parameters
- [ ] Backtest results documented with full metrics
- [ ] Risk controls clearly specified
- [ ] Documentation reviewed and approved by trading team

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I will cut losses later" | Later never comes. Set stop-losses before entering any trade. |
| "This time is different" | It never is. Follow your strategy, not your emotions. |
| "I do not need to journal" | Journaling reveals patterns in your behavior. Track every trade. |