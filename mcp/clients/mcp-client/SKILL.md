---
name: mcp-client
description: Generic MCP client implementation
domain: mcp
---
## Mcp Client

Generic MCP client implementation

### Usage

```
/mcp-client <task>
```

### Features

- Automated execution
- Error handling
- Result validation

## How to Use

1. Configure the MCP server connection in your client settings
2. Initialize the client with the server endpoint and authentication
3. List available tools, resources, and prompts from the server
4. Call tools with structured arguments and handle responses

## Client Configuration

```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "@my-org/mcp-server"],
      "env": { "API_KEY": "${MY_API_KEY}" }
    }
  }
}
```

## Common Patterns

- Use SSE transport for remote MCP servers
- Implement tool discovery before calling tools
- Handle server restarts with automatic reconnection
- Cache tool schemas to reduce initialization overhead
- Validate tool arguments against the server JSON schema

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

