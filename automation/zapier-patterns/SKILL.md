---
name: zapier-patterns
description: Zapier automation patterns — triggers, actions, filters, formatters,
  paths, code steps
domain: automation
---

## Overview

Zapier is the most popular no-code automation platform with 7000+ app integrations. It uses Zaps (workflows) with triggers, actions, filters, formatters, paths, and code steps.

## Capabilities

- Build Zaps with 7000+ app integrations
- Use triggers from apps, webhooks, or schedules
- Add filters to control data flow
- Format data with built-in Formatter
- Use Paths for conditional branching
- Write custom code with Code by Zapier
- Create multi-step Zaps with 100+ steps

## When to Use

- Automating repetitive business tasks
- Connecting SaaS tools without coding
- Building simple data pipelines
- Needing the largest app integration ecosystem
- Non-technical users building automations

## When NOT to Use

- Task requires custom code (use Pipedream or n8n)
- You need complex branching logic (use Make)
- Task is about data processing, not automation
- You don't have Zapier account or app connections
- Task requires real-time processing (use streaming tools)
- You need to build a custom API (use development tools)

## Pseudo Code

Implementation patterns for common use cases with this skill.


### Zap Structure

```
Trigger → Filter → Formatter → Action 1 → Action 2
                              ↘ Path A → Action A
                               ↘ Path B → Action B
```

### Trigger Types

| Type | Example |
|------|---------|
| App Event | New email, New row in spreadsheet |
| Webhook | Catch Hook (custom URL) |
| Schedule | Every hour, Daily at 9am |
| RSS | New feed item |

### Filter

```json
{
  "filter": {
    "conditions": [
      {
        "field": "status",
        "operator": "str",
        "value": "active"
      },
      {
        "field": "amount",
        "operator": "number_greater",
        "value": "100"
      }
    ]
  }
}
```

### Formatter (Data Transformation)

```javascript
// Text
{{formatter.text.uppercase(input)}}
{{formatter.text.replace(input, "old", "new")}}
{{formatter.text.substring(input, 0, 10)}}

// Number
{{formatter.number.round(input, 2)}}
{{formatter.number.formatCurrency(input, "USD")}}

// Date
{{formatter.date.format(input, "YYYY-MM-DD")}}
{{formatter.date.addDays(input, 7)}}

// Utilities
{{formatter.utilities.lookup(input, lookupTable)}}
```

### Paths (Conditional Branching)

```json
{
  "paths": [
    {
      "conditions": [
        {"field": "priority", "operator": "str", "value": "high"}
      ],
      "actions": ["send_slack", "create_ticket"]
    },
    {
      "conditions": [
        {"field": "priority", "operator": "str", "value": "low"}
      ],
      "actions": ["log_only"]
    }
  ]
}
```

### Code by Zapier (JavaScript)

```javascript
// Input from previous steps
const email = inputData.email;
const name = inputData.name;

// Process
const domain = email.split('@')[1];
const isCompany = domain !== 'gmail.com' && domain !== 'yahoo.com';

// Output
output = {
  processed: true,
  domain: domain,
  isCompany: isCompany,
  greeting: `Hello ${name}`,
};
```

### Code by Zapier (Python)

```python
import json

# Input
email = input_data['email']
amount = float(input_data['amount'])

# Process
tax = amount * 0.1
total = amount + tax

# Output
output = {
    'subtotal': amount,
    'tax': round(tax, 2),
    'total': round(total, 2),
}
```

### Webhook (Catch Hook)

```bash
# Zapier provides a URL like:
# https://hooks.zapier.com/hooks/catch/123456/abcdef/

# POST data to it
curl -X POST "https://hooks.zapier.com/hooks/catch/123456/abcdef/" \
  -H "Content-Type: application/json" \
  -d '{"event": "new_order", "amount": 99.99}'
```

## Common Patterns

| Pattern | When to Use |
|---------|------------|
| New Row → Filter → Send Email | Spreadsheet automation |
| Webhook → Process → Multiple Actions | Custom event handling |
| Schedule → Fetch → Transform → Store | Regular data sync |
| Path A / Path B | Conditional logic |
| Formatter → Clean Data | Data normalization |
| Code Step → Complex Logic | Custom transformations |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| Filter stopped Zap | Conditions not met | Check filter logic |
| Rate limit | Too many tasks | Add delay step or use Paths |
| Code error | Syntax or runtime error | Test code step individually |
| App disconnected | OAuth token expired | Reconnect app |

## Red Flags

- Not testing Zaps before enabling
- Ignoring error handling in Zaps
- Missing logging and monitoring
- Not documenting Zap logic
- Ignoring rate limits and quotas

## Verification

- [ ] Zaps are tested end-to-end
- [ ] Error handling is in place
- [ ] Logging and monitoring are configured
- [ ] Zap logic is documented
- [ ] Rate limits are respected