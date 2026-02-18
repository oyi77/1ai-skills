---
name: joko-moltbook
description: Queue-driven Moltbook posting agent with deduplication and monitoring
allowed-tools:
  - Bash(apify:*)
  - MCP(apify:*)
  - MCP(notion:*)
  - MCP(slack:*)
---

# Joko Moltbook Agent

Queue-driven Moltbook posting agent with deduplication, idempotency, and monitoring.

## Required Tools

### MCP Servers

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": ["-y", "@apify/mcp-server"],
      "env": { "APIFY_API_TOKEN": "${APIFY_API_TOKEN}" }
    },
    "notion": {
      "command": "npx",
      "args": ["-y", "@makenotion/mcp-server"],
      "env": { "NOTION_API_KEY": "${NOTION_API_KEY}" }
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": { "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}" }
    }
  }
}
```

## Authentication

### Setup

1. **Apify Token**
   ```bash
   export APIFY_API_TOKEN="your-token"
   ```

2. **Notion** (for content queue)
   - Create integration and share queue database

3. **Slack** (for alerts)
   ```bash
   export SLACK_BOT_TOKEN="xoxb-your-token"
   ```

## Pseudo Code

### Example 1: Queue-Driven Posting

```typescript
// 1. Fetch pending posts from Notion queue
const queue = await notion.query("Content Queue", {
  filter: { status: "pending" }
});

// 2. Process each with idempotency check
for (const item of queue) {
  const key = generateIdempotencyKey(item.content);
  
  // Check if already posted
  const exists = await cache.get(key);
  if (exists) {
    console.log(`Skipping duplicate: ${item.id}`);
    continue;
  }
  
  // Post to Moltbook
  const result = await moltbook.post(item.content);
  
  // Mark as posted
  await cache.set(key, result.postId);
  await notion.updatePage(item.id, { status: "posted" });
}
```

### Example 2: Deduplication with Content Hash

```typescript
// Generate deterministic hash for content
function hashContent(content) {
  return sha256(content.text + content.tags.sort().join());
}

// Check before posting
const contentHash = hashContent(newPost);
const existing = await db.posts.findOne({ contentHash });

if (existing) {
  console.log("Duplicate detected, skipping");
  return { status: "duplicate", existingPost: existing };
}

const result = await moltbook.post(newPost);
await db.posts.insert({ contentHash, postId: result.id });
```

### Example 3: Monitor and Alert

```typescript
// 1. Monitor posting health
const stats = await getPostingStats();

// 2. Check metrics
if (stats.failureRate > 0.1) {
  await slack.alert({
    channel: "#alerts",
    text: `High failure rate: ${stats.failureRate * 100}%`
  });
}

// 3. Daily summary
await slack.notify("#daily-reports", `
  Posts: ${stats.total}
  Success: ${stats.success}
  Failed: ${stats.failed}
`);
```

## CLI Reference

| Command | Description |
|---------|-------------|
| `joko queue status` | Check queue size |
| `joko post now` | Process queue immediately |
| `joko stats` | Show posting statistics |

## Error Handling

| Error Code | Meaning | Fix |
|------------|---------|-----|
| `AUTH_001` | Session expired | Refresh credentials |
| `RATE_001` | Rate limited | Backoff 10 min |
| `DUPLICATE_001` | Duplicate content | Skip, mark handled |
| `QUEUE_001` | Queue empty | Nothing to do |

## Common Patterns

### Idempotency Key Generation

```typescript
function generateIdempotencyKey(item) {
  return `moltbook:${sha256(item.text + item.createdAt)}`;
}
```

### Exponential Backoff

```typescript
async function withBackoff(fn, maxRetries = 5) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      const delay = Math.min(1000 * Math.pow(2, i), 60000);
      await sleep(delay);
    }
  }
}
```

---
*Skill v2.0 - Joko Moltbook*
