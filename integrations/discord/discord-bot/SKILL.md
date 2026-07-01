---
name: discord-bot
description: Discord Bot. Use when performing discord bot tasks in integrations workflows.
domain: integrations
tags:
- api
- bot
- discord
- integrations
- third-party
- workflow
---
# Discord Bot

## When to Use

**Trigger phrases:**
- "discord bot"
- "Help me with discord bot"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


## When NOT to Use

- When the platform has a native solution that works
- For one-time data imports (use CSV/JSON instead)
- When the API is deprecated or being sunset


## Overview

Discord Bot connects with external platforms via system connectivity.

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

```python
# Example: API integration with retry
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
async def api_call(url: str, payload: dict):
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()
```

1. **Understand requirements** — Clarify objectives and scope
2. **Set up tools** — Configure required tools and access
3. **Execute** — Perform the core operations
4. **Validate** — Verify results meet quality standards
5. **Document** — Record findings and decisions

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I will handle auth later" | Retrofitting auth is 10x harder. Build it from day one. |
| "APIs do not change" | APIs change. Version your integrations and handle deprecations. |
| "Webhooks are optional" | Without webhooks, you miss real-time events. They are essential. |


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run discord bot workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings