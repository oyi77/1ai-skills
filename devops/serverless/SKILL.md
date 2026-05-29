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

The serverless workflow follows a standard pipeline pattern.

Core flow:
```
# serverless primary flow
input = prepare(raw_data)
result = process(input, config={architecture, cloudflare, cold, design, driven})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


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

## How to Use

1. Define infrastructure as code (Terraform, CloudFormation, Pulumi)
2. Review changes through PR process before applying
3. Configure monitoring and alerting for critical paths
4. Set up secrets management (Vault, AWS Secrets Manager, etc.)
5. Document runbooks for deployment, rollback, and incident response
6. Test disaster recovery procedures regularly

## Red Flags

- **Infrastructure changes without review**: Unreviewed changes cause outages — use PRs for infra code
- **No rollback strategy**: Every deployment needs a tested rollback plan before it runs
- **Secrets in configuration files**: Secrets in YAML/JSON get committed to version control
- **Missing monitoring and alerting**: Without monitoring, outages go undetected until users report them
- **No documentation for runbooks**: Without runbooks, on-call engineers waste time re-discovering procedures
