"""
flow_provider.py — Flow Video Generation Provider

Wraps the Flow (Stability AI / independent) video generation API.
Adjust FLOW_API_BASE for the actual service endpoint you use.
"""

from __future__ import annotations

import logging
import os
import time
from typing import Any, Dict, Optional

import requests

from .base_provider import BaseProvider, ProviderCapability

logger = logging.getLogger(__name__)

FLOW_API_BASE = os.getenv("FLOW_API_BASE", "https://api.flow.ai/v1")


class FlowProvider(BaseProvider):
    """
    Flow video generation provider.

    Config keys:
        api_key         (str)  — Flow API key
        base_url        (str)  — API base URL
        poll_interval   (int)  — seconds between polls (default 10)
        max_wait        (int)  — max wait seconds (default 600)
        output_dir      (str)  — directory for downloaded videos
    """

    name = "flow"
    capabilities = [
        ProviderCapability.TEXT2VIDEO,
        ProviderCapability.IMAGE2VIDEO,
    ]
    cost_per_call = {
        ProviderCapability.TEXT2VIDEO: 50,
        ProviderCapability.IMAGE2VIDEO: 100,
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._api_key: str = self._config.get("api_key", os.getenv("FLOW_API_KEY", ""))
        self._base_url: str = self._config.get("base_url", FLOW_API_BASE)
        self._poll_interval: int = int(self._config.get("poll_interval", 10))
        self._max_wait: int = int(self._config.get("max_wait", 600))
        self._output_dir: str = self._config.get("output_dir", "/tmp/flow_output")
        os.makedirs(self._output_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

    def _submit_job(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            resp = requests.post(
                f"{self._base_url}{endpoint}", json=payload, headers=self._headers(), timeout=30
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as exc:
            logger.error("Flow submit error: %s", exc)
            return {"error": str(exc)}

    def _poll_job(self, job_id: str) -> Dict[str, Any]:
        deadline = time.time() + self._max_wait
        while time.time() < deadline:
            try:
                resp = requests.get(
                    f"{self._base_url}/jobs/{job_id}",
                    headers=self._headers(),
                    timeout=15,
                )
                resp.raise_for_status()
                data = resp.json()
                status = data.get("status", "")
                if status in ("completed", "failed"):
                    return data
                logger.debug("Flow job %s status=%s", job_id, status)
                time.sleep(self._poll_interval)
            except requests.RequestException as exc:
                logger.error("Flow poll error: %s", exc)
                time.sleep(self._poll_interval)
        return {"error": f"Flow job {job_id} timed out"}

    def _download(self, url: str, job_id: str) -> str:
        filename = f"flow_{job_id}_{int(time.time())}.mp4"
        filepath = os.path.join(self._output_dir, filename)
        try:
            resp = requests.get(url, stream=True, timeout=120)
            resp.raise_for_status()
            with open(filepath, "wb") as fh:
                for chunk in resp.iter_content(8192):
                    fh.write(chunk)
            return filepath
        except Exception as exc:  # noqa: BLE001
            logger.error("Flow download failed: %s", exc)
            return url

    # ------------------------------------------------------------------
    # BaseProvider interface
    # ------------------------------------------------------------------

    def generate(self, task_type: str, **kwargs: Any) -> Dict[str, Any]:
        """
        Generate video via Flow.

        Args:
            task_type: "text2video" | "image2video"
            **kwargs:
                prompt      (str)  — text prompt
                image_path  (str)  — source image (image2video)
                duration    (int)  — seconds (default 5)
                resolution  (str)  — e.g. "1080p" (default "720p")

        Returns:
            dict: success, output, cost, metadata, error
        """
        if not self.supports(task_type):
            return {
                "success": False, "output": None, "cost": 0, "metadata": {},
                "error": f"FlowProvider does not support {task_type!r}",
            }

        prompt: str = kwargs.get("prompt", "")
        duration: int = int(kwargs.get("duration", 5))
        resolution: str = kwargs.get("resolution", "720p")
        image_path: str = kwargs.get("image_path", "")

        try:
            payload: Dict[str, Any] = {
                "prompt": prompt,
                "duration": duration,
                "resolution": resolution,
            }

            if task_type == ProviderCapability.IMAGE2VIDEO and image_path:
                import base64
                if os.path.exists(image_path):
                    with open(image_path, "rb") as fh:
                        payload["image"] = base64.b64encode(fh.read()).decode()

            endpoint = "/text2video" if task_type == ProviderCapability.TEXT2VIDEO else "/image2video"
            resp = self._submit_job(endpoint, payload)

            if "error" in resp:
                return {"success": False, "output": None, "cost": 0, "metadata": {}, "error": resp["error"]}

            job_id = resp.get("job_id", "")
            if not job_id:
                return {"success": False, "output": None, "cost": 0, "metadata": resp, "error": "No job_id"}

            result = self._poll_job(job_id)
            if "error" in result or result.get("status") == "failed":
                err = result.get("error") or result.get("failure_reason", "Job failed")
                return {"success": False, "output": None, "cost": 0, "metadata": result, "error": err}

            video_url = result.get("output_url", "")
            if not video_url:
                return {"success": False, "output": None, "cost": 0, "metadata": result, "error": "No output_url"}

            local_path = self._download(video_url, job_id)
            return {
                "success": True,
                "output": local_path,
                "cost": self.cost_per_call[task_type],
                "metadata": {"job_id": job_id, "video_url": video_url},
                "error": None,
            }
        except Exception as exc:  # noqa: BLE001
            logger.exception("FlowProvider.generate() error: %s", exc)
            return {"success": False, "output": None, "cost": 0, "metadata": {}, "error": str(exc)}

    def check_credits(self) -> float:
        """Fetch remaining Flow credits."""
        try:
            resp = requests.get(f"{self._base_url}/account", headers=self._headers(), timeout=10)
            resp.raise_for_status()
            return float(resp.json().get("credits", 0))
        except Exception:  # noqa: BLE001
            return 0.0

    def is_available(self) -> bool:
        if not self._api_key:
            return False
        try:
            resp = requests.get(f"{self._base_url}/health", headers=self._headers(), timeout=10)
            return resp.status_code < 500
        except Exception:  # noqa: BLE001
            return False
