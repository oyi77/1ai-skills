---
name: notion-mcp
description: MCP server for Notion databases
domain: mcp
tags:
- mcp
- mcp-server
- model-context-protocol
- notion
- tool-integration
---
## When to Use

**Trigger phrases:**
- "notion mcp"
- "Help me with notion mcp"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

## Notion Mcp

MCP server for Notion databases

### Usage

```
/notion-mcp <task>
```

### Features

- Automated execution
- Error handling
- Result validation

## How to Use

1. Create a Notion integration at notion.so/my-integrations
2. Share target pages/databases with the integration
3. Configure the MCP server with NOTION_API_KEY

## Available Tools

| Tool | Description |
|------|-------------|
| `query_database` | Query a database with filters and sorts |
| `create_page` | Create a new page in a database |
| `update_page` | Update page properties |
| `get_page_content` | Read page blocks (content) |
| `append_blocks` | Add content blocks to a page |
| `search` | Full-text search across the workspace |

## Common Patterns

- Query databases with property filters for structured retrieval
- Use page templates for consistent content creation
- Append blocks in batches to minimize API calls
- Use relation properties to link pages across databases

## When NOT to Use

- When Notion stores regulated compliance documentation
- When the workspace data has specific data residency requirements
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- MCP server does not handle Notion block-based content model correctly
- Agent does not preserve Notion page metadata during updates
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Block-based content model is handled correctly
- [ ] Page metadata is preserved during update operations
- [ ] All required outputs generated
- [ ] Success criteria met

## Overview

> Section content — see SKILL.md body for full details.
