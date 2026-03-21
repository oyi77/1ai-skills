"""
pixverse_provider.py — PixVerse Video Generation Provider

Wraps the PixVerse API for AI video generation.
API: https://app.pixverse.ai (unofficial / reverse-engineered)
"""

from __future__ import annotations

import logging
import os
import time
from typing import Any, Dict, Optional

import requests

from .base_provider import BaseProvider, ProviderCapability

logger = logging.getLogger(__name__)

PIXVERSE_API_BASE = "https://app-api.pixverse.ai"


class PixVerseProvider(BaseProvider):
    """
    PixVerse video generation provider.

    Config keys:
        api_key         (str)  — PixVerse API/session token
        base_url        (str)  — API base URL override
        poll_interval   (int)  — seconds between status polls (default 10)
        max_wait        (int)  — max wait seconds (default 600)
        output_dir      (str)  — local download directory
        quality         (str)  — "360p" | "540p" | "720p" | "1080p" (default "720p")
    """

    name = "pixverse"
    capabilities = [
        ProviderCapability.TEXT2VIDEO,
        ProviderCapability.IMAGE2VIDEO,
    ]
    cost_per_call = {
        ProviderCapability.TEXT2VIDEO: 40,
        ProviderCapability.IMAGE2VIDEO: 80,
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._api_key: str = self._config.get("api_key", os.getenv("PIXVERSE_API_KEY", ""))
        self._base_url: str = self._config.get("base_url", PIXVERSE_API_BASE)
        self._poll_interval: int = int(self._config.get("poll_interval", 10))
        self._max_wait: int = int(self._config.get("max_wait", 600))
        self._output_dir: str = self._config.get("output_dir", "/tmp/pixverse_output")
        self._quality: str = self._config.get("quality", "720p")
        os.makedirs(self._output_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
            "User-Agent": "PixVerseClient/1.0",
        }

    def _create_video(self, payload: Dict[str, Any], endpoint: str) -> Dict[str, Any]:
        try:
            resp = requests.post(
                f"{self._base_url}{endpoint}",
                json=payload,
                headers=self._headers(),
                timeout=30,
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as exc:
            logger.error("PixVerse create error: %s", exc)
            return {"error": str(exc)}

    def _poll_video(self, video_id: str) -> Dict[str, Any]:
        deadline = time.time() + self._max_wait
        while time.time() < deadline:
            try:
                resp = requests.get(
                    f"{self._base_url}/creative/video/result/{video_id}",
                    headers=self._headers(),
                    timeout=15,
                )
                resp.raise_for_status()
                data = resp.json()
                status = data.get("ErrCode", -1)
                # 0 = success, 1 = processing, negative = error
                if status == 0:
                    return data
                if status < 0:
                    return {"error": f"PixVerse error code: {status}"}
                logger.debug("PixVerse video %s processing...", video_id)
                time.sleep(self._poll_interval)
            except requests.RequestException as exc:
                logger.error("PixVerse poll error: %s", exc)
                time.sleep(self._poll_interval)
        return {"error": f"PixVerse video {video_id} timed out"}

    def _download(self, url: str, video_id: str) -> str:
        filename = f"pixverse_{video_id}_{int(time.time())}.mp4"
        filepath = os.path.join(self._output_dir, filename)
        try:
            resp = requests.get(url, stream=True, timeout=120)
            resp.raise_for_status()
            with open(filepath, "wb") as fh:
                for chunk in resp.iter_content(8192):
                    fh.write(chunk)
            logger.info("PixVerse video downloaded: %s", filepath)
            return filepath
        except Exception as exc:  # noqa: BLE001
            logger.error("PixVerse download failed: %s", exc)
            return url

    # ------------------------------------------------------------------
    # BaseProvider interface
    # ------------------------------------------------------------------

    def generate(self, task_type: str, **kwargs: Any) -> Dict[str, Any]:
        """
        Generate video via PixVerse.

        Args:
            task_type: "text2video" | "image2video"
            **kwargs:
                prompt      (str)  — creative prompt
                image_path  (str)  — source image (image2video only)
                duration    (int)  — 4 | 8 (default 4)
                quality     (str)  — override default quality
                motion      (int)  — motion strength 1-10 (default 5)
                style       (str)  — "anime" | "3d_animation" | "clay" | "comic" | "" (default "")

        Returns:
            dict: success, output, cost, metadata, error
        """
        if not self.supports(task_type):
            return {
                "success": False, "output": None, "cost": 0, "metadata": {},
                "error": f"PixVerseProvider does not support {task_type!r}",
            }

        prompt: str = kwargs.get("prompt", "")
        duration: int = int(kwargs.get("duration", 4))
        quality: str = kwargs.get("quality", self._quality)
        motion: int = int(kwargs.get("motion", 5))
        style: str = kwargs.get("style", "")

        try:
            if task_type == ProviderCapability.TEXT2VIDEO:
                payload = {
                    "prompt": prompt,
                    "duration": duration,
                    "quality": quality,
                    "motion": motion,
                    "style": style,
                }
                resp = self._create_video(payload, "/creative/video/generate")
            else:  # image2video
                image_path: str = kwargs.get("image_path", "")
                image_id = self._upload_image(image_path)
                if not image_id:
                    return {"success": False, "output": None, "cost": 0, "metadata": {}, "error": "Image upload failed"}
                payload = {
                    "prompt": prompt,
                    "duration": duration,
                    "quality": quality,
                    "motion": motion,
                    "img_id": image_id,
                }
                resp = self._create_video(payload, "/creative/video/img/generate")

            if "error" in resp:
                return {"success": False, "output": None, "cost": 0, "metadata": {}, "error": resp["error"]}

            video_id = str(resp.get("Resp", {}).get("video_id", ""))
            if not video_id:
                return {"success": False, "output": None, "cost": 0, "metadata": resp, "error": "No video_id"}

            result = self._poll_video(video_id)
            if "error" in result:
                return {"success": False, "output": None, "cost": 0, "metadata": {}, "error": result["error"]}

            video_url = result.get("Resp", {}).get("url", "")
            if not video_url:
                return {"success": False, "output": None, "cost": 0, "metadata": result, "error": "No video URL"}

            local_path = self._download(video_url, video_id)
            return {
                "success": True,
                "output": local_path,
                "cost": self.cost_per_call[task_type],
                "metadata": {"video_id": video_id, "video_url": video_url, "quality": quality},
                "error": None,
            }
        except Exception as exc:  # noqa: BLE001
            logger.exception("PixVerseProvider.generate() error: %s", exc)
            return {"success": False, "output": None, "cost": 0, "metadata": {}, "error": str(exc)}

    def _upload_image(self, image_path: str) -> Optional[str]:
        """Upload an image to PixVerse and return the image_id."""
        if not image_path or not os.path.exists(image_path):
            return None
        try:
            with open(image_path, "rb") as fh:
                resp = requests.post(
                    f"{self._base_url}/creative/video/upload",
                    files={"file": fh},
                    headers={k: v for k, v in self._headers().items() if k != "Content-Type"},
                    timeout=60,
                )
                resp.raise_for_status()
                return str(resp.json().get("Resp", {}).get("img_id", ""))
        except Exception as exc:  # noqa: BLE001
            logger.error("PixVerse image upload failed: %s", exc)
            return None

    def check_credits(self) -> float:
        """Fetch remaining PixVerse credits."""
        try:
            resp = requests.get(
                f"{self._base_url}/user/account/info",
                headers=self._headers(),
                timeout=10,
            )
            resp.raise_for_status()
            return float(resp.json().get("Resp", {}).get("credits", 0))
        except Exception:  # noqa: BLE001
            return 0.0

    def is_available(self) -> bool:
        if not self._api_key:
            return False
        try:
            resp = requests.get(
                f"{self._base_url}/user/account/info",
                headers=self._headers(),
                timeout=10,
            )
            return resp.status_code < 500
        except Exception:  # noqa: BLE001
            return False
