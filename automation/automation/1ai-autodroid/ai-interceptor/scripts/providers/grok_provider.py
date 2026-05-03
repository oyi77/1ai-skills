"""
grok_provider.py — Grok AI Provider (xAI)

Wraps xAI's Grok API for text generation.
API: https://api.x.ai/v1 (OpenAI-compatible)
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

import requests

from .base_provider import BaseProvider, ProviderCapability

logger = logging.getLogger(__name__)

GROK_API_BASE = "https://api.x.ai/v1"
DEFAULT_MODEL = "grok-beta"


class GrokProvider(BaseProvider):
    """
    Grok AI provider for text generation tasks.

    Config keys:
        api_key     (str)  — xAI API key
        model       (str)  — model name (default "grok-beta")
        base_url    (str)  — API base URL override
        max_tokens  (int)  — max tokens per response (default 2048)
        temperature (float)— sampling temperature (default 0.7)
    """

    name = "grok"
    capabilities = [ProviderCapability.TEXT_GENERATION]
    cost_per_call = {ProviderCapability.TEXT_GENERATION: 1}  # tokens-based; 1 = placeholder

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._api_key: str = self._config.get("api_key", os.getenv("GROK_API_KEY", ""))
        self._model: str = self._config.get("model", DEFAULT_MODEL)
        self._base_url: str = self._config.get("base_url", GROK_API_BASE)
        self._max_tokens: int = int(self._config.get("max_tokens", 2048))
        self._temperature: float = float(self._config.get("temperature", 0.7))

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

    def _chat_complete(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
    ) -> Dict[str, Any]:
        payload = {
            "model": self._model,
            "messages": messages,
            "max_tokens": max_tokens or self._max_tokens,
            "temperature": temperature if temperature is not None else self._temperature,
        }
        try:
            resp = requests.post(
                f"{self._base_url}/chat/completions",
                json=payload,
                headers=self._headers(),
                timeout=60,
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as exc:
            logger.error("Grok API error: %s", exc)
            return {"error": str(exc)}

    # ------------------------------------------------------------------
    # BaseProvider interface
    # ------------------------------------------------------------------

    def generate(self, task_type: str, **kwargs: Any) -> Dict[str, Any]:
        """
        Generate text via Grok.

        Args:
            task_type: "text_generation"
            **kwargs:
                prompt      (str)           — user prompt (required)
                system      (str)           — system message (optional)
                messages    (list[dict])    — full message history (overrides prompt/system)
                max_tokens  (int)           — override default
                temperature (float)         — override default

        Returns:
            dict: success, output (str), cost (tokens), metadata, error
        """
        if not self.supports(task_type):
            return {
                "success": False,
                "output": None,
                "cost": 0,
                "metadata": {},
                "error": f"GrokProvider does not support task_type={task_type!r}",
            }

        messages: List[Dict[str, str]] = kwargs.get("messages", [])
        if not messages:
            system: str = kwargs.get("system", "You are a helpful AI assistant.")
            prompt: str = kwargs.get("prompt", "")
            messages = [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ]

        max_tokens = kwargs.get("max_tokens")
        temperature = kwargs.get("temperature")

        try:
            result = self._chat_complete(messages, max_tokens, temperature)
            if "error" in result:
                return {"success": False, "output": None, "cost": 0, "metadata": {}, "error": result["error"]}

            text = result["choices"][0]["message"]["content"]
            usage = result.get("usage", {})
            tokens_used = usage.get("total_tokens", 0)

            return {
                "success": True,
                "output": text,
                "cost": tokens_used,
                "metadata": {"model": self._model, "usage": usage},
                "error": None,
            }
        except Exception as exc:  # noqa: BLE001
            logger.exception("GrokProvider.generate() error: %s", exc)
            return {"success": False, "output": None, "cost": 0, "metadata": {}, "error": str(exc)}

    def check_credits(self) -> float:
        """
        Grok uses token-based billing; return a large sentinel value
        as credits are managed externally via xAI billing console.
        """
        # xAI doesn't expose a credits endpoint in v1 — return sentinel
        return 999999.0

    def is_available(self) -> bool:
        """Return True if API key configured and endpoint reachable."""
        if not self._api_key:
            return False
        try:
            resp = requests.get(f"{self._base_url}/models", headers=self._headers(), timeout=10)
            return resp.status_code < 500
        except Exception:  # noqa: BLE001
            return False
