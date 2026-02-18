---
name: joko-proactive-agent
description: Proactive agent that detects signals and suggests actions with Slack notifications
allowed-tools:
  - MCP(slack:*)
  - MCP(notion:*)
---

# Joko Proactive Agent

Proactive agent that detects signals and suggests actions.

## Required Tools

```json
{
  "mcpServers": {
    "slack": { "env": { "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}" } },
    "notion": { "env": { "NOTION_API_KEY": "${NOTION_API_KEY}" } }
  }
}
```

---
*Skill v2.0 - Joko Proactive Agent*
