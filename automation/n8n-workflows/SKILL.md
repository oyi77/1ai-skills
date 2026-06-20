---
name: n8n-workflows
description: n8n workflow automation — nodes, triggers, expressions, credentials, webhooks, error handling
domain: automation
tags:
- automation
- n8n
- productivity
- webhook
- workflow
- workflows
---

## Overview

n8n is a fair-code licensed workflow automation tool. It provides 400+ integrations, visual workflow design, self-hosting options, and code flexibility with JavaScript/Python nodes.

## Capabilities

- Build workflows with 400+ pre-built nodes
- Use triggers: webhook, cron, email, file changes, database
- Write custom code in JavaScript/Python nodes
- Handle errors with error workflows
- Use expressions for dynamic data mapping
- Self-host or use n8n cloud
- Manage credentials securely

## When to Use

- Automating business processes across multiple SaaS tools
- Building API integrations without coding
- Needing self-hosted automation (data sovereignty)
- Complex workflows with branching, loops, error handling
- Replacing Zapier/Make with more flexibility

## When NOT to Use

- Task is simple enough for Zapier (use Zapier for no-code)
- You need complex code execution (use Pipedream)
- Task is about data storage, not workflow automation
- You don't have n8n instance running
- Task requires real-time processing (use streaming tools)
- You need to build a custom application (use development tools)

## Pseudo Code

Implementation patterns for common use cases with this skill.


### Workflow Structure

```
Trigger → Set Variables → HTTP Request → IF Condition → Send Email / Slack
                                            ↓
                                      Code Node → Database
```

### Expressions

```javascript
// Access previous node data
{{ $json.fieldName }}
{{ $json.data.items[0].name }}

// Access trigger data
{{ $json.body.query }}

// Transform data
{{ $json.name.toUpperCase() }}
{{ $json.items.filter(i => i.active) }}

// Date
{{ $now.format('yyyy-MM-dd') }}
{{ $now.minus({ days: 7 }).toISO() }}

// Environment variables
{{ $env.API_KEY }}
```

### Webhook Trigger

```json
{
  "nodes": [{
    "type": "n8n-nodes-base.webhook",
    "parameters": {
      "httpMethod": "POST",
      "path": "my-webhook",
      "responseMode": "lastNode",
      "options": {}
    }
  }]
}
```

### Code Node (JavaScript)

```javascript
// Process items
const items = $input.all();
const results = items.map(item => ({
  json: {
    ...item.json,
    processed: true,
    timestamp: Date.now(),
  }
}));
return results;
```

### Code Node (Python)

```python
# Access input data
items = _input.all()

# Process
results = []
for item in items:
    results.append({
        "json": {
            **item["json"],
            "processed": True,
        }
    })

return results
```

### Error Handling

```json
{
  "settings": {
    "errorWorkflow": "workflow-id-for-error-handler"
  }
}
```

```javascript
// Error workflow receives:
// - error.message
// - error.node.name
// - workflow.name
// - execution.id
```

### Credentials

```json
{
  "credentials": {
    "httpHeaderAuth": {
      "id": "1",
      "name": "My API",
      "type": "httpHeaderAuth",
      "data": {
        "name": "Authorization",
        "value": "Bearer {{ $env.API_TOKEN }}"
      }
    }
  }
}
```

### Sub-Workflow

```javascript
// Execute Workflow node
{
  "type": "n8n-nodes-base.executeWorkflow",
  "parameters": {
    "workflowId": "sub-workflow-id",
    "inputDataFieldName": "items"
  }
}
```

## Common Patterns

| Pattern | When to Use |
|---------|------------|
| Webhook → Process → Response | API endpoint |
| Cron → Fetch → Transform → Store | Scheduled ETL |
| Email Trigger → Parse → Database | Email processing |
| IF → Branch A / Branch B | Conditional logic |
| SplitInBatches → Loop | Process large datasets |
| Error Trigger → Notify | Error alerting |
| Execute Workflow | Modular sub-workflows |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| Node execution failed | API error or timeout | Add retry on failure, increase timeout |
| Expression error | Invalid expression syntax | Check expression in editor |
| Credential expired | Token/key expired | Update credential |
| Workflow timeout | Long-running node | Increase execution timeout in settings |

## Red Flags

- Not testing workflows before deployment
- Ignoring error handling in workflows
- Missing logging and monitoring
- Not documenting workflow logic
- Ignoring rate limits and quotas

## Verification

- [ ] Workflows are tested end-to-end
- [ ] Error handling is in place
- [ ] Logging and monitoring are configured
- [ ] Workflow logic is documented
- [ ] Rate limits are respected