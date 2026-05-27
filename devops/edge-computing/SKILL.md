---
name: edge-computing
description: Edge computing — Cloudflare Workers, Vercel Edge, Deno Deploy. Edge rendering, caching, edge databases
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

- Low-latency global apps
- A/B testing at edge
- Geo-based routing
- Personalization at CDN edge

## Pseudo Code

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
