# FFmpegEditor Class

Advanced video editing using FFmpeg subprocess calls.

## Overview

```python
from scripts.ffmpeg_editor import FFmpegEditor

editor = FFmpegEditor()
```

Provides comprehensive video editing capabilities including trimming, text overlays, filters, transitions, audio mixing, and composition.

## Constructor

```python
def __init__(self, ffmpeg_path: str = "ffmpeg", ffprobe_path: str = "ffprobe"):
```

**Parameters:**
- `ffmpeg_path` - Path to ffmpeg binary (default: 'ffmpeg')
- `ffprobe_path` - Path to ffprobe binary (default: 'ffprobe')

---

## Enums

### Transition

Video transition types.

```python
class Transition(Enum):
    FADE = "fade"
    DISSOLVE = "dissolve"
    SLIDE_LEFT = "slide_left"
    SLIDE_RIGHT = "slide_right"
    ZOOM_IN = "zoom_in"
    WIPE = "wipe"
```

### TextPosition

Text positioning options.

```python
class TextPosition(Enum):
    TOP = "top"
    BOTTOM = "bottom"
    CENTER = "center"
    TOP_LEFT = "top_left"
    TOP_RIGHT = "top_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_RIGHT = "bottom_right"
```

---

## Dataclasses

### TextOverlay

Text overlay configuration.

```python
@dataclass
class TextOverlay:
    text: str
    position: TextPosition
    font_size: int = 24
    font_color: str = "white"
    background_color: Optional[str] = None
    start_time: float = 0
    duration: Optional[float] = None
    font: str = "Sans"
```

### FilterConfig

Video filter configuration.

```python
@dataclass
class FilterConfig:
    brightness: Optional[float] = None      # -1 to 1
    contrast: Optional[float] = None        # 0 to 2
    saturation: Optional[float] = None      # 0 to 3
    blur: Optional[int] = None
    vignette: bool = False
    grayscale: bool = False
    sepia: bool = False
    sharpness: Optional[float] = None
    gamma: Optional[float] = None
```

---

## Methods

### Cutting & Trimming

#### trim()

Trim video to specified start time and optional duration.

```python
def trim(
    self,
    input_path: str,
    output_path: str,
    start: float,
    duration: Optional[float] = None,
) -> str
```

#### cut_scenes()

Cut multiple scenes from video.

```python
def cut_scenes(
    self,
    input_path: str,
    output_path: str,
    timestamps: list[tuple[float, float]],
) -> str
```

### Speed & Motion

#### change_speed()

Change video playback speed.

```python
def change_speed(
    self,
    input_path: str,
    output_path: str,
    speed: float,
) -> str
```

**Parameters:**
- `speed` - Speed factor (2.0 = 2x faster, 0.5 = 2x slower)

#### slow_motion()

Create slow motion effect.

```python
def slow_motion(
    self,
    input_path: str,
    output_path: str,
    factor: float = 2.0,
) -> str
```

### Text & Overlays

#### add_text()

Add text overlays to video.

```python
def add_text(
    self,
    input_path: str,
    output_path: str,
    overlays: list[TextOverlay],
) -> str
```

#### add_subtitles()

Burn subtitles into video from SRT/VTT file.

```python
def add_subtitles(
    self,
    input_path: str,
    subtitle_path: str,
    output_path: str,
) -> str
```

#### add_watermark()

Add watermark/logo overlay.

```python
def add_watermark(
    self,
    input_path: str,
    watermark_path: str,
    output_path: str,
    position: str = "top_right",
    opacity: float = 0.5,
) -> str
```

### Filters & Color

#### apply_filters()

Apply video filters.

```python
def apply_filters(
    self,
    input_path: str,
    output_path: str,
    filters: FilterConfig,
) -> str
```

#### color_grade()

Apply color grading presets.

```python
def color_grade(
    self,
    input_path: str,
    output_path: str,
    preset: str = "cinematic",
) -> str
```

**Presets:** `cinematic`, `warm`, `cool`, `vintage`, `B&W`

#### add_vignette()

Add cinematic vignette effect.

```python
def add_vignette(
    self,
    input_path: str,
    output_path: str,
    intensity: float = 0.5,
) -> str
```

### Transitions

#### add_transition()

Add transition between two video clips.

```python
def add_transition(
    self,
    clip1_path: str,
    clip2_path: str,
    output_path: str,
    transition: Transition = Transition.FADE,
    duration: float = 1.0,
) -> str
```

#### create_transition_sequence()

Create video from multiple clips with transitions.

```python
def create_transition_sequence(
    self,
    clips: list[str],
    output_path: str,
    transition: Transition = Transition.FADE,
    transition_duration: float = 0.5,
) -> str
```

### Audio

#### add_music()

Add background music with fade in/out.

```python
def add_music(
    self,
    input_path: str,
    music_path: str,
    output_path: str,
    volume: float = 0.3,
    fade_in: float = 2.0,
    fade_out: float = 2.0,
) -> str
```

#### add_sound_effect()

Add sound effect at specific timestamp.

```python
def add_sound_effect(
    self,
    input_path: str,
    sfx_path: str,
    output_path: str,
    timestamp: float,
    volume: float = 1.0,
) -> str
```

#### mute_audio()

Remove audio track from video.

```python
def mute_audio(
    self,
    input_path: str,
    output_path: str,
) -> str
```

#### extract_audio()

Extract audio to separate file.

```python
def extract_audio(
    self,
    input_path: str,
    output_path: str,
) -> str
```

### Composition

#### resize()

Resize video to specific resolution.

```python
def resize(
    self,
    input_path: str,
    output_path: str,
    width: int,
    height: int,
) -> str
```

#### crop()

Crop video to specific region.

```python
def crop(
    self,
    input_path: str,
    output_path: str,
    x: int,
    y: int,
    width: int,
    height: int,
) -> str
```

#### convert_aspect_ratio()

Convert video between aspect ratios.

```python
def convert_aspect_ratio(
    self,
    input_path: str,
    output_path: str,
    target_ratio: str,
) -> str
```

**Target ratios:** `"9:16"`, `"16:9"`, `"1:1"`, `"4:3"`

#### picture_in_picture()

Create picture-in-picture effect.

```python
def picture_in_picture(
    self,
    main_path: str,
    pip_path: str,
    output_path: str,
    position: str = "bottom_right",
    size: float = 0.25,
) -> str
```

#### split_screen()

Create split screen video from multiple clips.

```python
def split_screen(
    self,
    clips: list[str],
    output_path: str,
    layout: str = "horizontal",
) -> str
```

**Layouts:** `horizontal`, `vertical`, `grid`

### Formats

#### convert_format()

Convert video between formats.

```python
def convert_format(
    self,
    input_path: str,
    output_path: str,
    format: str = "mp4",
) -> str
```

**Formats:** `mp4`, `mov`, `avi`, `webm`, `mkv`

#### compress()

Compress video file.

```python
def compress(
    self,
    input_path: str,
    output_path: str,
    crf: int = 23,
) -> str
```

**Parameters:**
- `crf` - Constant Rate Factor (0-51, lower = better quality, default 23)

#### generate_thumbnail()

Generate thumbnail at specific time.

```python
def generate_thumbnail(
    self,
    input_path: str,
    output_path: str,
    timestamp: float = 0,
) -> str
```

#### generate_gif()

Create GIF from video segment.

```python
def generate_gif(
    self,
    input_path: str,
    output_path: str,
    start: float,
    duration: float,
    fps: int = 10,
    width: int = 480,
) -> str
```

### Utility Methods

#### concatenate()

Concatenate multiple video clips.

```python
def concatenate(
    self,
    clips: list[str],
    output_path: str,
    method: str = "concat",
) -> str
```

#### reverse()

Reverse video (play backwards).

```python
def reverse(
    self,
    input_path: str,
    output_path: str,
) -> str
```

#### loop()

Loop video multiple times.

```python
def loop(
    self,
    input_path: str,
    output_path: str,
    count: int = 2,
) -> str
```

---

## Usage Example

```python
from scripts.ffmpeg_editor import (
    FFmpegEditor,
    TextOverlay,
    TextPosition,
    FilterConfig,
    Transition
)

editor = FFmpegEditor()

# Trim and add text
editor.trim("input.mp4", "trimmed.mp4", start=5, duration=30)

editor.add_text(
    "trimmed.mp4",
    "output.mp4",
    overlays=[
        TextOverlay(
            text="My Video",
            position=TextPosition.TOP,
            font_size=48,
            font_color="white"
        )
    ]
)

# Apply filters
editor.apply_filters(
    "output.mp4",
    "filtered.mp4",
    FilterConfig(
        brightness=0.1,
        contrast=1.1,
        saturation=1.2
    )
)

# Color grade
editor.color_grade("filtered.mp4", "graded.mp4", preset="cinematic")

# Add music
editor.add_music(
    "graded.mp4",
    "music.mp3",
    "final.mp4",
    volume=0.3,
    fade_in=2,
    fade_out=2
)

# Resize for TikTok
editor.resize("final.mp4", "tiktok.mp4", width=1080, height=1920)

# Create split screen
editor.split_screen(
    ["clip1.mp4", "clip2.mp4"],
    "split.mp4",
    layout="horizontal"
)
```
