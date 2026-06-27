---
name: kb
description: Query and maintain the knowledge base for project context, decisions, and architecture documentation. Use on
  session start.
domain: core
tags:
- infrastructure
- memory
- self-improvement
persona:
  name: Domain Expert
  title: Master of Kb
  expertise:
  - Core Excellence
  - Best Practices
  - Professional Standards
  philosophy: Excellence is not a skill, it's an attitude.
  credentials:
  - Industry leader
  - Practiced professional
  - Thought leader
  principles:
  - Quality first
  - Continuous improvement
  - Evidence-based
  - Customer focused
---
# Kb

## When to Use

Use this skill when:
- Searching company knowledge (strategies, playbooks, finance, trading, marketing)
- Reading specific knowledge files (e.g. `areas/finance/cashflow-tracker.md`)
- Writing new or updated knowledge entries to the KB with PARA structure
- Any agent (Vilona, Paijo via Telegram) needs to query or update company context

## Overview

Kb is a foundational core infrastructure skill that provides system foundation capabilities for the agent ecosystem.

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

