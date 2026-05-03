"""BytePlus ModelArk provider for video generation using Seedance.

This module provides the BytePlusProvider class for native video generation
through BytePlus ModelArk's Seedance API.

API Endpoints:
  - Create task: POST /contents/generations/tasks
  - Get task:    GET  /contents/generations/tasks/{task_id}

Base URL: https://ark.ap-southeast.bytepluses.com/api/v3
"""

import json
import os
import ssl
import time
import urllib.error
import urllib.request
from typing import Optional

from .base import AIProvider, GenerationResult, ProviderType


# Base URL for BytePlus ModelArk API
DEFAULT_BASE_URL = "https://ark.ap-southeast.bytepluses.com/api/v3"

# Seedance model versions
SEEDANCE_LITE_T2V = "seedance-1-0-lite-t2v-250428"
SEEDANCE_PRO_FAST = "seedance-1-0-pro-fast-251015"
SEEDANCE_PRO = "seedance-1-0-pro-250528"
SEEDANCE_PRO_15 = "seedance-1-5-pro-251215"

DEFAULT_MODEL = SEEDANCE_LITE_T2V

# Supported models
SUPPORTED_MODELS = [
    SEEDANCE_LITE_T2V,
    SEEDANCE_PRO_FAST,
    SEEDANCE_PRO,
    SEEDANCE_PRO_15,
]

# Cost per million tokens (USD)
MODEL_COSTS = {
    SEEDANCE_LITE_T2V: 1.0,
    SEEDANCE_PRO_FAST: 2.0,
    SEEDANCE_PRO: 2.5,
    SEEDANCE_PRO_15: 3.0,
}

# Task status values
STATUS_QUEUED = "queued"
STATUS_RUNNING = "running"
STATUS_SUCCEEDED = "succeeded"
STATUS_FAILED = "failed"
STATUS_CANCELLED = "cancelled"


class BytePlusProvider(AIProvider):
    """BytePlus ModelArk provider for video generation using Seedance.

    Uses async task-based API:
    1. Create task → get task_id
    2. Poll GET /contents/generations/tasks/{task_id}
    3. When status="succeeded", return content.video_url

    Supports text-to-video (T2V) and image-to-video (I2V).
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            provider_type=ProviderType.VIDEO,
            provider_name="BytePlus Seedance",
            api_key=api_key,
            **kwargs,
        )
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")

        if not self.api_key:
            self.api_key = os.environ.get("BYTEPLUS_API_KEY") or os.environ.get("ARK_API_KEY")

    @property
    def supported_models(self) -> list[str]:
        return SUPPORTED_MODELS

    def _make_request(self, method: str, path: str, body: Optional[dict] = None) -> dict:
        """Make authenticated HTTP request to BytePlus API."""
        url = f"{self.base_url}{path}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        data = json.dumps(body).encode("utf-8") if body else None
        req = urllib.request.Request(url, data=data, headers=headers, method=method)

        ssl_context = ssl.create_default_context()
        with urllib.request.urlopen(req, context=ssl_context, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def _create_task(self, model: str, content: list, **kwargs) -> str:
        """Create a video generation task. Returns task_id."""
        body = {
            "model": model,
            "content": content,
        }

        # Optional parameters (NOTE: do NOT include "resolution" — causes 400 error on lite model)
        for key in ["ratio", "duration", "seed", "watermark",
                    "camera_fixed", "generate_audio", "return_last_frame"]:
            if key in kwargs and kwargs[key] is not None:
                body[key] = kwargs[key]

        result = self._make_request("POST", "/contents/generations/tasks", body)
        task_id = result.get("id")
        if not task_id:
            raise ValueError(f"No task_id returned: {result}")
        return task_id

    def _poll_task(self, task_id: str, timeout: int = 300, interval: int = 5) -> dict:
        """Poll task until completed or timeout (seconds). Returns task result."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            result = self._make_request("GET", f"/contents/generations/tasks/{task_id}")
            status = result.get("status", "")

            if status == STATUS_SUCCEEDED:
                return result
            elif status in (STATUS_FAILED, STATUS_CANCELLED):
                error = result.get("error", {})
                raise RuntimeError(f"Task {status}: {error.get('message', 'Unknown error')} (code: {error.get('code', 'N/A')})")

            time.sleep(interval)

        raise TimeoutError(f"Task {task_id} timed out after {timeout}s")

    async def generate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> GenerationResult:
        """Generate video from text (or image) prompt.

        Args:
            prompt: Text description for video generation
            model: Seedance model ID (defaults to seedance-1-0-lite-t2v-250428)
            **kwargs:
                - image_url: str, for image-to-video (I2V mode)
                - resolution: str, e.g. "1280x720", "1920x1080"
                - ratio: str, e.g. "16:9", "9:16", "1:1"
                - duration: int, seconds (2-12 for pro, 5 for lite)
                - seed: int
                - poll_timeout: int, seconds to wait (default 300)

        Returns:
            GenerationResult with data["video_url"] on success
        """
        if not self.validate_api_key():
            return GenerationResult(
                success=False,
                provider=self.provider_name,
                model=model or DEFAULT_MODEL,
                metadata={"error": "API key not configured (set BYTEPLUS_API_KEY)"},
            )

        model = model or DEFAULT_MODEL
        poll_timeout = kwargs.pop("poll_timeout", 300)

        # Build content array
        content = [{"type": "text", "text": prompt}]

        # Add image for I2V if provided
        image_url = kwargs.pop("image_url", None)
        if image_url:
            content.append({
                "type": "image_url",
                "image_url": {"url": image_url},
                "role": "first_frame",
            })

        try:
            task_id = self._create_task(model, content, **kwargs)
            task_result = self._poll_task(task_id, timeout=poll_timeout)

            task_content = task_result.get("content", {})
            video_url = task_content.get("video_url", "")

            cost = self.get_cost_estimate(prompt, model)

            return GenerationResult(
                success=True,
                data={
                    "video_url": video_url,
                    "task_id": task_id,
                    "last_frame_url": task_content.get("last_frame_url", ""),
                    "duration": task_result.get("duration"),
                    "resolution": task_result.get("resolution"),
                    "ratio": task_result.get("ratio"),
                    "frames": task_result.get("frames"),
                    "fps": task_result.get("framespersecond"),
                    "seed": task_result.get("seed"),
                },
                cost=cost,
                provider=self.provider_name,
                model=model,
                metadata={
                    "prompt": prompt,
                    "revised_prompt": task_result.get("revised_prompt", ""),
                    "status": STATUS_SUCCEEDED,
                },
            )

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else str(e)
            return GenerationResult(
                success=False,
                provider=self.provider_name,
                model=model,
                metadata={"error": f"HTTP {e.code}: {error_body}"},
            )
        except (TimeoutError, RuntimeError) as e:
            return GenerationResult(
                success=False,
                provider=self.provider_name,
                model=model,
                metadata={"error": str(e)},
            )
        except Exception as e:
            return GenerationResult(
                success=False,
                provider=self.provider_name,
                model=model,
                metadata={"error": f"Unexpected error: {str(e)}"},
            )

    async def is_available(self) -> bool:
        """Check provider availability by listing recent tasks."""
        if not self.validate_api_key():
            return False
        try:
            self._make_request("GET", "/contents/generations/tasks?page_size=1")
            return True
        except urllib.error.HTTPError as e:
            # 400/404 still means the API is reachable and auth worked
            return e.code in (400, 404)
        except Exception:
            return False

    def get_cost_estimate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> float:
        model = model or DEFAULT_MODEL
        # Rough estimate: video generation uses ~10K tokens
        cost_per_m = MODEL_COSTS.get(model, 2.5)
        return round(cost_per_m * 10_000 / 1_000_000, 4)


__all__ = ["BytePlusProvider"]
