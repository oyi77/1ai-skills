---
name: analytics-reporting
description: Generate analytics reports, dashboards, and business metrics with Notion and Slack
allowed-tools:
  - MCP(notion:*)
  - MCP(slack:*)
---

# Analytics Reporting

Generate analytics reports, dashboards, and business metrics.

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
*Skill v2.0 - Analytics Reporting*
