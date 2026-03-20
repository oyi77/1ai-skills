---
name: api-design-principles
description: Master REST and GraphQL API design principles to build intuitive, scalable, and maintainable APIs that delight developers. Use when designing new APIs, reviewing API specifications, or establishing API design standards.
source: https://github.com/LeoYeAI/openclaw-master-skills
---

# API Design Principles

Master REST and GraphQL API design principles to build intuitive, scalable, and maintainable APIs that delight developers and stand the test of time.

## When to Use This Skill

- Designing new REST or GraphQL APIs
- Refactoring existing APIs for better usability
- Establishing API design standards for your team
- Reviewing API specifications before implementation
- Migrating between API paradigms (REST to GraphQL, etc.)
- Creating developer-friendly API documentation
- Optimizing APIs for specific use cases (mobile, third-party integrations)

## Core Concepts

### 1. RESTful Design Principles

**Resource-Oriented Architecture**

- Resources are nouns (users, orders, products), not verbs
- Use HTTP methods for actions (GET, POST, PUT, PATCH, DELETE)
- URLs represent resource hierarchies
- Consistent naming conventions

**HTTP Methods Semantics:**

- `GET`: Retrieve resources (idempotent, safe)
- `POST`: Create new resources
- `PUT`: Replace entire resource (idempotent)
- `PATCH`: Partial resource updates
- `DELETE`: Remove resources (idempotent)

### 2. GraphQL Design Principles

**Schema-First Development**

- Types define your domain model
- Queries for reading data
- Mutations for modifying data
- Subscriptions for real-time updates

**Query Structure:**

- Clients request exactly what they need
- Single endpoint, multiple operations
- Strongly typed schema
- Introspection built-in

### 3. API Versioning Strategies

**URL Versioning:**
```
/api/v1/users
/api/v2/users
```

**Header Versioning:**
```
Accept: application/vnd.api+json; version=1
```

**Query Parameter Versioning:**
```
/api/users?version=1
```

## REST API Design Patterns

### Pattern 1: Resource Collection Design

```python
# Good: Resource-oriented endpoints
GET    /api/users              # List users (with pagination)
POST   /api/users              # Create user
GET    /api/users/{id}         # Get specific user
PUT    /api/users/{id}         # Replace user
PATCH  /api/users/{id}         # Update user fields
DELETE /api/users/{id}         # Delete user

# Nested resources
GET    /api/users/{id}/orders  # Get user's orders
POST   /api/users/{id}/orders  # Create order for user

# Bad: Action-oriented endpoints (avoid)
POST   /api/createUser
POST   /api/getUserById
POST   /api/deleteUser
```

### Pattern 2: Pagination and Filtering

```python
from typing import List, Optional
from pydantic import BaseModel, Field

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")

class PaginatedResponse(BaseModel):
    items: List[dict]
    total: int
    page: int
    page_size: int
    pages: int

    @property
    def has_next(self) -> bool:
        return self.page < self.pages

    @property
    def has_prev(self) -> bool:
        return self.page > 1
```

### Pattern 3: Error Handling and Status Codes

```python
STATUS_CODES = {
    "success": 200,
    "created": 201,
    "no_content": 204,
    "bad_request": 400,
    "unauthorized": 401,
    "forbidden": 403,
    "not_found": 404,
    "conflict": 409,
    "unprocessable": 422,
    "internal_error": 500
}
```

### Pattern 4: HATEOAS

```python
class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    _links: dict  # self, orders, update, delete links
```

## GraphQL Design Patterns

### Pattern 1: Schema Design
- Clear type definitions with relationships
- Relay-style cursor pagination (Connection/Edge/PageInfo)
- Enums for type safety
- Input/Payload types for mutations

### Pattern 2: DataLoader (N+1 Prevention)
- Batch load related entities in single queries
- Map results back to input order
- Use per-request DataLoader instances

## Best Practices

### REST APIs
1. Consistent Naming: plural nouns for collections
2. Stateless: each request self-contained
3. Use HTTP Status Codes Correctly
4. Version Your API from day one
5. Always paginate large collections
6. Rate Limiting for protection
7. OpenAPI/Swagger documentation

### GraphQL APIs
1. Schema First design
2. DataLoaders for N+1 prevention
3. Input validation at schema + resolver levels
4. Structured errors in mutation payloads
5. Cursor-based pagination
6. `@deprecated` directive for migration
7. Query complexity monitoring

## Common Pitfalls

- Over-fetching/Under-fetching (REST) — fixed in GraphQL with DataLoaders
- Breaking Changes — version APIs or use deprecation strategies
- Inconsistent Error Formats — standardize error responses
- Missing Rate Limits — APIs without limits are vulnerable
- Poor Documentation — undocumented APIs frustrate developers
- Ignoring HTTP Semantics — POST for idempotent ops breaks expectations
- Tight Coupling — API structure shouldn't mirror database schema
