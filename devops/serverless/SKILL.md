---
name: serverless
description: Serverless architecture — AWS Lambda, Cloudflare Workers, Vercel Edge. Event-driven design, cold start optimization
---

## Overview

Serverless architecture patterns using AWS Lambda, Cloudflare Workers, and Vercel Edge Functions. Event-driven design with cold start optimization.

## Capabilities

- Lambda function deployment
- Cloudflare Workers with Wrangler
- Vercel Edge Functions
- API Gateway integration
- Step Functions orchestration
- Cold start optimization
- Event-driven patterns

## When to Use

- API backends without servers
- Event-driven processing
- Scheduled tasks (cron)
- Microservices at low cost

## Pseudo Code

### Lambda Function
```python
def handler(event, context):
    return {"statusCode": 200, "body": json.dumps({"message": "Hello!"})}
```

### Cloudflare Worker
```javascript
export default {
  async fetch(request) {
    return new Response("Hello from the edge!");
  },
};
```

## Common Patterns

- Keep functions small and focused
- Use provisioned concurrency for latency
- Connection pooling for DB access
- Idempotent handlers for retries
