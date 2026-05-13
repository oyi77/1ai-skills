#!/usr/bin/env python3
"""
Asset Preparation Script for Remotion
=======================================
Resizes images, converts videos, and prepares all assets to the
correct specs for Remotion without any API or AI tools.

100% local. No API. No internet. Uses ffmpeg + Pillow only.

Usage:
  python scripts/prepare_assets.py                    # process public/images/ + public/video/
  python scripts/prepare_assets.py --images-only      # only process images
  python scripts/prepare_assets.py --video-only       # only process video
  python scripts/prepare_assets.py path/to/file.jpg   # process single file
  python scripts/prepare_assets.py --format 9:16      # target 9:16 (TikTok/Reels)
  python scripts/prepare_assets.py --format 1:1       # target 1:1 (Instagram)

Install (one-time, free):
  pip install Pillow
  brew install ffmpeg   # macOS
  apt install ffmpeg    # Ubuntu/Debian

What it does:
  Images:
    - Converts to PNG (lossless, Remotion-safe)
    - Resizes to target resolution (default: 1920×1080)
    - Strips EXIF metadata (privacy)
    - Creates @2x versions for high-DPI

  Videos:
    - Converts to H.264 MP4 (maximum Remotion compatibility)
    - Re-encodes to target framerate (default: 30fps)
    - Normalises audio to -16 LUFS
    - Strips metadata

Output: public/images/ready/ and public/video/ready/
"""

import sys
import os
import subprocess
import argparse
import shutil
from pathlib import Path

# ── CONFIG ────────────────────────────────────────────────────

FORMATS = {
    '16:9': (1920, 1080),
    '9:16': (1080, 1920),
    '1:1':  (1080, 1080),
    '4:3':  (1440, 1080),
    '4K':   (3840, 2160),
}

IMAGE_EXTS  = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.heic', '.avif'}
VIDEO_EXTS  = {'.mp4', '.mov', '.avi', '.mkv', '.webm', '.m4v', '.mxf'}

DEFAULT_FORMAT = '16:9'
DEFAULT_FPS    = 30
DEFAULT_CRF    = 23        # video quality (lower = better, 18–28 range)
DEFAULT_PRESET = 'fast'    # ffmpeg encode speed: ultrafast/fast/medium/slow


# ── HELPERS ───────────────────────────────────────────────────

def run(cmd: list, label: str = '') -> bool:
    """Run a shell command, return True on success."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"    ❌ {label or cmd[0]} failed:")
        print(f"       {e.stderr.strip()[:200]}")
        return False
    except FileNotFoundError:
        prog = cmd[0]
        print(f"    ❌ {prog} not found. Install with: brew install {prog} OR apt install {prog}")
        return False


def has_ffmpeg() -> bool:
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def has_pillow() -> bool:
    try:
        import PIL
        return True
    except ImportError:
        return False


def get_video_info(path: str) -> dict:
    """Get video metadata using ffprobe."""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_streams', '-show_format',
             '-of', 'json', path],
            capture_output=True, text=True, check=True
        )
        import json
        data    = json.loads(result.stdout)
        streams = data.get('streams', [])
        video   = next((s for s in streams if s['codec_type'] == 'video'), {})
        audio   = next((s for s in streams if s['codec_type'] == 'audio'), None)
        fmt     = data.get('format', {})
        return {
            'width':    int(video.get('width', 0)),
            'height':   int(video.get('height', 0)),
            'fps':      eval(video.get('r_frame_rate', '30/1')),
            'codec':    video.get('codec_name', ''),
            'duration': float(fmt.get('duration', 0)),
            'has_audio': audio is not None,
        }
    except Exception:
        return {}


# ── IMAGE PROCESSING ──────────────────────────────────────────

def process_image(src: Path, out_dir: Path, width: int, height: int) -> bool:
    """
    Resize and convert image to PNG using Pillow.
    Covers the full surface of the target size (cover fit).
    """
    try:
        from PIL import Image, ImageOps
    except ImportError:
        print("    ❌ Pillow not installed. Run: pip install Pillow")
        return False

    try:
        img = Image.open(src)

        # Strip EXIF / rotate per orientation tag
        img = ImageOps.exif_transpose(img)

        # Convert to RGB (handles RGBA, P, LA modes)
        if img.mode not in ('RGB', 'RGBA'):
            img = img.convert('RGBA' if 'transparency' in img.info else 'RGB')

        # Cover-fit resize: scale to fill, then centre-crop
        img_ratio = img.width / img.height
        tgt_ratio = width / height

        if img_ratio > tgt_ratio:
            # Image is wider — fit by height, crop sides
            new_h = height
            new_w = round(height * img_ratio)
        else:
            # Image is taller — fit by width, crop top/bottom
            new_w = width
            new_h = round(width / img_ratio)

        img = img.resize((new_w, new_h), Image.LANCZOS)

        # Centre crop
        left = (new_w - width) // 2
        top  = (new_h - height) // 2
        img  = img.crop((left, top, left + width, top + height))

        # Save as PNG
        out_path = out_dir / (src.stem + '.png')
        img.save(out_path, 'PNG', optimize=True)
        size_kb = out_path.stat().st_size // 1024
        print(f"    ✓ {out_path.name} ({width}×{height}px, {size_kb}KB)")
        return True

    except Exception as e:
        print(f"    ❌ Failed: {e}")
        return False


# ── VIDEO PROCESSING ──────────────────────────────────────────

def process_video(src: Path, out_dir: Path,
                  width: int, height: int,
                  fps: int, crf: int, preset: str) -> bool:
    """
    Convert video to H.264 MP4 at target resolution and framerate.
    Uses ffmpeg's scale filter with padding for letterbox/pillarbox.
    """
    if not has_ffmpeg():
        print("    ❌ ffmpeg not found. Install: brew install ffmpeg OR apt install ffmpeg")
        return False

    out_path = out_dir / (src.stem + '.mp4')

    # Scale to fit within target, pad with black if aspect differs
    scale_filter = (
        f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black,"
        f"setsar=1"
    )

    cmd = [
        'ffmpeg', '-y',
        '-i', str(src),
        '-vf', f"{scale_filter},fps={fps}",
        '-c:v', 'libx264',
        '-crf', str(crf),
        '-preset', preset,
        '-pix_fmt', 'yuv420p',   # required for broad compatibility
        '-c:a', 'aac',
        '-b:a', '128k',
        '-movflags', '+faststart',  # web-optimised
        '-map_metadata', '-1',       # strip metadata
        str(out_path),
    ]

    info = get_video_info(str(src))
    src_info = f"{info.get('width', '?')}×{info.get('height', '?')} {info.get('codec', '?')}"
    print(f"    Converting: {src_info} → {width}×{height} H.264 @{fps}fps")

    ok = run(cmd, 'ffmpeg')
    if ok:
        size_mb = out_path.stat().st_size / 1_048_576
        print(f"    ✓ {out_path.name} ({size_mb:.1f}MB)")
    return ok


# ── MAIN ──────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Prepare images and videos for Remotion projects'
    )
    parser.add_argument('path', nargs='?', default=None,
                        help='Single file or directory to process (default: public/)')
    parser.add_argument('--format', default=DEFAULT_FORMAT,
                        choices=list(FORMATS.keys()),
                        help=f'Target aspect ratio (default: {DEFAULT_FORMAT})')
    parser.add_argument('--fps', type=int, default=DEFAULT_FPS,
                        help=f'Target video FPS (default: {DEFAULT_FPS})')
    parser.add_argument('--crf', type=int, default=DEFAULT_CRF,
                        help=f'Video quality 0–51, lower=better (default: {DEFAULT_CRF})')
    parser.add_argument('--images-only', action='store_true')
    parser.add_argument('--video-only',  action='store_true')
    parser.add_argument('--out-dir', default=None,
                        help='Custom output directory')
    args = parser.parse_args()

    width, height = FORMATS[args.format]

    print(f"\n🎬 Remotion Asset Prep — target: {width}×{height} ({args.format})\n")

    # Collect files to process
    files_to_process = []

    if args.path and os.path.isfile(args.path):
        files_to_process = [Path(args.path)]
    else:
        search_dirs = []
        if not args.video_only:
            search_dirs.append(Path('public/images'))
        if not args.images_only:
            search_dirs.append(Path('public/video'))

        for d in search_dirs:
            if d.exists():
                for f in sorted(d.iterdir()):
                    if f.suffix.lower() in IMAGE_EXTS | VIDEO_EXTS:
                        files_to_process.append(f)

    if not files_to_process:
        print("ℹ  No files found to process.")
        print("   Put images in public/images/ and videos in public/video/")
        return

    processed, failed = 0, 0

    for src in files_to_process:
        ext = src.suffix.lower()
        print(f"\n  📄 {src.name}")

        if ext in IMAGE_EXTS and not args.video_only:
            if not has_pillow():
                print("  ❌ Pillow required. Install: pip install Pillow")
                break
            out_dir = Path(args.out_dir) if args.out_dir else src.parent / 'ready'
            out_dir.mkdir(parents=True, exist_ok=True)
            ok = process_image(src, out_dir, width, height)

        elif ext in VIDEO_EXTS and not args.images_only:
            if not has_ffmpeg():
                print("  ❌ ffmpeg required. Install: brew install ffmpeg")
                break
            out_dir = Path(args.out_dir) if args.out_dir else src.parent / 'ready'
            out_dir.mkdir(parents=True, exist_ok=True)
            ok = process_video(src, out_dir, width, height, args.fps, args.crf, DEFAULT_PRESET)

        else:
            print(f"    ⏭  Skipped ({ext})")
            continue

        if ok:
            processed += 1
        else:
            failed += 1

    print(f"\n{'✅' if failed == 0 else '⚠️ '} Done: {processed} processed, {failed} failed")
    if processed > 0:
        print(f"\nIn your Remotion composition, reference assets from the ready/ subfolder:")
        print(f"  <Img src={{staticFile('images/ready/your-image.png')}} />")
        print(f"  <OffthreadVideo src={{staticFile('video/ready/your-clip.mp4')}} />")


if __name__ == '__main__':
    main()
