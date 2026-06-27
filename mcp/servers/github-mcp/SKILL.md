---
name: github-mcp
description: MCP server for GitHub automation
domain: mcp
tags:
- github
- mcp
- mcp-server
- model-context-protocol
- tool-integration
---
# Github Mcp

## When to Use

**Trigger phrases:**
- "github mcp"
- "Help me with github mcp"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

## Overview

Github Mcp implements a Model Context Protocol server for Model Context Protocol.

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

