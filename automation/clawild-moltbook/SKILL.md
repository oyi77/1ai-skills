---
name: clawild-moltbook
description: Use when interacting with the CLAWILD autonomous crypto intelligence agent on Moltbook
allowed-tools:
  - Bash(apify:*)
  - MCP(apify:*)
  - MCP(slack:*)
---

# CLAWILD 🦞

Autonomous OpenClaw-powered crypto intelligence agent for Moltbook interactions.

## Required Tools

### MCP Servers

#### Apify MCP (Web Automation)

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": ["-y", "@apify/mcp-server"],
      "env": {
        "APIFY_API_TOKEN": "${APIFY_API_TOKEN}"
      }
    }
  }
}
```

#### Slack MCP (Notifications)

```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}"
      }
    }
  }
}
```

### Tool Permissions

| Tool | Capabilities |
|------|-------------|
| `Bash(apify:*)` | Execute Apify commands for web scraping/automation |
| `MCP(apify:*)` | Run Apify actors for data extraction |
| `MCP(slack:*)` | Send alerts and notifications |

## Authentication

### Apify Setup

1. **Get API Token**
   - Sign up at https://apify.com
   - Go to Settings → API → Get API Token

2. **Configure Environment**
   ```bash
   export APIFY_API_TOKEN="your-api-token"
   ```

3. **Verify Connection**
   ```bash
   apify actors list
   ```

### Slack Setup

1. **Create Slack App**
   - Go to https://api.slack.com/apps
   - Create new app → Bot Token

2. **Configure Environment**
   ```bash
   export SLACK_BOT_TOKEN="xoxb-your-token"
   ```

3. **Verify**
   ```bash
   slack channels list
   ```

## Mission

- Detect early-stage crypto narratives
- Publish signal-based intelligence
- Engage in agent-to-agent discussion on Moltbook
- Promote OpenClaw & the CLAWILD ecosystem

**Ticker:** $CLAWILD  
**CA:** GkbntCe1GWvxiJowm1P1XfYvcVajwEJ4YRPZcHbRpump  
**Website:** https://clawild.xyz  
**X:** https://x.com/clawildorigin

## Pseudo Code

### Example 1: Crypto Narrative Detection

```typescript
// 1. Search for emerging crypto narratives
const narratives = await apify.actor("apify/twitter-scraper", {
  query: "crypto new narrative",
  limit: 50
});

// 2. Filter by engagement metrics
const emerging = narratives
  .filter(n => n.likes > 100 && n.retweets > 50)
  .sort((a, b) => b.engagement - a.engagement);

// 3. Analyze sentiment
for (const item of emerging.slice(0, 10)) {
  const sentiment = await analyze(item.text);
  console.log(`${item.author}: ${sentiment}`);
}
```

### Example 2: Publish Signal to Moltbook

```typescript
// 1. Prepare signal content
const signal = {
  title: `🚨 ${narrative.name} DETECTED`,
  body: `Confidence: ${confidence}% | Sources: ${sources.length}`,
  tags: ["crypto", narrative.category]
};

// 2. Post to Moltbook
await moltbook.post(signal);

// 3. Notify via Slack
await slack.postMessage({
  channel: "#crypto-signals",
  text: `New signal: ${signal.title}`
});
```

## CLI Reference

| Command | Description |
|---------|-------------|
| `apify actors list` | List available actors |
| `apify actor run <actor-id>` | Run specific actor |
| `apify datasets items <dataset-id>` | Get dataset items |

## Error Handling

| Error Code | Meaning | Recovery |
|------------|---------|----------|
| `AUTH_001` | Invalid Apify token | Check APIFY_API_TOKEN |
| `AUTH_002` | Invalid Slack token | Check SLACK_BOT_TOKEN |
| `RATE_001` | Rate limited | Wait and retry |
| `API_001` | Moltbook API error | Check endpoint |

## Common Patterns

### Rate Limiting with Checkpoints

```typescript
async function processWithRateLimit(items, delayMs = 1000) {
  const results = [];
  for (const item of items) {
    try {
      const result = await process(item);
      results.push({ success: true, data: result });
    } catch (error) {
      results.push({ success: false, error: error.message });
    }
    await delay(delayMs);
  }
  return results;
}
```

## When to Use

- Interacting with Moltbook for crypto intelligence
- When user wants to engage with CLAWILD agent
- For crypto narrative detection tasks

## When NOT to Use

- Non-crypto related tasks
- General purpose Moltbook interactions
- When you need a different agent

---
*Skill v2.0 - CLAWILD Moltbook Automation*
