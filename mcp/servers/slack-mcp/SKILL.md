---
name: slack-mcp
description: Use when MCP server for Slack integration. Send messages, manage channels,
  and automate Slack workflows via standardized protocol.
domain: mcp
author: oyi77
license: Apache-2.0
subdomain: mcp
tags:
- mcp
- mcp-server
- model-context-protocol
- slack
- tool-integration
- chat-ops
- bot
version: 1.0.0
category: mcp
---



# Slack Mcp

## When to Use

**Trigger phrases:**
- "slack mcp"
- "Help me with slack mcp"
- "post to slack"
- "send slack message"
- "slack bot"
- "slack automation"

**Use cases:**
- When an AI agent needs to send messages, notifications, or alerts to Slack channels
- When building an MCP server that exposes Slack API tools (post message, list channels, create channel, add reaction, search history)
- When wiring Slack as a communication channel in a multi-platform agent workflow
- When creating internal dev-ops bots that notify teams of deployments, builds, errors, or incidents
- When automating channel management, user invites, or message moderation via AI agents

**When NOT to use:**
- For tasks outside this skill's scope
- When a simpler HTTP client (curl, requests) would suffice for a single scripted Slack call
- When the tool is used by a single agent in a single context without needing MCP interoperability
- When the Slack integration is read-only and does not benefit from MCP's tool-discovery and streaming



## Anti-Rationalization Table

| Excuse | Reality | Rule |
|--------|---------|------|
| "Webhooks are fine" | Webhooks lack discovery, type safety, and protocol evolution | MCP provides schema, capabilities, and versioning |
| "I'll write custom Slack integration" | Custom integrations rot; MCP servers are maintained | Use the standard; contribute upstream |
| "MCP is overkill" | MCP pays off at 2+ tools; Slack + anything = 2+ | Start with MCP; don't retrofit later |


**Trigger phrases:**
- "slack mcp"
- "Help me with slack mcp"
- "post to slack"
- "send slack message"
- "slack bot"
- "slack automation"

**Use cases:**
- When an AI agent needs to send messages, notifications, or alerts to Slack channels
- When building an MCP server that exposes Slack API tools (post message, list channels, create channel, add reaction, search history)
- When wiring Slack as a communication channel in a multi-platform agent workflow
- When creating internal dev-ops bots that notify teams of deployments, builds, errors, or incidents
- When automating channel management, user invites, or message moderation via AI agents

**When NOT to use:**
- For tasks outside this skill's scope
- When a simpler HTTP client (curl, requests) would suffice for a single scripted Slack call
- When the tool is used by a single agent in a single context without needing MCP interoperability
- When the Slack integration is read-only and does not benefit from MCP's tool-discovery and streaming

## When NOT to Use

- When a simpler HTTP client would suffice
- For internal tools that do not need cross-platform compatibility
- When the tool is used by a single agent in a single context

## Overview

Slack Mcp is a specialized MCP server that wraps the Slack Web API into callable tools and resources accessible to any MCP-compatible client (Claude, Cursor, VS Code extensions, custom agent harnesses). Instead of each agent re-implementing Slack API calls, scope negotiation, and pagination, a single Slack MCP server exposes typed tool definitions — agents discover capabilities, invoke tools with validated parameters, and receive structured responses.

The server bridges the Slack Events API, Web API, and (optionally) Socket Mode into a unified MCP interface. Common operations exposed as tools include: `post_message`, `list_channels`, `create_channel`, `archive_channel`, `add_reaction`, `get_channel_history`, `search_messages`, `get_user_profile`, `invite_user`, and `upload_file`.

## Architecture

```
┌─────────────────────────┐
│   MCP Client            │
│   (Claude / Cursor /    │
│    Custom Agent)         │
└────────┬────────────────┘
         │ MCP Protocol (stdio/SSE)
         ▼
┌─────────────────────────┐
│   Slack MCP Server      │
│                         │
│  ┌───────────────────┐  │
│  │  Tool Definitions  │  │  ──  post_message, list_channels, etc.
│  │  Resource URIs     │  │  ──  slack://channel/{id}/messages
│  └───────────────────┘  │
└────────┬────────────────┘
         │ Slack Web API (HTTPS)
         ▼
┌─────────────────────────┐
│   Slack Platform        │
│   (Workspace / Channel  │
│    / User / Bot)        │
└─────────────────────────┘
```

- **Server** — MCP-compliant server exposing tools and resources
- **Transport** — stdio (for local agent harnesses) or HTTP SSE (for remote clients)
- **Tools** — Callable functions with JSON Schema definitions backed by Slack SDK calls
- **Resources** — Readable data sources with URI-based access (e.g., `slack://channel/C12345/messages`)
- **Auth** — Bot tokens (`xoxb-*`) for workspace-installed apps; User tokens (`xoxp-*`) for user-scoped actions

## Setup

### 1. Create a Slack App

1. Go to https://api.slack.com/apps and click **Create New App**
2. Choose **From scratch**, give it a name, and select your workspace
3. Navigate to **OAuth & Permissions** and add the following Bot Token Scopes:

| Scope | Purpose |
|---|---|
| `chat:write` | Send messages as the bot |
| `channels:read` | View public channel metadata |
| `channels:manage` | Create, archive, rename public channels |
| `groups:read` | View private channel metadata |
| `groups:write` | Manage private channels |
| `reactions:write` | Add emoji reactions to messages |
| `files:write` | Upload files to channels |
| `users:read` | Look up user profiles and emails |
| `search:read` | Search messages and files across workspace |
| `im:write` | Send DMs to users |
| `mpim:write` | Send messages to group DMs |

### 2. Install the App to Workspace

- Click **Install to Workspace** and authorize
- Copy the **Bot User OAuth Token** (`xoxb-...`) from the OAuth & Permissions page

### 3. Optional: Socket Mode

If the Slack MCP server runs locally and cannot expose a public HTTPS endpoint:

1. Enable **Socket Mode** in app settings
2. Generate an **App-Level Token** (`xapp-...`) with `connections:write` scope
3. Set `SLACK_APP_TOKEN` environment variable

### 4. Environment Variables

```bash
# Required — Bot token for Web API calls
export SLACK_BOT_TOKEN=xoxb-your-bot-token-here

# Required for verifying incoming webhook requests
export SLACK_SIGNING_SECRET=your-signing-secret

# Required for Socket Mode (optional, omit for HTTP mode)
export SLACK_APP_TOKEN=xapp-your-app-token-here

# Optional — User token for user-scoped operations
export SLACK_USER_TOKEN=xoxp-your-user-token-here
```

## Configuration

- **Server name** — `slack-mcp` or custom identifier
- **Transport type** — `stdio` (default for agent harnesses) or `sse` (HTTP for remote clients)
- **Tool definitions** — JSON Schema describing each Slack API tool's input and output
- **Resource URI patterns** — `slack://channel/{channel_id}/messages` for reading channel history
- **Authentication** — Bot token passed to `@slack/web-api` client; rate limiting handled by the SDK
- **Rate limiting** — Slack enforces tiered rate limits per method family (typical: 1-20 req/min per workspace). The MCP server should queue requests and respect `Retry-After` headers
- **Logging** — Enable at server startup with `--log-level debug` to trace API call responses

## Code Examples

### Python — Slack MCP Server with post_message and list_channels

```python
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from mcp.server import Server
from mcp.types import Tool, TextContent
import json

server = Server("slack-mcp")
client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="post_message",
            description="Send a message to a Slack channel",
            inputSchema={
                "type": "object",
                "properties": {
                    "channel": {
                        "type": "string",
                        "description": "Channel ID (C12345) or name (#general)",
                    },
                    "text": {
                        "type": "string",
                        "description": "Message text. Supports Markdown-formatted blocks.",
                    },
                    "thread_ts": {
                        "type": "string",
                        "description": "Optional thread timestamp to reply in a thread",
                    },
                },
                "required": ["channel", "text"],
            },
        ),
        Tool(
            name="list_channels",
            description="List public channels in the workspace",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Max channels to return (default 100, max 200)",
                        "default": 100,
                    },
                    "cursor": {
                        "type": "string",
                        "description": "Pagination cursor for next page",
                    },
                },
            },
        ),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "post_message":
        try:
            response = client.chat_postMessage(
                channel=arguments["channel"],
                text=arguments["text"],
                thread_ts=arguments.get("thread_ts"),
            )
            return [TextContent(
                type="text",
                text=json.dumps({
                    "ok": True,
                    "ts": response["ts"],
                    "channel": response["channel"],
                }, indent=2),
            )]
        except SlackApiError as e:
            return [TextContent(
                type="text",
                text=f"Slack API error: {e.response['error']}",
            )]

    elif name == "list_channels":
        try:
            response = client.conversations_list(
                types="public_channel",
                limit=arguments.get("limit", 100),
                cursor=arguments.get("cursor"),
            )
            channels = [
                {"id": c["id"], "name": c["name"],
                 "member_count": c.get("member_count", 0),
                 "topic": c.get("topic", {}).get("value", "")}
                for c in response["channels"]
            ]
            result = {"channels": channels}
            if response.get("response_metadata", {}).get("next_cursor"):
                result["next_cursor"] = response["response_metadata"]["next_cursor"]
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        except SlackApiError as e:
            return [TextContent(
                type="text",
                text=f"Slack API error: {e.response['error']}",
            )]

    raise ValueError(f"Unknown tool: {name}")

# Entry point: asyncio.run(main()) with stdio transport
```

### Python — Advanced Tools (add_reaction, create_channel, get_history)

```python
# Extend the call_tool handler with additional tools

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        if name == "add_reaction":
            resp = client.reactions_add(
                channel=arguments["channel"],
                name=arguments["reaction"],
                timestamp=arguments["timestamp"],
            )
            return [TextContent(type="text", text=json.dumps({"ok": resp["ok"]}))]

        elif name == "create_channel":
            resp = client.conversations_create(
                name=arguments["name"],
                is_private=arguments.get("is_private", False),
            )
            return [TextContent(
                type="text",
                text=json.dumps({
                    "id": resp["channel"]["id"],
                    "name": resp["channel"]["name"],
                }, indent=2),
            )]

        elif name == "get_channel_history":
            resp = client.conversations_history(
                channel=arguments["channel"],
                limit=arguments.get("limit", 10),
                cursor=arguments.get("cursor"),
            )
            messages = [
                {"ts": m["ts"], "user": m.get("user", ""),
                 "text": m.get("text", ""),
                 "reactions": m.get("reactions", [])}
                for m in resp["messages"]
            ]
            return [TextContent(type="text", text=json.dumps({"messages": messages}, indent=2))]

        elif name == "upload_file":
            resp = client.files_upload_v2(
                channel=arguments["channel"],
                file=arguments["file_path"],
                title=arguments.get("title", ""),
                initial_comment=arguments.get("initial_comment", ""),
            )
            return [TextContent(type="text", text=json.dumps({"ok": True, "file_id": resp["file"]["id"]}))]

    except SlackApiError as e:
        return [TextContent(
            type="text",
            text=f"Slack API error: {e.response['error']}",
        )]

    raise ValueError(f"Unknown tool: {name}")
```

### JavaScript / TypeScript — Slack MCP Server

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from "@modelcontextprotocol/sdk/types.js";
import { WebClient, LogLevel } from "@slack/web-api";

const token = process.env.SLACK_BOT_TOKEN;
if (!token) {
  console.error("SLACK_BOT_TOKEN is required");
  process.exit(1);
}

const slack = new WebClient(token, {
  logLevel: LogLevel.DEBUG,
});

const server = new Server(
  { name: "slack-mcp", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

const TOOLS: Tool[] = [
  {
    name: "post_message",
    description: "Send a message to a Slack channel",
    inputSchema: {
      type: "object",
      properties: {
        channel: {
          type: "string",
          description: "Channel ID (C12345) or name (#general)",
        },
        text: { type: "string", description: "Message text" },
        thread_ts: {
          type: "string",
          description: "Thread timestamp to reply in thread",
        },
      },
      required: ["channel", "text"],
    },
  },
  {
    name: "list_channels",
    description: "List public channels",
    inputSchema: {
      type: "object",
      properties: {
        limit: { type: "number", default: 100 },
        cursor: { type: "string" },
      },
    },
  },
  {
    name: "search_messages",
    description: "Search messages across the workspace",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string", description: "Search query" },
        sort: {
          type: "string",
          enum: ["score", "timestamp"],
          default: "timestamp",
        },
        count: { type: "number", default: 20 },
      },
      required: ["query"],
    },
  },
];

server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools: TOOLS }));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case "post_message": {
        const result = await slack.chat.postMessage({
          channel: args.channel,
          text: args.text,
          thread_ts: args.thread_ts,
        });
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({
                ok: result.ok,
                ts: result.ts,
                channel: result.channel,
              }),
            },
          ],
        };
      }

      case "list_channels": {
        const result = await slack.conversations.list({
          types: "public_channel",
          limit: args.limit ?? 100,
          cursor: args.cursor,
        });
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({
                channels: result.channels?.map((c) => ({
                  id: c.id,
                  name: c.name,
                  member_count: c.member_count,
                })),
                next_cursor: result.response_metadata?.next_cursor,
              }),
            },
          ],
        };
      }

      case "search_messages": {
        const result = await slack.search.messages({
          query: args.query,
          sort: args.sort ?? "timestamp",
          count: args.count ?? 20,
        });
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({
                matches: result.messages?.matches?.map((m) => ({
                  ts: m.ts,
                  channel: m.channel?.id,
                  user: m.user,
                  text: m.text,
                  permalink: m.permalink,
                })),
              }),
            },
          ],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error: any) {
    return {
      content: [
        {
          type: "text",
          text: `Slack API error: ${error.data?.error ?? error.message}`,
        },
      ],
      isError: true,
    };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

### Client-Side — Agent Invoking Slack MCP Tools

```python
# Agent-side usage via MCP client SDK
from mcp import ClientSession, StdioClient

async def notify_deployment():
    async with StdioClient(["python", "slack_mcp_server.py"]) as client:
        async with ClientSession(client) as session:
            await session.initialize()
            result = await session.call_tool(
                "post_message",
                {
                    "channel": "#deployments",
                    "text": f":rocket: Deploy v2.1.0 to production complete\n"
                            f"• Frontend: https://app.example.com\n"
                            f"• Branch: main (commit a1b2c3d)",
                },
            )
            print(result.content[0].text)
```

```javascript
// Agent-side usage in JS
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const transport = new StdioClientTransport({
  command: "node",
  args: ["slack-mcp-server.js"],
});

const client = new Client(
  { name: "agent", version: "1.0.0" },
  { capabilities: {} }
);
await client.connect(transport);

const result = await client.callTool({
  name: "post_message",
  arguments: {
    channel: "#ops-alerts",
    text: ":warning: CPU threshold exceeded on app-server-3 (92%)",
  },
});
console.log(result.content);
```

## Integration

- Compatible with Claude, Cursor, VS Code extensions, and any MCP-compatible agent harness
- Supports streaming responses for large payloads (channel history, search results)
- Handles errors with standard MCP error codes — wrap Slack API exceptions into `INTERNAL_ERROR` or `INVALID_PARAMS`
- Can run alongside other MCP servers (database, GitHub, file system) for multi-tool orchestration
- Combine with webhook patterns: the Slack MCP server can subscribe to Events API (message posted, reaction added) and expose them as MCP resources or callbacks

### Client Registration

Add the server to your MCP client config (e.g., `~/.claude/mcp-config.json` or Claude Desktop settings):

```json
{
  "mcpServers": {
    "slack": {
      "command": "python",
      "args": ["-m", "slack_mcp_server"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-...",
        "SLACK_SIGNING_SECRET": "..."
      }
    }
  }
}
```

## Common Issues

### Insufficient Scope / missing_scope Error

```
Slack API error: missing_scope
```

**Cause:** The bot token lacks required OAuth scopes for the called method. For example, `conversations.list` without `channels:read`.

**Fix:** Add the missing scope in `api.slack.com/apps > OAuth & Permissions > Scopes`, then **Reinstall the app** to generate a new token.

### not_in_channel Error

```
Slack API error: not_in_channel
```

**Cause:** The bot user has not been invited to a private channel or group DM.

**Fix:** Invite the bot to the channel: `/invite @botname` in Slack, or call `conversations.invite(channel=C12345, users=BOT_USER_ID)`.

### rate_limited Error

```
Slack API error: rate_limited
```

**Cause:** Exceeded the method-family rate limit. Slack returns HTTP 429 with a `Retry-After` header.

**Fix:** Implement exponential backoff. The `@slack/web-api` client retries automatically when used with the default `retryConfig`. For Python, wrap calls with `tenacity`:

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2))
def safe_post(client, channel, text):
    return client.chat_postMessage(channel=channel, text=text)
```

### invalid_auth / token_revoked

```
Slack API error: invalid_auth
```

**Cause:** The token is invalid, expired, or the app was uninstalled. Bot tokens do not expire on their own but can be revoked by workspace admins.

**Fix:** Generate a new token by reinstalling the app. Check `api.slack.com/apps > OAuth & Permissions`.

### Socket Mode — Connection Drops

**Cause:** Socket Mode connections require a valid `SLACK_APP_TOKEN` (starts with `xapp-`) with `connections:write` scope. The connection drops if the token is invalid or the server does not send a ping within 30 seconds.

**Fix:** Ensure `SLACK_APP_TOKEN` is set and the MCP server calls `socket_mode.start()` with proper heartbeat intervals.

### Token in Source Control

**Cause:** Bot tokens committed to git are a security incident waiting to happen.

**Fix:** Always load `SLACK_BOT_TOKEN` from environment variables, not code. Add `.env` to `.gitignore`. Rotate the token immediately if accidentally exposed.

## Monetization

### 1. Slack App Directory — Paid App

Publish the Slack MCP server as a listed Slack app in the Slack App Directory. Charge for premium features:

| Tier | Features | Price |
|---|---|---|
| Free | Basic messaging, 10 channels, 100 msg/day | $0 |
| Pro | Unlimited channels, search, file uploads, 10K msg/day | $19/mo |
| Enterprise | SSO, audit logs, custom workflows, SLA | $99/mo |

Monetize via Stripe integration with the Slack app's subscription management.

### 2. Internal Tool — DevOps Consulting

Deploy the Slack MCP server as part of an internal developer productivity suite. Charge businesses for:
- Custom deployment and configuration ($500–$2,000 setup fee)
- Monthly maintenance and uptime SLA ($200–$500/mo)
- Custom tool integrations (Jira, PagerDuty, Datadog) plugged into the same MCP server

### 3. MCP Server Marketplace

List the Slack MCP server on emerging MCP marketplace platforms. Charge per-request or per-seat:
- Usage-based: $0.001 per tool invocation
- Per-seat: $5/seat/month for teams of 10+

### 4. Multi-Platform Agent Orchestration Bundle

Bundle the Slack server with other MCP servers (GitHub, Notion, Linear, Stripe) into a "DevOps Agent Suite" sold as a package. Target small engineering teams that want AI-powered Slack bots managing their entire dev pipeline.

### 5. White-Label SaaS

Offer a hosted Slack MCP server as a SaaS product where customers authenticate via OAuth (their own Slack app) and get a managed MCP endpoint. Price based on message volume and channel count.

## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up Slack app + tokens
2. **Execute** — Run slack mcp workflow with configured parameters; test each exposed tool
3. **Verify** — Validate output meets requirements, document results, check rate limit behavior

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases (missing scope, rate limit, invalid token)
- [ ] Documentation updated with findings
