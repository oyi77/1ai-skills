"""BytePlus provider for video generation using Seedance.

This module provides the BytePlusProvider class for native video generation
through BytePlus Seedance API.
"""

import json
import urllib.request
import urllib.error
from typing import Optional

from .base import AIProvider, GenerationResult, ProviderType


class BytePlusProvider(AIProvider):
    """BytePlus provider for video generation using Seedance API.

    Supports both text-to-video and image-to-video generation through
    BytePlus's Seedance models.

    Attributes:
        seedance_t2v: Text-to-video model identifier
        seedance_i2v: Image-to-video model identifier
    """

    # Seedance model identifiers
    SEEDANCE_T2V = "seedance-t2v"
    SEEDANCE_I2V = "seedance-i2v"

    # Default model
    DEFAULT_MODEL = SEEDANCE_T2V

    # Cost per second in USD (approximate)
    COST_PER_SECOND = 0.05

    # API endpoints
    BASE_URL = "https://open.byteplusapi.com"

    def __init__(
        self,
        api_key: Optional[str] = None,
        region: str = "us-east-1",
        **kwargs,
    ):
        """Initialize the BytePlus provider.

        Args:
            api_key: BytePlus API key for authentication
            region: AWS region for API calls (default: us-east-1)
            **kwargs: Additional provider-specific configuration
        """
        super().__init__(
            provider_type=ProviderType.VIDEO,
            provider_name="BytePlus Seedance",
            api_key=api_key,
            **kwargs,
        )
        self.region = region

    @property
    def supported_models(self) -> list[str]:
        """Get list of supported model identifiers.

        Returns:
            List of supported model IDs
        """
        return [self.SEEDANCE_T2V, self.SEEDANCE_I2V]

    def _get_endpoint(self, model: str) -> str:
        """Get the appropriate API endpoint for the model.

        Args:
            model: Model identifier

        Returns:
            API endpoint URL
        """
        if model == self.SEEDANCE_I2V:
            return f"{self.BASE_URL}/videoextraction/v1/generation/image_to_video"
        return f"{self.BASE_URL}/videoextraction/v1/generation/text_to_video"

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

    def _make_request(self, endpoint: str, payload: dict) -> dict:
        """Make HTTP request to BytePlus API.

        Args:
            endpoint: API endpoint URL
            payload: Request payload

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
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))

    async def generate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> GenerationResult:
        """Generate video based on the given prompt.

        Args:
            prompt: The prompt/description for video generation
            model: Optional model identifier (uses default if not specified)
            **kwargs: Additional generation parameters:
                - image_url: str, required for image-to-video
                - duration: int, video duration in seconds (default: 5)
                - fps: int, frames per second (default: 24)
                - resolution: str, video resolution (default: "1280x720")

        Returns:
            GenerationResult containing the generated video URL and metadata
        """
        if not self.validate_api_key():
            return GenerationResult(
                success=False,
                provider=self.provider_name,
                model=model or self.get_default_model(),
                metadata={"error": "API key is required"},
            )

        model = model or self.get_default_model()

        # Extract generation parameters
        duration = kwargs.get("duration", 5)
        fps = kwargs.get("fps", 24)
        resolution = kwargs.get("resolution", "1280x720")
        image_url = kwargs.get("image_url")

        # Build request payload
        if model == self.SEEDANCE_I2V:
            if not image_url:
                return GenerationResult(
                    success=False,
                    provider=self.provider_name,
                    model=model,
                    metadata={
                        "error": "image_url is required for image-to-video generation"
                    },
                )
            payload = {
                "prompt": prompt,
                "image_url": image_url,
                "duration": duration,
                "fps": fps,
                "resolution": resolution,
            }
        else:
            payload = {
                "prompt": prompt,
                "duration": duration,
                "fps": fps,
                "resolution": resolution,
            }

        endpoint = self._get_endpoint(model)

        try:
            response = self._make_request(endpoint, payload)

            # Parse response
            if response.get("code") == 0 or response.get("status") == "success":
                video_url = response.get("data", {}).get("video_url") or response.get(
                    "video_url"
                )
                task_id = response.get("data", {}).get("task_id") or response.get(
                    "task_id"
                )

                cost = self.get_cost_estimate(prompt, model, **kwargs)

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
                        "duration": duration,
                        "fps": fps,
                        "resolution": resolution,
                        "prompt": prompt,
                    },
                )
            else:
                error_msg = (
                    response.get("message") or response.get("error") or "Unknown error"
                )
                return GenerationResult(
                    success=False,
                    provider=self.provider_name,
                    model=model,
                    metadata={"error": error_msg},
                )

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else str(e)
            return GenerationResult(
                success=False,
                provider=self.provider_name,
                model=model,
                metadata={"error": f"HTTP {e.code}: {error_body}"},
            )
        except urllib.error.URLError as e:
            return GenerationResult(
                success=False,
                provider=self.provider_name,
                model=model,
                metadata={"error": f"Network error: {str(e.reason)}"},
            )
        except Exception as e:
            return GenerationResult(
                success=False,
                provider=self.provider_name,
                model=model,
                metadata={"error": f"Unexpected error: {str(e)}"},
            )

    async def is_available(self) -> bool:
        """Check if the BytePlus provider is currently available.

        This performs a lightweight health check by verifying API connectivity.

        Returns:
            True if the provider is available, False otherwise
        """
        if not self.validate_api_key():
            return False

        # Try a simple connectivity check
        try:
            test_endpoint = f"{self.BASE_URL}/v1/health"
            req = urllib.request.Request(
                test_endpoint,
                headers=self._build_headers(),
                method="GET",
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.status == 200
        except urllib.error.HTTPError:
            # Health endpoint might not exist, check auth instead
            return self.validate_api_key()
        except urllib.error.URLError:
            return False
        except Exception:
            # If we can't determine availability, assume available if API key is set
            return self.validate_api_key()

    def get_cost_estimate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> float:
        """Estimate the cost of a video generation operation.

        Args:
            prompt: The prompt/description for video generation
            model: Optional model identifier
            **kwargs: Additional generation parameters:
                - duration: int, video duration in seconds (default: 5)

        Returns:
            Estimated cost in USD
        """
        model = model or self.get_default_model()
        duration = kwargs.get("duration", 5)

        # Base cost calculation
        cost = duration * self.COST_PER_SECOND

        # Add model-specific adjustments
        if model == self.SEEDANCE_I2V:
            # Image-to-video typically costs more
            cost *= 1.5

        return round(cost, 4)
