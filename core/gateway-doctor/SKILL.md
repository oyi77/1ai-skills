---
name: gateway-doctor
description: Diagnose and fix MCP gateway routing issues, health checks, and server connectivity problems.
domain: core
tags:
- doctor
- gateway
- infrastructure
- memory
- self-improvement
persona:
  name: Brendan Gregg
  title: The Systems Performance Expert - Master of Diagnostics
  expertise:
  - System Diagnostics
  - Performance Analysis
  - Observability
  - Troubleshooting
  philosophy: Performance issues are just bugs you haven't found yet.
  credentials:
  - Senior Performance Engineer at Netflix
  - Authored 'Systems Performance' book
  - Created DTrace tools
  principles:
  - Measure everything
  - Find the bottleneck
  - Optimize the critical path
  - Monitor continuously
---
# Gateway Doctor

## When to Use

- Periodic health checks (1 min interval)
- User reports lag
- After system sleep/resume
- Gateway unresponsive

## Overview

Gateway Doctor is a foundational core infrastructure skill that provides system foundation capabilities for the agent ecosystem.

## Architecture

- **Input layer** — Receives and validates incoming requests
- **Processing layer** — Core logic for system foundation
- **Output layer** — Formats and delivers results
- **State management** — Maintains context across invocations

## Configuration

- Set up required environment variables and paths
- Configure logging level and output format
- Define resource limits (memory, time, API calls)
- Enable/disable features via configuration flags

## Integration

- Exposes standard interfaces for other skills to consume
- Supports event-driven and request-response patterns
- Compatible with the 1ai-skills hook system
- Logs metrics for the skill performance monitor

