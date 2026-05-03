"""
base_provider.py — Abstract Base Class for AI Providers

All providers in the AI Interceptor ecosystem must implement this interface.
Provides a uniform contract for generate(), check_credits(), and is_available().
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class ProviderCapability:
    """Enumeration of known task types."""

    TEXT2VIDEO = "text2video"
    IMAGE2VIDEO = "image2video"
    TEXT2IMAGE = "text2image"
    IMAGE2IMAGE = "image2image"
    TEXT_GENERATION = "text_generation"
    SOCIAL_POST = "social_post"
    VIDEO_ENHANCE = "video_enhance"
    WATERMARK_REMOVE = "watermark_remove"


@dataclass
class ProviderResult:
    """Standardised return type from BaseProvider.generate()."""

    success: bool
    output: Any = None                   # File path, URL, text, etc.
    cost: int = 0                        # Credits / tokens consumed
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "output": self.output,
            "cost": self.cost,
            "metadata": self.metadata,
            "error": self.error,
        }


class BaseProvider(ABC):
    """
    Abstract base class that every AI provider must inherit from.

    Subclasses must define:
        - name          (class-level str)
        - capabilities  (class-level list[str])
        - cost_per_call (class-level dict)
        - generate()
        - check_credits()
        - is_available()

    Optional overrides:
        - configure()     — apply runtime config
        - health_check()  — extended liveness probe
    """

    # ---- class-level attributes (override in subclass) ----
    name: str = "base"
    capabilities: List[str] = []
    cost_per_call: Dict[str, int] = {}

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Args:
            config: Optional provider-specific configuration dict.
                    Keys depend on the concrete provider (API keys, URLs, etc.).
        """
        self._config: Dict[str, Any] = config or {}
        self._logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        if config:
            self.configure(config)

    def configure(self, config: Dict[str, Any]) -> None:
        """
        Apply provider-specific configuration at runtime.

        Args:
            config: Provider configuration dict.
        """
        self._config.update(config)

    @abstractmethod
    def generate(self, task_type: str, **kwargs: Any) -> Dict[str, Any]:
        """
        Execute the generation task.

        Args:
            task_type: One of ProviderCapability constants.
            **kwargs:  Task-specific parameters (prompt, image_path, etc.).

        Returns:
            dict with keys: success, output, cost, metadata, error
        """
        ...

    @abstractmethod
    def check_credits(self) -> float:
        """
        Return the current available credits/quota for this provider.

        Returns:
            float — remaining credits (semantics vary by provider).
        """
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check whether the provider can accept requests right now.

        Returns:
            True if the provider is online and configured.
        """
        ...

    def supports(self, task_type: str) -> bool:
        """Return True if this provider supports *task_type*."""
        return task_type in self.capabilities

    def estimated_cost(self, task_type: str) -> int:
        """
        Return the expected credit cost for *task_type*, or 0 if unknown.

        Args:
            task_type: Task type string.

        Returns:
            int — estimated credits.
        """
        return self.cost_per_call.get(task_type, 0)

    def health_check(self) -> Dict[str, Any]:
        """
        Extended health probe — calls is_available() and check_credits().

        Returns:
            dict with keys: provider, available, credits, capabilities.
        """
        try:
            available = self.is_available()
            credits = self.check_credits() if available else 0.0
        except Exception as exc:  # noqa: BLE001
            self._logger.warning("Health check failed for %s: %s", self.name, exc)
            available = False
            credits = 0.0

        return {
            "provider": self.name,
            "available": available,
            "credits": credits,
            "capabilities": self.capabilities,
        }

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r} caps={self.capabilities}>"
