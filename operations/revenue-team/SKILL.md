---
name: revenue-team
description: Manage sales pipeline, forecast revenue, track deals with HubSpot and Notion
allowed-tools:
  - MCP(hubspot:*)
  - MCP(notion:*)
  - MCP(slack:*)
---

# Revenue Team

Manage sales pipeline, forecast revenue, track deals with HubSpot and Notion integration.

## Required Tools

```json
{
  "mcpServers": {
    "hubspot": { "command": "npx", "args": ["-y", "@sheffieldp/mcp-hubspot"], "env": { "HUBSPOT_API_KEY": "${HUBSPOT_API_KEY}" } },
    "notion": { "command": "npx", "args": ["-y", "@makenotion/mcp-server"], "env": { "NOTION_API_KEY": "${NOTION_API_KEY}" } },
    "slack": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-slack"], "env": { "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}" } }
  }
}
```

## Pseudo Code

### Pipeline Update

```typescript
// 1. Get deals
const deals = await hubspot.getDeals({ stage: "qualified" });

// 2. Calculate forecast
const forecast = deals.reduce((sum, d) => sum + d.amount, 0);

// 3. Update Notion
await notion.update("Revenue Forecast", { forecast });
```

### Stage Progression

```typescript
// Move deal to next stage
await hubspot.updateDeal(dealId, { dealstage: "contract_sent" });
await slack.notify("#sales", `Deal moved to contract: ${dealName}`);
```

---
*Skill v2.0 - Revenue Team*
