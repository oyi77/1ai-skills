---
name: content-scheduler
description: Schedule and manage content publishing across platforms with Notion calendar
allowed-tools:
  - MCP(notion:*)
  - MCP(slack:*)
---

# Content Scheduler

Schedule and manage content publishing across platforms. Use Notion as a calendar and content repository, with Slack notifications for publishing alerts.

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

- Manage content calendar in Notion
- Schedule posts for multiple platforms
- Track publishing status
- Send alerts when content is ready to publish

## Pseudo Code

### Schedule Content

```typescript
// 1. Get content details
const content = {
  title: "Blog Post: 5 Tips for Better Productivity",
  platform: "LinkedIn",
  scheduledDate: new Date("2024-02-20T10:00:00Z"),
  author: "John",
  status: "Ready to Publish"
};

// 2. Create calendar entry in Notion
const scheduledPost = await notion.pages.create({
  parent: { databaseId: contentCalendarDbId },
  properties: {
    "Content": { "title": [{ "text": { "content": content.title } }] },
    "Platform": { "select": { "name": content.platform } },
    "Scheduled Date": { "date": { "start": content.scheduledDate.toISOString() } },
    "Status": { "status": { "name": content.status } },
    "Author": { "people": [{ "id": content.authorId }] }
  }
});

// 3. Set reminder for publishing
const reminderDate = new Date(content.scheduledDate);
reminderDate.setHours(reminderDate.getHours() - 2);

await slack.chat_postMessage({
  channel: "#content-publishing",
  text: `⏰ Content scheduled: "${content.title}" for ${content.platform} on ${formatDate(content.scheduledDate)}`
});
```

### Check Upcoming Content

```typescript
// 1. Query content calendar for next 7 days
const upcomingContent = await notion.databases.query({
  databaseId: contentCalendarDbId,
  filter: {
    "and": [
      {
        "property": "Scheduled Date",
        "date": { "after": "today" }
      },
      {
        "property": "Scheduled Date",
        "date": { "before": "7 days from now" }
      },
      {
        "property": "Status",
        "status": { "does_not_equal": "Published" }
      }
    ]
  },
  sorts: [{ "property": "Scheduled Date", "direction": "ascending" }]
});

// 2. Group by platform
const byPlatform = groupBy(upcomingContent.results, "Platform.select.name");

// 3. Send summary to Slack
await slack.chat_postMessage({
  channel: "#content-calendar",
  text: "📅 Upcoming content for the week:",
  blocks: Object.entries(byPlatform).map(([platform, posts]) => ({
    "type": "section",
    "text": {
      "type": "mrkdwn",
      "text": `*${platform}*\n${posts.map(p => `• ${p.properties.Content.title[0].plain_text}`).join("\n")}`
    }
  }))
});
```

### Update Publishing Status

```typescript
// Update status after publishing
await notion.pages.update({
  pageId: postId,
  properties: {
    "Status": { "status": { "name": "Published" } },
    "Published Date": { "date": { "start": new Date().toISOString() } }
  }
});

// Notify team
await slack.chat_postMessage({
  channel: "#content-published",
  text: `✅ Published: ${postTitle}`
});
```

---

*Skill v2.0 - Content Scheduler*
