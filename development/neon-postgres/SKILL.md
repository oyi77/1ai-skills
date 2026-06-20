---
name: neon-postgres
description: Neon serverless Postgres — branching, autoscaling, connection pooling, edge-compatible Postgres
domain: development
tags:
- coding
- neon
- postgres
- software-engineering
- testing
---


## Overview

Neon is a serverless Postgres platform that separates storage and compute. It offers database branching for dev workflows, autoscaling to zero for cost savings, and edge-compatible serverless drivers.

## Capabilities

- Database branching (copy-on-write, instant)
- Autoscaling to zero when idle
- @neondatabase/serverless driver for edge functions
- Connection pooling built-in
- Point-in-time restore
- Logical replication
- GitHub integration for preview deployments

## When to Use

- Serverless/edge deployments (Vercel, Cloudflare, Deno)
- Need database branching for PR previews
- Want to minimize Postgres costs (scale to zero)
- Modern Postgres with serverless characteristics

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The neon-postgres workflow follows a standard pipeline pattern.

Core flow:
```
# neon-postgres primary flow
input = prepare(raw_data)
result = process(input, config={autoscaling, branching, compatible, connection, edge})
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


### Setup
```typescript
import { neon } from '@neondatabase/serverless';

// For serverless/edge environments
const sql = neon(process.env.DATABASE_URL!);

// For Node.js with connection pooling
import { Pool } from '@neondatabase/serverless';
const pool = new Pool({ connectionString: process.env.DATABASE_URL });
```

### Queries (Serverless Driver)
```typescript
// Simple query
const users = await sql`SELECT * FROM users WHERE active = true`;

// Parameterized
const user = await sql`SELECT * FROM users WHERE id = ${userId}`;

// Transaction
const result = await sql.transaction([
  sql`INSERT INTO users (name) VALUES (${name}) RETURNING id`,
  sql`INSERT INTO profiles (user_id, bio) VALUES (${userId}, ${bio})`,
]);
```

### Database Branching
```bash
# Create branch via CLI
neon branches create --name dev-feature-x

# Get connection string for branch
neon connection-string dev-feature-x

# Reset branch to parent state
neon branches reset dev-feature-x

# Delete branch
neon branches delete dev-feature-x
```

### Vercel Integration
```typescript
// Vercel Postgres integration uses Neon under the hood
import { sql } from '@vercel/postgres';

const { rows } = await sql`SELECT * FROM users`;
```

### Edge Function Usage
```typescript
// Cloudflare Workers
export default {
  async fetch(request: Request, env: Env) {
    const sql = neon(env.DATABASE_URL);
    const users = await sql`SELECT * FROM users LIMIT 10`;
    return Response.json(users);
  },
};
```

### Drizzle + Neon
```typescript
import { drizzle } from 'drizzle-orm/neon-http';
import { neon } from '@neondatabase/serverless';

const sql = neon(process.env.DATABASE_URL!);
const db = drizzle(sql);

const users = await db.select().from(usersTable);
```

## Common Patterns

- **Branch per PR**: Use GitHub integration to auto-create branches for PR previews
- **Scale to zero**: Configure autosuspend delay (default 5 min) in dashboard
- **Connection pooling**: Use pooled connection string for traditional clients
- **Migrations**: Use Drizzle Kit or Prisma with Neon connection string
- **Monitoring**: Use Neon dashboard for query stats and autoscaling metrics

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
