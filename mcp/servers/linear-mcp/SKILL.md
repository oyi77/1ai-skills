---
name: linear-mcp
description: Linear Mcp. Use when working with linear mcp in mcp domain.
domain: mcp
tags:
- linear
- mcp
- mcp-server
- model-context-protocol
- tool-integration
---
## When to Use

**Trigger phrases:**
- "linear mcp"
- "Help me with linear mcp"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

## Linear Mcp

MCP server for Linear issues

### Usage

```
/linear-mcp <task>
```

### Features

- Automated execution
- Error handling
- Result validation

## How to Use

1. Generate a Linear API key at linear.app/settings/api
2. Configure the MCP server with the LINEAR_API_KEY environment variable
3. Use tools to manage issues, projects, and team workflows

## Available Tools

| Tool | Description |
|------|-------------|
| `list_issues` | Query issues by team, assignee, status |
| `create_issue` | Create a new issue with priority and labels |
| `update_issue` | Change status, assignee, priority, or labels |
| `list_projects` | List active projects with progress |
| `search_issues` | Full-text search across all issues |

## Common Patterns

- Use issue IDs (e.g., ENG-123) for precise references
- Set priority levels (0=urgent, 1=high, 2=medium, 3=low)
- Use cycles for sprint-based workflows
- Link GitHub PRs to Linear issues via branch naming conventions

## When NOT to Use

- When Linear is used to track compliance-mandated work items
- When the MCP server handles client-confidential project data
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- MCP server does not handle Linear workspace permission boundaries
- Agent creates issues without checking for existing duplicates
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Workspace permission boundaries are enforced
- [ ] Duplicate detection prevents redundant issue creation
- [ ] All required outputs generated
- [ ] Success criteria met

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
