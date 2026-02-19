"""Ollama provider for local LLM inference.

This module provides the OllamaProvider class for generating text content
using Ollama's local LLM inference API.
"""

import json
import urllib.request
import urllib.error
from typing import Any, Optional

from .base import AIProvider, GenerationResult, ProviderType


class OllamaProvider(AIProvider):
    """Ollama provider for local LLM inference.

    Ollama runs locally and provides inference for large language models
    without requiring any API keys or external services.

    Attributes:
        provider_type: Always ProviderType.LLM for this provider
        provider_name: Human-readable name ("Ollama")
        supported_models: List of supported Ollama models
    """

    # Ollama models (running locally - no API costs)
    PRICING = {
        "llama3.3": {"input": 0.0, "output": 0.0},
        "llama3.2": {"input": 0.0, "output": 0.0},
        "llama3.1": {"input": 0.0, "output": 0.0},
        "llama3": {"input": 0.0, "output": 0.0},
        "llama2": {"input": 0.0, "output": 0.0},
        "mistral": {"input": 0.0, "output": 0.0},
        "mixtral": {"input": 0.0, "output": 0.0},
        "phi3": {"input": 0.0, "output": 0.0},
        "phi3.5": {"input": 0.0, "output": 0.0},
        "phi4": {"input": 0.0, "output": 0.0},
        "qwen2.5": {"input": 0.0, "output": 0.0},
        "qwen2": {"input": 0.0, "output": 0.0},
        "gemma2": {"input": 0.0, "output": 0.0},
        "gemma": {"input": 0.0, "output": 0.0},
        "codellama": {"input": 0.0, "output": 0.0},
        "deepseek-coder-v2": {"input": 0.0, "output": 0.0},
        "command-r": {"input": 0.0, "output": 0.0},
        "command-r-plus": {"input": 0.0, "output": 0.0},
        "aya": {"input": 0.0, "output": 0.0},
        "falcon2": {"input": 0.0, "output": 0.0},
    }

    DEFAULT_MODEL = "llama3.3"

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "http://localhost:11434",
        **kwargs,
    ):
        """Initialize the Ollama provider.

        Args:
            api_key: Not required for Ollama (runs locally), kept for compatibility
            base_url: Base URL for the Ollama API (defaults to localhost:11434)
            **kwargs: Additional provider-specific configuration
        """
        super().__init__(
            provider_type=ProviderType.LLM,
            provider_name="Ollama",
            api_key=api_key,
            **kwargs,
        )
        self.base_url = base_url.rstrip("/")

    @property
    def supported_models(self) -> list[str]:
        """Get list of supported model identifiers.

        Returns:
            List of Ollama model IDs that can be used with this provider
        """
        return list(self.PRICING.keys())

    async def generate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> GenerationResult:
        """Generate text content using Ollama's generate API.

        Args:
            prompt: The prompt for text generation
            model: Optional model identifier (defaults to llama3.3)
            **kwargs: Additional parameters like temperature, max_tokens, etc.

        Returns:
            GenerationResult containing the generated text and metadata
        """
        model = model or self.get_default_model()

        # Build the request payload
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "temperature": kwargs.get("temperature", 0.7),
            "num_predict": kwargs.get("max_tokens", 1024),
            "top_p": kwargs.get("top_p", 1.0),
        }

        # Add optional parameters
        if "stop" in kwargs:
            payload["stop"] = kwargs["stop"]

        # Estimate cost before making request (always $0 for local)
        _ = self.get_cost_estimate(prompt, model, **kwargs)

        try:
            # Make the API request
            response_data = self._make_request(
                endpoint="/api/generate",
                payload=payload,
            )

            # Extract the generated content
            content = response_data.get("response", "")

            if not content:
                return GenerationResult(
                    success=False,
                    data=None,
                    cost=0.0,
                    provider=self.provider_name,
                    model=model,
                    metadata={"error": "No response returned from Ollama"},
                )

            # Get usage stats if available
            eval_count = response_data.get("eval_count", 0)
            prompt_eval_count = response_data.get("prompt_eval_count", 0)

            return GenerationResult(
                success=True,
                data=content,
                cost=0.0,  # Local inference is free
                provider=self.provider_name,
                model=model,
                metadata={
                    "done": response_data.get("done", True),
                    "eval_count": eval_count,
                    "prompt_eval_count": prompt_eval_count,
                    "context": response_data.get("context"),
                    "total_duration": response_data.get("total_duration"),
                    "load_duration": response_data.get("load_duration"),
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
        """Check if the Ollama service is available.

        Performs a lightweight check by attempting to reach the Ollama API.

        Returns:
            True if the provider is available, False otherwise
        """
        try:
            self._make_request(endpoint="/api/tags", method="GET")
            return True
        except Exception:
            return False

    def get_cost_estimate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> float:
        """Estimate the cost of a generation operation.

        Ollama runs locally, so the cost is always $0.

        Args:
            prompt: The input prompt
            model: Optional model identifier
            **kwargs: Additional parameters

        Returns:
            Estimated cost in USD (always 0.0 for local inference)
        """
        # Local inference is free
        return 0.0

    def _make_request(
        self, endpoint: str, payload: Optional[dict] = None, method: str = "POST"
    ) -> dict[str, Any]:
        """Make an HTTP request to the Ollama API.

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
        }

        # Add API key if provided (some local setups may use it)
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

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

    def list_installed_models(self) -> list[dict[str, Any]]:
        """List all models installed locally in Ollama.

        Returns:
            List of model information dictionaries

        Raises:
            urllib.error.HTTPError: On HTTP errors
        """
        try:
            response = self._make_request(endpoint="/api/tags", method="GET")
            return response.get("models", [])
        except Exception:
            return []
