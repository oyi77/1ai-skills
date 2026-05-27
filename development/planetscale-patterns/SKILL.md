---
name: planetscale-patterns
description: PlanetScale MySQL — branching, deploy requests, Vitess sharding, connection handling, schema management
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

- MySQL-compatible serverless database
- Need safe schema migrations without downtime
- Want database branching for CI/CD workflows
- Horizontal scaling requirements
- Existing MySQL workloads

## Pseudo Code

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
