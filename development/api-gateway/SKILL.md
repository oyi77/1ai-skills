---
name: api-gateway
description: Use when aPI gateway design — rate limiting, authentication, routing,
  caching, request transformation. Kong, Traefik, custom gateways. Use when working
  with api gateway.
domain: development
author: oyi77
license: Apache-2.0
subdomain: software-development
tags:
- api
- coding
- gateway
- software-engineering
- testing
version: 1.0.0
category: development
---



## Overview

An API gateway is a reverse proxy that sits between clients and backend services, handling cross-cutting concerns like authentication, rate limiting, routing, and caching. This skill covers designing and implementing gateways using Kong, Traefik, or custom Node.js/Go implementations.

## Capabilities

- Route requests to multiple backend services from a single entry point
- Implement rate limiting per user, IP, or API key
- Authenticate requests (JWT, OAuth2, API keys) before they reach services
- Transform requests and responses (header manipulation, body mapping)
- Cache responses to reduce backend load
- Monitor and log all API traffic
- Handle circuit breaking and retry logic

## When to Use
**Trigger phrases:**
- "api gateway"
- "API gateway design — rate limiting, authentication, routing, caching, request tr"


- Microservices architecture needing a unified entry point
- Public APIs requiring authentication, rate limiting, and monitoring
- Migrating from monolith to microservices (gateway routes to both)
- Need to add cross-cutting concerns without modifying services
- Multi-tenant SaaS with per-tenant routing rules

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The api-gateway workflow follows a standard pipeline pattern.

Core flow:
```
# api-gateway primary flow
input = prepare(raw_data)
result = process(input, config={api, authentication, caching, custom, design})
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


### Kong Gateway (Declarative)
```yaml
# kong.yml
services:
  - name: user-service
    url: http://user-service:3000
    routes:
      - name: user-routes
        paths: ["/api/v1/users"]
        strip_path: true
    plugins:
      - name: rate-limiting
        config:
          minute: 100
          policy: redis
          redis_host: redis
      - name: jwt
      - name: cors
        config:
          origins: ["https://app.example.com"]

  - name: order-service
    url: http://order-service:3001
    routes:
      - name: order-routes
        paths: ["/api/v1/orders"]
    plugins:
      - name: rate-limiting
        config:
          minute: 50
      - name: request-transformer
        config:
          add:
            headers: ["X-Request-ID:$(request_id)"]
```

### Traefik (Docker Labels)
```yaml
# docker-compose.yml
services:
  traefik:
    image: traefik:v3
    command:
      - --providers.docker=true
      - --entrypoints.web.address=:80
      - --api.dashboard=true
    ports:
      - "80:80"
      - "8080:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock

  user-service:
    labels:
      - traefik.enable=true
      - traefik.http.routers.user.rule=Host(`api.example.com`) && PathPrefix(`/users`)
      - traefik.http.routers.user.middlewares=auth,rate-limit
      - traefik.http.middlewares.auth.forwardauth.address=http://auth-service:4000/verify
      - traefik.http.middlewares.rate-limit.ratelimit.average=100
      - traefik.http.middlewares.rate-limit.ratelimit.burst=50
```

### Custom Gateway (Node.js)
```javascript
// gateway.js
const express = require('express');
const httpProxy = require('http-proxy');
const rateLimit = require('express-rate-limit');
const jwt = require('jsonwebtoken');

const app = express();
const proxy = httpProxy.createProxyServer();

// Service registry
const services = {
  users: 'http://user-service:3000',
  orders: 'http://order-service:3001',
  products: 'http://product-service:3002',
};

// Rate limiting
const limiter = rateLimit({
  windowMs: 60 * 1000,
  max: 100,
  keyGenerator: (req) => req.user?.id || req.ip,
  message: { error: 'Rate limit exceeded' },
});

// JWT authentication
const authenticate = (req, res, next) => {
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) return res.status(401).json({ error: 'No token' });
  try {
    req.user = jwt.verify(token, process.env.JWT_SECRET);
    next();
  } catch {
    res.status(401).json({ error: 'Invalid token' });
  }
};

// Request logging
const logRequest = (req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    console.log({
      method: req.method,
      path: req.path,
      status: res.statusCode,
      duration: Date.now() - start,
      userId: req.user?.id,
    });
  });
  next();
};

// Routing
app.use('/api/users', authenticate, limiter, logRequest, (req, res) => {
  proxy.web(req, res, { target: services.users });
});

app.use('/api/orders', authenticate, limiter, logRequest, (req, res) => {
  proxy.web(req, res, { target: services.orders });
});

app.use('/api/products', logRequest, (req, res) => {
  proxy.web(req, res, { target: services.products }); // Public endpoint
});

// Error handling
proxy.on('error', (err, req, res) => {
  res.status(502).json({ error: 'Service unavailable' });
});

app.listen(8080, () => console.log('Gateway on :8080'));
```

### Circuit Breaker
```javascript
const CircuitBreaker = require('opossum');

const breaker = new CircuitBreaker(
  (req, res) => proxy.web(req, res, { target: services.users }),
  {
    timeout: 5000,
    errorThresholdPercentage: 50,
    resetTimeout: 30000,
    volumeThreshold: 10,
  }
);

breaker.on('open', () => console.log('Circuit OPEN — fallback mode'));
breaker.fallback((req, res) => {
  res.status(503).json({ error: 'Service temporarily unavailable' });
});

app.use('/api/users', authenticate, (req, res) => breaker.fire(req, res));
```

## Production Rules

- **Timeout budget.** Set explicit upstream timeouts; gateway timeout must exceed upstream timeout + retry budget, or retries will outlive the client request.
- **Retry only idempotent calls.** Retry GET/HEAD and idempotent-keyed writes; never blindly retry POST/charges. Use jittered exponential backoff with a max attempt count.
- **Circuit breaker per upstream.** Open on sustained failure, half-open probe, close on recovery; return a clean 503 fallback, not a hung socket.
- **Rate limiting keyed by identity.** Limit per API key/user, not just IP; shared NAT makes IP-only limits unfair. Return `429` with `Retry-After`.
- **Auth at the edge, authorize at the service.** Gateway validates tokens; services still enforce object-level permissions.
- **Request IDs end-to-end.** Generate/propagate `X-Request-ID`; log method, route, status, latency, and upstream — never tokens or bodies by default.
- **Health/readiness.** Expose `/healthz` (process) and `/readyz` (dependencies); load balancers use readiness, not health.
- **Fail closed on auth errors, fail open on cache misses.** A cache outage should slow, not lock out, authenticated traffic.

### API Key Authentication
```javascript
const apiKeys = new Map(); // Store in Redis in production

const authenticateApiKey = (req, res, next) => {
  const key = req.headers['x-api-key'];
  if (!key || !apiKeys.has(key)) {
    return res.status(401).json({ error: 'Invalid API key' });
  }
  req.client = apiKeys.get(key);
  next();
};
```

### Request/Response Transformation
```javascript
// Add request ID, strip sensitive headers, transform response
app.use((req, res, next) => {
  req.headers['x-request-id'] = crypto.randomUUID();
  req.headers['x-forwarded-for'] = req.ip;
  next();
});
```

### Caching (Redis)
```javascript
const Redis = require('ioredis');
const redis = new Redis();

const cache = (ttl) => async (req, res, next) => {
  const key = `cache:${req.method}:${req.originalUrl}`;
  const cached = await redis.get(key);
  if (cached) return res.json(JSON.parse(cached));

  const originalJson = res.json.bind(res);
  res.json = (body) => {
    redis.setex(key, ttl, JSON.stringify(body));
    return originalJson(body);
  };
  next();
};

app.use('/api/products', cache(300), (req, res) => proxy.web(req, res, { target: services.products }));
```

## Verification

- [ ] Timeout hierarchy tested: gateway > upstream, retries counted in budget
- [ ] Retry policy proven idempotent; non-idempotent POST not retried blindly
- [ ] Circuit breaker opens/closes under injected upstream failure
- [ ] Rate limiting tested per key with `429` + `Retry-After`
- [ ] Auth invalid tokens rejected; service still authorizes object ownership
- [ ] Request ID propagated end-to-end; logs contain no secrets/PII
- [ ] `/healthz` and `/readyz` respond correctly with dependencies up/down
- [ ] Load test at expected p99 traffic; saturation causes shedding, not a hang

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Tests slow me down" | Bugs slow you down 10x more. Tests are speed, not overhead. |
| "I will refactor later" | Technical debt compounds. Refactor as you go. |
| "It works on my machine" | If it is not in CI, it does not work. Ship proof, not claims. |