---
name: slack-mcp
description: MCP server for Slack integration. Send messages, manage channels, and automate Slack workflows via standardized protocol.
domain: mcp
tags:
- mcp
- mcp-server
- model-context-protocol
- slack
- tool-integration
---
# Slack Mcp

## When to Use

**Trigger phrases:**
- "slack mcp"
- "Help me with slack mcp"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


## When NOT to Use

- When a simpler HTTP client would suffice
- For internal tools that do not need cross-platform compatibility
- When the tool is used by a single agent in a single context


## Overview

Slack Mcp implements a Model Context Protocol server for Model Context Protocol.

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

```typescript
// Example: MCP server tool definition
import { McpServer } from "@modelcontextprotocol/sdk";

const server = new McpServer({ name: "my-tools", version: "1.0.0" });

server.tool("search", { query: z.string() }, async ({ query }) => {
  const results = await search(query);
  return { content: [{ type: "text", text: JSON.stringify(results) }] };
});
```


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run slack mcp workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings