---
name: trading-team
description: Multi-agent trading team — Orchestrator coordinates Researcher, Strategist, Risk Manager, and Executor agents for comprehensive trade planning.
permissions:
  - fs
  - network
---

# Trading Team

Multi-agent trading team where an Orchestrator coordinates specialized agents for comprehensive trade planning and execution.

## Agents

| Agent | Role | Responsibility |
|-------|------|---------------|
| **Orchestrator** | Coordinator | Routes tasks, manages workflow, aggregates outputs |
| **Researcher** | Market Intel | Gathers data, news, correlations, macro context |
| **Strategist** | Trade Planning | Identifies setups, entry/exit levels, strategy selection |
| **Risk Manager** | Risk Control | Position sizing, exposure limits, drawdown monitoring |
| **Executor** | Trade Execution | Order placement, fill monitoring, slippage tracking |

## Workflow

1. Orchestrator receives trade request or market signal
2. Researcher gathers relevant market data and context
3. Strategist proposes trade setup with levels
4. Risk Manager validates sizing and exposure
5. Executor places and monitors the trade

## When to Use

- Pre-trade analysis requiring multiple perspectives
- Full trade lifecycle from research to execution
- Complex multi-asset or multi-timeframe analysis
- When you need coordinated risk-aware trade planning
