---
name: governance-team
description: Manage policies, access control, compliance, and governance processes with Notion and Slack
allowed-tools:
  - MCP(notion:*)
  - MCP(slack:*)
---

# Governance Team

Manage policies, access control, compliance, and governance processes.

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

### Policy Change

```typescript
// 1. Create proposal
const proposal = await notion.createPage("Governance", {
  title: "Update Data Retention Policy",
  type: "policy-change",
  status: "draft",
  content: policyDraft
});

// 2. Request review
await slack.notify("#governance", `New policy: ${proposal.title}`);

// 3. Collect approvals
for (const approver of approvers) {
  await slack.dm(approver, `Please review: ${proposal.url}`);
}
```

### Access Control

```typescript
// Check access
const hasAccess = await checkPermissions(user, resource);
if (!hasAccess) {
  await slack.alert("#security", `Unauthorized access: ${user} -> ${resource}`);
}
```

---
*Skill v2.0 - Governance Team*
