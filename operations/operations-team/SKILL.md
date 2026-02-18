---
name: operations-team
description: Execute SOPs, handle on-call triage, manage SLA breaches with Notion and Slack
allowed-tools:
  - MCP(notion:*)
  - MCP(slack:*)
---

# Operations Team

Execute SOPs, handle on-call triage, manage SLA breaches.

## Required Tools

```json
{
  "mcpServers": {
    "notion": { "command": "npx", "args": ["-y", "@makenotion/mcp-server"], "env": { "NOTION_API_KEY": "${NOTION_API_KEY}" } },
    "slack": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-slack"], "env": { "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}" } }
  }
}
```

## Pseudo Code

### SOP Execution

```typescript
// 1. Load SOP
const sop = await notion.get("sop-id");

// 2. Execute steps
for (const step of sop.steps) {
  await execute(step);
  await log(step.result);
}
```

### On-Call Triage

```typescript
// 1. Check alerts
const alerts = await fetchAlerts();

for (const alert of alerts) {
  const severity = await assessSeverity(alert);
  
  if (severity === "critical") {
    await slack.alert("#oncall", `CRITICAL: ${alert.message}`);
    await page(alert);
  }
}
```

---
*Skill v2.0 - Operations Team*
