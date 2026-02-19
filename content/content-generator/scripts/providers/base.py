"""Abstract base class for AI content generation providers.

This module defines the AIProvider abstract base class that all
content generation providers (NVIDIA, BytePlus, XAI, etc.) must implement.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class ProviderType(Enum):
    """Types of content that a provider can generate.

    Attributes:
        IMAGE: Static image generation
        VIDEO: Video generation
        LLM: Large language model (text generation)
    """

    IMAGE = "image"
    VIDEO = "video"
    LLM = "llm"


@dataclass
class GenerationResult:
    """Result of a content generation operation.

    Attributes:
        success: Whether the generation succeeded
        data: The generated content (URL, file path, text, etc.)
        cost: Estimated cost in USD
        provider: Name of the provider that generated the content
        model: Model identifier used for generation
        metadata: Additional provider-specific metadata
    """

    success: bool
    data: Any = None
    cost: float = 0.0
    provider: str = ""
    model: str = ""
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        """Validate the GenerationResult after initialization."""
        if self.cost < 0:
            raise ValueError("Cost cannot be negative")


class AIProvider(ABC):
    """Abstract base class for AI content generation providers.

    All providers must inherit from this class and implement the
    abstract methods: generate(), is_available(), and get_cost_estimate().

    Attributes:
        provider_type: The type of content this provider generates
        provider_name: Human-readable name of the provider
        supported_models: List of model identifiers this provider supports
    """

    def __init__(
        self,
        provider_type: ProviderType,
        provider_name: str,
        api_key: Optional[str] = None,
        **kwargs,
    ):
        """Initialize the AI provider.

        Args:
            provider_type: The type of content this provider generates
            provider_name: Human-readable name of the provider
            api_key: Optional API key for authentication
            **kwargs: Additional provider-specific configuration
        """
        self.provider_type = provider_type
        self.provider_name = provider_name
        self.api_key = api_key
        self.config = kwargs

    @property
    @abstractmethod
    def supported_models(self) -> list[str]:
        """Get list of supported model identifiers.

        Returns:
            List of model IDs that this provider can use
        """
        pass

    @abstractmethod
    async def generate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> GenerationResult:
        """Generate content based on the given prompt.

        Args:
            prompt: The prompt/description for content generation
            model: Optional model identifier (uses default if not specified)
            **kwargs: Additional provider-specific generation parameters

        Returns:
            GenerationResult containing the generated content and metadata
        """
        pass

    @abstractmethod
    async def is_available(self) -> bool:
        """Check if the provider is currently available and operational.

        This method should perform a lightweight health check,
        such as verifying API connectivity or checking rate limits.

        Returns:
            True if the provider is available, False otherwise
        """
        pass

    @abstractmethod
    def get_cost_estimate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> float:
        """Estimate the cost of a generation operation.

        Provides a cost estimate before actual generation to help
        with budget planning and fallback decisions.

        Args:
            prompt: The prompt/description for content generation
            model: Optional model identifier
            **kwargs: Additional generation parameters

        Returns:
            Estimated cost in USD
        """
        pass

    def validate_api_key(self) -> bool:
        """Validate that the API key is present and properly configured.

        Base implementation checks for non-empty API key.
        Override this method for providers with specific key requirements.

        Returns:
            True if API key is valid, False otherwise
        """
        if self.api_key is None or self.api_key.strip() == "":
            return False
        return True

    def get_default_model(self) -> str:
        """Get the default model identifier for this provider.

        Returns:
            The default model ID
        """
        if self.supported_models:
            return self.supported_models[0]
        raise ValueError(f"No supported models defined for {self.provider_name}")

    def __repr__(self) -> str:
        """Return string representation of the provider."""
        return (
            f"{self.__class__.__name__}("
            f"provider_type={self.provider_type.value}, "
            f"provider_name={self.provider_name!r})"
        )
