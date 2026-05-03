"""Scheduler for automated content posting."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Callable, Optional
import time
import threading


@dataclass
class Schedule:
    """Represents a scheduled post."""

    post_id: str
    scheduled_time: datetime
    content: str
    platform: str
    status: str = "pending"  # pending, posted, failed
    retry_count: int = 0
    max_retries: int = 3
    metadata: dict = field(default_factory=dict)


class Scheduler:
    """Manages scheduled posts and handles automated posting."""

    def __init__(self, check_interval: int = 60):
        """
        Initialize the scheduler.

        Args:
            check_interval: Seconds between checks for due posts (default: 60)
        """
        self.scheduled_posts: list[Schedule] = []
        self.check_interval = check_interval
        self.running = False
        self.post_callback: Optional[Callable[[Schedule], bool]] = None
        self._lock = threading.Lock()

    def schedule_post(
        self,
        post_id: str,
        scheduled_time: datetime,
        content: str,
        platform: str,
        max_retries: int = 3,
        metadata: Optional[dict] = None,
    ) -> Schedule:
        """
        Schedule a post for automated posting.

        Args:
            post_id: Unique identifier for the post
            scheduled_time: When to post the content
            content: The content to post
            platform: Target platform (e.g., 'twitter', 'linkedin')
            max_retries: Maximum retry attempts on failure
            metadata: Additional metadata for the post

        Returns:
            The created Schedule object
        """
        schedule = Schedule(
            post_id=post_id,
            scheduled_time=scheduled_time,
            content=content,
            platform=platform,
            max_retries=max_retries,
            metadata=metadata or {},
        )

        with self._lock:
            self.scheduled_posts.append(schedule)
            # Sort by scheduled time
            self.scheduled_posts.sort(key=lambda x: x.scheduled_time)

        return schedule

    def cancel_post(self, post_id: str) -> bool:
        """
        Cancel a scheduled post.

        Args:
            post_id: ID of the post to cancel

        Returns:
            True if cancelled, False if not found
        """
        with self._lock:
            for i, post in enumerate(self.scheduled_posts):
                if post.post_id == post_id and post.status == "pending":
                    self.scheduled_posts.pop(i)
                    return True
        return False

    def get_pending_posts(self) -> list[Schedule]:
        """Get all pending posts."""
        with self._lock:
            return [p for p in self.scheduled_posts if p.status == "pending"]

    def get_post(self, post_id: str) -> Optional[Schedule]:
        """Get a specific post by ID."""
        with self._lock:
            for post in self.scheduled_posts:
                if post.post_id == post_id:
                    return post
        return None

    def _execute_post(self, schedule: Schedule) -> bool:
        """Execute the post using the callback."""
        if self.post_callback:
            try:
                return self.post_callback(schedule)
            except Exception as e:
                print(f"Error executing post {schedule.post_id}: {e}")
                return False
        print(f"No callback set for post {schedule.post_id}")
        return False

    def _process_due_posts(self):
        """Process all posts that are due."""
        now = datetime.now()

        with self._lock:
            due_posts = [
                p
                for p in self.scheduled_posts
                if p.status == "pending" and p.scheduled_time <= now
            ]

        for schedule in due_posts:
            success = self._execute_post(schedule)

            with self._lock:
                if success:
                    schedule.status = "posted"
                else:
                    schedule.retry_count += 1
                    if schedule.retry_count >= schedule.max_retries:
                        schedule.status = "failed"
                    else:
                        # Reschedule with incremental backoff
                        schedule.scheduled_time = now + timedelta(
                            seconds=min(2**schedule.retry_count * 10, 300)
                        )

    def run_scheduler(self, duration: Optional[int] = None):
        """
        Main scheduler loop - runs continuously processing due posts.

        Args:
            duration: Optional duration in seconds (runs forever if None)
        """
        self.running = True
        start_time = time.time()

        print(f"Scheduler started (interval: {self.check_interval}s)")

        try:
            while self.running:
                self._process_due_posts()

                if duration and (time.time() - start_time) >= duration:
                    break

                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            print("\nScheduler interrupted")
        finally:
            self.running = False
            print("Scheduler stopped")

    def stop(self):
        """Stop the scheduler."""
        self.running = False

    def set_post_callback(self, callback: Callable[[Schedule], bool]):
        """
        Set the callback function for executing posts.

        Args:
            callback: Function that takes a Schedule and returns bool (success)
        """
        self.post_callback = callback


# Example usage
if __name__ == "__main__":

    def example_post_callback(schedule: Schedule) -> bool:
        """Example callback that simulates posting."""
        print(f"Posting to {schedule.platform}: {schedule.content[:50]}...")
        # Simulate posting success
        return True

    # Create scheduler
    scheduler = Scheduler(check_interval=10)
    scheduler.set_post_callback(example_post_callback)

    # Schedule some posts
    now = datetime.now()
    scheduler.schedule_post(
        post_id="post_001",
        scheduled_time=now + timedelta(seconds=15),
        content="Hello from the scheduler!",
        platform="twitter",
    )

    scheduler.schedule_post(
        post_id="post_002",
        scheduled_time=now + timedelta(seconds=25),
        content="Another scheduled post",
        platform="linkedin",
    )

    print("Running scheduler for 30 seconds...")
    scheduler.run_scheduler(duration=30)

    # Print results
    print("\nFinal post statuses:")
    for post in scheduler.scheduled_posts:
        print(f"  {post.post_id}: {post.status}")
