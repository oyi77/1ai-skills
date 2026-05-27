---
name: pipedream-workflows
description: Pipedream serverless workflows — triggers, code steps, pre-built actions, data stores, HTTP
---

## Overview

Pipedream is a serverless integration and compute platform. It lets you build event-driven workflows with Node.js code steps, 1000+ pre-built app actions, and HTTP triggers — all running on serverless infrastructure.

## Capabilities

- Build workflows with HTTP, cron, or app event triggers
- Write Node.js code steps with full npm access
- Use 1000+ pre-built app actions
- Store data in built-in Data Stores
- Make HTTP requests to any API
- Deploy as REST API endpoints
- Use connected accounts for OAuth apps

## When to Use

- Building event-driven automation with custom code
- Needing serverless compute for integration logic
- Wanting npm package access in automation workflows
- Building webhook receivers and API endpoints
- Replacing custom scripts with managed workflows

## Pseudo Code

### Workflow Structure

```
Trigger → Code Step → HTTP Request → IF → Pre-built Action → Code Step
```

### Trigger Types

| Type | Config |
|------|--------|
| HTTP | `$.interface.http` — webhook endpoint |
| Schedule | `$.interface.timer` — cron or interval |
| App Event | New email, GitHub issue, etc. |

### Code Step (Node.js)

```javascript
// Access previous step data
const prevData = $.steps.trigger.event;

// Use npm packages
const axios = require('axios');
const _ = require('lodash');

// Make HTTP request
const response = await axios.get('https://api.example.com/data', {
  headers: { Authorization: `Bearer ${$.auth.api_key}` },
});

// Process data
const filtered = _.filter(response.data, item => item.active);

// Return data to next step
return {
  count: filtered.length,
  items: filtered,
};
```

### HTTP Request Step

```javascript
// Built-in HTTP request
const response = await $.http.request({
  method: 'POST',
  url: 'https://api.example.com/webhook',
  headers: {
    'Content-Type': 'application/json',
  },
  data: {
    event: $.steps.trigger.event.type,
    payload: $.steps.process.items,
  },
});

return response.data;
```

### Data Store

```javascript
// Get value
const count = await $.service.data_store.get('counter') || 0;

// Set value
await $.service.data_store.set('counter', count + 1);

// Delete
await $.service.data_store.delete('counter');

// List keys
const keys = await $.service.data_store.keys();
```

### Connected Accounts

```javascript
// Access connected account
const slack = $.app.slack;
const github = $.app.github;

// Use in API calls
const response = await axios.post('https://slack.com/api/chat.postMessage', {
  channel: '#alerts',
  text: `New event: ${$.steps.trigger.event.type}`,
}, {
  headers: { Authorization: `Bearer ${slack.$auth.oauth_access_token}` },
});
```

### Deploy as API

```javascript
// HTTP trigger creates an endpoint like:
// https://endpoint.p.punique.com/abc123

// Handle different methods
if ($.trigger.event.http.method === 'POST') {
  return { status: 'received', data: $.trigger.event.body };
}

if ($.trigger.event.http.method === 'GET') {
  return { status: 'ok', timestamp: Date.now() };
}
```

### Error Handling in Steps

```javascript
try {
  const result = await riskyOperation();
  return { success: true, data: result };
} catch (error) {
  // Return error to flow (doesn't stop workflow)
  return {
    success: false,
    error: error.message,
    step: 'process_data',
  };
}
```

## Common Patterns

| Pattern | When to Use |
|---------|------------|
| HTTP Trigger → Process → Respond | API endpoint |
| Schedule → Fetch → Transform → Store | ETL |
| App Event → Code → Notify | Event-driven automation |
| Webhook → Validate → Route | Multi-tenant webhooks |
| Data Store get/set | Stateful workflows |
| Code Step + npm | Complex logic with libraries |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| Step timeout | Long-running code | Optimize or use `$.flow.delay()` |
| npm package not found | Not in allowed list | Use built-in `$.http` instead |
| Data Store limit exceeded | Too many keys | Clean up old entries |
| Auth error | Expired token | Reconnect account |
