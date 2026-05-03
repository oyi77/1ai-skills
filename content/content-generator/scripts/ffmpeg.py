"""Basic FFmpeg operations for video processing."""

import os
import subprocess
from typing import Optional


def _run_ffmpeg(
    args: list, capture_output: bool = False
) -> subprocess.CompletedProcess:
    cmd = ["ffmpeg", "-y", *args]
    result = subprocess.run(cmd, capture_output=capture_output, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"FFmpeg failed: {result.stderr if result.stderr else 'Unknown error'}"
        )
    return result


def slideshow_from_images(
    image_paths: list[str],
    output_path: str,
    duration_per_image: float = 3.0,
    fps: int = 30,
    transition: str = "fade",
    transition_duration: float = 0.5,
    resolution: Optional[tuple[int, int]] = None,
    audio_path: Optional[str] = None,
) -> str:
    """Create slideshow from images."""
    if not image_paths:
        raise ValueError("At least one image path required")

    for img in image_paths:
        if not os.path.exists(img):
            raise ValueError(f"Image not found: {img}")

    concat_file = output_path + ".txt"

    with open(concat_file, "w") as f:
        for img in image_paths:
            f.write(f"file '{os.path.abspath(img)}'\n")
            f.write(f"duration {duration_per_image}\n")
        f.write(f"file '{os.path.abspath(image_paths[-1])}'\n")

    args = [
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        concat_file,
    ]

    if resolution:
        args.extend(["-vf", f"scale={resolution[0]}:{resolution[1]}"])

    args.extend(["-r", str(fps)])

    if audio_path and os.path.exists(audio_path):
        args.extend(["-i", audio_path])
        total_duration = len(image_paths) * duration_per_image
        args.extend(
            [
                "-filter_complex",
                f"aloop=loop=-1:size=2e+09,atrim={total_duration}",
                "-shortest",
            ]
        )

    args.append(output_path)

    try:
        _run_ffmpeg(args)
    finally:
        if os.path.exists(concat_file):
            os.remove(concat_file)

    return output_path


def merge_videos(
    video_paths: list[str],
    output_path: str,
    method: str = "concat",
) -> str:
    """Merge videos into one."""
    if not video_paths:
        raise ValueError("At least one video path required")

    for vid in video_paths:
        if not os.path.exists(vid):
            raise ValueError(f"Video not found: {vid}")

    if method == "concat":
        concat_file = output_path + ".txt"

        with open(concat_file, "w") as f:
            for vid in video_paths:
                f.write(f"file '{os.path.abspath(vid)}'\n")

        args = [
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            concat_file,
            "-c",
            "copy",
            output_path,
        ]

        try:
            _run_ffmpeg(args)
        finally:
            if os.path.exists(concat_file):
                os.remove(concat_file)
    else:
        raise ValueError(f"Unknown merge method: {method}. Use 'concat'")

    return output_path


def apply_zoom_effect(
    input_path: str,
    output_path: str,
    zoom_level: float = 1.5,
    duration: Optional[float] = None,
    x: int = 0,
    y: int = 0,
) -> str:
    """Apply zoom/pan effect to video."""
    if not os.path.exists(input_path):
        raise ValueError(f"Input video not found: {input_path}")

    if duration is None:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                input_path,
            ],
            capture_output=True,
            text=True,
        )
        duration = float(result.stdout.strip())

    filter_complex = (
        f"zoompan=z='min(zoom+0.001,{zoom_level})':"
        f"x='iw/2-(iw/zoom/2)+({x}/100*iw)':"
        f"y='ih/2-(ih/zoom/2)+({y}/100*ih)':"
        f"d={int(duration * 30)}:"
        f"s=iw*min({zoom_level},1):ih*min({zoom_level},1):"
        "fps=30"
    )

    args = [
        "-i",
        input_path,
        "-vf",
        filter_complex,
        "-c:v",
        "libx264",
        "-preset",
        "fast",
        "-crf",
        "23",
        output_path,
    ]

    _run_ffmpeg(args)
    return output_path


def trim_video(
    input_path: str,
    output_path: str,
    start: float = 0,
    duration: Optional[float] = None,
) -> str:
    """Trim video to time range."""
    if not os.path.exists(input_path):
        raise ValueError(f"Input video not found: {input_path}")

    args = [
        "-ss",
        str(start),
        "-i",
        input_path,
    ]

    if duration is not None:
        args.extend(["-t", str(duration)])

    args.extend(["-c", "copy", output_path])

    _run_ffmpeg(args)
    return output_path


def convert_format(
    input_path: str,
    output_path: str,
    codec: Optional[str] = None,
    bitrate: Optional[str] = None,
    resolution: Optional[tuple[int, int]] = None,
    fps: Optional[int] = None,
) -> str:
    """Convert video format/codec."""
    if not os.path.exists(input_path):
        raise ValueError(f"Input video not found: {input_path}")

    args = ["-i", input_path]

    filters = []

    if resolution:
        filters.append(f"scale={resolution[0]}:{resolution[1]}")

    if filters:
        args.extend(["-vf", ",".join(filters)])

    if codec:
        args.extend(["-c:v", codec])

    if bitrate:
        args.extend(["-b:v", bitrate])

    if fps:
        args.extend(["-r", str(fps)])

    args.append(output_path)

    _run_ffmpeg(args)
    return output_path


def extract_frames(
    input_path: str,
    output_dir: str,
    fps: Optional[int] = None,
    start: float = 0,
    duration: Optional[float] = None,
    pattern: str = "frame_%04d.png",
) -> list[str]:
    """Extract frames from video as images."""
    if not os.path.exists(input_path):
        raise ValueError(f"Input video not found: {input_path}")

    os.makedirs(output_dir, exist_ok=True)

    args = [
        "-i",
        input_path,
    ]

    if start > 0:
        args.extend(["-ss", str(start)])

    if duration is not None:
        args.extend(["-t", str(duration)])

    output_pattern = os.path.join(output_dir, pattern)
    args.append(output_pattern)

    if fps:
        args.extend(["-vf", f"fps={fps}"])
    else:
        args.extend(["-vf", "fps=1"])

    _run_ffmpeg(args)

    frame_paths = sorted(
        [
            os.path.join(output_dir, f)
            for f in os.listdir(output_dir)
            if f.startswith("frame_") and f != pattern.replace("%04d", "")
        ]
    )

    return frame_paths
