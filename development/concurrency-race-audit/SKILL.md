---
name: concurrency-race-audit
description: Auditing concurrent async code, thread safety, shared state mutation, event loop blocking, and connection pool leaks. Use when debugging intermittent race conditions, async deadlocks, database connection exhaustion, or unhandled promise leaks.
domain: development
subdomain: software-development
author: oyi77
license: Apache-2.0
version: 1.0.0
category: development
tags:
  - concurrency
  - race-conditions
  - async
  - event-loop
  - performance
  - thread-safety
---

## Overview

Concurrent software fails subtly through non-deterministic execution timing, unprotected shared mutable memory, interleaved asynchronous microtasks, and connection pool starvation. The Concurrency Race Audit playbook provides a rigorous method for analyzing asynchronous call graphs, identifying atomicity breaks, eliminating event loop blocking, and validating concurrent throughput under stress.

## Anti-Rationalization Table

| Rationalization | Engineering Reality | Strict Protocol |
|---|---|---|
| "It works fine in local testing without crashing." | Concurrency defects are timing-dependent and rarely reproduce under single-user local development loads. | Subject concurrent pathways to synthetic load tests, high-concurrency race harnesses, and chaos injectors. |
| "Node.js is single-threaded, so mutex locks are unnecessary." | Single-threaded applies only to JavaScript execution; interleaved `await` points allow check-then-act race conditions. | Protect critical state transitions with async mutexes, atomic operations, or transactional database locks. |
| "Adding a short sleep or `setTimeout` resolves the race condition." | Fixed delays create flaky tests, slow down pipelines, and fail whenever system load changes. | Never use time delays for synchronization. Use explicit coordination primitives (mutex, semaphore, event barrier). |
| "Database transactions guarantee concurrency safety automatically." | Default isolation levels (e.g. READ COMMITTED) permit non-repeatable reads and lost updates during concurrent writes. | Use pessimistic locking (`SELECT ... FOR UPDATE`), optimistic version checks, or SERIALIZABLE isolation for money and inventory. |
| "Fire-and-forget background tasks are fine without awaiting." | Unawaited promises swallow runtime exceptions, lose request tracing context, and exhaust DB connection pools. | Always track background tasks with structured concurrency, worker queues (e.g. BullMQ, Celery), or bounded process managers. |
| "Spawning more workers will fix throughput stalls." | If the root cause is synchronous CPU blocking or connection pool saturation, additional workers exacerbate the stall. | Profile CPU blocking and pool utilization first. Offload heavy synchronous computation to worker threads or subprocesses. |

## When to Use

- Systems handling concurrent writes to shared balances, inventory counts, or booking slots.
- Services experiencing mysterious intermittent database connection timeouts or pool exhaustion under traffic spikes.
- Diagnosing event loop latency spikes, dropped WebSocket heartbeats, or hung HTTP requests.
- Auditing Node.js / Python async architectures for unhandled promise rejections and race conditions.

## When NOT to Use

- Purely static, single-threaded batch CLI scripts that run sequentially from start to finish.
- Stateless pure functions that operate strictly on immutable input data and return new values.
- CRUD operations where database unique constraints already provide complete idempotency guarantees.

## Workflow

```
┌────────────────────────────────────────────────────────┐
│             Concurrency Race Audit Workflow            │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 1. Async Call-Path & Shared State Inventory            │
│    - Identify global state, module singletons, caches  │
│    - Trace read-modify-write patterns across awaits    │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 2. Check-Then-Act & Atomicity Analysis                 │
│    - Locate interleaved await gaps in state updates    │
│    - Audit DB queries for lost update vulnerabilities   │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 3. Synchronization & Concurrency Primitives            │
│    - Apply in-memory async mutex / keyed locking       │
│    - Implement DB pessimistic locks (FOR UPDATE)       │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 4. Connection Pool & Resource Leak Inspection          │
│    - Verify every client acquisition has guaranteed release│
│    - Configure pool timeouts and max lifecycle bounds  │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 5. Stress Testing & Race Condition Verification        │
│    - Run concurrent burst tests with Promise.all       │
│    - Prove deterministic output under heavy contention │
└───────────────────────────┘
```

### Step 1: Async Call-Path & Shared State Inventory
Audit the codebase for shared in-memory mutable state:
- Search for module-level variables modified across async functions: `let cache`, `globalState`, `Map` instances.
- Trace every sequence where data is read, awaited, modified, and written back.

### Step 2: Check-Then-Act & Atomicity Analysis
Check if another async task can mutate state between the check and the action:
- Example flaw: `if (balance >= amount) { await doWork(); balance -= amount; }`.
- Another request can execute while `doWork()` is awaiting, causing double-spending.

### Step 3: Synchronization & Concurrency Primitives
Introduce robust synchronization:
- **In-Memory**: Use a keyed async mutex so operations on the same entity (e.g. user ID) queue sequentially while different entities run concurrently.
- **Distributed / DB**: Use `SELECT ... FOR UPDATE` in SQL or Redis redlock for multi-instance deployments.

### Step 4: Connection Pool & Resource Leak Inspection
Audit pool acquisition lifecycles:
- Ensure all DB connections, file descriptors, and HTTP clients are released in `finally` blocks.
- Set explicit acquisition timeouts to prevent infinite request queuing during outages.

### Step 5: Stress Testing & Race Condition Verification
Write an automated regression test simulating concurrent requests:
- Fire 50 concurrent requests simultaneously using `Promise.all` or `asyncio.gather`.
- Assert that final state (balance, inventory, counter) matches exact mathematical invariants.

## Code Examples

### TypeScript Keyed Async Mutex for Safe Entity Mutation

```typescript
export class KeyedAsyncMutex {
  private queues = new Map<string, Promise<void>>();

  async runExclusive<T>(key: string, task: () => Promise<T>): Promise<T> {
    while (this.queues.has(key)) {
      await this.queues.get(key);
    }

    let release: () => void;
    const lockPromise = new Promise<void>((resolve) => {
      release = resolve;
    });

    this.queues.set(key, lockPromise);

    try {
      return await task();
    } finally {
      this.queues.delete(key);
      release!();
    }
  }
}

// Usage in controller or service:
const mutex = new KeyedAsyncMutex();

export async function deductBalance(userId: string, amount: number) {
  return mutex.runExclusive(userId, async () => {
    const user = await db.user.findUnique({ where: { id: userId } });
    if (!user || user.balance < amount) {
      throw new Error('Insufficient funds');
    }
    return db.user.update({
      where: { id: userId },
      data: { balance: user.balance - amount },
    });
  });
}
```

### Python Asyncio Semaphore for Bounded Concurrent Scraping

```python
import asyncio
import httpx
from typing import List, Dict

async def fetch_item(client: httpx.AsyncClient, semaphore: asyncio.Semaphore, item_id: int) -> Dict:
    async with semaphore:
        # Guarantee no more than N concurrent HTTP requests
        response = await client.get(f"https://api.example.com/items/{item_id}", timeout=10.0)
        response.raise_for_status()
        return response.json()

async def fetch_all_items(item_ids: List[int], max_concurrency: int = 5) -> List[Dict]:
    semaphore = asyncio.Semaphore(max_concurrency)
    async with httpx.AsyncClient() as client:
        tasks = [fetch_item(client, semaphore, i) for i in item_ids]
        return await asyncio.gather(*tasks, return_exceptions=False)
```

### Database Pessimistic Row Locking in Raw SQL / Knex

```typescript
import { Knex } from 'knex';

export async function processPaymentTransaction(knex: Knex, accountId: string, amount: number) {
  return knex.transaction(async (trx) => {
    // Pessimistic lock: SELECT ... FOR UPDATE blocks concurrent reads for update
    const account = await trx('accounts')
      .where({ id: accountId })
      .forUpdate()
      .first();

    if (!account || account.balance < amount) {
      throw new Error('Transaction rejected: insufficient balance');
    }

    const newBalance = account.balance - amount;
    await trx('accounts')
      .where({ id: accountId })
      .update({ balance: newBalance, updated_at: new Date() });

    await trx('audit_ledger').insert({
      account_id: accountId,
      amount: -amount,
      balance_after: newBalance,
      created_at: new Date(),
    });

    return newBalance;
  });
}
```

## Verification Checklist

- [ ] All check-then-act sequences inspected for interleaved `await` or `yield` points.
- [ ] Critical state updates protected by appropriate synchronization (mutex, DB lock, optimistic versioning).
- [ ] Connection pool acquisitions guaranteed release via `try ... finally` blocks.
- [ ] No unbounded `Promise.all` calls over large dynamic collections; concurrency bounded with p-limit or semaphores.
- [ ] Event loop lag monitored; CPU-intensive JSON or crypto operations offloaded to worker threads.
- [ ] Automated concurrent stress test verifies mathematical invariants under 50+ parallel requests.
