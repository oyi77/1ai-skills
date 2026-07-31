---
name: mcp-discover
description: Discover and connect to MCP servers automatically. Browse available tools and register new server endpoints. Use when working with mcp discover.
domain: mcp
author: oyi77
license: Apache-2.0
subdomain: mcp
tags:
- discover
- mcp
- mcp-server
- model-context-protocol
- tool-integration
version: 1.0.0
---


# MCP Discover — Find and Register MCP Servers

## Quick Reference

Automatically discover MCP servers in your environment, list their available tools, check health, and register new endpoints. The discovery layer for the MCP ecosystem.

## Overview

MCP Discover scans local network, registry files, or known URLs to find available MCP servers. For each server it reports the transport type (stdio/HTTP/SSE), available tools with full JSON Schema, health status, and authentication requirements. Combined with MCP Client, it enables zero-config server onboarding: discover, connect, invoke — no manual configuration needed.

## Quick Start

1. **Broadcast scan**: `mcp-discover scan --network 192.168.1.0/24 --port-range 5000-5100` — finds servers on local network
2. **List registered**: `mcp-discover list --verbose` — shows all known servers with tool counts
3. **Check health**: `mcp-discover --health-check --timeout 5s` — validates each server is responsive

## Key Pattern: Continuous Discovery Agent

```python
from mcp_discover import DiscoveryAgent

agent = DiscoveryAgent(
    scan_interval=300,       # check every 5 minutes
    auto_register=True,      # register new servers automatically
    health_required=True     # only register healthy servers
)
agent.start()

@agent.on_server_registered
def handle_new(server):
    print(f"New server: {server.name} ({server.transport})")
    client = MCPClient(server.name)
    tools = client.list_tools()
    print(f"  Tools: {[t.name for t in tools]}")
```

## Discovery Methods

| Method | Use Case | Command |
|---|---|---|
| Network scan | Find servers on LAN | `mcp-discover scan --network 10.0.0.0/8` |
| Registry | Pre-registered servers | `mcp-discover list --verbose` |
| URL probe | Remote server catalog | `mcp-discover probe https://mcp.example.com/tools.json` |

## Discovery Checklist

- [ ] `mcp-discover list` shows all expected servers with tool schemas
- [ ] Health check passes for every server (timeout policy configured)
- [ ] Auto-discovery runs on schedule (scan_interval set appropriately)
- [ ] New servers are auto-registered and appear in tool routing
- [ ] Failed servers are detected and removed from active pool within configured interval

## When to Use

Use when working with mcp discover.

## Workflow

Execute these steps sequentially:

1. **Broadcast scan**: `mcp-discover scan --network 192.168.1.0/24 --port-range 5000-5100` — finds servers on local network
2. **List registered**: `mcp-discover list --verbose` — shows all known servers with tool counts
3. **Check health**: `mcp-discover --health-check --timeout 5s` — validates each server is responsive

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I know all the servers I need" | Discovery often surfaces servers you did not know existed — that is the point. Manual lists go stale |
| "Discovery is a one-time setup" | Servers come and go, ports change, versions update. Continuous discovery keeps the ecosystem alive |
| "Auto-discovery is over-engineering" | With 5+ servers, manual registration breaks constantly. Automate it before it becomes a time sink |
