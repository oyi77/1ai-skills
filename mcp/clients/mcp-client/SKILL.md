---
name: mcp-client
description: Generic MCP client implementation for connecting to any Model Context Protocol server with standardized tool access. Use when working with mcp client.
domain: mcp
author: oyi77
license: Apache-2.0
subdomain: mcp
tags:
- client
- mcp
- mcp-server
- model-context-protocol
- tool-integration
version: 1.0.0
---


# MCP Client — Connect to Any MCP Server

## Quick Reference

Connect to any Model Context Protocol server, list its tools, invoke them with typed parameters, and handle results. The core building block for MCP-powered automation.

## Overview

The MCP client is your connection layer to MCP servers. It handles transports (stdio for local processes, HTTP/SSE for remote), tool schema resolution, type-safe invocation, error classification (protocol errors, connection failures, timeouts), and result handling. Every server interaction starts here: connect, list tools, call tool, disconnect.

## Quick Start

1. **Connect**: `client = MCPClient("server-name", transport={"type": "stdio", "command": "node", "args": ["server.js"]})`
2. **Discover tools**: `tools = client.list_tools()` — returns typed schemas for every tool
3. **Invoke**: `result = client.call_tool("tool_name", {"param": "value"})` — returns structured output

## Key Pattern: Resilient Tool Invocation

```python
def safe_invoke(client, tool, params, retries=2):
    errors = []
    for attempt in range(retries + 1):
        try:
            result = client.call_tool(tool, params)
            if result.is_error:
                code = result.error.get("code", -1)
                if code in (-32700, -32600, -32601):
                    raise RuntimeError(f"Protocol error: {result.error['message']}")
            return result
        except (ConnectionError, TimeoutError) as e:
            errors.append(f"Attempt {attempt + 1}: {e}")
            if attempt < retries:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"Failed: {'; '.join(errors)}")
```

## When NOT to Use

- You need a full SDK with application-level abstractions (use language-specific MCP SDK)
- You're building a long-running server (this is a client, not a server implementation)
- Connection management isn't needed (direct HTTP calls suffice for one-off tool calls)

## Transports

| Transport | When | Example |
|---|---|---|
| stdio | Local process | `{"command": "node", "args": ["server.js"]}` |
| HTTP/SSE | Remote server | `{"url": "https://mcp.example.com", "headers": {"Auth": "Bearer token"}}` |

## Client Checklist

- [ ] `ping()` succeeds before any tool invocation
- [ ] `list_tools()` returns valid JSON Schema for each parameter
- [ ] Error handling covers all 3 failure modes: protocol error, connection failure, timeout
- [ ] Exponential backoff configured for transient failures
- [ ] Disconnect/cleanup called after each session

## Commands

```bash
# List all available tools from a connected MCP server
# (implement via client.list_tools())

# Call a tool with typed parameters
# (implement via client.call_tool("tool_name", {"param": "value"}))

# Standard health check before any tool call
# client.ping()  → throws on unreachable server
```

## Dependencies

- Python 3.10+ (for async/await patterns)
- `mcp` package: Python MCP SDK
- `httpx` or `aiohttp`: for HTTP/SSE transport
- No external services required (connects to local or remote MCP servers)

## Verification

- [ ] `client.ping()` succeeds before invoking tools
- [ ] `list_tools()` returns valid JSON Schema for every tool parameter
- [ ] Error handling tested for all 3 failure modes: protocol error, connection failure, timeout
- [ ] Exponential backoff configured for transient failures
- [ ] `disconnect()` called after each session (no dangling processes)

## When to Use

Use when working with mcp client.

## Workflow

Execute these steps sequentially:

1. **Connect**: `client = MCPClient("server-name", transport={"type": "stdio", "command": "node", "args": ["server.js"]})`
2. **Discover tools**: `tools = client.list_tools()` — returns typed schemas for every tool
3. **Invoke**: `result = client.call_tool("tool_name", {"param": "value"})` — returns structured output

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll just use curl/requests directly" | MCP handles auth, retries, streaming, and type-safe schemas — curl duplicates all of that manually |
| "I only need one connection, no abstraction needed" | One connection today becomes three next month. The client abstraction pays for itself at server #2 |
| "Synchronous calls are fine" | MCP pipelines need async for parallel tool execution. Plan for it from the start |
