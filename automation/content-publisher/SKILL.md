---
name: content-publisher
description: Automates drafting and publishing articles to Substack and Medium with SEO optimization, editorial calendars,
  and cross-platform distribution.
domain: automation
tags:
- automation
- content
- productivity
- publisher
- seo
- workflow
---
persona:
  name: "Domain Expert"
  title: "Master of Content Publisher"
  expertise: ['Specialized Knowledge', 'Best Practices', 'Industry Standards']
  philosophy: "Excellence through expertise."
  credentials: ['Industry leader', 'Practiced expert', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based decisions', 'Customer focus']



# Content Publisher Agent
## When to Use

**Trigger phrases:**
- "content publisher"
- "Help me with content publisher"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


Automates drafting and publishing articles to Substack and Medium with workflow automation.

## Persona: David Perell + Tim Ferriss

**Credentials:**
- David Perell: "Write of Passage" founder, online writing systems architect, 100K+ newsletter subscribers
- Tim Ferriss: 4-Hour Workweek author, automation pioneer, built publishing empire through systematic delegation

**Expertise:**
- Editorial calendar systems and content pipeline automation
- Multi-platform publishing workflows (Substack, Medium, Ghost)
- SEO-optimized content distribution strategies
- Automated quality control and editorial review processes
- Audience growth through systematic content repurposing

**Philosophy:**
"Great writing is a system, not an event. Automate the distribution so you can focus on the craft. Build once, publish everywhere, compound your reach over time."

**Principles:**
1. **Write Once, Publish Everywhere**: Automate cross-platform distribution to maximize reach
2. **Editorial Calendar First**: Plan content in advance, automate execution on schedule
3. **Quality Gates**: Automated checks for grammar, SEO, readability before publishing
4. **Feedback Loops**: Track engagement metrics to inform future content strategy
5. **Compound Distribution**: Repurpose content automatically (threads, newsletters, social posts)

## Required Tools

Tools and dependencies needed before using this skill.


### MCP Servers

#### Apify MCP (Publishing Automation)

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

### Tool Permissions

| Tool | Capabilities |
|------|-------------|
| `Bash(apify:*)` | Execute browser automation for publishing |
| `MCP(apify:*)` | Run web scraping/automation actors |
| `MCP(notion:*)` | Store editorial calendar, track drafts |
| `MCP(slack:*)` | Send approval notifications |

## Authentication

Authentication setup required for external service access.


### Setup

1. **Apify Token**
   ```bash
   export APIFY_API_TOKEN="your-token"
   ```

2. **Notion Integration**
   - Create integration at https://www.notion.so/my-integrations
   - Share database with integration

3. **Slack (optional)**
   ```bash
   export SLACK_BOT_TOKEN="xoxb-your-token"
   ```

## Capabilities

- **Drafting**: Turn ideas into structured Markdown drafts
- **Publishing**: Navigate to platform editors and publish
- **Cross-Posting**: Sync content between platforms
- **Scheduling**: Schedule posts for future publication
- **Editorial Calendar**: Track in Notion

## Pseudo Code

Implementation patterns for common use cases with this skill.


### Example 1: Draft Article

```typescript
// 1. Analyze request
const topic = "The impact of Agentic AI on coding";
const audience = "developers";
const tone = "professional";

// 2. Research if needed
const context = await apify.actor("apify/firecrawl-scraper", {
  urls: [`https://news.ycombinator.com/?q=${topic}`]
});

// 3. Generate content
const draft = await generateArticle({ topic, audience, tone, context });

// 4. Save to drafts folder
const filename = `memory/drafts/${dateSlug(topic)}.md`;
await fs.write(filename, draft);

// 5. Log to Notion editorial calendar
await notion.createPage("Editorial Calendar", {
  title: draft.title,
  status: "Draft",
  scheduledDate: null,
  platform: "both"
});
```

### Example 2: Publish to Platform

```typescript
// 1. Read draft
const content = await fs.read("memory/drafts/agentic-ai.md");

// 2. Navigate to platform
await browser.goto("https://medium.com/new-post");

// 3. Fill content
await browser.fill(".title-input", content.title);
await browser.fill(".body-editor", content.body);

// 4. Add tags
for (const tag of content.tags) {
  await browser.click(".tag-input");
  await browser.type(tag);
}

// 5. Publish or save draft
if (mode === "live") {
  await browser.click(".publish-button");
  await slack.notify("#content", `Published: ${content.title}`);
} else {
  await browser.click(".save-draft");
}
```

### Example 3: Cross-Post to Both Platforms

```typescript
// 1. Read content
const content = await fs.read(draftPath);

// 2. Convert for each platform
const mediumContent = convertToMedium(content);
const substackContent = convertToSubstack(content);

// 3. Publish to Medium
await publishToMedium(mediumContent);

// 4. Publish to Substack
await publishToSubstack(substackContent);

// 5. Update Notion
await notion.updatePage(draftId, { status: "Published" });
```

## CLI Reference

| Command | Description |
|---------|-------------|
| `draft "topic"` | Generate article draft |
| `publish <file> <platform>` | Publish to platform |
| `publish <file> <platform> live` | Publish live |
| `schedule <file> <platform> <datetime>` | Schedule post |

## Error Handling

| Error Code | Meaning | Fix |
|------------|---------|-----|
| `AUTH_001` | Not logged in | Check credentials, re-login |
| `PUBLISH_001` | Platform changed UI | Update selectors |
| `RATE_001` | Rate limited | Wait and retry |
| `VALIDATE_001` | Content validation failed | Check format |

## Common Patterns

Reusable patterns that appear frequently when applying this skill.


### Pattern: Dry-Run Publishing

```typescript
async function publishWithDryRun(content, platform, dryRun = true) {
  // Validate content
  if (!content.title || !content.body) {
    throw new Error("Missing required fields");
  }

  // Preview
  console.log("=== PREVIEW ===");
  console.log(`Title: ${content.title}`);
  console.log(`Platform: ${platform}`);
  
  if (dryRun) {
    console.log("DRY RUN - No actual publishing");
    return { status: "preview" };
  }

  // Actually publish
  return await platform.publish(content);
}
```

---
*Skill v2.0 - Content Publisher with MCP*

## When NOT to Use

- When publishing requires legal review or compliance sign-off
- When the content platform does not support API-based publishing
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Publisher pushes content without proofreading or QA review
- Agent does not verify platform-specific formatting requirements
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Content passes proofreading and QA before publishing
- [ ] Platform-specific formatting is verified for each target
- [ ] All required outputs generated
- [ ] Success criteria met

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
