---
name: github-mcp
description: Use when mCP server for GitHub automation. Manage repos, issues, PRs,
  and workflows through the Model Context Protocol. Use when working with github mcp.
domain: mcp
author: oyi77
license: Apache-2.0
subdomain: mcp
tags:
- github
- mcp
- mcp-server
- model-context-protocol
- tool-integration
version: 1.0.0
category: mcp
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


## When NOT to Use

- When a simpler HTTP client would suffice
- For internal tools that do not need cross-platform compatibility
- When the tool is used by a single agent in a single context


## Overview

GitHub MCP is a Model Context Protocol server that bridges AI agents with the GitHub API. By exposing repository operations, issue tracking, pull request management, and workflow automation as standardized MCP tools and resources, it allows LLMs to interact with GitHub programmatically — reading code, creating issues, reviewing PRs, and triggering CI/CD — all through natural language or structured tool calls.

The server wraps GitHub's REST and GraphQL APIs behind the MCP interface, handling authentication, pagination, rate limiting, and error formatting so that the AI agent never deals with raw HTTP responses. Common operations (listing issues, creating PRs, searching code, managing labels) become atomic tool calls with typed JSON Schema parameters, while frequently accessed data (repo contents, issue comments, workflow runs) is available through MCP resource URIs for efficient read access.

In the broader MCP ecosystem, GitHub-MCP plays a key role for developer-tooling agents. It pairs naturally with file-system MCP servers (for local code changes) and shell-execution MCP servers (for running tests), giving an AI agent end-to-end capability to read code, create PRs, review changes, and merge — all within a single orchestrated session.

Both Python (via PyGithub) and Node.js/TypeScript (via Octokit) ecosystems are fully supported. The choice depends on your MCP host's runtime: TypeScript servers are more common for Claude Desktop integrations, while Python servers integrate naturally with FastAPI-based agent backends or Jupyter-based workflows.

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

## Setup & Configuration

### Python

```bash
pip install pygithub mcp
```

### Node.js

```bash
npm install @octokit/rest @modelcontextprotocol/sdk
```

### GitHub Token

1. Go to GitHub Settings → **Developer settings** → **Personal access tokens** → **Fine-grained tokens**
2. Click **Generate new token**, select the repo(s) you need, and choose scopes:
   - `repo` — Full control of private repositories
   - `issues` — Issue management
   - `pull_requests` — Pull request management
   - `workflows` — Update GitHub Action workflows
3. Copy the token and set it as an environment variable:

```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
```

### MCP Client Registration

Add the server definition to your MCP client configuration (e.g., `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "github": {
      "command": "node",
      "args": ["path/to/your-github-mcp-server.mjs"],
      "env": {
        "GITHUB_TOKEN": "ghp_xxxxxxxxxxxx"
      }
    }
  }
}
```

## Anti-Rationalization Table

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



## Code Examples

### Python (PyGithub)

```python
from github import Github

# Authenticate with personal access token
g = Github("ghp_xxxxxxxxxxxx")

# List open issues
repo = g.get_repo("owner/repo")
for issue in repo.get_issues(state="open"):
    print(f"#{issue.number}: {issue.title}")

# Create a new issue
issue = repo.create_issue(
    title="Bug: login fails on empty input",
    body="## Steps to reproduce\n1. Open login page\n2. Submit empty form",
    labels=["bug", "priority-high"],
)
print(f"Created issue #{issue.number}")
```

### JavaScript (Octokit)

```javascript
import { Octokit } from "@octokit/rest";

const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });

// List open pull requests
const { data: pulls } = await octokit.pulls.list({
  owner: "owner",
  repo: "repo",
  state: "open",
});
pulls.forEach(pr => console.log(`#${pr.number}: ${pr.title}`));

// Create a pull request
await octokit.pulls.create({
  owner: "owner",
  repo: "repo",
  title: "Fix login validation",
  head: "fix/login-validation",
  base: "main",
  body: "Adds input validation to the login form.",
});
```

### MCP Tool Wrapping GitHub API

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { Octokit } from "@octokit/rest";

const server = new McpServer({ name: "github-mcp", version: "1.0.0" });
const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });

server.tool("create_issue", {
  owner: z.string(),
  repo: z.string(),
  title: z.string(),
  body: z.string().optional(),
  labels: z.array(z.string()).optional(),
}, async ({ owner, repo, title, body, labels }) => {
  const { data } = await octokit.issues.create({ owner, repo, title, body, labels });
  return { content: [{ type: "text", text: `Created issue #${data.number}` }] };
});
```

## Process

1. **Configure credentials** — Generate a GitHub personal access token with appropriate scopes (repo, issues, pull_requests). Set `GITHUB_TOKEN` in your environment or MCP client config file.

2. **Register the server** — Add the GitHub MCP server to your client configuration (`claude_desktop_config.json`, `~/.config/agents/servers.json`, or the equivalent for your MCP client).

3. **Define tool schemas** — Map each GitHub operation to an MCP tool with Zod/JSON Schema definitions for parameters. Cover at minimum issues, PRs, repos, and workflow actions.

4. **Implement handlers** — Write handler functions that call the GitHub API via Octokit (JS) or PyGithub (Python), then transform responses into MCP `TextContent` blocks.

5. **Test tool invocations** — Start the MCP server and call each tool from the client. Verify correct input parsing, API response formatting, and error propagation for 404/403 responses.

6. **Add resource endpoints** — Expose GitHub data as MCP resources (e.g., `github://owner/repo/issues`, `github://owner/repo/pulls/{number}`) for read access without tool calls.

7. **Monitor and iterate** — Check server logs for rate limit warnings or auth errors. Adjust token scopes or pagination limits as usage scales.

## Common Issues & Troubleshooting

| Problem | Solution |
|---|---|
| `401 Bad credentials` | Token is invalid or expired. Generate a new fine-grained PAT at `github.com/settings/tokens` and update `GITHUB_TOKEN`. |
| `403 API rate limit exceeded` | Unauthenticated requests are limited to 60/hr. Add a valid token to raise the limit to 5,000/hr. For higher volume, use a GitHub App installation token. |
| `404 Not Found` | The token may lack access to the repo. Verify the token has `repo` scope for private repos, or that the owner/repo name is correct. |
| `GraphQL: \"Resource protected by organization SAML\"` | Authorize the token under your org's SSO at `github.com/settings/tokens`. Each token must be SSO-approved per-org. |
| Tool hangs or times out on large results | Large repos need pagination. Pass `per_page=100` and iterate with the `Link` header or Octokit's `paginate` helper. |
| `Module not found: @modelcontextprotocol/sdk` | The MCP SDK is not installed. Run `npm install @modelcontextprotocol/sdk` in the server directory, or `pip install mcp` for Python. |

## Verification

- [ ] GitHub token has correct scopes (repo, issues, pull_requests, workflows) for your intended operations
- [ ] MCP server starts without errors and registers all tools in the client's tool list
- [ ] Each tool can be invoked and returns properly formatted MCP TextContent responses
- [ ] API errors (404, 403, rate limit) are caught and surfaced as readable MCP error messages, not crashes
- [ ] Pagination works for list operations that return more than one page of results
- [ ] Resource URIs resolve correctly for at least one issue and one pull request
- [ ] Empty or null inputs are handled gracefully without uncaught exceptions
- [ ] Environment variables and authentication are documented in the server README or config file

## Monetization

- **Managed MCP server hosting** — Offer a hosted GitHub MCP server as a SaaS add-on for teams that don't want to self-host. Charge per-seat monthly with tiered plans based on API call volume and team size.
- **Custom MCP tool development** — Build bespoke GitHub MCP servers for enterprise clients: custom workflow triggers, compliance checks, auto-labeling bots, and secret-scanning gates exposed as MCP tools. $5K-20K per engagement.
- **GitHub Actions + MCP integration consulting** — Help teams wire MCP tools into GitHub Actions pipelines for AI-assisted code review, auto-issue triage, and PR management. Package as a 2-week accelerator at $8K.
- **Open-source Pro tier** — Release the core MCP server as open-source with a paid "Pro" edition adding premium tools (dependency graph analysis, merge conflict prediction, SLA breach alerts). $29/mo per org.
- **Internal tool accelerators** — Sell pre-built MCP server configurations for common enterprise workflows (onboarding automation, release management gates, security compliance checks) as a one-time implementation fee plus monthly retainer.