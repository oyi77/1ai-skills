---
name: postgres-queries
description: PostgreSQL optimization — query tuning, schema design, indexing strategies, and performance analysis
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

## Pseudo Code

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
