"""
AI Interceptor — Universal AI Middleware for BerkahKarya Skills
Global, provider-agnostic, cross-platform.
"""
from .ai_interceptor import AIInterceptor, LLMClient, get_interceptor, intercept
from .adb_interceptor import ADBInterceptor, get_adb_interceptor
from .video_enhancer import VideoEnhancer

__all__ = [
    # Core middleware
    "AIInterceptor",
    "LLMClient",
    "get_interceptor",
    "intercept",
    # Platform-specific
    "ADBInterceptor",
    "get_adb_interceptor",
    # Post-processing
    "VideoEnhancer",
]
