"""
Content Kingdom — Video Producer Module
========================================
Covers capabilities from deprecated skills:
- video-production (video editing via FFmpeg)
- tiktok-slideshow (image slideshow for TikTok)
- youtube-factory (full YouTube video generation)
- content-factory (content → video pipeline)

Uses GeminiGen API (Grok) as primary, FFmpeg for post-processing.
"""

import json
import subprocess
import shutil
import time
import tempfile
from pathlib import Path
from typing import Optional

# FFmpeg check
FFMPEG = shutil.which("ffmpeg")


class VideoProducer:
    """Unified video production — covers all deprecated video skills."""

    def __init__(self, geminigen_client=None):
        """
        Args:
            geminigen_client: GeminiGenClient instance (optional, lazy-loaded)
        """
        self._client = geminigen_client

    @property
    def client(self):
        if self._client is None:
            from .geminigen_client import GeminiGenClient

            self._client = GeminiGenClient()
        return self._client

    # ── Video Generation (replaces geminigen-video, content-factory) ──────

    def generate_video(
        self,
        prompt: str,
        duration: int = 6,
        aspect_ratio: str = "portrait",
        model: str = "grok-3",
        ref_image_url: str = None,
    ) -> dict:
        """Generate AI video via GeminiGen Grok API."""
        file_urls = [ref_image_url] if ref_image_url else None
        return self.client.generate_video_grok(
            prompt=prompt,
            model=model,
            aspect_ratio=aspect_ratio,
            duration=duration,
            file_urls=file_urls,
        )

    def generate_product_video(
        self,
        product_name: str,
        hook: str,
        duration: int = 6,
    ) -> dict:
        """Generate a product promo video using Veris design principles."""
        from .veris_design import build_video_prompt

        params = build_video_prompt(product_name, hook, duration)
        return self.client.generate_video_grok(
            prompt=params["prompt"],
            model=params.get("model", "grok-3"),
            aspect_ratio=params.get("aspect_ratio", "portrait"),
            duration=duration,
        )

    # ── Slideshow (replaces tiktok-slideshow) ────────────────────────────

    def create_slideshow(
        self,
        image_paths: list[str],
        output_path: str,
        duration_per_image: float = 3.0,
        transition: str = "fade",
        music_path: str = None,
        fps: int = 30,
    ) -> Optional[str]:
        """
        Create video slideshow from images via FFmpeg.
        Replaces: tiktok-slideshow.

        Args:
            image_paths: List of image file paths
            output_path: Output video file path
            duration_per_image: Seconds per image
            transition: "fade", "none", "slide"
            music_path: Optional background music
            fps: Frames per second

        Returns:
            Output path if successful, None if failed
        """
        if not FFMPEG:
            print("❌ FFmpeg not installed")
            return None

        if not image_paths:
            print("❌ No images provided")
            return None

        try:
            # Create concat file
            concat_path = Path(output_path).parent / "concat_list.txt"
            with open(concat_path, "w") as f:
                for img in image_paths:
                    f.write(f"file '{img}'\n")
                    f.write(f"duration {duration_per_image}\n")
                # Repeat last image for duration
                f.write(f"file '{image_paths[-1]}'\n")

            cmd = [
                FFMPEG,
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_path),
                "-vf",
                f"fps={fps},format=yuv420p",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
            ]

            if music_path and Path(music_path).exists():
                cmd.extend(["-i", music_path, "-c:a", "aac", "-shortest"])

            cmd.append(output_path)

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

            # Cleanup
            concat_path.unlink(missing_ok=True)

            if result.returncode == 0:
                return output_path
            else:
                print(f"FFmpeg error: {result.stderr[:200]}")
                return None

        except Exception as e:
            print(f"Slideshow error: {e}")
            return None

    # ── Video Editing (replaces video-production) ────────────────────────

    def add_captions(
        self,
        video_path: str,
        output_path: str,
        captions: list[dict],
        font_size: int = 48,
        font_color: str = "white",
        bg_color: str = "black@0.5",
    ) -> Optional[str]:
        """
        Add text captions/subtitles to video.
        Replaces: video-production caption feature.

        Args:
            video_path: Input video
            output_path: Output video
            captions: List of {text, start, end} dicts (times in seconds)
            font_size: Caption font size
            font_color: Caption color
            bg_color: Background color with opacity
        """
        if not FFMPEG:
            return None

        # Build drawtext filter
        filters = []
        for cap in captions:
            text = cap["text"].replace("'", "\\'").replace(":", "\\:")
            start = cap.get("start", 0)
            end = cap.get("end", start + 3)
            filters.append(
                f"drawtext=text='{text}'"
                f":fontsize={font_size}"
                f":fontcolor={font_color}"
                f":borderw=2:bordercolor=black"
                f":x=(w-text_w)/2:y=h-th-50"
                f":enable='between(t,{start},{end})'"
            )

        filter_str = ",".join(filters)

        try:
            cmd = [
                FFMPEG,
                "-y",
                "-i",
                video_path,
                "-vf",
                filter_str,
                "-c:a",
                "copy",
                output_path,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            return output_path if result.returncode == 0 else None
        except Exception as e:
            print(f"Caption error: {e}")
            return None

    def trim_video(
        self,
        video_path: str,
        output_path: str,
        start: float = 0,
        duration: float = None,
        end: float = None,
    ) -> Optional[str]:
        """Trim video to specific segment."""
        if not FFMPEG:
            return None

        cmd = [FFMPEG, "-y", "-i", video_path, "-ss", str(start)]
        if duration:
            cmd.extend(["-t", str(duration)])
        elif end:
            cmd.extend(["-to", str(end)])
        cmd.extend(["-c", "copy", output_path])

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            return output_path if result.returncode == 0 else None
        except:
            return None

    def concat_videos(
        self,
        video_paths: list[str],
        output_path: str,
    ) -> Optional[str]:
        """Concatenate multiple videos into one."""
        if not FFMPEG or not video_paths:
            return None

        concat_path = Path(output_path).parent / "video_concat.txt"
        with open(concat_path, "w") as f:
            for v in video_paths:
                f.write(f"file '{v}'\n")

        try:
            cmd = [
                FFMPEG,
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_path),
                "-c",
                "copy",
                output_path,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            concat_path.unlink(missing_ok=True)
            return output_path if result.returncode == 0 else None
        except:
            concat_path.unlink(missing_ok=True)
            return None

    # ── YouTube Factory (replaces youtube-factory) ───────────────────────

    def generate_youtube_content(
        self,
        topic: str,
        style: str = "educational",
        duration_minutes: int = 1,
    ) -> dict:
        """
        Generate YouTube-ready content package.
        Replaces: youtube-factory.

        Returns dict with:
            - script: Generated script text
            - video_uuid: GeminiGen video generation UUID
            - thumbnail_uuid: GeminiGen thumbnail UUID
        """
        result = {"topic": topic, "style": style}

        # Generate video via Grok
        video_prompt = (
            f"Professional {style} video about {topic}. "
            f"Clear narration style. Engaging visuals. "
            f"Dark professional aesthetic. High production value."
        )

        try:
            video_resp = self.client.generate_video_grok(
                prompt=video_prompt,
                model="grok-3",
                aspect_ratio="landscape",
                duration=15,
            )
            result["video_uuid"] = video_resp.get("uuid")
            result["video_status"] = video_resp.get("status")
        except Exception as e:
            result["video_error"] = str(e)

        # Generate thumbnail via image API
        thumb_prompt = (
            f"YouTube thumbnail for video about {topic}. "
            f"Dark background, bold white text, "
            f"professional, high contrast, clickbait-style. "
            f"16:9 landscape format."
        )

        try:
            thumb_resp = self.client.generate_image(
                prompt=thumb_prompt,
                model="nano-banana-pro",
                aspect_ratio="16:9",
                style="Photorealistic",
            )
            result["thumbnail_uuid"] = thumb_resp.get("uuid")
        except Exception as e:
            result["thumbnail_error"] = str(e)

        return result

    # ── Scene chaining (video extend) ─────────────────────────────────────────

    def _extract_last_frame(self, video_path: str, output_path: str) -> bool:
        """Extract last frame from video as PNG. Returns True on success."""
        if not FFMPEG:
            return False
        try:
            result = subprocess.run(
                [
                    FFMPEG,
                    "-y",
                    "-s",
                    "ws",
                    "-i",
                    video_path,
                    "-vf",
                    "select=eq(n\\,0)+eq(pict_type\\,I),trim=start=0:delta=0",
                    "-vframes",
                    "1",
                    output_path,
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0 and Path(output_path).exists():
                return True
            result = subprocess.run(
                [
                    FFMPEG,
                    "-y",
                    "-s",
                    "ws",
                    "-i",
                    video_path,
                    "-vf",
                    "select=eq(n\\,0),trim=start=0",
                    "-vframes",
                    "1",
                    output_path,
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )
            return result.returncode == 0 and Path(output_path).exists()
        except Exception:
            return False

    def generate_extended_video(
        self,
        scenes: list[dict],
        output_path: str,
        aspect_ratio: str = "portrait",
        duration: int = 6,
        max_retries: int = 3,
    ) -> Optional[str]:
        """
        Chain multiple video scenes into one video using GeminiGen video-extend.
        Scene 1 → Scene 2 → Scene 3 → Scene 4 → FFmpeg concat.

        Args:
            scenes: List of dicts with "prompt" key, e.g. [{"prompt": "..."}]
            output_path: Final output file path
            aspect_ratio: portrait, landscape, square
            duration: Seconds per scene (6, 10, or 15)
            max_retries: Retry attempts on rate-limit failures

        Returns:
            Output path if successful, None if failed
        """
        if not FFMPEG:
            print("FFmpeg not installed")
            return None
        if len(scenes) < 1:
            print("No scenes provided")
            return None

        tmp_dir = Path(tempfile.mkdtemp(prefix="video_chain_"))
        scene_paths = []
        prev_uuid = None

        for i, scene in enumerate(scenes):
            prompt = scene.get("prompt", "")
            if not prompt:
                continue

            print(f"[Scene {i + 1}/{len(scenes)}] Submitting: {prompt[:60]}...")
            resp = None

            for attempt in range(max_retries):
                try:
                    if prev_uuid:
                        resp = self.client.generate_video_extend(
                            ref_history_uuid=prev_uuid,
                            ref_image_prompt=prompt,
                            aspect_ratio=aspect_ratio,
                            duration=duration,
                        )
                    else:
                        resp = self.client.generate_video_grok(
                            prompt=prompt,
                            aspect_ratio=aspect_ratio,
                            duration=duration,
                        )
                    break
                except Exception as e:
                    if attempt < max_retries - 1:
                        wait = 2**attempt
                        print(
                            f"  Attempt {attempt + 1} failed: {e}. Retrying in {wait}s..."
                        )
                        time.sleep(wait)
                    else:
                        print(f"  All {max_retries} attempts failed for scene {i + 1}")
                        resp = None
                        break

            if not resp:
                continue

            uuid = resp.get("uuid") or resp.get("id", "")
            if not uuid:
                print(f"  No UUID returned for scene {i + 1}")
                continue

            try:
                completed = self.client.wait_for_completion(uuid, timeout=300)
                video_url = self.client.get_video_url(completed)
                if not video_url:
                    print(f"  No video URL for scene {i + 1}")
                    continue

                scene_path = tmp_dir / f"scene_{i:02d}.mp4"
                dl = subprocess.run(
                    ["curl", "-s", "-o", str(scene_path), "-L", video_url],
                    timeout=30,
                    capture_output=True,
                )
                if (
                    dl.returncode == 0
                    and scene_path.exists()
                    and scene_path.stat().st_size > 1000
                ):
                    scene_paths.append(str(scene_path))
                    prev_uuid = uuid
                    print(f"  Scene {i + 1} done: {scene_path.stat().st_size} bytes")
                else:
                    print(f"  Download failed for scene {i + 1}")

                if i < len(scenes) - 1:
                    time.sleep(2)

                if i < len(scenes) - 1 and prev_uuid:
                    status = self.client.get_status(prev_uuid)
                    rate_limit = (status.get("error_message") or "").lower() in [
                        "rate limit",
                        "rate limit exceeded",
                        "too many requests",
                    ]
                    if rate_limit and i >= 1:
                        print(f"  Rate limit near, stopping scene chain at {i + 1}")
                        break

            except TimeoutError:
                print(f"  Timeout for scene {i + 1}")
                continue
            except Exception as e:
                print(f"  Error completing scene {i + 1}: {e}")
                continue

        if len(scene_paths) < 1:
            print("No scenes generated")
            shutil.rmtree(tmp_dir, ignore_errors=True)
            return None

        concat_path = tmp_dir / "concat.txt"
        with open(concat_path, "w") as f:
            for sp in scene_paths:
                f.write(f"file '{sp}'\n")

        try:
            cmd = [
                FFMPEG,
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_path),
                "-c",
                "copy",
                output_path,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode == 0 and Path(output_path).exists():
                print(f"Final video: {Path(output_path).stat().st_size} bytes")
                return output_path
            else:
                print(f"FFmpeg concat failed: {result.stderr[:200]}")
                return None
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)
