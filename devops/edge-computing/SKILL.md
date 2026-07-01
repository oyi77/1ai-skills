---
name: edge-computing
description: Edge computing — Cloudflare Workers, Vercel Edge, Deno Deploy. Edge rendering, caching, edge databases. Use when working with edge computing.
domain: devops
tags:
- ci-cd
- computing
- devops
- edge
- infrastructure
---


## Overview

Edge computing with Cloudflare Workers, Vercel Edge Runtime, and Deno Deploy. Edge-side rendering, caching, and edge databases.

## Capabilities

- Cloudflare Workers development
- Vercel Edge Runtime
- Deno Deploy
- Edge caching strategies
- Edge databases (D1, Turso)
- Edge middleware
- KV storage at edge

## When to Use
**Trigger phrases:**
- "edge computing"
- "Edge computing — Cloudflare Workers, Vercel Edge, Deno Deploy"


- Low-latency global apps
- A/B testing at edge
- Geo-based routing
- Personalization at CDN edge

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The edge-computing workflow follows a standard pipeline pattern.

Core flow:
```
# edge-computing primary flow
input = prepare(raw_data)
result = process(input, config={caching, cloudflare, computing, databases, deno})
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


### Cloudflare Worker + D1
```javascript
export default {
  async fetch(request, env) {
    const { results } = await env.DB.prepare("SELECT * FROM users").all();
    return Response.json(results);
  },
};
```

## Common Patterns

- Cache at edge, compute at origin
- Use KV for config, D1 for data
- Middleware for auth/geo routing
- Minimize bundle size

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

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Manual deployments are fine" | Manual deployments are error-prone and不可 repeatable. Automate. |
| "We do not need monitoring" | Without monitoring, you are flying blind. Add observability from day one. |
| "Infrastructure as code is overkill" | IaC enables reproducibility, version control, and disaster recovery. |