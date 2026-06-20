---
name: mcp-discover
description: Discover and connect to MCP servers
domain: mcp
tags:
- discover
- mcp
- mcp-server
- model-context-protocol
- tool-integration
---
## When to Use

**Trigger phrases:**
- "mcp discover"
- "Help me with mcp discover"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

## Mcp Discover

Discover and connect to MCP servers

### Usage

```
/mcp-discover <task>
```

### Features

- Automated execution
- Error handling
- Result validation

## How to Use

1. Connect to an MCP server and request its capability manifest
2. Enumerate available tools, resources, and prompt templates
3. Inspect tool schemas for argument types and descriptions
4. Build a capability map for routing and orchestration

## Discovery Flow

```python
async def discover_server(server_config):
    client = MCPClient(server_config)
    await client.initialize()

    capabilities = {
        "tools": await client.list_tools(),
        "resources": await client.list_resources(),
        "prompts": await client.list_prompts()
    }

    for tool in capabilities["tools"]:
        print(f"Tool: {tool.name}")
        print(f"  Description: {tool.description}")

    return capabilities
```

## Common Patterns

- Cache discovery results to avoid repeated initialization
- Use tool descriptions for intelligent routing decisions
- Map MCP capabilities to your agent skill requirements
- Handle servers that dynamically add/remove tools at runtime

## When NOT to Use

- When the MCP server handles credentials or authentication tokens
- When the server processes data subject to regulatory retention requirements
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- MCP server does not validate inputs causing downstream errors
- Agent does not handle server connection failures with retry logic
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Input parameters are validated before server-side processing
- [ ] Connection failures trigger automatic retry with backoff
- [ ] All required outputs generated
- [ ] Success criteria met

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
