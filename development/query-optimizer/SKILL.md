---
name: query-optimizer
description: Slow query analysis — EXPLAIN plans, index recommendations, N+1 detection, and caching strategies. Use when working with query optimizer.
domain: development
tags:
- coding
- optimizer
- query
- software-engineering
- testing
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
**Trigger phrases:**
- "query optimizer"
- "Slow query analysis — EXPLAIN plans, index recommendations, N+1 detection, and c"


- Application response time is degraded
- Database CPU/IO is consistently high
- Specific queries are timing out
- Need to optimize for cost (fewer DB compute hours)

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The query-optimizer workflow follows a standard pipeline pattern.

Core flow:
```
# query-optimizer primary flow
input = prepare(raw_data)
result = process(input, config={analysis, caching, detection, explain, index})
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