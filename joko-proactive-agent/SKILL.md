---
name: joko-proactive-agent
description: Use when transforming AI agents from task-followers into proactive partners that anticipate needs and continuously improve.
---

# Proactive Agent

## Overview
A proactive, self-improving architecture for AI agents. Transforms agents from task-followers into proactive partners that anticipate needs and continuously improve.

## When to Use
- When building self-improving agent systems
- When implementing autonomous cron jobs
- When adding memory and persistence layers
- When you want agents that anticipate needs

## When NOT to Use
- For simple, stateless task execution
- When you need fully deterministic behavior

## Quick Reference

**Key Features:**
- WAL Protocol - Write-Ahead Logging for corrections
- Working Buffer - Survive context truncation
- Unified Search - Search all sources before saying "I don't know"
- Security Hardening - Safe skill installation

## What's New (v3.0+)
- **WAL Protocol** — Write-Ahead Logging for corrections, decisions, details
- **Working Buffer** — Survive the danger zone between memory flush and compaction
- **Compaction Recovery** — Step-by-step recovery when context gets truncated
- **Unified Search** — Search all sources before saying "I don't know"
- **Security Hardening** — Skill installation vetting, agent network warnings

## Common Mistakes
- Not implementing persistence layers
- Skipping security vetting for skills
- Not using the WAL protocol

## Core Principles
- **Relentless Resourcefulness** — Try 10 approaches before asking for help
- **Self-Improvement Guardrails** — Safe evolution with protocols
- **Verify Implementation** — Check the mechanism, not just the text
