---
name: slash-commands
description: Use when slack Slash Commands — Custom /command handlers, parameter parsing, ephemeral responses, modals, interactive workflows. See parent skill for all Slack automation capabilities.
domain: integrations
tags:
- api
- commands
- integrations
- slack
version: 1.0.0
---

# Slash Commands — Quick Reference

**Role:** Slash Commands let users trigger bot actions by typing `/command` in any Slack channel or DM. The sub-skill covers registering custom commands, parsing parameters, sending ephemeral vs in-channel responses, opening modals, and chaining commands with interactive components. Commands run in Socket Mode or via HTTP endpoint and must respond within 3 seconds.

## Quick Start

### 1. Register a Command (Bolt.js)
The `/standup` command collects daily standup reports:

```javascript
const { App } = require('@slack/bolt');
const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  signingSecret: process.env.SLACK_SIGNING_SECRET,
  socketMode: true,
  appToken: process.env.SLACK_APP_TOKEN,
});

app.command('/standup', async ({ command, ack, respond, client }) => {
  await ack(); // MUST ack within 3 seconds
  const parts = command.text.match(/(\w+)\s+"([^"]+)"/g) || [];
  const params = {};
  for (const p of parts) {
    const [key, ...val] = p.split(/\s+/);
    params[key.toLowerCase()] = val.join(' ').replace(/^"|"$/g, '');
  }
  await respond({ response_type: 'ephemeral', text: 'Standup recorded! :white_check_mark:' });
  await client.chat.postMessage({
    channel: '#standup-logs',
    text: `*Standup from <@${command.user_id}>\n> Yesterday: ${params.yesterday || 'N/A'}`,
  });
});
```

### 2. Ephemeral vs In-Channel Responses
Control who sees the command response:

```python
# Ephemeral — only the user who typed the command sees this
respond({"response_type": "ephemeral", "text": "Only you can see this"})

# In_channel — everyone in the channel sees the response
respond({"response_type": "in_channel", "text": "Everyone sees this"})
```

Use ephemeral for confirmations, errors, and help text. Use in_channel for broadcast-worthy results.

### 3. Open a Modal from a Command
For complex input, defer to a modal dialog:

```javascript
app.command('/feedback', async ({ ack, client, body }) => {
  await ack();
  await client.views.open({
    trigger_id: body.trigger_id,
    view: {
      type: 'modal',
      callback_id: 'feedback_submit',
      title: { type: 'plain_text', text: 'Submit Feedback' },
      blocks: [
        { type: 'input', block_id: 'rating', element: { type: 'static_select', placeholder: { type: 'plain_text', text: 'Rating' }, options: [{ text: { type: 'plain_text', text: '👍' }, value: 'good' }] } },
        { type: 'input', block_id: 'comment', element: { type: 'plain_text_input', multiline: true } },
      ],
      submit: { type: 'plain_text', text: 'Submit' },
    }
  });
});
```

## One Focused Code Snippet — Command Parameter Parser

```python
import re
def parse_slash_command(text):
    """Parse `/command key:"value with spaces" key2:value2` into a dict."""
    params = {}
    pairs = re.findall(r'(\w+):("(?:[^"]*)"|(?:[^\s]+))', text)
    for key, val in pairs:
        params[key.lower()] = val.strip('"')
    return params

# Example: /deploy v2.1.0 env:production
# parse_slash_command("v2.1.0 env:production") → {"0": "v2.1.0", "env": "production"}
```

## Checklist

- [ ] `ack()` called within 3 seconds of command invocation — Slack drops unresponsive commands
- [ ] Slash command registered in Slack API dashboard → Slash Commands → Create New Command
- [ ] Ephemeral responses for individual confirmations; in_channel for public displays
- [ ] Modals use `views.open` with `trigger_id` from the command payload — trigger_id expires in 3 seconds
- [ ] `commands` scope enabled in OAuth scopes. Reinstall app after adding scope

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Users can just type free-form text" | Structured parameters (`/standup yesterday:"Fixed bug" today:"Auth work"`) are parseable. Free text requires NLP and breaks silently. |
| "3 seconds is plenty of time" | The 3-second ack is for the initial response. Complex processing after ack is fine — use `respond()` for delayed follow-ups. Always ack immediately. |
| "Slash commands don't need Socket Mode" | Socket Mode avoids the HTTPS endpoint + certificate requirement. For a single-workspace bot, Socket Mode is simpler. HTTP mode matters only for multi-workspace distribution. |
|---|---|
| "I'll figure it out as I go" | A structured approach saves time and reduces errors. Follow the workflow in this skill rather than improvising. |
| "I already know this topic" | Familiarity breeds shortcuts. Use the checklist to verify you haven't missed critical steps. |
| "This doesn't apply to my situation" | The patterns here generalize across contexts. Adapt, don't skip — the underlying principles hold. |
| "One more tool will fix it" | Adding complexity rarely solves process gaps. Master the core workflow first. |

## When to Use
Use this skill when working with slash commands.


## Workflow
See the parent skill for authoritative workflow documentation.
