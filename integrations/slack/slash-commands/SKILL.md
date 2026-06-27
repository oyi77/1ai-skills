---
name: slash-commands
description: Slash Commands. Use when working with slash commands in integrations domain.
domain: integrations
tags:
- api
- commands
- integrations
- slash
- third-party
---
# Slash Commands

## When to Use

**Trigger phrases:**
- "slash commands"
- "Help me with slash commands"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

## Overview

Slash Commands connects with external platforms via system connectivity.

## Setup

1. **Authenticate** — Configure API keys, OAuth tokens, or webhooks
2. **Map data** — Define field mappings between systems
3. **Test connection** — Verify connectivity and permissions
4. **Sync data** — Initial data synchronization
5. **Monitor** — Track sync health and error rates

## Configuration

- API credentials (stored securely, never hardcoded)
- Rate limiting and retry policies
- Webhook endpoints for real-time updates
- Data transformation rules

## Error Handling

- Retry with exponential backoff on transient failures
- Alert on auth failures or rate limit hits
- Log all API requests/responses for debugging
- Graceful degradation when external service is down


## Workflow

1. **Understand requirements** — Clarify objectives and scope
2. **Set up tools** — Configure required tools and access
3. **Execute** — Perform the core operations
4. **Validate** — Verify results meet quality standards
5. **Document** — Record findings and decisions

