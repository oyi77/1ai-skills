---
name: slack-notifier
description: Use when slack Notifier — Webhook-based push notifications, rich message formatting (blocks, attachments), channel routing. See parent skill for all Slack automation capabilities.
domain: integrations
tags:
- api
- integrations
- notifications
- slack
version: 1.0.0
---

# Slack Notifier — Quick Reference

**Role:** The Slack Notifier handles outbound push notifications only — send messages to Slack channels via incoming webhooks or the `chat.postMessage` API. No event listening, no slash commands. Ideal for CI/CD alerts, monitoring dashboards, error reporting, and any system-to-Slack broadcast. Uses the simplest auth mode (webhook URL or bot token) with rich formatting via Blocks and attachments.

## Quick Start

### 1. Webhook — Simplest Send (Bash)
No token, no API — just a URL:

```bash
export SLACK_WEBHOOK="https://hooks.slack.com/services/T00/B00/YOUR_ID"
curl -s -X POST "$SLACK_WEBHOOK" -H "Content-Type: application/json" \
  -d '{"text": "Deploy complete :rocket:"}'
```

### 2. Block Message via API (Python)
Richer formatting with headers, sections, and context blocks:

```python
import os, requests

TOKEN = os.environ["SLACK_BOT_TOKEN"]
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def send_rich(channel, title, message, severity="info"):
    colors = {"info": "#36a64f", "warning": "#ffcc00", "error": "#ff0000"}
    blocks = [
        {"type": "header", "text": {"type": "plain_text", "text": title}},
        {"type": "section", "text": {"type": "mrkdwn", "text": message}},
        {"type": "context", "elements": [{"type": "mrkdwn", "text": f":signal_strength: {severity}"}]},
    ]
    resp = requests.post("https://slack.com/api/chat.postMessage", headers=HEADERS, json={"channel": channel, "blocks": blocks, "text": title})
    return resp.json()
```

### 3. Multi-Channel Routing by Severity
Route notifications to the right channel based on severity:

```bash
pipeline-notify.sh() {
  local color sev=$1 msg=$2
  case $sev in
    info)    color="#36a64f"; channel="#deployments";;
    warning) color="#ffcc00"; channel="#ops-alerts";;
    error)   color="#ff0000"; channel="#incidents"; channel+="?@here";;
  esac
  curl -s -X POST "$SLACK_WEBHOOK" -H "Content-Type: application/json" \
    -d "{\"channel\":\"$channel\",\"attachments\":[{\"color\":\"$color\",\"text\":\"$msg\"}]}"
}
```

## One Focused Code Snippet — CI/CD Deploy Notifier

```python
def notify_deploy(version, env, duration, status="success"):
    emoji = ":rocket:" if status == "success" else ":x:"
    color = "#36a64f" if status == "success" else "#ff0000"
    blocks = [
        {"type": "header", "text": {"type": "plain_text", "text": f"Deploy {status.upper()} {emoji}"}},
        {"type": "section", "text": {"type": "mrkdwn", "text": f"*Version:* {version}\n*Environment:* {env}\n*Duration:* {duration}"}},
        {"type": "divider"},
    ]
    return send_rich("#deployments", f"Deploy {status}", "", "info")
```

## Checklist

- [ ] Webhook URL kept secret — never committed to git. Load from env var or secret manager
- [ ] Block Kit rendered correctly in Slack client — test each block type (header, section, divider, context, image)
- [ ] Rate limits: Tier 1 (default) = 1 msg/sec. Use chat.postMessage with `reply_broadcast` sparingly
- [ ] Channel name vs ID: `#general` works for public channels; DMs need user ID. Channel IDs are permanent, names can change
- [ ] Error handling: check `resp.json().get("ok")` and log the `error` field. On 429, honor `Retry-After` header

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Plain text messages are good enough" | Block Kit messages (headers, buttons, context) get 3x more engagement. Slack's own research confirms formatted messages are read and acted on faster. |
| "One webhook for everything" | Per-channel webhooks give you channel isolation and per-message formatting. Use separate webhooks per use case. |
| "I'll handle rate limits if they happen" | Slack's tier-1 rate limit is 1 message per second per channel. A CI pipeline reporting 20 services will hit this immediately. Implement queuing with exponential backoff upfront. |
|---|---|
| "I'll figure it out as I go" | A structured approach saves time and reduces errors. Follow the workflow in this skill rather than improvising. |
| "I already know this topic" | Familiarity breeds shortcuts. Use the checklist to verify you haven't missed critical steps. |
| "This doesn't apply to my situation" | The patterns here generalize across contexts. Adapt, don't skip — the underlying principles hold. |
| "One more tool will fix it" | Adding complexity rarely solves process gaps. Master the core workflow first. |

## When to Use
Use this skill when working with slack notifier.


## Workflow
See the parent skill for authoritative workflow documentation.
