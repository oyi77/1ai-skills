---
name: market-research
description: Conduct market research, competitive analysis, and industry insights with Exa and Firecrawl
allowed-tools:
  - MCP(exa:*)
  - MCP(firecrawl:*)
  - MCP(notion:*)
---

# Market Research

Conduct market research, competitive analysis, and industry insights.

## Required Tools

```json
{
  "mcpServers": {
    "exa": { "command": "npx", "args": ["-y", "@exa/mcp-server"], "env": { "EXA_API_KEY": "${EXA_API_KEY}" } },
    "firecrawl": { "command": "npx", "args": ["-y", "@firecrawl/mcp-server"], "env": { "FIRECRAWL_API_KEY": "${FIRECRAWL_API_KEY}" } },
    "notion": { "command": "npx", "args": ["-y", "@makenotion/mcp-server"], "env": { "NOTION_API_KEY": "${NOTION_API_KEY}" } }
  }
}
```

## Pseudo Code

### Competitor Analysis

```typescript
const competitors = await exa.search("SaaS competitors", { category: "company" });
for (const comp of competitors) {
  const details = await firecrawl.scrape(comp.website);
}
```

---
*Skill v2.0 - Market Research*
