---
name: slack-notifier
description: Slack Notifier. Use when working with slack notifier in integrations domain.
domain: integrations
tags:
- api
- integrations
- notifier
- slack
- third-party
---
## When to Use

**Trigger phrases:**
- "slack notifier"
- "Help me with slack notifier"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

## Slack Notifier

Send Slack notifications

### Usage

```
/slack-notifier <task>
```

### Features

- Automated execution
- Error handling
- Result validation

## How to Use

1. Set up an incoming webhook or bot token for your Slack workspace
2. Configure notification rules (events, severity levels, channels)
3. Format messages with Block Kit for readability
4. Implement rate limiting to avoid notification fatigue

## Notification Templates

```python
import requests

def notify_deploy(service, version, status):
    color = "#36a64f" if status == "success" else "#ff0000"
    requests.post(WEBHOOK_URL, json={
        "attachments": [{
            "color": color,
            "title": f"Deploy: {service} v{version}",
            "fields": [
                {"title": "Status", "value": status, "short": True},
                {"title": "Environment", "value": "production", "short": True}
            ]
        }]
    })

def notify_alert(message, severity="warning"):
    requests.post(WEBHOOK_URL, json={
        "text": f"*{severity.upper()}*: {message}"
    })
```

## Common Patterns

- Use threads to group related notifications
- Deduplicate alerts to prevent notification storms
- Route different severity levels to different channels
- Include actionable links in notification messages

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
