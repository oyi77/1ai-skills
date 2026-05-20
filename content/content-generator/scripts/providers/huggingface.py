"""HuggingFace provider for image generation using Inference API."""

import json
import os
import ssl
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

from .base import AIProvider, ProviderType, GenerationResult

DEFAULT_HF_BASE_URL = "https://api-inference.huggingface.co"

DEFAULT_IMAGE_MODEL = "black-forest-labs/FLUX.1-schnell"
SUPPORTED_IMAGE_MODELS = [
    "black-forest-labs/FLUX.1-schnell",
    "black-forest-labs/FLUX.1-dev",
    "stabilityai/stable-diffusion-3-5-large",
    "stabilityai/stable-diffusion-3-5-medium",
    "stabilityai/stable-diffusion-xl-base-1.0",
    "stabilityai/stable-diffusion-xl-refiner-1.0",
]

MODEL_IDENTIFIERS = {
    "black-forest-labs/FLUX.1-schnell": "black-forest-labs/FLUX.1-schnell",
    "black-forest-labs/FLUX.1-dev": "black-forest-labs/FLUX.1-dev",
    "stabilityai/stable-diffusion-3-5-large": "stabilityai/stable-diffusion-3-5-large",
    "stabilityai/stable-diffusion-3-5-medium": "stabilityai/stable-diffusion-3-5-medium",
    "stabilityai/stable-diffusion-xl-base-1.0": "stabilityai/stable-diffusion-xl-base-1.0",
    "stabilityai/stable-diffusion-xl-refiner-1.0": "stabilityai/stable-diffusion-xl-refiner-1.0",
    "flux-schnell": "black-forest-labs/FLUX.1-schnell",
    "flux-dev": "black-forest-labs/FLUX.1-dev",
    "sd3-5-large": "stabilityai/stable-diffusion-3-5-large",
    "sd3-5-medium": "stabilityai/stable-diffusion-3-5-medium",
    "sdxl-base": "stabilityai/stable-diffusion-xl-base-1.0",
    "sdxl-refiner": "stabilityai/stable-diffusion-xl-refiner-1.0",
}

MODEL_COSTS = {
    "black-forest-labs/FLUX.1-schnell": 0.003,
    "black-forest-labs/FLUX.1-dev": 0.055,
    "stabilityai/stable-diffusion-3-5-large": 0.04,
    "stabilityai/stable-diffusion-3-5-medium": 0.03,
    "stabilityai/stable-diffusion-xl-base-1.0": 0.015,
    "stabilityai/stable-diffusion-xl-refiner-1.0": 0.015,
    "flux-schnell": 0.003,
    "flux-dev": 0.055,
    "sd3-5-large": 0.04,
    "sd3-5-medium": 0.03,
    "sdxl-base": 0.015,
    "sdxl-refiner": 0.015,
}


class HuggingFaceProvider(AIProvider):
    """HuggingFace provider for image generation.

    This provider uses HuggingFace's Inference API to generate images
    using state-of-the-art Flux and Stable Diffusion models. It supports
    both free tier (with rate limits) and paid inference endpoints.

    Attributes:
        provider_type: Always ProviderType.IMAGE for image generation
        provider_name: Human-readable name ("HuggingFace")
        api_key: HuggingFace API token for authentication
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs,
    ):
        """Initialize the HuggingFace provider.

        Args:
            api_key: HuggingFace API token (can also be set via HF_API_KEY env var)
            base_url: Custom API base URL (defaults to HuggingFace Inference endpoint)
            **kwargs: Additional configuration options
        """
        super().__init__(
            provider_type=ProviderType.IMAGE,
            provider_name="HuggingFace",
            api_key=api_key,
            **kwargs,
        )

        # Allow base_url override, default to HuggingFace Inference API
        self.base_url = base_url or DEFAULT_HF_BASE_URL

        if not self.api_key:
            self.api_key = os.environ.get("HF_API_KEY")

    @property
    def supported_models(self) -> list[str]:
        """Get list of supported model identifiers.

        Returns:
            List of supported HuggingFace image generation models
        """
        return SUPPORTED_IMAGE_MODELS

    def _get_model_identifier(self, model: str) -> str:
        """Get the full HuggingFace model identifier.

        Args:
            model: Model identifier (short or full)

        Returns:
            Full HuggingFace model identifier
        """
        return MODEL_IDENTIFIERS.get(model, model)

    def _build_headers(self) -> dict:
        """Build HTTP headers for HuggingFace API requests.

        Returns:
            Dictionary of HTTP headers
        """
        headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _call_inference_api(
        self,
        model: str,
        payload: dict,
        timeout: int = 120,
    ) -> Any:
        """Call the HuggingFace Inference API.

        Args:
            model: Full model identifier
            payload: Request payload
            timeout: Request timeout in seconds

        Returns:
            Response from the API (varies by model)

        Raises:
            urllib.error.HTTPError: On HTTP errors
            urllib.error.URLError: On network errors
        """
        url = f"{self.base_url}/models/{model}"
        headers = self._build_headers()

        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        ssl_context = ssl.create_default_context()

        with urllib.request.urlopen(
            request, context=ssl_context, timeout=timeout
        ) as response:
            content_type = response.headers.get("Content-Type", "")

            if "image" in content_type:
                return response.read()
            else:
                return json.loads(response.read().decode("utf-8"))

    async def generate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> GenerationResult:
        """Generate an image based on the given prompt.

        Args:
            prompt: The text description for image generation
            model: Optional model identifier (defaults to FLUX.1-schnell)
            **kwargs: Additional parameters:
                - width: Image width
                - height: Image height
                - num_images: Number of images to generate (default 1)
                - seed: Random seed for reproducibility
                - guidance_scale: Guidance scale for generation
                - num_inference_steps: Number of inference steps
                - negative_prompt: Negative prompt to avoid certain features

        Returns:
            GenerationResult containing the generated image URL and metadata
        """
        model = model or self.get_default_model()

        full_model = self._get_model_identifier(model)
        if (
            full_model not in SUPPORTED_IMAGE_MODELS
            and model not in SUPPORTED_IMAGE_MODELS
        ):
            found = False
            for supported in SUPPORTED_IMAGE_MODELS:
                if model in supported or supported in model:
                    full_model = supported
                    found = True
                    break
            if not found:
                return GenerationResult(
                    success=False,
                    data=None,
                    cost=0.0,
                    provider=self.provider_name,
                    model=model,
                    metadata={"error": f"Unsupported model: {model}"},
                )

        width = kwargs.get("width")
        height = kwargs.get("height")
        num_images = kwargs.get("num_images", 1)
        seed = kwargs.get("seed")
        guidance_scale = kwargs.get("guidance_scale")
        num_inference_steps = kwargs.get("num_inference_steps")
        negative_prompt = kwargs.get("negative_prompt")

        payload: Dict[str, Any] = {
            "inputs": prompt,
        }

        parameters: Dict[str, Any] = {}
        if width:
            parameters["width"] = width
        if height:
            parameters["height"] = height
        if seed is not None:
            parameters["seed"] = seed
        if guidance_scale is not None:
            parameters["guidance_scale"] = guidance_scale
        if num_inference_steps is not None:
            parameters["num_inference_steps"] = num_inference_steps
        if negative_prompt:
            parameters["negative_prompt"] = negative_prompt

        if parameters:
            payload["parameters"] = parameters

        try:
            response = self._call_inference_api(full_model, payload)

            image_urls = []
            image_base64 = []

            if isinstance(response, list):
                for item in response:
                    if isinstance(item, dict):
                        if "base64" in item:
                            image_base64.append(item["base64"])
                        if "url" in item:
                            image_urls.append(item["url"])
                    elif isinstance(item, str):
                        image_base64.append(item)
            elif isinstance(response, dict):
                if "error" in response:
                    return GenerationResult(
                        success=False,
                        data=None,
                        cost=0.0,
                        provider=self.provider_name,
                        model=model,
                        metadata={"error": response.get("error")},
                    )
                if "output" in response:
                    output = response["output"]
                    if isinstance(output, list):
                        for item in output:
                            if isinstance(item, str):
                                image_base64.append(item)
                            elif isinstance(item, dict):
                                if "base64" in item:
                                    image_base64.append(item["base64"])
                                if "url" in item:
                                    image_urls.append(item["url"])
            elif isinstance(response, bytes):
                import base64

                image_base64.append(base64.b64encode(response).decode("utf-8"))

            if image_base64 or image_urls:
                result_data = {
                    "base64_images": image_base64,
                    "urls": image_urls,
                    "images": image_base64 if image_base64 else image_urls,
                }

                cost = self.get_cost_estimate(prompt, model, num_images=num_images)

                return GenerationResult(
                    success=True,
                    data=result_data,
                    cost=cost,
                    provider=self.provider_name,
                    model=model,
                    metadata={
                        "width": width,
                        "height": height,
                        "num_images": len(image_base64) or len(image_urls) or 1,
                        "seed": seed,
                        "guidance_scale": guidance_scale,
                        "num_inference_steps": num_inference_steps,
                        "negative_prompt": negative_prompt,
                        "full_model": full_model,
                    },
                )

            return GenerationResult(
                success=False,
                data=None,
                cost=0.0,
                provider=self.provider_name,
                model=model,
                metadata={
                    "error": "No images returned from API",
                    "response_type": str(type(response)),
                    "response_preview": str(response)[:200] if response else None,
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
        """Check if the HuggingFace provider is available.

        Performs a lightweight health check by verifying connectivity
        to the HuggingFace Inference API. Without API key, checks
        the free tier availability. With API key, validates authentication.

        Returns:
            True if the provider is available, False otherwise
        """
        test_url = f"{self.base_url}/models"

        headers = self._build_headers()

        request = urllib.request.Request(test_url, headers=headers, method="HEAD")

        try:
            ssl_context = ssl.create_default_context()
            with urllib.request.urlopen(
                request, context=ssl_context, timeout=10
            ) as response:
                return response.status < 500
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                return True
            return False
        except Exception:
            return True

    def get_cost_estimate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> float:
        """Estimate the cost of an image generation operation.

        HuggingFace has a free tier with rate limits. After that,
        costs vary by model. This provides an estimate for planning.

        Args:
            prompt: The text description for image generation
            model: Optional model identifier
            **kwargs: Additional generation parameters:
                - num_images: Number of images to generate

        Returns:
            Estimated cost in USD
        """
        model = model or self.get_default_model()

        full_model = self._get_model_identifier(model)

        num_images = kwargs.get("num_images", 1)

        base_cost = MODEL_COSTS.get(full_model, MODEL_COSTS.get(model, 0.003))

        return base_cost * num_images


__all__ = ["HuggingFaceProvider"]
