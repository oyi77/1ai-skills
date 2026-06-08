---
name: postgres-queries
description: PostgreSQL optimization — query tuning, schema design, indexing strategies,
  and performance analysis
domain: development
---


## Overview

PostgreSQL query optimization and schema design. Covers EXPLAIN ANALYZE, index types, query rewriting, partitioning, and connection pooling.

## Capabilities

- Analyze query performance with EXPLAIN ANALYZE
- Design optimal indexes (B-tree, GIN, GiST, BRIN)
- Optimize slow queries through rewriting and restructuring
- Implement table partitioning for large datasets
- Configure connection pooling (PgBouncer, Supabase Pooler)

## When to Use

- Queries taking >100ms that should be <10ms
- Database CPU or I/O is a bottleneck
- Designing schema for a new high-traffic feature
- Planning partitioning strategy for large tables

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The postgres-queries workflow follows a standard pipeline pattern.

Core flow:
```
# postgres-queries primary flow
input = prepare(raw_data)
result = process(input, config={analysis, design, indexing, optimization, performance})
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


### EXPLAIN ANALYZE
```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.name, COUNT(o.id)
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE o.created_at > NOW() - INTERVAL '30 days'
GROUP BY u.name;
```

### Index Strategy
```sql
-- Composite index for common query pattern
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at DESC);

-- Partial index for active records
CREATE INDEX idx_active_users ON users(email) WHERE deleted_at IS NULL;

-- GIN index for JSONB
CREATE INDEX idx_metadata ON products USING GIN(metadata);
```

## Common Patterns

- **EXPLAIN first**: Always EXPLAIN ANALYZE before optimizing
- **Composite indexes**: Column order matters — put equality columns first, range last
- **Partial indexes**: Index only rows you query frequently
- **Connection pooling**: Use PgBouncer for >100 concurrent connections

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
