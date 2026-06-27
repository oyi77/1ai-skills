---
name: github-pr
description: Create PR via CLI. Use when performing github pr tasks in integrations workflows.
domain: integrations
tags:
- api
- github
- integrations
- third-party
- workflow
---
# Github Pr

## When to Use

**Trigger phrases:**
- "github pr"
- "Help me with github pr"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

gh pr create --title "feat: add user auth" --body "## Summary
- Added JWT-based auth
- Protected /api routes"

# Review and merge
gh pr review 123 --approve
gh pr merge 123 --squash
```

## Overview

Github Pr connects with external platforms via system connectivity.

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

