---
name: stripe-mcp
description: MCP server for Stripe payments
---
## Stripe Mcp

MCP server for Stripe payments

### Usage

```
/stripe-mcp <task>
```

### Features

- Automated execution
- Error handling
- Result validation

## How to Use

1. Get a Stripe API key from dashboard.stripe.com/apikeys
2. Configure the MCP server with STRIPE_SECRET_KEY
3. Use tools to manage customers, subscriptions, and payments

## Available Tools

| Tool | Description |
|------|-------------|
| `list_customers` | List customers with search and pagination |
| `create_customer` | Create a new customer record |
| `create_checkout_session` | Generate a Stripe Checkout URL |
| `list_subscriptions` | List active subscriptions |
| `create_invoice` | Create and send an invoice |
| `list_charges` | List payment charges with filters |

## Common Patterns

- Use Checkout Sessions for hosted payment pages
- Create customers before subscriptions to track billing
- Use webhooks for real-time payment event processing
- Idempotency keys prevent duplicate charges on retries

## When NOT to Use

- When payment processing requires PCI-DSS Level 1 compliance
- When the Stripe integration handles recurring billing with complex tax calculations
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- MCP server does not verify webhook signatures from Stripe
- Agent does not handle Stripe API versioning correctly
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Webhook signatures are verified for authenticity
- [ ] API versioning is handled consistently
- [ ] All required outputs generated
- [ ] Success criteria met

