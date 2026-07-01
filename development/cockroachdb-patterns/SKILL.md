---
name: cockroachdb-patterns
description: CockroachDB distributed SQL — PostgreSQL compatible, serializable isolation, geo-partitioning, multi-region
domain: development
tags:
- cockroachdb
- coding
- patterns
- software-engineering
- testing
---


## Overview

CockroachDB is a distributed SQL database that's wire-compatible with PostgreSQL. It provides serializable isolation, automatic sharding, geo-partitioning, and multi-region deployment out of the box.

## Capabilities

- PostgreSQL wire protocol compatibility
- Serializable isolation by default
- Automatic data sharding and rebalancing
- Geo-partitioning for data locality
- Multi-region with zone configurations
- Changefeeds for CDC (Change Data Capture)
- Follower reads for low-latency reads
- Online schema changes

## When to Use
**Trigger phrases:**
- "cockroachdb patterns"
- "CockroachDB distributed SQL — PostgreSQL compatible, serializable isolation, geo"


- Need distributed SQL with PostgreSQL compatibility
- Multi-region deployments with data locality requirements
- Want serializable isolation without performance penalty
- Migrating from PostgreSQL to distributed architecture

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The cockroachdb-patterns workflow follows a standard pipeline pattern.

Core flow:
```
# cockroachdb-patterns primary flow
input = prepare(raw_data)
result = process(input, config={cockroachdb, compatible, distributed, isolation, multi})
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


### Connection
```typescript
import { Pool } from 'pg';

const pool = new Pool({
  connectionString: 'postgresql://root@localhost:26257/defaultdb?sslmode=disable',
});
```

### Geo-Partitioning
```sql
-- Create partitioned table
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name STRING,
  region STRING NOT NULL
) PARTITION BY LIST (region);

-- Create partitions
ALTER TABLE users PARTITION BY LIST (region) (
  PARTITION us VALUES IN ('us-east', 'us-west'),
  PARTITION eu VALUES IN ('eu-west', 'eu-central'),
  PARTITION apac VALUES IN ('ap-southeast', 'ap-northeast')
);

-- Configure zones
ALTER PARTITION us OF TABLE users CONFIGURE ZONE USING
  constraints = '[+region=us-east1]';
```

### Changefeeds
```sql
-- Create changefeed to cloud storage
CREATE CHANGEFEED FOR users INTO 's3://bucket/changefeed'
  WITH format = 'json', resolved = '10s';

-- Create changefeed to Kafka
CREATE CHANGEFEED FOR users INTO 'kafka://broker:9092'
  WITH format = 'json', topic_name = 'users';
```

### Follower Reads
```sql
-- Read from nearest follower (slightly stale)
SELECT * FROM users AS OF SYSTEM TIME follower_read_timestamp();

-- Bounded staleness
SELECT * FROM users AS OF SYSTEM TIME '-5s';
```

### Multi-Region Setup
```sql
-- Set regions
ALTER DATABASE mydb SET PRIMARY REGION "us-east1";
ALTER DATABASE mydb ADD REGION "eu-west1";
ALTER DATABASE mydb ADD REGION "ap-southeast1";

-- Global table (low-latency reads everywhere)
ALTER TABLE config SET LOCALITY GLOBAL;

-- Regional by row (data pinned to user's region)
ALTER TABLE users SET LOCALITY REGIONAL BY ROW;
```

## Common Patterns

- **Schema migrations**: Use `flyway` or `migrate` with CockroachDB dialect
- **Connection pooling**: Use PgBouncer or built-in connection handling
- **Serializable retries**: Wrap transactions in retry loops for serialization errors
- **Performance**: Use `EXPLAIN ANALYZE` to optimize distributed queries

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