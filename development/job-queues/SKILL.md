---
name: job-queues
description: Background job processing — Bull/BullMQ, agenda, delayed jobs, retries, rate limiting, scheduled tasks
domain: development
tags:
- coding
- job
- queues
- software-engineering
- testing
---


## Overview

Implement background job processing — Bull/BullMQ for Redis-backed queues, delayed jobs, retries with backoff, rate limiting, and scheduled tasks.

## Capabilities

- Bull/BullMQ queue management
- Delayed and scheduled jobs
- Retry with exponential backoff
- Rate limiting
- Job priorities and concurrency
- Progress tracking and events
- Repeatable/cron jobs

## When to Use
**Trigger phrases:**
- "job queues"
- "Background job processing — Bull/BullMQ, agenda, delayed jobs, retries, rate lim"


- Sending emails/notifications asynchronously
- Processing image/video uploads
- Running scheduled reports
- Rate-limited API calls
- Long-running computations

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The job-queues workflow follows a standard pipeline pattern.

Core flow:
```
# job-queues primary flow
input = prepare(raw_data)
result = process(input, config={agenda, background, bull, bullmq, delayed})
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


### BullMQ Queue Setup

```javascript
import { Queue, Worker, QueueScheduler } from 'bullmq'

const emailQueue = new Queue('email', { connection: { host: 'localhost', port: 6379 } })

// Add jobs
await emailQueue.add('welcome', { userId: '123', email: 'user@example.com' })
await emailQueue.add('report', { reportId: '456' }, { delay: 5000 }) // Delayed 5s
await emailQueue.add('newsletter', { campaignId: '789' }, {
  repeat: { cron: '0 9 * * 1' } // Every Monday 9am
})
```

### Worker with Retries

```javascript
const worker = new Worker('email', async (job) => {
  if (job.name === 'welcome') {
    await sendWelcomeEmail(job.data.email)
  } else if (job.name === 'report') {
    await generateReport(job.data.reportId)
  }
}, {
  connection: { host: 'localhost', port: 6379 },
  concurrency: 5,
  limiter: { max: 100, duration: 60000 }, // 100 jobs per minute
})

// Retry options per job
await emailQueue.add('risky-job', data, {
  attempts: 3,
  backoff: { type: 'exponential', delay: 1000 },
  removeOnComplete: 100,
  removeOnFail: 500,
})
```

### Job Events

```javascript
worker.on('completed', (job) => {
  console.log(`Job ${job.id} completed`)
})

worker.on('failed', (job, err) => {
  console.error(`Job ${job.id} failed: ${err.message}`)
})

worker.on('progress', (job, progress) => {
  console.log(`Job ${job.id} progress: ${progress}%`)
})

// Update progress from inside job
await job.updateProgress(50)
```

### Rate Limiting

```javascript
const worker = new Worker('api-calls', processJob, {
  limiter: {
    max: 10,        // Max 10 jobs
    duration: 1000,  // Per second
    groupKey: 'accountId', // Rate limit per account
  },
})
```

### Priority Jobs

```javascript
await queue.add('urgent', data, { priority: 1 })  // Highest
await queue.add('normal', data, { priority: 5 })
await queue.add('low', data, { priority: 10 })     // Lowest
```

### Scheduled/Repeatable Jobs

```javascript
// Cron-based
await queue.add('cleanup', {}, {
  repeat: { cron: '0 2 * * *' }, // Daily at 2am
})

// Interval-based
await queue.add('sync', {}, {
  repeat: { every: 300000 }, // Every 5 minutes
})
```

## Common Patterns

- **Email queue**: Async email sending with retries
- **Image processing**: Resize/optimize uploads in background
- **Webhook delivery**: Retry failed webhooks with backoff
- **Rate-limited API**: Respect third-party API rate limits
- **Scheduled reports**: Generate and send reports on schedule

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