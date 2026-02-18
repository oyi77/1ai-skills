---
name: workflow-builder
description: Build and automate workflows for business operations with Notion and Slack integration
allowed-tools:
  - MCP(notion:*)
  - MCP(slack:*)
---

# Workflow Builder

Build and automate workflows for business operations using Notion for task tracking and Slack for notifications.

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

- Create automated workflows in Notion databases
- Trigger Slack notifications on task status changes
- Build multi-step business processes
- Connect external events to Notion updates

## Pseudo Code

### Create Workflow Pipeline

```typescript
// 1. Create Notion database for workflow
const db = await notion.createDatabase({
  parentId: workspaceId,
  title: "Sales Pipeline",
  properties: {
    "Stage": { "select": { "options": ["Lead", "Qualified", "Proposal", "Closed"] } },
    "Contact": { "people": {} },
    "Due Date": { "date": {} },
    "Status": { "status": { "options": ["Not Started", "In Progress", "Done"] } }
  }
});

// 2. Set up Slack notification for new items
async function notifyNewLead(page: any) {
  await slack.chat_postMessage({
    channel: "#sales-leads",
    text: `New lead: ${page.properties.Name.title[0].plain_text}`,
    blocks: [
      {
        "type": "section",
        "text": { "type": "mrkdwn", "text": `*New Lead*\n${page.url}` }
      }
    ]
  });
}

// 3. Create automation trigger
const trigger = await notion.createWebhook({
  databaseId: db.id,
  url: "https://api.yourautomation.com/trigger",
  events: ["page.created"]
});
```

### Update Task and Notify

```typescript
// Update task status in Notion
await notion.pages.update({
  pageId: taskId,
  properties: {
    "Status": { "status": { "name": "In Progress" } }
  }
});

// Send Slack update
await slack.chat_postMessage({
  channel: "#tasks",
  text: `Task updated: https://notion.so/page/${taskId}`
});
```

---

*Skill v2.0 - Workflow Builder*
