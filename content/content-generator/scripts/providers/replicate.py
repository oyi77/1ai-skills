"""Replicate provider for image generation.

This module provides the ReplicateProvider class for generating images
using Replicate's API with Flux and Stable Diffusion 3.5 models.
"""

import asyncio
import json
import os
import ssl
import urllib.error
import urllib.request
from typing import Optional

from .base import AIProvider, ProviderType, GenerationResult

# Default Replicate API base URL
DEFAULT_REPLICATE_BASE_URL = "https://api.replicate.com"

# Default image generation models
DEFAULT_IMAGE_MODEL = "flux-schnell"
SUPPORTED_IMAGE_MODELS = [
    "flux-schnell",
    "flux-dev",
    "sd3-5-medium",
]

# Cost estimates per image (USD)
MODEL_COSTS = {
    "flux-schnell": 0.003,
    "flux-dev": 0.055,
    "sd3-5-medium": 0.04,
}

# Model to Replicate model identifier mapping
MODEL_IDENTIFIERS = {
    "flux-schnell": "black-forest-labs/flux-schnell",
    "flux-dev": "black-forest-labs/flux-dev",
    "sd3-5-medium": "stability-ai/stable-diffusion-3-5-medium",
}


class ReplicateProvider(AIProvider):
    """Replicate provider for image generation.

    This provider uses Replicate's API to generate images using
    state-of-the-art Flux and Stable Diffusion models. It supports
    both synchronous (wait for completion) and asynchronous (webhook)
    generation modes.

    Attributes:
        provider_type: Always ProviderType.IMAGE for image generation
        provider_name: Human-readable name ("Replicate")
        api_key: Replicate API token for authentication
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs,
    ):
        """Initialize the Replicate provider.

        Args:
            api_key: Replicate API token (can also be set via REPLICATE_API_KEY env var)
            base_url: Custom API base URL (defaults to Replicate API endpoint)
            **kwargs: Additional configuration options
        """
        super().__init__(
            provider_type=ProviderType.IMAGE,
            provider_name="Replicate",
            api_key=api_key,
            **kwargs,
        )

        # Allow base_url override, default to Replicate API
        self.base_url = base_url or DEFAULT_REPLICATE_BASE_URL

        # Get API key from environment if not provided
        if not self.api_key:
            self.api_key = os.environ.get("REPLICATE_API_KEY")

    @property
    def supported_models(self) -> list[str]:
        """Get list of supported model identifiers.

        Returns:
            List of supported Replicate image generation models
        """
        return SUPPORTED_IMAGE_MODELS

    def _get_model_identifier(self, model: str) -> str:
        """Get the full Replicate model identifier.

        Args:
            model: Short model identifier (e.g., "flux-schnell")

        Returns:
            Full Replicate model identifier
        """
        return MODEL_IDENTIFIERS.get(model, model)

    def _build_headers(self) -> dict:
        """Build HTTP headers for Replicate API requests.

        Returns:
            Dictionary of HTTP headers
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token {self.api_key}",
        }
        return headers

    def _create_prediction(
        self,
        model: str,
        prompt: str,
        **kwargs,
    ) -> dict:
        """Create a prediction on Replicate.

        Args:
            model: Short model identifier
            prompt: Text prompt for image generation
            **kwargs: Additional generation parameters

        Returns:
            Prediction response from Replicate API

        Raises:
            urllib.error.HTTPError: On HTTP errors
            urllib.error.URLError: On network errors
        """
        full_model = self._get_model_identifier(model)

        # Build input payload
        input_params = {
            "prompt": prompt,
        }

        # Optional parameters
        if "aspect_ratio" in kwargs:
            input_params["aspect_ratio"] = kwargs["aspect_ratio"]
        if "width" in kwargs:
            input_params["width"] = kwargs["width"]
        if "height" in kwargs:
            input_params["height"] = kwargs["height"]
        if "num_outputs" in kwargs:
            input_params["num_outputs"] = kwargs["num_outputs"]
        if "seed" in kwargs:
            input_params["seed"] = kwargs["seed"]
        if "guidance_scale" in kwargs:
            input_params["guidance_scale"] = kwargs["guidance_scale"]
        if "num_inference_steps" in kwargs:
            input_params["num_inference_steps"] = kwargs["num_inference_steps"]
        if "prompt_strength" in kwargs:
            input_params["prompt_strength"] = kwargs["prompt_strength"]

        payload = {
            "version": full_model,
            "input": input_params,
        }

        # Add webhook for async mode
        if kwargs.get("webhook"):
            payload["webhook"] = kwargs["webhook"]
        if kwargs.get("webhook_events_filter"):
            payload["webhook_events_filter"] = kwargs["webhook_events_filter"]

        url = f"{self.base_url}/v1/predictions"
        headers = self._build_headers()

        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        ssl_context = ssl.create_default_context()

        with urllib.request.urlopen(
            request, context=ssl_context, timeout=60
        ) as response:
            return json.loads(response.read().decode("utf-8"))

    def _get_prediction(self, prediction_id: str) -> dict:
        """Get prediction status from Replicate.

        Args:
            prediction_id: ID of the prediction to check

        Returns:
            Prediction status from Replicate API

        Raises:
            urllib.error.HTTPError: On HTTP errors
            urllib.error.URLError: On network errors
        """
        url = f"{self.base_url}/v1/predictions/{prediction_id}"
        headers = self._build_headers()

        request = urllib.request.Request(url, headers=headers, method="GET")

        ssl_context = ssl.create_default_context()

        with urllib.request.urlopen(
            request, context=ssl_context, timeout=30
        ) as response:
            return json.loads(response.read().decode("utf-8"))

    async def _wait_for_completion(
        self,
        prediction_id: str,
        timeout: int = 300,
        poll_interval: int = 2,
    ) -> dict:
        """Wait for prediction to complete.

        Args:
            prediction_id: ID of the prediction to wait for
            timeout: Maximum time to wait in seconds
            poll_interval: Time between status checks in seconds

        Returns:
            Completed prediction from Replicate API

        Raises:
            TimeoutError: If prediction doesn't complete within timeout
            urllib.error.HTTPError: On HTTP errors
            urllib.error.URLError: On network errors
        """
        elapsed = 0
        while elapsed < timeout:
            prediction = self._get_prediction(prediction_id)
            status = prediction.get("status")

            if status == "succeeded":
                return prediction
            elif status == "failed":
                raise Exception(
                    f"Prediction failed: {prediction.get('error', 'Unknown error')}"
                )
            elif status == "canceled":
                raise Exception("Prediction was canceled")

            await asyncio.sleep(poll_interval)
            elapsed += poll_interval

        raise TimeoutError(f"Prediction timed out after {timeout} seconds")

    async def generate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> GenerationResult:
        """Generate an image based on the given prompt.

        Args:
            prompt: The text description for image generation
            model: Optional model identifier (defaults to flux-schnell)
            **kwargs: Additional parameters:
                - width: Image width
                - height: Image height
                - aspect_ratio: Image aspect ratio (e.g., "1:1", "16:9")
                - num_outputs: Number of images to generate (default 1)
                - seed: Random seed for reproducibility
                - guidance_scale: Guidance scale for generation
                - num_inference_steps: Number of inference steps
                - sync: If True, wait for completion (default True)
                - timeout: Max wait time for sync mode (default 300s)
                - webhook: Webhook URL for async mode

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
        aspect_ratio = kwargs.get("aspect_ratio")
        num_outputs = kwargs.get("num_outputs", 1)
        seed = kwargs.get("seed")
        guidance_scale = kwargs.get("guidance_scale")
        num_inference_steps = kwargs.get("num_inference_steps")
        sync = kwargs.get("sync", True)
        timeout = kwargs.get("timeout", 300)

        # Build parameters dict
        params = {}
        if width:
            params["width"] = width
        if height:
            params["height"] = height
        if aspect_ratio:
            params["aspect_ratio"] = aspect_ratio
        if num_outputs:
            params["num_outputs"] = num_outputs
        if seed is not None:
            params["seed"] = seed
        if guidance_scale is not None:
            params["guidance_scale"] = guidance_scale
        if num_inference_steps is not None:
            params["num_inference_steps"] = num_inference_steps

        try:
            # Create prediction
            prediction = self._create_prediction(model, prompt, **params)

            # Check for immediate errors
            if prediction.get("error"):
                return GenerationResult(
                    success=False,
                    data=None,
                    cost=0.0,
                    provider=self.provider_name,
                    model=model,
                    metadata={"error": prediction.get("error")},
                )

            prediction_id = prediction.get("id")
            if not prediction_id:
                return GenerationResult(
                    success=False,
                    data=None,
                    cost=0.0,
                    provider=self.provider_name,
                    model=model,
                    metadata={"error": "No prediction ID returned from API"},
                )

            status = prediction.get("status")

            # For async mode, return immediately with prediction ID
            if not sync or status == "processing":
                return GenerationResult(
                    success=True,
                    data={
                        "prediction_id": prediction_id,
                        "status": status,
                    },
                    cost=self.get_cost_estimate(prompt, model, **kwargs),
                    provider=self.provider_name,
                    model=model,
                    metadata={
                        "width": width,
                        "height": height,
                        "aspect_ratio": aspect_ratio,
                        "num_outputs": num_outputs,
                        "seed": seed,
                        "guidance_scale": guidance_scale,
                        "num_inference_steps": num_inference_steps,
                        "mode": "async",
                    },
                )

            # For sync mode, wait for completion
            if status == "succeeded":
                output = prediction.get("output", [])
            else:
                # Wait for the prediction to complete
                completed_prediction = await self._wait_for_completion(
                    prediction_id, timeout=timeout
                )
                output = completed_prediction.get("output", [])

            # Extract image URLs from output
            image_urls = []
            if isinstance(output, list):
                for item in output:
                    if isinstance(item, str):
                        image_urls.append(item)
                    elif isinstance(item, dict):
                        image_urls.append(item.get("url", item.get("image")))

            if not image_urls:
                return GenerationResult(
                    success=False,
                    data=None,
                    cost=self.get_cost_estimate(prompt, model, **kwargs),
                    provider=self.provider_name,
                    model=model,
                    metadata={"error": "No images returned from API"},
                )

            # Calculate cost
            cost = self.get_cost_estimate(prompt, model, **kwargs)

            return GenerationResult(
                success=True,
                data={
                    "urls": image_urls,
                    "images": image_urls,
                    "prediction_id": prediction_id,
                },
                cost=cost,
                provider=self.provider_name,
                model=model,
                metadata={
                    "width": width,
                    "height": height,
                    "aspect_ratio": aspect_ratio,
                    "num_outputs": len(image_urls),
                    "seed": seed,
                    "guidance_scale": guidance_scale,
                    "num_inference_steps": num_inference_steps,
                    "mode": "sync",
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
        except TimeoutError as e:
            return GenerationResult(
                success=False,
                data=None,
                cost=0.0,
                provider=self.provider_name,
                model=model,
                metadata={"error": str(e)},
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
        """Check if the Replicate provider is available.

        Performs a lightweight health check by verifying API key
        and attempting a minimal connectivity test.

        Returns:
            True if the provider is available, False otherwise
        """
        # First check if API key is configured
        if not self.validate_api_key():
            return False

        # Try a simple connectivity check
        test_url = f"{self.base_url}/v1/account"

        headers = self._build_headers()

        request = urllib.request.Request(test_url, headers=headers, method="GET")

        try:
            ssl_context = ssl.create_default_context()
            with urllib.request.urlopen(
                request, context=ssl_context, timeout=10
            ) as response:
                return response.status == 200
        except urllib.error.HTTPError:
            # If we get 401, the API key is invalid
            # Otherwise, assume available
            return self.validate_api_key()
        except Exception:
            # If we can't determine availability, assume available if API key is set
            return self.validate_api_key()

    def get_cost_estimate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> float:
        """Estimate the cost of an image generation operation.

        Args:
            prompt: The text description for image generation
            model: Optional model identifier
            **kwargs: Additional generation parameters:
                - num_outputs: Number of images to generate

        Returns:
            Estimated cost in USD
        """
        model = model or self.get_default_model()
        num_outputs = kwargs.get("num_outputs", 1)

        # Get base cost for the model
        base_cost = MODEL_COSTS.get(model, 0.003)

        # Calculate total cost
        return base_cost * num_outputs


# Export the provider
__all__ = ["ReplicateProvider"]
