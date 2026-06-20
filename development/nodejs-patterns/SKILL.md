---
name: nodejs-patterns
description: Node.js patterns — Express, Fastify, streams, worker threads, clustering, performance optimization
domain: development
tags:
- coding
- nodejs
- patterns
- software-engineering
- testing
---


## Overview

Production Node.js patterns — framework selection (Express vs Fastify), streams for large data, worker threads for CPU tasks, clustering for multi-core, and performance optimization.

## Capabilities

- Express and Fastify framework patterns
- Stream processing for large datasets
- Worker threads for CPU-intensive tasks
- Cluster mode for multi-core utilization
- Memory leak detection and profiling
- Error handling and graceful shutdown
- Health checks and readiness probes

## When to Use

- Building REST APIs and backend services
- Processing large files or data streams
- CPU-intensive computations (image processing, crypto)
- Optimizing throughput on multi-core servers
- Debugging memory leaks or performance issues

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The nodejs-patterns workflow follows a standard pipeline pattern.

Core flow:
```
# nodejs-patterns primary flow
input = prepare(raw_data)
result = process(input, config={clustering, express, fastify, node, nodejs})
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


### Fastify Server

```javascript
import Fastify from 'fastify'

const app = Fastify({ logger: true })

// Schema-based validation
app.post('/users', {
  schema: {
    body: {
      type: 'object',
      required: ['email', 'name'],
      properties: { email: { type: 'string' }, name: { type: 'string' } },
    },
  },
}, async (request, reply) => {
  const user = await db.users.create(request.body)
  return reply.status(201).send(user)
})

await app.listen({ port: 3000 })
```

### Stream Processing

```javascript
import { createReadStream, createWriteStream } from 'fs'
import { Transform } from 'stream'
import { pipeline } from 'stream/promises'

const transform = new Transform({
  transform(chunk, encoding, callback) {
    const processed = chunk.toString().toUpperCase()
    callback(null, processed)
  },
})

await pipeline(
  createReadStream('input.txt'),
  transform,
  createWriteStream('output.txt')
)
```

### Worker Threads

```javascript
// worker.js
import { parentPort, workerData } from 'worker_threads'

const result = heavyComputation(workerData)
parentPort.postMessage(result)

// main.js
import { Worker } from 'worker_threads'

function runTask(data) {
  return new Promise((resolve, reject) => {
    const worker = new Worker('./worker.js', { workerData: data })
    worker.on('message', resolve)
    worker.on('error', reject)
  })
}

// Run 4 tasks in parallel
const results = await Promise.all([1, 2, 3, 4].map(n => runTask(n)))
```

### Cluster Mode

```javascript
import cluster from 'cluster'
import os from 'os'

if (cluster.isPrimary) {
  const cpus = os.cpus().length
  for (let i = 0; i < cpus; i++) cluster.fork()

  cluster.on('exit', (worker) => {
    console.log(`Worker ${worker.process.pid} died, restarting...`)
    cluster.fork()
  })
} else {
  const app = express()
  app.get('/', (req, res) => res.send('OK'))
  app.listen(3000)
}
```

### Graceful Shutdown

```javascript
process.on('SIGTERM', async () => {
  console.log('SIGTERM received, shutting down...')
  server.close(() => {
    db.end()
    process.exit(0)
  })
  setTimeout(() => process.exit(1), 10000) // Force after 10s
})
```

## Common Patterns

- **Fastify over Express**: 2-3x faster, schema validation built-in
- **Streams**: Never load large files entirely in memory
- **Worker threads**: Offload CPU tasks (image resize, PDF gen)
- **Clustering**: Use PM2 or native cluster for multi-core
- **Health checks**: `/health` endpoint for load balancers

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
