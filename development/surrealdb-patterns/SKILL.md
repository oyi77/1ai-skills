---
name: surrealdb-patterns
description: SurrealDB multi-model database — document, graph, key-value. SurrealQL, realtime subscriptions, embedded mode. Use when working with surrealdb patterns.
domain: development
tags:
- coding
- patterns
- software-engineering
- surrealdb
- testing
---


## Overview

SurrealDB is a multi-model database that combines document, graph, key-value, and relational models in one engine. It uses SurrealQL (SQL-like), supports realtime subscriptions, and can run embedded or as a server.

## Capabilities

- SurrealQL: SQL-like syntax with graph traversal
- Record links (no foreign keys needed)
- Graph traversal with -> and <- operators
- LIVE SELECT for realtime subscriptions
- Schemaful and schemaless tables
- Authentication and permissions at table/record level
- Embedded mode (Rust, JS, Go) or server mode
- HTTP REST API and WebSocket connections

## When to Use
**Trigger phrases:**
- "surrealdb patterns"
- "SurrealDB multi-model database — document, graph, key-value"


- Building applications needing both document and graph capabilities
- Need realtime data subscriptions
- Want a single database instead of polyglot persistence
- Edge/embedded deployments

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The surrealdb-patterns workflow follows a standard pipeline pattern.

Core flow:
```
# surrealdb-patterns primary flow
input = prepare(raw_data)
result = process(input, config={database, document, embedded, graph, mode})
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


### Connection
```javascript
import Surreal from 'surrealdb';

const db = new Surreal();
await db.connect('http://localhost:8000/rpc');
await db.use({ namespace: 'test', database: 'test' });
await db.signin({ username: 'root', password: 'root' });
```

### CRUD
```javascript
// Create
const user = await db.create('user', {
  name: 'Alice',
  email: 'alice@example.com',
  posts: [],
});

// Read
const users = await db.select('user');
const alice = await db.select(`user:${id}`);

// Update
await db.update(`user:${id}`, { name: 'Updated' });

// Delete
await db.delete(`user:${id}`);
```

### SurrealQL
```sql
-- Create with specific ID
CREATE user:alice SET name = 'Alice', email = 'alice@example.com';

-- Select with WHERE
SELECT * FROM user WHERE email LIKE '%@example.com' ORDER BY name LIMIT 10;

-- Graph relation (no foreign key)
RELATE user:alice->wrote->post:hello SET timestamp = time::now();

-- Graph traversal
SELECT ->wrote->post.* FROM user:alice;

-- Subquery
SELECT *, (SELECT ->wrote->post.* FROM user) AS posts FROM user;
```

### LIVE SELECT (Realtime)
```javascript
// Subscribe to changes
const stream = await db.live('user', (action, result) => {
  if (action === 'CREATE') console.log('New user:', result);
  if (action === 'UPDATE') console.log('Updated:', result);
  if (action === 'DELETE') console.log('Deleted:', result);
});

// Kill subscription
await db.kill(stream);
```

### Schema Definition
```sql
DEFINE TABLE user SCHEMAFULL;
DEFINE FIELD name ON user TYPE string;
DEFINE FIELD email ON user TYPE string ASSERT string::is::email($value);
DEFINE FIELD posts ON user TYPE array;
DEFINE INDEX email_index ON user FIELDS email UNIQUE;
```

## Common Patterns

- **Embedded mode**: Use `surrealdb` npm package with `mem://` or `file://` protocol
- **Auth**: `DEFINE SCOPE`, `DEFINE ACCESS`, JWT tokens
- **Migrations**: Use `DEFINE TABLE` and `DEFINE FIELD` in `.surql` files
- **Graph modeling**: Use RELATE for edges, traverse with `->` and `<-`

## How to Use

1. Understand the requirement and existing codebase patterns
2. Design the solution with error handling and testability in mind
3. Implement incrementally with tests for each change
4. Verify against expected outcomes (manual and automated)
5. Document usage, edge cases, and integration points
6. Review with team before merging to shared branches

## Red Flags

- **Skipping tests to ship faster**: Untested code breaks in production when you least expect it
- **No error handling in production code**: Unhandled errors crash services and lose user data
- **Hardcoded configuration values**: Hardcoded values prevent environment switching and leak secrets
- **Ignoring security implications**: Missing input validation, auth bypasses, and injection vulnerabilities
- **Over-engineering simple solutions**: Premature abstraction adds complexity without proportional benefit

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Tests slow me down" | Bugs slow you down 10x more. Tests are speed, not overhead. |
| "I will refactor later" | Technical debt compounds. Refactor as you go. |
| "It works on my machine" | If it is not in CI, it does not work. Ship proof, not claims. |