---
name: cassandra-patterns
description: Apache Cassandra patterns — data modeling, CQL, partition keys, clustering, replication, performance tuning
---

## Overview

Apache Cassandra is a distributed NoSQL database designed for high availability and linear scalability. It uses CQL (Cassandra Query Language) and follows a partition-row data model optimized for write-heavy workloads.

## Capabilities

- Linear scalability by adding nodes
- CQL (SQL-like query language)
- Partition key design for even data distribution
- Clustering columns for sorted storage within partitions
- Tunable consistency levels (ONE, QUORUM, ALL, etc.)
- Multi-datacenter replication
- Compaction strategies for storage optimization
- Lightweight transactions (LWT) for conditional updates

## When to Use

- Write-heavy workloads requiring high throughput
- Multi-datacenter, globally distributed applications
- Need linear scalability without downtime
- Time-series data or IoT sensor data
- Applications tolerant of eventual consistency

## Pseudo Code

### Schema Design
```sql
CREATE KEYSPACE myapp WITH REPLICATION = {
  'class': 'NetworkTopologyStrategy',
  'us-east1': 3,
  'eu-west1': 3
};

CREATE TABLE myapp.users (
  user_id UUID PRIMARY KEY,
  name TEXT,
  email TEXT,
  created_at TIMESTAMP
);

-- Partition key + clustering for time-series
CREATE TABLE myapp.sensor_data (
  sensor_id UUID,
  reading_time TIMESTAMP,
  value DOUBLE,
  PRIMARY KEY (sensor_id, reading_time)
) WITH CLUSTERING ORDER BY (reading_time DESC);
```

### Queries (Node.js)
```typescript
import { Client } from 'cassandra-driver';

const client = new Client({
  contactPoints: ['node1', 'node2'],
  localDataCenter: 'us-east1',
  keyspace: 'myapp',
});

// Insert
await client.execute(
  'INSERT INTO users (user_id, name, email) VALUES (uuid(), ?, ?)',
  ['Alice', 'alice@example.com'],
  { prepare: true }
);

// Select with partition key
const result = await client.execute(
  'SELECT * FROM sensor_data WHERE sensor_id = ? AND reading_time > ?',
  [sensorId, startDate],
  { prepare: true }
);

// Batch (same partition only)
const batch = [
  { query: 'INSERT INTO sensor_data (sensor_id, reading_time, value) VALUES (?, ?, ?)', params: [id, time1, val1] },
  { query: 'INSERT INTO sensor_data (sensor_id, reading_time, value) VALUES (?, ?, ?)', params: [id, time2, val2] },
];
await client.batch(batch, { prepare: true });
```

### Consistency Levels
```typescript
import { types } from 'cassandra-driver';

// Strong consistency
await client.execute(query, params, {
  consistency: types.consistencies.quorum,
  prepare: true,
});

// Eventually consistent (faster)
await client.execute(query, params, {
  consistency: types.consistencies.one,
  prepare: true,
});
```

### Lightweight Transactions
```sql
-- Conditional insert (IF NOT EXISTS)
INSERT INTO users (user_id, email) VALUES (uuid(), 'alice@example.com') IF NOT EXISTS;

-- Conditional update
UPDATE users SET name = 'Updated' WHERE user_id = ? IF name = 'Old';
```

## Common Patterns

- **Partition key design**: Choose high-cardinality keys for even distribution; avoid hot partitions
- **Clustering columns**: Use for sorting data within a partition (time-series, alphabetical)
- **Denormalization**: Create multiple tables for different query patterns (no JOINs)
- **TTL**: Use `USING TTL 86400` for auto-expiring data (sessions, cache)
- **Compaction**: STCS (write-heavy), LCS (read-heavy), TWCS (time-series)
