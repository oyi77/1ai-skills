---
name: linear-mcp
description: Use when linear Mcp. Use when working with linear mcp in mcp domain.
domain: mcp
author: oyi77
license: Apache-2.0
subdomain: mcp
tags:
- linear
- mcp
- mcp-server
- model-context-protocol
- tool-integration
- issue-tracking
- project-management
- graphql
version: 1.0.0
category: mcp
---


# Linear MCP Server

## When to Use

**Trigger phrases:**
- "linear mcp"
- "connect linear to claude"
- "linear issue tracking"
- "manage linear issues"
- "linear project management"
- "linear graphql"
- "linear automation"

**Use cases:**
- Connecting AI agents (Claude, Cursor, VS Code, Windsurf, Zed) to Linear for issue management
- Automating issue creation, triage, and status updates via MCP tools
- Reading Linear issues, projects, cycles, and team data programmatically
- Generating sprint reports, standup summaries, and implementation plans from Linear data
- Creating and linking GitHub PRs to Linear issues through MCP tool calls
- Building custom workflows that bridge Linear with external systems

**When NOT to use:**
- For tasks that only need raw Linear GraphQL access without MCP — use the `linear-api` skill (integrations/linear-api) for direct API calls
- When a simpler HTTP client or curl command suffices for one-off queries
- For building UIs that consume Linear data — use a dedicated GraphQL client
- When you need bulk data export or ETL pipelines — use Linear's CSV export or REST API

## Overview

The Linear MCP server provides a standardized Model Context Protocol interface to Linear's project management platform. It is hosted by Linear as a remote MCP endpoint at `https://mcp.linear.app/mcp`, using OAuth 2.1 for authentication and Streamable HTTP as the primary transport.

This server acts as a bridge between any MCP-compatible AI client (Claude Code, Claude Desktop, Cursor, VS Code, Windsurf, Zed, Codex, v0) and Linear's GraphQL API. Through MCP tools, the AI can find, create, update issues, manage projects, track cycles, post comments, and query team data — all without leaving the terminal or switching to the browser.

Linear's MCP server follows the authenticated remote MCP spec, meaning the server is centrally hosted and managed by Linear. No local server process is required — just a network connection and OAuth authentication.

**Key capabilities:**
- **Issue tools** — create, update, search, assign, and transition issues
- **Project tools** — create and query projects
- **Cycle tools** — view active cycles and issue distribution
- **Comment tools** — add comments to issues
- **Team tools** — query team membership and configuration
- **User tools** — find and assign users
- **Read-only mode** — connect to `https://mcp.linear.app/mcp/readonly` for queries only

## Architecture

```
┌─────────────────────┐     Streamable HTTP      ┌─────────────────────┐
│   AI Client         │ ◄──────────────────────► │  Linear MCP Server  │
│  (Claude, Cursor,   │      OAuth 2.1            │  mcp.linear.app     │
│   VS Code, etc.)    │                           │                     │
└─────────────────────┘                           └──────┬──────────────┘
                                                          │
                                                  GraphQL API
                                                          │
                                              ┌───────────▼──────────┐
                                              │   Linear Platform    │
                                              │  (Issues, Projects,  │
                                              │   Cycles, Teams)     │
                                              └──────────────────────┘
```

- **Transport** — Streamable HTTP (remote MCP). SSE fallback at `/sse` for legacy clients.
- **Auth** — OAuth 2.1 with dynamic client registration. Supports API key bearer tokens for non-interactive use.
- **Tools** — Predefined MCP tool definitions that map to Linear GraphQL mutations/queries.
- **Security** — Read-only mode available via `/mcp/readonly` endpoint or `read` OAuth scope.
- **Multi-workspace** — Supports separate auth contexts via `MCP_REMOTE_CONFIG_DIR`.

## Setup

### Prerequisites

- Linear account (any plan)
- Node.js 18+ (for `mcp-remote` bridge if needed)
- MCP-compatible client (Claude Code, Claude Desktop, Cursor, VS Code, Windsurf, Zed, Codex, or v0)

### Quick Start — Claude Code

```json
claude mcp add --transport http linear-server https://mcp.linear.app/mcp
```

Then start a Claude Code session and run `/mcp` to authenticate via OAuth.

### Claude Desktop / Claude.ai

**Team/Enterprise (Claude.ai):** Navigate to Settings → Connectors and connect Linear.

**Free/Pro (Claude Desktop):** Open Settings → Connectors → Add Linear connector.

### VS Code

```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.linear.app/mcp"]
    }
  }
}
```

Install via command palette: `CMD+P` → "MCP: Add Server" → Command (stdio) → paste `npx -y mcp-remote https://mcp.linear.app/mcp`.

### Cursor

Install via the [MCP Directory](https://cursor.com/docs/context/mcp/directory) — search for "Linear" and connect.

### Windsurf

```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.linear.app/mcp"]
    }
  }
}
```

Settings → Cascade → MCP Servers → Add Server.

### Zed

```json
{
  "context_servers": {
    "linear": {
      "source": "custom",
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.linear.app/mcp"],
      "env": {}
    }
  }
}
```

### Codex

```sh
codex mcp add linear --url https://mcp.linear.app/mcp
```

### Read-Only Access

```json
{
  "mcpServers": {
    "linear-readonly": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.linear.app/mcp/readonly"]
    }
  }
}
```

### Authenticating with API Key (Non-Interactive)

```sh
curl -X POST https://mcp.linear.app/mcp \
  -H "Authorization: Bearer lin_api_xxxxxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

### Multi-Workspace Configuration

```sh
# Workspace A
MCP_REMOTE_CONFIG_DIR=~/.mcp-auth/workspace-a npx mcp-remote https://mcp.linear.app/mcp

# Workspace B
MCP_REMOTE_CONFIG_DIR=~/.mcp-auth/workspace-b npx mcp-remote https://mcp.linear.app/mcp
```

### Enterprise — Okta SAML Integration

If using Okta, configure SAML for Linear first, then set the Okta Issuer URI:
```json
https://your-org.okta.com/oauth2/default
```

Enable "MCP enterprise managed authentication" on your Okta identity provider in Linear.

## Configuration

### Client Configuration Reference

| Client | Connection Method | Auth Flow | Notes |
|---|---|---|---|
| Claude Code | `claude mcp add` | OAuth | Run `/mcp` in session |
| Claude Desktop | Settings → Connectors | OAuth | Built-in UI |
| Claude.ai | Settings → Connectors | OAuth | Team/Enterprise |
| VS Code | `mcp-remote` via stdio | OAuth | npx wrapper |
| Cursor | MCP Directory | OAuth | Built-in |
| Windsurf | MCP Server Settings | OAuth | npx wrapper |
| Zed | `context_servers` JSON | OAuth | npx wrapper |
| Codex | `codex mcp add` CLI | OAuth | |
| v0 | Connections Settings | OAuth | Built-in |
| Custom | Direct HTTP to `/mcp` | OAuth or Bearer Token | Any MCP client |

### Environment Variables

For stdio-based setups (VS Code, Windsurf, Zed), no environment variables are needed — authentication is handled via the interactive OAuth flow triggered on first connection.

For direct HTTP access, pass the bearer token:
```sh
Authorization: Bearer lin_api_xxxxxxxxxxxxxxxxxxxxx
```

### Available Tools (Subject to Change)

The MCP server exposes tools for:
- **Issues** — `issues_list`, `issues_search`, `issue_create`, `issue_update`, `issue_delete`
- **Projects** — `projects_list`, `project_create`, `project_update`
- **Cycles** — `cycles_list`, `cycles_active`
- **Comments** — `comments_list`, `comment_create`
- **Teams** — `teams_list`, `team_get`
- **Users** — `users_list`, `users_search`, `user_get`

Run `tools/list` via MCP to get the exact current tool list with schemas.

## Code Examples

### Python — Linear GraphQL API via MCP

The MCP server wraps Linear's GraphQL API. These examples show how to interact directly with the API that powers the MCP tools.

```python
"""Linear GraphQL API client — the underlying API the MCP server wraps."""
import os
import requests

LINEAR_API_KEY = os.environ.get("LINEAR_API_KEY", "lin_api_xxx")
API_URL = "https://api.linear.app/graphql"
HEADERS = {
    "Authorization": LINEAR_API_KEY,
    "Content-Type": "application/json",
}


def graphql(query: str, variables: dict = None) -> dict:
    """Execute a GraphQL query against Linear API."""
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    resp = requests.post(API_URL, json=payload, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        raise RuntimeError(f"GraphQL error: {data['errors']}")
    return data["data"]


# ── List issues for a team ─────────────────────────────────────────
ISSUES_QUERY = """
query ListIssues($teamKey: String!, $first: Int) {
  team(key: $teamKey) {
    issues(first: $first) {
      nodes {
        id
        identifier
        title
        priority
        state { name }
        assignee { name }
        updatedAt
      }
    }
  }
}
"""
data = graphql(ISSUES_QUERY, {"teamKey": "BACK", "first": 25})
for issue in data["team"]["issues"]["nodes"]:
    assignee = issue["assignee"]["name"] if issue["assignee"] else "unassigned"
    print(f"{issue['identifier']} [{issue['state']['name']}] {issue['title']} — {assignee}")


# ── Create an issue ─────────────────────────────────────────────────
CREATE_ISSUE = """
mutation CreateIssue($input: IssueCreateInput!) {
  issueCreate(input: $input) {
    success
    issue { id identifier url title }
  }
}
"""
new_issue = graphql(CREATE_ISSUE, {
    "input": {
        "title": "Fix login timeout on Safari",
        "teamId": "team-uuid-here",
        "priority": 1,
        "description": "Users on Safari 17+ experience a 30-second timeout during OAuth redirect.",
        "labelIds": ["label-uuid-bug"],
    }
})
print(f"Created: {new_issue['issueCreate']['issue']['identifier']}")


# ── Update issue status ─────────────────────────────────────────────
UPDATE_STATE = """
mutation UpdateState($id: String!, $input: IssueUpdateInput!) {
  issueUpdate(id: $id, input: $input) {
    success
    issue { state { name } }
  }
}
"""
graphql(UPDATE_STATE, {
    "id": "issue-uuid-here",
    "input": {"stateId": "state-uuid-in-progress"},
})


# ── Add a comment ───────────────────────────────────────────────────
ADD_COMMENT = """
mutation AddComment($input: CommentCreateInput!) {
  commentCreate(input: $input) {
    success
    comment { id body }
  }
}
"""
graphql(ADD_COMMENT, {
    "input": {
        "issueId": "issue-uuid-here",
        "body": "Investigated root cause: Safari's Intelligent Tracking Prevention blocks the redirect cookie. Fix in progress.",
    }
})


# ── Search issues by text ───────────────────────────────────────────
SEARCH_QUERY = """
query SearchIssues($query: String!) {
  issueSearch(query: $query, first: 10) {
    nodes {
      id identifier title state { name } priority
    }
  }
}
"""
results = graphql(SEARCH_QUERY, {"query": "database connection timeout"})
for issue in results["issueSearch"]["nodes"]:
    print(f"{issue['identifier']} [{issue['state']['name']}] {issue['title']}")


# ── Get active cycle with issues ────────────────────────────────────
ACTIVE_CYCLE = """
query ActiveCycle($teamId: String!) {
  team(id: $teamId) {
    activeCycle {
      id name startsAt endsAt
      issues { nodes { identifier title state { name } assignee { name } } }
    }
  }
}
"""
cycle_data = graphql(ACTIVE_CYCLE, {"teamId": "team-uuid-here"})
cycle = cycle_data["team"]["activeCycle"]
if cycle:
    print(f"Cycle: {cycle['name']} ({cycle['startsAt']} → {cycle['endsAt']})")
    print(f"Issues: {len(cycle['issues']['nodes'])}")
```

### JavaScript — Linear GraphQL API via MCP

```javascript
/**
 * Linear GraphQL API client — the underlying API the MCP server wraps.
 */
const LINEAR_API_KEY = process.env.LINEAR_API_KEY || "lin_api_xxx";
const API_URL = "https://api.linear.app/graphql";

async function graphql(query, variables = {}) {
  const resp = await fetch(API_URL, {
    method: "POST",
    headers: {
      Authorization: LINEAR_API_KEY,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query, variables }),
  });
  if (!resp.ok) throw new Error(`HTTP ${resp.status}: ${resp.statusText}`);
  const { data, errors } = await resp.json();
  if (errors) throw new Error(`GraphQL: ${JSON.stringify(errors)}`);
  return data;
}

// ── List unassigned issues ─────────────────────────────────────────
async function listUnassignedIssues(teamKey) {
  const data = await graphql(`
    query Unassigned($teamKey: String!) {
      team(key: $teamKey) {
        issues(filter: { assignee: { isNull: true } }) {
          nodes { identifier title priority state { name } }
        }
      }
    }
  `, { teamKey });
  return data.team.issues.nodes;
}

// ── Bulk create issues from a template ────────────────────────────
async function createIssuesFromTemplate(tasks, teamId, projectId) {
  const results = [];
  for (const task of tasks) {
    const data = await graphql(`
      mutation Create($input: IssueCreateInput!) {
        issueCreate(input: $input) { success issue { identifier url } }
      }
    `, {
      input: {
        title: task.title,
        description: task.description || "",
        teamId,
        projectId,
        priority: task.priority || 2,
        estimate: task.estimate || 1,
      },
    });
    results.push(data.issueCreate.issue);
  }
  return results;
}

// ── Move issues to next state ────────────────────────────────────
async function transitionIssues(issueIds, targetStateId) {
  for (const id of issueIds) {
    await graphql(`
      mutation Transition($id: String!, $input: IssueUpdateInput!) {
        issueUpdate(id: $id, input: $input) { success }
      }
    `, { id, input: { stateId: targetStateId } });
  }
}

// Usage
(async () => {
  const unassigned = await listUnassignedIssues("BACK");
  console.table(unassigned.map(i => ({
    id: i.identifier, title: i.title, priority: i.priority, state: i.state.name,
  })));
})();
```

### TypeScript — Using MCP SDK to Call Linear

```typescript
/**
 * Example: Using the MCP client SDK to call Linear MCP server tools.
 * This demonstrates how an AI agent programmatically invokes the server.
 */
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const transport = new StdioClientTransport({
  command: "npx",
  args: ["-y", "mcp-remote", "https://mcp.linear.app/mcp"],
});

const client = new Client({ name: "linear-agent", version: "1.0.0" });
await client.connect(transport);

// List available tools
const { tools } = await client.listTools();
console.log(tools.map(t => t.name));

// Search issues
const searchResult = await client.callTool({
  name: "issues_search",
  arguments: { query: "bug priority:urgent" },
});
console.log(searchResult.content[0].text);

// Create an issue
const createResult = await client.callTool({
  name: "issue_create",
  arguments: {
    teamId: "team-uuid",
    title: "Memory leak in WebSocket handler",
    description: "Heap grows 2MB/hour under sustained load",
    priority: 1,
    labelIds: ["label-uuid-bug"],
  },
});
console.log(createResult.content[0].text);

await client.close();
```

### Bash — Direct HTTP to Linear MCP Server

```bash
# List MCP tools
curl -s -X POST "https://mcp.linear.app/mcp" \
  -H "Authorization: Bearer $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'

# Call a tool (example: search issues)
curl -s -X POST "https://mcp.linear.app/mcp" \
  -H "Authorization: Bearer $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0","id":2,"method":"tools/call",
    "params":{"name":"issues_search","arguments":{"query":"auth bug"}}
  }'
```

## Common Issues

### MCP Server Connection Drops

**Symptom:** "Connection refused" or "Tool call failed — server not responding"

**Fix:** The remote MCP server can occasionally drop idle connections. Disconnect and reconnect the server from your MCP client settings. This is a routine client-side reset and does not affect your Linear data or authentication.

### Authentication Errors (401)

**Symptom:** "Unauthorized" or "Invalid token" when calling tools

**Fix:** 
- For OAuth: Run the authentication flow again (`/mcp` in Claude Code, or reconnect in client settings)
- Clear stale auth cache: `rm -rf ~/.mcp-auth` then re-authenticate
- For API key: Verify the key has the correct scopes (issues:read, issues:write, etc.)
- Regenerate the key at Linear → Settings → API → Personal API Keys

### Internal Server Error on Connection

**Symptom:** "Internal Server Error" when first connecting

**Fix:** Clear saved auth info and re-authenticate:
```bash
rm -rf ~/.mcp-auth
```
Also ensure Node.js 18+ is installed (required for `mcp-remote`).

### "Team not found" Errors

**Symptom:** Tools return errors about non-existent teams or projects

**Fix:** 
- Team identifiers are case-sensitive — verify the team key in your Linear workspace
- Use the `teams_list` tool to get the exact team IDs and keys
- For UUID-based queries, ensure you're passing the 36-character UUID, not the 4-character team key

### WSL / Windows Issues

**Symptom:** Connection fails when using WSL on Windows

**Fix:** Use the SSE fallback transport:
```json
{
  "mcpServers": {
    "linear": {
      "command": "wsl",
      "args": ["npx", "-y", "mcp-remote", "https://mcp.linear.app/sse", "--transport", "sse-only"]
    }
  }
}
```

### Rate Limiting (429)

**Symptom:** "Rate limit exceeded" on batch operations

**Fix:** 
- Reduce batch operations to 5 simultaneous calls at a time
- The MCP server handles retries automatically for most cases
- If you see sustained 429s, add delays between batches
- Linear's API rate limit is 60 requests per minute for most plans

### Multi-Workspace Auth Conflicts

**Symptom:** Tools operate on the wrong workspace after switching

**Fix:** Each workspace needs its own auth context:
```bash
export MCP_REMOTE_CONFIG_DIR=~/.mcp-auth/workspace-b
npx mcp-remote https://mcp.linear.app/mcp
```
Authenticate each workspace separately.

## Monetization

The Linear MCP server is free to use, but the value it unlocks can be monetized through the following strategies:

### 1. AI Automation Consulting ($500–$5,000/project)

Offer a service that connects client teams' Linear workspaces to AI agents (Claude Code, Cursor). The deliverable:
- Configure MCP connections for all team members
- Create CLAUDE.md files with Linear workflows, team conventions, and label schemas
- Build custom MCP tool wrappers for client-specific workflows (auto-triage, sprint reports)
- Train teams on prompt patterns for Linear MCP

**Pitch:** "Reduce sprint admin by 2 hours/developer/week — issues auto-transition, standup notes become comments, PRs link to tickets automatically."

### 2. Custom Workflow Automation ($1,000–$10,000/engagement)

Build and deploy custom MCP-driven automation for Linear:
- **Auto-triage bots** — new issues are assessed, labeled, and assigned via MCP tools
- **Sprint report generators** — weekly cycle summaries posted to Slack/Teams
- **Cross-platform syncing** — sync Linear with GitHub, Jira, Notion, or internal tools
- **SLI/SLO dashboards** — track issue lifecycle metrics (time-to-triage, cycle time, throughput)

### 3. MCP Plugin/Extension Development ($2,000–$15,000)

Build custom MCP servers that extend Linear's MCP with additional capabilities:
- Wrap Linear's full GraphQL API with granular tool definitions
- Add resource endpoints for Linear data (URIs for issues, projects, cycles)
- Create specialized tools for your domain (e.g., "roadmap_plan", "sprint_retrospective")

### 4. Internal Productivity Tool ($saved hours)

Within your own team or company, MCP-connecting Linear saves significant time:
- Eliminates context-switching between terminal and browser for issue operations
- Automates PR-to-issue linking via branch naming conventions
- Auto-generates implementation plans from Linear issues
- Developers using Linear + MCP report closing issues ~25% faster by eliminating manual status updates

### 5. Training & Content ($500–$3,000/session)

Create and sell:
- Workshops: "AI-Enhanced Project Management with Linear + MCP"
- Video courses: "Automate Your Sprint with Claude Code and Linear"
- Templates: Ready-made CLAUDE.md files and MCP configs for common Linear workflows
- Playbooks: "10 Linear Automations Every Engineering Team Needs"

## Common Patterns

### Auto-Triage Pipeline

```python
# Example: New issue with "bug" label gets auto-assigned to on-call
# Triggered via webhook or scheduled MCP tool call
def auto_triage(issue_id: str):
    # 1. Fetch issue details via MCP
    issue = mcp_call("issues_get", {"id": issue_id})
    # 2. Detect labels and determine action
    if "bug" in [l["name"] for l in issue["labels"]]:
        oncall = find_oncall_engineer()
        mcp_call("issue_update", {
            "id": issue_id,
            "assigneeId": oncall["id"],
            "priority": 1,
        })
```

### Cycle End Sprint Report

```
Agent: Summarize the completed cycle for the Backend team
→ MCP calls: cycles_list, issues_list per cycle
→ Output: markdown summary with completion stats, top contributors, blocker analysis
```

### Implementation Plan Generator

```
Agent: Break this spec into Linear issues with milestones
→ MCP calls: project_create, issue_create (bulk), issue_update (dependencies)
→ Output: structured project with milestones and task dependencies
```

## Process

1. **Audit** — Check existing Linear workspace setup: teams, projects, cycles
2. **Connect** — Configure the MCP server in the appropriate client (see Setup)
3. **Verify** — Run `/mcp` to authenticate, then test with a simple query: "List my assigned issues"
4. **Integrate** — Add Linear context to project CLAUDE.md (team key, label conventions, estimate scale)
5. **Automate** — Build workflow-specific prompts for common patterns (triage, standup, sprint reports)
6. **Review** — Validate MCP responses against Linear web UI for correctness

## Verification

- [ ] MCP server connected and authenticated successfully
- [ ] Can list teams, issues, projects, and cycles via MCP tools
- [ ] Can create, update, and transition issues
- [ ] Can add comments to issues
- [ ] Read-only endpoint works if needed (`/mcp/readonly`)
- [ ] Multi-workspace setup tested (if applicable)
- [ ] CLAUDE.md updated with Linear context
- [ ] Common workflow prompts tested end-to-end

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll just open Linear in the browser" | You lose AI context. MCP keeps the agent aware of your issues, enabling automated triage, PR linking, and status updates without leaving the terminal. |
| "Our CI already handles issue transitions" | CI only catches commits. MCP enables before/after automation: planning, estimation, assignment, review progression, and sprint reporting. |
| "OAuth setup is a hassle" | Linear's MCP uses OAuth 2.1 with dynamic client registration — one-time setup, zero config maintenance. For CI, use a bearer API key. |
| "I only need read access" | Use `/mcp/readonly` or restrict the OAuth scope to `read`. Full separation without a separate server config. |
| "MCP is Claude-only" | Linear's MCP server works with Cursor, VS Code, Windsurf, Zed, Codex, v0, and any MCP-compatible client. It's an open protocol. |
| "The SSE endpoint is enough" | SSE is deprecated. Use the Streamable HTTP endpoint at `/mcp` — it's faster, handles auth better, and is the recommended path. |
