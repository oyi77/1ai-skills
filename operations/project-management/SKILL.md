---
name: project-management
description: Coordinate tasks, track deadlines, manage sprints, and maintain project documentation with Notion integration
allowed-tools:
  - MCP(notion:*)
  - MCP(slack:*)
---

# Project Management

Coordinate tasks, track deadlines, manage sprints, and maintain project documentation.

## Required Tools

### MCP Servers

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

## Capabilities

- **Task Management**: Create, assign, track tasks
- **Sprint Planning**: Organize work into sprints
- **Deadline Tracking**: Monitor due dates and milestones
- **Status Reporting**: Generate project updates

## Pseudo Code

### Example 1: Create Task

```typescript
// 1. Create task in Notion
const task = await notion.createPage("Project Tasks", {
  title: "Implement user authentication",
  properties: {
    Status: "Not Started",
    Priority: "P1",
    Assignee: "john@company.com",
    DueDate: "2024-03-15",
    Sprint: "Sprint 12"
  }
});

console.log(`Created: ${task.id}`);
```

### Example 2: Sprint Planning

```typescript
// 1. Get backlog
const backlog = await notion.query("Backlog", {
  filter: { property: "Status", equals: "Ready" }
});

// 2. Estimate effort
const estimated = await estimateEffort(backlog);

// 3. Allocate to sprint (max 40 points)
const sprint = [];
let points = 0;
for (const item of backlog) {
  if (points + item.estimate <= 40) {
    sprint.push(item);
    points += item.estimate;
  }
}

// 4. Create sprint
await notion.createPage("Sprints", {
  title: "Sprint 12",
  items: sprint,
  startDate: "2024-03-01",
  endDate: "2024-03-14"
});
```

### Example 3: Status Report

```typescript
// 1. Get active tasks
const tasks = await notion.query("Project Tasks", {
  filter: { property: "Status", does_not_equal: "Done" }
});

// 2. Group by status
const byStatus = groupBy(tasks, "Status");

// 3. Generate report
const report = `# Status Report - ${new Date().toLocaleDateString()}

## Summary
- Total: ${tasks.length}
- In Progress: ${byStatus["In Progress"]?.length || 0}
- Blocked: ${byStatus["Blocked"]?.length || 0}

## Blockers
${byStatus["Blocked"]?.map(t => `- ${t.title}`).join("\n") || "None"}
`;

await slack.post("#project-updates", report);
```

## CLI Reference

| Command | Description |
|---------|-------------|
| `pm task create <title>` | Create new task |
| `pm sprint plan` | Plan next sprint |
| `pm report` | Generate status report |

## Error Handling

| Error Code | Meaning | Fix |
|------------|---------|-----|
| `NOTION_001` | API error | Retry later |
| `SLACK_001` | Failed to notify | Manual update |

## Priority Framework

| Priority | Definition | Response Time |
|----------|------------|---------------|
| P0 | Revenue impacted | Immediate |
| P1 | Major feature blocked | 24 hours |
| P2 | Normal work | 1 week |
| P3 | Nice to have | Next sprint |

---
*Skill v2.0 - Project Management*
