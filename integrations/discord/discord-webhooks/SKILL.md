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
## Discord Webhooks

Send Discord webhooks

### Usage

```
/discord-webhooks <task>
```

### Features

- Automated execution
- Error handling
- Result validation

## How to Use

1. Create a webhook in Discord channel settings (Integrations > Webhooks)
2. Copy the webhook URL for use in automation scripts
3. Send messages via POST request with JSON payload
4. Use embeds for rich formatting (colors, fields, images)

## Webhook Payload Examples

```bash
# Simple message
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

## Common Patterns

- Use environment variables for webhook URLs (never hardcode)
- Batch multiple messages to respect rate limits (5 per 2 seconds)
- Use thread_id parameter to post in forum channels
- Rotate webhook URLs periodically for security

## When NOT to Use

- When the integration requires admin-level permissions on the target platform
- When the data exchange involves regulated information requiring encryption
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Integration does not handle API errors or service unavailability
- Agent does not verify data consistency across connected systems
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] API errors and service outages are handled with appropriate retry logic
- [ ] Data consistency is verified across all connected systems
- [ ] All required outputs generated
- [ ] Success criteria met

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
