---
name: query-optimizer
description: Slow query analysis — EXPLAIN plans, index recommendations, N+1 detection, and caching strategies
---

## Overview

Systematic approach to finding and fixing slow queries. Covers EXPLAIN plan interpretation, index recommendations, N+1 detection, query caching, and connection pooling.

## Capabilities

- Interpret EXPLAIN ANALYZE output to find bottlenecks
- Recommend indexes based on query patterns
- Detect and fix N+1 query problems
- Implement query caching strategies
- Monitor and alert on slow queries

## When to Use

- Application response time is degraded
- Database CPU/IO is consistently high
- Specific queries are timing out
- Need to optimize for cost (fewer DB compute hours)

## Pseudo Code

### N+1 Detection
```python
# BAD: N+1 queries
for user in users:
    orders = db.query("SELECT * FROM orders WHERE user_id = ?", user.id)  # N queries

# GOOD: Single query with JOIN
users_with_orders = db.query("""
    SELECT u.*, json_agg(o.*) as orders
    FROM users u LEFT JOIN orders o ON o.user_id = u.id
    GROUP BY u.id
""")
```

### Query Cache
```python
import redis

def cached_query(key, query, ttl=300):
    result = redis.get(key)
    if result:
        return json.loads(result)
    result = db.execute(query)
    redis.setex(key, ttl, json.dumps(result))
    return result
```

## Common Patterns

- **EXPLAIN ANALYZE always**: Never guess — measure with EXPLAIN ANALYZE
- **Index for WHERE + ORDER BY**: Composite index covering both clauses
- **Batch over N+1**: Always use JOINs or IN clauses instead of loops
- **Cache hot queries**: Cache frequently accessed, rarely changed data
