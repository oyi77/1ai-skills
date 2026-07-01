---
name: drizzle-orm
description: Drizzle ORM — type-safe SQL, schema definitions, migrations, queries, relations for TypeScript/Node.js. Use when working with drizzle orm.
domain: development
tags:
- coding
- drizzle
- orm
- software-engineering
- testing
---


## Overview

Drizzle ORM is a lightweight TypeScript ORM that feels like writing SQL. It provides type-safe schema definitions, automatic migrations, and a query builder that maps 1:1 to SQL.

## Capabilities

- Type-safe schema definitions with Drizzle schema language
- Automatic migration generation with Drizzle Kit
- Select, insert, update, delete with full type inference
- Relations API for one-to-one, one-to-many, many-to-many
- Transactions and batch operations
- Support for PostgreSQL, MySQL, SQLite, Turso, D1

## When to Use
**Trigger phrases:**
- "drizzle orm"
- "Drizzle ORM — type-safe SQL, schema definitions, migrations, queries, relations "


- Building TypeScript/Node.js backends with SQL databases
- Need type safety without heavy ORM overhead
- Want SQL-like syntax instead of Active Record patterns
- Working with edge databases (D1, Turso, Neon)

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The drizzle-orm workflow follows a standard pipeline pattern.

Core flow:
```
# drizzle-orm primary flow
input = prepare(raw_data)
result = process(input, config={definitions, drizzle, migrations, node, orm})
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
```typescript
import { pgTable, serial, text, integer, timestamp } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
  createdAt: timestamp('created_at').defaultNow(),
});

export const posts = pgTable('posts', {
  id: serial('id').primaryKey(),
  title: text('title').notNull(),
  authorId: integer('author_id').references(() => users.id),
});
```

### Queries
```typescript
import { eq, and, desc } from 'drizzle-orm';
import { db } from './db';
import { users, posts } from './schema';

// Select
const allUsers = await db.select().from(users);
const user = await db.select().from(users).where(eq(users.id, 1));

// Insert
await db.insert(users).values({ name: 'Alice', email: 'alice@example.com' });

// Update
await db.update(users).set({ name: 'Bob' }).where(eq(users.id, 1));

// Delete
await db.delete(users).where(eq(users.id, 1));

// Join
const result = await db
  .select({ userName: users.name, postTitle: posts.title })
  .from(users)
  .leftJoin(posts, eq(users.id, posts.authorId))
  .orderBy(desc(users.createdAt))
  .limit(10);
```

### Relations
```typescript
import { relations } from 'drizzle-orm';

export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
}));

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, { fields: [posts.authorId], references: [users.id] }),
}));

// Query with relations
const usersWithPosts = await db.query.users.findMany({
  with: { posts: true },
});
```

### Migrations
```bash
# Generate migration
npx drizzle-kit generate

# Apply migration
npx drizzle-kit migrate

# Push schema directly (dev only)
npx drizzle-kit push

# Open studio
npx drizzle-kit studio
```

### Transactions
```typescript
await db.transaction(async (tx) => {
  const user = await tx.insert(users).values({ name: 'Alice' }).returning();
  await tx.insert(posts).values({ title: 'Hello', authorId: user[0].id });
});
```

## Common Patterns

- **drizzle.config.ts**: Configure schema path, output dir, DB driver
- **Connection pooling**: Use with Neon serverless, PgBouncer, or Hyperdrive
- **Edge deployment**: Works with Cloudflare D1, Turso, Neon serverless driver
- **Seeding**: Create seed scripts using the same schema types

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