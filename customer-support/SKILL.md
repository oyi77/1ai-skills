# customer-support Skill

> **Framework Agnostic** - This skill works with ANY AI agent (OpenCode, OpenClaw, Claude Desktop, custom agents, etc.)
> 
> **How to Use**: Read this file and follow the instructions. No special loading required.

## What It Does

Automated customer support via browser - email responses, chat interactions, ticket management, FAQ handling, and escalation workflows.

## When to Use

- Handle customer support emails
- Process support tickets
- Generate FAQ responses
- Escalate complex issues
- Maintain support knowledge base

## Key Capabilities

- **Email Automation**: Check and respond to support emails via Gmail
- **Ticket Triage**: Classify and prioritize incoming tickets
- **Response Generation**: Generate context-aware responses via ChatGPT
- **FAQ Handling**: Answer common questions automatically
- **Escalation**: Route complex issues to human review
- **Logging**: Track all interactions in CRM

## Browser Workflows

### Email Support Automation

1. Navigate: https://mail.google.com (Gmail)
2. Search: unread support emails (label:support)
3. Classify: urgency and type
4. Draft: response via ChatGPT
5. Send: or flag for review
6. Log: in CRM (Notion/Sheets)

### Ticket Processing

1. Navigate: support dashboard (e.g., Zendesk, Freshdesk)
2. Fetch: new tickets
3. Analyze: issue type and urgency
4. Generate: response draft
5. Quality check: against response rubric
6. Submit: response or escalate

## Response Quality Rubric

| Criterion | Weight | Threshold |
|-----------|--------|-----------|
| Relevance | 30% | Addresses customer issue |
| Tone | 25% | Professional and empathetic |
| Completeness | 25% | All aspects covered |
| Actionability | 20% | Clear next steps |

## Usage Examples

### Respond to Refund Request
```
User: "Process refund request from customer #1234"
Skill: Checks ticket → reviews policy → generates response → sends
```

### Handle Technical Issue
```
User: "Customer reporting login error"
Skill: Classifies issue → searches KB → generates solution → sends
```

### Escalate Complex Case
```
User: "Review escalation from enterprise client"
Skill: Analyzes history → prepares summary → routes to human
```

## Skills It Coordinates

- `agent-browser` - Browser automation
- `copywriting` - Response generation
- `notion` MCP - Ticket tracking (when available)
- `google-workspace` MCP - Gmail access (when available)

## Escalation Rules

| Condition | Action |
|-----------|--------|
| Legal matter | Always escalate to human |
| Refund > $500 | Escalate to human |
| VIP customer | Always escalate to human |
| 3+ previous tickets | Escalate to human |
| Media/PR issue | Always escalate to human |

## Files Created

- `support-logs/` - Interaction history
- `knowledge-base/` - FAQ and solutions
- `escalation-queue/` - Cases needing human review
