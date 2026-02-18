---
name: self-improving-agent
description: Agent that learns from feedback and improves its own performance over time
allowed-tools:
  - MCP(notion:*)
  - MCP(slack:*)
---

# Self-Improving Agent

Agent that learns from feedback and improves performance.

## Required Tools

```json
{
  "mcpServers": {
    "notion": { "env": { "NOTION_API_KEY": "${NOTION_API_KEY}" } },
    "slack": { "env": { "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}" } }
  }
}
```

---
*Skill v2.0 - Self-Improving Agent*
