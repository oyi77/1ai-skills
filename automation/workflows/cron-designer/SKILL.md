---
name: cron-designer
description: Use when cron job scheduling for time-based automation. See parent skill for full docs.
domain: automation
tags:
- automation
- cron
- scheduling
version: 1.0.0
---

# Cron Designer

Design, implement, and operate time-based job scheduling in production systems. This skill covers cron expression authoring, common scheduling libraries, error handling, and monitoring patterns across Python, Node.js, and systemd environments.

## When to Use

Use this skill when scheduling recurring jobs, automating periodic maintenance, setting up data pipeline timers, or debugging a cron expression that doesn't fire when expected.


## Quick Start

### crontab.guru — The Cron Expression Builder

The fastest way to write or decode any cron expression is [crontab.guru](https://crontab.guru). Paste an expression, get a human-readable explanation instantly.

### Expression Anatomy

A cron expression has five fields separated by spaces:

```
┌───────── minute (0-59)
│ ┌──────── hour (0-23)
│ │ ┌─────── day of month (1-31)
│ │ │ ┌────── month (1-12)
│ │ │ │ ┌───── day of week (0-7, 0=Sun, 7=Sun)
│ │ │ │ │
* * * * *
```

Common special characters:

| Char | Meaning | Example |
|------|---------|---------|
| `*` | every | `* * * * *` = every minute |
| `*/N` | every N units | `*/15 * * * *` = every 15 minutes |
| `N,M` | list | `0,30 * * * *` = at :00 and :30 |
| `N-M` | range | `9-17 * * *` | every hour 9am-5pm|
| `L` | last (day-of-month only) | `0 0 L * *` = midnight last day of month |
| `#` | Nth weekday | `0 9 * * 1#1` = 9am first Monday of month |

### Quick Reference by Schedule

| Desired Schedule | Cron Expression |
|---|---|
| Every minute | `* * * * *` |
| Every 5 minutes | `*/5 * * * *` |
| Every hour at :00 | `0 * * * *` |
| Every 6 hours at :00 | `0 */6 * * *` |
| Daily at midnight | `0 0 * * *` |
| Daily at 9:30 AM | `30 9 * * *` |
| Monday–Friday 8am | `0 8 * * 1-5` |
| Weekdays hourly 9–5 | `0 9-17 * * 1-5` |
| First of month at noon | `0 12 1 * *` |
| Every Sunday at 6pm | `0 18 * * 0` |


## Code Examples

### Python — `schedule` Library

Lightweight, human-readable in-process scheduler.

```python
import schedule
import time
from datetime import datetime

def daily_report():
   print(f"[{datetime.now()}] Generating daily report...")
   # ... generate report ...

def health_check():
   print(f"[{datetime.now()}] Health check OK")

# Every minute (for testing)
schedule.every(1).minutes.do(health_check)

# Daily at 9:30 AM
schedule.every().day.at("09:30").do(daily_report)

# Every Monday at 8 AM
schedule.every().monday.at("08:00").do(daily_report)

# Every 30 minutes between 9-17 on weekdays
schedule.every(30).minutes.do(health_check)

while True:
   schedule.run_pending()
   time.sleep(1)
```

**Limitations:** The `schedule` library does **not** handle daylight saving time shifts, does **not** persist jobs across restarts, and uses the system clock directly — test edge cases around DST transitions.

### Node.js — `node-cron`

Native cron expression support in Node.js.

```javascript
const cron = require('node-cron');
const { backupDatabase } = require('./tasks');

// Every 15 minutes
cron.schedule('*/15 * * * *', () => {
  console.log('Running cleanup task...');
});

// Daily at midnight — backup database
cron.schedule('0 0 * * *', async () => {
  try {
    await backupDatabase();
    console.log('Database backup completed');
  } catch (err) {
    console.error('Backup failed:', err.message);
  }
});

// Weekdays at 9am — send digest
const task = cron.schedule('0 9 * * 1-5', () => {
  sendDigestEmail();
}, {
  scheduled: false  // manual start
});

task.start();   // start when ready
// task.stop(); // pause without losing the definition
```

### systemd Timers — The Production-Grade Scheduler

For system-level or container-level scheduling, systemd timers are superior to cron: they survive reboots, log to journald, and support monotonic (time-since-boot) schedules.

**Service unit** (`/etc/systemd/system/daily-cleanup.service`):

```ini
[Unit]
Description=Daily cleanup job

[Service]
Type=oneshot
ExecStart=/usr/local/bin/cleanup.sh
User=app
```

**Timer unit** (`/etc/systemd/system/daily-cleanup.timer`):

```ini
[Unit]
Description=Run daily cleanup at 3am

[Timer]
OnCalendar=daily
OnCalendar=*-*-* 03:00:00
Persistent=true          # catch up after boot
RandomizedDelaySec=300   # stagger 0-5min to avoid thundering herd

[Install]
WantedBy=timers.target
```

**Activation:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now daily-cleanup.timer
sudo systemctl list-timers --all
```

| systemd Calendar | Equivalent Cron |
|---|---|
| `hourly` | `0 * * * *` |
| `daily` | `0 0 * * *` |
| `weekly` | `0 0 * * 0` |
| `monthly` | `0 0 1 * *` |
| `Mon..Fri 09:00:00` | `0 9 * * 1-5` |


## Common Patterns

### Every N Minutes with Offset

```cron
# :05, :20, :35, :50  (every 15 minutes, offset 5)
5-59/15 * * * *

# :00, :30
*/30 * * * *

# :07, :37
7,37 * * * *
```

### Specific Times During Business Hours

```cron
# 8:00, 12:00, 17:00 weekdays only
0 8,12,17 * * 1-5

# Quarter-hourly during work hours
*/15 9-18 * * 1-5
```

### Day-of-Month + Day-of-Week Intersection

Cron treats day-of-month AND day-of-week as OR — a pattern runs if **either** matches. Use shell guard for AND behavior:

```cron
# Run at 8am but ONLY on the 1st AND it's a Monday
0 8 1 * *  [ "$(date +\%u)" = "1" ] || exit 0
```

### Run Once After Deploy (One-Shot)

```python
import os

SENTINEL = "/var/run/myapp/init-done.flag"

def run_once():
   if os.path.exists(SENTINEL):
       return
   # ... do initialization ...
   open(SENTINEL, "w").close()
```


## Error Handling

Every scheduled job is a potential silent failure. Apply these three layers:

### 1. Structured Logging

Log every run start, success, and failure with a consistent format:

```python
import logging

logger = logging.getLogger("scheduler")

def monitored_job(name: str):
   def decorator(func):
       def wrapper(*args, **kwargs):
           logger.info("job_start", extra={"job": name})
           try:
               result = func(*args, **kwargs)
               logger.info("job_success", extra={"job": name})
               return result
           except Exception as e:
               logger.error("job_failure", extra={"job": name, "error": str(e)})
               raise
       return wrapper
   return decorator

@monitored_job("daily-report")
def daily_report():
   ...
```

### 2. Retry with Backoff

```python
import time
from functools import wraps

def retry(max_attempts=3, delay=5):
   def decorator(func):
       @wraps(func)
       def wrapper(*args, **kwargs):
           for attempt in range(1, max_attempts + 1):
               try:
                   return func(*args, **kwargs)
               except Exception as e:
                   if attempt == max_attempts:
                       raise
                   logger.warning("retry", extra={"attempt": attempt, "error": str(e)})
                   time.sleep(delay * attempt)
           return None
       return wrapper
   return decorator
```

### 3. Notification on Failure

When a critical job fails after all retries, alert the team:

```python
import requests

def notify_failure(job_name: str, error: str):
   webhook_url = os.getenv("SLACK_WEBHOOK_URL")
   if not webhook_url:
       return
   requests.post(webhook_url, json={
       "text": f"⏰ Cron job *{job_name}* failed: `{error}`",
   })
```


## Workflow

Follow this four-step workflow for every new cron job:

### Step 1 — Define the Schedule

1. Write the cron expression using [crontab.guru](https://crontab.guru)
2. Decide: in-process scheduler (`schedule`/`node-cron`) or system-level (systemd timer, classic crontab)
3. For systemd: use `OnCalendar=` with a named alias (`daily`, `hourly`) when possible

### Step 2 — Implement the Job

1. Write the job as a standalone function — no side effects outside its body
2. Wrap with monitoring decorator (logging + retry)
3. Add a `run_if` guard for conditional execution
4. Test manually: `python -c "from jobs import my_task; my_task()"`

### Step 3 — Deploy

1. Add the cron config to your deployment package
2. For systemd timers: commit `.service` + `.timer` units to your repo, deploy via Ansible/Chef/symlink
3. For in-process: start/restart the application after config change
4. Verify: check the first execution in logs

### Step 4 — Monitor

1. Confirm the job runs at the expected time (first 3 executions)
2. Set up log aggregation — each job should emit a unique log tag
3. Add a dead-man's-switch: if the job doesn't report success for N hours, alert
4. For critical jobs: instrument with metrics (Prometheus gauge `last_success_timestamp`)


## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll remember the cron syntax, no need to look it up" | You won't. Always verify with crontab.guru before deploying. |
| "My job only runs once a day, I don't need monitoring" | One missed run can corrupt data for 24h. Every job needs monitoring. |
| "Five fields is enough, I never need seconds" | `node-cron` and Quartz support sixth-field seconds — but standard cron on Linux does NOT. Stick to five fields for portability. |
| "systemd timers are too complex, I'll just use crontab" | systemd timers are the recommended replacement: journald logs, dependency ordering, monotonic schedules, and no environment surprises. |
| "A silent try/except is fine for a cleanup job" | Swallowed exceptions turn recoverable failures into permanent data loss. Always log and alert. |
| "DST is a one-hour problem, I'll deal with it later" | DST causes jobs to skip or double-fire. `schedule` doesn't handle it — use UTC-based scheduling or systemd timers. |
| "I can test cron with `sleep 30` inside the job" | `sleep` blocks the scheduler thread. Use a side-effect-free test that logs and returns immediately. |


## Verification

Before deploying a new cron job, verify:

- [ ] Expression is valid on crontab.guru and matches the expected schedule
- [ ] Job runs correctly when called directly (outside of cron)
- [ ] Timezone is correct — prefer UTC for server jobs
- [ ] DST transition is safe (jobs at 2-3am on DST days)
- [ ] Failure path is tested: trigger the error condition, confirm retry + notification
- [ ] Log output contains a unique tag for grep/filtering
- [ ] systemd timer: `systemctl list-timers` shows the timer as active
- [ ] In-process: scheduler process is supervised (systemd, PM2, Docker restart policy)
- [ ] Dead-man's-switch or metric exists for production jobs
- [ ] Rollback plan: disable the cron line or stop the timer, confirm it does NOT run
