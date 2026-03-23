"""
PostBridge API Client
Handles all PostBridge API interactions: posts, media upload, analytics.
Rate-limited to 10 req/s. Auto-retry on transient errors.
"""

import os
import time
import logging
import requests
from pathlib import Path
from typing import Optional, Union
from datetime import datetime, timezone

logger = logging.getLogger("eddie.postbridge")


class RateLimiter:
    """Token bucket rate limiter."""

    def __init__(self, rate: float = 10.0):
        self.rate = rate
        self.tokens = rate
        self.last = time.monotonic()

    def acquire(self):
        now = time.monotonic()
        elapsed = now - self.last
        self.last = now
        self.tokens = min(self.rate, self.tokens + elapsed * self.rate)
        if self.tokens < 1:
            sleep_time = (1 - self.tokens) / self.rate
            logger.debug(f"Rate limit: sleeping {sleep_time:.2f}s")
            time.sleep(sleep_time)
        self.tokens -= 1


class PostBridgeClient:
    """PostBridge API client with rate limiting, retry, and error handling."""

    BASE_URL = "https://api.post-bridge.com/v1"

    def __init__(self, api_key: str, rate_limit: float = 10.0,
                 timeout: int = 30, max_retries: int = 3, retry_delay: float = 2.0):
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.rate_limiter = RateLimiter(rate=rate_limit)
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Execute an API request with rate limiting and retry logic."""
        url = f"{self.BASE_URL}{endpoint}"
        last_error = None

        for attempt in range(1, self.max_retries + 1):
            self.rate_limiter.acquire()
            try:
                resp = self.session.request(method, url, timeout=self.timeout, **kwargs)

                if resp.status_code == 429:
                    retry_after = int(resp.headers.get("Retry-After", self.retry_delay * attempt))
                    logger.warning(f"Rate limited (429). Retrying after {retry_after}s")
                    time.sleep(retry_after)
                    continue

                if resp.status_code >= 500:
                    logger.warning(f"Server error {resp.status_code} on attempt {attempt}/{self.max_retries}")
                    last_error = f"HTTP {resp.status_code}: {resp.text[:200]}"
                    time.sleep(self.retry_delay * attempt)
                    continue

                resp.raise_for_status()

                try:
                    return resp.json()
                except Exception:
                    return {"status": "ok", "raw": resp.text}

            except requests.exceptions.Timeout:
                last_error = f"Request timeout after {self.timeout}s"
                logger.warning(f"Timeout on attempt {attempt}/{self.max_retries}")
                time.sleep(self.retry_delay * attempt)
            except requests.exceptions.ConnectionError as e:
                last_error = f"Connection error: {e}"
                logger.warning(f"Connection error on attempt {attempt}: {e}")
                time.sleep(self.retry_delay * attempt)
            except requests.exceptions.HTTPError as e:
                logger.error(f"HTTP error: {e} | Response: {resp.text[:500]}")
                raise

        raise RuntimeError(f"PostBridge API failed after {self.max_retries} attempts: {last_error}")

    # ──────────────────── ACCOUNTS ────────────────────

    def get_social_accounts(self) -> list:
        """List all connected social accounts."""
        resp = self._request("GET", "/social-accounts")
        return resp.get("data", resp) if isinstance(resp, dict) else resp

    # ──────────────────── MEDIA ────────────────────

    def create_upload_url(self, name: str, mime_type: str, size_bytes: int) -> dict:
        """
        Step 1: Create a signed upload URL.
        Returns: {upload_url, media_id}
        """
        payload = {
            "name": name,
            "mime_type": mime_type,
            "size_bytes": size_bytes
        }
        return self._request("POST", "/media/create-upload-url", json=payload)

    def upload_to_signed_url(self, signed_url: str, file_path: str, mime_type: str) -> bool:
        """
        Step 2: PUT file to the signed URL.
        Returns True on success.
        """
        file_path = Path(file_path)
        size = file_path.stat().st_size

        logger.info(f"Uploading {file_path.name} ({size} bytes) to signed URL")

        for attempt in range(1, self.max_retries + 1):
            try:
                with open(file_path, "rb") as f:
                    resp = requests.put(
                        signed_url,
                        data=f,
                        headers={
                            "Content-Type": mime_type,
                            "Content-Length": str(size)
                        },
                        timeout=120  # Larger timeout for file uploads
                    )
                resp.raise_for_status()
                logger.info(f"Upload successful: {file_path.name}")
                return True
            except requests.exceptions.RequestException as e:
                logger.warning(f"Upload attempt {attempt} failed: {e}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * attempt)

        raise RuntimeError(f"Media upload failed after {self.max_retries} attempts: {file_path.name}")

    def upload_media(self, file_path: str) -> str:
        """
        Full media upload flow.
        Returns media_id to use in post creation.
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Media file not found: {file_path}")

        # Determine MIME type
        ext = file_path.suffix.lower()
        mime_map = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".mp4": "video/mp4",
            ".mov": "video/quicktime",
            ".gif": "image/gif"
        }
        mime_type = mime_map.get(ext, "application/octet-stream")
        size_bytes = file_path.stat().st_size

        logger.info(f"Starting media upload: {file_path.name} ({mime_type}, {size_bytes} bytes)")

        # Step 1: Get signed URL + media_id
        upload_info = self.create_upload_url(
            name=file_path.name,
            mime_type=mime_type,
            size_bytes=size_bytes
        )

        upload_url = upload_info.get("upload_url") or upload_info.get("url")
        media_id = upload_info.get("media_id") or upload_info.get("id")

        if not upload_url or not media_id:
            raise ValueError(f"Invalid upload URL response: {upload_info}")

        # Step 2: Upload file
        self.upload_to_signed_url(upload_url, str(file_path), mime_type)

        logger.info(f"Media uploaded successfully. media_id={media_id}")
        return str(media_id)

    # ──────────────────── POSTS ────────────────────

    def create_post(
        self,
        caption: str,
        social_account_ids: list,
        media_ids: Optional[list] = None,
        scheduled_at: Optional[str] = None
    ) -> dict:
        """
        Create a post on one or more accounts.

        Args:
            caption: Post caption text
            social_account_ids: List of social account IDs (strings)
            media_ids: List of media IDs (required for TikTok/Instagram)
            scheduled_at: ISO 8601 datetime string (None = immediate)

        Returns:
            API response dict with post ID
        """
        payload = {
            "caption": caption,
            "social_accounts": [str(aid) for aid in social_account_ids]
        }

        if media_ids:
            payload["media"] = [str(mid) for mid in media_ids]

        if scheduled_at:
            payload["scheduled_at"] = scheduled_at

        logger.info(f"Creating post on accounts {social_account_ids} | media={media_ids}")
        return self._request("POST", "/posts", json=payload)

    def get_posts(self, platform: Optional[str] = None, status: Optional[str] = None,
                  limit: int = 50) -> list:
        """List posts with optional filters."""
        params = {"limit": limit}
        if platform:
            params["platform"] = platform
        if status:
            params["status"] = status
        resp = self._request("GET", "/posts", params=params)
        return resp.get("data", resp) if isinstance(resp, dict) else resp

    def get_post_results(self, limit: int = 50) -> list:
        """Check success/failure of posts."""
        resp = self._request("GET", "/post-results", params={"limit": limit})
        return resp.get("data", resp) if isinstance(resp, dict) else resp

    # ──────────────────── ANALYTICS ────────────────────

    def get_analytics(self, account_id: Optional[str] = None,
                      start_date: Optional[str] = None,
                      end_date: Optional[str] = None) -> dict:
        """
        Fetch analytics data.
        Dates in YYYY-MM-DD format.
        """
        params = {}
        if account_id:
            params["account_id"] = account_id
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        return self._request("GET", "/analytics", params=params)

    def sync_analytics(self) -> dict:
        """Trigger analytics refresh for all platforms."""
        logger.info("Triggering analytics sync...")
        return self._request("POST", "/analytics/sync")


def get_client_from_config(config: dict) -> PostBridgeClient:
    """Instantiate client from config dict."""
    pb = config.get("postbridge", {})
    return PostBridgeClient(
        api_key=pb.get("api_key", ""),
        rate_limit=pb.get("rate_limit_rps", 10),
        timeout=pb.get("timeout_seconds", 30),
        max_retries=pb.get("retry_attempts", 3),
        retry_delay=pb.get("retry_delay_seconds", 2)
    )
