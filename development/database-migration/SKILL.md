---
name: database-migration
description: Safe database migrations — schema changes, data migrations, rollback strategies, and zero-downtime deploys
---

## Overview

Safe database migration practices. Covers migration tools (Prisma, Knex, Flyway), forward-only migrations, rollback strategies, data backfill, and zero-downtime deployments.

## Capabilities

- Write safe schema migrations (add column, rename, drop)
- Design rollback strategies for destructive changes
- Plan zero-downtime migrations for production
- Backfill data without locking tables
- Test migrations against production data snapshots

## When to Use

- Adding or modifying database schema
- Need zero-downtime deployment with schema changes
- Data migration between tables or formats
- Production migration needs rollback plan

## Pseudo Code

### Safe Column Addition
```sql
-- Step 1: Add column (nullable, no lock)
ALTER TABLE users ADD COLUMN phone VARCHAR(20) NULL;

-- Step 2: Backfill (in batches)
UPDATE users SET phone = legacy_phone WHERE phone IS NULL LIMIT 1000;

-- Step 3: Add NOT NULL constraint (after backfill complete)
ALTER TABLE users ALTER COLUMN phone SET NOT NULL;
```

### Prisma Migration
```bash
# Create migration
npx prisma migrate dev --name add_phone_column

# Deploy to production
npx prisma migrate deploy
```

## Common Patterns

- **Nullable first**: Add columns as NULL, backfill, then add NOT NULL
- **Batch backfill**: Update in batches of 1000 to avoid locking
- **Shadow tables**: Create new table, migrate data, swap names
- **Test with prod snapshot**: Always test migrations against prod data copy
