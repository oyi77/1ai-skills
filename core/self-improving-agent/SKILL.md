---
name: self-improving-agent
description: Agent that learns from feedback and improves its own performance over time
allowed-tools:
  - MCP(notion:*)
  - MCP(slack:*)
---
persona:
  name: "Domain Expert"
  title: "Master of Self Improving Agent"
  expertise: ['Specialized Knowledge', 'Best Practices', 'Industry Standards']
  philosophy: "Excellence through expertise."
  credentials: ['Industry leader', 'Practiced expert', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based decisions', 'Customer focus']



# Self-Improving Agent

Agent that learns from feedback, tracks performance metrics, and continuously improves its own performance using Notion for knowledge base and Slack for notifications.

## Required Tools

```json
{
  "mcpServers": {
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

## MCP References

- **Notion MCP**: https://github.com/makenotion/mcp-server-notion
- **Slack MCP**: https://github.com/modelcontextprotocol/server-slack

## Capabilities

- Track feedback and performance metrics in Notion
- Analyze patterns in successful vs unsuccessful attempts
- Suggest improvements based on learned patterns
- Alert team to significant performance changes

## Pseudo Code

### Track Feedback

```typescript
// 1. Log feedback in Notion
await notion.pages.create({
  parent: { databaseId: feedbackDbId },
  properties: {
    "Task Type": { "select": { "name": taskType } },
    "Outcome": { "select": { "name": success ? "Success" : "Failure" } },
    "Feedback": { "rich_text": [{ "text": { "content": feedback } }] },
    "Suggestions": { "rich_text": [{ "text": { "content": suggestions } }] },
    "Date": { "date": { "start": new Date().toISOString() } }
  }
});
```

### Analyze Performance Patterns

```typescript
// 1. Query feedback database
const feedback = await notion.databases.query({
  databaseId: feedbackDbId,
  filter: {
    "property": "Date",
    "date": { "after": "30 days ago" }
  }
});

// 2. Calculate success rate by task type
const byType = groupBy(feedback.results, "Task Type");
const metrics = Object.entries(byType).map(([type, items]) => ({
  type,
  successRate: items.filter(i => i.properties.Outcome.select.name === "Success").length / items.length,
  avgScore: calculateAvgScore(items)
}));

// 3. Identify improvement opportunities
const lowPerformers = metrics.filter(m => m.successRate < 0.7);
if (lowPerformers.length > 0) {
  // 4. Notify team
  await slack.chat_postMessage({
    channel: "#agent-metrics",
    text: `Performance alert: ${lowPerformers.map(p => `${p.type}: ${p.successRate*100}%`).join(", ")}`
  });
}
```

### Self-Improvement Loop

```typescript
async function improveFromFeedback(): Promise<void> {
  // 1. Get recent feedback
  const recentFeedback = await getRecentFeedback(days: 7);
  
  // 2. Extract common failure patterns
  const patterns = extractPatterns(recentFeedback.failures);
  
  // 3. Generate improvement suggestions
  const suggestions = patterns.map(pattern => ({
    pattern,
    recommendation: generateRecommendation(pattern),
    priority: pattern.frequency * pattern.impact
  }));
  
  // 4. Update knowledge base in Notion
  for (const suggestion of suggestions) {
    await notion.pages.create({
      parent: { databaseId: improvementsDbId },
      properties: {
        "Pattern": { "rich_text": [{ "text": { "content": suggestion.pattern } }] },
        "Recommendation": { "rich_text": [{ "text": { "content": suggestion.recommendation } }] },
        "Priority": { "select": { "name": suggestion.priority > 0.5 ? "High" : "Medium" } },
        "Status": { "status": { "name": "To Implement" } }
      }
    });
  }
  
  // 5. Alert if major improvement opportunity found
  if (suggestions.some(s => s.priority > 0.7)) {
    await slack.chat_postMessage({
      channel: "#agent-updates",
      text": "Major improvement opportunities identified - review recommended changes"
    });
  }
}
```

---

*Skill v2.0 - Self-Improving Agent*
