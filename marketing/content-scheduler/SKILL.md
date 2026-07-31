---
name: content-scheduler
description: Schedule and manage content publishing across platforms with Notion calendar. Use when scheduleing and manage content publishing across platforms with notion calendar.
domain: marketing
author: oyi77
license: Apache-2.0
subdomain: marketing
tags:
- content
- growth
- marketing
- notion
- scheduler
- seo
allowed-tools: "|\n  - MCP(notion:*)\n    - MCP(slack:*)\n"
version: 1.0.0
---
# Content Scheduler

## When to Use

**Trigger phrases:**
- "content scheduler"
- "Help me with content scheduler"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


## When NOT to Use

- When the audience is too small to justify the effort
- For regulated industries without compliance review
- When the campaign budget does not support the channel


## Overview

Content Scheduler is a structured system for planning, organizing, and automating content publication across multiple platforms from a single calendar. It enables creators, marketers, and publishers to map out a full content pipeline — blog posts, social media updates, newsletters, videos, and ads — on a shared timeline, ensuring consistent output without last-minute scrambling.

At its core, the scheduler maintains a master content calendar (backed by Notion or a similar database) that tracks every piece of content through its lifecycle: ideation, drafting, review, scheduling, publishing, and post-performance analysis. Each entry carries metadata for the target platform, publish time, status, assigned creator, and cross-post relationships so a single blog post can automatically spawn a Twitter thread, LinkedIn summary, and newsletter excerpt at the right intervals.

Multi-platform scheduling is handled through platform-specific publishing queues. The scheduler respects each platform's optimal posting times, content format constraints, and audience time zones. Batch content planning allows you to generate a month's worth of posts in one session, queue up with cadence rules (every Mon/Wed/Fri at 10AM), and let the automation handle daily distribution. Notion calendar integration provides a visual drag-and-drop interface to adjust dates, swap slots, and see the full publishing landscape at a glance.

Publishing workflow automation ties everything together: when content reaches its scheduled time, the system pushes it to the destination platform (via API or browser automation), updates the calendar status to "published," logs the performance baseline, and triggers the next item in the cross-post chain. This transforms content management from a daily firefight into a predictable, scalable operation.

## Workflow

```python
# Example: Generate a monthly content calendar with cadence rules
from datetime import datetime, timedelta
from dataclasses import dataclass, field

@dataclass
class ScheduledPost:
    platform: str
    content: str
    publish_at: datetime
    status: str = "draft"  # draft | scheduled | published | failed
    cross_post_of: str | None = None

def generate_monthly_calendar(
    start_date: datetime,
    platforms: dict[str, list[str]],  # platform -> [days of week]
    time_slots: dict[str, str],        # platform -> "HH:MM"
    timezone: str = "UTC"
) -> list[ScheduledPost]:
    """Generate a month of scheduled posts from cadence rules."""
    calendar = []
    current = start_date
    end = start_date + timedelta(days=30)
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    while current < end:
        day_abbr = day_names[current.weekday()]
        for platform, days in platforms.items():
            if day_abbr in days:
                hour, minute = time_slots[platform].split(":")
                publish_at = current.replace(
                    hour=int(hour), minute=int(minute),
                    second=0, microsecond=0
                )
                calendar.append(ScheduledPost(
                    platform=platform,
                    content="",  # filled during batch creation
                    publish_at=publish_at,
                ))
        current += timedelta(days=1)
    return sorted(calendar, key=lambda p: p.publish_at)
```

1. **Calendar Setup** — Initialize a master content calendar in Notion, Airtable, or a local SQLite database with fields for date, time, platform, status, content draft, and cross-post references.
2. **Cadence Definition** — Define per-platform posting frequencies (e.g., Twitter 3x/day, LinkedIn 2x/week, blog 1x/week) and preferred time slots. Build re-usable content templates per platform.
3. **Batch Planning** — Generate a month of time slots, then fill them in bulk: write all blog posts, social captions, and newsletter drafts in one dedicated session. Each piece references the master calendar slot.
4. **Review & Approve** — Run each piece through the review gate: check platform-specific formatting, brand voice compliance, link validation, and legal disclaimers. Approve items move to "scheduled" status.
5. **Queue to Platforms** — Push scheduled items into platform-specific publishing queues. Blog posts go to CMS draft, social posts to a buffer app, newsletter drafts to the email platform. Cross-post links are recorded so publishing one auto-triggers the next.
6. **Automated Publishing** — At each scheduled time, the publisher service picks the next due item, formats it for the target platform, posts via API or browser automation, and updates the calendar status to "published."
7. **Performance Logging** — After each publish, capture baseline metrics (views, reach, engagement) from the platform API. Store alongside the calendar entry for trend analysis and future optimization.

## Code Examples

### Notion Calendar Integration

```python
import requests
from datetime import datetime

NOTION_TOKEN = "secret_YOUR_TOKEN"
DATABASE_ID = "your_calendar_db_id"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def add_calendar_entry(title: str, platform: str, publish_at: datetime, status: str = "draft") -> dict:
    """Add a scheduled post to the Notion calendar database."""
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Title": {"title": [{"text": {"content": title}}]},
            "Platform": {"select": {"name": platform}},
            "Publish Date": {"date": {"start": publish_at.isoformat()}},
            "Status": {"status": {"name": status}},
        },
    }
    resp = requests.post(
        "https://api.notion.com/v1/pages",
        headers=HEADERS, json=payload
    )
    resp.raise_for_status()
    return resp.json()

def get_scheduled_for_today(platform: str | None = None) -> list[dict]:
    """Retrieve items scheduled for today, optionally filtered by platform."""
    today = datetime.utcnow().date().isoformat()
    filters = {
        "and": [
            {"property": "Publish Date", "date": {"equals": today}},
            {"property": "Status", "status": {"equals": "scheduled"}},
        ]
    }
    if platform:
        filters["and"].append(
            {"property": "Platform", "select": {"equals": platform}}
        )
    payload = {"filter": filters}
    resp = requests.post(
        f"https://api.notion.com/v1/databases/{DATABASE_ID}/query",
        headers=HEADERS, json=payload
    )
    resp.raise_for_status()
    return resp.json()["results"]
```

### Batch Content Queue

```python
import json
from pathlib import Path

class ContentQueue:
    """Local file-based publishing queue for offline batch planning."""

    def __init__(self, queue_path: str = "content_queue.json"):
        self.path = Path(queue_path)
        self.queue: list[dict] = []
        if self.path.exists():
            self.queue = json.loads(self.path.read_text())

    def enqueue(self, entry: dict) -> None:
        """Add a scheduled entry to the queue."""
        self.queue.append(entry)
        self._save()

    def enqueue_batch(self, entries: list[dict]) -> None:
        """Add multiple entries at once (batch planning output)."""
        self.queue.extend(entries)
        self._save()

    def dequeue_due(self, reference_time: str | None = None) -> list[dict]:
        """Return all entries due for publishing and mark them in-flight."""
        import datetime as dt
        now = dt.datetime.utcnow().isoformat() if reference_time is None else reference_time
        due = [e for e in self.queue
               if e.get("publish_at", "") <= now
               and e.get("status") == "scheduled"]
        for entry in due:
            entry["status"] = "publishing"
        self._save()
        return due

    def mark_complete(self, entry_id: str) -> None:
        """Mark a published entry as complete."""
        for entry in self.queue:
            if entry.get("id") == entry_id:
                entry["status"] = "published"
                break
        self._save()

    def _save(self) -> None:
        self.path.write_text(json.dumps(self.queue, indent=2))
```

## Key Metrics

- **Scheduling accuracy** — Percentage of posts published within 15 minutes of scheduled time
- **Content throughput** — Total posts published per week/month across all platforms
- **Calendar fill rate** — Percentage of available time slots that have content assigned
- **Review cycle time** — Average hours from draft submission to approval
- **Cross-post completion** — Rate at which scheduled cross-posts actually publish on time
- **Platform delivery rate** — Successful publishes vs. scheduled per platform (accounts for API failures, rate limits, content rejections)

## Best Practices

- **Maintain a single source of truth calendar** — Never split schedules across spreadsheets, Notion, and platform-native tools. One calendar feeds all platforms.
- **Timezone-lock your schedule** — Choose one canonical timezone for the entire calendar. Convert to local time only at publish time, not during planning.
- **Plan in batches, publish atomically** — Dedicate one session per month to fill the calendar, then let automation handle daily execution. Never write a post the day it goes live.
- **Build buffer slots** — Reserve 20% of calendar slots for timely content (trends, news, product updates). Over-scheduling every slot leaves no room for reactive content.
- **Audit cross-post chains** — A blog -> Twitter thread -> LinkedIn summary -> newsletter chain has four failure points. Each step should log its own publish status and alert on failure.
- **Respect platform rate limits** — Schedule batch pushes with interleaved delays. Publishing 30 posts in 3 seconds triggers spam filters on every platform.
- **Version-control your calendar** — Treat the calendar file (JSON/YAML) as code. Commit it alongside content drafts so you can roll back schedule changes.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I can just post whenever I feel like it" | Audiences expect consistency. Sporadic posting destroys algorithmic reach and subscriber trust. A schedule turns intention into discipline. |
| "Planning a month ahead kills spontaneity" | A 70% filled calendar with 30% buffer slots gives you both structure and room for hot takes. The alternative is scrambling for content every morning. |
| "I remember what needs to go out today" | You do not. A written calendar beats human memory for every metric: on-time rate, platform coverage, cross-post completion. Write it down. |
| "Notion is overkill for a publishing calendar" | A flat spreadsheet works for one platform. Add Twitter, LinkedIn, newsletter, blog, YouTube, and cross-post chains — you need a relational database with status tracking. |
| "Auto-publishing removes the human touch" | Automation handles the delivery. Humans write the content, choose the timing, and craft the voice. Removing the delivery chore frees time for better writing. |
| "Schedule once and forget it" | Platforms change APIs, optimal posting times shift, holidays disrupt cadence. Revisit the calendar weekly to validate upcoming slots and bi-monthly to tune cadence rules. |

## Setup / Configuration

### Notion Calendar Template

Create a Notion database with these properties:

| Property | Type | Purpose |
|---|---|---|
| Title | Title | Post title or headline |
| Platform | Select | Target platform (Twitter, LinkedIn, Blog, Newsletter, YouTube) |
| Publish Date | Date | Scheduled publish date and time |
| Status | Status | draft -> review -> scheduled -> publishing -> published -> failed |
| Content | Text | Full post content or draft link |
| Cross-Post Source | Relation | Links to the parent post if this is a cross-post |
| Tags | Multi-select | Topic labels for content mix analysis |
| Notes | Text | Internal instructions, review feedback, links |

### Integration Tokens

```bash
# Notion API — create an integration at https://www.notion.so/my-integrations
export NOTION_TOKEN="secret_YOUR_TOKEN"
export NOTION_CALENDAR_DB_ID="your_database_id"

# Social platform API keys (one per platform)
export TWITTER_API_KEY="..."
export LINKEDIN_ACCESS_TOKEN="..."
export BUFFER_ACCESS_TOKEN="..."
```

### Queue File Location

```python
# config.py
import os

CONTENT_QUEUE_PATH = os.getenv("CONTENT_QUEUE_PATH", "data/queue.json")
CALENDAR_DB_PATH = os.getenv("CALENDAR_DB_PATH", "data/calendar.db")
CALENDAR_TIMEZONE = os.getenv("CALENDAR_TIMEZONE", "UTC")
PUBLISH_POLL_INTERVAL = int(os.getenv("PUBLISH_POLL_INTERVAL", "300"))  # seconds
```

## Common Issues / Troubleshooting

| Issue | Root Cause | Solution |
|---|---|---|
| Post missed its scheduled time | Timezone mismatch between calendar and publisher | Lock the entire pipeline to one timezone (UTC). Convert only at display time. |
| Notion API returns 401 | Token expired or integration not shared with database | Regenerate token at notion.so/my-integrations. Share the database with the integration via the Share button. |
| Platform rejects post | Content exceeds platform character limit or has blocked links | Add a pre-flight validation step that checks length, link domains, and formatting before setting status to "scheduled". |
| Cross-post chain breaks | Downstream platform API is down when the chain triggers | Make each cross-post an independent scheduled entry with its own status. Do not cascade — poll for parent publish, don't chain. |
| Duplicate posts published | Publisher process runs twice due to overlapping cron jobs | Use a lock file (`/tmp/publisher.lock`) with PID. Skip the run if another instance is active. |
| Calendar growls stale | No regular review cadence | Set a recurring weekly calendar review event. Check next 7 days for completeness and adjust. |
| Rate limited by platform | Batch pushing too many posts at once | Implement inter-post delay (30-60s between social posts). Spread high-volume pushes across hours. |

## Monetization

| Approach | Timeframe | Description |
|---|---|---|
| Content scheduling as a service | 1-2 weeks | Offer to manage a client's content calendar. 20 posts/week on 3 platforms for $500-1000/month. Includes batch planning, scheduling, and monthly performance report. |
| Notion calendar template pack | 1-3 days | Sell a pre-built Notion content calendar database with automation templates on Gumroad for $19-49. Include Zapier/Make integration guides. |
| Queue automation setup | 2-5 days | Install and configure the ContentQueue + publisher pipeline for a client's existing content operation. $200-500 setup + $50/month maintenance. |
| Content ops audit | 3-5 days | Review a client's current scheduling process, find gaps (missed slots, no cross-posts, timezone chaos). Deliver a written report with fix plan. $300-800 per audit. |
| Platform-specific scheduling course | 1-2 weeks | Create a video course teaching batch planning + Notion calendar + automated publishing for a single platform (e.g., LinkedIn scheduling system). $97-197 per enrollment. |

## Process

### Preparation

- Audit current publishing output: how many posts/month per platform, what content types, current cadence.
- Choose a master calendar tool (Notion recommended for relational properties and API access).
- Define per-platform posting cadence and time slots. Start conservative — 30% buffer is minimum.
- Collect all platform API tokens and verify write access with a test post.
- Set up the ContentQueue file or database and the publisher polling service.

### Execution

- Run the monthly batch planning session: generate time slots, assign content, write drafts.
- Push all planned content into the calendar with status="draft".
- Move items through the review gate: format check -> brand voice -> link validation -> status="scheduled".
- At each scheduled time, the publisher picks due items, formats and posts, then logs the result.
- Monitor the first week of automated publishing for platform rejections or timing drift.

### Stewardship

- Review the calendar weekly: confirm next 7 days are fully filled, adjust timings for holidays or events.
- Audit delivery metrics monthly: what percentage of scheduled posts actually published on time? Which platform has the highest failure rate?
- Update cadence rules quarterly based on engagement data. If Tuesday posts underperform, shift them to Wednesday.
- Archive published entries monthly to keep the calendar responsive. Retain performance data for trend analysis.

## Verification

- [ ] Calendar database has all required properties (Title, Platform, Publish Date, Status, Cross-Post Source)
- [ ] API tokens for all platforms return valid test responses before scheduling
- [ ] Batch generation produces correct number of slots for the month (verified against expected cadence)
- [ ] Timezone is consistent across calendar, queue, and publisher (all UTC)
- [ ] Review gate catches at least: character overflows, broken links, missing disclaimers
- [ ] Publisher process has PID lock to prevent duplicate execution
- [ ] Cross-post chain items each have independent status tracking (not cascading)
- [ ] First week of automated publishing monitored and no timing drift exceeds 15 minutes
- [ ] Weekly calendar review scheduled as recurring event
- [ ] Monthly delivery audit captures: on-time rate, platform failure rate, content throughput