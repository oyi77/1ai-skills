# FFmpeg Functions

Basic FFmpeg operations for video processing.

## Overview

```python
from scripts import ffmpeg
```

This module provides fundamental video processing functions using FFmpeg subprocess calls.

---

## Functions

### slideshow_from_images()

Create a slideshow from a list of images.

```python
def slideshow_from_images(
    image_paths: list[str],
    output_path: str,
    duration_per_image: float = 3.0,
    fps: int = 30,
    transition: str = "fade",
    transition_duration: float = 0.5,
    resolution: Optional[tuple[int, int]] = None,
    audio_path: Optional[str] = None,
) -> str
```

**Parameters:**
- `image_paths` - List of image file paths
- `output_path` - Output video path
- `duration_per_image` - Duration each image displays (default: 3.0 seconds)
- `fps` - Frames per second (default: 30)
- `transition` - Transition type (default: "fade")
- `transition_duration` - Duration of transition effect (default: 0.5)
- `resolution` - Optional (width, height) tuple
- `audio_path` - Optional background audio file

**Returns:** Output path on success

**Raises:**
- `ValueError` - If no images provided or image not found
- `RuntimeError` - If FFmpeg fails

---

### merge_videos()

Merge multiple videos into one.

```python
def merge_videos(
    video_paths: list[str],
    output_path: str,
    method: str = "concat",
) -> str
```

**Parameters:**
- `video_paths` - List of video file paths
- `output_path` - Output video path
- `method` - Merge method (default: "concat")

**Returns:** Output path on success

**Raises:**
- `ValueError` - If no videos provided or video not found

---

### apply_zoom_effect()

Apply zoom/pan effect to video.

```python
def apply_zoom_effect(
    input_path: str,
    output_path: str,
    zoom_level: float = 1.5,
    duration: Optional[float] = None,
    x: int = 0,
    y: int = 0,
) -> str
```

**Parameters:**
- `input_path` - Source video path
- `output_path` - Output video path
- `zoom_level` - Zoom level (default: 1.5)
- `duration` - Optional video duration (auto-detected if None)
- `x` - Horizontal pan percentage (default: 0)
- `y` - Vertical pan percentage (default: 0)

**Returns:** Output path on success

---

### trim_video()

Trim video to a specific time range.

```python
def trim_video(
    input_path: str,
    output_path: str,
    start: float = 0,
    duration: Optional[float] = None,
) -> str
```

**Parameters:**
- `input_path` - Source video path
- `output_path` - Output video path
- `start` - Start time in seconds (default: 0)
- `duration` - Optional duration in seconds

**Returns:** Output path on success

---

### convert_format()

Convert video format/codec.

```python
def convert_format(
    input_path: str,
    output_path: str,
    codec: Optional[str] = None,
    bitrate: Optional[str] = None,
    resolution: Optional[tuple[int, int]] = None,
    fps: Optional[int] = None,
) -> str
```

**Parameters:**
- `input_path` - Source video path
- `output_path` - Output video path
- `codec` - Video codec (e.g., "libx264")
- `bitrate` - Video bitrate (e.g., "5000k")
- `resolution` - Optional (width, height) tuple
- `fps` - Optional frames per second

**Returns:** Output path on success

---

### extract_frames()

Extract frames from video as images.

```python
def extract_frames(
    input_path: str,
    output_dir: str,
    fps: Optional[int] = None,
    start: float = 0,
    duration: Optional[float] = None,
    pattern: str = "frame_%04d.png",
) -> list[str]
```

**Parameters:**
- `input_path` - Source video path
- `output_dir` - Directory to save frames
- `fps` - Frames per second to extract (default: 1)
- `start` - Start time in seconds (default: 0)
- `duration` - Optional duration to extract
- `pattern` - Output filename pattern (default: "frame_%04d.png")

**Returns:** List of extracted frame file paths

---

## Internal Functions

### _run_ffmpeg()

Internal function to run FFmpeg commands.

```python
def _run_ffmpeg(
    args: list, capture_output: bool = False
) -> subprocess.CompletedProcess
```

**Parameters:**
- `args` - FFmpeg command arguments
- `capture_output` - Whether to capture output

**Returns:** CompletedProcess object

**Raises:** RuntimeError if FFmpeg fails

---

## Usage Example

```python
from scripts import ffmpeg

# Create slideshow from images
ffmpeg.slideshow_from_images(
    image_paths=["img1.jpg", "img2.jpg", "img3.jpg"],
    output_path="slideshow.mp4",
    duration_per_image=3.0,
    audio_path="background.mp3"
)

# Trim video
ffmpeg.trim_video(
    input_path="long_video.mp4",
    output_path="short_video.mp4",
    start=10,
    duration=30
)

# Convert format
ffmpeg.convert_format(
    input_path="video.avi",
    output_path="video.mp4",
    codec="libx264",
    resolution=(1920, 1080)
)

# Extract frames
frames = ffmpeg.extract_frames(
    input_path="video.mp4",
    output_dir="frames",
    fps=1
)
print(f"Extracted {len(frames)} frames")
```
