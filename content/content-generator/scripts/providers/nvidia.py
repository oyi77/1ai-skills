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


# Default NVIDIA NIM API base URL
DEFAULT_NIM_BASE_URL = "https://integrate.api.nvidia.com"

# Default image generation models
DEFAULT_IMAGE_MODEL = "nvidia/flux-1.1-pro"
SUPPORTED_IMAGE_MODELS = [
    "nvidia/flux-1.1-pro",
    "nvidia/flux-1.1-dev",
    "nvidia/flux-1-schnell",
    "nvidia/stable-diffusion-xl-1024-v1-0",
    "nvidia/stable-diffusion-3-medium",
]

# Cost estimates per image (USD)
MODEL_COSTS = {
    "nvidia/flux-1.1-pro": 0.003,
    "nvidia/flux-1.1-dev": 0.004,
    "nvidia/flux-1-schnell": 0.001,
    "nvidia/stable-diffusion-xl-1024-v1-0": 0.002,
    "nvidia/stable-diffusion-3-medium": 0.0025,
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
        width = kwargs.get("width", 1024)
        height = kwargs.get("height", 1024)
        num_images = kwargs.get("num_images", 1)
        seed = kwargs.get("seed")
        steps = kwargs.get("steps")

        # Build request payload
        payload = {
            "prompt": prompt,
            "width": width,
            "height": height,
            "num_images": num_images,
        }

        if seed is not None:
            payload["seed"] = seed
        if steps is not None:
            payload["steps"] = steps

        # Build request URL
        url = f"{self.base_url}/v1/images/generation/{model}"

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
            images = response_data.get("data", [])
            if not images:
                # Try alternative response format
                images = response_data.get("images", [])

            if not images:
                return GenerationResult(
                    success=False,
                    data=None,
                    cost=self.get_cost_estimate(prompt, model),
                    provider=self.provider_name,
                    model=model,
                    metadata={"error": "No images returned from API"},
                )

            # Get the first image (or list of images)
            image_data = images[0] if len(images) == 1 else images

            # Extract image URL or base64 data
            image_url = (
                image_data.get("url") if isinstance(image_data, dict) else image_data
            )
            image_base64 = (
                image_data.get("base64") if isinstance(image_data, dict) else None
            )

            # Prepare result data
            result_data = {
                "url": image_url,
                "base64": image_base64,
                "images": images,
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
                    "num_images": len(images) if isinstance(images, list) else 1,
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
        num_images = kwargs.get("num_images", 1)

        # Get base cost for the model
        base_cost = MODEL_COSTS.get(model, 0.003)

        # Calculate total cost
        return base_cost * num_images


# Export the provider
__all__ = ["NVIDIAProvider"]
