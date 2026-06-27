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
# Mcp Server Builder

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

- When a simpler HTTP client would suffice
- For internal tools that do not need cross-platform compatibility
- When the tool is used by a single agent in a single context


## Overview

Mcp Server Builder implements a Model Context Protocol server for Model Context Protocol.

## Architecture

- **Server** — MCP-compliant server exposing tools and resources
- **Transport** — stdio or HTTP transport layer
- **Tools** — Callable functions with JSON Schema definitions
- **Resources** — Readable data sources with URI-based access

## Setup

1. Install the MCP server package
2. Configure environment variables and credentials
3. Register the server in MCP client configuration
4. Test tool invocations and resource access

## Configuration

- Server name and version
- Transport type (stdio, SSE, HTTP)
- Tool definitions with input/output schemas
- Resource URI patterns
- Authentication and rate limiting

## Integration

- Compatible with Claude, Cursor, and other MCP clients
- Supports streaming responses for large payloads
- Handles errors with standard MCP error codes

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I will just use curl" | MCP handles auth, retries, streaming, and type safety. Use the SDK. |
| "One mega-server is simpler" | Single-responsibility servers are easier to debug and maintain. |
| "MCP is just a wrapper" | MCP enables cross-platform tool sharing. It is infrastructure, not overhead. |

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings