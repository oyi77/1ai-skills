---
name: multi-channel-reminder
description: 'Skill: multi-channel-reminder. See SKILL.md body for details. Use when this domain is relevant.'
domain: operations
author: oyi77
license: Apache-2.0
subdomain: business-operations
tags:
- business-ops
- channel
- management
- multi
- operations
- reminder
version: 1.0.0
---
# Multi-Channel Reminder & Notification System

> Design, build, and operate a reliable multi-channel notification system that delivers reminders across email, SMS, Slack, Telegram, Discord, WhatsApp, and push notifications. Handles scheduling, templating, deduplication, delivery tracking, and failure recovery.

---

## Overview

A multi-channel reminder system delivers time-sensitive notifications across multiple communication channels to maximize delivery probability. Core concerns:

1. **Channel diversity** — Each channel has different reliability, cost, latency, and formatting characteristics
2. **Scheduling** — Cron expressions, timezone-aware scheduling, recurring vs one-shot, escalation sequences
3. **Templating** — Dynamic content generation with Jinja2/Nunjucks, localization, HTML vs plaintext
4. **Delivery guarantees** — Queue-backed delivery with retry, dead letter queues, deduplication
5. **Status tracking** — Delivery receipts, read receipts, failure analytics

This skill covers end-to-end design from channel integration to production operations.

---

## When to Use

- Building any system that needs to notify users at specific times or intervals
- Appointment booking systems (doctor, salon, service) requiring reminder sequences
  - 24h before, 2h before, 15min before
- Deadline management (contract renewals, subscription expirations, payment due dates)
- System monitoring alerts needing redundant delivery (email + Slack + SMS)
- Daily/weekly digest generation (reports, activity summaries)
- Billing and invoice notifications (receipts, overdue escalations)

## When NOT to Use

- Real-time streaming events requiring sub-second delivery (use WebSocket/SSE or a message broker directly)
- One-shot notifications where email alone suffices (adding channels = unnecessary complexity)
- Systems under 100 notifications/day where a simple cron + curl is adequate
- Regulatory-required communications where you need an audit trail provider (use SendGrid/Mailgun delivery APIs)

---

## Architecture

```
                    ┌──────────────────┐
                    │  Schedule Engine  │
                    │  (cron / APS)     │
                    └────────┬─────────┘
                             │ due events
                             ▼
                    ┌──────────────────┐
                    │   Task Queue     │
                    │ (Redis / BullMQ) │
                    └────────┬─────────┘
                             │ dequeue
                             ▼
                    ┌──────────────────┐
                    │ Notification     │
                    │  Dispatcher      │
                    └───┬───┬───┬──────┘
                        │   │   │
           ┌────────────┘   │   └──────────────┐
           ▼                ▼                  ▼
     ┌──────────┐    ┌──────────┐     ┌──────────────┐
     │ Priority │    │  Batch   │     │  Escalation  │
     │ Channel  │    │ Channel  │     │  Sequence    │
     └──────────┘    └──────────┘     └──────┬───────┘
                                             │
        ┌──────┬──────┬──────┬──────┬──────┐ │
        ▼      ▼      ▼      ▼      ▼      ▼▼
     ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐
     │SMTP│ │SMS │ │SLK │ │TG  │ │DSC │ │WHA │
     └────┘ └────┘ └────┘ └────┘ └────┘ └────┘
```

---

## Channel Integrations

### Email (SMTP / SendGrid / Mailgun)

Three delivery tiers:

| Tier | Provider | Use Case | Cost |
|------|----------|----------|------|
| Self-hosted SMTP | Postfix, Exim | Dev/test, low volume | Free |
| Transactional API | SendGrid, Mailgun, SES | Production, moderate volume | ~$15-80/mo |
| Enterprise | SendGrid Pro, AWS SES | High volume, dedicated IP | ~$90+/mo |

**Python (smtplib with SendGrid):**

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email_smtp(to: str, subject: str, html: str, text: str) -> dict:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"Reminder System <{os.environ['SMTP_FROM']}>"
    msg["To"] = to
    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(
        os.environ["SMTP_HOST"],
        int(os.environ.get("SMTP_PORT", 587)),
    ) as server:
        server.starttls()
        server.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"])
        server.send_message(msg)

    return {"channel": "email", "to": to, "status": "sent", "subject": subject}
```

**JavaScript (nodemailer):**

```javascript
import nodemailer from "nodemailer";

const transporter = nodemailer.createTransport({
  host: process.env.SMTP_HOST,
  port: parseInt(process.env.SMTP_PORT || "587"),
  secure: false,
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS,
  },
});

export async function sendEmail(to, subject, html, text) {
  const info = await transporter.sendMail({
    from: `"Reminder" <${process.env.SMTP_FROM}>`,
    to,
    subject,
    text,
    html,
  });
  return { channel: "email", to, messageId: info.messageId, status: "sent" };
}
```

**SendGrid API (Python):**

```python
import requests

def send_email_sendgrid(to: str, subject: str, html: str, text: str) -> dict:
    resp = requests.post(
        "https://api.sendgrid.com/v3/mail/send",
        headers={
            "Authorization": f"Bearer {os.environ['SENDGRID_API_KEY']}",
            "Content-Type": "application/json",
        },
        json={
            "personalizations": [{"to": [{"email": to}]}],
            "from": {"email": os.environ["SMTP_FROM"]},
            "subject": subject,
            "content": [
                {"type": "text/plain", "value": text},
                {"type": "text/html", "value": html},
            ],
        },
    )
    resp.raise_for_status()
    return {"channel": "email", "to": to, "status": "sent"}
```

**Bash (curl via Mailgun):**

```bash
curl -s --user "api:$MAILGUN_API_KEY" \
  "https://api.mailgun.net/v3/$MAILGUN_DOMAIN/messages" \
  -F from="Reminder <$SMTP_FROM>" \
  -F to="$TO_EMAIL" \
  -F subject="$SUBJECT" \
  -F text="$TEXT_BODY" \
  -F html="$HTML_BODY"
```

### SMS (Twilio)

**Python:**

```python
from twilio.rest import Client

client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])

def send_sms(to: str, body: str) -> dict:
    msg = client.messages.create(
        body=body,
        from_=os.environ["TWILIO_PHONE_NUMBER"],
        to=_normalize_phone(to),
    )
    return {
        "channel": "sms",
        "to": to,
        "sid": msg.sid,
        "status": msg.status,
        "cost": f"${msg.price}" if msg.price else "pending",
    }

def _normalize_phone(number: str) -> str:
    """Ensure E.164 format: +<country><number>."""
    number = number.strip()
    if not number.startswith("+"):
        # Assume local number — prepend default country code
        number = os.environ.get("DEFAULT_COUNTRY_CODE", "+1") + number.lstrip("0")
    return number
```

### Slack Webhooks

**Python (slack-sdk):**

```python
from slack_sdk import WebhookClient

def send_slack(webhook_url: str, text: str, blocks: list | None = None) -> dict:
    client = WebhookClient(webhook_url)
    payload = {"text": text}
    if blocks:
        payload["blocks"] = blocks
    resp = client.send(**payload)
    return {
        "channel": "slack",
        "status": "sent" if resp.status_code == 200 else "error",
        "status_code": resp.status_code,
    }
```

**Bash (curl):**

```bash
curl -X POST -H "Content-type: application/json" \
  --data '{"text":"Reminder: Meeting in 15 minutes"}' \
  "$SLACK_WEBHOOK_URL"
```

### Telegram Bot

**Python (python-telegram-bot):**

```python
import asyncio
from telegram import Bot

bot = Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])

async def send_telegram(chat_id: str | int, text: str, parse_mode: str = "HTML") -> dict:
    msg = await bot.send_message(
        chat_id=int(chat_id) if isinstance(chat_id, str) else chat_id,
        text=text,
        parse_mode=parse_mode,
        disable_web_page_preview=True,
    )
    return {
        "channel": "telegram",
        "chat_id": str(chat_id),
        "message_id": msg.message_id,
        "status": "sent",
    }

# Synchronous wrapper for cron jobs
def send_telegram_sync(chat_id: str | int, text: str) -> dict:
    return asyncio.run(send_telegram(chat_id, text))
```

### Discord Webhooks

**Python (requests):**

```python
import requests

def send_discord(webhook_url: str, content: str, username: str = "Reminder") -> dict:
    resp = requests.post(
        webhook_url,
        json={"content": content, "username": username},
        timeout=10,
    )
    resp.raise_for_status()
    return {"channel": "discord", "status": "sent"}
```

### WhatsApp Business API

**Python (requests via Meta Graph API):**

```python
def send_whatsapp(to: str, template_name: str, params: dict) -> dict:
    """Send a pre-approved WhatsApp template message."""
    resp = requests.post(
        f"https://graph.facebook.com/v18.0/{os.environ['WHATSAPP_PHONE_ID']}/messages",
        headers={"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"},
        json={
            "messaging_product": "whatsapp",
            "to": _normalize_phone(to),
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": params.get("locale", "en")},
                "components": [{
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": str(v)}
                        for v in params.get("variables", [])
                    ],
                }],
            },
        },
    )
    return {
        "channel": "whatsapp",
        "to": to,
        "status": "sent" if resp.ok else "error",
        "response": resp.json() if resp.ok else resp.text,
    }
```

### Push Notifications (FCM / APNs)

**Python (firebase-admin):**

```python
import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate(os.environ["FCM_SERVICE_ACCOUNT_PATH"])
firebase_admin.initialize_app(cred)

def send_push(device_token: str, title: str, body: str, data: dict | None = None) -> dict:
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        data=data or {},
        token=device_token,
    )
    response = messaging.send(message)
    return {"channel": "fcm", "token": device_token[:16] + "...", "message_id": response}
```

---

## Scheduling Patterns

### Cron Expressions (Standard)

```
# ┌───────── minute (0-59)
# │ ┌───────── hour (0-23)
# │ │ ┌───────── day of month (1-31)
# │ │ │ ┌───────── month (1-12)
# │ │ │ │ ┌───────── day of week (0-6, 0=Sun)
# │ │ │ │ │
# * * * * *
```

**Common patterns:**

```
0 9 * * 1-5      # Weekdays at 9:00 AM (daily standup reminder)
0 8 1 * *        # 1st of month at 8 AM (invoice reminder)
*/15 * * * *     # Every 15 minutes (health check alert)
0 0 * * 0        # Sunday midnight (weekly digest)
0 6,18 * * *     # Twice daily at 6 AM and 6 PM (medication reminder)
30 9 * * 1-6     # 9:30 AM Mon-Sat (appointment day reminder)
```

### Timezone Handling

Store all schedules in UTC. Convert to user timezone at display time. Handle DST by using IANA timezone names (not UTC offsets).

```python
from datetime import datetime, timezone
import zoneinfo

def schedule_time_str(user_tz: str, hour: int, minute: int) -> str:
    """Return cron time in UTC for a user's local desired time."""
    tz = zoneinfo.ZoneInfo(user_tz)
    now_utc = datetime.now(timezone.utc)
    # Target today at local hour:minute
    local_dt = now_utc.astimezone(tz).replace(hour=hour, minute=minute, second=0, microsecond=0)
    utc_dt = local_dt.astimezone(timezone.utc)
    return f"{utc_dt.minute} {utc_dt.hour} * * *"
```

### Reminder Escalation Sequences

```python
# Escalation stages with time offsets
ESCALATION_STAGES = [
    {"name": "first_notice",  "offset": timedelta(hours=-48), "urgency": "normal"},
    {"name": "second_notice", "offset": timedelta(hours=-24), "urgency": "normal"},
    {"name": "one_day_before", "offset": timedelta(hours=-24), "urgency": "medium"},
    {"name": "due",            "offset": timedelta(),          "urgency": "high"},
    {"name": "overdue_6h",    "offset": timedelta(hours=6),   "urgency": "high"},
    {"name": "overdue_24h",   "offset": timedelta(hours=24),  "urgency": "urgent"},
]

def compute_escalations(event: dict) -> list[dict]:
    """Generate all reminder events for a deadline."""
    deadline = event["deadline"]
    reminders = []
    for stage in ESCALATION_STAGES:
        remind_at = deadline + stage["offset"]
        reminders.append({
            "remind_at": remind_at,
            "type": stage["name"],
            "urgency": stage["urgency"],
            "event_id": event["id"],
        })
    return [r for r in reminders if r["remind_at"] >= datetime.now(timezone.utc)]
```

### Recurring vs One-Shot

```python
from enum import Enum
import uuid

class ScheduleType(Enum):
    ONE_SHOT = "one_shot"
    RECURRING = "recurring"
    RECURRING_WITH_END = "recurring_with_end"

class ReminderSchedule:
    def __init__(
        self,
        cron_expr: str,
        schedule_type: ScheduleType,
        channels: list[str],
        recipient: dict,
        template_name: str,
        template_data: dict,
        tz: str = "UTC",
        end_at: datetime | None = None,
    ):
        self.id = uuid.uuid4().hex[:12]
        self.cron = cron_expr
        self.type = schedule_type
        self.channels = channels
        self.recipient = recipient
        self.template = template_name
        self.data = template_data
        self.tz = tz
        self.end_at = end_at
        self.last_fired: datetime | None = None
```

---

## Template Systems

### Jinja2 (Python)

```python
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader("templates/"),
    autoescape=select_autoescape(["html", "xml"]),
)

def render_notification(template_name: str, data: dict, locale: str = "en") -> dict:
    """Render subject, text body, HTML body from template files."""
    env.globals["locale"] = locale
    subject = env.get_template(f"{template_name}/{locale}/subject.j2").render(**data)
    text    = env.get_template(f"{template_name}/{locale}/body.txt.j2").render(**data)
    html    = env.get_template(f"{template_name}/{locale}/body.html.j2").render(**data)
    return {"subject": subject.strip(), "text": text.strip(), "html": html.strip()}
```

**Template structure:**

```
templates/
└── appointment-reminder/
    ├── en/
    │   ├── subject.j2          # "Reminder: {{ title }} tomorrow at {{ time }}"
    │   ├── body.txt.j2         # Plain text version
    │   └── body.html.j2        # HTML version with styling
    ├── id/
    │   ├── subject.j2          # "Pengingat: {{ title }} besok jam {{ time }}"
    │   ├── body.txt.j2
    │   └── body.html.j2
    └── zh/
        └── ...
```

**Example template (body.html.j2):**

```html
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: sans-serif; max-width: 600px; margin: auto; padding: 20px;">
  <div style="background: #f8f9fa; border-radius: 8px; padding: 24px;">
    <h2 style="color: {{ 'red' if urgency == 'urgent' else '#333' }};">
      {% if urgency == 'normal' %}🔔{% elif urgency == 'high' %}⚠️{% else %}🚨{% endif %}
      {{ title }}
    </h2>
    <p>Hi {{ recipient_name }},</p>
    <p>{{ body_text }}</p>
    {% if action_url %}
    <a href="{{ action_url }}"
       style="display: inline-block; background: #007bff; color: white;
              padding: 10px 20px; text-decoration: none; border-radius: 4px;">
      {{ action_label or 'View Details' }}
    </a>
    {% endif %}
    <hr style="margin-top: 24px;">
    <p style="color: #666; font-size: 12px;">
      Sent {{ sent_at }} | <a href="{{ unsubscribe_url }}">Unsubscribe</a>
    </p>
  </div>
</body>
</html>
```

### Nunjucks (JavaScript)

```javascript
import nunjucks from "nunjucks";

nunjucks.configure("templates", { autoescape: true });

export function renderNotification(templateName, data, locale = "en") {
  const subject = nunjucks.render(`${templateName}/${locale}/subject.njk`, data);
  const text = nunjucks.render(`${templateName}/${locale}/body.txt.njk`, data);
  const html = nunjucks.render(`${templateName}/${locale}/body.html.njk`, data);
  return { subject: subject.trim(), text: text.trim(), html: html.trim() };
}
```

---

## Deduplication

Prevent double-sending when the same event fires multiple triggers (e.g., a row updated and a cron job both trigger for the same deadline).

### Idempotency Key Pattern

```python
import redis
import hashlib
import json

r = redis.Redis.from_url(os.environ["REDIS_URL"])

def already_sent(event_id: str, channel: str, stage: str, ttl: int = 86400) -> bool:
    """Check and mark a notification as sent. Returns True if already sent."""
    key = f"sent:{event_id}:{channel}:{stage}"
    if r.get(key):
        return True
    r.setex(key, ttl, "1")
    return False

def dispatch_dedup(event: dict, channel_fn, channel: str):
    """Dispatch a notification only if not already sent."""
    if already_sent(event["id"], channel, event.get("stage", "default")):
        return {"status": "duplicate", "event_id": event["id"], "channel": channel}
    result = channel_fn(event)
    return result
```

### Concurrent Trigger Guard

When cron + webhook + manual trigger fire near-simultaneously, use Redis locks:

```python
def dispatch_with_lock(event_id: str, lock_ttl: int = 60):
    lock_key = f"lock:dispatch:{event_id}"
    lock = r.lock(lock_key, timeout=lock_ttl)
    if not lock.acquire(blocking=False):
        return {"status": "locked", "event_id": event_id}
    try:
        # ... dispatch logic ...
        pass
    finally:
        lock.release()
```

---

## Delivery Tracking & Retry

### Status Model

```python
from enum import Enum

class DeliveryStatus(Enum):
    PENDING = "pending"
    QUEUED = "queued"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"
    BOUNCED = "bounced"
    DLQ = "dead_letter"

# Delivery record schema
DELIVERY_RECORD = {
    "notification_id": "uuid",
    "channel": "email | sms | slack | telegram | discord | whatsapp | push",
    "recipient": "user@example.com",
    "status": DeliveryStatus,
    "attempts": 0,
    "max_attempts": 5,
    "last_error": None,
    "queued_at": "datetime_utc",
    "sent_at": None,
    "delivered_at": None,
    "read_at": None,
    "metadata": {},
}
```

### Exponential Backoff Retry

```python
import time
import logging

logger = logging.getLogger(__name__)

def retry_with_backoff(fn, max_attempts: int = 5, base_delay: float = 2.0) -> dict:
    """Call fn() with exponential backoff. Raises on final failure."""
    last_error = None
    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except Exception as e:
            last_error = e
            if attempt < max_attempts:
                delay = base_delay * (2 ** (attempt - 1))
                jitter = delay * 0.1 * (time.time() % 1)  # 10% jitter
                logger.warning("Attempt %d/%d failed: %s. Retrying in %.1fs",
                               attempt, max_attempts, e, delay + jitter)
                time.sleep(delay + jitter)
    raise last_error

# Usage
def send_with_retry(channel_fn, payload: dict) -> dict:
    try:
        result = retry_with_backoff(lambda: channel_fn(payload))
        result["attempts"] = result.get("attempts", 1)
        return result
    except Exception as e:
        return {
            "status": DeliveryStatus.DLQ,
            "error": str(e),
            "channel": payload.get("channel", "unknown"),
        }
```

### Delivery Receipts

```python
def track_delivery(notification_id: str, channel: str, status: DeliveryStatus, metadata: dict = None):
    """Write delivery status to database or Redis."""
    record = {
        "notification_id": notification_id,
        "channel": channel,
        "status": status.value,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metadata": metadata or {},
    }
    # PostgreSQL
    # INSERT INTO delivery_log (notification_id, channel, status, metadata)
    # VALUES (...)
    # Redis as hash
    r.hset(f"delivery:{notification_id}", channel, json.dumps(record, default=str))
    return record
```

---

## Queue Pattern (Redis / BullMQ)

### Redis Queue (Simple Python)

```python
import json

def enqueue_notification(schedule: ReminderSchedule, event: dict):
    """Push notification job to Redis list."""
    job = {
        "schedule_id": schedule.id,
        "event_id": event.get("id"),
        "channels": schedule.channels,
        "recipient": schedule.recipient,
        "template": schedule.template,
        "data": schedule.data,
        "enqueued_at": datetime.now(timezone.utc).isoformat(),
        "retries": 0,
        "max_retries": 5,
    }
    r.lpush("notification:queue", json.dumps(job, default=str))
    return job

def worker_loop():
    """Blocking consumer."""
    while True:
        _, data = r.brpop("notification:queue", timeout=30)
        job = json.loads(data)
        process_job(job)
```

### BullMQ (Node.js)

```javascript
import { Queue, Worker, QueueScheduler } from "bullmq";
import IORedis from "ioredis";

const connection = new IORedis(process.env.REDIS_URL);
const notificationQueue = new Queue("notifications", { connection });

// Enqueue
async function enqueue(jobData) {
  return await notificationQueue.add("send", jobData, {
    attempts: 5,
    backoff: { type: "exponential", delay: 2000 },
    removeOnComplete: { age: 3600 * 24 * 7 },  // keep 7 days
    removeOnFail: { age: 3600 * 24 * 30 },      // keep 30 days for DLQ
  });
}

// Worker
const worker = new Worker(
  "notifications",
  async (job) => {
    const { channels, recipient, template, data } = job.data;
    for (const channel of channels) {
      const fn = channelHandlers[channel];
      if (fn) await fn(recipient, template, data);
    }
  },
  { connection, concurrency: 5 }
);

worker.on("failed", (job, err) => {
  console.error(`Job ${job.id} failed after ${job.attemptsMade} attempts:`, err);
});
```

### Dead Letter Queue

```python
def move_to_dlq(job: dict, error: str):
    """Move a failed job to the dead letter queue for manual inspection."""
    dlq_entry = {
        **job,
        "failed_at": datetime.now(timezone.utc).isoformat(),
        "error": error,
    }
    r.lpush("notification:dlq", json.dumps(dlq_entry, default=str))

def process_dlq():
    """Inspect and retry DLQ items."""
    dlq_items = r.lrange("notification:dlq", 0, -1)
    for item_json in dlq_items:
        item = json.loads(item_json)
        print(f"DLQ: {item['schedule_id']} - {item['error']}")
        # Optionally re-enqueue:
        # if manual_approval(item):
        #     r.enqueue(...)
```

---

## Common Patterns

### Appointment Reminders

```python
def schedule_appointment_reminders(appointment: dict):
    """Schedule 3-tier reminders for an appointment."""
    start = appointment["start_time"]
    stages = [
        {"name": "24h_before", "offset": timedelta(hours=-24),  "urgency": "normal"},
        {"name": "2h_before",  "offset": timedelta(hours=-2),   "urgency": "medium"},
        {"name": "15min",      "offset": timedelta(minutes=-15), "urgency": "high"},
    ]
    reminders = []
    for stage in stages:
        remind_at = start + stage["offset"]
        reminders.append({
            "id": f"apt:{appointment['id']}:{stage['name']}",
            "remind_at": remind_at,
            "channels": ["sms", "email"] if stage["urgency"] == "high" else ["email"],
            "template": "appointment-reminder",
            "data": {
                "title": appointment["title"],
                "time": remind_at.strftime("%H:%M"),
                "location": appointment.get("location", "TBD"),
                "urgency": stage["urgency"],
                "recipient_name": appointment["patient_name"],
                "action_url": appointment.get("cancel_url"),
            },
            "recipient": {"email": appointment["email"], "phone": appointment["phone"]},
        })
    return reminders
```

### Deadline Escalations

```python
def render_deadline_alert(event: dict, stage: str) -> str:
    subjects = {
        "upcoming": "Reminder: {title} is due in {days} day(s)",
        "due_today": "DUE TODAY: {title}",
        "overdue_24h": "OVERDUE: {title} was due yesterday",
        "overdue_3d": "URGENT: {title} is {days} days overdue",
    }
    return subjects.get(stage, "Reminder: {title}").format(**event)

ESCALATION_CHANNELS = {
    "upcoming":    ["email"],
    "due_today":   ["email", "slack"],
    "overdue_24h": ["email", "slack", "sms"],
    "overdue_3d":  ["email", "slack", "sms", "telegram"],
}
```

### Billing Alerts

```python
BILLING_ALERTS = {
    "invoice_generated": {
        "channels": ["email"],
        "priority": "normal",
    },
    "payment_due_3d": {
        "channels": ["email", "sms"],
        "priority": "normal",
    },
    "payment_due_today": {
        "channels": ["email", "sms", "telegram"],
        "priority": "high",
    },
    "payment_failed": {
        "channels": ["email", "sms", "telegram", "slack"],
        "priority": "high",
    },
    "payment_overdue_7d": {
        "channels": ["email", "sms", "telegram", "whatsapp"],
        "priority": "urgent",
    },
}
```

### System Monitoring Alerts

```python
def system_alert_channel(severity: str) -> list[str]:
    mapping = {
        "critical": ["pagerduty", "sms", "slack", "email"],
        "warning":  ["slack", "email"],
        "info":     ["slack"],
    }
    return mapping.get(severity, ["email"])

def send_monitoring_alert(alert: dict):
    channels = system_alert_channel(alert["severity"])
    for ch in channels:
        payload = {
            "channel": ch,
            "recipient": alert.get(f"{ch}_target") or os.environ.get(f"ALERT_{ch.upper()}_URL"),
            "template": "system-alert",
            "data": alert,
        }
        enqueue_notification(payload)
```

### Daily / Weekly Digest

```python
def generate_digest(user_id: str, period: str = "daily") -> dict:
    """Aggregate notifications and send as a single digest."""
    items = fetch_pending_items(user_id, period)
    if not items:
        return {"status": "no_items", "user": user_id}
    digest = {
        "id": uuid.uuid4().hex,
        "type": f"{period}_digest",
        "recipient": {"email": items[0]["email"]},
        "channels": ["email"],
        "template": f"{period}-digest",
        "data": {
            "period": period,
            "count": len(items),
            "items": items,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
    }
    return digest
```

---

## Unified Dispatcher

```python
CHANNEL_REGISTRY = {
    "email":    send_email_smtp,
    "sendgrid": send_email_sendgrid,
    "sms":      send_sms,
    "slack":    send_slack,
    "telegram": send_telegram_sync,
    "discord":  send_discord,
    "whatsapp": send_whatsapp,
    "fcm":      send_push,
}

def dispatch(notification: dict) -> list[dict]:
    """Send a notification across all configured channels with dedup and retry."""
    results = []
    for channel in notification.get("channels", []):
        fn = CHANNEL_REGISTRY.get(channel)
        if not fn:
            results.append({"channel": channel, "status": "error", "error": "unknown_channel"})
            continue
        event_id = notification.get("event_id", notification.get("id"))
        stage = notification.get("stage", "default")
        if already_sent(event_id, channel, stage):
            results.append({"channel": channel, "status": "duplicate"})
            continue
        result = send_with_retry(lambda: fn(notification))
        results.append(result)
        track_delivery(event_id, channel, result.get("status", DeliveryStatus.SENT))
    return results
```

---

## Red Flags

| Issue | Risk | Mitigation |
|-------|------|------------|
| Phone numbers without country codes | SMS delivery failure | Normalize to E.164 on input; reject non-compliant numbers |
| Missing SPF/DKIM/DMARC | Email lands in spam | Configure DNS records before first send; test with mail-tester.com |
| Twilio/API rate limits (1 msg/segment per second) | Throttled or dropped | Implement rate limiter per channel; stagger sends |
| SMS costs at scale ($0.0079/msg US = $7.90/1000) | Budget overrun | Prefer email for non-urgent; budget alerts at 80% spend |
| Timezone confusion (DST transitions, non-existent times) | Wrong time or missed alarm | IANA tz database; validate cron with `validate_cron()` |
| API keys in source code | Credential leak | Env vars only; commit-hook scanning with gitleaks |
| Channel provider outages | Silent failures | Fallback channel chain; health check each provider |
| Unsubscribe compliance (CAN-SPAM, GDPR) | Legal liability | Unsubscribe link in every email; opt-out tracking |
| WhatsApp template approval delays | Cannot send | Submit templates weeks in advance; maintain fallback channel |
| FCM/APNs token expiration | Silent push failure | Track token last-used; deactivate stale tokens |

---

## Verification Checklist

- [ ] Each channel tested independently with real credentials
- [ ] Email deliverability verified: SPF, DKIM, DMARC passing (check via MXToolbox)
- [ ] SMS numbers in E.164 format, international prefix confirmed per recipient country
- [ ] Slack/Discord webhook URLs tested with POST and verified in channel
- [ ] Telegram bot added to group/channel, chat_id confirmed
- [ ] WhatsApp template approved by Meta, parameter order matches template
- [ ] FCM/APNs token tested with real device, handled expired token gracefully
- [ ] Cron expressions validated for all timezones in use (test DST boundary)
- [ ] Deduplication tested: same event fired twice within TTL produces one notification
- [ ] Concurrent trigger guard tested: 3 simultaneous API calls produce one notification
- [ ] Retry logic tested: invalid credentials error handled, backoff delay observed
- [ ] Dead letter queue populated on final failure, inspectable via admin tool
- [ ] Escalation sequence fires at correct intervals with correct channel expansion
- [ ] Template renders correctly: subject line length (email: <78 chars), HTML email renders on mobile
- [ ] Logging captures every dispatch, delivery receipt, and failure event
- [ ] Rate limits documented per channel: Twilio (1/sec), SendGrid (100/sec), Slack (1/sec per webhook)
- [ ] Unsubscribe mechanism exists in every email (List-Unsubscribe header + link)
- [ ] Rollback plan: emergency disable all notifications, stop workers, drain queue
- [ ] Monitoring: alerts fire when delivery failure rate exceeds threshold (e.g., >5%)

---

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Email is enough, no one needs SMS" | Email has 20%+ deliverability problem (spam, bounce). SMS delivers in seconds at 99%+. Use both. |
| "We'll send everything through every channel" | Every channel costs money and attention. Over-notification trains users to ignore. Prioritize channels. |
| "Just use a cron job" | Cron is fire-and-forget with no retry, no tracking, no dedup. You need a queue. |
| "FCM is free, use it for everything" | Push tokens expire, users opt out, iOS/Android differences matter. Never single-channel. |
| "Exponential backoff is over-engineering" | Without backoff, a transient provider outage triggers thundering-herd failures on every notification. |
| "Deduplication isn't needed for a simple system" | Double charging a customer because webhook + cron fired for the same invoice is expensive. |
| "We need delivery receipts for every channel" | Only email and WhatsApp provide meaningful delivery receipts. SMS delivery receipts cost extra. |
| "HTML email is prettier" | Plaintext has higher spam delivery rate. Send multipart/alternative always. |
| "Timezone handling can be an afterthought" | A "9 AM" reminder in UTC fires at 4 AM EST and 7 PM WIB. Destroys trust. |
| "WhatsApp API is the best option" | WhatsApp requires pre-approved templates, 24h conversation window, and Meta approval. Build it last. |

---

## Process

### Phase 1: Foundation
1. Identify notification events and their timing requirements
2. Design channels per event type based on urgency, cost, and user preference
3. Set up Redis/queue infrastructure
4. Implement channel adapters one at a time, testing each independently

### Phase 2: Scheduling & Templating
5. Configure schedule engine with appropriate cron expressions
6. Build template directory with Jinja2/Nunjucks
7. Implement timezone logic: store UTC, convert at render time
8. Write escalation sequences for time-critical events

### Phase 3: Reliability
9. Add idempotency keys and deduplication
10. Implement retry with exponential backoff
11. Set up dead letter queue with admin inspection
12. Add delivery tracking (attempt count, status transitions)

### Phase 4: Production
13. Configure monitoring: delivery success rate, queue depth, DLQ count
14. Set up email deliverability: SPF, DKIM, DMARC
15. Add rate limiters per channel
16. Deploy workers with concurrency control
17. Write rollback procedure and emergency stop

---

## Example: Complete Reminder Scheduler

```python
#!/usr/bin/env python3
"""appointment_reminder.py — Full example tying scheduling, dispatch, and retry together."""

import os
import json
import time
import logging
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass, field, asdict
from typing import Optional
import uuid

import redis
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

r = redis.Redis.from_url(os.environ.get("REDIS_URL", "redis://localhost:6379/0"))


@dataclass
class Appointment:
    id: str
    patient_name: str
    email: str
    phone: str
    start_time: datetime
    title: str
    location: str = ""


def normalize_phone(number: str) -> str:
    number = number.strip()
    if not number.startswith("+"):
        number = os.environ.get("DEFAULT_COUNTRY_CODE", "+1") + number.lstrip("0")
    return number


def already_sent(key: str, ttl: int = 86400) -> bool:
    if r.get(key):
        return True
    r.setex(key, ttl, "1")
    return False


def send_email(payload: dict) -> dict:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = payload["subject"]
    msg["From"] = os.environ["SMTP_FROM"]
    msg["To"] = payload["to"]
    msg.attach(MIMEText(payload["text"], "plain"))
    msg.attach(MIMEText(payload["html"], "html"))
    with smtplib.SMTP(os.environ["SMTP_HOST"], int(os.environ.get("SMTP_PORT", 587))) as s:
        s.starttls()
        s.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"])
        s.send_message(msg)
    return {"status": "sent", "channel": "email"}


def send_sms(payload: dict) -> dict:
    resp = requests.post(
        f"https://api.twilio.com/2010-04-01/Accounts/{os.environ['TWILIO_ACCOUNT_SID']}/Messages.json",
        auth=(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"]),
        data={"Body": payload["text"], "From": os.environ["TWILIO_PHONE_NUMBER"], "To": normalize_phone(payload["to"])},
        timeout=10,
    )
    resp.raise_for_status()
    return {"status": "sent", "channel": "sms", "sid": resp.json().get("sid")}


def apply_backoff(fn, max_attempts: int = 5, base_delay: float = 2.0):
    """Execute fn with exponential backoff."""
    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except Exception as e:
            logger.warning("Attempt %d/%d failed: %s", attempt, max_attempts, e)
            if attempt == max_attempts:
                raise
            delay = base_delay * (2 ** (attempt - 1)) * (0.9 + 0.2 * (time.time() % 1))
            time.sleep(delay)


def schedule_reminders(appointment: Appointment) -> list[dict]:
    stages = [
        ("24h", timedelta(hours=-24), ["email"]),
        ("2h", timedelta(hours=-2), ["email", "sms"]),
        ("15min", timedelta(minutes=-15), ["email", "sms"]),
    ]
    jobs = []
    for name, offset, channels in stages:
        remind_at = appointment.start_time + offset
        if remind_at <= datetime.now(timezone.utc):
            continue
        job_id = f"remind:{appointment.id}:{name}"
        if already_sent(f"generated:{job_id}", 86400 * 30):
            continue
        jobs.append({
            "id": job_id,
            "channels": channels,
            "remind_at": remind_at.isoformat(),
            "to_email": appointment.email,
            "to_phone": appointment.phone,
            "subject": f"Reminder: {appointment.title} ({name})",
            "text": f"Hi {appointment.patient_name}, this is a reminder for {appointment.title}.",
            "html": f"<p>Hi {appointment.patient_name},</p><p>Reminder: <b>{appointment.title}</b></p>",
        })
    return jobs


def process_due_reminders():
    """Poll reminder queue and dispatch due items."""
    while True:
        _, data = r.brpop("reminder:queue", timeout=5)
        job = json.loads(data)
        remind_at = datetime.fromisoformat(job["remind_at"])
        if remind_at > datetime.now(timezone.utc):
            # Not yet due — requeue with delay
            delay = (remind_at - datetime.now(timezone.utc)).total_seconds()
            if delay < 300:
                time.sleep(delay)
            else:
                r.zadd("reminder:scheduled", {json.dumps(job): remind_at.timestamp()})
                continue
        for channel in job["channels"]:
            dedup_key = f"sent:{job['id']}:{channel}"
            if already_sent(dedup_key):
                continue
            try:
                if channel == "email":
                    apply_backoff(lambda: send_email(job))
                elif channel == "sms":
                    apply_backoff(lambda: send_sms(job))
                logger.info("Delivered %s via %s", job["id"], channel)
            except Exception as e:
                logger.error("Failed %s via %s: %s", job["id"], channel, e)
                r.lpush("reminder:dlq", json.dumps({"job": job, "error": str(e)}))


if __name__ == "__main__":
    # Example: schedule reminders for a new appointment
    apt = Appointment(
        id=uuid.uuid4().hex[:8],
        patient_name="Alice",
        email="alice@example.com",
        phone="+1234567890",
        start_time=datetime.now(timezone.utc) + timedelta(hours=2),
        title="Dentist Checkup",
        location="Suite 201",
    )
    reminders = schedule_reminders(apt)
    for rm in reminders:
        r.lpush("reminder:queue", json.dumps(rm))
        logger.info("Enqueued %s", rm["id"])
    # Start worker
    process_due_reminders()
```

---

## References

- [IANA Time Zone Database](https://www.iana.org/time-zones) — Official timezone data
- [crontab.guru](https://crontab.guru) — Cron expression editor and reference
- [SendGrid Email Deliverability Guide](https://docs.sendgrid.com/ui/sending-email/deliverability)
- [Twilio SMS Best Practices](https://www.twilio.com/docs/sms/best-practices)
- [BullMQ Documentation](https://docs.bullmq.io)
- [Redis as a queue](https://redis.io/learn/howtos/queues)