"""Fallback chain logic for automatic provider switching.

This module provides the ProviderStrategy class for defining provider fallback
orderings and the FallbackManager class for executing the fallback chain with
automatic failure handling.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from providers.base import AIProvider, GenerationResult, ProviderType


class StrategyType(Enum):
    """Predefined strategy types for provider selection."""

    FAST = "fast"
    QUALITY = "quality"
    CHEAP = "cheap"
    BALANCED = "balanced"
    FAILSAFE = "failsafe"


STRATEGIES: dict[StrategyType, dict[ProviderType, list[str]]] = {
    StrategyType.FAST: {
        ProviderType.IMAGE: ["nvidia", "replicate", "huggingface"],
        ProviderType.VIDEO: ["byteplus", "xai"],
        ProviderType.LLM: ["groq", "ollama"],
    },
    StrategyType.QUALITY: {
        ProviderType.IMAGE: ["nvidia", "replicate", "huggingface"],
        ProviderType.VIDEO: ["xai", "byteplus"],
        ProviderType.LLM: ["groq", "ollama"],
    },
    StrategyType.CHEAP: {
        ProviderType.IMAGE: ["huggingface", "replicate", "nvidia"],
        ProviderType.VIDEO: ["byteplus", "xai"],
        ProviderType.LLM: ["ollama", "groq"],
    },
    StrategyType.BALANCED: {
        ProviderType.IMAGE: ["nvidia", "replicate", "huggingface"],
        ProviderType.VIDEO: ["byteplus", "xai"],
        ProviderType.LLM: ["groq", "ollama"],
    },
    StrategyType.FAILSAFE: {
        ProviderType.IMAGE: ["huggingface", "replicate", "nvidia"],
        ProviderType.VIDEO: ["byteplus", "xai"],
        ProviderType.LLM: ["ollama", "groq"],
    },
}


class ProviderStrategy:
    """Manages provider fallback strategies.

    This class defines different strategies for provider selection based on
    priorities like speed, quality, cost, or reliability.

    Attributes:
        strategy_type: The type of strategy to use
        providers: Dictionary mapping provider names to provider instances
    """

    def __init__(
        self,
        strategy_type: StrategyType = StrategyType.BALANCED,
        providers: Optional[dict[str, AIProvider]] = None,
    ):
        """Initialize the provider strategy.

        Args:
            strategy_type: The strategy type to use (default: BALANCED)
            providers: Dictionary of provider name -> provider instance
        """
        self.strategy_type = strategy_type
        self.providers = providers or {}
        self._strategy_map = STRATEGIES.get(
            strategy_type, STRATEGIES[StrategyType.BALANCED]
        )

    def get_chain(self, provider_type: ProviderType) -> list[AIProvider]:
        """Get the provider fallback chain for a given type.

        Args:
            provider_type: The type of provider needed (IMAGE, VIDEO, LLM)

        Returns:
            List of provider instances in fallback order
        """
        provider_names = self._strategy_map.get(provider_type, [])
        chain = []
        for name in provider_names:
            provider = self.providers.get(name)
            if provider is not None:
                chain.append(provider)
        return chain

    def get_provider_names(self, provider_type: ProviderType) -> list[str]:
        """Get the provider names in fallback order for a given type.

        Args:
            provider_type: The type of provider needed

        Returns:
            List of provider names in fallback order
        """
        return self._strategy_map.get(provider_type, [])

    def set_strategy(self, strategy_type: StrategyType) -> None:
        """Change the current strategy type.

        Args:
            strategy_type: The new strategy type to use
        """
        self.strategy_type = strategy_type
        self._strategy_map = STRATEGIES.get(
            strategy_type, STRATEGIES[StrategyType.BALANCED]
        )

    def add_provider(self, name: str, provider: AIProvider) -> None:
        """Add or update a provider in the registry.

        Args:
            name: Provider identifier
            provider: Provider instance
        """
        self.providers[name] = provider

    def remove_provider(self, name: str) -> None:
        """Remove a provider from the registry.

        Args:
            name: Provider identifier to remove
        """
        self.providers.pop(name, None)


@dataclass
class FallbackAttempt:
    """Record of a single fallback attempt.

    Attributes:
        provider_name: Name of the provider attempted
        success: Whether the attempt succeeded
        error: Error message if failed
        cost: Cost of the attempt
    """

    provider_name: str
    success: bool
    error: Optional[str] = None
    cost: float = 0.0


@dataclass
class FallbackResult:
    """Result of a fallback chain execution.

    Attributes:
        success: Whether any provider succeeded
        result: The successful generation result
        attempts: List of all fallback attempts
        final_provider: Name of the provider that succeeded (if any)
    """

    success: bool
    result: Optional[GenerationResult] = None
    attempts: list[FallbackAttempt] = field(default_factory=list)
    final_provider: Optional[str] = None


class FallbackManager:
    """Manages provider fallback chains with automatic failure handling.

    This class handles attempting generation with multiple providers in sequence,
    automatically switching to the next provider when one fails.

    Attributes:
        strategy: The ProviderStrategy to use for determining fallback order
        max_attempts: Maximum number of providers to try (default: 3)
    """

    def __init__(
        self,
        strategy: Optional[ProviderStrategy] = None,
        max_attempts: int = 3,
    ):
        """Initialize the fallback manager.

        Args:
            strategy: ProviderStrategy instance (creates default if None)
            max_attempts: Maximum providers to try before giving up
        """
        self.strategy = strategy or ProviderStrategy()
        self.max_attempts = max_attempts

    async def try_provider(
        self,
        provider: AIProvider,
        prompt: str,
        model: Optional[str] = None,
        **kwargs,
    ) -> GenerationResult:
        """Attempt generation with a single provider.

        This method wraps the provider's generate method with additional
        error handling and availability checks.

        Args:
            provider: The provider instance to use
            prompt: The generation prompt
            model: Optional model identifier
            **kwargs: Additional generation parameters

        Returns:
            GenerationResult from the provider

        Raises:
            Exception: Any error from the provider
        """
        if not await provider.is_available():
            raise RuntimeError(f"Provider {provider.provider_name} is not available")

        result = await provider.generate(prompt, model, **kwargs)
        return result

    async def handle_failure(
        self,
        current_provider: AIProvider,
        error: Exception,
        provider_type: ProviderType,
    ) -> Optional[AIProvider]:
        """Handle provider failure and get the next provider in chain.

        This method is called when a provider fails. It logs the failure
        and returns the next provider in the fallback chain.

        Args:
            current_provider: The provider that failed
            error: The exception that was raised
            provider_type: The type of content being generated

        Returns:
            The next provider in the chain, or None if no more providers
        """
        print(f"Provider {current_provider.provider_name} failed: {error}")

        chain = self.strategy.get_chain(provider_type)
        current_name = current_provider.provider_name.lower()

        for i, p in enumerate(chain):
            if p.provider_name.lower() == current_name:
                if i + 1 < len(chain):
                    return chain[i + 1]
                break

        return None

    async def generate_with_fallback(
        self,
        provider_type: ProviderType,
        prompt: str,
        model: Optional[str] = None,
        **kwargs,
    ) -> FallbackResult:
        """Execute generation with automatic fallback.

        This is the main method that attempts generation with providers
        in sequence, falling back to the next provider on failure.

        Args:
            provider_type: The type of content to generate
            prompt: The generation prompt
            model: Optional model identifier
            **kwargs: Additional generation parameters

        Returns:
            FallbackResult containing the result and attempt history
        """
        chain = self.strategy.get_chain(provider_type)

        if not chain:
            return FallbackResult(success=False, attempts=[], final_provider=None)

        providers_to_try = chain[: self.max_attempts]
        provider = None

        for provider in providers_to_try:
            attempt = FallbackAttempt(
                provider_name=provider.provider_name, success=False
            )

            try:
                if not await provider.is_available():
                    attempt.error = "Provider not available"
                    continue

                result = await provider.generate(prompt, model, **kwargs)

                if result.success:
                    attempt.success = True
                    attempt.cost = result.cost
                    return FallbackResult(
                        success=True,
                        result=result,
                        attempts=[attempt],
                        final_provider=provider.provider_name,
                    )
                else:
                    attempt.error = result.metadata.get("error", "Generation failed")

            except Exception as e:
                attempt.error = str(e)

        return FallbackResult(success=False, attempts=[], final_provider=None)

    def get_available_providers(self, provider_type: ProviderType) -> list[AIProvider]:
        """Get list of available providers for a given type.

        Args:
            provider_type: The type of provider to filter by

        Returns:
            List of available provider instances
        """
        chain = self.strategy.get_chain(provider_type)
        available = []
        for provider in chain:
            if provider.validate_api_key():
                available.append(provider)
        return available
