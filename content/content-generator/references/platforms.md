# Platforms Module

Defines platform specifications for social media platforms.

## Platform Enum

Supported social media platforms for content publishing.

```python
class Platform(Enum):
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
```

**Values:**
- `TIKTOK` - Short-form video platform (vertical 9:16)
- `YOUTUBE` - Long-form video platform (horizontal 16:9)
- `INSTAGRAM` - Multi-format platform (Reels, Feed, Stories)
- `FACEBOOK` - Video and Reels platform

---

## PlatformSpec Dataclass

Specifications for a social media platform's video requirements.

```python
@dataclass
class PlatformSpec:
    platform: Platform
    aspect_ratio: str
    resolution: tuple[int, int]
    max_duration: Optional[int]
    ideal_duration: int
    format: str
    fps: int
    bitrate: int
```

**Attributes:**
- `platform` - The platform enum value
- `aspect_ratio` - Video aspect ratio (e.g., "9:16", "16:9")
- `resolution` - Video resolution tuple (width, height)
- `max_duration` - Maximum video duration in seconds (None for unlimited)
- `ideal_duration` - Ideal video duration in seconds for best performance
- `format` - Video format (e.g., "mp4", "mov")
- `fps` - Frames per second
- `bitrate` - Video bitrate in kbps

---

## Platform Specifications

### TikTok

```python
PLATFORM_SPECS[Platform.TIKTOK]
```

| Property | Value |
|----------|-------|
| Aspect Ratio | 9:16 |
| Resolution | 1080x1920 |
| Max Duration | 180 seconds |
| Ideal Duration | 30 seconds |
| Format | mp4 |
| FPS | 30 |
| Bitrate | 8000 kbps |

---

### YouTube

```python
PLATFORM_SPECS[Platform.YOUTUBE]
```

| Property | Value |
|----------|-------|
| Aspect Ratio | 16:9 |
| Resolution | 1920x1080 |
| Max Duration | None (unlimited) |
| Ideal Duration | 600 seconds |
| Format | mp4 |
| FPS | 30 |
| Bitrate | 12000 kbps |

---

### Instagram

```python
PLATFORM_SPECS[Platform.INSTAGRAM]
```

| Property | Value |
|----------|-------|
| Aspect Ratio | 9:16 |
| Resolution | 1080x1920 |
| Max Duration | 90 seconds |
| Ideal Duration | 30 seconds |
| Format | mp4 |
| FPS | 30 |
| Bitrate | 6000 kbps |

---

### Facebook

```python
PLATFORM_SPECS[Platform.FACEBOOK]
```

| Property | Value |
|----------|-------|
| Aspect Ratio | 16:9 |
| Resolution | 1920x1080 |
| Max Duration | 240 seconds |
| Ideal Duration | 60 seconds |
| Format | mp4 |
| FPS | 30 |
| Bitrate | 8000 kbps |

---

## Usage Example

```python
from scripts.platforms.base import Platform, PlatformSpec, PLATFORM_SPECS

# Get platform spec
tiktok_spec = PLATFORM_SPECS[Platform.TIKTOK]

print(f"Resolution: {tiktok_spec.resolution}")
print(f"Aspect Ratio: {tiktok_spec.aspect_ratio}")
print(f"Max Duration: {tiktok_spec.max_duration}s")

# Iterate all platforms
for platform, spec in PLATFORM_SPECS.items():
    print(f"{platform.value}: {spec.resolution}")
```

---

## Adding Custom Platforms

To add a new platform, create a new Platform value and PlatformSpec:

```python
class Platform(Enum):
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    CUSTOM = "custom"  # Add new platform

PLATFORM_SPECS[Platform.CUSTOM] = PlatformSpec(
    platform=Platform.CUSTOM,
    aspect_ratio="1:1",
    resolution=(1080, 1080),
    max_duration=60,
    ideal_duration=30,
    format="mp4",
    fps=30,
    bitrate=6000,
)
```
