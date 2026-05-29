---
name: prisma-orm
description: Prisma ORM — schema modeling, migrations, client queries, middleware, performance optimization
---


## Overview

Prisma is a Node.js/TypeScript ORM with auto-generated queries, type safety, and a visual data browser (Prisma Studio). It uses a declarative schema to model data and generates a type-safe client.

## Capabilities

- Declarative schema with `schema.prisma`
- Auto-generated type-safe client
- Database migrations with `prisma migrate`
- Relations, enums, composite types
- Middleware for logging, soft delete, caching
- Connection pooling with PgBouncer / Prisma Accelerate
- Prisma Studio for visual data exploration

## When to Use

- Building Node.js/TypeScript applications with SQL databases
- Want auto-generated types from database schema
- Need a visual database browser for development
- Working with PostgreSQL, MySQL, SQLite, MongoDB, SQL Server, CockroachDB

## Pseudo Code

The prisma-orm workflow follows a standard pipeline pattern.

Core flow:
```
# prisma-orm primary flow
input = prepare(raw_data)
result = process(input, config={client, middleware, migrations, modeling, optimization})
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


### Schema Definition
```prisma
// prisma/schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String?
  posts     Post[]
  profile   Profile?
  createdAt DateTime @default(now())
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  Int
}

model Profile {
  id     Int    @id @default(autoincrement())
  bio    String
  user   User   @relation(fields: [userId], references: [id])
  userId Int    @unique
}
```

### Migrations
```bash
# Create migration
npx prisma migrate dev --name add_posts

# Apply migrations in production
npx prisma migrate deploy

# Reset database
npx prisma migrate reset

# Generate client
npx prisma generate
```

### Queries
```typescript
import { PrismaClient } from '@prisma/client';
const prisma = new PrismaClient();

// Create
const user = await prisma.user.create({
  data: { email: 'alice@example.com', name: 'Alice' },
});

// Read with relations
const users = await prisma.user.findMany({
  where: { email: { contains: '@example.com' } },
  include: { posts: true, profile: true },
  orderBy: { createdAt: 'desc' },
  take: 10,
});

// Update
await prisma.user.update({
  where: { id: 1 },
  data: { name: 'Updated Name' },
});

// Delete
await prisma.user.delete({ where: { id: 1 } });

// Transaction
const [user, post] = await prisma.$transaction([
  prisma.user.create({ data: { email: 'bob@example.com' } }),
  prisma.post.create({ data: { title: 'Hello', authorId: 1 } }),
]);

// Raw query
const result = await prisma.$queryRaw`SELECT * FROM "User" WHERE id = ${1}`;
```

### Middleware
```typescript
prisma.$use(async (params, next) => {
  if (params.model === 'User' && params.action === 'delete') {
    params.action = 'update';
    params.args.data = { deletedAt: new Date() };
  }
  return next(params);
});
```

## Common Patterns

- **Connection pooling**: Use `pgbouncer=true` in connection string or Prisma Accelerate
- **Seeding**: Create `prisma/seed.ts` and run with `npx prisma db seed`
- **Multiple databases**: Use multiple Prisma clients with different datasources
- **Soft delete**: Implement via middleware pattern

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
