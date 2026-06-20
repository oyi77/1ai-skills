---
name: joko-proactive-agent
description: Proactive agent that detects signals and suggests actions with Slack notifications
domain: core
tags:
- agent
- ai-agent
- infrastructure
- joko
- memory
- proactive
- self-improvement
- slack
allowed-tools:
- MCP(slack:*)
- MCP(notion:*)
---
persona:
  name: "Adam Cheyer"
  title: "The Virtual Assistant Pioneer - Master of Proactive AI"
  expertise: ['Proactive Agents', 'Virtual Assistants', 'Context Awareness', 'Predictive Systems']
  philosophy: "The best interface is no interface."
  credentials: ['Co-founder of Siri', 'Created Viv Labs (acquired by Samsung)', 'Pioneer of conversational AI']
  principles: ['Anticipate needs', 'Act on context', 'Minimize user input', 'Be helpful proactively']



# Joko Proactive Agent
## When to Use

**Trigger phrases:**
- "joko proactive agent"
- "Help me with joko proactive agent"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


Proactive agent that monitors business signals, detects opportunities/issues, and suggests actions with Slack notifications.

## Required Tools

```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": { "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}" }
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

- **Slack MCP**: https://github.com/modelcontextprotocol/server-slack
- **Notion MCP**: https://github.com/makenotion/mcp-server-notion

## Capabilities

- Monitor Notion databases for changes
- Send proactive alerts to Slack channels
- Suggest actions based on detected patterns
- Log all detections in Notion for tracking

## Pseudo Code
```python
# Example workflow for this skill
def execute(input_data):
    # Step 1: Validate input
    if not input_data:
        raise ValueError("Input data is required")

    # Step 2: Process core logic
    result = process(input_data)

    # Step 3: Validate output
    validate_output(result)

    return result
```


### Monitor Database Changes

```typescript
// 1. Query Notion database for recent items
const recentItems = await notion.databases.query({
  databaseId: salesPipelineId,
  filter: {
    "property": "Last Updated",
    "date": { "after": "24 hours ago" }
  }
});

// 2. Analyze each item for signals
for (const item of recentItems.results) {
  const signals = detectSignals(item);
  
  if (signals.length > 0) {
    // 3. Log detection in Notion
    await notion.pages.create({
      parent: { databaseId: signalLogDbId },
      properties: {
        "Signal": { "rich_text": [{ "text": { "content": signals.join(", ") } }] },
        "Source": { "url": item.url },
        "Priority": { "select": { "name": signals.length > 2 ? "High" : "Medium" } },
        "Status": { "status": { "name": "New" } }
      }
    });

    // 4. Send proactive Slack notification
    await slack.chat_postMessage({
      channel: "#sales-alerts",
      text: `Signal detected: ${item.properties.Name.title[0].plain_text}`,
      blocks: [
        {
          "type": "section",
          "text": {
            "type": "mrkdwn",
            "text": `*Action Required*\n${signals.join("\n• ")}\n<${item.url}|View in Notion>`
          }
        },
        {
          "type": "actions",
          "elements": [
            {
              "type": "button",
              "text": { "type": "plain_text", "text": "Take Action" },
              "url": item.url
            }
          ]
        }
      ]
    });
  }
}
```

### Detect Business Signals

```typescript
function detectSignals(item: any): string[] {
  const signals: string[] = [];
  
  // Signal: Deal stuck in same stage > 7 days
  const daysInStage = getDaysInStage(item);
  if (daysInStage > 7) {
    signals.push(`Deal stalled: ${daysInStage} days in current stage`);
  }
  
  // Signal: High-value deal
  const value = item.properties.Value?.number || 0;
  if (value > 10000) {
    signals.push(`High-value deal: $${value.toLocaleString()}`);
  }
  
  // Signal: Competitor mentioned
  const notes = item.properties.Notes?.rich_text[0]?.plain_text || "";
  if (notes.match(/competitor|comparison|alternative/gi)) {
    signals.push("Competitor mentioned in notes");
  }
  
  return signals;
}
```

---

*Skill v2.0 - Joko Proactive Agent*

## When NOT to Use

- When the task requires domain expertise the agent has not been configured with
- When human review is mandated by compliance or regulatory requirements
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Agent output is not validated against expected quality standards
- Prerequisites are not verified before task execution
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Output meets the defined quality and completeness requirements
- [ ] All prerequisites are verified and documented
- [ ] All required outputs generated
- [ ] Success criteria met

## Overview

> Section content — see SKILL.md body for full details.
