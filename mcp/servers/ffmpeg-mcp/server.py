#!/usr/bin/env python3
"""ffmpeg-mcp — expose FFmpeg/FFprobe as MCP tools for coding agents.

First runnable MCP server in 1ai-skills. Wraps 12 core FFmpeg operations
behind a machine-readable tool contract so an agent can inspect, cut, join,
transcode, extract audio, and thumbnail media without shelling out ad hoc.

Requires `ffmpeg` and `ffprobe` on PATH. No API keys, no cloud.

Run:  python3 server.py
"""
from __future__ import annotations

import json
import os
import shlex
import subprocess
import tempfile
from pathlib import Path
from typing import Annotated

from mcp.server.fastmcp import FastMCP

CMD_TIMEOUT = int(os.environ.get("FFMPEG_MCP_TIMEOUT", "300"))
DEFAULT_DIR = os.environ.get("FFMPEG_MCP_WORKDIR", os.getcwd())

mcp = FastMCP("ffmpeg-mcp")


class FFmpegError(RuntimeError):
    pass


def _resolve(path: str) -> Path:
    """Resolve a user-supplied path, allowing a bare filename in the workdir."""
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = Path(DEFAULT_DIR) / p
    return p


def _check_input(path: str) -> Path:
    """Require the input file to exist before building any command."""
    resolved = _resolve(path)
    if not resolved.exists():
        raise FFmpegError(f"input not found: {resolved}")
    return resolved


def _run(cmd: list[str], *, capture: bool = True) -> str:
    """Run a subprocess in the foreground with a hard timeout.

    Never background, never shell — argv is passed directly. On timeout or
    non-zero exit, raise FFmpegError carrying stderr for the agent.
    """
    try:
        proc = subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            timeout=CMD_TIMEOUT,
            cwd=DEFAULT_DIR,
        )
    except subprocess.TimeoutExpired as exc:
        raise FFmpegError(f"timed out after {CMD_TIMEOUT}s: {shlex.join(cmd)}") from exc
    except FileNotFoundError as exc:
        raise FFmpegError(f"binary not found on PATH: {cmd[0]}") from exc
    if proc.returncode != 0:
        raise FFmpegError(
            f"exit {proc.returncode} from {shlex.join(cmd[:3])}...\n"
            f"stderr: {(proc.stderr or '')[-2000:]}"
        )
    return proc.stdout or ""


def _output_path(src: Path, suffix: str, override: str | None) -> Path:
    if override:
        out = _resolve(override)
    else:
        out = src.with_name(f"{src.stem}{suffix}")
    out.parent.mkdir(parents=True, exist_ok=True)
    return out


@mcp.tool()
def probe(path: str) -> str:
    """Return media metadata (codec, width, height, fps, duration, streams) as JSON via ffprobe."""
    src = _check_input(path)
    out = _run([
        "ffprobe", "-v", "error", "-print_format", "json",
        "-show_format", "-show_streams", str(src),
    ])
    return json.dumps(json.loads(out), indent=2)


@mcp.tool()
def transcode(
    path: str,
    output: str | None = None,
    video_codec: str = "libx264",
    crf: int = 20,
    preset: str = "medium",
    width: int | None = None,
    height: int | None = None,
    audio_codec: str = "aac",
    audio_bitrate: str = "192k",
) -> str:
    """Transcode a media file with chosen codecs and optional scaling.

    crf: 0-51 quality (lower = better, 18-23 typical). preset: ultrafast..veryslow.
    """
    src = _check_input(path)
    out = _output_path(src, f"_transcoded{src.suffix or '.mp4'}", output)
    vf = None
    if width or height:
        vf = f"scale={width or -2}:{height or -2}"
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
        "-c:v", video_codec, "-crf", str(crf), "-preset", preset,
        "-c:a", audio_codec, "-b:a", audio_bitrate,
    ]
    if vf:
        cmd += ["-vf", vf]
    cmd.append(str(out))
    _run(cmd)
    return f"wrote {out}"


@mcp.tool()
def cut(
    path: str,
    start: str,
    duration: str | None = None,
    end: str | None = None,
    output: str | None = None,
    reencode: bool = False,
) -> str:
    """Cut a segment [start, end|start+duration] from a media file.

    start/duration/end accept HH:MM:SS or seconds. reencode=True is frame-accurate;
    default is stream copy (fast, keyframe-snapped).
    """
    src = _check_input(path)
    out = _output_path(src, "_cut.mp4", output)
    if not duration and not end:
        raise FFmpegError("provide either duration or end")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", start]
    if reencode:
        cmd += ["-i", str(src)]
    else:
        cmd += ["-i", str(src)]
    if duration:
        cmd += ["-t", duration]
    elif end:
        cmd += ["-to", end]
    cmd += ["-c:v", "libx264", "-c:a", "aac"] if reencode else ["-c", "copy"]
    cmd.append(str(out))
    _run(cmd)
    return f"wrote {out}"


@mcp.tool()
def extract_audio(path: str, output: str | None = None, codec: str = "aac") -> str:
    """Extract the audio stream into a standalone file (aac/mp3/flac)."""
    src = _check_input(path)
    ext = {"aac": ".m4a", "mp3": ".mp3", "flac": ".flac"}.get(codec, f".{codec}")
    out = _output_path(src, ext, output)
    _run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-vn", "-c:a", codec, str(out)])
    return f"wrote {out}"


@mcp.tool()
def thumbnail(path: str, time: str = "00:00:01", output: str | None = None, scale: int = 720) -> str:
    """Capture a single still frame at `time` scaled to `scale` pixels wide."""
    src = _check_input(path)
    out = _output_path(src, ".jpg", output)
    _run([
        "ffmpeg", "-y", "-loglevel", "error", "-ss", time, "-i", str(src),
        "-frames:v", "1", "-vf", f"scale={scale}:-2", str(out),
    ])
    return f"wrote {out}"


@mcp.tool()
def make_gif(path: str, start: str = "0", duration: str = "3", width: int = 480, fps: int = 12, output: str | None = None) -> str:
    """Convert a short segment into an optimized GIF (palette-based)."""
    src = _check_input(path)
    out = _output_path(src, ".gif", output)
    palette = Path(tempfile.mktemp(suffix=".png"))
    _run([
        "ffmpeg", "-y", "-loglevel", "error", "-ss", start, "-t", duration, "-i", str(src),
        "-vf", f"fps={fps},scale={width}:-2:flags=lanczos,palettegen", str(palette),
    ])
    _run([
        "ffmpeg", "-y", "-loglevel", "error", "-ss", start, "-t", duration, "-i", str(src),
        "-i", str(palette), "-lavfi", f"fps={fps},scale={width}:-2:flags=lanczos[x];[x][1:v]paletteuse",
        str(out),
    ])
    palette.unlink(missing_ok=True)
    return f"wrote {out}"


@mcp.tool()
def concat(paths: list[str], output: str = "concat.mp4") -> str:
    """Concatenate multiple media files with identical codecs (stream copy)."""
    resolved = [_check_input(p) for p in paths]
    if len(resolved) < 2:
        raise FFmpegError("concat requires at least 2 inputs")
    listfile = Path(tempfile.mktemp(suffix=".txt"))
    listfile.write_text("".join(f"file '{p.resolve()}'\n" for p in resolved))
    out = _resolve(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    _run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
          "-i", str(listfile), "-c", "copy", str(out)])
    listfile.unlink(missing_ok=True)
    return f"wrote {out} ({len(resolved)} inputs)"


@mcp.tool()
def normalize_audio(path: str, target_lufs: int = -14, output: str | None = None) -> str:
    """Loudness-normalize audio to a target integrated LUFS via loudnorm."""
    src = _check_input(path)
    out = _output_path(src, "_loudnorm.mp4", output)
    _run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
        "-af", f"loudnorm=I={target_lufs}:TP=-1.5:LRA=11",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", str(out),
    ])
    return f"wrote {out}"


@mcp.tool()
def compress(path: str, quality: str = "medium", output: str | None = None) -> str:
    """Re-encode to a smaller file. quality: low|medium|high maps to CRF 28/23/18."""
    crf = {"low": 28, "medium": 23, "high": 18}.get(quality)
    if crf is None:
        raise FFmpegError(f"unknown quality {quality!r}; use low|medium|high")
    return transcode(path, output, crf=crf, preset="slow")


@mcp.tool()
def extract_frames(path: str, fps: int = 1, output_dir: str | None = None) -> str:
    """Extract frames as PNGs at `fps` into a directory; returns the pattern."""
    src = _check_input(path)
    outdir = _resolve(output_dir or f"{src.stem}_frames")
    outdir.mkdir(parents=True, exist_ok=True)
    pattern = outdir / "frame_%06d.png"
    _run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-vf", f"fps={fps}", str(pattern)])
    return f"frames at {pattern}"


@mcp.tool()
def add_subtitles(path: str, subtitle_path: str, output: str | None = None) -> str:
    """Burn a subtitle file (SRT/ASS/VTT) onto the video."""
    src = _check_input(path)
    subs = _check_input(subtitle_path)
    out = _output_path(src, "_subbed.mp4", output)
    _run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
        "-vf", f"subtitles={shlex.quote(str(subs))}",
        "-c:v", "libx264", "-crf", "20", "-c:a", "copy", str(out),
    ])
    return f"wrote {out}"


@mcp.tool()
def strip_metadata(path: str, output: str | None = None) -> str:
    """Remove all metadata and chapters (useful before publishing)."""
    src = _check_input(path)
    out = _output_path(src, "_clean.mp4", output)
    _run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
          "-map_metadata", "-1", "-map_chapters", "-1", "-c", "copy", str(out)])
    return f"wrote {out}"


if __name__ == "__main__":
    mcp.run()
