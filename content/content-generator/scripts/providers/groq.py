"""Groq provider for fast LLM inference.

This module provides the GroqProvider class for generating text content
using Groq's high-speed LLM inference API.
"""

import json
import urllib.request
import urllib.error
from typing import Any, Optional

from .base import AIProvider, GenerationResult, ProviderType


class GroqProvider(AIProvider):
    """Groq provider for fast LLM inference.

    Groq provides high-speed inference for large language models,
    making it ideal for applications requiring low latency.

    Attributes:
        provider_type: Always ProviderType.LLM for this provider
        provider_name: Human-readable name ("Groq")
        supported_models: List of supported Groq models
    """

    # Groq pricing per 1M input/output tokens (as of 2024)
    PRICING = {
        "llama-3.3-70b-versatile": {"input": 0.0, "output": 0.0},  # Free
        "llama-3.1-70b-versatile": {"input": 0.0, "output": 0.0},  # Free
        "llama-3.1-8b-instant": {"input": 0.0, "output": 0.0},  # Free
        "llama-3-70b-instruct": {"input": 0.59, "output": 0.79},
        "llama-3-8b-instruct": {"input": 0.05, "output": 0.08},
        "mixtral-8x7b-32768": {"input": 0.24, "output": 0.24},
        "gemma-7b-it": {"input": 0.07, "output": 0.07},
    }

    DEFAULT_MODEL = "llama-3.3-70b-versatile"

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.groq.com/openai/v1",
        **kwargs,
    ):
        """Initialize the Groq provider.

        Args:
            api_key: Groq API key for authentication
            base_url: Base URL for the Groq API (defaults to OpenAI-compatible endpoint)
            **kwargs: Additional provider-specific configuration
        """
        super().__init__(
            provider_type=ProviderType.LLM,
            provider_name="Groq",
            api_key=api_key,
            **kwargs,
        )
        self.base_url = base_url.rstrip("/")

    @property
    def supported_models(self) -> list[str]:
        """Get list of supported model identifiers.

        Returns:
            List of Groq model IDs that can be used with this provider
        """
        return list(self.PRICING.keys())

    async def generate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> GenerationResult:
        """Generate text content using Groq's chat completions API.

        Args:
            prompt: The prompt for text generation
            model: Optional model identifier (defaults to llama-3.3-70b-versatile)
            **kwargs: Additional parameters like temperature, max_tokens, etc.

        Returns:
            GenerationResult containing the generated text and metadata
        """
        model = model or self.get_default_model()

        # Build the request payload
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 1024),
            "top_p": kwargs.get("top_p", 1.0),
        }

        # Add optional parameters
        if "stop" in kwargs:
            payload["stop"] = kwargs["stop"]

        # Estimate cost before making request (used as fallback if API fails)
        _ = self.get_cost_estimate(prompt, model, **kwargs)

        try:
            # Make the API request
            response_data = self._make_request(
                endpoint="/chat/completions",
                payload=payload,
            )

            # Extract the generated content
            choices = response_data.get("choices", [])
            if not choices:
                return GenerationResult(
                    success=False,
                    data=None,
                    cost=0.0,
                    provider=self.provider_name,
                    model=model,
                    metadata={"error": "No choices returned from API"},
                )

            message = choices[0].get("message", {})
            content = message.get("content", "")

            # Calculate actual cost based on API response usage
            actual_cost = self._calculate_cost_from_usage(
                response_data.get("usage", {}), model
            )

            return GenerationResult(
                success=True,
                data=content,
                cost=actual_cost,
                provider=self.provider_name,
                model=model,
                metadata={
                    "finish_reason": choices[0].get("finish_reason"),
                    "usage": response_data.get("usage", {}),
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
                metadata={"error": f"HTTP {e.code}: {error_body}"},
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
        """Check if the Groq API is available.

        Performs a lightweight check by attempting to list available models.

        Returns:
            True if the provider is available, False otherwise
        """
        if not self.validate_api_key():
            return False

        try:
            self._make_request(endpoint="/models", method="GET")
            return True
        except Exception:
            return False

    def get_cost_estimate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> float:
        """Estimate the cost of a generation operation.

        Provides a cost estimate based on prompt length and model pricing.

        Args:
            prompt: The input prompt
            model: Optional model identifier
            **kwargs: Additional parameters (max_tokens affects output cost)

        Returns:
            Estimated cost in USD
        """
        model = model or self.get_default_model()

        if model not in self.PRICING:
            # Default to a reasonable estimate if model not found
            return 0.0

        pricing = self.PRICING[model]

        # Estimate tokens (rough approximation: 1 token ≈ 4 characters)
        input_tokens = len(prompt) / 4
        output_tokens = kwargs.get("max_tokens", 1024)

        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]

        return round(input_cost + output_cost, 6)

    def _make_request(
        self, endpoint: str, payload: Optional[dict] = None, method: str = "POST"
    ) -> dict[str, Any]:
        """Make an HTTP request to the Groq API.

        Args:
            endpoint: API endpoint path
            payload: Request body (for POST requests)
            method: HTTP method (GET or POST)

        Returns:
            Parsed JSON response

        Raises:
            urllib.error.HTTPError: On HTTP errors
        """
        url = f"{self.base_url}{endpoint}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        request_data = None
        if method == "POST" and payload:
            request_data = json.dumps(payload).encode("utf-8")

        request = urllib.request.Request(
            url,
            data=request_data,
            headers=headers,
            method=method,
        )

        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))

    def _calculate_cost_from_usage(self, usage: dict[str, int], model: str) -> float:
        """Calculate actual cost from API usage data.

        Args:
            usage: Usage dictionary from API response
            model: Model identifier

        Returns:
            Actual cost in USD
        """
        if model not in self.PRICING:
            return 0.0

        pricing = self.PRICING[model]
        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)

        input_cost = (prompt_tokens / 1_000_000) * pricing["input"]
        output_cost = (completion_tokens / 1_000_000) * pricing["output"]

        return round(input_cost + output_cost, 6)
