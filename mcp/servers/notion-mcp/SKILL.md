---
name: notion-mcp
description: Use when MCP server for Notion databases. Query pages, manage databases, and automate Notion workflows via standardized protocol.
domain: mcp
author: oyi77
license: Apache-2.0
subdomain: mcp
tags:
- mcp
- mcp-server
- model-context-protocol
- notion
- tool-integration
version: 1.0.0
---
# Notion Mcp

## When to Use

**Trigger phrases:**
- "notion mcp"
- "Help me with notion mcp"

**Use cases:**
- Give AI coding agents read/write access to project databases, sprint backlogs, and documentation
- Automate meeting-note processing — extract action items and create Notion database records
- Build a personal knowledge base where an AI agent reads, classifies, and cross-references Notion pages
- Sync Notion databases with external sources (GitHub issues, Google Calendar, email inboxes)
- Generate weekly reports by querying multiple databases and aggregating results via MCP tool chains

**When NOT to use:**
- For tasks outside this skill's scope


## When NOT to Use

- When a simpler HTTP client would suffice
- For internal tools that do not need cross-platform compatibility
- When the tool is used by a single agent in a single context
- When you only need one-time bulk export — use Notion's native export instead
- When the data is ephemeral and doesn't need structured tool discovery


## Overview

Notion Mcp gives AI agents structured read/write access to Notion workspaces through the official Notion API. It wraps database queries, page creation, block appending, search, and property updates into MCP tools that any MCP-compatible client (Claude, Cursor, VS Code) can invoke directly. The server uses `@notionhq/client` (Node.js) or `notion-client` (Python) for all Notion API operations, with JSON Schema input validation for type-safe parameter passing.

## Architecture

- **Server** — MCP-compliant server exposing tools and resources
- **Transport** — stdio or HTTP transport layer
- **Tools** — Callable functions with JSON Schema definitions
- **Resources** — Readable data sources with URI-based access

## Setup
### Prerequisites

- **Notion Integration** — Create one at [notion.so/my-integrations](https://www.notion.so/my-integrations): pick a workspace, copy the "Internal Integration Secret".
- **Workspace Access** — Open the target database or page in Notion, click **Share** → **Invite** → enter the integration name.

### Installation

```bash
# Node.js
npm install @modelcontextprotocol/sdk @notionhq/client

# Python
pip install mcp notion-client
```

### Environment

```bash
export NOTION_API_KEY=ntn_your_integration_secret_here
```

### MCP Client Registration

Add to your `claude_desktop_config.json` or equivalent:

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-notion"],
      "env": {
        "NOTION_API_KEY": "ntn_your_integration_secret_here"
      }
    }
  }
}
```

## Configuration
- `NOTION_API_KEY` (required) — Internal Integration Secret from notion.so/my-integrations
- **Database/Page sharing** — Each target object must be explicitly shared with the integration; the API returns 404 for unshared objects
- **Rate-limit handling** — Default 3 requests/second per integration. The SDK retries automatically, but bulk operations may need a throttling wrapper
- **Property schema** — Before writing filters or updates, call `retrieve_database` to discover column types (title, rich_text, select, status, date, multi_select, etc.)
- **Transport** — Prefer **stdio** for local agent use; **SSE** (Server-Sent Events) for remote server deployment behind a reverse proxy
- **Tool naming** — Use `snake_case` and avoid generic names (`search` → `search_workspace`)

## Integration

- Compatible with Claude, Cursor, and other MCP clients
- Supports streaming responses for large payloads
- Handles errors with standard MCP error codes

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I can just use the Notion API directly" | MCP handles auth, structured tool discovery, and client-agnostic invocation. Your tool works in any MCP host without integration-specific code. |
| "Building a server is overkill for one query" | Even a single tool benefits from JSON Schema input validation, consistent error formatting, and documented arguments. |
| "Database schema changes will break everything" | The MCP input schema catches property mismatches at invocation time. Version your tools with v1/v2 handlers for backward compatibility. |
| "MCP is just a wrapper" | MCP enables cross-platform tool sharing. It is infrastructure, not overhead. |

```python
# Python — using mcp and notion-client packages
from mcp.server.fastmcp import FastMCP
from notion_client import Client

server = FastMCP("notion-mcp-server")
notion = Client(auth="ntn_your_integration_secret")


@server.tool()
def query_database(database_id: str, status_filter: str = "") -> str:
    """Query a Notion database, optionally filtering by Status."""
    filter_params = {}
    if status_filter:
        filter_params["filter"] = {
            "property": "Status",
            "select": {"equals": status_filter},
        }
    results = notion.databases.query(
        database_id=database_id, **filter_params
    )
    pages = [
        {
            "id": p["id"],
            "title": "".join(
                t["plain_text"]
                for t in p["properties"].get("Name", {}).get("title", [])
            ),
            "url": p["url"],
        }
        for p in results["results"]
    ]
    return str(pages)


@server.tool()
def create_todo(database_id: str, title: str, assignee: str = "") -> str:
    """Create a to-do page in a Notion database."""
    properties = {"Name": {"title": [{"text": {"content": title}}]}}
    if assignee:
        properties["Assignee"] = {"rich_text": [{"text": {"content": assignee}}]}
    page = notion.pages.create(
        parent={"database_id": database_id}, properties=properties
    )
    return f"Created: {page['url']}"


if __name__ == "__main__":
    server.run()
```

```typescript
// TypeScript — using @modelcontextprotocol/sdk and @notionhq/client
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { Client } from "@notionhq/client";

const notion = new Client({ auth: process.env.NOTION_API_KEY! });
const server = new Server(
  { name: "notion-mcp", version: "1.0.0" },
  { capabilities: { tools: {} } },
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "query_database",
      description: "Query a Notion database",
      inputSchema: {
        type: "object",
        properties: {
          database_id: { type: "string", description: "Notion database ID" },
          status_filter: { type: "string", description: "Filter by Status field" },
        },
        required: ["database_id"],
      },
    },
    {
      name: "create_todo",
      description: "Create a to-do page in a database",
      inputSchema: {
        type: "object",
        properties: {
          database_id: { type: "string" },
          title: { type: "string" },
          assignee: { type: "string" },
        },
        required: ["database_id", "title"],
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  if (name === "query_database") {
    const { database_id, status_filter } = args as any;
    const response = await notion.databases.query({
      database_id,
      filter: status_filter
        ? { property: "Status", select: { equals: status_filter } }
        : undefined,
    });
    return {
      content: [{ type: "text", text: JSON.stringify(response.results) }],
    };
  }
  if (name === "create_todo") {
    const { database_id, title, assignee } = args as any;
    const properties: Record<string, any> = {
      Name: { title: [{ text: { content: title } }] },
    };
    if (assignee) {
      properties.Assignee = { rich_text: [{ text: { content: assignee } }] };
    }
    const page = await notion.pages.create({
      parent: { database_id },
      properties,
    });
    return { content: [{ type: "text", text: page.url }] };
  }
  throw new Error(`Unknown tool: ${name}`);
});

const transport = new StdioServerTransport();
await server.connect(transport);
```


## Common Issues

- **401 Unauthorized** — The integration secret is invalid or not set as `NOTION_API_KEY`. Verify at [notion.so/my-integrations](https://www.notion.so/my-integrations).
- **404 Object Not Found** — The database/page ID is wrong, or the integration doesn't have access. Share the target with the integration via the Share menu.
- **429 Rate Limited** — Notion enforces 3 requests/second per integration. The SDK handles retry-after automatically; for bulk pipelines add a queuing wrapper.
- **Empty Results** — The filter property name doesn't match the database schema. Call `retrieve_database` first to inspect column names and types.
- **Property Type Mismatch** — A filter uses the wrong type (e.g. `select` vs `status`). Use `retrieve_database` to discover the exact type for each property.
- **MCP Client Disconnected** — The server process crashed or the transport config is invalid. Check the MCP client logs and verify the config JSON is valid.

## Process

1. **Integration setup** — Create a Notion integration at notion.so/my-integrations, copy the secret, and share target pages/databases with the integration by name.
2. **Server configuration** — Install the MCP server package and `@notionhq/client`, set `NOTION_API_KEY`, register the server in your MCP client configuration file (e.g. `claude_desktop_config.json`).
3. **Tool inventory** — Identify which Notion operations your workflow needs: query databases, create pages, append block children (paragraphs, headings, to-do lists), update page properties, and search the workspace.
4. **Test with real workspace data** — Execute each tool against actual Notion databases and pages. Verify property types match schemas, filters return correct subsets, and pagination works for datasets over 100 records.
5. **Workflow integration** — Chain tool calls in the MCP client to build automation pipelines: query → filter → create page with properties → append block content → update status. Add error handling for rate limits and missing properties.

## Verification

- [ ] Notion integration secret is valid and set as `NOTION_API_KEY` environment variable
- [ ] Target database/page is shared with the integration via the Share menu
- [ ] `list_databases` or `search` tool returns results from the workspace
- [ ] `query_database` with compound filters returns correctly filtered results
- [ ] `create_page` creates a page with all specified properties in the correct database
- [ ] `append_blocks` adds block content (paragraphs, headings, lists, code) to an existing page
- [ ] Error responses for 401, 404, and 429 produce meaningful MCP error messages
- [ ] MCP client config persists across restarts and the server reconnects automatically
- [ ] Rate-limit backoff works correctly — sustained queries don't trigger 429s

## Monetization

- **Custom Notion MCP server for enterprise teams** — Build and deploy private MCP servers giving AI agents secure access to company Notion workspaces. Charge per-seat licensing ($50-200/seat/mo) or a flat monthly retainer ($2K-5K/mo).
- **Notion automation consulting** — Offer setup services: integrating Notion with MCP-powered AI agents, designing database schemas for automation, and building custom workflow pipelines (CRM sync, content publishing, project tracking).
- **Template marketplace** — Create and sell pre-configured MCP tool bundles for common Notion workflows: meeting-notes-to-tasks, email-to-database, research-to-knowledge-base. Package as one-click server configs ($50-200 per bundle).
- **Hosted Notion MCP gateway** — Build a SaaS platform that handles auth, multi-workspace management, rate-limit queuing, and provides a dashboard for monitoring tool usage and API consumption. Charge by API call volume or flat monthly fee.
- **Content pipeline service** — Sell automated publishing workflows where an AI agent drafts, reviews, and publishes documentation or blog posts directly into Notion databases via MCP tools. Recurring retainer model ($1K-3K/mo).