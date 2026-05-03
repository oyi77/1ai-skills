"""
kling_provider.py — Kling AI Provider (video & image generation)

Wraps the Kling API for text-to-video and image-to-video generation.
API docs: https://klingai.com/api-docs
"""

from __future__ import annotations

import logging
import os
import time
from typing import Any, Dict, Optional

import requests

from .base_provider import BaseProvider, ProviderCapability

logger = logging.getLogger(__name__)

KLING_API_BASE = "https://api.klingai.com"
DEFAULT_POLL_INTERVAL = 10   # seconds between status polls
DEFAULT_MAX_WAIT = 600        # 10 minutes


class KlingProvider(BaseProvider):
    """
    Kling AI provider for text-to-video and image-to-video generation.

    Config keys:
        api_key         (str)  — Kling API key or cookie string
        cookie          (str)  — raw cookie header value (alternative to api_key)
        base_url        (str)  — override API base URL
        poll_interval   (int)  — seconds between status checks (default 10)
        max_wait        (int)  — max seconds to wait for generation (default 600)
        output_dir      (str)  — directory to save downloaded videos
    """

    name = "kling"
    capabilities = [
        ProviderCapability.TEXT2VIDEO,
        ProviderCapability.IMAGE2VIDEO,
        ProviderCapability.TEXT2IMAGE,
    ]
    cost_per_call = {
        ProviderCapability.TEXT2VIDEO: 60,
        ProviderCapability.IMAGE2VIDEO: 144,
        ProviderCapability.TEXT2IMAGE: 10,
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._api_key: str = self._config.get("api_key", os.getenv("KLING_API_KEY", ""))
        self._cookie: str = self._config.get("cookie", os.getenv("KLING_COOKIE", ""))
        self._base_url: str = self._config.get("base_url", KLING_API_BASE)
        self._poll_interval: int = int(self._config.get("poll_interval", DEFAULT_POLL_INTERVAL))
        self._max_wait: int = int(self._config.get("max_wait", DEFAULT_MAX_WAIT))
        self._output_dir: str = self._config.get("output_dir", "/tmp/kling_output")
        os.makedirs(self._output_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _headers(self) -> Dict[str, str]:
        headers: Dict[str, str] = {"Content-Type": "application/json"}
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"
        if self._cookie:
            headers["Cookie"] = self._cookie
        return headers

    def _post(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self._base_url}{endpoint}"
        try:
            resp = requests.post(url, json=payload, headers=self._headers(), timeout=30)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as exc:
            logger.error("Kling POST %s failed: %s", endpoint, exc)
            return {"error": str(exc)}

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        url = f"{self._base_url}{endpoint}"
        try:
            resp = requests.get(url, params=params, headers=self._headers(), timeout=30)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as exc:
            logger.error("Kling GET %s failed: %s", endpoint, exc)
            return {"error": str(exc)}

    def _poll_task(self, task_id: str, endpoint: str) -> Dict[str, Any]:
        """Poll a Kling task until completion or timeout."""
        deadline = time.time() + self._max_wait
        while time.time() < deadline:
            result = self._get(f"{endpoint}/{task_id}")
            if "error" in result:
                return result
            status = result.get("data", {}).get("task_status", "")
            if status in ("succeed", "failed"):
                return result
            logger.debug("Kling task %s: status=%s — waiting %ds", task_id, status, self._poll_interval)
            time.sleep(self._poll_interval)
        return {"error": f"Kling task {task_id} timed out after {self._max_wait}s"}

    def _download_video(self, url: str, task_id: str) -> str:
        """Download generated video to output_dir, return local path."""
        filename = f"kling_{task_id}_{int(time.time())}.mp4"
        filepath = os.path.join(self._output_dir, filename)
        try:
            resp = requests.get(url, stream=True, timeout=120)
            resp.raise_for_status()
            with open(filepath, "wb") as fh:
                for chunk in resp.iter_content(chunk_size=8192):
                    fh.write(chunk)
            logger.info("Kling video downloaded: %s", filepath)
            return filepath
        except Exception as exc:  # noqa: BLE001
            logger.error("Failed to download Kling video: %s", exc)
            return url  # fallback: return URL

    # ------------------------------------------------------------------
    # BaseProvider interface
    # ------------------------------------------------------------------

    def generate(self, task_type: str, **kwargs: Any) -> Dict[str, Any]:
        """
        Generate content via Kling AI.

        Args:
            task_type: "text2video" | "image2video" | "text2image"
            **kwargs:
                prompt      (str)  — text prompt (required for all)
                image_path  (str)  — local image path (required for image2video)
                duration    (str)  — "5" or "10" seconds (default "5")
                mode        (str)  — "std" | "pro" (default "std")
                aspect_ratio (str) — e.g. "16:9" (default "16:9")

        Returns:
            dict: success, output (local path), cost, metadata, error
        """
        if not self.supports(task_type):
            return {
                "success": False,
                "output": None,
                "cost": 0,
                "metadata": {},
                "error": f"KlingProvider does not support task_type={task_type!r}",
            }

        prompt: str = kwargs.get("prompt", "")
        duration: str = str(kwargs.get("duration", "5"))
        mode: str = kwargs.get("mode", "std")
        aspect_ratio: str = kwargs.get("aspect_ratio", "16:9")

        try:
            if task_type == ProviderCapability.TEXT2VIDEO:
                return self._text2video(prompt, duration, mode, aspect_ratio)
            elif task_type == ProviderCapability.IMAGE2VIDEO:
                image_path = kwargs.get("image_path", "")
                return self._image2video(prompt, image_path, duration, mode)
            elif task_type == ProviderCapability.TEXT2IMAGE:
                return self._text2image(prompt, aspect_ratio)
            else:
                return {"success": False, "output": None, "cost": 0, "metadata": {}, "error": "Unknown task_type"}
        except Exception as exc:  # noqa: BLE001
            logger.exception("KlingProvider.generate() error: %s", exc)
            return {"success": False, "output": None, "cost": 0, "metadata": {}, "error": str(exc)}

    def _text2video(self, prompt: str, duration: str, mode: str, aspect_ratio: str) -> Dict[str, Any]:
        payload = {
            "model_name": "kling-v1",
            "prompt": prompt,
            "duration": duration,
            "mode": mode,
            "aspect_ratio": aspect_ratio,
        }
        resp = self._post("/v1/videos/text2video", payload)
        if "error" in resp:
            return {"success": False, "output": None, "cost": 0, "metadata": {}, "error": resp["error"]}

        task_id = resp.get("data", {}).get("task_id", "")
        if not task_id:
            return {"success": False, "output": None, "cost": 0, "metadata": resp, "error": "No task_id returned"}

        result = self._poll_task(task_id, "/v1/videos/text2video")
        if "error" in result:
            return {"success": False, "output": None, "cost": 0, "metadata": {}, "error": result["error"]}

        video_url = (
            result.get("data", {})
            .get("task_result", {})
            .get("videos", [{}])[0]
            .get("url", "")
        )
        if not video_url:
            return {"success": False, "output": None, "cost": 0, "metadata": result, "error": "No video URL in result"}

        local_path = self._download_video(video_url, task_id)
        return {
            "success": True,
            "output": local_path,
            "cost": self.cost_per_call[ProviderCapability.TEXT2VIDEO],
            "metadata": {"task_id": task_id, "video_url": video_url, "mode": mode, "duration": duration},
            "error": None,
        }

    def _image2video(self, prompt: str, image_path: str, duration: str, mode: str) -> Dict[str, Any]:
        # In real usage, image would need to be uploaded first or sent as base64
        import base64

        image_b64 = ""
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as fh:
                image_b64 = base64.b64encode(fh.read()).decode()

        payload = {
            "model_name": "kling-v1",
            "prompt": prompt,
            "duration": duration,
            "mode": mode,
            "image": image_b64,
        }
        resp = self._post("/v1/videos/image2video", payload)
        if "error" in resp:
            return {"success": False, "output": None, "cost": 0, "metadata": {}, "error": resp["error"]}

        task_id = resp.get("data", {}).get("task_id", "")
        if not task_id:
            return {"success": False, "output": None, "cost": 0, "metadata": resp, "error": "No task_id returned"}

        result = self._poll_task(task_id, "/v1/videos/image2video")
        if "error" in result:
            return {"success": False, "output": None, "cost": 0, "metadata": {}, "error": result["error"]}

        video_url = (
            result.get("data", {})
            .get("task_result", {})
            .get("videos", [{}])[0]
            .get("url", "")
        )
        if not video_url:
            return {"success": False, "output": None, "cost": 0, "metadata": result, "error": "No video URL"}

        local_path = self._download_video(video_url, task_id)
        return {
            "success": True,
            "output": local_path,
            "cost": self.cost_per_call[ProviderCapability.IMAGE2VIDEO],
            "metadata": {"task_id": task_id, "video_url": video_url, "image_path": image_path},
            "error": None,
        }

    def _text2image(self, prompt: str, aspect_ratio: str) -> Dict[str, Any]:
        payload = {
            "model_name": "kling-v1",
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "n": 1,
        }
        resp = self._post("/v1/images/generations", payload)
        if "error" in resp:
            return {"success": False, "output": None, "cost": 0, "metadata": {}, "error": resp["error"]}

        task_id = resp.get("data", {}).get("task_id", "")
        if not task_id:
            return {"success": False, "output": None, "cost": 0, "metadata": resp, "error": "No task_id"}

        result = self._poll_task(task_id, "/v1/images/generations")
        images = result.get("data", {}).get("task_result", {}).get("images", [])
        if not images:
            return {"success": False, "output": None, "cost": 0, "metadata": result, "error": "No images returned"}

        image_url = images[0].get("url", "")
        return {
            "success": True,
            "output": image_url,
            "cost": self.cost_per_call[ProviderCapability.TEXT2IMAGE],
            "metadata": {"task_id": task_id, "images": images},
            "error": None,
        }

    def check_credits(self) -> float:
        """Query Kling API for remaining credits."""
        resp = self._get("/v1/account/credits")
        if "error" in resp:
            logger.warning("Could not fetch Kling credits: %s", resp["error"])
            return 0.0
        return float(resp.get("data", {}).get("remaining_credits", 0))

    def is_available(self) -> bool:
        """Return True if API key/cookie is configured and endpoint reachable."""
        if not (self._api_key or self._cookie):
            return False
        try:
            resp = requests.get(f"{self._base_url}/v1/account/credits", headers=self._headers(), timeout=10)
            return resp.status_code < 500
        except Exception:  # noqa: BLE001
            return False
