---
name: stripe-mcp
description: MCP server for Stripe payments. Process payments, manage subscriptions, and handle billing via standardized protocol. Use when working with stripe mcp.
domain: mcp
author: oyi77
license: Apache-2.0
subdomain: mcp
tags:
- mcp
- mcp-server
- model-context-protocol
- stripe
- tool-integration
version: 1.0.0
---
# Stripe Mcp

## When to Use

**Trigger phrases:**
- "stripe mcp"
- "Help me with stripe mcp"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


## When NOT to Use

- When a simpler HTTP client would suffice
- For internal tools that do not need cross-platform compatibility
- When the tool is used by a single agent in a single context


## Overview

The Stripe MCP server bridges AI agents with the Stripe payment infrastructure through the Model Context Protocol. Hosted at `https://mcp.stripe.com`, it exposes a comprehensive set of tools that let LLMs create customers, manage subscriptions, process payments, search documentation, and interact with virtually every Stripe API endpoint — all through natural language or structured tool calls.

The server supports two authentication modes: **OAuth** for interactive MCP clients (Cursor, Claude Code, VS Code, ChatGPT) and **restricted API key** bearer tokens for autonomous agent deployments. This flexibility makes it suitable for both human-in-the-loop workflows and fully automated agentic pipelines where the AI operates independently within defined scopes.

Key capabilities include customer lifecycle management (create, retrieve, list, update), payment operations (charges, refunds, PaymentIntents, Checkout Sessions), subscription and billing management (invoices, subscriptions, coupons), product catalog management (products, prices, promotion codes), Stripe Treasury operations (financial accounts, transfers, payouts), Issuing (cards, authorizations, cardholders), dispute handling, webhook endpoint management, and built-in documentation search through `search_stripe_documentation` and `search_stripe_resources`.

## Architecture

- **Server** — MCP-compliant server exposing tools and resources
- **Transport** — stdio or HTTP transport layer
- **Tools** — Callable functions with JSON Schema definitions
- **Resources** — Readable data sources with URI-based access

## Setup

1. **Install the MCP client** — Add the Stripe MCP server URL to your MCP client configuration (see Configuration below). No npm/pip install required — Stripe hosts the server at `https://mcp.stripe.com`.
2. **Authenticate** — Use OAuth via the browser consent flow (recommended for interactive clients) or create a restricted API key from the Stripe Dashboard (`Developers → API keys → Create restricted key`) for autonomous agents.
3. **Restrict scope** — For production use, create a restricted key that only allows the specific operations your agent needs (e.g., read-only access, or only customer and subscription operations).
4. **Verify connectivity** — Run `claude /mcp` (Claude Code) or check your client's MCP server list. Call `get_stripe_account_info` as a smoke test.
5. **Test a full flow** — Create a test customer, list products, or generate a Checkout Session link in a sandbox environment before deploying agents to live mode.

## Configuration

### Claude Code

```bash
claude mcp add --transport http stripe https://mcp.stripe.com/
```
After adding, authenticate via the OAuth flow: `claude /mcp`

### Cursor

Add to `~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "stripe": {
      "url": "https://mcp.stripe.com"
    }
  }
}
```

### VS Code

Add to `.vscode/mcp.json` in your workspace:
```json
{
  "servers": {
    "stripe": {
      "type": "http",
      "url": "https://mcp.stripe.com"
    }
  }
}
```

### OpenAI Responses API (Autonomous Agents)

Pass a restricted API key in the Authorization header:
```json
{
  "stripe": {
    "url": "https://mcp.stripe.com",
    "headers": {
      "Authorization": "Bearer rk_restricted_key_here"
    }
  }
}
```

### Connected Accounts (Stripe Connect)

Pass the `Stripe-Account` header to make calls as a connected account:
```json
{
  "mcpServers": {
    "stripe": {
      "url": "https://mcp.stripe.com",
      "headers": {
        "Authorization": "Bearer rk_...",
        "Stripe-Account": "acct_connected_account_id"
      }
    }
  }
}

## Integration

- Compatible with Claude, Cursor, and other MCP clients
- Supports streaming responses for large payloads
- Handles errors with standard MCP error codes

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I will just use curl" | MCP handles auth, retries, streaming, and type safety. Use the SDK. |
| "One mega-server is simpler" | Single-responsibility servers are easier to debug and maintain. |
| "MCP is just a wrapper" | MCP enables cross-platform tool sharing. It is infrastructure, not overhead. |
| "I don't need OAuth, my API key is fine in code" | Embedded API keys leak via logs, git history, and CI output. OAuth limits scope per session. |
| "Stripe MCP is just for read-only queries" | The server exposes write tools (`stripe_api_write`) that can create charges, modify subscriptions, and trigger payouts. Treat it as a write-capable integration. |
| "My agent only needs one Stripe operation" | MCP exposes dozens of interrelated tools. Scoping with restricted keys prevents accidental escalation beyond the intended workflow. |

## Code Examples

### Python — Create a Customer and Payment Link via MCP

```python
import httpx
import os

STRIPE_MCP_URL = "https://mcp.stripe.com"
API_KEY = os.environ["STRIPE_RESTRICTED_KEY"]

def call_stripe_mcp(tool_name: str, arguments: dict) -> dict:
    """Call a Stripe MCP tool and return the result."""
    with httpx.Client() as client:
        response = client.post(
            STRIPE_MCP_URL,
            json={
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {"name": tool_name, "arguments": arguments},
                "id": 1,
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}",
            },
        )
        response.raise_for_status()
        return response.json()

# Create a customer
result = call_stripe_mcp("create_customer", {
    "name": "Acme Corp",
    "email": "billing@acme.com",
    "metadata": {"source": "ai-agent"},
})
print(f"Customer: {result['result']['content'][0]['text']}")

# Create a payment link
link = call_stripe_mcp("stripe_api_write", {
    "method": "post",
    "path": "/v1/payment_links",
    "body": {
        "line_items": [{"price": "price_abc123", "quantity": 1}],
    },
})
print(f"Payment link: {link['result']['content'][0]['text']}")
```

### JavaScript — Retrieve Account Info and List Customers

```javascript
const STRIPE_MCP_URL = "https://mcp.stripe.com";
const API_KEY = process.env.STRIPE_RESTRICTED_KEY;

async function callStripeMcp(toolName, arguments) {
  const response = await fetch(STRIPE_MCP_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${API_KEY}`,
    },
    body: JSON.stringify({
      jsonrpc: "2.0",
      method: "tools/call",
      params: { name: toolName, arguments },
      id: 1,
    }),
  });
  return response.json();
}

// Verify account connection
const account = await callStripeMcp("get_stripe_account_info", {});
console.log("Account:", JSON.parse(account.result.content[0].text).id);

// List recent customers
const customers = await callStripeMcp("stripe_api_read", {
  method: "get",
  path: "/v1/customers",
  params: { limit: 5 },
});
const data = JSON.parse(customers.result.content[0].text);
console.log(`Found ${data.data.length} customers`);
```


## Common Issues & Troubleshooting

| Problem | Solution |
|---|---|
| OAuth consent window doesn't open | Verify your MCP client supports OAuth redirects. For CLI tools, use `claude mcp add --transport http stripe https://mcp.stripe.com/` which handles the flow interactively. |
| "401 Unauthorized" with restricted key | Check the key has the necessary permissions. Go to Stripe Dashboard → Developers → API keys → edit the restricted key and enable the required resources. |
| MCP tool returns empty data | The Stripe MCP routes API calls to your Stripe account's data. If the account is new, there may be no customers or charges yet. Try `get_stripe_account_info` which always returns data. |
| Rate limiting errors | Stripe API rate limits apply. For bulk operations, add delays between calls or use Stripe's pagination parameters (`limit`, `starting_after`). |
| CORS errors from browser-based MCP clients | Stripe's MCP endpoint is designed for backend-to-backend communication. Use a server-side agent runtime rather than calling directly from browser JS. |
| Connected account requests fail | Ensure both `Authorization` and `Stripe-Account` headers are passed. The connected account must be active, and the key must have the necessary Connect permissions. |

## Process

1. **Define scope** — Determine which Stripe operations your agent needs (read-only reporting, customer management, subscription billing, payment link generation). Create a restricted API key with matching permissions.
2. **Configure client** — Register the Stripe MCP server in your client's configuration with OAuth or a bearer token. Test with `get_stripe_account_info`.
3. **Build tool calls** — Identify the MCP tools that map to your workflow. Use `stripe_api_search` to discover API methods, or `search_stripe_documentation` to find implementation guidance.
4. **Implement agent workflow** — Chain MCP tool calls to complete a business flow (e.g., create customer, create subscription, generate invoice, send payment link).
5. **Handle errors** — Parse MCP error responses for Stripe-specific error codes (`card_declined`, `insufficient_funds`, `expired_card`). Implement retry logic with exponential backoff for transient failures.
6. **Test in sandbox** — Run the full workflow against Stripe test mode (default for restricted keys). Verify idempotency by replaying requests.
7. **Deploy and monitor** — Switch to live mode with a tightly-scoped restricted key. Monitor the MCP server's response times and error rates. Set up alerts for failed payment operations.

## Verification

- [ ] Stripe MCP server responds to `get_stripe_account_info` with valid account data
- [ ] OAuth flow completes successfully (or restricted key authenticates without errors)
- [ ] Read operations (`stripe_api_read`, `list_customers`) return expected data
- [ ] Write operations (`create_customer`, `create_subscription`) create resources in Stripe Dashboard
- [ ] Error handling catches Stripe API errors (invalid requests, authentication failures, resource not found)
- [ ] Idempotency works — replaying the same request does not create duplicate resources
- [ ] Restricted key permissions are scoped to the minimum required operations
- [ ] Connected account header (`Stripe-Account`) works if using Stripe Connect

## Monetization

- **Agentic billing assistant** — Build and sell an AI agent that handles subscription management, invoice creation, dunning follow-ups, and payment retry logic for SaaS companies. Charge a monthly subscription ($200–$500/mo per client).
- **Revenue intelligence dashboard** — Use MCP read tools to create an AI-powered analytics layer that answers natural language questions about revenue, churn, MRR, and customer trends. Offer as a SaaS add-on ($50–$200/mo).
- **Automated refund and dispute handler** — Build a human-in-the-loop agent that triages refund requests, checks policy compliance, and processes approved refunds through the MCP. Sell to e-commerce merchants ($0.50–$1.00 per transaction or flat $300/mo).
- **Stripe onboarding concierge** — Create an agent that guides new Stripe users through setup: creating products, setting up prices, configuring webhooks, and building a Checkout flow. Charge per onboarding ($500–$2,000 flat fee).
- **Embedded payment agent for SaaS platforms** — Offer Stripe MCP as a white-labeled payment agent inside your SaaS platform, letting your customers manage billing through natural language. Monetize via platform markup on Stripe fees (0.5–1% uplift).