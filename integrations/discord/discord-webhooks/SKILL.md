---
name: discord-webhooks
description: Simple message. Use when working with discord webhooks in integrations domain.
domain: integrations
tags:
- api
- discord
- integrations
- third-party
- webhook
- webhooks
---
# Discord Webhooks

## When to Use

**Trigger phrases:**
- "discord webhooks"
- "Help me with discord webhooks"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

curl -X POST "$WEBHOOK_URL" -H "Content-Type: application/json" -d '{
  "content": "Deployment complete: v2.3.1",
  "username": "CI/CD Bot"
}'

# Rich embed
curl -X POST "$WEBHOOK_URL" -H "Content-Type: application/json" -d '{
  "embeds": [{
    "title": "Build Status",
    "color": 3066993,
    "fields": [
      {"name": "Branch", "value": "main", "inline": true},
      {"name": "Status", "value": "Passed", "inline": true}
    ]
  }]'
}
```


## When NOT to Use

- When the platform has a native solution that works
- For one-time data imports (use CSV/JSON instead)
- When the API is deprecated or being sunset


## Overview

Discord Webhooks connects with external platforms via system connectivity.

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

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I will handle auth later" | Retrofitting auth is 10x harder. Build it from day one. |
| "APIs do not change" | APIs change. Version your integrations and handle deprecations. |
| "Webhooks are optional" | Without webhooks, you miss real-time events. They are essential. |


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run discord webhooks workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings