"""GeminiGen AI image generation provider.

Primary image provider using Gemini 2.0 Flash via GeminiGen API.
Fastest option with free tier available.
"""

import os
import asyncio
import aiohttp
from typing import Optional

from .base import AIProvider, ProviderType, GenerationResult


class GeminiGenProvider(AIProvider):
    """GeminiGen image provider - Primary in fallback chain.

    Uses GeminiGen API (Gemini 2.0 Flash) for fast, cost-effective
    image generation with free tier support.
    """

    API_BASE = "https://api.geminigen.ai/uapi/v1"

    MODELS = {
        "nano-banana-pro": {"cost": 0.0, "description": "Free tier model"},
        "gemini-2.0-flash": {"cost": 0.001, "description": "Fast generation"},
    }

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        api_key = api_key or os.environ.get("GEMINIGEN_API_KEY", "")
        super().__init__(
            provider_type=ProviderType.IMAGE,
            provider_name="GeminiGen",
            api_key=api_key,
            **kwargs,
        )

    @property
    def supported_models(self) -> list[str]:
        return list(self.MODELS.keys())

    async def generate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> GenerationResult:
        model = model or self.get_default_model()
        if not self.validate_api_key():
            return GenerationResult(
                success=False,
                provider=self.provider_name,
                model=model,
                metadata={"error": "No API key configured"},
            )

        payload = {
            "model": model,
            "prompt": prompt,
            "aspect": kwargs.get("aspect", "9:16"),
            "style": kwargs.get("style", "Photorealistic"),
            "resolution": kwargs.get("resolution", "1K"),
        }

        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                }
                async with session.post(
                    f"{self.API_BASE}/generate-image",
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=60),
                ) as resp:
                    if resp.status == 429:
                        raise RateLimitError("GeminiGen rate limited")
                    if resp.status != 200:
                        body = await resp.text()
                        raise APIError(f"GeminiGen HTTP {resp.status}: {body}")

                    data = await resp.json()

                # If async task, poll for result
                if data.get("task_id"):
                    data = await self._wait_for_result(
                        session, headers, data["task_id"]
                    )

                image_url = (
                    data.get("image_url") or data.get("url") or data.get("output")
                )
                return GenerationResult(
                    success=bool(image_url),
                    data=image_url,
                    cost=self.MODELS.get(model, {}).get("cost", 0.0),
                    provider=self.provider_name,
                    model=model,
                    metadata={"raw_response": data},
                )

        except (RateLimitError, APIError):
            raise
        except Exception as e:
            return GenerationResult(
                success=False,
                provider=self.provider_name,
                model=model,
                metadata={"error": str(e)},
            )

    async def _wait_for_result(
        self,
        session: aiohttp.ClientSession,
        headers: dict,
        task_id: str,
        max_polls: int = 30,
        interval: float = 2.0,
    ) -> dict:
        """Poll for async task completion."""
        for _ in range(max_polls):
            async with session.get(
                f"{self.API_BASE}/task/{task_id}",
                headers=headers,
            ) as resp:
                result = await resp.json()
                status = result.get("status", "")
                if status in ("succeeded", "completed", "done"):
                    return result
                if status in ("failed", "error"):
                    raise APIError(f"GeminiGen task failed: {result}")
            await asyncio.sleep(interval)
        raise APIError("GeminiGen task timed out")

    async def is_available(self) -> bool:
        if not self.validate_api_key():
            return False
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.API_BASE,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as resp:
                    return resp.status < 500
        except Exception:
            return False

    def get_cost_estimate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> float:
        model = model or self.get_default_model()
        return self.MODELS.get(model, {}).get("cost", 0.001)


class RateLimitError(Exception):
    """Raised when a provider hits rate limits (HTTP 429)."""

    pass


class APIError(Exception):
    """Raised when a provider API returns an error."""

    pass
