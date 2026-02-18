---
name: workflow-builder
description: Build and automate workflows for business operations with Notion and Slack integration
allowed-tools:
  - MCP(notion:*)
  - MCP(slack:*)
---

# Workflow Builder

Build and automate workflows for business operations.

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
*Skill v2.0 - Workflow Builder*
