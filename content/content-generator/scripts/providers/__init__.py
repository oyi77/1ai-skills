"""Provider package for content generation.

This package contains the abstract base class for AI providers
and specific implementations with automatic fallback chains.

Image Fallback: GeminiGen → NVIDIA → Replicate → Fal.ai → Remotion Static
Video Fallback: BytePlus Seedance → XAI Grok → Remotion → FFmpeg Slideshow
"""

from .base import AIProvider, ProviderType, GenerationResult
from .geminigen import GeminiGenProvider, RateLimitError, APIError
from .nvidia import NVIDIAProvider
from .replicate import ReplicateProvider
from .falai import FalAIProvider
from .huggingface import HuggingFaceProvider
from .byteplus import BytePlusProvider
from .xai import XAIProvider
from .remotion_local import RemotionVideoProvider, RemotionImageProvider
from .ffmpeg_fallback import FFmpegSlideshowProvider
from .groq import GroqProvider
from .ollama import OllamaProvider
from .fallback import FallbackChain, build_default_fallback_chain

__all__ = [
    # Base
    "AIProvider", "ProviderType", "GenerationResult",
    # Errors
    "RateLimitError", "APIError",
    # Image providers (priority order)
    "GeminiGenProvider",
    "NVIDIAProvider",
    "ReplicateProvider",
    "FalAIProvider",
    "HuggingFaceProvider",
    "RemotionImageProvider",
    # Video providers (priority order)
    "BytePlusProvider",
    "XAIProvider",
    "RemotionVideoProvider",
    "FFmpegSlideshowProvider",
    # LLM providers
    "GroqProvider",
    "OllamaProvider",
    # Fallback system
    "FallbackChain",
    "build_default_fallback_chain",
]
