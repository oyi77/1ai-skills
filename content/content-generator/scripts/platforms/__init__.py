"""Platform package for social media content generation.

This package contains platform specifications for different social media
platforms (TikTok, YouTube, Instagram, Facebook) with their respective
video requirements and constraints.
"""

from .base import Platform, PlatformSpec, PLATFORM_SPECS

__all__ = [
    "Platform",
    "PlatformSpec",
    "PLATFORM_SPECS",
]
