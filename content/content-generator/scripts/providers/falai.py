"""Fal.ai image generation provider.

Quaternary image provider using Fal.ai's Flux models.
Reliable paid option when other providers are unavailable.
"""

import os
import asyncio
import aiohttp
from typing import Optional

from .base import AIProvider, ProviderType, GenerationResult
from .geminigen import RateLimitError, APIError


class FalAIProvider(AIProvider):
    """Fal.ai image provider - Quaternary in fallback chain.

    Uses Fal.ai serverless infrastructure for Flux model access.
    """

    API_BASE = "https://queue.fal.run"

    MODELS = {
        "flux-dev": {
            "endpoint": "fal-ai/flux/dev",
            "cost": 0.025,
        },
        "flux-schnell": {
            "endpoint": "fal-ai/flux/schnell",
            "cost": 0.003,
        },
        "flux-pro": {
            "endpoint": "fal-ai/flux-pro",
            "cost": 0.05,
        },
    }

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        api_key = api_key or os.environ.get("FAL_KEY", "")
        super().__init__(
            provider_type=ProviderType.IMAGE,
            provider_name="Fal.ai",
            api_key=api_key,
            **kwargs,
        )

    @property
    def supported_models(self) -> list[str]:
        return list(self.MODELS.keys())

    async def generate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> GenerationResult:
        model = model or "flux-schnell"
        model_config = self.MODELS.get(model)
        if not model_config:
            return GenerationResult(
                success=False,
                provider=self.provider_name,
                model=model,
                metadata={"error": f"Unknown model: {model}"},
            )

        if not self.validate_api_key():
            return GenerationResult(
                success=False,
                provider=self.provider_name,
                model=model,
                metadata={"error": "No API key configured"},
            )

        endpoint = model_config["endpoint"]
        payload = {
            "prompt": prompt,
            "image_size": kwargs.get("image_size", "portrait_16_9"),
            "num_images": kwargs.get("num_images", 1),
            "enable_safety_checker": kwargs.get("safety_checker", True),
        }
        if kwargs.get("seed") is not None:
            payload["seed"] = kwargs["seed"]

        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Key {self.api_key}",
                    "Content-Type": "application/json",
                }

                # Submit to queue
                async with session.post(
                    f"{self.API_BASE}/{endpoint}",
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as resp:
                    if resp.status == 429:
                        raise RateLimitError("Fal.ai rate limited")
                    if resp.status != 200:
                        body = await resp.text()
                        raise APIError(f"Fal.ai HTTP {resp.status}: {body}")
                    data = await resp.json()

                # Poll for result if queued
                request_id = data.get("request_id")
                if request_id:
                    data = await self._poll_result(
                        session, headers, endpoint, request_id
                    )

                images = data.get("images", [])
                image_url = images[0].get("url") if images else data.get("url")

                return GenerationResult(
                    success=bool(image_url),
                    data=image_url,
                    cost=model_config["cost"],
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

    async def _poll_result(
        self,
        session: aiohttp.ClientSession,
        headers: dict,
        endpoint: str,
        request_id: str,
        max_polls: int = 60,
        interval: float = 2.0,
    ) -> dict:
        """Poll queue for completed result."""
        status_url = f"{self.API_BASE}/{endpoint}/requests/{request_id}/status"
        result_url = f"https://queue.fal.run/{endpoint}/requests/{request_id}"

        for _ in range(max_polls):
            async with session.get(status_url, headers=headers) as resp:
                status_data = await resp.json()
                status = status_data.get("status", "")
                if status == "COMPLETED":
                    async with session.get(result_url, headers=headers) as result_resp:
                        return await result_resp.json()
                if status in ("FAILED", "ERROR"):
                    raise APIError(f"Fal.ai task failed: {status_data}")
            await asyncio.sleep(interval)
        raise APIError("Fal.ai task timed out")

    async def is_available(self) -> bool:
        if not self.validate_api_key():
            return False
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"Authorization": f"Key {self.api_key}"}
                async with session.get(
                    "https://queue.fal.run",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as resp:
                    return resp.status < 500
        except Exception:
            return False

    def get_cost_estimate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> float:
        model = model or "flux-schnell"
        return self.MODELS.get(model, {}).get("cost", 0.003)
