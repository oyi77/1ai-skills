---
name: api-design
description: REST API design — resource modeling, versioning, pagination, error handling, OpenAPI/Swagger documentation
---

## Overview

Design production REST APIs — resource naming conventions, versioning strategies, pagination, error formats, rate limiting, and OpenAPI documentation.

## Capabilities

- RESTful resource modeling and naming
- API versioning (URL, header, query)
- Pagination (cursor, offset, keyset)
- Consistent error response format
- Rate limiting strategies
- OpenAPI/Swagger documentation
- Authentication patterns (JWT, API keys, OAuth)

## When to Use

- Designing a new REST API
- Refactoring existing API for consistency
- Documenting APIs with OpenAPI
- Implementing rate limiting or pagination
- Standardizing error responses across services

## Pseudo Code

### Resource Naming

```
# Good
GET    /api/v1/users
GET    /api/v1/users/123
POST   /api/v1/users
PATCH  /api/v1/users/123
DELETE /api/v1/users/123
GET    /api/v1/users/123/orders

# Bad (verbs in URL)
GET    /api/getUsers
POST   /api/createUser
POST   /api/deleteUser/123
```

### Pagination (Cursor-based)

```javascript
// Request
GET /api/v1/users?limit=20&cursor=eyJpZCI6MTIzfQ

// Response
{
  "data": [...],
  "pagination": {
    "next_cursor": "eyJpZCI6MTQzfQ",
    "has_more": true
  }
}
```

### Consistent Error Format

```javascript
// Express error handler
app.use((err, req, res, next) => {
  const status = err.status || 500
  res.status(status).json({
    error: {
      code: err.code || 'INTERNAL_ERROR',
      message: err.message,
      details: err.details || [],
      request_id: req.headers['x-request-id'],
    },
  })
})

// Usage
throw Object.assign(new Error('Not found'), {
  status: 404,
  code: 'RESOURCE_NOT_FOUND',
  details: [{ field: 'id', message: 'User not found' }],
})
```

### Rate Limiting

```javascript
import rateLimit from 'express-rate-limit'

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,
  standardHeaders: true, // Return rate limit info in headers
  legacyHeaders: false,
  keyGenerator: (req) => req.headers['x-api-key'] || req.ip,
})

app.use('/api/', limiter)
```

### OpenAPI Spec

```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: limit
          in: query
          schema: { type: integer, default: 20 }
        - name: cursor
          in: query
          schema: { type: string }
      responses:
        '200':
          description: User list
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items: { $ref: '#/components/schemas/User' }
                  pagination:
                    $ref: '#/components/schemas/Pagination'
```

### API Versioning

```javascript
// URL versioning (most common)
app.use('/api/v1', v1Router)
app.use('/api/v2', v2Router)

// Header versioning
app.use((req, res, next) => {
  const version = req.headers['api-version'] || 'v1'
  req.apiVersion = version
  next()
})
```

## Common Patterns

- **HATEOAS**: Include links for resource navigation
- **Idempotency keys**: Prevent duplicate operations on retries
- **Request IDs**: Track requests across services
- **Field filtering**: `?fields=id,name,email` to reduce payload
- **Bulk operations**: `POST /api/v1/users/batch` for bulk create/update
