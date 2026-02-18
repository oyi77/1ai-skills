---
name: market-research
description: Conduct market research, competitive analysis, and industry insights with Exa and Firecrawl
allowed-tools:
  - MCP(exa:*)
  - MCP(firecrawl:*)
  - MCP(notion:*)
---

# Market Research

Conduct comprehensive market research, competitive analysis, and industry insights. Uses Exa for searching and Firecrawl for detailed data extraction, with Notion for storing research.

## Required Tools

```json
{
  "mcpServers": {
    "exa": {
      "command": "npx",
      "args": ["-y", "@exa/mcp-server"],
      "env": { "EXA_API_KEY": "${EXA_API_KEY}" }
    },
    "firecrawl": {
      "command": "npx",
      "args": ["-y", "@firecrawl/mcp-server"],
      "env": { "FIRECRAWL_API_KEY": "${FIRECRAWL_API_KEY}" }
    },
    "notion": {
      "command": "npx",
      "args": ["-y", "@makenotion/mcp-server"],
      "env": { "NOTION_API_KEY": "${NOTION_API_KEY}" }
    }
  }
}
```

## MCP References

- **Exa MCP**: https://github.com/exa/mcp-server
- **Firecrawl MCP**: https://github.com/mendableai/firecrawl-mcp-server
- **Notion MCP**: https://github.com/makenotion/mcp-server-notion

## Capabilities

- Search for companies, industries, and trends
- Scrape detailed information from websites
- Analyze competitors and market positioning
- Store research in organized Notion databases

## Pseudo Code

### Competitor Analysis

```typescript
// 1. Search for competitors in the market
const competitors = await exa.search("SaaS competitors enterprise software", {
  category: "company",
  numResults: 20,
  fields: ["company", "description", "domain", "employeeCount", "funding"]
});

// 2. Filter to top competitors
const topCompetitors = competitors
  .filter(c => c.employeeCount > 50)
  .slice(0, 5);

// 3. Scrape detailed info from each competitor
const competitorData = [];
for (const comp of topCompetitors) {
  try {
    const details = await firecrawl.scrape({
      url: `https://${comp.domain}`,
      options: { formats: ["markdown", "html"] }
    });
    
    competitorData.push({
      name: comp.company,
      domain: comp.domain,
      description: comp.description,
      content: details.markdown
    });
  } catch (e) {
    console.log(`Failed to scrape ${comp.domain}:`, e);
  }
}

// 4. Store in Notion
const researchPage = await notion.pages.create({
  parent: { databaseId: researchDbId },
  properties: {
    "Title": { "title": [{ "text": { "content": `Competitor Analysis: ${industry}` } }] },
    "Type": { "select": { "name": "Competitor Analysis" } },
    "Date": { "date": { "start": new Date().toISOString() } }
  },
  children: competitorData.map(comp => ({
    "object": "block",
    "type": "heading_3",
    "heading_3": { "rich_text": [{ "text": { "content": comp.name } }] }
  }))
});
```

### Industry Trend Analysis

```typescript
// 1. Search for recent industry news and trends
const trends = await exa.search(`${industry} trends 2024`, {
  type: "news",
  numResults: 20,
  fields: ["title", "url", "publishedDate", "author"]
});

// 2. Get in-depth articles
const trendDetails = await Promise.all(
  trends.slice(0, 5).map(trend => 
    firecrawl.scrape({ url: trend.url, options: { formats: ["markdown"] } })
  )
);

// 3. Identify key themes
const themes = extractThemes(trendDetails.map(t => t.markdown));

// 4. Create trend report in Notion
await notion.pages.create({
  parent: { databaseId: researchDbId },
  properties: {
    "Title": { "title": [{ "text": { "content": `Trend Report: ${industry} - ${formatDate(new Date())}` } }] },
    "Type": { "select": { "name": "Trend Analysis" } }
  },
  children: [
    {
      "object": "block",
      "type": "heading_2",
      "heading_2": { "rich_text": [{ "text": { "content": "Key Themes" } }] }
    },
    ...themes.map(theme => ({
      "object": "block",
      "type": "bulleted_list_item",
      "bulleted_list_item": { "rich_text": [{ "text": { "content": theme } }] }
    }))
  ]
});
```

### Market Size Estimation

```typescript
// 1. Search for market data
const marketData = await exa.search(`${industry} market size revenue 2024`, {
  numResults: 10,
  fields: ["title", "url", "description"]
});

// 2. Extract key statistics
const stats = {
  totalMarketSize: extractMarketSize(marketData),
  growthRate: extractGrowthRate(marketData),
  keyPlayers: extractKeyPlayers(marketData)
};

// 3. Store in Notion for reference
await notion.pages.create({
  parent: { databaseId: marketDataDbId },
  properties: {
    "Metric": { "title": [{ "text": { "content": `${industry} Market Size` } }] },
    "Value": { "rich_text": [{ "text": { "content": stats.totalMarketSize } }] },
    "Source": { "url": marketData[0].url }
  }
});
```

---

*Skill v2.0 - Market Research*
