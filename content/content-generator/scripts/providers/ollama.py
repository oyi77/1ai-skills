"""Ollama provider for local/Cloud LLM inference.

This module provides the OllamaProvider class for generating text content
using Ollama's API (both local and cloud).
"""

import json
import urllib.request
import urllib.error
from typing import Any, Optional

from .base import AIProvider, GenerationResult, ProviderType


class OllamaProvider(AIProvider):
    """Ollama provider for LLM inference.

    Ollama provides inference for large language models.
    Supports both local (localhost:11434) and cloud (api.ollama.com) endpoints.

    Attributes:
        provider_type: Always ProviderType.LLM for this provider
        provider_name: Human-readable name ("Ollama")
        supported_models: List of supported Ollama models
    """

    # Ollama models
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
        base_url: Optional[str] = None,
        **kwargs,
    ):
        """Initialize the Ollama provider.

        Args:
            api_key: Ollama Cloud API key (required for cloud)
            base_url: Base URL for Ollama API (defaults to https://api.ollama.com for cloud)
            **kwargs: Additional provider-specific configuration
        """
        super().__init__(
            provider_type=ProviderType.LLM,
            provider_name="Ollama",
            api_key=api_key,
            **kwargs,
        )
        # Default to Ollama Cloud if not specified
        self.base_url = (base_url or "https://api.ollama.com").rstrip("/")

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
            GenerationResult containing generated text and metadata
        """
        model = model or self.get_default_model()

        # Build request payload
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

        # Estimate cost before making request
        _ = self.get_cost_estimate(prompt, model, **kwargs)

        try:
            # Make API request
            response_data = self._make_request(
                endpoint="/api/generate",
                payload=payload,
            )

            # Extract generated content
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
                cost=0.0,
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
        """Check if Ollama service is available.

        Performs a lightweight check by attempting to reach Ollama API.

        Returns:
            True if provider is available, False otherwise
        """
        try:
            self._make_request(endpoint="/api/tags", method="GET")
            return True
        except Exception:
            return False

    def get_cost_estimate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> float:
        """Estimate cost of a generation operation.

        Ollama Cloud charges apply, local is free.

        Args:
            prompt: The input prompt
            model: Optional model identifier
            **kwargs: Additional parameters

        Returns:
            Estimated cost in USD
        """
        # Local inference is free, cloud charges apply
        return 0.0

    def _make_request(
        self, endpoint: str, payload: Optional[dict] = None, method: str = "POST"
    ) -> dict[str, Any]:
        """Make an HTTP request to Ollama API.

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

        # Add API key for cloud authentication
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
        """List all models available in Ollama.

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
