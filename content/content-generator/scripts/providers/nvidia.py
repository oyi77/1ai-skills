"""NVIDIA NIM provider for image generation.

This module provides the NVIDIAProvider class for generating images
using NVIDIA's NIM (NVIDIA Inference Microservice) API with Flux and
Stable Diffusion models.
"""

import json
import os
import ssl
import urllib.error
import urllib.request
from typing import Any, Optional

from .base import AIProvider, ProviderType, GenerationResult


# Default NVIDIA NIM API base URL for image generation (genai endpoint)
DEFAULT_NIM_BASE_URL = "https://ai.api.nvidia.com"

# Default image generation models (format: provider/model-id for genai endpoint)
DEFAULT_IMAGE_MODEL = "black-forest-labs/flux.1-dev"
SUPPORTED_IMAGE_MODELS = [
    "black-forest-labs/flux.1-dev",
    "black-forest-labs/flux_1-schnell",
    "stabilityai/stable-diffusion-xl",
    "stabilityai/stable-diffusion-3-medium",
    "stabilityai/stable-video-diffusion",
]

# Cost estimates per image (USD)
MODEL_COSTS = {
    "black-forest-labs/flux.1-dev": 0.004,
    "black-forest-labs/flux_1-schnell": 0.001,
    "stabilityai/stable-diffusion-xl": 0.002,
    "stabilityai/stable-diffusion-3-medium": 0.0025,
    "stabilityai/stable-video-diffusion": 0.005,
}


class NVIDIAProvider(AIProvider):
    """NVIDIA NIM provider for image generation.

    This provider uses NVIDIA's NIM API to generate images using
    state-of-the-art Flux and Stable Diffusion models.

    Attributes:
        provider_type: Always ProviderType.IMAGE for image generation
        provider_name: Human-readable name ("NVIDIA NIM")
        api_key: NVIDIA API key for authentication
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs,
    ):
        """Initialize the NVIDIA provider.

        Args:
            api_key: NVIDIA API key (can also be set via NVIDIA_API_KEY env var)
            base_url: Custom API base URL (defaults to NVIDIA NIM endpoint)
            **kwargs: Additional configuration options
        """
        super().__init__(
            provider_type=ProviderType.IMAGE,
            provider_name="NVIDIA NIM",
            api_key=api_key,
            **kwargs,
        )

        # Allow base_url override, default to NVIDIA NIM
        self.base_url = base_url or DEFAULT_NIM_BASE_URL

        # Get API key from environment if not provided
        if not self.api_key:
            self.api_key = os.environ.get("NVIDIA_API_KEY")

    @property
    def supported_models(self) -> list[str]:
        """Get list of supported model identifiers.

        Returns:
            List of supported NVIDIA NIM image generation models
        """
        return SUPPORTED_IMAGE_MODELS

    async def generate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> GenerationResult:
        """Generate an image based on the given prompt.

        Args:
            prompt: The text description for image generation
            model: Optional model identifier (defaults to flux-1.1-pro)
            **kwargs: Additional parameters:
                - width: Image width (default 1024)
                - height: Image height (default 1024)
                - num_images: Number of images to generate (default 1)
                - seed: Random seed for reproducibility
                - steps: Number of inference steps

        Returns:
            GenerationResult containing the generated image URL and metadata
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
        width = kwargs.get("width")
        height = kwargs.get("height")
        seed = kwargs.get("seed")
        steps = kwargs.get("steps")

        # Build minimal request payload (genai endpoint only needs prompt)
        payload = {"prompt": prompt}

        # Only add optional fields if explicitly provided
        if width is not None:
            payload["width"] = width
        if height is not None:
            payload["height"] = height
        if seed is not None:
            payload["seed"] = seed
        if steps is not None:
            payload["steps"] = steps

        # Build request URL - NVIDIA genai endpoint pattern: /v1/genai/{provider}/{model-id}
        url = f"{self.base_url}/v1/genai/{model}"

        # Create request with headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        try:
            # Create SSL context (handle cert verification)
            ssl_context = ssl.create_default_context()

            # Make the request
            with urllib.request.urlopen(
                request, context=ssl_context, timeout=120
            ) as response:
                response_data = json.loads(response.read().decode("utf-8"))

            # Extract image data from response
            # genai endpoint returns: {"artifacts": [{"finishReason": "SUCCESS", "base64": "...", "seed": ...}]}
            # fallback: standard OpenAI format {"data": [{"url": "...", "b64_json": "..."}]}
            artifacts = response_data.get("artifacts", [])
            images = response_data.get("data", []) or response_data.get("images", [])

            if artifacts:
                # genai endpoint format
                art = artifacts[0]
                image_base64 = art.get("base64")
                image_url = art.get("url")
                all_images = artifacts
            elif images:
                # OpenAI-compat format
                img = images[0] if isinstance(images, list) else images
                image_base64 = img.get("b64_json") or img.get("base64") if isinstance(img, dict) else None
                image_url = img.get("url") if isinstance(img, dict) else None
                all_images = images
            else:
                return GenerationResult(
                    success=False,
                    data=None,
                    cost=self.get_cost_estimate(prompt, model),
                    provider=self.provider_name,
                    model=model,
                    metadata={"error": f"No images returned from API. Response: {response_data}"},
                )

            # Prepare result data
            result_data = {
                "url": image_url,
                "base64": image_base64,
                "images": all_images,
            }

            # Calculate cost
            cost = self.get_cost_estimate(prompt, model)

            return GenerationResult(
                success=True,
                data=result_data,
                cost=cost,
                provider=self.provider_name,
                model=model,
                metadata={
                    "width": width,
                    "height": height,
                    "seed": seed,
                    "steps": steps,
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
        """Check if the NVIDIA NIM provider is available.

        Performs a lightweight health check by verifying API key
        and attempting a minimal connectivity test.

        Returns:
            True if the provider is available, False otherwise
        """
        # First check if API key is configured
        if not self.validate_api_key():
            return False

        # Try a simple connectivity check
        test_url = f"{self.base_url}/v1/models"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

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
        """Estimate the cost of an image generation operation.

        Args:
            prompt: The text description for image generation
            model: Optional model identifier
            **kwargs: Additional generation parameters

        Returns:
            Estimated cost in USD
        """
        model = model or self.get_default_model()
        # Get base cost for the model (per image)
        base_cost = MODEL_COSTS.get(model, 0.003)
        return base_cost


# Export the provider
__all__ = ["NVIDIAProvider"]
