---
name: dynamodb-patterns
description: Amazon DynamoDB patterns — single table design, GSI/LSI, DynamoDB Streams, PartiQL, performance optimization
domain: development
tags:
- coding
- dynamodb
- patterns
- software-engineering
- testing
---


## Overview

DynamoDB is a fully managed NoSQL key-value and document database by AWS. It delivers single-digit millisecond performance at any scale with built-in security, backup, and in-memory caching.

## Capabilities

- Single table design for access pattern optimization
- Partition key and sort key for data distribution
- Global Secondary Indexes (GSI) and Local Secondary Indexes (LSI)
- DynamoDB Streams for change data capture
- PartiQL for SQL-compatible queries
- DAX (DynamoDB Accelerator) for caching
- On-demand or provisioned capacity modes
- Transactions for multi-item operations

## When to Use

- Serverless applications on AWS
- Need predictable single-digit millisecond latency
- Access patterns are well-defined upfront
- Need automatic scaling without capacity planning
- Event-driven architectures with DynamoDB Streams

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The dynamodb-patterns workflow follows a standard pipeline pattern.

Core flow:
```
# dynamodb-patterns primary flow
input = prepare(raw_data)
result = process(input, config={amazon, design, dynamodb, optimization, partiql})
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


### Single Table Design
```typescript
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient, PutCommand, QueryCommand } from '@aws-sdk/lib-dynamodb';

const client = new DynamoDBClient({ region: 'us-east-1' });
const docClient = DynamoDBDocumentClient.from(client);

// Single table with overloaded keys
// PK: USER#123, SK: PROFILE
// PK: USER#123, SK: ORDER#456
// PK: ORDER#456, SK: USER#123

await docClient.send(new PutCommand({
  TableName: 'MyTable',
  Item: {
    PK: 'USER#123',
    SK: 'PROFILE',
    name: 'Alice',
    email: 'alice@example.com',
    GSI1PK: 'EMAIL#alice@example.com',
    GSI1SK: 'USER',
  },
}));
```

### Query Patterns
```typescript
// Query by partition key
const result = await docClient.send(new QueryCommand({
  TableName: 'MyTable',
  KeyConditionExpression: 'PK = :pk',
  ExpressionAttributeValues: { ':pk': 'USER#123' },
}));

// Query with sort key condition
const orders = await docClient.send(new QueryCommand({
  TableName: 'MyTable',
  KeyConditionExpression: 'PK = :pk AND begins_with(SK, :sk)',
  ExpressionAttributeValues: { ':pk': 'USER#123', ':sk': 'ORDER#' },
}));

// Query GSI
const byEmail = await docClient.send(new QueryCommand({
  TableName: 'MyTable',
  IndexName: 'GSI1',
  KeyConditionExpression: 'GSI1PK = :pk',
  ExpressionAttributeValues: { ':pk': 'EMAIL#alice@example.com' },
}));
```

### Transactions
```typescript
import { TransactWriteCommand } from '@aws-sdk/lib-dynamodb';

await docClient.send(new TransactWriteCommand({
  TransactItems: [
    { Put: { TableName: 'MyTable', Item: { PK: 'USER#123', SK: 'PROFILE', name: 'Alice' } } },
    { Put: { TableName: 'MyTable', Item: { PK: 'USER#123', SK: 'ORDER#789', total: 99 } } },
  ],
}));
```

### DynamoDB Streams + Lambda
```typescript
// Lambda handler for DynamoDB Stream
export const handler = async (event) => {
  for (const record of event.Records) {
    if (record.eventName === 'INSERT') {
      console.log('New item:', record.dynamodb.NewImage);
    }
    if (record.eventName === 'MODIFY') {
      console.log('Old:', record.dynamodb.OldImage);
      console.log('New:', record.dynamodb.NewImage);
    }
  }
};
```

### PartiQL
```sql
-- Insert
INSERT INTO "MyTable" VALUE {'PK': 'USER#123', 'SK': 'PROFILE', 'name': 'Alice'}

-- Select
SELECT * FROM "MyTable" WHERE "PK" = 'USER#123'

-- Update
UPDATE "MyTable" SET "name" = 'Updated' WHERE "PK" = 'USER#123' AND "SK" = 'PROFILE'
```

## Common Patterns

- **Access pattern first**: Design table around query patterns, not entity relationships
- **GSI overloading**: Use one GSI with overloaded attribute names for multiple access patterns
- **Write sharding**: Add random suffix to hot partition keys for write distribution
- **DAX caching**: Use DAX for read-heavy, latency-sensitive workloads
- **Capacity modes**: On-demand for unpredictable, provisioned for steady-state

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
