"""
GeminiGen API client — images, videos, video-extend via unified API.

API base: https://api.geminigen.ai
Auth: x-api-key header
Config: workspace/config/geminigen_api.json → {"api_key": "..."}

Status codes (from /uapi/v1/history/:uuid):
  0 = pending
  1 = processing
  2 = done / completed
  3 = failed
"""

from __future__ import annotations

import json
import subprocess
import tempfile
import time
import urllib.request
import urllib.error
import shutil
from pathlib import Path
from typing import Optional


class GeminiGenClient:
    """Thin client for GeminiGen unified media API (images, videos, TTS)."""

    BASE = "https://api.geminigen.ai"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or self._load_key()

    # ── Key loading ───────────────────────────────────────────────────────────

    def _load_key(self) -> str:
        """
        Load API key from workspace config.
        Path: workspace/config/geminigen_api.json
        Falls back to empty string (caller must handle missing key).
        """
        cfg_path = (
            Path(__file__).parent.parent.parent.parent.parent
            / "config/geminigen_api.json"
        )
        if cfg_path.exists():
            try:
                with open(cfg_path) as f:
                    return json.load(f).get("api_key", "")
            except (json.JSONDecodeError, OSError):
                pass
        return ""

    # ── Image generation ──────────────────────────────────────────────────────

    def generate_image(
        self,
        prompt: str,
        model: str = "nano-banana-pro",
        aspect_ratio: str = "4:5",
        style: str = "Photorealistic",
        output_format: str = "jpeg",
        resolution: str = "1K",
        file_urls: list[str] | None = None,
    ) -> dict:
        """
        Submit image generation request.

        Returns dict with ``uuid`` and ``status`` keys on success.
        Use ``wait_for_completion(uuid)`` to poll until done.

        Args:
            prompt: Image description prompt
            model: GeminiGen model (e.g. "nano-banana-pro")
            aspect_ratio: e.g. "4:5", "1:1", "9:16", "3:4"
            style: e.g. "Photorealistic", "Digital Art", "Anime"
            output_format: "png" or "jpg"
            resolution: "1K", "2K", or "4K"
            file_urls: Optional reference image URLs for image-to-image
        """
        cmd = [
            "curl",
            "-s",
            "-X",
            "POST",
            f"{self.BASE}/uapi/v1/generate_image",
            "-H",
            f"x-api-key: {self.api_key}",
            "--form",
            f"prompt={prompt}",
            "--form",
            f"model={model}",
            "--form",
            f"aspect_ratio={aspect_ratio}",
            "--form",
            f"style={style}",
            "--form",
            f"output_format={output_format}",
            "--form",
            f"resolution={resolution}",
        ]
        if file_urls:
            for url in file_urls:
                cmd.extend(["--form", f"file_urls={url}"])

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0 or not result.stdout.strip():
            return {"error": result.stderr or "empty response", "status": 3}
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {"error": f"invalid JSON: {result.stdout[:200]}", "status": 3}

    # ── Video generation ──────────────────────────────────────────────────────

    def generate_video_grok(
        self,
        prompt: str,
        model: str = "grok-3",
        aspect_ratio: str = "portrait",
        duration: int = 6,
        file_urls: list[str] | None = None,
    ) -> dict:
        """
        Submit video generation request via Grok model.
        CRITICAL: Do NOT include resolution or mode — causes "Failed to create Grok video".

        Returns dict with ``uuid`` and ``status`` keys on success.
        """
        cmd = [
            "curl",
            "-s",
            "-X",
            "POST",
            f"{self.BASE}/uapi/v1/video-gen/grok",
            "-H",
            f"x-api-key: {self.api_key}",
            "--form",
            f"prompt={prompt}",
            "--form",
            f"model={model}",
            "--form",
            f"aspect_ratio={aspect_ratio}",
            "--form",
            f"duration={str(duration)}",
        ]
        if file_urls:
            for url in file_urls:
                cmd.extend(["--form", f"file_urls={url}"])

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0 or not result.stdout.strip():
            return {"error": result.stderr or "empty response", "status": 3}
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {"error": f"invalid JSON: {result.stdout[:200]}", "status": 3}

    # ── Status & polling ──────────────────────────────────────────────────────

    def get_status(self, uuid: str) -> dict:
        req = urllib.request.Request(
            f"{self.BASE}/uapi/v1/history/{uuid}",
            headers={"x-api-key": self.api_key},
        )
        try:
            resp = urllib.request.urlopen(req, timeout=15)
            return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}", "status": 3}
        except Exception as e:
            return {"error": str(e), "status": 3}

    def wait_for_completion(
        self,
        uuid: str,
        timeout: int = 120,
        poll_interval: int = 5,
    ) -> dict:
        """
        Poll until generation completes or fails.

        Args:
            uuid: Job UUID from generate_image() / generate_video_grok()
            timeout: Max seconds to wait before raising TimeoutError
            poll_interval: Seconds between status checks

        Returns:
            Completed result dict (status == 2)

        Raises:
            RuntimeError: If generation fails (status == 3)
            TimeoutError: If timeout exceeded
        """
        start = time.time()
        while time.time() - start < timeout:
            result = self.get_status(uuid)
            status = result.get("status", 0)
            if status == 2:  # completed
                return result
            if status == 3:  # failed
                raise RuntimeError(
                    f"Generation failed: {result.get('error_message', '?')}"
                )
            time.sleep(poll_interval)
        raise TimeoutError(f"Generation {uuid} timed out after {timeout}s")

    # ── URL extraction ────────────────────────────────────────────────────────

    def get_image_url(self, result: dict) -> str:
        """Extract the primary image CDN URL from a completed result."""
        images = result.get("generated_image", [])
        if images:
            uri = images[0].get("image_uri", "")
            if uri:
                return f"https://cdn.geminigen.ai/{uri}"
        # Fallback: thumbnail_url sometimes present on completed results
        return result.get("thumbnail_url", "")

    def get_video_url(self, result: dict) -> str:
        """Extract the primary video URL from a completed result."""
        videos = result.get("generated_video", [])
        if videos:
            return videos[0].get("video_url", videos[0].get("video_uri", ""))
        return ""

    # ── Convenience: submit → wait → url ─────────────────────────────────────

    def generate_image_sync(self, **kwargs) -> str:
        """
        Submit image generation and wait for completion. Returns image URL.

        Keyword args are passed directly to generate_image().
        Returns empty string on any failure.
        """
        try:
            resp = self.generate_image(**kwargs)
            uuid = resp.get("uuid") or resp.get("id", "")
            if not uuid:
                return ""
            completed = self.wait_for_completion(uuid)
            return self.get_image_url(completed)
        except Exception:
            return ""

    def generate_video_sync(self, **kwargs) -> str:
        try:
            resp = self.generate_video_grok(**kwargs)
            uuid = resp.get("uuid") or resp.get("id", "")
            if not uuid:
                return ""
            completed = self.wait_for_completion(uuid, timeout=300)
            return self.get_video_url(completed)
        except Exception:
            return ""

    # ── Video extend (scene chaining) ───────────────────────────────────────────

    def _download_file(self, url: str, dest: str) -> bool:
        """Download a file to dest path. Returns True on success."""
        try:
            result = subprocess.run(
                ["curl", "-s", "-o", dest, "-L", url],
                timeout=30,
                capture_output=True,
            )
            return result.returncode == 0
        except Exception:
            return False

    def _extract_last_frame(self, video_path: str, output_path: str) -> bool:
        """Extract the last frame from a video as PNG. Returns True on success."""
        if not shutil.which("ffmpeg"):
            return False
        result = subprocess.run(
            [
                "ffmpeg",
                "-s",
                "ws",
                "-y",
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
                "ffmpeg",
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

    def generate_video_extend(
        self,
        ref_history_uuid: str,
        ref_image_prompt: str,
        model: str = "grok-3",
        aspect_ratio: str = "portrait",
        duration: int = 6,
    ) -> dict:
        """
        Extend a video by extracting the last frame and passing it as ref_image.
        The API requires ref_image as a multipart file upload (not a URL).

        Flow:
          1. Poll ref_history_uuid to get the ref video URL
          2. Download ref video
          3. Extract last frame as PNG via ffmpeg
          4. Submit /video-extend/grok with multipart ref_image
        """
        ref_video_path = Path(tempfile.mktemp(suffix=".mp4"))
        ref_frame_path = Path(tempfile.mktemp(suffix=".png"))

        try:
            ref_status = self.get_status(ref_history_uuid)
            ref_video_url = self.get_video_url(ref_status)
            if not ref_video_url:
                return {
                    "error": f"No video URL for ref_history {ref_history_uuid}",
                    "status": 3,
                }

            if not self._download_file(ref_video_url, str(ref_video_path)):
                return {"error": "Failed to download ref video", "status": 3}

            if not self._extract_last_frame(str(ref_video_path), str(ref_frame_path)):
                return {"error": "Failed to extract last frame", "status": 3}

            cmd = [
                "curl",
                "-s",
                "-X",
                "POST",
                f"{self.BASE}/uapi/v1/video-extend/grok",
                "-H",
                f"x-api-key: {self.api_key}",
                "--form",
                f"prompt={ref_image_prompt}",
                "--form",
                f"model={model}",
                "--form",
                f"aspect_ratio={aspect_ratio}",
                "--form",
                f"duration={str(duration)}",
                "--form",
                f"ref_history={ref_history_uuid}",
                "--form",
                f"ref_image=@{ref_frame_path}",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode != 0 or not result.stdout.strip():
                return {"error": result.stderr or "empty response", "status": 3}
            return json.loads(result.stdout)

        finally:
            ref_video_path.unlink(missing_ok=True)
            ref_frame_path.unlink(missing_ok=True)

    def generate_video_extend_sync(
        self,
        ref_history_uuid: str,
        ref_image_prompt: str,
        model: str = "grok-3",
        aspect_ratio: str = "portrait",
        duration: int = 6,
    ) -> str:
        """Blocking version: extend video → wait → return URL."""
        try:
            resp = self.generate_video_extend(
                ref_history_uuid=ref_history_uuid,
                ref_image_prompt=ref_image_prompt,
                model=model,
                aspect_ratio=aspect_ratio,
                duration=duration,
            )
            uuid = resp.get("uuid") or resp.get("id", "")
            if not uuid:
                return ""
            completed = self.wait_for_completion(uuid, timeout=300)
            return self.get_video_url(completed)
        except Exception:
            return ""
