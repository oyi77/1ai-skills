"""
provider_registry.py — AI Provider Registry with Auto-Discovery

Central registry that maps provider names → provider instances.
Supports lazy initialisation, capability-based lookup, and best-provider selection.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Type

from .base_provider import BaseProvider

logger = logging.getLogger(__name__)

# Module-level singleton
_registry: Optional["ProviderRegistry"] = None


def get_registry() -> "ProviderRegistry":
    """Return the global ProviderRegistry singleton."""
    global _registry  # noqa: PLW0603
    if _registry is None:
        _registry = ProviderRegistry()
        _registry.auto_register()
    return _registry


class ProviderRegistry:
    """
    Registry that maps provider names to BaseProvider instances.

    Usage::

        registry = get_registry()
        kling = registry.get("kling")
        best = registry.best_for("text2video", min_credits=60)
    """

    def __init__(self) -> None:
        self._classes: Dict[str, Type[BaseProvider]] = {}
        self._instances: Dict[str, BaseProvider] = {}
        self._configs: Dict[str, Dict[str, Any]] = {}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register_class(self, provider_class: Type[BaseProvider], name: Optional[str] = None) -> None:
        """
        Register a provider class (not yet instantiated).

        Args:
            provider_class: A subclass of BaseProvider.
            name: Override the provider's class-level name attribute.
        """
        n = name or getattr(provider_class, "name", provider_class.__name__.lower())
        self._classes[n] = provider_class
        logger.debug("ProviderRegistry: registered class %s as %r", provider_class.__name__, n)

    def register(self, instance: BaseProvider, name: Optional[str] = None) -> None:
        """
        Register an already-instantiated provider.

        Args:
            instance: A BaseProvider instance.
            name: Override the instance's name attribute.
        """
        n = name or instance.name
        self._instances[n] = instance
        logger.info("ProviderRegistry: registered instance %r", n)

    def configure(self, name: str, config: Dict[str, Any]) -> None:
        """
        Store configuration for a named provider (applied on first get()).

        Args:
            name:   Provider name.
            config: Configuration dict.
        """
        self._configs[name] = config

    def auto_register(self) -> None:
        """
        Auto-discover and register all built-in providers.
        Silently skips providers that fail to import.
        """
        _builtin_providers = [
            ("kling", "kling_provider", "KlingProvider"),
            ("grok", "grok_provider", "GrokProvider"),
            ("flow", "flow_provider", "FlowProvider"),
            ("pixverse", "pixverse_provider", "PixVerseProvider"),
            ("postbridge", "postbridge_provider", "PostBridgeProvider"),
        ]
        for name, module_name, class_name in _builtin_providers:
            try:
                import importlib
                mod = importlib.import_module(f".{module_name}", package=__package__)
                cls = getattr(mod, class_name)
                self.register_class(cls, name)
            except Exception as exc:  # noqa: BLE001
                logger.warning("Could not auto-register provider %r: %s", name, exc)

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get(self, name: str, config: Optional[Dict[str, Any]] = None) -> Optional[BaseProvider]:
        """
        Get a provider instance by name, creating it if necessary.

        Args:
            name:   Provider name (e.g. "kling").
            config: Runtime config override (merged with stored config).

        Returns:
            BaseProvider instance or None if not found.
        """
        # Return existing instance unless config overrides it
        if name in self._instances and config is None:
            return self._instances[name]

        # Merge stored config with runtime override
        merged_config = {**self._configs.get(name, {}), **(config or {})}

        # Instantiate from class registry
        if name in self._classes:
            try:
                instance = self._classes[name](config=merged_config)
                self._instances[name] = instance
                return instance
            except Exception as exc:  # noqa: BLE001
                logger.error("Failed to instantiate provider %r: %s", name, exc)
                return None

        logger.warning("ProviderRegistry: provider %r not found", name)
        return None

    def list_providers(self) -> List[str]:
        """Return all registered provider names."""
        return sorted(set(list(self._classes.keys()) + list(self._instances.keys())))

    def providers_for(self, capability: str) -> List[BaseProvider]:
        """
        Return all providers that support the given capability.

        Args:
            capability: e.g. "text2video"

        Returns:
            List of BaseProvider instances.
        """
        result: List[BaseProvider] = []
        for name in self.list_providers():
            p = self.get(name)
            if p and p.supports(capability):
                result.append(p)
        return result

    def best_for(
        self,
        capability: str,
        min_credits: float = 0,
        prefer_available: bool = True,
    ) -> Optional[BaseProvider]:
        """
        Select the best available provider for a capability.

        Selection order:
            1. Supports the capability
            2. is_available() == True (if prefer_available)
            3. check_credits() >= min_credits
            4. Lowest cost_per_call for the capability

        Args:
            capability:         Desired capability string.
            min_credits:        Minimum required credits.
            prefer_available:   Skip unavailable providers (default True).

        Returns:
            Best matching BaseProvider or None.
        """
        candidates: List[BaseProvider] = []
        for name in self.list_providers():
            p = self.get(name)
            if not p or not p.supports(capability):
                continue
            if prefer_available and not p.is_available():
                continue
            try:
                credits = p.check_credits()
                if credits < min_credits:
                    continue
                candidates.append(p)
            except Exception:  # noqa: BLE001
                if not prefer_available:
                    candidates.append(p)

        if not candidates:
            return None

        # Sort by cost ascending
        candidates.sort(key=lambda p: p.estimated_cost(capability))
        return candidates[0]

    def health_report(self) -> List[Dict[str, Any]]:
        """
        Run health_check() on all registered providers.

        Returns:
            List of health dicts.
        """
        report = []
        for name in self.list_providers():
            p = self.get(name)
            if p:
                report.append(p.health_check())
        return report

    def __repr__(self) -> str:
        return f"<ProviderRegistry providers={self.list_providers()}>"
