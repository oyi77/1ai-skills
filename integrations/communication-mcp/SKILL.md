---
name: communication-mcp
description: MCP servers for team communication. Connect AI agents to Slack, Discord, and Telegram for notifications, messaging, and channel management.
---

# Communication MCP Skill

## Overview

MCP servers enabling AI agents to interact with Slack, Discord, and Telegram. Send notifications, manage messages, and automate communication workflows across platforms.

**Supported Platforms**: Slack, Discord, Telegram  
**Use Cases**: Alerts, notifications, automation, community management

---

## When to Use

- Send notifications to channels
- Automate status updates
- Monitor mentions and messages
- Community management
- Alert systems

---

## Slack MCP Setup

### Installation
```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}",
        "SLACK_TEAM_ID": "${SLACK_TEAM_ID}"
      }
    }
  }
}
```

### Slack Tools
```typescript
// Send message
slack.chat.postMessage({
  channel: "#alerts",
  text: "Deployment completed!",
  blocks: [...]
})

// Search messages
slack.search.messages({
  query: "deployment error",
  count: 10
})

// List channels
slack.conversations.list({
  types: "public_channel,private_channel"
})

// Post to thread
slack.chat.postMessage({
  channel: "C123456",
  text: "Update: Issue resolved",
  thread_ts: "1234567890.123"
})
```

---

## Discord MCP Setup

### Installation
```json
{
  "mcpServers": {
    "discord": {
      "command": "npx",
      "args": ["-y", "mcp-discord"],
      "env": {
        "DISCORD_BOT_TOKEN": "${DISCORD_BOT_TOKEN}"
      }
    }
  }
}
```

### Discord Tools
```typescript
// Send message
discord.sendMessage({
  channel_id: "123456789",
  content: "Server alert!"
})

// Send embed
discord.sendEmbed({
  channel_id: "123456789",
  title: "Deployment Status",
  description: "Successfully deployed!",
  color: 0x00ff00
})

// Get channel messages
discord.getMessages({
  channel_id: "123456789",
  limit: 10
})

// React to message
discord.addReaction({
  channel_id: "123456789",
  message_id: "987654321",
  emoji: "✅"
})
```

---

## Telegram MCP Setup

### Installation
```json
{
  "mcpServers": {
    "telegram": {
      "command": "npx",
      "args": ["-y", "mcp-telegram"],
      "env": {
        "TELEGRAM_BOT_TOKEN": "${TELEGRAM_BOT_TOKEN}"
      }
    }
  }
}
```

### Telegram Tools
```typescript
// Send message
telegram.sendMessage({
  chat_id: "@channel",
  text: "Alert: High CPU usage!"
})

// Send with keyboard
telegram.sendMessage({
  chat_id: "@channel",
  text: "Choose an option:",
  reply_markup: {
    keyboard: [["Option 1", "Option 2"]]
  }
})

// Get updates
telegram.getUpdates({
  limit: 10
})

// Send photo
telegram.sendPhoto({
  chat_id: "@channel",
  photo: "https://example.com/chart.png",
  caption: "Daily stats"
})
```

---

## Use Cases

### 1. Monitoring Alerts
```
Trigger: Server down
Action: Slack → #alerts → "Server is down!"
```

### 2. Deployment Notifications
```
Trigger: CI/CD complete
Action: Discord → #deploys → Embed with status
```

### 3. Customer Support
```
Trigger: New ticket
Action: Telegram → @team → "New ticket: [issue]"
```

### 4. Daily Reports
```
Schedule: Daily 9 AM
Action: All platforms → Post daily summary
```

### 5. Incident Management
```
Trigger: Error rate spike
Action: 
  1. Slack → Alert channel
  2. Discord → Update status
  3. Telegram → Notify on-call
```

---

## Message Templates

### Deployment Alert
```typescript
{
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "🚀 *Deployment Complete*"
      }
    },
    {
      "type": "section",
      "fields": [
        { "type": "mrkdwn", "text": "*Environment:*\nproduction" },
        { "type": "mrkdwn", "text": "*Version:*\nv2.1.0" }
      ]
    }
  ]
}
```

### Incident Alert
```typescript
{
  "embeds": [{
    "title": "🚨 Incident Detected",
    "description": "Error rate > 5%",
    "color": 0xff0000,
    "fields": [
      { "name": "Service", "value": "api" },
      { "name": "Error Rate", "value": "7.2%" }
    ]
  }]
}
```

---

## Integration with 1ai-skills

### With Monitoring
```
skill-performance-monitor → communication-mcp → alerts
       ↓                    ↓
  Detect issue          Notify team
```

### With CI/CD
```
automation → communication-mcp → status updates
     ↓                ↓
 Deploy            Notify
```

### With Research
```
ai-research-agent → communication-mcp → share findings
        ↓                    ↓
  Analyze             Post to channels
```

---

## Best Practices

### Do's
✅ Use threads for related messages  
✅ Include actionable buttons  
✅ Format for readability  
✅ Set up appropriate permissions  

### Don'ts
❌ Don't spam channels  
❌ Don't send sensitive data  
❌ Don't ignore rate limits  

---

## Version History

- **v1.0** (2026-02-27) - Initial creation
  - Slack, Discord, Telegram support

---

## Related Skills

- [skill-performance-monitor](/skills/skill-performance-monitor) - Monitoring
- [automation](/skills/automation) - Workflow automation
- [alerting](/skills/alerting) - Alert management
