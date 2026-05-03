"""Runware provider for video generation.

Unified API gateway to 300K+ AI models via Runware Sonic Inference Engine.
Supports T2V, I2V, and video-to-video via WebSocket SDK.

Usage:
    provider = RunwareProvider(api_key="rw_...")
    result = await provider.generate("a cat running in the rain")
    print(result.data["video_url"])  # MP4 URL

Pricing (Seedance Lite):
    T2V: $0.14/clip (5s) — via Runware
    I2V: varies by model
"""

import os
import time
from typing import Optional

from .base import AIProvider, GenerationResult, ProviderType

RUNWARE_API_KEY_ENV = "RUNWARE_API_KEY"

DEFAULT_MODEL = "runware:100@1"
SUPPORTED_MODELS = [
    "runware:100@1",
    "runware:100@2",
    "runware:100@3",
    "runware:101@1",
    "runware:101@2",
    "runware:101@3",
    "runware:100@1.S",
    "runware:100@1.K",
]

COST_PER_CLIP = 0.14


class RunwareError(Exception):
    pass


class RunwareProvider(AIProvider):
    """Runware Sonic Inference Engine for video generation.

    Wraps the Runware WebSocket SDK. Uses Runware's unified API
    to access multiple video models (Seedance Lite, Kling, PixVerse, etc.)
    behind a single OpenAI-compatible-style interface.

    Supported models (model string format: "provider:model@version"):
        runware:100@1  — Seedance Lite (5s, 720p, T2V/I2V)
        runware:100@2  — Seedance Pro (10s, 1080p)
        runware:100@3  — Seedance Ultra
        runware:101@1  — PixVerse V4 (5s)
        runware:101@2  — PixVerse V4.5
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        timeout: int = 480,
        **kwargs,
    ):
        super().__init__(
            provider_type=ProviderType.VIDEO,
            provider_name="Runware",
            api_key=api_key,
            **kwargs,
        )
        self.api_key = api_key or os.environ.get(RUNWARE_API_KEY_ENV)
        self.model = model
        self.timeout = timeout
        self._client = None

    @property
    def supported_models(self) -> list[str]:
        return SUPPORTED_MODELS

    def _get_client(self):
        if self._client is None:
            try:
                from runware import Runware
            except ImportError:
                raise RunwareError("runware not installed. Run: pip install runware")
            if not self.api_key:
                raise RunwareError(
                    f"Runware API key not set. "
                    f"Set ${RUNWARE_API_KEY_ENV} env var or pass api_key='...'."
                )
            self._client = Runware(api_key=self.api_key, timeout=self.timeout * 1000)
        return self._client

    def _build_video_input(
        self,
        prompt: str,
        negative_prompt: str = "",
        seed: int = -1,
        duration: float = 5.0,
        width: int = 720,
        height: int = 1280,
        image: Optional[str] = None,
        steps: int = 25,
        cfg: float = 7.0,
        **kwargs,
    ):
        from runware import IVideoInference

        is_i2v = image is not None

        return IVideoInference(
            model=self.model,
            positivePrompt=prompt,
            negativePrompt=negative_prompt
            or "blurry, low quality, distorted, watermark",
            duration=duration,
            width=width,
            height=height,
            steps=steps,
            CFGScale=cfg,
            seed=seed if seed != -1 else None,
            frameImages=[image] if is_i2v else [],
            deliveryMethod="async",
            outputFormat="MP4",
            outputType="URL",
            includeCost=True,
            numberResults=1,
        )

    async def generate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> GenerationResult:
        if not self.validate_api_key():
            return GenerationResult(
                success=False,
                provider=self.provider_name,
                model=model or self.model,
                metadata={
                    "error": f"Set ${RUNWARE_API_KEY_ENV} env var or pass api_key='...'."
                },
            )

        duration = kwargs.get("duration", 5.0)
        image = kwargs.get("image")
        width = kwargs.get("width", 720)
        height = kwargs.get("height", 1280)
        negative_prompt = kwargs.get("negative_prompt", "")
        seed = kwargs.get("seed", -1)
        steps = kwargs.get("steps", 25)
        cfg = kwargs.get("cfg", 7.0)

        actual_model = model or self.model

        video_input = self._build_video_input(
            prompt=prompt,
            negative_prompt=negative_prompt,
            seed=seed,
            duration=duration,
            width=width,
            height=height,
            image=image,
            steps=steps,
            cfg=cfg,
        )

        try:
            client = self._get_client()
            result = await client.videoInference(requestVideo=video_input)

            if isinstance(result, list) and len(result) > 0:
                video = result[0]
                return GenerationResult(
                    success=True,
                    data={
                        "video_url": video.videoURL or video.mediaURL,
                        "video_uuid": video.videoUUID or video.mediaUUID,
                    },
                    cost=video.cost if video.cost else COST_PER_CLIP,
                    provider=self.provider_name,
                    model=actual_model,
                    metadata={
                        "prompt": prompt,
                        "duration": duration,
                        "seed": video.seed,
                        "i2v": image is not None,
                    },
                )
            else:
                return GenerationResult(
                    success=False,
                    provider=self.provider_name,
                    model=actual_model,
                    metadata={
                        "error": "No video returned from Runware",
                        "result": str(result),
                    },
                )

        except Exception as e:
            return GenerationResult(
                success=False,
                provider=self.provider_name,
                model=actual_model,
                metadata={"error": str(e)},
            )

    async def is_available(self) -> bool:
        if not self.validate_api_key():
            return False
        try:
            from runware import Runware

            test_client = Runware(api_key=self.api_key)
            return test_client is not None
        except Exception:
            return False

    def get_cost_estimate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> float:
        duration = kwargs.get("duration", 5.0)
        return round((duration / 5.0) * COST_PER_CLIP, 4)


__all__ = ["RunwareProvider", "RunwareError"]
