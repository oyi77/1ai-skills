---
name: event-driven
description: Event-driven architecture — event sourcing, CQRS, saga pattern, event
  buses, pub/sub patterns
domain: development
---


## Overview

Design event-driven systems — event sourcing for audit trails, CQRS for read/write separation, saga pattern for distributed transactions, and event bus implementation.

## Capabilities

- Event sourcing (append-only event log)
- CQRS (Command Query Responsibility Segregation)
- Saga choreography and orchestration
- Event bus design (in-process and distributed)
- Event versioning and schema evolution
- Idempotent event handling
- Eventual consistency patterns

## When to Use

- Need complete audit trail of all state changes
- High read/write ratio with different optimization needs
- Distributed transactions across microservices
- Complex business workflows with compensating actions
- Real-time event streaming to multiple consumers

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The event-driven workflow follows a standard pipeline pattern.

Core flow:
```
# event-driven primary flow
input = prepare(raw_data)
result = process(input, config={architecture, buses, cqrs, driven, event})
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


### Event Sourcing — Event Store

```javascript
class EventStore {
  constructor() { this.events = [] }

  append(aggregateId, eventType, data, metadata = {}) {
    const event = {
      id: crypto.randomUUID(),
      aggregateId,
      type: eventType,
      data,
      metadata,
      timestamp: Date.now(),
      version: this.getLatestVersion(aggregateId) + 1,
    }
    this.events.push(event)
    return event
  }

  getEvents(aggregateId) {
    return this.events.filter(e => e.aggregateId === aggregateId)
  }

  replay(aggregateId) {
    return this.getEvents(aggregateId).reduce((state, event) => {
      return applyEvent(state, event)
    }, initialState)
  }
}

// Usage
const store = new EventStore()
store.append('order-123', 'OrderCreated', { items: [...], total: 99.99 })
store.append('order-123', 'OrderPaid', { paymentId: 'pay-456' })
store.append('order-123', 'OrderShipped', { trackingId: 'track-789' })
```

### CQRS — Separate Read/Write Models

```javascript
// Command side (write model)
class OrderCommandHandler {
  constructor(eventStore) { this.eventStore = eventStore }

  handleCreateOrder(command) {
    const event = { type: 'OrderCreated', data: command }
    this.eventStore.append(command.orderId, 'OrderCreated', command)
    // Publish to event bus
    eventBus.publish(event)
  }

  handlePayOrder(command) {
    const order = this.eventStore.replay(command.orderId)
    if (order.status !== 'created') throw new Error('Invalid state')
    this.eventStore.append(command.orderId, 'OrderPaid', command)
  }
}

// Query side (read model — optimized for reads)
class OrderProjection {
  constructor(db) { this.db = db }

  async handleEvent(event) {
    if (event.type === 'OrderCreated') {
      await this.db.orders.insert({ id: event.data.orderId, status: 'created', ...event.data })
    } else if (event.type === 'OrderPaid') {
      await this.db.orders.update(event.data.orderId, { status: 'paid' })
    }
  }

  async getOrder(id) {
    return this.db.orders.findById(id) // Fast read from projection
  }
}
```

### Saga — Choreography

```javascript
// Order Saga — each service handles its own step and publishes events

// Order Service
eventBus.on('OrderCreated', async (event) => {
  await reserveInventory(event.data)
  eventBus.publish({ type: 'InventoryReserved', data: event.data })
})

// Payment Service
eventBus.on('InventoryReserved', async (event) => {
  await processPayment(event.data)
  eventBus.publish({ type: 'PaymentProcessed', data: event.data })
})

// Shipping Service
eventBus.on('PaymentProcessed', async (event) => {
  await createShipment(event.data)
  eventBus.publish({ type: 'OrderShipped', data: event.data })
})

// Compensation — if payment fails
eventBus.on('PaymentFailed', async (event) => {
  await releaseInventory(event.data)
  eventBus.publish({ type: 'OrderCancelled', data: event.data })
})
```

### Saga — Orchestration

```javascript
class OrderSaga {
  constructor() { this.step = 0 }

  async execute(order) {
    try {
      await this.step1ReserveInventory(order)
      await this.step2ProcessPayment(order)
      await this.step3CreateShipment(order)
    } catch (err) {
      await this.compensate(order, err)
    }
  }

  async compensate(order, err) {
    if (this.step >= 3) await this.undoShipment(order)
    if (this.step >= 2) await this.refundPayment(order)
    if (this.step >= 1) await this.releaseInventory(order)
  }
}
```

### Event Bus (In-Process)

```javascript
class EventBus {
  constructor() { this.handlers = new Map() }

  on(eventType, handler) {
    if (!this.handlers.has(eventType)) this.handlers.set(eventType, [])
    this.handlers.get(eventType).push(handler)
  }

  async publish(event) {
    const handlers = this.handlers.get(event.type) || []
    await Promise.all(handlers.map(h => h(event)))
  }
}
```

## Common Patterns

- **Event sourcing + CQRS**: Write events, project to read models
- **Saga choreography**: Decentralized, each service handles its step
- **Saga orchestration**: Centralized coordinator for complex flows
- **Event versioning**: Support old event schemas during migration
- **Idempotency**: Process events exactly once with deduplication
- **Snapshotting**: Periodically snapshot aggregate state for fast replay

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
