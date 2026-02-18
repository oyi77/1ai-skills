---
name: business-development
description: Generate leads, research prospects, and manage outreach with HubSpot and Exa integration
allowed-tools:
  - MCP(hubspot:*)
  - MCP(exa:*)
  - MCP(slack:*)
---

# Business Development

Generate leads, research prospects, and manage outreach.

## Required Tools

```json
{
  "mcpServers": {
    "hubspot": { "env": { "HUBSPOT_API_KEY": "${HUBSPOT_API_KEY}" } },
    "exa": { "env": { "EXA_API_KEY": "${EXA_API_KEY}" } },
    "slack": { "env": { "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}" } }
  }
}
```

---
*Skill v2.0 - Business Development*
