"""Video Workflow Module - Combines AI Generation + FFmpeg Editing."""

import os
import asyncio
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .ffmpeg_editor import FFmpegEditor, TextOverlay, FilterConfig
from .providers import AIProvider


@dataclass
class StoryboardScene:
    """A single scene in a storyboard template."""

    prompt: str
    duration: float = 3.0
    text_overlay: Optional[str] = None
    transition: str = "fade"


@dataclass
class StoryboardTemplate:
    """A storyboard template for video creation."""

    name: str
    scenes: list[StoryboardScene] = field(default_factory=list)
    resolution: tuple[int, int] = (1920, 1080)
    fps: int = 30
    aspect_ratio: str = "16:9"
    music: Optional[str] = None
    style: str = "cinematic"


@dataclass
class VideoWorkflowResult:
    """Result of a video workflow operation."""

    success: bool
    output_path: Optional[str] = None
    scenes_generated: int = 0
    total_duration: float = 0.0
    cost: float = 0.0
    error: Optional[str] = None


class VideoWorkflow:
    """Video workflow that combines AI generation + FFmpeg editing."""

    def __init__(
        self,
        image_provider: Optional[AIProvider] = None,
        video_provider: Optional[AIProvider] = None,
        ffmpeg_path: str = "ffmpeg",
        ffprobe_path: str = "ffprobe",
        output_dir: str = "output",
    ):
        self.image_provider = image_provider
        self.video_provider = video_provider
        self.editor = FFmpegEditor(ffmpeg_path, ffprobe_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def _generate_scene_image(
        self, prompt: str, scene_index: int
    ) -> Optional[str]:
        """Generate an image for a scene using the image provider."""
        if not self.image_provider:
            return None

        try:
            result = await self.image_provider.generate(
                prompt=prompt,
                model=self.image_provider.get_default_model(),
            )

            if result.success and result.data:
                return result.data
        except Exception:
            pass

        return None

    def create_from_template(
        self,
        template: StoryboardTemplate,
        output_name: str,
    ) -> VideoWorkflowResult:
        """Create a video from a storyboard template."""
        output_path = str(self.output_dir / f"{output_name}.mp4")
        scene_clips = []
        total_cost = 0.0

        try:
            for i, scene in enumerate(template.scenes):
                scene_content = asyncio.run(self._generate_scene_image(scene.prompt, i))

                if scene_content and self.image_provider:
                    cost = self.image_provider.get_cost_estimate(scene.prompt)
                    total_cost += cost

            if not scene_clips:
                return VideoWorkflowResult(
                    success=False,
                    error="No scene content generated. Ensure AI providers are configured.",
                    cost=total_cost,
                )

            self.editor.concatenate(scene_clips, output_path)

            if template.style:
                styled_path = str(self.output_dir / f"{output_name}_styled.mp4")
                self.editor.color_grade(output_path, styled_path, template.style)
                os.replace(styled_path, output_path)

            if template.music and os.path.exists(template.music):
                with_music_path = str(self.output_dir / f"{output_name}_with_music.mp4")
                self.editor.add_music(output_path, template.music, with_music_path)
                os.replace(with_music_path, output_path)

            total_duration = sum(scene.duration for scene in template.scenes)

            return VideoWorkflowResult(
                success=True,
                output_path=output_path,
                scenes_generated=len(template.scenes),
                total_duration=total_duration,
                cost=total_cost,
            )

        except Exception as e:
            return VideoWorkflowResult(
                success=False,
                error=str(e),
                cost=total_cost,
            )

    def quick_edit(
        self,
        input_path: str,
        output_name: str,
        text_overlays: Optional[list[TextOverlay]] = None,
        filters: Optional[FilterConfig] = None,
        add_music: Optional[str] = None,
        style: Optional[str] = None,
        resize: Optional[tuple[int, int]] = None,
        trim_start: Optional[float] = None,
        trim_end: Optional[float] = None,
    ) -> VideoWorkflowResult:
        """Quick edit pipeline for video enhancement."""
        output_path = str(self.output_dir / f"{output_name}.mp4")
        current_path = input_path

        try:
            if trim_start is not None or trim_end is not None:
                start = trim_start or 0
                duration = (trim_end - trim_start) if trim_start and trim_end else None
                trimmed_path = str(self.output_dir / f"{output_name}_trimmed.mp4")
                self.editor.trim(input_path, trimmed_path, start, duration)
                current_path = trimmed_path

            if resize:
                resized_path = str(self.output_dir / f"{output_name}_resized.mp4")
                self.editor.resize(current_path, resized_path, resize[0], resize[1])
                current_path = resized_path

            if filters:
                filtered_path = str(self.output_dir / f"{output_name}_filtered.mp4")
                self.editor.apply_filters(current_path, filtered_path, filters)
                current_path = filtered_path

            if style:
                styled_path = str(self.output_dir / f"{output_name}_styled.mp4")
                self.editor.color_grade(current_path, styled_path, style)
                current_path = styled_path

            if text_overlays:
                text_path = str(self.output_dir / f"{output_name}_text.mp4")
                self.editor.add_text(current_path, text_path, text_overlays)
                current_path = text_path

            if add_music and os.path.exists(add_music):
                music_path = str(self.output_dir / f"{output_name}_music.mp4")
                self.editor.add_music(current_path, add_music, music_path)
                current_path = music_path

            os.replace(current_path, output_path)
            duration = self.editor._get_video_duration(output_path)

            return VideoWorkflowResult(
                success=True,
                output_path=output_path,
                total_duration=duration,
            )

        except Exception as e:
            return VideoWorkflowResult(
                success=False,
                error=str(e),
            )


async def create_video_from_prompts(
    prompts: list[str],
    provider: AIProvider,
    output_path: str,
    duration_per_scene: float = 3.0,
) -> VideoWorkflowResult:
    """Create a video from a list of image generation prompts."""
    scenes = [
        StoryboardScene(prompt=prompt, duration=duration_per_scene)
        for prompt in prompts
    ]

    template = StoryboardTemplate(name="auto_generated", scenes=scenes)
    workflow = VideoWorkflow(image_provider=provider)
    output_name = Path(output_path).stem
    return workflow.create_from_template(template, output_name)


def quick_trim(
    input_path: str,
    output_path: str,
    start: float,
    duration: Optional[float] = None,
) -> str:
    """Quick video trimming using FFmpeg."""
    editor = FFmpegEditor()
    return editor.trim(input_path, output_path, start, duration)


def quick_watermark(
    input_path: str,
    output_path: str,
    watermark_path: str,
    position: str = "bottom_right",
    opacity: float = 0.5,
) -> str:
    """Quick watermark addition."""
    editor = FFmpegEditor()
    return editor.add_watermark(
        input_path, watermark_path, output_path, position, opacity
    )
