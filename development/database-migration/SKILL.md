---
name: database-migration
description: Safe database migrations — schema changes, data migrations, rollback strategies, and zero-downtime deploys
domain: development
tags:
- coding
- database
- migration
- software-engineering
- testing
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

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The database-migration workflow follows a standard pipeline pattern.

Core flow:
```
# database-migration primary flow
input = prepare(raw_data)
result = process(input, config={changes, data, database, deploys, downtime})
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
