---
name: content-scheduler
description: Schedule and manage content publishing across platforms with Notion calendar
allowed-tools:
  - MCP(notion:*)
  - MCP(slack:*)
---

# Content Scheduler

Schedule and manage content publishing.

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
*Skill v2.0 - Content Scheduler*
