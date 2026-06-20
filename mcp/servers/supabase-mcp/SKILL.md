---
name: supabase-mcp
description: MCP server for Supabase databases
domain: mcp
tags:
- mcp
- mcp-server
- model-context-protocol
- supabase
- tool-integration
---
## When to Use

**Trigger phrases:**
- "supabase mcp"
- "Help me with supabase mcp"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

## Supabase Mcp

MCP server for Supabase databases

### Usage

```
/supabase-mcp <task>
```

### Features

- Automated execution
- Error handling
- Result validation

## How to Use

1. Get project URL and anon/service key from Supabase dashboard
2. Configure the MCP server with SUPABASE_URL and SUPABASE_KEY
3. Use tools for database queries, auth management, and storage

## Available Tools

| Tool | Description |
|------|-------------|
| `query_table` | Query rows from a table with filters |
| `insert_rows` | Insert one or more rows into a table |
| `update_rows` | Update rows matching a filter |
| `invoke_function` | Call an Edge Function |
| `list_buckets` | List storage buckets |
| `get_user` | Retrieve user details by ID |

## Common Patterns

- Use Row Level Security (RLS) policies for multi-tenant access
- Use Edge Functions for server-side logic with low latency
- Enable realtime subscriptions for live data updates
- Use storage buckets for file uploads with signed URLs

## When NOT to Use

- When Supabase stores regulated data requiring specific compliance certifications
- When the database operations affect production data without backup verification
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- MCP server does not enforce row-level security policies
- Agent does not handle Supabase connection pool exhaustion
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Row-level security policies are enforced
- [ ] Connection pool exhaustion is handled gracefully
- [ ] All required outputs generated
- [ ] Success criteria met

## Overview

> Section content — see SKILL.md body for full details.
