---
name: planetscale-patterns
description: PlanetScale MySQL — branching, deploy requests, Vitess sharding, connection handling, schema management
domain: development
tags:
- coding
- patterns
- planetscale
- software-engineering
- testing
---


## Overview

PlanetScale is a MySQL-compatible serverless database platform built on Vitess. It provides database branching, non-blocking schema changes via deploy requests, and horizontal sharding.

## Capabilities

- Database branching for development workflows
- Deploy requests with schema diff review
- Non-blocking schema changes (no table locks)
- Horizontal sharding via Vitess
- @planetscale/database serverless driver
- Connection pooling and edge support
- Foreign key support (opt-in)
- Data imports from existing MySQL databases

## When to Use
**Trigger phrases:**
- "planetscale patterns"
- "PlanetScale MySQL — branching, deploy requests, Vitess sharding, connection hand"


- MySQL-compatible serverless database
- Need safe schema migrations without downtime
- Want database branching for CI/CD workflows
- Horizontal scaling requirements
- Existing MySQL workloads

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The planetscale-patterns workflow follows a standard pipeline pattern.

Core flow:
```
# planetscale-patterns primary flow
input = prepare(raw_data)
result = process(input, config={branching, connection, deploy, handling, management})
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


### Setup (Serverless Driver)
```typescript
import { connect } from '@planetscale/database';

const conn = connect({
  host: process.env.DATABASE_HOST,
  username: process.env.DATABASE_USERNAME,
  password: process.env.DATABASE_PASSWORD,
});
```

### Queries
```typescript
// Simple query
const result = await conn.execute('SELECT * FROM users WHERE active = ?', [true]);

// Multiple results
const { rows } = await conn.execute('SELECT * FROM users LIMIT ?', [10]);

// Insert
await conn.execute(
  'INSERT INTO users (name, email) VALUES (?, ?)',
  ['Alice', 'alice@example.com']
);

// Transaction
const tx = await conn.transaction();
try {
  await tx.execute('INSERT INTO users (name) VALUES (?)', ['Bob']);
  await tx.execute('INSERT INTO profiles (user_id) VALUES (?)', [userId]);
  await tx.commit();
} catch (e) {
  await tx.rollback();
}
```

### Drizzle + PlanetScale
```typescript
import { drizzle } from 'drizzle-orm/planetscale-serverless';
import { connect } from '@planetscale/database';

const conn = connect({
  host: process.env.DATABASE_HOST,
  username: process.env.DATABASE_USERNAME,
  password: process.env.DATABASE_PASSWORD,
});

const db = drizzle(conn);
const users = await db.select().from(usersTable);
```

### Database Branching
```bash
# Create branch
pscale branch create mydb feature-branch

# Get connection string
pscale connect mydb feature-branch

# Create deploy request
pscale deploy-request create mydb feature-branch

# Review and deploy
pscale deploy-request deploy mydb 1
```

### Schema Changes
```sql
-- Safe in PlanetScale (no table locks):
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
ALTER TABLE users MODIFY COLUMN name VARCHAR(500);
ALTER TABLE users ADD INDEX idx_email (email);

-- These are also safe (Vitess handles):
ALTER TABLE users ADD CONSTRAINT fk_profile FOREIGN KEY (profile_id) REFERENCES profiles(id);
```

### Prisma + PlanetScale
```prisma
// schema.prisma
datasource db {
  provider     = "mysql"
  url          = env("DATABASE_URL")
  relationMode = "prisma"  // Handle relations in Prisma, not FK in DB
}
```

## Common Patterns

- **Branch per PR**: Create branches for each feature, merge via deploy requests
- **Relation mode**: Use `relationMode = "prisma"` in Prisma for FK compatibility
- **Serverless driver**: Use `@planetscale/database` for edge/serverless functions
- **Vitess limitations**: No `FOREIGN KEY` in schema by default (use Prisma relations)
- **Connection pooling**: Built-in; use connection string directly

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