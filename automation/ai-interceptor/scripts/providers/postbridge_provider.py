"""
postbridge_provider.py — PostBridge Social Media Publishing Provider

Wraps the PostBridge API for scheduling and publishing social media posts.
API: https://api.post-bridge.com/v1
"""

from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests

from .base_provider import BaseProvider, ProviderCapability

logger = logging.getLogger(__name__)

POSTBRIDGE_API_BASE = "https://api.post-bridge.com/v1"


class PostBridgeProvider(BaseProvider):
    """
    PostBridge social media publishing provider.

    Config keys:
        api_key         (str)           — PostBridge API key (pb_live_...)
        base_url        (str)           — API base URL override
        social_accounts (list[int])     — default list of social account IDs
        default_delay_min (int)         — minutes to offset scheduled_at (default 5)
    """

    name = "postbridge"
    capabilities = [ProviderCapability.SOCIAL_POST]
    cost_per_call = {ProviderCapability.SOCIAL_POST: 0}  # no credit cost

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._api_key: str = self._config.get("api_key", os.getenv("POSTBRIDGE_API_KEY", ""))
        self._base_url: str = self._config.get("base_url", POSTBRIDGE_API_BASE)
        self._social_accounts: List[int] = self._config.get("social_accounts", [])
        self._delay_min: int = int(self._config.get("default_delay_min", 5))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

    def _post(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            resp = requests.post(
                f"{self._base_url}{endpoint}", json=payload, headers=self._headers(), timeout=30
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as exc:
            logger.error("PostBridge POST %s error: %s", endpoint, exc)
            return {"error": str(exc)}

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        try:
            resp = requests.get(
                f"{self._base_url}{endpoint}", params=params, headers=self._headers(), timeout=30
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as exc:
            logger.error("PostBridge GET %s error: %s", endpoint, exc)
            return {"error": str(exc)}

    def upload_media(self, file_path: str) -> Optional[str]:
        """
        Upload a media file to PostBridge and return the media_id.

        Args:
            file_path: Local path to the media file.

        Returns:
            str media_id or None on failure.
        """
        if not os.path.exists(file_path):
            logger.error("Media file not found: %s", file_path)
            return None
        try:
            # Step 1: Get upload URL
            ext = os.path.splitext(file_path)[1].lstrip(".").lower()
            mime_map = {"mp4": "video/mp4", "jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png"}
            mime = mime_map.get(ext, "application/octet-stream")

            resp = requests.post(
                f"{self._base_url}/media/create-upload-url",
                json={"content_type": mime, "filename": os.path.basename(file_path)},
                headers=self._headers(),
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            upload_url = data.get("upload_url", "")
            media_id = data.get("media_id", "")

            if not upload_url or not media_id:
                logger.error("PostBridge: no upload_url or media_id returned")
                return None

            # Step 2: Upload file
            with open(file_path, "rb") as fh:
                put_resp = requests.put(upload_url, data=fh, headers={"Content-Type": mime}, timeout=120)
                put_resp.raise_for_status()

            logger.info("PostBridge media uploaded: %s → %s", file_path, media_id)
            return media_id
        except Exception as exc:  # noqa: BLE001
            logger.error("PostBridge upload_media failed: %s", exc)
            return None

    # ------------------------------------------------------------------
    # BaseProvider interface
    # ------------------------------------------------------------------

    def generate(self, task_type: str, **kwargs: Any) -> Dict[str, Any]:
        """
        Publish or schedule a social media post via PostBridge.

        Args:
            task_type: "social_post"
            **kwargs:
                caption         (str)           — post caption/text
                social_accounts (list[int])     — account IDs to post to
                media_paths     (list[str])     — local media file paths (upload automatically)
                media_ids       (list[str])     — pre-uploaded media IDs (bypasses upload)
                scheduled_at    (str|datetime)  — ISO 8601 datetime or datetime object
                delay_minutes   (int)           — minutes from now if no scheduled_at
                platform_opts   (dict)          — per-platform extra options

        Returns:
            dict: success, output (post_id), cost, metadata, error
        """
        if not self.supports(task_type):
            return {
                "success": False, "output": None, "cost": 0, "metadata": {},
                "error": f"PostBridgeProvider does not support {task_type!r}",
            }

        caption: str = kwargs.get("caption", "")
        accounts: List[int] = kwargs.get("social_accounts", self._social_accounts)
        media_paths: List[str] = kwargs.get("media_paths", [])
        media_ids: List[str] = kwargs.get("media_ids", [])
        scheduled_at = kwargs.get("scheduled_at")
        delay_minutes: int = int(kwargs.get("delay_minutes", self._delay_min))
        platform_opts: Dict[str, Any] = kwargs.get("platform_opts", {})

        try:
            # Upload any local media files
            uploaded_ids = list(media_ids)
            for path in media_paths:
                mid = self.upload_media(path)
                if mid:
                    uploaded_ids.append(mid)

            # Build scheduled_at string
            if scheduled_at is None:
                from datetime import timedelta
                scheduled_at = (datetime.now(timezone.utc) + timedelta(minutes=delay_minutes)).isoformat()
            elif isinstance(scheduled_at, datetime):
                scheduled_at = scheduled_at.isoformat()

            payload: Dict[str, Any] = {
                "caption": caption,
                "social_accounts": accounts,
                "scheduled_at": scheduled_at,
            }
            if uploaded_ids:
                payload["media"] = [{"media_id": mid} for mid in uploaded_ids]
            if platform_opts:
                payload.update(platform_opts)

            resp = self._post("/posts", payload)
            if "error" in resp:
                return {"success": False, "output": None, "cost": 0, "metadata": {}, "error": resp["error"]}

            post_id = resp.get("id") or resp.get("post_id", "")
            return {
                "success": True,
                "output": post_id,
                "cost": 0,
                "metadata": {
                    "post_id": post_id,
                    "scheduled_at": scheduled_at,
                    "accounts": accounts,
                    "media_count": len(uploaded_ids),
                },
                "error": None,
            }
        except Exception as exc:  # noqa: BLE001
            logger.exception("PostBridgeProvider.generate() error: %s", exc)
            return {"success": False, "output": None, "cost": 0, "metadata": {}, "error": str(exc)}

    def get_accounts(self) -> List[Dict[str, Any]]:
        """Fetch all connected social accounts."""
        resp = self._get("/social-accounts")
        if "error" in resp:
            return []
        return resp.get("data", [])

    def check_credits(self) -> float:
        """PostBridge is subscription-based; return large sentinel value."""
        return 999999.0

    def is_available(self) -> bool:
        if not self._api_key:
            return False
        try:
            resp = requests.get(
                f"{self._base_url}/social-accounts", headers=self._headers(), timeout=10
            )
            return resp.status_code < 500
        except Exception:  # noqa: BLE001
            return False
