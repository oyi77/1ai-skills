"""
Video Enhancer — Watermark Removal + AI Quality Enhancement
===========================================================
Wraps KLing-Video-WatermarkRemover-Enhancer + FFmpeg fallback.

Pipeline:
  1. Watermark removal (FFmpeg delogo fast, or STTN ML-based)
  2. AI quality enhancement (Real-ESRGAN upscale, GFPGAN face restore)
  3. Output: clean, enhanced video

Requirements:
  - ffmpeg (always available — fast path)
  - basicsr, realesrgan, gfpgan (optional — ML path, Python 3.10/3.11)
  - Weights: RealESRGAN_x2plus.pth, GFPGANv1.4.pth, sttn.pth
"""

import os
import sys
import shutil
import logging
import subprocess
import urllib.request
from pathlib import Path
from typing import Optional
from datetime import datetime


# ---- Logging ----
log = logging.getLogger("video_enhancer")
log.setLevel(logging.DEBUG)
_log_dir = Path.home() / ".openclaw" / "workspace" / "logs"
_log_dir.mkdir(parents=True, exist_ok=True)
_fh = logging.FileHandler(_log_dir / "video_enhancer.log")
_fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
log.addHandler(_fh)
_sh = logging.StreamHandler()
_sh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
log.addHandler(_sh)


# ---- Defaults ----
REPO_DIR = Path(__file__).parent.parent.parent / "KLing-Video-WatermarkRemover-Enhancer"
WEIGHTS_DIR = REPO_DIR / "weights"

# Kling watermark position (x1, y1, x2, y2)
DEFAULT_WATERMARK_POSITION = [556, 1233, 701, 1267]

# Public model weights URLs
WEIGHT_URLS = {
    "RealESRGAN_x2plus.pth": "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth",
    "GFPGANv1.4.pth": "https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/GFPGANv1.4.pth",
    # sttn.pth requires Google Drive — manual download
    # https://drive.google.com/file/d/1ZAMV8547wmZylKRt5qR_tC5VlosXD4Wv/view
}


class VideoEnhancer:
    """
    Video watermark removal and quality enhancement.
    
    Two modes:
    - **Fast** (FFmpeg): delogo filter, instant, good quality
    - **ML** (STTN+ESRGAN): best quality, requires Python 3.10+ and GPU
    
    Usage:
        enhancer = VideoEnhancer()
        output = enhancer.process("input.mp4", remove_wm=True, enhance=True)
    """

    def __init__(
        self,
        repo_path: Optional[str] = None,
        weights_dir: Optional[str] = None,
        watermark_position: Optional[list] = None,
        output_dir: Optional[str] = None,
    ):
        self.repo_path = Path(repo_path) if repo_path else REPO_DIR
        self.weights_dir = Path(weights_dir) if weights_dir else WEIGHTS_DIR
        self.watermark_pos = watermark_position or DEFAULT_WATERMARK_POSITION
        self.output_dir = Path(output_dir) if output_dir else (
            Path.home() / ".openclaw" / "workspace" / "downloads" / "enhanced_videos"
        )
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.weights_dir.mkdir(parents=True, exist_ok=True)

        # Check capabilities
        self._ffmpeg_available = bool(shutil.which("ffmpeg"))
        self._ml_available = self._check_ml_available()

        log.info(f"VideoEnhancer initialized")
        log.info(f"  FFmpeg: {'✅' if self._ffmpeg_available else '❌'}")
        log.info(f"  ML (STTN+ESRGAN): {'✅' if self._ml_available else '❌ (requires Python 3.10 + basicsr)'}")
        log.info(f"  Weights dir: {self.weights_dir}")

    def _check_ml_available(self) -> bool:
        """Check if ML-based processing is available."""
        try:
            import basicsr
            import realesrgan
            import gfpgan
            return True
        except ImportError:
            return False

    def is_ready(self) -> bool:
        """Check if enough components are available to process videos."""
        return self._ffmpeg_available  # FFmpeg fallback always works

    def weights_status(self) -> dict:
        """Report which weights are present."""
        status = {}
        for name, url in WEIGHT_URLS.items():
            path = self.weights_dir / name
            status[name] = {
                "present": path.exists(),
                "size_mb": round(path.stat().st_size / 1024 / 1024, 1) if path.exists() else 0,
                "url": url,
            }
        # sttn.pth (ML-only, optional)
        sttn_path = self.weights_dir / "sttn.pth"
        status["sttn.pth"] = {
            "present": sttn_path.exists(),
            "size_mb": round(sttn_path.stat().st_size / 1024 / 1024, 1) if sttn_path.exists() else 0,
            "url": "https://drive.google.com/file/d/1ZAMV8547wmZylKRt5qR_tC5VlosXD4Wv/ (manual download)",
        }
        return status

    def download_weights(self, verbose: bool = True) -> bool:
        """
        Download publicly available model weights.
        Note: sttn.pth requires manual download from Google Drive.
        """
        success = True
        for name, url in WEIGHT_URLS.items():
            path = self.weights_dir / name
            if path.exists():
                log.info(f"  ✅ {name} already present ({path.stat().st_size / 1024 / 1024:.1f} MB)")
                continue
            try:
                log.info(f"  📥 Downloading {name}...")
                urllib.request.urlretrieve(url, str(path))
                log.info(f"  ✅ {name} downloaded ({path.stat().st_size / 1024 / 1024:.1f} MB)")
            except Exception as e:
                log.error(f"  ❌ Failed to download {name}: {e}")
                success = False

        sttn_path = self.weights_dir / "sttn.pth"
        if not sttn_path.exists():
            log.warning(
                "  ⚠️  sttn.pth missing (required for ML watermark removal). "
                "Manual download from: https://drive.google.com/file/d/1ZAMV8547wmZylKRt5qR_tC5VlosXD4Wv/"
            )

        return success

    # ================================================================
    # WATERMARK REMOVAL
    # ================================================================
    def remove_watermark(
        self,
        video_path: str,
        output_path: Optional[str] = None,
        method: str = "auto",  # "auto" | "ffmpeg" | "ml"
    ) -> Optional[str]:
        """
        Remove Kling watermark from video.
        
        Args:
            video_path: Input video path
            output_path: Output path (auto-generated if None)
            method: "auto" tries ML first, falls back to FFmpeg
        
        Returns:
            Output video path or None on failure
        """
        if not os.path.isfile(video_path):
            log.error(f"Input video not found: {video_path}")
            return None

        if output_path is None:
            stem = Path(video_path).stem
            timestamp = datetime.now().strftime("%H%M%S")
            output_path = str(self.output_dir / f"{stem}_nowm_{timestamp}.mp4")

        log.info(f"🔧 Removing watermark: {Path(video_path).name}")

        if method == "auto":
            # Try ML if available and weights present
            if self._ml_available and (self.weights_dir / "sttn.pth").exists():
                result = self._remove_watermark_ml(video_path, output_path)
                if result:
                    return result
                log.warning("ML watermark removal failed, falling back to FFmpeg")
            result = self._remove_watermark_ffmpeg(video_path, output_path)
        elif method == "ml":
            result = self._remove_watermark_ml(video_path, output_path)
        else:  # ffmpeg
            result = self._remove_watermark_ffmpeg(video_path, output_path)

        return result

    def _remove_watermark_ffmpeg(self, video_path: str, output_path: str) -> Optional[str]:
        """
        Fast watermark removal using FFmpeg delogo filter.
        Quality: good (blur/inpaint the watermark area).
        """
        if not self._ffmpeg_available:
            log.error("FFmpeg not available")
            return None

        x1, y1, x2, y2 = self.watermark_pos
        w = x2 - x1
        h = y2 - y1

        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vf", f"delogo=x={x1}:y={y1}:w={w}:h={h}:show=0",
            "-c:a", "copy",
            "-preset", "fast",
            output_path
        ]

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=120
            )
            if result.returncode == 0 and os.path.isfile(output_path):
                size_mb = os.path.getsize(output_path) / 1024 / 1024
                log.info(f"  ✅ FFmpeg watermark removed: {Path(output_path).name} ({size_mb:.1f} MB)")
                return output_path
            else:
                log.error(f"  ❌ FFmpeg delogo failed: {result.stderr[-300:]}")
        except subprocess.TimeoutExpired:
            log.error("  ❌ FFmpeg timed out")
        except Exception as e:
            log.error(f"  ❌ FFmpeg error: {e}")

        return None

    def _remove_watermark_ml(self, video_path: str, output_path: str) -> Optional[str]:
        """
        ML-based watermark removal using STTN inpainting.
        Better quality but requires Python 3.10 + basicsr.
        """
        if not self._ml_available:
            log.warning("ML not available (requires basicsr/realesrgan/gfpgan)")
            return None

        try:
            sys.path.insert(0, str(self.repo_path))
            sys.path.insert(0, str(self.repo_path / "STTN"))
            from modules.erase import remove_watermark
            from utils.video_utils import extract_frames, create_video, detect_fps

            fps = detect_fps(video_path)
            extract_frames(video_path, fps)

            from utils.video_utils import get_temp_directory_path, get_temp_frame_paths
            temp_dir = get_temp_directory_path(video_path)
            frame_paths = get_temp_frame_paths(temp_dir)

            remove_watermark(frame_paths)
            create_video(video_path, output_path, fps)

            if os.path.isfile(output_path):
                log.info(f"  ✅ ML watermark removed: {output_path}")
                return output_path
        except Exception as e:
            log.error(f"  ❌ ML watermark removal failed: {e}")

        return None

    # ================================================================
    # VIDEO ENHANCEMENT
    # ================================================================
    def enhance(
        self,
        video_path: str,
        output_path: Optional[str] = None,
        upscale: int = 2,
        method: str = "auto",  # "auto" | "ffmpeg" | "ml"
    ) -> Optional[str]:
        """
        AI-enhance video quality.
        
        Args:
            video_path: Input video path
            output_path: Output path (auto-generated if None)
            upscale: Upscale factor (1, 2, 4)
            method: "auto" tries ML, falls back to FFmpeg
        
        Returns:
            Output path or None
        """
        if not os.path.isfile(video_path):
            log.error(f"Input not found: {video_path}")
            return None

        if output_path is None:
            stem = Path(video_path).stem
            timestamp = datetime.now().strftime("%H%M%S")
            output_path = str(self.output_dir / f"{stem}_enhanced_{timestamp}.mp4")

        log.info(f"✨ Enhancing video: {Path(video_path).name} (x{upscale})")

        if method == "auto":
            if self._ml_available and (self.weights_dir / "RealESRGAN_x2plus.pth").exists():
                result = self._enhance_ml(video_path, output_path, upscale)
                if result:
                    return result
                log.warning("ML enhancement failed, falling back to FFmpeg")
            return self._enhance_ffmpeg(video_path, output_path, upscale)
        elif method == "ml":
            return self._enhance_ml(video_path, output_path, upscale)
        else:
            return self._enhance_ffmpeg(video_path, output_path, upscale)

    def _enhance_ffmpeg(self, video_path: str, output_path: str, upscale: int = 2) -> Optional[str]:
        """
        FFmpeg-based enhancement: sharpening + contrast boost.
        Not AI, but fast and always available.
        """
        if not self._ffmpeg_available:
            return None

        # FFmpeg enhancement filters: unsharp, vibrance boost
        filters = "unsharp=5:5:0.8:3:3:0.4,eq=contrast=1.05:brightness=0.01:saturation=1.1"
        if upscale > 1:
            filters = f"scale=iw*{upscale}:ih*{upscale}:flags=lanczos,{filters}"

        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vf", filters,
            "-c:v", "libx264",
            "-crf", "18",
            "-preset", "medium",
            "-c:a", "copy",
            output_path
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            if result.returncode == 0 and os.path.isfile(output_path):
                size_mb = os.path.getsize(output_path) / 1024 / 1024
                log.info(f"  ✅ FFmpeg enhanced: {Path(output_path).name} ({size_mb:.1f} MB)")
                return output_path
        except Exception as e:
            log.error(f"  ❌ FFmpeg enhance error: {e}")

        return None

    def _enhance_ml(self, video_path: str, output_path: str, upscale: int = 2) -> Optional[str]:
        """Real-ESRGAN + GFPGAN enhancement (ML, requires GPU/CPU + weights)."""
        if not self._ml_available:
            return None

        try:
            sys.path.insert(0, str(self.repo_path))
            from modules.enhance import enhance_frames
            from utils.video_utils import extract_frames, create_video, detect_fps, get_temp_directory_path, get_temp_frame_paths

            fps = detect_fps(video_path)
            extract_frames(video_path, fps)
            temp_dir = get_temp_directory_path(video_path)
            frame_paths = get_temp_frame_paths(temp_dir)

            enhance_frames(frame_paths)
            create_video(video_path, output_path, fps)

            if os.path.isfile(output_path):
                log.info(f"  ✅ ML enhanced: {output_path}")
                return output_path
        except Exception as e:
            log.error(f"  ❌ ML enhancement failed: {e}")

        return None

    # ================================================================
    # FULL PIPELINE
    # ================================================================
    def process(
        self,
        video_path: str,
        output_path: Optional[str] = None,
        remove_wm: bool = True,
        enhance: bool = True,
        method: str = "auto",
    ) -> Optional[str]:
        """
        Full pipeline: remove watermark → enhance quality.
        
        Args:
            video_path: Input video path
            output_path: Final output path
            remove_wm: Remove Kling watermark
            enhance: Enhance video quality
            method: "auto" | "ffmpeg" | "ml"
        
        Returns:
            Final processed video path or None
        """
        if not os.path.isfile(video_path):
            log.error(f"Input not found: {video_path}")
            return None

        import time
        start = time.time()
        log.info(f"\n{'='*50}")
        log.info(f"🎬 Processing: {Path(video_path).name}")
        log.info(f"  remove_wm={remove_wm}, enhance={enhance}, method={method}")

        current = video_path
        temp_files = []

        try:
            if remove_wm:
                stem = Path(video_path).stem
                wm_path = str(self.output_dir / f"{stem}_nowm_tmp.mp4")
                result = self.remove_watermark(current, wm_path, method=method)
                if result:
                    temp_files.append(wm_path)
                    current = result
                else:
                    log.warning("  ⚠️  Watermark removal failed, using original")

            if enhance:
                stem = Path(current).stem
                enhanced_path = output_path or str(self.output_dir / f"{stem}_final.mp4")
                result = self.enhance(current, enhanced_path, method=method)
                if result:
                    current = result
                else:
                    log.warning("  ⚠️  Enhancement failed, using watermark-removed version")
            elif output_path and current != output_path:
                # Just copy to final output path
                shutil.copy2(current, output_path)
                current = output_path

            # Clean up temp files
            for tmp in temp_files:
                if tmp != current and os.path.isfile(tmp):
                    os.remove(tmp)

            elapsed = time.time() - start
            size_mb = os.path.getsize(current) / 1024 / 1024 if os.path.isfile(current) else 0
            log.info(f"✅ Done in {elapsed:.1f}s — {current} ({size_mb:.1f} MB)")
            return current

        except Exception as e:
            log.error(f"❌ Processing pipeline failed: {e}")
            # Clean up temps
            for tmp in temp_files:
                if os.path.isfile(tmp):
                    os.remove(tmp)
            return None

    # ================================================================
    # SETUP
    # ================================================================
    def setup(self) -> bool:
        """
        Download weights and install dependencies.
        Returns True if ready for at least FFmpeg processing.
        """
        log.info("🔧 Setting up VideoEnhancer...")

        # Download public weights
        self.download_weights()

        # Try to install ML dependencies
        if not self._ml_available:
            log.info("📦 Attempting ML dependency install...")
            install_cmd = [
                sys.executable, "-m", "pip", "install",
                "basicsr", "gfpgan", "realesrgan",
                "--break-system-packages", "-q"
            ]
            result = subprocess.run(install_cmd, capture_output=True, text=True, timeout=120)
            self._ml_available = self._check_ml_available()
            if self._ml_available:
                log.info("  ✅ ML dependencies installed")
            else:
                log.warning(
                    "  ⚠️  ML dependencies failed (likely Python 3.12+ incompatibility). "
                    "FFmpeg fallback will be used. For full ML support, use Python 3.10/3.11."
                )

        log.info(f"Setup complete. FFmpeg: {'✅' if self._ffmpeg_available else '❌'}, ML: {'✅' if self._ml_available else '❌ (fallback: FFmpeg)'}")
        return self._ffmpeg_available


# ================================================================
# CLI
# ================================================================
def main():
    import argparse

    parser = argparse.ArgumentParser(description="Kling Video Enhancer")
    parser.add_argument("input", help="Input video path")
    parser.add_argument("-o", "--output", help="Output video path")
    parser.add_argument("--no-watermark", action="store_true", default=True, help="Remove watermark (default: on)")
    parser.add_argument("--no-enhance", action="store_true", help="Skip video enhancement")
    parser.add_argument("--method", choices=["auto", "ffmpeg", "ml"], default="auto")
    parser.add_argument("--setup", action="store_true", help="Download weights and setup")
    parser.add_argument("--status", action="store_true", help="Show weights status")
    args = parser.parse_args()

    enhancer = VideoEnhancer()

    if args.setup:
        enhancer.setup()
        return

    if args.status:
        print("\n📋 Weights Status:")
        for name, info in enhancer.weights_status().items():
            status = "✅" if info["present"] else "❌"
            size = f" ({info['size_mb']} MB)" if info["present"] else ""
            print(f"  {status} {name}{size}")
        print(f"\nFFmpeg: {'✅' if enhancer._ffmpeg_available else '❌'}")
        print(f"ML (ESRGAN/GFPGAN): {'✅' if enhancer._ml_available else '❌'}")
        return

    output = enhancer.process(
        args.input,
        output_path=args.output,
        remove_wm=args.no_watermark,
        enhance=not args.no_enhance,
        method=args.method,
    )

    if output:
        print(f"✅ Output: {output}")
    else:
        print("❌ Processing failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
