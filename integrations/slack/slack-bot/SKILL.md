---
name: slack-bot
description: Use when slack Bot — Event-driven messaging, app_mention handlers, interactive components, user lookup, channel management. See parent skill for all Slack automation capabilities.
domain: integrations
tags:
- api
- bot
- integrations
- slack
version: 1.0.0
---

# Slack Bot — Quick Reference

**Role:** The Slack Bot sub-skill covers event-driven messaging — listening for `app_mention`, `message` events, responding to users, managing channels, looking up users, and building interactive components (buttons, modals, dropdowns). Unlike the Notifier (webhook-only) or Slash Commands (triggered by `/command`), the Bot operates as a persistent socket-mode presence that reacts to events in real time.

## Quick Start

### 1. Socket-Mode Bot (Python)
Listen for mentions and respond without a public HTTPS endpoint:

```python
import os
from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient

bot_token = os.environ["SLACK_BOT_TOKEN"]
app_token = os.environ["SLACK_APP_TOKEN"]

client = WebClient(token=bot_token)
socket_client = SocketModeClient(app_token=app_token, web_client=client)

def handle_events(client, req):
    if req.type != "events_api":
        return
    event = req.payload.get("event", {})
    if event.get("type") == "app_mention":
        client.web_client.chat_postMessage(channel=event["channel"], text=f"Hey <@{event['user']}>! How can I help?")

socket_client.socket_mode_request_listeners.append(handle_events)
socket_client.connect()
import time
while True: time.sleep(1)
```

### 2. User Lookup and Channel History
Resolve user info and read recent messages programmatically:

```python
user_info = client.users_info(user="U0123456")  # returns email, display name, timezone, etc.
history = client.conversations_history(channel="C0123456", limit=20)
members = client.conversations_members(channel="C0123456")  # list of user IDs
```

### 3. Interactive Components — Button Handlers
Buttons and modals require an interactive endpoint (or Socket Mode). Handle payloads:

```python
@app.route("/slack/actions", methods=["POST"])
def handle_actions():
    payload = json.loads(request.form["payload"])
    action = payload["actions"][0]
    user = payload["user"]["id"]
    channel = payload["channel"]["id"]
    # action["value"] contains the button's custom payload
    client.chat_postMessage(channel=channel, text=f"Action '{action['value']}' by <@{user}>")
    return "", 200
```

## One Focused Code Snippet — Multi-Channel Message Monitor

```python
def monitor_keywords(channels, keywords, report_channel):
    """Listen in channels and alert when keywords appear."""
    def handler(client, req):
        if req.type != "events_api":
            return
        event = req.payload.get("event", {})
        if event.get("type") != "message" or event.get("channel") not in channels:
            return
        text = event.get("text", "").lower()
        for kw in keywords:
            if kw in text:
                client.web_client.chat_postMessage(
                    channel=report_channel,
                    text=f":eyes: Keyword *{kw}* spotted in <#{event['channel']}> by <@{event['user']}>:\n>{event.get('text','')[:300]}"
                )
                break
```

## Checklist

- [ ] Socket Mode connects without public URL — use for dev/small deployments; production prefers HTTP with `ngrok` or public endpoint
- [ ] `app_mention` events require `subscribes_to_bot_events: ["app_mention"]` in app manifest
- [ ] Interactive components (buttons, modals) send payloads to either Socket Mode or a `/slack/actions` HTTP endpoint
- [ ] Rate limits: Bot token tier allows ~1 msg/sec per channel. Use `chat.postMessage` with `reply_broadcast` for threads
- [ ] Bot scope `channels:history` required to read messages; `users:read` for user info; `reactions:read` for emoji

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Socket Mode is only for toys" | Socket Mode handles real production loads up to ~100 simultaneous connections and removes TLS/cert management. Switch to HTTP when you need fan-out to 1,000+ workspaces. |
| "The bot just needs chat:write" | Without `channels:history` and `users:read`, your bot is blind. You can't respond contextually without reading the channel. |
| "Interactive components are optional" | Buttons and modals turn a bot from a text relay into an interactive tool. Approval workflows, forms, and menus require them. |
|---|---|
| "I'll figure it out as I go" | A structured approach saves time and reduces errors. Follow the workflow in this skill rather than improvising. |
| "I already know this topic" | Familiarity breeds shortcuts. Use the checklist to verify you haven't missed critical steps. |
| "This doesn't apply to my situation" | The patterns here generalize across contexts. Adapt, don't skip — the underlying principles hold. |
| "One more tool will fix it" | Adding complexity rarely solves process gaps. Master the core workflow first. |

## When to Use
Use this skill when working with slack bot.


## Workflow
See the parent skill for authoritative workflow documentation.
