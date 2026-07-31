---
name: resend-mcp
description: Resend Mcp. Use when working with resend mcp in mcp domain.
domain: mcp
author: oyi77
license: Apache-2.0
subdomain: mcp
tags:
- mcp
- mcp-server
- model-context-protocol
- resend
- tool-integration
version: 1.0.0
---
# Resend Mcp

## When to Use

**Trigger phrases:**
- "resend mcp"
- "Help me with resend mcp"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


## When NOT to Use

- When a simpler HTTP client would suffice
- For internal tools that do not need cross-platform compatibility
- When the tool is used by a single agent in a single context


## Overview

Resend Mcp implements a Model Context Protocol server for Model Context Protocol.

Resend is a modern email API that provides reliable email delivery for transactional, marketing, and broadcast use cases. It handles domain verification (SPF, DKIM, DMARC), bounce and complaint processing, and delivery analytics out of the box. The Resend MCP server wraps this API into model-context-protocol tools, allowing AI agents to send and track emails as part of autonomous workflows.

The MCP server exposes a `send-email` tool with typed parameters for recipient, subject, body, and optional configuration (HTML content, attachments, CC/BCC, reply-to headers). Agents can integrate email delivery into their decision loops — sending verification codes, lead follow-ups, alert notifications, or report summaries without leaving the MCP conversation. The server also supports SSE transport for production deployments behind reverse proxies with TLS termination.

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


### Python installation
```bash
pip install resend-sdk mcp
```

### Node.js installation
```bash
npm install resend @modelcontextprotocol/sdk
# or
pnpm add resend @modelcontextprotocol/sdk
```

### Environment variables
```bash
export RESEND_API_KEY="re_xxxxxxxxxxxxx"
```
Add to your `.env` file for local development.

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

## Workflow

1. **Set up Resend account** — Sign up at resend.com, verify your sending domain by adding the required DNS records (SPF, DKIM, DMARC). Generate an API key from the dashboard.
2. **Install MCP server dependencies** — Add the Resend SDK and MCP server SDK to your project via pip (Python) or npm (Node.js). Configure environment variables for the API key.
3. **Define the email tool** — Register an MCP tool with a `send-email` action. Specify typed parameters: recipient, subject, body, and optional fields (CC, attachments, HTML content).
4. **Wire the Resend client** — Instantiate the Resend client inside the tool handler, call `resend.emails.send()` with the validated parameters, and return the result or error to the MCP client.
5. **Register and test with an MCP client** — Add the server to your MCP client config (Claude Desktop, Cursor, etc.). Send a test email and verify delivery in the Resend logs.
6. **Handle delivery feedback** — Configure Resend webhooks for bounce, complaint, and delivery events. Route these through MCP resources so your agent can query delivery status.
7. **Deploy to production** — Run the MCP server with SSE transport behind a reverse proxy (nginx, Caddy) with TLS. Monitor uptime and email delivery health via dashboards.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I will just use curl" | MCP handles auth, retries, streaming, and type safety. Use the SDK. |
| "One mega-server is simpler" | Single-responsibility servers are easier to debug and maintain. |
| "MCP is just a wrapper" | MCP enables cross-platform tool sharing. It is infrastructure, not overhead. |
| "Resend is just for transactional email" | Resend supports transactional, marketing, and broadcast emails. The MCP server abstracts all of them behind a unified tool interface. |
| "I should build my own email API" | Resend handles deliverability, DKIM, bounce handling, and domain warmup. Building these in-house is weeks of work. |
| "MCP tools are only for text" | MCP tools can integrate full email capabilities — attachments, HTML templates, CC/BCC, reply-to headers, and delivery webhooks. |

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

### Python — Send email via Resend SDK

```python
import os
from resend import Resend

resend = Resend(api_key=os.environ["RESEND_API_KEY"])

r = resend.emails.send({
    "from": "onboarding@resend.dev",   # Use your verified domain in production
    "to": ["user@example.com"],
    "subject": "Hello from Resend MCP",
    "text": "This email was sent through the Resend API.",
})
print(f"Email sent: {r['id']}")
```

### JavaScript/Node.js — Send email via Resend SDK

```javascript
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

const { data, error } = await resend.emails.send({
  from: 'onboarding@resend.dev',
  to: ['user@example.com'],
  subject: 'Hello from Resend MCP',
  text: 'This email was sent through the Resend API.',
});

if (error) {
  console.error('Send failed:', error);
} else {
  console.log('Email sent:', data.id);
}
```

### Registering a Resend MCP tool with email capability

```typescript
import { McpServer } from "@modelcontextprotocol/sdk";
import { z } from "zod";
import { Resend } from "resend";

const resend = new Resend(process.env.RESEND_API_KEY);

const server = new McpServer({ name: "email-tools", version: "1.0.0" });

server.tool(
  "send-email",
  {
    to: z.string().describe("Recipient email address"),
    subject: z.string().describe("Email subject line"),
    text: z.string().describe("Email body text"),
  },
  async ({ to, subject, text }) => {
    const { data, error } = await resend.emails.send({
      from: "noreply@yourdomain.com",
      to: [to],
      subject,
      text,
    });
    if (error) return { content: [{ type: "text", text: `Error: ${error}` }] };
    return { content: [{ type: "text", text: `Email sent: ${data.id}` }] };
  }
);
```


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run resend mcp workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results
1. **Configure SDK** — Set up Resend SDK with API key from dashboard, configure sender domain verification and DNS records.
1. **Define tool schema** — Create or extend MCP tool definitions with typed input/output schemas using zod (TS) or pydantic (Python).
1. **Test send** — Execute a test email send through the MCP tool to verify end-to-end: client → MCP server → Resend API → inbox delivery.
1. **Monitor & iterate** — Check delivery logs in Resend dashboard, handle bounce/complaint webhooks, and update tool parameters as needed.

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings

## Common Issues & Troubleshooting

| Problem | Solution |
|---|---|
| "Resend API key not recognized" | Verify `RESEND_API_KEY` is set in environment and the key is active in the Resend dashboard. Keys start with `re_`. |
| "MCP tool returns empty response" | Ensure the transport (stdio/SSE) is properly configured on both server and client sides. Check for port conflicts. |
| "Email delivery delayed or dropped" | Confirm sender domain is verified in Resend. SPF, DKIM, and DMARC records must be configured for the sending domain. |
| "Rate limit exceeded (429)" | Resend defaults to 5 req/s on free tier. Implement exponential backoff retry logic in your MCP tool handler. |
| "Connection refused on SSE transport" | The MCP server process may not be running. Verify the process is alive and listening on the configured port. Use `ps aux | grep mcp` to confirm. |
| "TypeError in tool schema validation" | Ensure all JSON Schema definitions in your tool parameters match the actual types sent. Use `zod` for TypeScript or `pydantic` for Python schema validation. |

## Monetization

- **Custom email MCP server for clients** — Build and host a private Resend MCP server for businesses that need transactional email, marketing campaigns, and newsletter sending from their AI agents. Charge $50-200/mo per deployment.
- **Email automation SaaS** — Offer a ready-to-use Resend MCP integration as a service, combining it with templating and analytics. Tiered pricing ($29-99/mo) based on email volume.
- **Consulting: domain deliverability setup** — Help clients configure SPF, DKIM, DMARC, and warm up sending domains for reliable email delivery through Resend. One-time $500-1500 per domain.
- **MCP server marketplace listing** — Package the Resend MCP server as a plug-and-play tool on MCP marketplaces. Charge per download or offer premium features (HTML templates, attachment support, bulk send).
- **White-label email API wrapper** — White-label the Resend integration for agencies that need branded email infrastructure for their clients. Monthly retainer model ($200-500/mo).