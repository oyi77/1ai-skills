"""XAI Grok provider for video generation and vision analysis.

This module provides the XAIProvider class for generating videos and
analyzing images using xAI's Grok API.
"""

import json
import os
import ssl
import urllib.error
import urllib.request
from typing import Any, Optional

from .base import AIProvider, ProviderType, GenerationResult


# Default XAI API base URL
DEFAULT_XAI_BASE_URL = "https://api.x.ai/v1"

# Default models
DEFAULT_MODEL = "grok-vision-beta"

# Supported models
SUPPORTED_MODELS = [
    "grok-vision-beta",
    "grok-2-vision-1212",
    "grok-2-1212",
    # Video generation models (when available via Grok)
    # "grok-video",
]

# Cost estimates per request (USD) - placeholder values
MODEL_COSTS = {
    "grok-vision-beta": 0.002,
    "grok-2-vision-1212": 0.003,
    "grok-2-1212": 0.001,
}


class XAIProvider(AIProvider):
    """XAI Grok provider for video generation and vision analysis.

    This provider uses xAI's Grok API to generate videos and analyze images.
    Grok supports text-to-video, image-to-video, and vision analysis tasks.

    Attributes:
        provider_type: ProviderType.VIDEO for video generation
        provider_name: Human-readable name ("xAI Grok")
        api_key: XAI API key for authentication
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs,
    ):
        """Initialize the XAI provider.

        Args:
            api_key: XAI API key (can also be set via XAI_API_KEY env var)
            base_url: Custom API base URL (defaults to xAI endpoint)
            **kwargs: Additional configuration options
        """
        super().__init__(
            provider_type=ProviderType.VIDEO,
            provider_name="xAI Grok",
            api_key=api_key,
            **kwargs,
        )

        # Allow base_url override, default to xAI API
        self.base_url = base_url or DEFAULT_XAI_BASE_URL

        # Get API key from environment if not provided
        if not self.api_key:
            self.api_key = os.environ.get("XAI_API_KEY")

    @property
    def supported_models(self) -> list[str]:
        """Get list of supported model identifiers.

        Returns:
            List of supported xAI Grok models
        """
        return SUPPORTED_MODELS

    def _build_headers(self) -> dict:
        """Build HTTP headers for API requests.

        Returns:
            Dictionary of HTTP headers
        """
        headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _make_request(self, endpoint: str, payload: dict, method: str = "POST") -> dict:
        """Make HTTP request to XAI API.

        Args:
            endpoint: API endpoint URL
            payload: Request payload
            method: HTTP method (default: POST)

        Returns:
            Response data as dictionary

        Raises:
            urllib.error.HTTPError: On HTTP errors
            urllib.error.URLError: On network errors
        """
        headers = self._build_headers()

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            endpoint,
            data=data,
            headers=headers,
            method=method,
        )

        ssl_context = ssl.create_default_context()

        with urllib.request.urlopen(req, context=ssl_context, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))

    async def generate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> GenerationResult:
        """Generate video or analyze image based on the given prompt.

        Args:
            prompt: The text description for generation
            model: Optional model identifier (defaults to grok-vision-beta)
            **kwargs: Additional generation parameters:
                - image_url: str, optional image URL for vision or image-to-video
                - duration: int, video duration in seconds (default: 5)
                - fps: int, frames per second (default: 24)
                - resolution: str, video resolution (default: "1280x720")
                - mode: str, generation mode ("text-to-video", "image-to-video", "vision")
                - seed: int, random seed for reproducibility
                - num_frames: int, number of frames for video

        Returns:
            GenerationResult containing the generated content and metadata
        """
        # Use default model if not specified
        model = model or self.get_default_model()

        # Validate model
        if model not in self.supported_models:
            return GenerationResult(
                success=False,
                data=None,
                cost=0.0,
                provider=self.provider_name,
                model=model,
                metadata={"error": f"Unsupported model: {model}"},
            )

        # Validate API key
        if not self.validate_api_key():
            return GenerationResult(
                success=False,
                data=None,
                cost=0.0,
                provider=self.provider_name,
                model=model,
                metadata={"error": "API key not configured"},
            )

        # Extract generation parameters
        image_url = kwargs.get("image_url")
        duration = kwargs.get("duration", 5)
        fps = kwargs.get("fps", 24)
        resolution = kwargs.get("resolution", "1280x720")
        mode = kwargs.get("mode", "text-to-video")
        seed = kwargs.get("seed")
        num_frames = kwargs.get("num_frames")

        # Determine the operation mode
        # For vision models, we can do image analysis
        # For video models (when available), we can do text-to-video or image-to-video

        # Build the request based on mode
        if "vision" in model and image_url:
            # Vision analysis mode
            endpoint = f"{self.base_url}/chat/completions"
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": image_url},
                            },
                        ],
                    }
                ],
                "max_tokens": 1024,
            }
        elif image_url:
            # Image-to-video mode (when video generation is available)
            endpoint = f"{self.base_url}/video/generation"
            payload = {
                "model": model,
                "prompt": prompt,
                "image_url": image_url,
                "duration": duration,
                "fps": fps,
                "resolution": resolution,
            }
            if seed is not None:
                payload["seed"] = seed
            if num_frames is not None:
                payload["num_frames"] = num_frames
        else:
            # Text-to-video mode (when video generation is available)
            endpoint = f"{self.base_url}/video/generation"
            payload = {
                "model": model,
                "prompt": prompt,
                "duration": duration,
                "fps": fps,
                "resolution": resolution,
            }
            if seed is not None:
                payload["seed"] = seed
            if num_frames is not None:
                payload["num_frames"] = num_frames

        try:
            response = self._make_request(endpoint, payload)

            # Calculate cost
            cost = self.get_cost_estimate(prompt, model, **kwargs)

            # Parse response based on mode
            if "vision" in model and image_url:
                # Vision analysis response
                choices = response.get("choices", [])
                if choices:
                    content = choices[0].get("message", {}).get("content", "")
                    return GenerationResult(
                        success=True,
                        data={"analysis": content},
                        cost=cost,
                        provider=self.provider_name,
                        model=model,
                        metadata={
                            "mode": "vision",
                            "prompt": prompt,
                            "image_url": image_url,
                        },
                    )
                else:
                    return GenerationResult(
                        success=False,
                        data=None,
                        cost=cost,
                        provider=self.provider_name,
                        model=model,
                        metadata={"error": "No analysis returned from API"},
                    )
            else:
                # Video generation response
                video_data = response.get("data", {}) or response.get("video") or {}
                video_url = (
                    video_data.get("url")
                    or video_data.get("video_url")
                    or response.get("video_url")
                )
                task_id = video_data.get("task_id") or response.get("task_id")

                if video_url:
                    return GenerationResult(
                        success=True,
                        data={
                            "video_url": video_url,
                            "task_id": task_id,
                        },
                        cost=cost,
                        provider=self.provider_name,
                        model=model,
                        metadata={
                            "mode": mode,
                            "duration": duration,
                            "fps": fps,
                            "resolution": resolution,
                            "prompt": prompt,
                            "image_url": image_url,
                            "seed": seed,
                        },
                    )
                else:
                    return GenerationResult(
                        success=False,
                        data=None,
                        cost=cost,
                        provider=self.provider_name,
                        model=model,
                        metadata={
                            "error": "No video URL returned from API",
                            "response": response,
                        },
                    )

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else str(e)
            return GenerationResult(
                success=False,
                data=None,
                cost=0.0,
                provider=self.provider_name,
                model=model,
                metadata={
                    "error": f"HTTP {e.code}: {e.reason}",
                    "details": error_body,
                },
            )
        except urllib.error.URLError as e:
            return GenerationResult(
                success=False,
                data=None,
                cost=0.0,
                provider=self.provider_name,
                model=model,
                metadata={"error": f"Connection error: {e.reason}"},
            )
        except Exception as e:
            return GenerationResult(
                success=False,
                data=None,
                cost=0.0,
                provider=self.provider_name,
                model=model,
                metadata={"error": str(e)},
            )

    async def is_available(self) -> bool:
        """Check if the XAI Grok provider is available.

        Performs a lightweight health check by verifying API key
        and attempting a minimal connectivity test.

        Returns:
            True if the provider is available, False otherwise
        """
        # First check if API key is configured
        if not self.validate_api_key():
            return False

        # Try a simple connectivity check
        test_url = f"{self.base_url}/models"

        headers = self._build_headers()

        request = urllib.request.Request(test_url, headers=headers, method="GET")

        try:
            ssl_context = ssl.create_default_context()
            with urllib.request.urlopen(
                request, context=ssl_context, timeout=10
            ) as response:
                return response.status == 200
        except Exception:
            # If the models endpoint doesn't exist, assume available
            # as long as API key is valid
            return self.validate_api_key()

    def get_cost_estimate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> float:
        """Estimate the cost of a generation operation.

        Args:
            prompt: The text description for generation
            model: Optional model identifier
            **kwargs: Additional generation parameters:
                - duration: int, video duration in seconds (default: 5)
                - mode: str, generation mode

        Returns:
            Estimated cost in USD
        """
        model = model or self.get_default_model()
        duration = kwargs.get("duration", 5)
        mode = kwargs.get("mode", "text-to-video")

        # Get base cost for the model
        base_cost = MODEL_COSTS.get(model, 0.002)

        # For vision analysis, cost is per request
        if mode == "vision" or "vision" in model:
            return base_cost

        # For video generation, cost is based on duration
        # Video generation is typically more expensive
        video_cost = base_cost * duration * 10  # Video costs more per second

        # Image-to-video costs more than text-to-video
        if kwargs.get("image_url"):
            video_cost *= 1.5

        return round(video_cost, 4)


# Export the provider
__all__ = ["XAIProvider"]
