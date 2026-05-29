---
name: task-scheduler
description: Task scheduling and cron patterns — node-cron, BullMQ, Celery, systemd timers. Recurring jobs, distributed scheduling
---


## Overview

Task schedulers handle recurring jobs, delayed execution, and distributed work scheduling. This skill covers node-cron for simple scheduling, BullMQ for Redis-based job queues with delays and priorities, Celery for Python distributed task queues, and systemd timers for OS-level scheduling.

## Capabilities

- Schedule recurring tasks with cron expressions
- Build delayed and prioritized job queues with BullMQ
- Implement distributed task scheduling with Celery
- Use systemd timers for OS-level scheduling
- Handle job retries, backoff, and failure recovery
- Monitor job queues and execution metrics

## When to Use

- Running periodic tasks (cleanup, reports, sync)
- Need delayed job execution (send email after 5 min)
- Distributing work across multiple workers
- Scheduling at OS level without application dependency
- Need job persistence, retries, and monitoring

## Pseudo Code

The task-scheduler workflow follows a standard pipeline pattern.

Core flow:
```
# task-scheduler primary flow
input = prepare(raw_data)
result = process(input, config={bullmq, celery, cron, distributed, jobs})
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


### Node-Cron
```javascript
const cron = require('node-cron');

// Every day at 9am
cron.schedule('0 9 * * *', async () => {
  await generateDailyReport();
}, { timezone: 'Asia/Jakarta' });

// Every 5 minutes
cron.schedule('*/5 * * * *', async () => {
  await syncExternalData();
});

// Every Monday at 8am
cron.schedule('0 8 * * 1', async () => {
  await sendWeeklyDigest();
});

// Graceful shutdown
process.on('SIGTERM', () => {
  cron.getTasks().forEach(task => task.stop());
});
```

### BullMQ (Redis-based)
```javascript
const { Queue, Worker, QueueScheduler } = require('bullmq');

const emailQueue = new Queue('emails', {
  connection: { host: 'localhost', port: 6379 },
});

// Add delayed job
await emailQueue.add('send-welcome', {
  userId: '123',
  email: 'user@example.com',
}, {
  delay: 5000,                    // 5 second delay
  attempts: 3,                    // Retry 3 times
  backoff: { type: 'exponential', delay: 1000 },
  priority: 1,                    // Lower = higher priority
});

// Add recurring job
await emailQueue.add('send-digest', {}, {
  repeat: { cron: '0 9 * * *', tz: 'Asia/Jakarta' },
});

// Worker with concurrency
const worker = new Worker('emails', async (job) => {
  if (job.name === 'send-welcome') {
    await sendWelcomeEmail(job.data);
  } else if (job.name === 'send-digest') {
    await sendDigestEmail(job.data);
  }
}, {
  connection: { host: 'localhost', port: 6379 },
  concurrency: 10,
  limiter: { max: 100, duration: 60000 },  // Rate limit
});

worker.on('completed', (job) => console.log(`Done: ${job.id}`));
worker.on('failed', (job, err) => console.log(`Failed: ${job.id}`, err));

// Monitor
const scheduler = new QueueScheduler('emails', {
  connection: { host: 'localhost', port: 6379 },
});
```

### Celery (Python)
```python
from celery import Celery
from celery.schedules import crontab

app = Celery('tasks', broker='redis://localhost:6379/0')

# Simple task
@app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_email(self, to, subject, body):
    try:
        smtp_send(to, subject, body)
    except SMTPException as exc:
        raise self.retry(exc=exc)

# Scheduled tasks
app.conf.beat_schedule = {
    'daily-report': {
        'task': 'tasks.generate_report',
        'schedule': crontab(hour=9, minute=0),
        'args': (),
    },
    'cleanup-every-hour': {
        'task': 'tasks.cleanup_temp',
        'schedule': 3600.0,         # Every hour (seconds)
    },
    'weekly-digest': {
        'task': 'tasks.send_digest',
        'schedule': crontab(hour=8, minute=0, day_of_week=1),
    },
}

# Run worker: celery -A tasks worker --loglevel=info
# Run beat:   celery -A tasks beat --loglevel=info
```

### Systemd Timers
```ini
# /etc/systemd/user/myjob.timer
[Unit]
Description=Run myjob every hour

[Timer]
OnCalendar=*-*-* *:00:00
Persistent=true
RandomizedDelaySec=60

[Install]
WantedBy=timers.target
```

```ini
# /etc/systemd/user/myjob.service
[Unit]
Description=My scheduled job

[Service]
Type=oneshot
ExecStart=/usr/local/bin/python3 /opt/scripts/cleanup.py
WorkingDirectory=/opt/scripts
Environment=PYTHONUNBUFFERED=1
```

```bash
# Enable and start
systemctl --user enable myjob.timer
systemctl --user start myjob.timer
systemctl --user list-timers    # Check status
journalctl --user -u myjob      # Check logs
```

### Distributed Locking
```python
import redis

r = redis.Redis()

def run_with_lock(job_name, fn, timeout=300):
    lock = r.lock(f'job:{job_name}', timeout=timeout, blocking_timeout=5)
    if lock.acquire(blocking=False):
        try:
            fn()
        finally:
            lock.release()
    else:
        print(f'{job_name} already running, skipping')

# Prevent duplicate execution across workers
run_with_lock('daily-report', generate_report)
```

## Common Patterns

| Pattern | Use Case |
|---------|----------|
| **Cron schedule** | Simple recurring tasks |
| **Delayed job** | Execute after N seconds |
| **Priority queue** | Process urgent jobs first |
| **Rate limiting** | Prevent API overload |
| **Distributed lock** | Prevent duplicate execution |
| **Exponential backoff** | Smart retry on failure |
| **Job chaining** | Sequential pipeline |
| **Dead letter queue** | Handle permanently failed jobs |

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
