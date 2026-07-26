---
name: discord-webhooks
description: Use when discord Webhooks — HTTP push notifications, rich embeds, custom usernames/avatars, file attachments, channel routing. See parent skill for all Discord automation capabilities.
domain: integrations
tags:
- api
- discord
- integrations
- webhook
version: 1.0.0
---

# Discord Webhooks

## Quick Reference

The Discord webhooks sub-skill covers HTTP push notifications — the simplest way to get data into Discord without a full bot. Create once, POST forever. This layers on the parent [Discord Automation Hub](../SKILL.md) which covers bots and the full automation ecosystem.

**Use this when** you need to push alerts, deploy notifications, or formatted messages from any system that can make HTTP requests.

## Overview

Webhooks are Discord's simplest integration pattern: an HTTP URL that accepts JSON payloads. No WebSocket connection, no event handlers, no always-on process. Best for:
- **CI/CD notifications** — deploy success/failure alerts
- **Monitoring alerts** — server health, uptime, error rate spikes
- **Crypto/trading signals** — price alerts, stop-loss triggers
- **Cross-platform bridges** — GitHub/GitLab/PagerDuty → Discord forwarding

Key differences from a bot: webhooks cannot read messages, manage roles, respond interactively, or handle events. They are write-only by design. The parent skill's `discord-notify.sh`, `python-notify.py`, and `alert-pipeline.sh` are the canonical templates.

## Quick Start

### 1. Get a Webhook URL
```bash
# In Discord: Channel Settings → Integrations → Webhooks → New Webhook
# Or create via API:
curl -X POST "https://discord.com/api/v10/channels/CHANNEL_ID/webhooks" \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Deploy Bot"}'
```

### 2. Send a Simple Message
```bash
curl -X POST "$DISCORD_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello from webhook!"}'
```

### 3. Send a Rich Embed
```bash
curl -X POST "$DISCORD_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "Deploy Bot",
    "embeds": [{
      "title": "Deploy Complete",
      "description": "v2.3.1 pushed to production",
      "color": 3066993,
      "timestamp": "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'"
    }]
  }'
```

## Code Snippet: Python Webhook Sender

```python
import os, requests
from datetime import datetime

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

def send_embed(title, description, color=3066993, fields=None):
    """Send a rich embed via Discord webhook. Returns HTTP status."""
    embed = {
        "title": title,
        "description": description,
        "color": color,  # 3066993=green, 15158332=red, 15105570=yellow
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    if fields:
        embed["fields"] = fields
    resp = requests.post(WEBHOOK_URL, json={"embeds": [embed]})
    return resp.status_code

# Example: deploy notification
send_embed("Deployment Complete", "v2.3.1 deployed to production", 3066993, [
    {"name": "Branch", "value": "main", "inline": True},
    {"name": "Duration", "value": "2m 34s", "inline": True},
])
```

See the parent for the complete embed builder (`build_embed()`) and severity-routing alert pipeline.

## Verification Checklist

- [ ] Webhook URL is kept secret (anyone with the URL can POST to the channel)
- [ ] Embeds render with correct colors, fields, timestamps, and footers
- [ ] Rate limits respected: 5 requests per 2 seconds per webhook URL
- [ ] File attachments work via multipart/form-data (up to 25MB, 8MB without boost)
- [ ] Custom username and avatar_url display correctly in the channel

## When to Use

Use when discord Webhooks — HTTP push notifications, rich embeds, custom usernames/avatars, file attachments, channel routing. See parent skill for all Discord automation capabilities.

## Workflow

Execute these steps sequentially:

### 1. Get a Webhook URL
```bash
# In Discord: Channel Settings → Integrations → Webhooks → New Webhook
# Or create via API:
curl -X POST "https://discord.com/api/v10/channels/CHANNEL_ID/webhooks" \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Deploy Bot"}'
```

### 2. Send a Simple Message
```bash
curl -X POST "$DISCORD_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello from webhook!"}'
```

### 3. Send a Rich Embed
```bash
curl -X POST "$DISCORD_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "Deploy Bot",
    "embeds": [{
      "title": "Deploy Complete",
      "description": "v2.3.1 pushed to production",
      "color": 3066993,
      "timestamp": "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'"
    }]
  }'
```

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll build a full bot just to send notifications" | Webhooks are 3 lines of curl vs a multi-file bot project. Start with a webhook, only add a bot when you need two-way interaction. |
| "Polling is simpler than webhooks" | Webhooks are push — zero polling overhead. The source system POSTs on state change, no cron, no wasted API calls. |
| "Plain text messages are good enough" | Rich embeds with color-coded severity, fields, and timestamps increase signal-to-noise ratio. Color alone makes critical alerts instantly scannable. |
