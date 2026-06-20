---
name: rabbitmq-patterns
description: RabbitMQ patterns — exchanges, queues, routing, dead letter queues, priority queues, clustering
domain: development
tags:
- coding
- patterns
- rabbitmq
- software-engineering
- testing
---


## Overview

Design and operate RabbitMQ — exchange types, queue bindings, dead letter handling, priority queues, publisher confirms, and clustering.

## Capabilities

- Exchange types (direct, fanout, topic, headers)
- Queue management and bindings
- Dead letter queues
- Priority queues
- Publisher confirms
- Consumer acknowledgments
- Clustering and high availability

## When to Use

- Task queue / background job processing
- Request-reply patterns
- Pub/sub messaging
- Message routing with complex rules
- Reliable message delivery

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The rabbitmq-patterns workflow follows a standard pipeline pattern.

Core flow:
```
# rabbitmq-patterns primary flow
input = prepare(raw_data)
result = process(input, config={clustering, dead, exchanges, letter, patterns})
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


### Setup (Node.js with amqplib)

```javascript
import amqplib from 'amqplib'

const conn = await amqplib.connect('amqp://localhost')
const ch = await conn.createChannel()

// Declare exchange
await ch.assertExchange('events', 'topic', { durable: true })

// Declare queue with dead letter
await ch.assertQueue('order-processing', {
  durable: true,
  deadLetterExchange: 'dlx',
  deadLetterRoutingKey: 'dead.order',
  messageTtl: 60000,
  maxLength: 10000,
})

// Bind queue to exchange
await ch.bindQueue('order-processing', 'events', 'order.*')
```

### Publish with Confirm

```javascript
await ch.assertExchange('events', 'topic', { durable: true })
await ch.publish('events', 'order.created', Buffer.from(JSON.stringify(order)), {
  persistent: true,
  correlationId: orderId,
  timestamp: Date.now(),
})

// Wait for confirm
const confirmed = await ch.waitForConfirms()
```

### Consume with Acknowledgment

```javascript
await ch.consume('order-processing', async (msg) => {
  try {
    const order = JSON.parse(msg.content.toString())
    await processOrder(order)
    ch.ack(msg) // Success
  } catch (err) {
    // Requeue if retryable, otherwise dead letter
    ch.nack(msg, false, false) // Send to DLQ
  }
})
```

### Topic Routing

```javascript
// Exchange: events
// Routing keys: order.created, order.paid, order.shipped
//               payment.received, payment.failed
//               user.signup, user.updated

// Queue subscribes to all order events
await ch.bindQueue('order-service', 'events', 'order.*')

// Queue subscribes to specific payment events
await ch.bindQueue('payment-alerts', 'events', 'payment.failed')

// Queue subscribes to everything
await ch.bindQueue('audit-log', 'events', '#')
```

### Priority Queue

```javascript
await ch.assertQueue('priority-tasks', {
  durable: true,
  maxPriority: 10,
})

await ch.publish('', 'priority-tasks', Buffer.from(msg), {
  priority: 9, // Higher = processed first
})
```

### Dead Letter Queue Processing

```javascript
// Setup DLQ
await ch.assertExchange('dlx', 'direct', { durable: true })
await ch.assertQueue('dead-letters', { durable: true })
await ch.bindQueue('dead-letters', 'dlx', 'dead.order')

// Process dead letters
await ch.consume('dead-letters', async (msg) => {
  console.error('Dead letter:', JSON.parse(msg.content.toString()))
  // Log, alert, or retry with delay
  ch.ack(msg)
})
```

## Common Patterns

- **Work queue**: Competing consumers for task distribution
- **Pub/sub fanout**: Broadcast events to all subscribers
- **Topic routing**: Route by pattern (order.*, payment.*)
- **Dead letter queue**: Capture failed messages for analysis
- **Priority queue**: Process urgent messages first
- **Publisher confirms**: Ensure messages are persisted

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
