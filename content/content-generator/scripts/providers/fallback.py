"""Failover/Fallback system for content generation providers.

Implements automatic provider switching when rate limited or API errors occur.
Each provider type (IMAGE, VIDEO) has a prioritized fallback chain.
"""

import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from .base import AIProvider, ProviderType, GenerationResult
from .geminigen import RateLimitError, APIError

logger = logging.getLogger("openclaw.fallback")


class Situation(Enum):
    """Current system situation determining provider priority."""

    NORMAL = "normal"
    RATE_LIMITED = "rate_limited"
    BOTH_LIMITED = "both_limited"
    ALL_APIS_DOWN = "all_apis_down"
    NO_INTERNET = "no_internet"


@dataclass
class ProviderAttempt:
    """Record of a provider generation attempt."""

    provider_name: str
    success: bool
    error: Optional[str] = None
    duration_ms: float = 0.0
    timestamp: float = field(default_factory=time.time)


@dataclass
class FallbackChainResult:
    """Result from a fallback chain execution."""

    result: Optional[GenerationResult] = None
    attempts: list[ProviderAttempt] = field(default_factory=list)
    total_providers_tried: int = 0

    @property
    def success(self) -> bool:
        return self.result is not None and self.result.success


class FallbackChain:
    """Manages provider fallback chains with automatic switching.

    Image Generation Fallback Chain:
        1. GeminiGen (Gemini 2.0 Flash) → Primary (fastest, free tier)
        2. NVIDIA Flux.1-dev → Secondary (quality, API key needed)
        3. Replicate Flux → Tertiary (paid, reliable)
        4. Fal.ai Flux → Quaternary
        5. Remotion static image → LAST RESORT (local, no API needed)

    Video Generation Fallback Chain:
        1. Seedance 1.0 Pro Fast → Primary (BytePlus API)
        2. Seedance 1.5 Pro → Secondary (newest BytePlus)
        3. Grok Aurora (video) → Tertiary
        4. Remotion Animation → FALLBACK (fully local, no API needed)
        5. FFmpeg slideshow → LAST RESORT (static images → video, always works)
    """

    def __init__(self):
        self._image_chain: list[AIProvider] = []
        self._video_chain: list[AIProvider] = []
        self._llm_chain: list[AIProvider] = []
        self._rate_limit_tracker: dict[
            str, float
        ] = {}  # provider_name → cooldown_until
        self._failure_tracker: dict[
            str, int
        ] = {}  # provider_name → consecutive failures

    # ── Chain Registration ──────────────────────────────────────────

    def register_image_chain(self, providers: list[AIProvider]):
        """Register image providers in priority order."""
        self._image_chain = providers
        logger.info(
            "Image fallback chain: %s",
            " → ".join(p.provider_name for p in providers),
        )

    def register_video_chain(self, providers: list[AIProvider]):
        """Register video providers in priority order."""
        self._video_chain = providers
        logger.info(
            "Video fallback chain: %s",
            " → ".join(p.provider_name for p in providers),
        )

    def register_llm_chain(self, providers: list[AIProvider]):
        """Register LLM providers in priority order."""
        self._llm_chain = providers

    def _get_chain(self, provider_type: ProviderType) -> list[AIProvider]:
        chains = {
            ProviderType.IMAGE: self._image_chain,
            ProviderType.VIDEO: self._video_chain,
            ProviderType.LLM: self._llm_chain,
        }
        return chains.get(provider_type, [])

    # ── Core Fallback Logic ─────────────────────────────────────────

    async def generate_with_fallback(
        self,
        prompt: str,
        provider_type: ProviderType,
        model: Optional[str] = None,
        **kwargs,
    ) -> FallbackChainResult:
        """Generate content with automatic provider fallback.

        Tries each provider in the chain sequentially. On rate limit or
        API error, automatically switches to the next provider.

        Args:
            prompt: Generation prompt
            provider_type: IMAGE, VIDEO, or LLM
            model: Optional model override (provider-specific)
            **kwargs: Additional generation parameters

        Returns:
            FallbackChainResult with the successful result or all attempts
        """
        chain = self._get_chain(provider_type)
        if not chain:
            logger.error("No providers registered for %s", provider_type.value)
            return FallbackChainResult()

        chain_result = FallbackChainResult()

        for provider in chain:
            # Skip providers in cooldown
            if self._is_in_cooldown(provider.provider_name):
                logger.info("%s in cooldown, skipping", provider.provider_name)
                continue

            # Skip providers with too many consecutive failures
            if self._failure_tracker.get(provider.provider_name, 0) >= 5:
                logger.info(
                    "%s has 5+ consecutive failures, skipping",
                    provider.provider_name,
                )
                continue

            start = time.time()
            chain_result.total_providers_tried += 1

            try:
                logger.info(
                    "Trying %s for %s generation...",
                    provider.provider_name,
                    provider_type.value,
                )
                result = await provider.generate(prompt, model=model, **kwargs)

                duration_ms = (time.time() - start) * 1000
                attempt = ProviderAttempt(
                    provider_name=provider.provider_name,
                    success=result.success,
                    duration_ms=duration_ms,
                )

                if result.success:
                    self._failure_tracker[provider.provider_name] = 0
                    chain_result.result = result
                    chain_result.attempts.append(attempt)
                    logger.info(
                        "✓ %s succeeded (%.0fms)",
                        provider.provider_name,
                        duration_ms,
                    )
                    return chain_result

                # Generation returned but wasn't successful
                attempt.error = result.metadata.get("error", "Unknown error")
                chain_result.attempts.append(attempt)
                self._record_failure(provider.provider_name)
                logger.warning(
                    "✗ %s returned failure: %s",
                    provider.provider_name,
                    attempt.error,
                )

            except RateLimitError as e:
                duration_ms = (time.time() - start) * 1000
                chain_result.attempts.append(
                    ProviderAttempt(
                        provider_name=provider.provider_name,
                        success=False,
                        error=f"Rate limited: {e}",
                        duration_ms=duration_ms,
                    )
                )
                self._set_cooldown(provider.provider_name, cooldown_seconds=60)
                logger.warning(
                    "⚠ %s rate limited, trying next...",
                    provider.provider_name,
                )

            except APIError as e:
                duration_ms = (time.time() - start) * 1000
                chain_result.attempts.append(
                    ProviderAttempt(
                        provider_name=provider.provider_name,
                        success=False,
                        error=f"API error: {e}",
                        duration_ms=duration_ms,
                    )
                )
                self._record_failure(provider.provider_name)
                logger.warning(
                    "✗ %s API error: %s, trying next...",
                    provider.provider_name,
                    e,
                )

            except Exception as e:
                duration_ms = (time.time() - start) * 1000
                chain_result.attempts.append(
                    ProviderAttempt(
                        provider_name=provider.provider_name,
                        success=False,
                        error=str(e),
                        duration_ms=duration_ms,
                    )
                )
                self._record_failure(provider.provider_name)
                logger.error(
                    "✗ %s unexpected error: %s",
                    provider.provider_name,
                    e,
                )

        logger.error(
            "All %d providers exhausted for %s generation",
            chain_result.total_providers_tried,
            provider_type.value,
        )
        return chain_result

    # ── Rate Limit & Failure Tracking ───────────────────────────────

    def _is_in_cooldown(self, provider_name: str) -> bool:
        cooldown_until = self._rate_limit_tracker.get(provider_name, 0)
        return time.time() < cooldown_until

    def _set_cooldown(self, provider_name: str, cooldown_seconds: float = 60):
        self._rate_limit_tracker[provider_name] = time.time() + cooldown_seconds
        logger.info("%s in cooldown for %ds", provider_name, cooldown_seconds)

    def _record_failure(self, provider_name: str):
        self._failure_tracker[provider_name] = (
            self._failure_tracker.get(provider_name, 0) + 1
        )

    def reset_provider(self, provider_name: str):
        """Reset cooldown and failure count for a provider."""
        self._rate_limit_tracker.pop(provider_name, None)
        self._failure_tracker.pop(provider_name, None)

    def reset_all(self):
        """Reset all cooldowns and failure counters."""
        self._rate_limit_tracker.clear()
        self._failure_tracker.clear()

    # ── Status & Diagnostics ────────────────────────────────────────

    def get_status(self) -> dict:
        """Get current status of all registered providers."""
        now = time.time()
        status = {"image_chain": [], "video_chain": [], "llm_chain": []}

        for chain_name, chain in [
            ("image_chain", self._image_chain),
            ("video_chain", self._video_chain),
            ("llm_chain", self._llm_chain),
        ]:
            for provider in chain:
                name = provider.provider_name
                cooldown_remaining = max(0, self._rate_limit_tracker.get(name, 0) - now)
                status[chain_name].append(
                    {
                        "name": name,
                        "type": provider.provider_type.value,
                        "in_cooldown": cooldown_remaining > 0,
                        "cooldown_remaining_s": round(cooldown_remaining, 1),
                        "consecutive_failures": self._failure_tracker.get(name, 0),
                    }
                )

        return status


# ── Factory: Build Default Chains ───────────────────────────────────


def build_default_fallback_chain() -> FallbackChain:
    """Build the default fallback chain with all available providers.

    Image chain: GeminiGen → NVIDIA → Replicate → Fal.ai → Remotion Static
    Video chain: BytePlus Seedance → XAI Grok → Remotion → FFmpeg
    LLM chain: Groq → Ollama
    """
    chain = FallbackChain()

    # ── Image Providers ─────────────────────────────────────────
    from .geminigen import GeminiGenProvider
    from .nvidia import NVIDIAProvider
    from .replicate import ReplicateProvider
    from .falai import FalAIProvider
    from .remotion_local import RemotionImageProvider

    chain.register_image_chain(
        [
            GeminiGenProvider(),  # 1. Primary - fastest, free tier
            NVIDIAProvider(),  # 2. Secondary - quality
            ReplicateProvider(),  # 3. Tertiary - paid, reliable
            FalAIProvider(),  # 4. Quaternary
            RemotionImageProvider(),  # 5. LAST RESORT - local PIL
        ]
    )

    # ── Video Providers ─────────────────────────────────────────
    from .byteplus import BytePlusProvider
    from .runware import RunwareProvider
    from .vastai import VastAIProvider
    from .xai import XAIProvider
    from .remotion_local import RemotionVideoProvider
    from .ffmpeg_fallback import FFmpegSlideshowProvider

    chain.register_video_chain(
        [
            BytePlusProvider(),
            RunwareProvider(),
            VastAIProvider(),
            XAIProvider(),
            RemotionVideoProvider(),
            FFmpegSlideshowProvider(),
        ]
    )

    # ── LLM Providers ──────────────────────────────────────────
    from .groq import GroqProvider
    from .ollama import OllamaProvider

    chain.register_llm_chain(
        [
            GroqProvider(),
            OllamaProvider(),
        ]
    )

    return chain
