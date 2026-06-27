---
name: github-issues
description: Create an issue. Use when performing github issues tasks in integrations workflows.
domain: integrations
tags:
- api
- github
- integrations
- issues
- third-party
- workflow
---
# Github Issues

## When to Use

**Trigger phrases:**
- "github issues"
- "Help me with github issues"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

curl -X POST "https://api.github.com/repos/OWNER/REPO/issues" \
  -H "Authorization: token $GITHUB_TOKEN" \
  -d '{"title": "Bug: login fails", "labels": ["bug"]}'

# Add a comment
curl -X POST "https://api.github.com/repos/OWNER/REPO/issues/123/comments" \
  -H "Authorization: token $GITHUB_TOKEN" \
  -d '{"body": "Investigating this now."}'
```

## Overview

Github Issues connects with external platforms via system connectivity.

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

