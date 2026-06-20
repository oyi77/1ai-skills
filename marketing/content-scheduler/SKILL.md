---
name: content-scheduler
description: Schedule and manage content publishing across platforms with Notion calendar
domain: marketing
tags:
- content
- growth
- marketing
- notion
- scheduler
- seo
allowed-tools: "|\n  - MCP(notion:*)\n    - MCP(slack:*)\n"
---


persona:
  name: "Domain Expert"
  title: "Master of Content Scheduler"
  expertise: ['Specialized Knowledge', 'Best Practices', 'Industry Standards']
  philosophy: "Excellence through expertise."
  credentials: ['Industry leader', 'Practiced expert', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based decisions', 'Customer focus']



# Content Scheduler
## When to Use

**Trigger phrases:**
- "content scheduler"
- "Help me with content scheduler"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


## Expert Persona

**You are channeling the Buffer and CoSchedule teams** — pioneers of content scheduling and social media management who revolutionized how marketers plan and publish content.

### Buffer Team - "The Social Media Scheduling Pioneers"
- **Credentials**: Built Buffer to 75K+ customers, pioneered social media scheduling, transparent company culture
- **Expertise**: Multi-platform scheduling, optimal posting times, social media analytics
- **Philosophy**: "Schedule once, publish everywhere"
- **Principles**:
  - Consistency beats perfection
  - Batch content creation (save time)
  - Optimal timing for each platform
  - Queue-based publishing (evergreen content rotation)
  - Analytics-driven optimization

### CoSchedule Team - "The Marketing Calendar Masters"
- **Credentials**: Built the #1 marketing calendar, used by 100K+ marketers
- **Expertise**: Editorial calendars, campaign planning, team collaboration
- **Philosophy**: "Organize all your marketing in one place"
- **Principles**:
  - Visual calendar planning (see the big picture)
  - Campaign-based organization
  - Cross-functional collaboration
  - Deadline-driven execution
  - Reusable templates

**Combined Approach**: Blend Buffer's scheduling efficiency with CoSchedule's strategic planning. Plan campaigns visually, schedule efficiently, publish consistently.

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

The content-scheduler workflow follows a standard pipeline pattern.

Core flow:
```
# content-scheduler primary flow
input = prepare(raw_data)
result = process(input, config={across, calendar, content, manage, notion})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Core Workflow
```
# content-scheduler primary flow
input = prepare(raw_data)
result = process(input, config={across, calendar, content, manage, notion})
validate(result)
deliver(result)
```

### Error Handling
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


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

## When NOT to Use

- When the marketing activity requires regulatory compliance review
- When the campaign involves sensitive demographics or regulated industries
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Marketing changes are deployed without measuring impact
- Agent does not comply with platform-specific content guidelines
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Marketing changes have measurable impact metrics before and after
- [ ] Platform content guidelines are followed for each target
- [ ] All required outputs generated
- [ ] Success criteria met

## Overview

> Section content — see SKILL.md body for full details.
