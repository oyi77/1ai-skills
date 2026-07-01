---
name: make-scenarios
description: Make.com scenario automation — modules, routes, filters, error handlers, data stores, webhooks. Use when working with make scenarios.
domain: automation
tags:
- automation
- make
- productivity
- scenarios
- webhook
- workflow
---

## Overview

Make.com (formerly Integromat) is a visual automation platform with 1500+ app integrations. It uses scenarios with modules connected by routes, with filters, error handlers, and data stores for complex automation logic.

## Capabilities

- Build scenarios with 1500+ app modules
- Use routers for conditional branching
- Add filters to control data flow
- Handle errors with error handler routes
- Store data in Data Stores
- Use webhooks for custom triggers
- Schedule scenarios with cron

## When to Use

- Automating workflows across SaaS applications
- Needing visual automation with complex branching
- Building customer-facing integrations
- Managing data synchronization between systems
- Replacing manual processes with automated scenarios

## When NOT to Use

- Task requires custom code (use Pipedream or n8n)
- You need complex data transformations (use ETL tools)
- Task is about data storage, not workflow automation
- You don't have access to the SaaS apps being connected
- Task requires real-time processing (use streaming tools)
- You need to build a custom API (use development tools)

## Pseudo Code

Implementation patterns for common use cases with this skill.


### Scenario Architecture

```
Trigger Module → Iterator → Aggregator → Router → Filter → Action
                                                    ↓
                                              Error Handler → Notify
```

### Module Types

| Type | Examples |
|------|----------|
| Trigger | Webhook, Schedule, Email, Form |
| Action | HTTP Request, Send Email, Create Record |
| Search | Get Records, List Items |
| Iterator | Process arrays |
| Aggregator | Combine array items |
| Router | Conditional branching |
| Filter | Stop/continue based on conditions |

### Filter Configuration

```json
{
  "filter": {
    "name": "Only active users",
    "conditions": [
      {
        "field": "{{1.status}}",
        "operator": "equal",
        "value": "active"
      },
      {
        "field": "{{1.email}}",
        "operator": "notEqual",
        "value": ""
      }
    ]
  }
}
```

### Error Handler

```json
{
  "error_handler": {
    "type": "continue",
    "resume": {
      "type": "fallback",
      "parameters": {
        "fallback_value": "default"
      }
    }
  }
}
```

### Data Store Operations

```json
// Get record
{
  "module": "datastore",
  "operation": "get",
  "key": "user_{{1.id}}"
}

// Create/update record
{
  "module": "datastore",
  "operation": "upsert",
  "key": "user_{{1.id}}",
  "value": {
    "name": "{{1.name}}",
    "last_seen": "{{now}}"
  }
}
```

### Webhook Response

```json
{
  "module": "webhook",
  "operation": "respond",
  "parameters": {
    "status": 200,
    "body": {
      "received": true,
      "id": "{{1.id}}"
    }
  }
}
```

### Custom Functions (Mapping)

```javascript
// Date formatting
{{formatDate(now; "YYYY-MM-DD")}}

// Conditional
{{if(1.status = "active"; "yes"; "no")}}

// Array operations
{{length(1.items)}}
{{get(1.items; 0)}}
{{map(1.items; "name")}}

// String
{{replace(1.text; "old"; "new")}}
{{substring(1.text; 0; 10)}}
```

## Common Patterns

| Pattern | When to Use |
|---------|------------|
| Webhook → Process → Respond | Custom API endpoint |
| Schedule → Fetch → Transform → Store | Data sync |
| Email → Parse → Route → Action | Email automation |
| Router → Filter A / Filter B | Conditional processing |
| Error Handler → Log + Notify | Error management |
| Iterator → Process → Aggregator | Batch processing |
| Data Store get/set | Stateful workflows |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| Module timeout | Slow API response | Increase timeout in module settings |
| Data size limit | Payload too large | Use pagination or split data |
| Rate limit | Too many API calls | Add delay between operations |
| Connection error | Auth expired | Re-authorize connection |

## Red Flags

- Not testing scenarios before deployment
- Ignoring error handling in scenarios
- Missing logging and monitoring
- Not documenting scenario logic
- Ignoring rate limits and quotas

## Verification

- [ ] Scenarios are tested end-to-end
- [ ] Error handling is in place
- [ ] Logging and monitoring are configured
- [ ] Scenario logic is documented
- [ ] Rate limits are respected

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Manual is faster for one-off tasks" | One-off tasks become recurring. Automate early, save time later. |
| "I will add error handling later" | You never do. Handle errors from day one. |
| "Automation is overkill" | If you do it twice, automate it. If you do it daily, it is critical infrastructure. |