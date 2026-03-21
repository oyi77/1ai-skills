"""
AI Provider Registry — Universal AI Middleware
Exposes all registered providers and the registry singleton.
"""

from .base_provider import BaseProvider, ProviderCapability
from .provider_registry import ProviderRegistry, get_registry

from .kling_provider import KlingProvider
from .grok_provider import GrokProvider
from .flow_provider import FlowProvider
from .pixverse_provider import PixVerseProvider
from .postbridge_provider import PostBridgeProvider

__all__ = [
    "BaseProvider",
    "ProviderCapability",
    "ProviderRegistry",
    "get_registry",
    "KlingProvider",
    "GrokProvider",
    "FlowProvider",
    "PixVerseProvider",
    "PostBridgeProvider",
]
