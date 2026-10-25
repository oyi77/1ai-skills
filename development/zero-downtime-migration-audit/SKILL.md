---
name: zero-downtime-migration-audit
description: Auditing database migrations for backward and forward compatibility, table locks, safe index creation, and zero-downtime expand-contract patterns. Use when modifying production database schemas, renaming columns, adding NOT NULL constraints, or dropping tables.
domain: development
subdomain: software-development
author: oyi77
license: Apache-2.0
version: 1.0.0
category: development
tags:
  - database
  - migration
  - zero-downtime
  - postgres
  - schema-design
  - expand-contract
---

## Overview

In modern continuous deployment environments, application replicas run old and new versions concurrently during rolling updates. Naive schema migrations (such as instant column renames, adding `NOT NULL` columns without defaults, or standard index creation) acquire exclusive table locks or immediately break in-flight application pods. The Zero-Downtime Migration Audit playbook enforces the multi-phase Expand/Contract pattern, guaranteeing zero downtime and safe forward-only rollouts.

## Anti-Rationalization Table

| Rationalization | Engineering Reality | Strict Protocol |
|---|---|---|
| "We can rename the column directly with `ALTER TABLE RENAME COLUMN`." | Old application pods still executing during the rolling deployment will query the old column name and crash with 500 errors. | Never rename columns directly. Use the Expand/Contract pattern: add new column, dual-write, backfill, switch reads, drop old column. |
| "Adding a default value to a column is always instantaneous." | Volatile defaults (e.g. `clock_timestamp()`) or DDL in older database engines rewrite the whole table, locking reads and writes for hours. | Use constant defaults or add the column nullable, backfill values in batches, then set the default. |
| "`CREATE INDEX` is fast enough that users won't notice." | Standard `CREATE INDEX` acquires an `ACCESS EXCLUSIVE` lock in Postgres, blocking all write operations until the index finishes building. | Always create indexes concurrently: `CREATE INDEX CONCURRENTLY` in Postgres, or `ALGORITHM=INPLACE, LOCK=NONE` in MySQL. |
| "Adding a `NOT NULL` constraint won't fail because our frontend validates inputs." | Historical rows in the database may contain `NULL` values. Validating the table in a single transaction locks all writes. | Add constraints with `NOT VALID` first (no table scan lock), then validate in a separate non-blocking statement: `VALIDATE CONSTRAINT`. |
| "We can drop the deprecated column in the same migration as the new code deploy." | In-flight background workers or rolling back pods still reference the dropped column, causing instant crashes. | Decommission columns only in a subsequent release after all old application code has been completely replaced in production. |
| "Down migrations are always ready if the deploy fails." | Down migrations that drop columns destroy newly created user data permanently. | Schema migrations must be forward-compatible. Design migrations so that rolling back the application code requires zero database rollbacks. |

## When to Use

- Production database schema migrations on high-availability web applications requiring continuous uptime.
- Modifying tables with more than 50,000 rows where table locks cause connection pool exhaustion and cascading outages.
- Performing breaking schema changes: column renames, column splits, foreign key constraints, or changing data types.
- Rolling deployments across Kubernetes, ECS, or multi-server fleets where old and new app versions coexist.

## When NOT to Use

- Local testing environments using isolated ephemeral SQLite databases.
- Pre-launch greenfield applications with zero active production users and zero uptime requirements.
- Read-only data warehouse reporting tables rebuilt entirely from scratch via nightly batch jobs.

## Workflow

```
┌────────────────────────────────────────────────────────┐
│         Zero-Downtime Migration Audit Workflow         │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 1. Migration Risk Classification                       │
│    - Scan DDL for ACCESS EXCLUSIVE locks               │
│    - Classify: Additive (Safe) vs Destructive (Multi)  │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 2. Phase 1: Expand Phase (Additive Non-Breaking)       │
│    - Add new column as NULLABLE                        │
│    - Create indexes with CONCURRENTLY                  │
│    - Deploy dual-writing application code              │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 3. Phase 2: Historical Data Backfill                   │
│    - Backfill legacy rows in small, throttled batches  │
│    - Verify row count parity and checksum equality     │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 4. Phase 3: Switch Reads & Apply Constraints           │
│    - Switch application readers to the new column      │
│    - Add NOT NULL / CHECK constraints with NOT VALID   │
│    - Run VALIDATE CONSTRAINT in separate transaction   │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 5. Phase 4: Contract Phase (Safe Cleanup)              │
│    - Remove legacy write code from application         │
│    - Mark old column as DEPRECATED or drop safely      │
└───────────────────────────┘
```

### Step 1: Migration Risk Classification
Audit every DDL statement before applying to production:
- High-risk operations: `RENAME COLUMN`, `DROP COLUMN`, `ALTER COLUMN TYPE`, `CREATE INDEX` (without concurrent flag).
- Any high-risk operation MUST be rejected from single-step deployment and converted into an Expand/Contract workflow.

### Step 2: Phase 1 — Expand Phase
Apply non-blocking additive changes:
- Add the new column as `NULLABLE` without locks.
- If an index is needed, build it concurrently.
- Deploy the application version that writes to BOTH the old column and the new column, but continues reading from the old column.

### Step 3: Phase 2 — Historical Data Backfill
Migrate historical data without database stress:
- Execute backfills in small primary-key batches (e.g. 1,000 rows per batch) with sleep intervals to prevent I/O spikes.
- Monitor database replication lag and connection counts during backfill execution.

### Step 4: Phase 3 — Switch Reads & Enforce Invariants
Once backfill is complete:
- Deploy application code that reads from the new column and writes to both columns.
- Add constraints using non-blocking two-step validation (`ADD CONSTRAINT ... NOT VALID`, followed by `VALIDATE CONSTRAINT`).

### Step 5: Phase 4 — Contract Phase
After confirming zero application traffic touches the old column:
- Deploy application code that removes dual-writing logic.
- Drop or ignore the old column in a final, isolated cleanup migration.

## Code Examples

### PostgreSQL Safe Non-Blocking DDL Recipes (`migrations/safe_ddl.sql`)

```sql
-- 1. SAFE INDEX CREATION (Never blocks concurrent writes)
-- BAD: CREATE INDEX idx_users_email ON users(email);
-- GOOD:
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email ON users(email);

-- 2. SAFE NOT NULL CONSTRAINT ADDITION
-- BAD: ALTER TABLE users ALTER COLUMN phone SET NOT NULL;
-- GOOD (2-step non-blocking validation):
ALTER TABLE users ADD CONSTRAINT chk_users_phone_not_null CHECK (phone IS NOT NULL) NOT VALID;
ALTER TABLE users VALIDATE CONSTRAINT chk_users_phone_not_null;

-- 3. SAFE FOREIGN KEY ADDITION
-- BAD: ALTER TABLE orders ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id);
-- GOOD:
ALTER TABLE orders ADD CONSTRAINT fk_orders_user_id FOREIGN KEY (user_id) REFERENCES users(id) NOT VALID;
ALTER TABLE orders VALIDATE CONSTRAINT fk_orders_user_id;

-- 4. SAFE COLUMN DEFAULT ADDITION (Postgres >= 11)
-- Fast metadata-only update for constant defaults
ALTER TABLE orders ADD COLUMN status VARCHAR(32) DEFAULT 'pending' NOT NULL;
```

### Throttled Safe Backfill Script (Python / SQLAlchemy)

```python
import time
from sqlalchemy import create_engine, text

def safe_batch_backfill(database_url: str, batch_size: int = 1000, pause_sec: float = 0.1):
    engine = create_engine(database_url)
    
    with engine.connect() as conn:
        last_id = 0
        total_migrated = 0

        while True:
            # Query batch by indexed primary key
            query = text("""
                UPDATE users
                SET full_name = TRIM(first_name || ' ' || COALESCE(last_name, ''))
                WHERE id IN (
                    SELECT id FROM users
                    WHERE id > :last_id AND full_name IS NULL
                    ORDER BY id ASC
                    LIMIT :limit
                )
                RETURNING id;
            """)
            
            result = conn.execute(query, {"last_id": last_id, "limit": batch_size})
            updated_ids = [row[0] for row in result.fetchall()]
            conn.commit()

            if not updated_ids:
                print(f"Backfill complete! Total rows migrated: {total_migrated}")
                break

            last_id = max(updated_ids)
            total_migrated += len(updated_ids)
            print(f"Migrated batch up to ID {last_id} ({total_migrated} rows total)...")
            
            # Throttling to protect connection pool and replication lag
            time.sleep(pause_sec)

if __name__ == "__main__":
    import os
    db_url = os.environ.get("DATABASE_URL", "postgresql://user:pass@localhost:5432/appdb")
    safe_batch_backfill(db_url)
```

### Dual-Write Expand Pattern (TypeScript / Prisma)

```typescript
import { PrismaClient, User } from '@prisma/client';

export class UserRepository {
  constructor(private prisma: PrismaClient) {}

  // Phase 1 & 2: Dual-write to both legacy name and new firstName/lastName
  async createUser(data: { firstName: string; lastName: string; email: string }): Promise<User> {
    const fullName = `${data.firstName} ${data.lastName}`.trim();

    return await this.prisma.user.create({
      data: {
        email: data.email,
        // Legacy column (still read by older pods)
        name: fullName,
        // New columns (for zero-downtime transition)
        firstName: data.firstName,
        lastName: data.lastName,
      },
    });
  }

  // Phase 3: Read from new columns with safe fallback to legacy column
  async getUserDisplayName(id: string): Promise<string> {
    const user = await this.prisma.user.findUnique({
      where: { id },
      select: { name: true, firstName: true, lastName: true },
    });

    if (!user) return '';

    if (user.firstName || user.lastName) {
      return `${user.firstName ?? ''} ${user.lastName ?? ''}`.trim();
    }

    return user.name ?? '';
  }
}
```

## Verification Checklist

- [ ] All DDL statements audited for long-lived `ACCESS EXCLUSIVE` table locks.
- [ ] No `CREATE INDEX` statements executed without the `CONCURRENTLY` flag on Postgres.
- [ ] Column renames and type modifications converted into multi-step Expand/Contract workflows.
- [ ] Dual-writing implemented and deployed in application code prior to any data backfill.
- [ ] Historical data backfill executed using batched primary-key queries with throttling.
- [ ] `NOT NULL` constraints applied using `NOT VALID` followed by asynchronous validation.
- [ ] Zero database rollbacks required if newly deployed application code must be rolled back.
