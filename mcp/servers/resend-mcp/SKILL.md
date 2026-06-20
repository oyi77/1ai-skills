---
name: resend-mcp
description: Resend Mcp. Use when working with resend mcp in mcp domain.
domain: mcp
tags:
- mcp
- mcp-server
- model-context-protocol
- resend
- tool-integration
---
## When to Use

**Trigger phrases:**
- "resend mcp"
- "Help me with resend mcp"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

## Resend Mcp

MCP server for Resend email

### Usage

```
/resend-mcp <task>
```

### Features

- Automated execution
- Error handling
- Result validation

## How to Use

1. Get a Resend API key from resend.com/api-keys
2. Configure the MCP server with RESEND_API_KEY
3. Use tools to send transactional emails with templates

## Available Tools

| Tool | Description |
|------|-------------|
| `send_email` | Send an email to recipients |
| `create_contact` | Add a contact to an audience |
| `list_contacts` | List contacts with pagination |
| `send_batch` | Send multiple emails in a single API call |

## Common Patterns

- Use HTML templates for consistent email formatting
- Send batch emails to reduce API calls for bulk operations
- Use audiences to segment contacts by purpose
- Set reply-to addresses for two-way communication

## When NOT to Use

- When email sending must comply with CAN-SPAM or GDPR requirements
- When the email content is transactional and requires delivery guarantees
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- MCP server does not validate email addresses before sending
- Agent does not handle bounce and complaint webhooks from Resend
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Email addresses are validated before send operations
- [ ] Bounce and complaint webhooks are processed and acted upon
- [ ] All required outputs generated
- [ ] Success criteria met

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
