"""FFmpeg slideshow video fallback provider.

LAST RESORT video provider - converts static images to video using FFmpeg.
Always works as long as FFmpeg is installed. Zero API dependency.
"""

import os
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Optional

from .base import AIProvider, ProviderType, GenerationResult


class FFmpegSlideshowProvider(AIProvider):
    """FFmpeg slideshow video provider - last resort fallback.

    Creates videos from static images using FFmpeg:
    - Smooth crossfade transitions between images
    - Ken Burns zoom/pan effect via zoompan filter
    - Background music overlay
    - Always works locally with no API calls
    """

    def __init__(self, **kwargs):
        super().__init__(
            provider_type=ProviderType.VIDEO,
            provider_name="FFmpeg Slideshow",
            api_key="local",
            **kwargs,
        )

    @property
    def supported_models(self) -> list[str]:
        return ["slideshow-crossfade", "slideshow-kenburns", "slideshow-simple"]

    async def generate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> GenerationResult:
        """Generate slideshow video from images.

        Args:
            prompt: Not used directly (images required)
            model: Style - slideshow-crossfade, slideshow-kenburns, slideshow-simple
            **kwargs:
                images: List of image file paths (required)
                output_path: Where to save the video
                duration_per_image: Seconds per image (default 5)
                audio_path: Optional background music
                width: Video width (default 1080)
                height: Video height (default 1920)
                fps: Frames per second (default 30)
        """
        model = model or "slideshow-kenburns"
        images = kwargs.get("images", [])

        if not images:
            return GenerationResult(
                success=False, provider=self.provider_name, model=model,
                metadata={"error": "No images provided for slideshow"},
            )

        # Validate images exist
        valid_images = [img for img in images if os.path.isfile(img)]
        if not valid_images:
            return GenerationResult(
                success=False, provider=self.provider_name, model=model,
                metadata={"error": "No valid image files found"},
            )

        output_path = kwargs.get("output_path")
        if not output_path:
            output_dir = Path(__file__).resolve().parents[4] / "output" / "ffmpeg_slideshow"
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = str(output_dir / f"slideshow_{int(time.time())}.mp4")

        duration_per = kwargs.get("duration_per_image", 5)
        width = kwargs.get("width", 1080)
        height = kwargs.get("height", 1920)
        fps = kwargs.get("fps", 30)
        audio_path = kwargs.get("audio_path")

        try:
            if model == "slideshow-kenburns":
                cmd = self._build_kenburns_cmd(
                    valid_images, output_path, duration_per, width, height, fps, audio_path
                )
            elif model == "slideshow-crossfade":
                cmd = self._build_crossfade_cmd(
                    valid_images, output_path, duration_per, width, height, fps, audio_path
                )
            else:
                cmd = self._build_simple_cmd(
                    valid_images, output_path, duration_per, width, height, fps, audio_path
                )

            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=300,
            )

            if result.returncode != 0:
                return GenerationResult(
                    success=False, provider=self.provider_name, model=model,
                    metadata={"error": result.stderr[:500]},
                )

            return GenerationResult(
                success=True,
                data=output_path,
                cost=0.0,
                provider=self.provider_name,
                model=model,
                metadata={
                    "local": True,
                    "image_count": len(valid_images),
                    "total_duration": duration_per * len(valid_images),
                },
            )

        except subprocess.TimeoutExpired:
            return GenerationResult(
                success=False, provider=self.provider_name, model=model,
                metadata={"error": "FFmpeg render timed out (5min)"},
            )
        except Exception as e:
            return GenerationResult(
                success=False, provider=self.provider_name, model=model,
                metadata={"error": str(e)},
            )

    def _build_kenburns_cmd(
        self, images, output, dur, w, h, fps, audio
    ) -> list[str]:
        """Ken Burns zoom/pan effect on each image."""
        # Create a concat file for input
        concat_file = self._write_concat_file(images, dur)

        filter_complex = (
            f"[0:v]scale={w*2}:{h*2},"
            f"zoompan=z='min(zoom+0.0015,1.5)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
            f":d={dur * fps}:s={w}x{h}:fps={fps}[v]"
        )

        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0", "-i", concat_file,
            "-filter_complex", filter_complex,
            "-map", "[v]",
            "-c:v", "libx264", "-preset", "fast",
            "-pix_fmt", "yuv420p",
            "-t", str(dur * len(images)),
        ]
        if audio and os.path.isfile(audio):
            cmd.extend(["-i", audio, "-map", "1:a", "-c:a", "aac", "-shortest"])
        cmd.append(output)
        return cmd

    def _build_crossfade_cmd(
        self, images, output, dur, w, h, fps, audio
    ) -> list[str]:
        """Simple crossfade transitions between images."""
        inputs = []
        for img in images:
            inputs.extend(["-loop", "1", "-t", str(dur), "-i", img])

        # Build xfade filter chain
        n = len(images)
        if n == 1:
            filter_str = f"[0:v]scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2[v]"
        else:
            parts = []
            for i in range(n):
                parts.append(f"[{i}:v]scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,setsar=1[s{i}]")

            xfade_parts = []
            prev = "s0"
            for i in range(1, n):
                out = f"x{i}" if i < n - 1 else "v"
                offset = i * dur - 1  # 1 second overlap
                xfade_parts.append(f"[{prev}][s{i}]xfade=transition=fade:duration=1:offset={offset}[{out}]")
                prev = out

            filter_str = ";".join(parts + xfade_parts)

        cmd = [
            "ffmpeg", "-y",
            *inputs,
            "-filter_complex", filter_str,
            "-map", "[v]",
            "-c:v", "libx264", "-preset", "fast",
            "-pix_fmt", "yuv420p",
        ]
        if audio and os.path.isfile(audio):
            cmd.extend(["-i", audio, "-map", f"{n}:a", "-c:a", "aac", "-shortest"])
        cmd.append(output)
        return cmd

    def _build_simple_cmd(
        self, images, output, dur, w, h, fps, audio
    ) -> list[str]:
        """Simple concatenation with no transitions."""
        concat_file = self._write_concat_file(images, dur)
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0", "-i", concat_file,
            "-vf", f"scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2",
            "-c:v", "libx264", "-preset", "fast",
            "-pix_fmt", "yuv420p",
            "-r", str(fps),
        ]
        if audio and os.path.isfile(audio):
            cmd.extend(["-i", audio, "-c:a", "aac", "-shortest"])
        cmd.append(output)
        return cmd

    def _write_concat_file(self, images: list[str], duration: float) -> str:
        """Write FFmpeg concat demuxer file."""
        fd, path = tempfile.mkstemp(suffix=".txt", prefix="ffmpeg_concat_")
        with os.fdopen(fd, "w") as f:
            for img in images:
                f.write(f"file '{img}'\n")
                f.write(f"duration {duration}\n")
            # Last image needs no duration
            f.write(f"file '{images[-1]}'\n")
        return path

    async def is_available(self) -> bool:
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"], capture_output=True, text=True, timeout=5,
            )
            return result.returncode == 0
        except Exception:
            return False

    def get_cost_estimate(self, prompt: str, model: Optional[str] = None, **kwargs) -> float:
        return 0.0

    def validate_api_key(self) -> bool:
        return True
