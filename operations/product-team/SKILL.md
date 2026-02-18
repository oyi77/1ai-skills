---
name: product-team
description: Manage PRD creation, roadmap planning, sprint coordination, and release management with Notion
allowed-tools:
  - MCP(notion:*)
  - MCP(slack:*)
---

# Product Team

Manage PRD creation, roadmap planning, sprint coordination, and release management.

## Required Tools

```json
{
  "mcpServers": {
    "notion": { "command": "npx", "args": ["-y", "@makenotion/mcp-server"], "env": { "NOTION_API_KEY": "${NOTION_API_KEY}" } },
    "slack": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-slack"], "env": { "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}" } }
  }
}
```

## Pseudo Code

### PRD Creation

```typescript
const prd = await notion.createPage("Product PRDs", {
  title: "User Authentication Feature",
  problem: "Users cannot securely access...",
  solution: "Implement OAuth2...",
  successMetrics: ["Login success rate > 95%"],
  timeline: "Q2 2024"
});
```

### Roadmap Planning

```typescript
const roadmap = await notion.query("Features", {
  filter: { property: "Status", equals: "Planned" }
});

const byQuarter = groupBy(roadmap, "quarter");
```

---
*Skill v2.0 - Product Team*
