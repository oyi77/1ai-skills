---
name: mcp-server-builder
description: Create MCP (Model Context Protocol) servers for any API or service. Auto-generate tools, resources, and prompts
  that any AI agent can use.
domain: mcp
tags:
- ai-agent
- api
- builder
- mcp
- mcp-server
- model-context-protocol
- server
- tool-integration
persona:
  name: Anthropic MCP Team
  expertise: Protocol design, API integration, AI agent architecture
  philosophy: Standards enable interoperability
  credentials: Created MCP standard at Anthropic
---
## MCP Server Builder

Create Model Context Protocol servers that expose any API to AI agents.

### Quick Start

```python
# Generate MCP server from OpenAPI spec
## When to Use

**Trigger phrases:**
- "mcp server builder"
- "Help me with mcp server builder"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

mcp generate --spec https://api.example.com/openapi.json

# Or create custom server
mcp create --name "my-service" --tools getData,postData
```

### What is MCP?

MCP is a protocol that allows AI systems to access external tools and data through a standardized interface. Think USB-C for AI applications.

### Server Components

**Tools:** Functions the AI can call
```json
{
  "name": "searchDatabase",
  "description": "Search company database",
  "input_schema": {
    "query": "string",
    "limit": "number"
  }
}
```

**Resources:** Data the AI can read
```json
{
  "uri": "docs://readme",
  "name": "Project README",
  "mimeType": "text/markdown"
}
```

**Prompts:** Pre-defined templates
```json
{
  "name": "debug_error",
  "template": "Analyze this error: {{error}}"
}
```

### Building a Server

1. Define your API endpoints as tools
2. Document responses as resources
3. Create reusable prompts
4. Package and distribute

### Integration

Works with Claude Code, Cursor, and any MCP-compatible client.

## When NOT to Use

- When the MCP server handles authentication credentials
- When the server processes data subject to regulatory retention requirements
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- MCP server does not validate input parameters causing runtime errors
- Agent does not handle MCP server connection failures with retry logic
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Input parameters are validated before processing
- [ ] Connection failures trigger retry with exponential backoff
- [ ] All required outputs generated
- [ ] Success criteria met

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
