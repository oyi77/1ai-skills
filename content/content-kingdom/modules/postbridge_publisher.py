"""
Module 9: PostBridgePublisher
Direct PostBridge API client — no external dependencies.

Provides:
  - health_check()
  - create_post() / get_accounts() / upload_media()
  - retry_failed_posts()
  - delete_post()
  - get_analytics() / sync_analytics()
"""

import json
import logging
import os
import time
import urllib.error
import urllib.request
import ssl
from datetime import datetime, timezone, timedelta
from typing import Optional, List

from .base import BaseModule

logger = logging.getLogger("content_kingdom.postbridge")

API_BASE = "https://api.post-bridge.com/v1"


class PostBridgeClient:
    """Thin HTTP client for PostBridge API. No external deps (uses urllib)."""

    def __init__(self, api_key: str, rate_limit: float = 10.0, max_retries: int = 3):
        self.api_key = api_key
        self.rate_limit = rate_limit
        self.max_retries = max_retries
        self._ctx = ssl.create_default_context()
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def _request(self, method: str, path: str, data: dict | None = None,
                 params: dict | None = None) -> dict | list:
        url = f"{API_BASE}{path}"
        if params:
            qs = "&".join(f"{k}={v}" for k, v in params.items())
            url = f"{url}?{qs}"

        body = json.dumps(data).encode() if data else None
        req = urllib.request.Request(url, data=body, method=method, headers=self._headers)

        for attempt in range(self.max_retries):
            try:
                with urllib.request.urlopen(req, timeout=30, context=self._ctx) as resp:
                    return json.loads(resp.read())
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt < self.max_retries - 1:
                    time.sleep(1.0 / self.rate_limit)
                    continue
                raise
            except Exception:
                if attempt < self.max_retries - 1:
                    time.sleep(0.5)
                    continue
                raise
        return {}

    def get_social_accounts(self, limit: int = 100) -> list:
        resp = self._request("GET", "/social-accounts", params={"limit": limit})
        if isinstance(resp, dict):
            return resp.get("data", [])
        return resp

    def create_post(self, caption: str, social_account_ids: list,
                    media_ids: list | None = None, scheduled_at: str | None = None) -> dict:
        payload = {"caption": caption, "social_accounts": social_account_ids}
        if media_ids:
            payload["media"] = media_ids
        if scheduled_at:
            payload["scheduled_at"] = scheduled_at
        resp = self._request("POST", "/posts", data=payload)
        return resp if isinstance(resp, dict) else {}

    def get_posts(self, status: str | None = None, limit: int = 50) -> list:
        params = {"limit": limit}
        if status:
            params["status"] = status
        resp = self._request("GET", "/posts", params=params)
        if isinstance(resp, dict):
            return resp.get("data", [])
        return resp

    def get_post_results(self, limit: int = 50) -> list:
        resp = self._request("GET", "/post-results", params={"limit": limit})
        if isinstance(resp, dict):
            return resp.get("data", [])
        return resp

    def upload_media(self, file_path: str) -> str:
        """Upload file to PostBridge, return media_id."""
        name = os.path.basename(file_path)
        size = os.path.getsize(file_path)
        ext = name.rsplit(".", 1)[-1].lower()
        mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
                "mp4": "video/mp4", "gif": "image/gif"}.get(ext, "application/octet-stream")

        resp = self._request("POST", "/media/create-upload-url",
                             data={"name": name, "mime_type": mime, "size_bytes": size})
        upload_url = resp.get("upload_url", "")
        media_id = resp.get("media_id", "")
        if not upload_url:
            raise ValueError(f"No upload_url in response: {resp}")

        with open(file_path, "rb") as f:
            put_req = urllib.request.Request(upload_url, data=f.read(), method="PUT",
                                            headers={"Content-Type": mime})
            urllib.request.urlopen(put_req, timeout=60, context=self._ctx)

        return media_id

    def get_analytics(self, start_date: str, end_date: str) -> dict:
        resp = self._request("GET", "/analytics",
                             params={"start_date": start_date, "end_date": end_date})
        return resp if isinstance(resp, dict) else {}

    def sync_analytics(self) -> dict:
        resp = self._request("POST", "/analytics/sync")
        return resp if isinstance(resp, dict) else {}


class PostBridgePublisher(BaseModule):
    """
    Unified PostBridge posting interface.

    Usage:
        from modules.base import load_config
        cfg = load_config()
        pub = PostBridgePublisher(cfg)
        print(pub.health_check())
    """

    def __init__(self, config: dict):
        super().__init__(config)
        api_key = config.get("postbridge_api_key", "")
        if not api_key:
            raise ValueError("postbridge_api_key missing from config")
        self._client = PostBridgeClient(api_key=api_key, rate_limit=10.0, max_retries=3)

    def get_accounts(self) -> list:
        return self._client.get_social_accounts()

    def upload_media(self, file_path: str, mime_type: Optional[str] = None) -> str:
        return self._client.upload_media(file_path)

    def create_post(self, caption: str, media_ids: Optional[List[str]] = None,
                    account_ids: Optional[List[str]] = None,
                    scheduled_at: Optional[str] = None) -> dict:
        return self._client.create_post(
            caption=caption, social_account_ids=account_ids or [],
            media_ids=media_ids or [], scheduled_at=scheduled_at)

    def get_scheduled_posts(self, limit: int = 50) -> list:
        return self._client.get_posts(status="scheduled", limit=limit)

    def get_post_results(self, limit: int = 50) -> list:
        return self._client.get_post_results(limit=limit)

    def delete_post(self, post_id: str) -> dict:
        return self._client._request("DELETE", f"/posts/{post_id}")

    def get_analytics(self, days: int = 7) -> dict:
        end = datetime.now(timezone.utc)
        start = end - timedelta(days=days)
        return self._client.get_analytics(
            start_date=start.strftime("%Y-%m-%d"), end_date=end.strftime("%Y-%m-%d"))

    def sync_analytics(self) -> dict:
        return self._client.sync_analytics()

    def health_check(self) -> dict:
        t0 = time.monotonic()
        try:
            accounts = self.get_accounts()
            ms = round((time.monotonic() - t0) * 1000, 1)
            n = len(accounts) if isinstance(accounts, list) else 0
            return {"status": "ok", "latency_ms": ms, "accounts_count": n,
                    "message": f"{n} account(s) connected"}
        except Exception as e:
            ms = round((time.monotonic() - t0) * 1000, 1)
            return {"status": "error", "latency_ms": ms, "accounts_count": 0,
                    "message": str(e)}

    def retry_failed_posts(self, hours: int = 24) -> dict:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        results = self.get_post_results(limit=100)
        found = retried = failed = 0
        details = []

        for r in results:
            if r.get("success", True):
                continue
            found += 1
            post = r.get("post") or {}
            caption = post.get("caption", "")
            media_ids = [m.get("media_id") or m.get("id") for m in post.get("media", [])]
            account_ids = [a.get("id") for a in post.get("social_accounts", [])]
            if not caption or not account_ids:
                details.append({"id": r.get("id"), "status": "skipped", "reason": "missing data"})
                continue
            try:
                new = self.create_post(caption=caption, media_ids=media_ids or None,
                                       account_ids=account_ids)
                retried += 1
                details.append({"id": r.get("id"), "new_id": new.get("id"), "status": "retried"})
            except Exception as e:
                failed += 1
                details.append({"id": r.get("id"), "status": "retry_failed", "error": str(e)})

        return {"found": found, "retried": retried, "failed": failed, "details": details}
