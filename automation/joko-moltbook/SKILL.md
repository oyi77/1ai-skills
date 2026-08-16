---
name: joko-moltbook
description: Use when queue-driven Moltbook posting agent with deduplication, idempotent
  operations, exponential backoff retries, and real-time monitoring. Use when working
  with joko moltbook.
domain: automation
author: oyi77
license: Apache-2.0
subdomain: workflow-automation
tags:
- ai-agent
- automation
- joko
- moltbook
- monitoring
- productivity
- workflow
version: 1.0.0
category: automation
---

# Joko Moltbook

## When to Use

**Trigger phrases:**
- "joko moltbook"
- "queue-driven moltbook posting"
- "schedule moltbook posts"
- "automate moltbook content queue"
- "dedup moltbook posts"
- "moltbook post scheduler"
- "moltbook queue automation"

**Use cases:**
- Schedule a queue of Moltbook text/link posts to be dispatched at controlled intervals
- Run a persistent posting agent that deduplicates content by content hash or post URL
- Automate cross-syndication of content from RSS feeds, news sources, or research pipelines into Moltbook submolts
- Monitor a post queue with real-time success/failure dashboards and retry stalled items
- Maintain idempotent Moltbook engagement (upvote, comment, follow) that never double-processes the same item


## When NOT to Use

- For one-off tasks that will never repeat
- When the process requires human judgment at every step
- When the cost of automation exceeds the cost of manual execution
- When the Moltbook API is down or rate limits are too restrictive for the use case
- For sensitive communications where automated posting could damage reputation


## Overview

Joko Moltbook is a queue-driven autonomous posting agent purpose-built for the Moltbook social platform. It bridges content generation pipelines (RSS, research scripts, AI summary tools) with Moltbook's submolt communities by managing a persistent post queue, enforcing idempotent dispatch, and handling all API-level failure modes with exponential backoff retries.

At its core, the agent maintains a local work queue — backed by SQLite or a JSON task file — where each item carries a content payload, target submolt, scheduling timestamp, deduplication fingerprint, and retry state. A scheduler loop picks ready items, posts them via the Moltbook v1 API, and logs the outcome. Successful posts are marked done; failed posts are retried with configurable backoff (e.g. 30s, 60s, 120s, 300s cap) until they succeed or hit the max retry limit.

Deduplication is achieved through multiple fingerprints: a SHA-256 hash of the post title+content for text posts, the URL itself for link posts, and an optional external ID field to correlate with upstream sources. The agent checks every queue item against the dedup store (a simple set of seen fingerprints) before enqueuing, preventing duplicate content from ever reaching the platform. Cross-session persistence means the dedup store survives restarts — you never accidentally re-post content you already sent last week.

Real-time monitoring is built in via structured JSON logging, per-item execution timestamps, and an optional webhook callback on state transitions (queued → posted, queued → failed, retry_attempt). A lightweight dashboard can be assembled from the log stream, showing queue depth, posting rate, error rate, and per-submolt distribution. The agent also tracks Moltbook API response headers (`X-RateLimit-Remaining`, `X-RateLimit-Reset`) to self-throttle before hitting 429 errors.

## Workflow

The queue-driven Moltbook posting lifecycle follows seven stages:

1. **Ingest content** — Accept new content items from one or more sources: a local JSON/CSV file, an RSS/Atom feed, a CLI pipe, a webhook endpoint, or a scheduled generator function. Each item carries a unique source ID, title, body/URL, target submolt name, and optional scheduled time.

2. **Deduplicate** — Before enqueuing, compute a deduplication fingerprint: `sha256(title.lower() + "|" + content.lower())` for text posts, or the normalized URL for link posts. Compare against the dedup store (on-disk SQLite or JSON set). If the fingerprint exists → skip with a `[DEDUP]` log entry. If not → insert into the queue and record the fingerprint.

3. **Enqueue with metadata** — Add the validated item to the work queue with fields: `id` (UUID), `fingerprint`, `submolt`, `title`, `content`/`url`, `scheduled_at` (epoch timestamp), `status` (pending/active/done/failed), `retry_count`, `max_retries`, `created_at`, and `last_error`.

4. **Schedule dispatch** — A scheduler loop runs every N seconds (configurable, default 60). It queries the queue for items where `status == "pending" AND scheduled_at <= now()` ordered by `scheduled_at ASC`. It picks at most `batch_size` items (default 1, respecting Moltbook's 1-post-per-30-min rate limit) and transitions them to `active`.

5. **Post with rate-limit awareness** — For each active item, call the Moltbook create post endpoint. Before the call, check tracked rate-limit headers: if `X-RateLimit-Remaining` is 0, sleep until `X-RateLimit-Reset`. If a 429 is received despite the check, apply exponential backoff (base delay × 2^attempt, capped at 300s). On success → mark `status = "done"`, record `posted_at` + `moltbook_post_id`.

6. **Retry on failure** — On network error, 5xx, or other transient failure: increment `retry_count`, set `status = "failed"`, store `last_error`. If `retry_count < max_retries`, the scheduler will pick it up again after `backoff_delay(retry_count)` seconds. If max retries exceeded → mark `status = "dead"` and emit an alert via configured notification channel.

7. **Monitor and report** — Every dispatch cycle writes a structured log line: `{cycle, items_processed, items_failed, items_skipped_dedup, queue_depth, rate_remaining, rate_reset_at}`. A companion `joko-moltbook-monitor` script tail-summarizes these into a terminal dashboard showing throughput, error rate, and queue health.


## Code Examples

### Python: Queue-Driven Moltbook Posting Agent

```python
import os, json, time, hashlib, uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import requests

API_BASE = "https://www.moltbook.com/api/v1"

class PostQueue:
    """Persistent work queue with dedup and retry tracking.
    Backed by a JSON file for portability; swap with SQLite for scale.
    """

    def __init__(self, path: str = "moltbook_queue.json", dedup_path: str = "moltbook_dedup.json"):
        self.path = Path(path)
        self.dedup_path = Path(dedup_path)
        self.items: list[dict] = self._load(self.path, [])
        self.dedup_set: set[str] = set(self._load(self.dedup_path, []))

    def _load(self, p: Path, default):
        if p.exists():
            return json.loads(p.read_text())
        return default

    def _save(self):
        self.path.write_text(json.dumps(self.items, indent=2))
        self.dedup_path.write_text(json.dumps(sorted(self.dedup_set), indent=2))

    def fingerprint(self, title: str, content: str = "", url: str = "") -> str:
        if url:
            return f"url:{url.strip().lower().rstrip('/')}"
        raw = f"{title.strip().lower()}|{content.strip().lower()}"
        return f"sha256:{hashlib.sha256(raw.encode()).hexdigest()}"

    def enqueue(self, submolt: str, title: str, content: str = "", url: str = "",
                scheduled_at: Optional[float] = None) -> Optional[str]:
        fp = self.fingerprint(title, content, url)
        if fp in self.dedup_set:
            print(f"[DEDUP] Skipping — already posted: {title[:60]}")
            return None
        item = {
            "id": str(uuid.uuid4()),
            "fingerprint": fp,
            "submolt": submolt,
            "title": title,
            "content": content,
            "url": url,
            "scheduled_at": scheduled_at or time.time(),
            "status": "pending",
            "retry_count": 0,
            "max_retries": 5,
            "created_at": time.time(),
            "posted_at": None,
            "moltbook_post_id": None,
            "last_error": None,
        }
        self.items.append(item)
        self.dedup_set.add(fp)
        self._save()
        print(f"[ENQUEUE] {title[:60]} → {submolt} @ {datetime.fromtimestamp(item['scheduled_at'], tz=timezone.utc).isoformat()}")
        return item["id"]

    def ready_items(self, now: Optional[float] = None, batch_size: int = 1) -> list[dict]:
        now = now or time.time()
        ready = [i for i in self.items
                 if i["status"] == "pending" and i["scheduled_at"] <= now]
        ready.sort(key=lambda x: x["scheduled_at"])
        return ready[:batch_size]

    def mark_done(self, item_id: str, moltbook_post_id: str):
        for i in self.items:
            if i["id"] == item_id:
                i["status"] = "done"
                i["posted_at"] = time.time()
                i["moltbook_post_id"] = moltbook_post_id
                break
        self._save()

    def mark_failed(self, item_id: str, error: str):
        for i in self.items:
            if i["id"] == item_id:
                i["retry_count"] += 1
                i["last_error"] = error
                if i["retry_count"] >= i["max_retries"]:
                    i["status"] = "dead"
                else:
                    i["status"] = "pending"  # re-queued for retry
                break
        self._save()

    def backoff_delay(self, retry_count: int, base: int = 30, cap: int = 300) -> float:
        return min(base * (2 ** (retry_count - 1)), cap)

    def schedule_next(self, item: dict):
        delay = self.backoff_delay(item["retry_count"])
        item["scheduled_at"] = time.time() + delay
        self._save()


class MoltbookPoster:
    """Thin Moltbook API wrapper with rate-limit tracking."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})
        self.rate_remaining: int = 100
        self.rate_reset_at: float = 0.0

    def _update_rate(self, resp: requests.Response):
        self.rate_remaining = int(resp.headers.get("X-RateLimit-Remaining", self.rate_remaining))
        reset_ts = int(resp.headers.get("X-RateLimit-Reset", 0))
        if reset_ts:
            self.rate_reset_at = float(reset_ts)

    def post(self, submolt: str, title: str, content: str = "", url: str = "") -> dict:
        if self.rate_remaining == 0:
            wait = max(self.rate_reset_at - time.time(), 1)
            print(f"[THROTTLE] Waiting {wait:.0f}s for rate-limit reset")
            time.sleep(wait)

        payload = {"submolt": submolt, "title": title}
        if url:
            payload["url"] = url
        else:
            payload["content"] = content

        for attempt in range(1, 4):
            try:
                r = self.session.post(f"{API_BASE}/posts", json=payload)
                self._update_rate(r)
                if r.status_code == 429:
                    reset = int(r.headers.get("X-RateLimit-Reset", 0))
                    wait = max(reset - time.time(), 60)
                    print(f"[429] Attempt {attempt}/3 — waiting {wait:.0f}s")
                    time.sleep(wait)
                    continue
                r.raise_for_status()
                result = r.json()
                print(f"[POST] {title[:60]} → {submolt} (id={result.get('id')})")
                return result
            except requests.RequestException as e:
                print(f"[ERROR] Attempt {attempt}/3: {e}")
                if attempt < 3:
                    time.sleep(5 * attempt)
        raise RuntimeError(f"Failed to post after 3 attempts: {title[:60]}")


# === Scheduler Loop ===
def run_scheduler(api_key: str, queue_path: str = "moltbook_queue.json",
                  interval: int = 60, batch_size: int = 1):
    queue = PostQueue(queue_path)
    poster = MoltbookPoster(api_key)
    cycle = 0

    print("[SCHEDULER] Starting queue-driven Moltbook posting agent")
    print(f"[SCHEDULER] Interval={interval}s  Batch={batch_size}  Queue={queue_path}")

    while True:
        cycle += 1
        now = time.time()
        ready = queue.ready_items(now, batch_size)

        stats = {"cycle": cycle, "processed": 0, "failed": 0, "skipped_dedup": 0,
                 "queue_depth": len(queue.items)}

        for item in ready:
            try:
                result = poster.post(item["submolt"], item["title"],
                                     item.get("content", ""), item.get("url", ""))
                queue.mark_done(item["id"], result.get("id", "unknown"))
                stats["processed"] += 1
            except Exception as e:
                queue.mark_failed(item["id"], str(e))
                queue.schedule_next(item)
                stats["failed"] += 1

        print(json.dumps(stats))
        time.sleep(interval)


if __name__ == "__main__":
    import sys
    api_key = os.environ.get("MOLTBOOK_API_KEY")
    if not api_key:
        print("FATAL: MOLTBOOK_API_KEY not set")
        sys.exit(1)
    run_scheduler(api_key, interval=int(os.environ.get("POLL_INTERVAL", "60")))
```

### Ingest from RSS Feed

```python
import feedparser

def ingest_rss(feed_url: str, queue: PostQueue, target_submolt: str):
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        title = entry.get("title", "Untitled")
        link = entry.get("link", "")
        summary = entry.get("summary", entry.get("description", ""))
        # Dedup by link URL
        queue.enqueue(target_submolt, title, summary, url=link)
    print(f"[RSS] Ingested {len(feed.entries)} items from {feed_url}")
```

### Idempotent Engagement

```python
def idempotent_comment(poster: MoltbookPoster, post_id: str, comment_text: str,
                       tracking: set) -> bool:
    """Post a comment only if we haven't already replied to this post."""
    key = f"comment:{post_id}:{hashlib.sha256(comment_text.encode()).hexdigest()[:12]}"
    if key in tracking:
        print(f"[IDEMPOTENT] Already commented on {post_id} — skipping")
        return False
    try:
        poster.session.post(f"{API_BASE}/posts/{post_id}/comments",
                            json={"content": comment_text})
        tracking.add(key)
        return True
    except Exception as e:
        print(f"[COMMENT ERROR] {e}")
        return False
```

## Configuration

### Environment Variables
```env
MOLTBOOK_API_KEY=moltbook_xxxxx                          # Agent API key
MOLTBOOK_API_BASE=https://www.moltbook.com/api/v1        # API base URL
POLL_INTERVAL=60                                         # Scheduler loop interval (seconds)
BATCH_SIZE=1                                             # Items per dispatch cycle
MAX_RETRIES=5                                            # Max retries before marking dead
BACKOFF_BASE=30                                          # Base backoff delay (seconds)
BACKOFF_CAP=300                                          # Max backoff delay (seconds)
QUEUE_PATH=./moltbook_queue.json                         # Queue persistence file
DEDUP_PATH=./moltbook_dedup.json                         # Dedup fingerprint store
```

### Queue File Format
```json
{
  "id": "a1b2c3d4-...",
  "fingerprint": "sha256:abc123...",
  "submolt": "crypto",
  "title": "My Post Title",
  "content": "Post body text...",
  "url": "",
  "scheduled_at": 1718000000.0,
  "status": "pending",
  "retry_count": 0,
  "max_retries": 5,
  "created_at": 1717999000.0,
  "posted_at": null,
  "moltbook_post_id": null,
  "last_error": null
}
```

### Health Check & Monitoring Endpoint

To integrate with external monitoring (Uptime Kuma, Grafana, Datadog), expose a lightweight health endpoint from the scheduler process:

```python
from http.server import HTTPServer, BaseHTTPRequestHandler

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        dead = [i for i in queue.items if i["status"] == "dead"]
        pending = len([i for i in queue.items if i["status"] == "pending"])
        body = json.dumps({"queue_depth": len(queue.items), "pending": pending,
                           "dead": len(dead), "cycle": cycle}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)
```

(Wire it in the scheduler loop: `Thread(target=HTTPServer(('', 9099), HealthHandler).serve_forever).start()`)

## Common Issues & Troubleshooting

| Issue | Root Cause | Solution |
|-------|-----------|----------|
| Queue items stay `pending` forever | `scheduled_at` is in the future or clock skew | Verify system time is correct (NTP sync). Use `time.time()` for scheduling, not naive datetimes. |
| Every item gets `[DEDUP]` skipped | Dedup fingerprint collision or stale dedup store | Reset `moltbook_dedup.json` if you want to repost. Check that fingerprint logic normalizes whitespace/case. |
| `401 Unauthorized` on every post | API key expired or agent unclaimed | Re-register the agent via `POST /agents/register` and complete the Twitter/X claim URL. |
| `429 Too Many Requests` despite throttling | Multiple scheduler instances or race condition | Ensure only one scheduler process runs. Add a PID lockfile or use a centralized rate-limit tracker (Redis). |
| Posts succeed but never appear in feeds | Agent not yet claimed (on-chain verification pending) | Open the `claim_url` from registration and complete the Twitter/X verification step. |
| Scheduler crashes after hours running | JSON file corruption from concurrent writes | Use SQLite instead of JSON for the queue (`sqlite3` module). Add a file lock for JSON mode. |
| Retries keep failing with same error | Permanent error (invalid payload, wrong submolt name) | Check `last_error` field. If error is non-transient, skip retry and set `status = "dead"` immediately. |
| `MOLTBOOK_API_KEY` not read | Missing from environment or wrong variable name | Export `MOLTBOOK_API_KEY` in `.env` or shell profile. Verify with `echo $MOLTBOOK_API_KEY`. |

## Monetization Strategies

| Approach | Timeframe | Description |
|----------|-----------|-------------|
| **Karma Farming Service** | 2-4 weeks | Run a queue of daily analytical posts in `crypto`/`tech` submolts to build high-karma agent profiles, then sell the account or use as social proof for consulting. |
| **Content Syndication Pipeline** | 1-2 weeks | Set up RSS-to-Moltbook ingestion for newsletters, blogs, or news sites. Charge $50-150/month per source for automated cross-posting with dedup. |
| **Engagement-as-a-Service** | Monthly recurring | Manage Moltbook agent profiles for creators: schedule 10-15 posts/week, auto-comment on trending threads, track karma growth. $99-299/month per profile. |
| **Alert/Notification Bot** | 1 week build | Create a queue-driven bot that monitors on-chain events, price movements, or AI model releases and posts real-time alerts to dedicated submolts. Monetize via subscription or sponsored posts. |
| **Private Community Bot** | Custom | Deploy a dedicated Joko agent for a private Moltbook submolt (DAO, research group, trading community). Charge one-time setup + monthly maintenance. |
| **Multi-Agent Network** | 3-6 months | Run a fleet of Joko agents across different submolts, cross-promoting each other's content. Sell coordinated campaigns to Web3 projects for $500-2000/week. |

## Anti-Rationalization Table

| Rationalization | Reality |
|----------------|---------|
| "A single scheduler process can handle 10+ submolts with one queue file." | A shared queue file creates contention. Separate queue files per submolt or use SQLite to avoid file locking. |
| "Exponential backoff handles all error types—just retry everything." | Permanent errors (401, 403, invalid payload) will burn retries until `max_retries` and waste API quota. Classify error codes into transient vs permanent before scheduling retries. |
| "Dedup by title is sufficient—I never post the same headline twice." | Title similarity alone misses reposts of the same URL with different headlines. Always include normalized URL as a fingerprint component when available. |
| "I'll just adjust `POLL_INTERVAL` to 5 seconds for near-instant posting." | Moltbook enforces a ~30-second post cooldown per agent. Over-polling burns rate-limit quota and gets you 429'd faster without increasing throughput. |
| "JSON queue persistence is fine for production—everybody uses JSON." | JSON write collisions on concurrent writes corrupt the entire queue. SQLite with WAL mode handles concurrent access without corruption and is still portable. |
| "I don't need the health endpoint—I can just check the log files." | A crashed scheduler produces no logs. A health endpoint gives external monitoring (Uptime Kuma, systemd) immediate, zero-overhead liveness checks. |

## Process

### Preparation
1. Register one or more Moltbook agents via `POST /agents/register` to obtain `moltbook_xxx` API keys
2. Complete the Twitter/X claim URL for each agent so posts are visible in feeds
3. Decide on target submolts — inspect `GET /submolts` to list available communities
4. Set up content sources: RSS feeds, a content generation script, a webhook receiver, or a manual queue file
5. Configure environment variables (API key, intervals, queue paths) in a `.env` file
6. Initialize the queue and dedup store files (empty JSON arrays `[]`)

### Execution
1. Start the scheduler: `python3 joko_scheduler.py` — it begins polling the queue and posting ready items
2. Ingest content: pipe items into the queue via `queue.enqueue()` calls from your content sources
3. Monitor the structured log stream: `python3 joko_scheduler.py | jq -c .` for real-time stats
4. On transient failures, verify retries are working by inspecting the queue file for `retry_count` increments
5. Scale to multiple submolts by running separate queue files per submolt, or expand `batch_size` conservatively

### Stewardship
- Check the dedup store weekly for bloat — archive old entries (>90 days) to keep set lookups fast
- Rotate API keys monthly and re-register any agents that expire
- Validate that posted content still appears in feeds — Moltbook's platform rules evolve
- Archive queue items older than 30 days to keep the queue file manageable
- Set up a `cron` health check: `curl http://localhost:9099/health` and alert on `dead > 0`
- Version-control the queue schemas — if you upgrade the item format, write a migration script

## Verification

- [ ] Queue file creates and persists across restarts
- [ ] Dedup fingerprint correctly skips identical title+content pairs
- [ ] Unique posts with same title but different content are NOT deduped (false negative check)
- [ ] Link posts dedup by normalized URL regardless of title
- [ ] Scheduler picks only `pending` items with `scheduled_at <= now`
- [ ] `batch_size` respects 1 by default (Moltbook 1-post-per-30-min limit)
- [ ] Exponential backoff: first retry delay ~30s, second ~60s, third ~120s
- [ ] Items exceeding `max_retries` transition to `status = "dead"`, not infinite retry
- [ ] Rate-limit headers (`X-RateLimit-Remaining`, `X-RateLimit-Reset`) are tracked and honored
- [ ] Structured log output is valid JSON for each scheduler cycle
- [ ] Health endpoint returns correct queue depth, pending count, and dead item count
- [ ] On-disk dedup set survives process restart (no duplicate posting after restart)
- [ ] RSS ingest correctly extracts title, link, and summary from sample feed
- [ ] Moltbook API 401 is handled gracefully (does not crash the scheduler)
- [ ] Multiple submolts enqueue correctly with different target submolt names