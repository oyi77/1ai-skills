# Content Generator Skill - Comprehensive Implementation Plan

## Overview

Build a complete **End-to-End Automated Content Generation Platform** that supports:
- Single video generation
- Batch processing (multiple videos)
- Scheduled automated posting
- Multi-platform output (TikTok, YouTube, Instagram, Facebook)

## Use Cases

| Use Case | Description |
|----------|-------------|
| **One-off** | Generate 1 video from prompt |
| **Batch** | Generate 10+ videos for content calendar |
| **Automated** | Scheduled daily/weekly posting to social platforms |
| **Pipeline** | Full workflow: generate → edit → post |

---

## Architecture

### File Structure

```
content-generator/
├── SKILL.md                         # Skill definition for agents
├── README.md                        # User documentation  
├── config.yaml                      # Configuration template
├── content_calendar.yaml            # Batch/schedule config
├── scripts/
│   ├── __init__.py
│   ├── cli.py                       # CLI entry point
│   ├── generator.py                 # Core ContentGenerator
│   ├── batch_processor.py           # Batch processing
│   ├── scheduler.py                 # Scheduled posting
│   ├── platforms/                   # Social media integrations
│   │   ├── __init__.py
│   │   ├── tiktok.py
│   │   ├── youtube.py
│   │   ├── instagram.py
│   │   └── facebook.py
│   ├── providers/
│   │   ├── __init__.py
│   │   ├── base.py                  # Abstract AIProvider
│   │   ├── nvidia.py               # NVIDIA NIM (images)
│   │   ├── replicate.py             # Replicate (images)
│   │   ├── huggingface.py           # HuggingFace (images)
│   │   ├── byteplus.py              # BytePlus Seedance (video)
│   │   ├── xai.py                  # XAI Grok (video + editing)
│   │   ├── groq.py                 # Groq (LLM)
│   │   └── ollama.py               # Ollama (LLM)
│   ├── cache.py                     # SQLite caching
│   ├── cost_tracker.py              # Cost limits & tracking
│   ├── fallback.py                  # Fallback chain logic
│   ├── ffmpeg.py                    # Basic video processing
│   ├── ffmpeg_editor.py             # Advanced FFmpeg editing
│   ├── video_workflow.py           # AI + FFmpeg workflow
│   ├── upload.py                    # ImgBB uploader
│   ├── state.py                     # State management (resume)
│   └── storyboard.py               # Storyboard templates
├── references/
│   ├── nvidia-api.md
│   ├── byteplus-api.md
│   ├── xai-video-api.md
│   └── workflow.md
├── templates/                       # Storyboard templates
│   ├── ad_short.json
│   ├── product_showcase.json
│   ├── storytelling.json
│   └── tutorial.json
└── tests/
    ├── test_providers.py
    └── test_e2e.py
```

---

## Core Components

### 1. Multi-Platform Output

```python
# scripts/platforms/base.py
from enum import Enum
from dataclasses import dataclass

class Platform(Enum):
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"

@dataclass
class PlatformSpec:
    platform: Platform
    aspect_ratio: str      # "9:16", "16:9", "1:1"
    resolution: tuple     # (1080, 1920), (1920, 1080), etc.
    max_duration: int      # seconds
    ideal_duration: int    # optimal for algorithm
    format: str           # "mp4", "mov"
    fps: int
    bitrate: str

PLATFORM_SPECS = {
    Platform.TIKTOK: PlatformSpec(
        platform=Platform.TIKTOK,
        aspect_ratio="9:16",
        resolution=(1080, 1920),
        max_duration=180,
        ideal_duration=30,
        format="mp4",
        fps=30,
        bitrate="8000k"
    ),
    Platform.YOUTUBE: PlatformSpec(
        platform=Platform.YOUTUBE,
        aspect_ratio="16:9",
        resolution=(1920, 1080),
        max_duration=43200,  # 12 hours
        ideal_duration=600,  # 10 min
        format="mp4",
        fps=30,
        bitrate="20000k"
    ),
    Platform.INSTAGRAM: PlatformSpec(
        platform=Platform.INSTAGRAM,
        aspect_ratio="9:16",
        resolution=(1080, 1920),
        max_duration=60,
        ideal_duration=15,
        format="mp4",
        fps=30,
        bitrate="3500k"
    ),
    Platform.FACEBOOK: PlatformSpec(
        platform=Platform.FACEBOOK,
        aspect_ratio="16:9",
        resolution=(1920, 1080),
        max_duration=14400,  # 4 hours
        ideal_duration=120,
        format="mp4",
        fps=30,
        bitrate="10000k"
    ),
}
```

### 2. Storyboard Templates

```python
# scripts/storyboard.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class StoryboardTemplate:
    name: str
    description: str
    duration: int          # seconds
    scenes: list[dict]     # scene definitions
    
# Pre-defined templates
TEMPLATES = {
    "ad_short": StoryboardTemplate(
        name="Short Ad",
        description="Quick product advertisement (15-30s)",
        duration=30,
        scenes=[
            {"type": "hook", "duration": 3, "prompt_template": "{product} - attention grabber"},
            {"type": "problem", "duration": 5, "prompt_template": "Show the problem {pain_point}"},
            {"type": "solution", "duration": 7, "prompt_template": "{product} solves this"},
            {"type": "benefits", "duration": 10, "prompt_template": "Key benefits: {benefits}"},
            {"type": "cta", "duration": 5, "prompt_template": "Call to action: {cta}"},
        ]
    ),
    "product_showcase": StoryboardTemplate(
        name="Product Showcase",
        description="Detailed product feature showcase (30-60s)",
        duration=45,
        scenes=[
            {"type": "intro", "duration": 5, "prompt_template": "{product} unboxing/first look"},
            {"type": "feature_1", "duration": 10, "prompt_template": "Feature 1 demonstration"},
            {"type": "feature_2", "duration": 10, "prompt_template": "Feature 2 demonstration"},
            {"type": "feature_3", "duration": 10, "prompt_template": "Feature 3 demonstration"},
            {"type": "summary", "duration": 5, "prompt_template": "Quick summary"},
            {"type": "cta", "duration": 5, "prompt_template": "Link in bio CTA"},
        ]
    ),
    "storytelling": StoryboardTemplate(
        name="Storytelling",
        description="Narrative-driven content (60s+)",
        duration=60,
        scenes=[
            {"type": "setup", "duration": 10, "prompt_template": "Character setup {context}"},
            {"type": "conflict", "duration": 15, "prompt_template": "Challenge/problem appears"},
            {"type": "journey", "duration": 20, "prompt_template": "Journey to solution"},
            {"type": "resolution", "duration": 10, "prompt_template": "Solution found"},
            {"type": "message", "duration": 5, "prompt_template": "Key message takeaway"},
        ]
    ),
    "tutorial": StoryboardTemplate(
        name="Tutorial",
        description="How-to / educational content",
        duration=120,
        scenes=[
            {"type": "intro", "duration": 10, "prompt_template": "What you'll learn"},
            {"type": "step_1", "duration": 25, "prompt_template": "Step 1: {step_1}"},
            {"type": "step_2", "duration": 25, "prompt_template": "Step 2: {step_2}"},
            {"type": "step_3", "duration": 25, "prompt_template": "Step 3: {step_3}"},
            {"type": "conclusion", "duration": 15, "prompt_template": "Summary & next steps"},
            {"type": "cta", "duration": 20, "prompt_template": "Subscribe/follow CTA"},
        ]
    ),
}
```

### 3. Batch Processing

```python
# scripts/batch_processor.py
from dataclasses import dataclass
from typing import Optional
import asyncio

@dataclass
class BatchJob:
    job_id: str
    prompts: list[str]
    platform: Platform
    template: str
    strategy: str
    status: str  # pending, running, completed, failed
    results: list[dict]
    created_at: datetime
    completed_at: Optional[datetime]

class BatchProcessor:
    def __init__(self, generator: ContentGenerator):
        self.generator = generator
        self.jobs: dict[str, BatchJob] = {}
    
    async def process_batch(self, prompts: list[str],
                           platform: Platform,
                           template: str = "ad_short",
                           strategy: str = "balanced",
                           max_concurrent: int = 3) -> BatchJob:
        """Process multiple prompts with concurrency control"""
        job = BatchJob(
            job_id=generate_id(),
            prompts=prompts,
            platform=platform,
            template=template,
            strategy=strategy,
            status="running",
            results=[],
            created_at=now()
        )
        
        # Process with semaphore for concurrency
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def process_one(prompt: str):
            async with semaphore:
                result = await self.generator.generate(
                    prompt=prompt,
                    platform=platform,
                    template=template,
                    strategy=strategy
                )
                job.results.append(result)
                return result
        
        await asyncio.gather(*[process_one(p) for p in prompts])
        job.status = "completed"
        job.completed_at = now()
        
        return job
```

### 4. State Management (Resume Capability)

```python
# scripts/state.py
import json
import os
from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime

@dataclass
class GenerationState:
    state_id: str
    prompt: str
    platform: Platform
    template: str
    current_step: int        # 0=storyboard, 1=character, 2=product, 3=background, 4=video, 5=final
    step_results: dict       # Results from each step
    failed_step: Optional[int]
    error_message: Optional[str]
    created_at: datetime
    updated_at: datetime

class StateManager:
    STATE_DIR = ".content_generator_states"
    
    def __init__(self):
        os.makedirs(self.STATE_DIR, exist_ok=True)
    
    def save_state(self, state: GenerationState):
        """Save state for potential resume"""
        path = f"{self.STATE_DIR}/{state.state_id}.json"
        with open(path, 'w') as f:
            json.dump(asdict(state), f, default=str)
    
    def load_state(self, state_id: str) -> Optional[GenerationState]:
        """Load previous state"""
        path = f"{self.STATE_DIR}/{state_id}.json"
        if not os.path.exists(path):
            return None
        with open(path) as f:
            data = json.load(f)
        return GenerationState(**data)
    
    def resume_generation(self, state_id: str) -> dict:
        """Resume from failed step"""
        state = self.load_state(state_id)
        if not state:
            raise ValueError(f"State {state_id} not found")
        
        # Resume from failed step
        if state.failed_step == 1:  # Character failed
            state.step_results['character'] = await self.generate_character(...)
        # ... continue
        
        state.updated_at = now()
        self.save_state(state)
        return state.step_results
```

### 5. Scheduler (Automated Posting)

```python
# scripts/scheduler.py
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional
import time

@dataclass
class Schedule:
    schedule_id: str
    prompt: str
    platform: Platform
    template: str
    post_at: datetime          # When to post
    timezone: str             # "Asia/Jakarta"
    status: str               # scheduled, posted, failed
    posted_at: Optional[datetime]
    media_path: str           # Generated video path

class Scheduler:
    def __init__(self, generator: ContentGenerator):
        self.generator = generator
        self.schedules: list[Schedule] = []
    
    def schedule_post(self, prompt: str, platform: Platform,
                     post_at: datetime, template: str = "ad_short") -> Schedule:
        """Schedule a post for future"""
        schedule = Schedule(
            schedule_id=generate_id(),
            prompt=prompt,
            platform=platform,
            template=template,
            post_at=post_at,
            timezone="UTC",
            status="scheduled",
            posted_at=None,
            media_path=None
        )
        self.schedules.append(schedule)
        return schedule
    
    def run_scheduler(self):
        """Main scheduler loop"""
        while True:
            now = datetime.now()
            for schedule in self.schedules:
                if schedule.status == "scheduled" and now >= schedule.post_at:
                    self._execute_scheduled_post(schedule)
            time.sleep(60)  # Check every minute
    
    def _execute_scheduled_post(self, schedule: Schedule):
        """Generate and post"""
        # Generate video
        result = asyncio.run(self.generator.generate(
            prompt=schedule.prompt,
            platform=schedule.platform,
            template=schedule.template
        ))
        
        schedule.media_path = result['video']
        
        # Post to platform
        if schedule.platform == Platform.TIKTOK:
            self._post_tiktok(schedule)
        elif schedule.platform == Platform.YOUTUBE:
            self._post_youtube(schedule)
        # ...
        
        schedule.status = "posted"
        schedule.posted_at = datetime.now()
```

### 6. Video Editing (XAI Integration)

```python
# scripts/video_editor.py
class VideoEditor:
    def __init__(self, xai_provider):
        self.xai = xai_provider
    
    async def edit_video(self, video_path: str, 
                        edit_prompt: str) -> str:
        """Edit existing video with XAI"""
        result = await self.xai.edit_video(
            video_url=video_path,
            prompt=edit_prompt
        )
        return result.data['url']
    
    async def extend_video(self, video_path: str,
                          extension_prompt: str,
                          additional_seconds: int = 5) -> str:
        """Extend video duration"""
        # XAI supports up to 8.7s for editing
        pass
    
    async def change_style(self, video_path: str,
                         style: str) -> str:
        """Apply visual style"""
        # e.g., "cinematic", "vintage", "high contrast"
        pass
```

### 6. FFmpeg Video Editor (Advanced Editing)

```python
# scripts/ffmpeg_editor.py
from dataclasses import dataclass
from typing import Optional
from enum import Enum

class Transition(Enum):
    FADE = "fade"
    DISSOLVE = "dissolve"
    SLIDE_LEFT = "slide_left"
    SLIDE_RIGHT = "slide_right"
    ZOOM_IN = "zoom_in"
    WIPE = "wipe"

class TextPosition(Enum):
    TOP = "top"
    BOTTOM = "bottom"
    CENTER = "center"
    TOP_LEFT = "top_left"
    TOP_RIGHT = "top_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_RIGHT = "bottom_right"

@dataclass
class TextOverlay:
    text: str
    position: TextPosition
    font_size: int = 24
    font_color: str = "white"
    background_color: Optional[str] = None
    start_time: float = 0
    duration: Optional[float] = None

@dataclass
class FilterConfig:
    brightness: Optional[float] = None
    contrast: Optional[float] = None
    saturation: Optional[float] = None
    blur: Optional[int] = None
    vignette: bool = False
    grayscale: bool = False
    sepia: bool = False

class FFmpegEditor:
    """Advanced video editing using FFmpeg"""
    
    # ============ CUTTING & TRIMMING ============
    
    def trim(self, input_path: str, output_path: str,
             start: float, duration: Optional[float] = None) -> str:
        """Trim video: start time (seconds), optional duration"""
        pass
    
    def cut_scenes(self, input_path: str, output_path: str,
                   timestamps: list[tuple[float, float]]) -> str:
        """Cut multiple scenes: [(start1, end1), (start2, end2), ...]"""
        pass
    
    # ============ SPEED & MOTION ============
    
    def change_speed(self, input_path: str, output_path: str,
                    speed: float) -> str:
        """Change speed: 2.0 = 2x faster, 0.5 = 2x slower"""
        pass
    
    def slow_motion(self, input_path: str, output_path: str,
                    factor: float = 2.0) -> str:
        """Create slow motion effect"""
        pass
    
    # ============ TEXT & OVERLAYS ============
    
    def add_text(self, input_path: str, output_path: str,
                 overlays: list[TextOverlay]) -> str:
        """Add text overlays with positioning"""
        pass
    
    def add_subtitles(self, input_path: str, subtitle_path: str,
                      output_path: str) -> str:
        """Burn in subtitles from SRT/VTT"""
        pass
    
    def add_watermark(self, input_path: str, watermark_path: str,
                     output_path: str,
                     position: str = "top_right",
                     opacity: float = 0.5) -> str:
        """Add watermark/logo"""
        pass
    
    # ============ FILTERS & COLOR ============
    
    def apply_filters(self, input_path: str, output_path: str,
                     filters: FilterConfig) -> str:
        """Apply color/filters"""
        pass
    
    def color_grade(self, input_path: str, output_path: str,
                    preset: str = "cinematic") -> str:
        """Color grading presets: cinematic, warm, cool, vintage, B&W"""
        pass
    
    def add_vignette(self, input_path: str, output_path: str,
                    intensity: float = 0.5) -> str:
        """Add cinematic vignette"""
        pass
    
    # ============ TRANSITIONS ============
    
    def add_transition(self, clip1_path: str, clip2_path: str,
                      output_path: str,
                      transition: Transition = Transition.FADE,
                      duration: float = 1.0) -> str:
        """Add transition between two clips"""
        pass
    
    def create_transition_sequence(self, clips: list[str],
                                  output_path: str,
                                  transition: Transition = Transition.FADE,
                                  transition_duration: float = 0.5) -> str:
        """Create video from multiple clips with transitions"""
        pass
    
    # ============ AUDIO ============
    
    def add_music(self, input_path: str, music_path: str,
                  output_path: str,
                  volume: float = 0.3,
                  fade_in: float = 2.0,
                  fade_out: float = 2.0) -> str:
        """Add background music with fades"""
        pass
    
    def add_sound_effect(self, input_path: str, sfx_path: str,
                        output_path: str,
                        timestamp: float,
                        volume: float = 1.0) -> str:
        """Add sound effect at specific timestamp"""
        pass
    
    def mute_audio(self, input_path: str, output_path: str) -> str:
        """Remove audio track"""
        pass
    
    def extract_audio(self, input_path: str, output_path: str) -> str:
        """Extract audio to separate file"""
        pass
    
    # ============ COMPOSITION ============
    
    def resize(self, input_path: str, output_path: str,
              width: int, height: int) -> str:
        """Resize video"""
        pass
    
    def crop(self, input_path: str, output_path: str,
            x: int, y: int, width: int, height: int) -> str:
        """Crop video to specific region"""
        pass
    
    def convert_aspect_ratio(self, input_path: str, output_path: str,
                           target_ratio: str) -> str:
        """Convert between aspect ratios (9:16, 16:9, 1:1)"""
        pass
    
    def picture_in_picture(self, main_path: str, pip_path: str,
                          output_path: str,
                          position: str = "bottom_right",
                          size: float = 0.25) -> str:
        """Create PiP effect"""
        pass
    
    def split_screen(self, clips: list[str], output_path: str,
                    layout: str = "horizontal") -> str:
        """Split screen: horizontal, vertical, grid 2x2"""
        pass
    
    # ============ FORMATS ============
    
    def convert_format(self, input_path: str, output_path: str,
                      format: str = "mp4") -> str:
        """Convert between formats"""
        pass
    
    def compress(self, input_path: str, output_path: str,
                crf: int = 23) -> str:
        """Compress video file"""
        pass
    
    def generate_thumbnail(self, input_path: str, output_path: str,
                          timestamp: float = 0) -> str:
        """Generate thumbnail at specific time"""
        pass
    
    def generate_gif(self, input_path: str, output_path: str,
                    start: float, duration: float,
                    fps: int = 10, width: int = 480) -> str:
        """Create GIF from video segment"""
        pass
```

### 7. Combined Video Workflow

```python
# scripts/video_workflow.py
from ffpeg_editor import FFmpegEditor, Transition
from storyboard import StoryboardTemplate

class VideoWorkflow:
    """Combine AI generation + FFmpeg editing"""
    
    def __init__(self):
        self.editor = FFmpegEditor()
    
    async def create_from_template(self, template: StoryboardTemplate,
                                  ai_generator: ContentGenerator,
                                  platform: Platform) -> str:
        """Create video from storyboard template using AI"""
        
        # 1. Generate each scene with AI
        scenes = []
        for scene in template.scenes:
            scene_video = await ai_generator.generate_scene(
                prompt=scene["prompt_template"],
                duration=scene["duration"],
                platform=platform
            )
            scenes.append(scene_video)
        
        # 2. Concatenate with transitions
        raw_video = await self.editor.create_transition_sequence(
            clips=scenes,
            output_path="temp/raw.mp4",
            transition=Transition.FADE,
            transition_duration=0.5
        )
        
        # 3. Add text overlays
        if template.text_overlays:
            raw_video = await self.editor.add_text(
                input_path=raw_video,
                output_path="temp/with_text.mp4",
                overlays=template.text_overlays
            )
        
        # 4. Color grade
        graded = await self.editor.color_grade(
            input_path=raw_video,
            output_path="temp/graded.mp4",
            preset="cinematic"
        )
        
        # 5. Add music
        final = await self.editor.add_music(
            input_path=graded,
            music_path="assets/music/upbeat.mp3",
            output_path="output/final.mp4",
            volume=0.3,
            fade_in=2.0,
            fade_out=3.0
        )
        
        return final
    
    def quick_edit(self, input_path: str,
                   operations: list[dict]) -> str:
        """Quick edit pipeline"""
        current = input_path
        for op in operations:
            if op["op"] == "trim":
                current = self.editor.trim(current, "temp.mp4", 
                                         op["start"], op.get("duration"))
            elif op["op"] == "text":
                current = self.editor.add_text(current, "temp.mp4", op["overlays"])
            elif op["op"] == "music":
                current = self.editor.add_music(current, "temp.mp4", 
                                              op["music"], volume=op.get("volume", 0.3))
        return current
```

---

## Implementation Tasks

### Wave 1: Foundation (Essential)

1. **SKILL.md** - Skill definition
2. **config.yaml** - Main configuration
3. **Provider base class** - Abstract AIProvider
4. **Platform specs** - Multi-platform support

### Wave 2: Core Pipeline

5. **Cache system** - SQLite caching
6. **Cost tracker** - Budget management
7. **Fallback logic** - Provider chain
8. **State manager** - Resume capability

### Wave 3: Providers (Image)

9. **NVIDIA** - Flux/SD images
10. **Replicate** - SD 3.5
11. **HuggingFace** - Inference API

### Wave 4: Providers (Video + LLM)

12. **BytePlus** - Seedance video
13. **XAI** - Video + editing
14. **Groq** - LLM
15. **Ollama** - LLM

### Wave 5: Processing

16. **FFmpeg basic** - Slideshow, zoom effects, merge
17. **FFmpeg Editor** - Advanced editing (trim, text, filters, transitions)
18. **Video Workflow** - Combine AI + FFmpeg editing
19. **ImgBB** - Image upload
20. **Storyboard templates** - Pre-defined structures

### Wave 6: Advanced Features

21. **Batch processor** - Multiple videos
22. **Scheduler** - Automated posting
23. **Video editor** - XAI editing (alternative to FFmpeg)
24. **Platform integrations** - TikTok, YouTube, IG, FB

### Wave 7: CLI & Documentation

23. **CLI** - Full command interface
24. **README.md** - User guide
25. **Reference docs** - API docs

---

## Usage Examples

### Single Video Generation
```bash
python cli.py generate \
    --prompt "Create a 30s smartwatch ad" \
    --platform tiktok \
    --template ad_short \
    --strategy balanced \
    --output ./output
```

### Batch Processing
```bash
python cli.py batch \
    --prompts-file prompts.txt \
    --platform tiktok \
    --template ad_short \
    --max-concurrent 3 \
    --output ./batch_output
```

### Scheduled Posting
```python
from scheduler import Scheduler

scheduler = Scheduler(gen)
scheduler.schedule_post(
    prompt="Daily product feature",
    platform=Platform.TIKTOK,
    post_at=datetime(2025, 1, 1, 9, 0),  # 9 AM
    template="product_showcase"
)
scheduler.run_scheduler()
```

### Video Editing (XAI)
```python
from video_editor import VideoEditor

editor = VideoEditor(xai_provider)
edited = await editor.edit_video(
    video_path="original.mp4",
    edit_prompt="Make it more cinematic with better lighting"
)
```

### FFmpeg Video Editing (CLI)
```bash
# Trim video
python -m ffmpeg_editor trim input.mp4 --start 5 --duration 30 --output trimmed.mp4

# Add text overlay
python -m ffmpeg_editor text input.mp4 \
    --text "Limited Time Offer!" \
    --position bottom_center \
    --font-size 36 \
    --font-color white \
    --bg-color black@0.5 \
    --output with_text.mp4

# Add subtitles
python -m ffmpeg_editor subtitles input.mp4 --subs subtitles.srt --output with_subs.mp4

# Change speed (2x faster)
python -m ffmpeg_editor speed input.mp4 --factor 2.0 --output fast.mp4

# Slow motion (0.5x)
python -m ffmpeg_editor speed input.mp4 --factor 0.5 --output slowmo.mp4

# Color grading
python -m ffmpeg_editor color-grade input.mp4 --preset cinematic --output graded.mp4

# Add watermark
python -m ffmpeg_editor watermark input.mp4 --logo logo.png --position top_right --opacity 0.5 --output with_watermark.mp4

# Add background music
python -m ffmpeg_editor music input.mp4 --audio background.mp3 --volume 0.3 --fade-in 2 --fade-out 3 --output with_music.mp4

# Convert aspect ratio (16:9 -> 9:16 with blur)
python -m ffmpeg_editor convert-ratio input.mp4 --to 9:16 --output vertical.mp4

# Picture in Picture
python -m ffmpeg_editor pip main.mp4 --pip overlay.mp4 --position bottom_right --size 0.25 --output pip.mp4

# Split screen (2 videos side by side)
python -m ffmpeg_editor splitscreen clip1.mp4 clip2.mp4 --layout horizontal --output split.mp4

# Create GIF
python -m ffmpeg_editor gif input.mp4 --start 5 --duration 10 --fps 15 --width 480 --output preview.gif

# Compress video
python -m ffmpeg_editor compress input.mp4 --crf 28 --output compressed.mp4

# Quick edit pipeline (multiple operations)
python -m ffmpeg_editor pipeline input.mp4 \
    --ops trim:start=5:duration=30 \
    --ops text:text="Hello":position=bottom \
    --ops music:audio=bgm.mp3:volume=0.3 \
    --output final.mp4
```

### FFmpeg Video Editing (Python API)
```python
from ffpeg_editor import FFmpegEditor, TextOverlay, TextPosition, Transition, FilterConfig

editor = FFmpegEditor()

# Trim
editor.trim("input.mp4", "output.mp4", start=10, duration=30)

# Add text
editor.add_text("input.mp4", "output.mp4", [
    TextOverlay(
        text="Limited Time!",
        position=TextPosition.BOTTOM_CENTER,
        font_size=36,
        font_color="white",
        background_color="black@0.5",
        start_time=0,
        duration=5
    )
])

# Color grade
editor.color_grade("input.mp4", "output.mp4", preset="cinematic")

# Add music with fades
editor.add_music("input.mp4", "music.mp3", "output.mp4", 
                 volume=0.3, fade_in=2.0, fade_out=3.0)

# Convert to vertical (9:16)
editor.convert_aspect_ratio("input.mp4", "output.mp4", "9:16")

# Transition sequence
editor.create_transition_sequence(
    clips=["scene1.mp4", "scene2.mp4", "scene3.mp4"],
    output_path="final.mp4",
    transition=Transition.FADE,
    transition_duration=0.5
)
```

---

## Configuration

### config.yaml
```yaml
content_generation:
  strategy: "balanced"
  default_platform: "tiktok"
  
providers:
  nvidia:
    api_key: "${NVIDIA_API_KEY}"
    enabled: true
  byteplus:
    api_key: "${BYTEPLUS_API_KEY}"
    enabled: true
  # ...

cost_limits:
  max_per_generation: 1.0
  max_per_month: 100.0
  
platforms:
  tiktok:
    aspect_ratio: "9:16"
    resolution: [1080, 1920]
  youtube:
    aspect_ratio: "16:9"
    resolution: [1920, 1080]
```

### content_calendar.yaml (Batch)
```yaml
batch:
  prompts:
    - "Product 1 ad"
    - "Product 2 ad"
    - "Product 3 ad"
  platform: "tiktok"
  template: "ad_short"
  strategy: "balanced"
  max_concurrent: 3
```

---

## Success Criteria

- [ ] SKILL.md works with OpenCode agents
- [ ] Single video generation works
- [ ] Batch processing (10+ videos) works
- [ ] Scheduler posts automatically
- [ ] Multi-platform output (TikTok, YouTube, IG, FB)
- [ ] All providers implement AIProvider
- [ ] Fallback chain works
- [ ] Cost tracking enforces budget
- [ ] State management for resume
- [ ] Video editing with XAI
- [ ] FFmpeg editing (trim, text, filters, transitions)
- [ ] Storyboard templates
- [ ] CLI full-featured
- [ ] Tests cover critical paths
