"""Platform specifications for social media platforms.

This module defines the Platform enum and PlatformSpec dataclass
with configuration for each supported social media platform.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Platform(Enum):
    """Supported social media platforms for content publishing.

    Attributes:
        TIKTOK: Short-form video platform (vertical 9:16)
        YOUTUBE: Long-form video platform (horizontal 16:9)
        INSTAGRAM: Multi-format platform (Reels, Feed, Stories)
        FACEBOOK: Video and Reels platform
    """

    TIKTOK = "tiktok"
    YOUTUBE = "youtube"
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"


@dataclass
class PlatformSpec:
    """Specifications for a social media platform's video requirements.

    Attributes:
        platform: The platform enum value
        aspect_ratio: Video aspect ratio (e.g., "9:16", "16:9")
        resolution: Video resolution tuple (width, height)
        max_duration: Maximum video duration in seconds (None for unlimited)
        ideal_duration: Ideal video duration in seconds for best performance
        format: Video format (e.g., "mp4", "mov")
        fps: Frames per second
        bitrate: Video bitrate in kbps
    """

    platform: Platform
    aspect_ratio: str
    resolution: tuple[int, int]
    max_duration: Optional[int]
    ideal_duration: int
    format: str
    fps: int
    bitrate: int


PLATFORM_SPECS: dict[Platform, PlatformSpec] = {
    Platform.TIKTOK: PlatformSpec(
        platform=Platform.TIKTOK,
        aspect_ratio="9:16",
        resolution=(1080, 1920),
        max_duration=180,
        ideal_duration=30,
        format="mp4",
        fps=30,
        bitrate=8000,
    ),
    Platform.YOUTUBE: PlatformSpec(
        platform=Platform.YOUTUBE,
        aspect_ratio="16:9",
        resolution=(1920, 1080),
        max_duration=None,
        ideal_duration=600,
        format="mp4",
        fps=30,
        bitrate=12000,
    ),
    Platform.INSTAGRAM: PlatformSpec(
        platform=Platform.INSTAGRAM,
        aspect_ratio="9:16",
        resolution=(1080, 1920),
        max_duration=90,
        ideal_duration=30,
        format="mp4",
        fps=30,
        bitrate=6000,
    ),
    Platform.FACEBOOK: PlatformSpec(
        platform=Platform.FACEBOOK,
        aspect_ratio="16:9",
        resolution=(1920, 1080),
        max_duration=240,
        ideal_duration=60,
        format="mp4",
        fps=30,
        bitrate=8000,
    ),
}
