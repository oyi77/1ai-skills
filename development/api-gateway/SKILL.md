---
name: api-gateway
description: API gateway design — rate limiting, authentication, routing, caching, request transformation. Kong, Traefik, custom gateways
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

- Microservices architecture needing a unified entry point
- Public APIs requiring authentication, rate limiting, and monitoring
- Migrating from monolith to microservices (gateway routes to both)
- Need to add cross-cutting concerns without modifying services
- Multi-tenant SaaS with per-tenant routing rules

## Pseudo Code

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

## Common Patterns

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
