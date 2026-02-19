# Scheduler Class

Manages scheduled posts and handles automated posting.

## Overview

```python
from scripts.scheduler import Scheduler, Schedule
```

Provides scheduling functionality for automated content posting with retry logic.

---

## Dataclasses

### Schedule

Represents a scheduled post.

```python
@dataclass
class Schedule:
    post_id: str
    scheduled_time: datetime
    content: str
    platform: str
    status: str = "pending"  # pending, posted, failed
    retry_count: int = 0
    max_retries: int = 3
    metadata: dict = field(default_factory=dict)
```

**Attributes:**
- `post_id` - Unique identifier for the post
- `scheduled_time` - When to post the content
- `content` - The content to post
- `platform` - Target platform (e.g., 'twitter', 'linkedin')
- `status` - Current status ("pending", "posted", "failed")
- `retry_count` - Number of retry attempts made
- `max_retries` - Maximum retry attempts on failure
- `metadata` - Additional metadata for the post

---

## Scheduler Class

```python
class Scheduler:
    def __init__(self, check_interval: int = 60):
```

**Constructor Parameters:**
- `check_interval` - Seconds between checks for due posts (default: 60)

---

## Methods

### schedule_post()

Schedule a post for automated posting.

```python
def schedule_post(
    self,
    post_id: str,
    scheduled_time: datetime,
    content: str,
    platform: str,
    max_retries: int = 3,
    metadata: Optional[dict] = None,
) -> Schedule
```

**Parameters:**
- `post_id` - Unique identifier for the post
- `scheduled_time` - When to post the content
- `content` - The content to post
- `platform` - Target platform
- `max_retries` - Maximum retry attempts on failure (default: 3)
- `metadata` - Additional metadata for the post

**Returns:** The created Schedule object

**Note:** Posts are automatically sorted by scheduled time

---

### cancel_post()

Cancel a scheduled post.

```python
def cancel_post(self, post_id: str) -> bool
```

**Parameters:**
- `post_id` - ID of the post to cancel

**Returns:** True if cancelled, False if not found or not pending

---

### get_pending_posts()

Get all pending posts.

```python
def get_pending_posts(self) -> list[Schedule]
```

**Returns:** List of pending Schedule objects

---

### get_post()

Get a specific post by ID.

```python
def get_post(self, post_id: str) -> Optional[Schedule]
```

**Parameters:**
- `post_id` - ID of the post to retrieve

**Returns:** Schedule object if found, None otherwise

---

### set_post_callback()

Set the callback function for executing posts.

```python
def set_post_callback(self, callback: Callable[[Schedule], bool]):
```

**Parameters:**
- `callback` - Function that takes a Schedule and returns bool (success)

---

### run_scheduler()

Main scheduler loop - runs continuously processing due posts.

```python
def run_scheduler(self, duration: Optional[int] = None):
```

**Parameters:**
- `duration` - Optional duration in seconds (runs forever if None)

**Note:** Processes due posts and handles retries with exponential backoff

---

### stop()

Stop the scheduler.

```python
def stop(self):
```

---

## Internal Methods

### _execute_post()

Execute the post using the callback.

```python
def _execute_post(self, schedule: Schedule) -> bool
```

**Returns:** True if successful, False otherwise

---

### _process_due_posts()

Process all posts that are due.

**Logic:**
1. Find all pending posts where `scheduled_time <= now`
2. Execute each post using the callback
3. On success: mark as "posted"
4. On failure: increment retry_count
5. If max_retries reached: mark as "failed"
6. Otherwise: reschedule with exponential backoff (min 10s, max 300s)

---

## Retry Logic

The scheduler implements exponential backoff for failed posts:

```python
# Reschedule with incremental backoff
schedule.scheduled_time = now + timedelta(
    seconds=min(2**schedule.retry_count * 10, 300)
)
```

| Retry Count | Backoff |
|-------------|---------|
| 1 | 20 seconds |
| 2 | 40 seconds |
| 3 | 80 seconds |
| 4+ | 300 seconds (max) |

---

## Usage Example

```python
from datetime import datetime, timedelta
from scripts.scheduler import Scheduler, Schedule

def my_post_callback(schedule: Schedule) -> bool:
    """Callback to execute the actual post"""
    print(f"Posting to {schedule.platform}: {schedule.content[:50]}...")
    
    # Your posting logic here
    # Return True on success, False on failure
    return True

# Create scheduler
scheduler = Scheduler(check_interval=60)

# Set the callback
scheduler.set_post_callback(my_post_callback)

# Schedule posts
now = datetime.now()

scheduler.schedule_post(
    post_id="post_001",
    scheduled_time=now + timedelta(hours=1),
    content="Hello, this is my first scheduled post!",
    platform="twitter"
)

scheduler.schedule_post(
    post_id="post_002",
    scheduled_time=now + timedelta(hours=2),
    content="Another post coming soon",
    platform="linkedin"
)

# Run scheduler for 3 hours
print("Starting scheduler...")
scheduler.run_scheduler(duration=10800)

# Check final status
print("\nFinal post statuses:")
for post in scheduler.scheduled_posts:
    print(f"  {post.post_id}: {post.status}")
```

---

## Async Usage

For async applications, you can wrap the scheduler:

```python
import asyncio
from scripts.scheduler import Scheduler, Schedule

class AsyncScheduler(Scheduler):
    async def _execute_post(self, schedule: Schedule) -> bool:
        # Your async posting logic
        await post_to_platform(schedule)
        return True

async def main():
    scheduler = AsyncScheduler(check_interval=30)
    scheduler.set_post_callback(your_callback)
    
    # Schedule posts
    scheduler.schedule_post(...)
    
    # Run async loop
    while scheduler.running:
        scheduler._process_due_posts()
        await asyncio.sleep(scheduler.check_interval)

asyncio.run(main())
```

---

## Thread Safety

The Scheduler is thread-safe:
- Uses `threading.Lock` for all list operations
- Safe to call from multiple threads
- Callback execution happens in the main thread
