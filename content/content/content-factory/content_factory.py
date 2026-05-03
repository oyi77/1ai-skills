#!/usr/bin/env python3
"""
Content Factory - Generate YouTube videos and Shorts from prompts or long videos
Combines best of youtube-factory (100% free tools) and AI-Youtube-Shorts-Generator

Usage:
    python content_factory.py "5 Morning Habits"              # Regular video
    python content_factory.py "Quick Tips" --shorts           # Shorts from scratch
    python content_factory.py "https://youtu.be/VIDEO"       # Shorts from long video
    python content_factory.py "/path/to/video.mp4"           # Shorts from local file

Homepage: https://github.com/Mayank8290/openclaw-video-skills
"""

import os
import sys
import json
import argparse
import tempfile
import subprocess
import re
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from urllib.parse import urlparse, parse_qs
import shutil

# Try importing optional dependencies
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

# =============================================================================
# CONFIGURATION
# =============================================================================

OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "~/Videos/OpenClaw")).expanduser()
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load config from env file (only known keys for security)
_ALLOWED_CONFIG_KEYS = {
    "PEXELS_API_KEY", "OPENAI_API_KEY", "OUTPUT_DIR",
    "DEFAULT_VOICE", "WHISPER_MODEL"
}
_config_path = Path.home() / ".openclaw-content-factory" / "config.env"
if _config_path.exists():
    for line in _config_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            key, val = line.split("=", 1)
            key = key.strip()
            if key in _ALLOWED_CONFIG_KEYS:
                os.environ.setdefault(key, val.strip())

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Default configurations
DEFAULT_VOICE = os.getenv("DEFAULT_VOICE", "en-US-ChristopherNeural")
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")

ALLOWED_STOCK_DOMAINS = [
    "pexels.com", "videos.pexels.com", "images.pexels.com",
]

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def slugify(text: str) -> str:
    """Convert text to URL-friendly slug"""
    text = re.sub(r'[^\w\s-]', '', text).strip()
    text = re.sub(r'[-\s]+', '-', text)
    return text.lower()


def secure_tempfile(suffix: str = "") -> str:
    """Create a secure temporary file"""
    fd, path = tempfile.mkstemp(suffix=suffix)
    os.close(fd)
    return path


def validate_stock_url(url: str) -> bool:
    """Validate URL is from Pexels"""
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False
        return any(
            parsed.netloc == d or parsed.netloc.endswith("." + d)
            for d in ALLOWED_STOCK_DOMAINS
        )
    except Exception:
        return False


def validate_youtube_url(url: str) -> bool:
    """Validate YouTube URL"""
    try:
        parsed = urlparse(url)
        return parsed.netloc in ("youtube.com", "www.youtube.com", "youtu.be")
    except Exception:
        return False


def get_youtube_video_id(url: str) -> Optional[str]:
    """Extract video ID from YouTube URL"""
    try:
        if "youtu.be" in url:
            return url.split("/")[-1].split("?")[0]
        elif "youtube.com" in url:
            query = parse_qs(urlparse(url).query)
            return query.get("v", [None])[0]
    except Exception:
        pass
    return None


# =============================================================================
# TTS FUNCTIONS
# =============================================================================

def text_to_speech(text: str, output_path: str, voice: str = None,
                   rate: str = "+0%", pitch: str = "+0Hz") -> str:
    """Convert text to speech using Edge TTS (free Microsoft voices)"""
    voice = voice or DEFAULT_VOICE

    try:
        result = subprocess.run([
            "edge-tts", "--voice", voice, "--rate", rate,
            "--pitch", pitch, "--text", text, "--write-media", output_path
        ], capture_output=True, text=True, check=True)

        if os.path.exists(output_path):
            logger.info(f"TTS generated: {output_path}")
            return output_path
        else:
            raise FileNotFoundError(f"edge-tts didn't create {output_path}")
    except subprocess.CalledProcessError as e:
        logger.error(f"TTS failed: {e.stderr}")
        raise
    except FileNotFoundError:
        logger.error("edge-tts not found. Install with: pip install edge-tts")
        raise


# =============================================================================
# STOCK FOOTAGE
# =============================================================================

def search_stock_videos(query: str, count: int = 5,
                        orientation: str = "landscape") -> List[Dict]:
    """Search Pexels for free stock videos"""
    if not PEXELS_API_KEY:
        logger.warning("No Pexels API key. Get one free at https://www.pexels.com/api/")
        return []

    if not REQUESTS_AVAILABLE:
        logger.warning("requests library not available")
        return []

    try:
        headers = {"Authorization": PEXELS_API_KEY}
        params = {
            "query": query,
            "per_page": count,
            "orientation": orientation
        }

        response = requests.get(
            "https://api.pexels.com/videos/search",
            headers=headers,
            params=params,
            timeout=30
        )
        response.raise_for_status()

        data = response.json()
        videos = data.get("videos", [])

        results = []
        for video in videos:
            video_files = video.get("video_files", [])
            if video_files:
                # Pick HD version if available
                best_file = min(video_files, key=lambda x: abs(x.get("width", 0) - 1920))
                if validate_stock_url(best_file["link"]):
                    results.append({
                        "url": best_file["link"],
                        "duration": video.get("duration", 0),
                        "width": best_file.get("width", 0),
                        "height": best_file.get("height", 0)
                    })

        return results

    except Exception as e:
        logger.error(f"Error searching stock videos: {e}")
        return []


def download_stock_video(url: str, output_path: str) -> str:
    """Download stock video from Pexels"""
    if not validate_stock_url(url):
        raise ValueError(f"Invalid stock video URL: {url}")

    if not REQUESTS_AVAILABLE:
        raise RuntimeError("requests library not available")

    try:
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()

        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        logger.info(f"Downloaded: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"Error downloading stock video: {e}")
        raise


# =============================================================================
# VIDEO ASSEMBLY
# =============================================================================

def create_video_with_captions(
    video_path: str,
    audio_path: str,
    segments: List[Dict],  # [{"text": "...", "start": 0.0, "end": 5.0}]
    output_path: str,
    style: str = "documentary"
) -> str:
    """
    Create final video with captions burned in using FFmpeg

    Args:
        video_path: Input video file
        audio_path: Audio file
        segments: Text segments with timing
        output_path: Output video file
        style: Caption style (documentary, casual, bold)

    Returns:
        Path to final video
    """
    # Determine caption style
    colors = {
        "documentary": {"color": "white", "bgcolor": "black@0.5", "font": "Arial"},
        "casual": {"color": "#ffeb3b", "bgcolor": "black@0.7", "font": "Arial"},
        "bold": {"color": "#ff5722", "bgcolor": "black@0.7", "font": "Arial-Bold"}
    }
    style_config = colors.get(style, colors["documentary"])

    # Create FFmpeg filter for captions
    filter_complex = []

    for i, seg in enumerate(segments):
        text = seg["text"].replace('"', '\\"').replace("'", "\\'")
        start = seg["start"]
        end = seg["end"]
        duration = end - start

        # Add text overlay
        filter_complex.append(
            f"drawtext=text='{text}':"
            f"fontsize=48:fontcolor={style_config['color']}:"
            f"box=1:boxcolor={style_config['bgcolor']}:"
            f"boxborderw=10:x=(w-text_w)/2:y=h-100:"
            f"enable='between(t,{start},{end})'"
        )

    # Construct FFmpeg command
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-af", "apad=whole_dur=first",
        "-shortest",
        "-vf", ",".join(filter_complex) if filter_complex else "null",
        output_path
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        logger.info(f"Video created with captions: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg failed: {e.stderr.decode()}")
        raise


def assemble_video(
    video_clips: List[str],
    audio_path: str,
    output_path: str
) -> str:
    """
    Assemble multiple video clips into one with audio
    Loops clips if needed to match audio duration
    """
    if not video_clips:
        raise ValueError("No video clips provided")

    # Get audio duration
    audio_dur_cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", audio_path
    ]
    result = subprocess.run(audio_dur_cmd, capture_output=True, text=True)
    audio_duration = float(result.stdout.strip())

    # Calculate total clips duration
    clip_durations = []
    for clip in video_clips:
        cmd = [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", clip
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        clip_durations.append(float(result.stdout.strip()))

    total_clip_duration = sum(clip_durations)

    # Create concat file
    concat_file = secure_tempfile(suffix=".txt")
    with open(concat_file, "w") as f:
        # If clips are shorter than audio, repeat them
        iterations = max(1, int(audio_duration / total_clip_duration) + 1)
        for _ in range(iterations):
            for i, clip in enumerate(video_clips):
                duration = clip_durations[i]
                f.write(f"file '{clip}'\n")
                # Truncate last clip if over
                if sum(clip_durations) > audio_duration:
                    f.write(f"duration {audio_duration:.2f}\n")

    # Assemble
    try:
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", concat_file,
            "-i", audio_path,
            "-c:v", "libx264", "-preset", "medium",
            "-c:a", "aac", "-shortest",
            output_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)

        os.unlink(concat_file)
        logger.info(f"Video assembled: {output_path}")
        return output_path

    except subprocess.CalledProcessError as e:
        if os.path.exists(concat_file):
            os.unlink(concat_file)
        logger.error(f"Assembly failed: {e.stderr.decode()}")
        raise


# =============================================================================
# GENERATION FUNCTIONS
# =============================================================================

def regular_video_mode(
    topic: str,
    style: str = "documentary",
    length_minutes: int = 5,
    voice: str = None
) -> Dict:
    """
    Generate a regular YouTube video from topic prompt

    Returns:
        Dict with paths to generated files
    """
    logger.info(f"Generating regular video for: {topic}")

    slug = slugify(topic)
    output_dir = OUTPUT_DIR / slug
    output_dir.mkdir(exist_ok=True)

    try:
        # 1. Generate script (placeholder -在实际应用中需要LLM)
        script = generate_script(topic, style, length_minutes)
        script_path = output_dir / "script.md"
        script_path.write_text(script)

        # 2. Split script into segments
        segments = split_script_into_segments(script)

        # 3. Generate voiceover
        voiceover_path = output_dir / "voiceover.mp3"
        full_text = "\n\n".join([seg["text"] for seg in segments])
        text_to_speech(full_text, str(voiceover_path), voice)

        # 4. Search and download stock footage
        video_clips = []
        for seg in segments[:3]:  # Limit to 3 keywords for now
            keyword = extract_keyword(seg["text"])
            if keyword:
                videos = search_stock_videos(keyword, count=1, orientation="landscape")
                if videos:
                    clip_path = secure_tempfile(suffix=".mp4")
                    download_stock_video(videos[0]["url"], clip_path)
                    video_clips.append(clip_path)

        # 5. Assemble video
        video_raw_path = output_dir / "video_raw.mp4"
        if video_clips:
            assemble_video(video_clips, str(voiceover_path), str(video_raw_path))
        else:
            logger.warning("No stock footage found, using black background")
            # Create black video
            subprocess.run([
                "ffmpeg", "-y",
                "-f", "lavfi", "-i", f"color=c=black:s=1920x1080:d=00:05:00",
                "-i", str(voiceover_path),
                "-c:v", "libx264", "-c:a", "aac", "-shortest",
                str(video_raw_path)
            ], check=True, capture_output=True)

        # 6. Add captions
        final_path = output_dir / "video_final.mp4"
        create_video_with_captions(
            str(video_raw_path),
            str(voiceover_path),
            segments,
            str(final_path),
            style
        )

        # 7. Generate metadata
        metadata = {
            "title": f"{topic}",
            "description": f"Learn about {topic}",
            "tags": [slug, topic.lower()],
            "generated": datetime.now().isoformat()
        }
        metadata_path = output_dir / "metadata.json"
        metadata_path.write_text(json.dumps(metadata, indent=2))

        # 8. Simple thumbnail (use the first frame of video)
        thumbnail_path = output_dir / "thumbnail.jpg"
        subprocess.run([
            "ffmpeg", "-y",
            "-i", str(final_path),
            "-ss", "00:00:01", "-vframes", "1",
            str(thumbnail_path)
        ], capture_output=True, check=True)

        # Cleanup temp files
        for clip in video_clips:
            if os.path.exists(clip):
                os.unlink(clip)

        return {
            "status": "success",
            "output_dir": str(output_dir),
            "final_video": str(final_path),
            "thumbnail": str(thumbnail_path),
            "script": str(script_path),
            "metadata": str(metadata_path)
        }

    except Exception as e:
        logger.error(f"Error generating video: {e}")
        return {"status": "error", "message": str(e)}


def shorts_from_long_mode(
    video_source: str,
    highlight_duration: int = 60
) -> Dict:
    """
    Generate YouTube Shorts from long video

    Args:
        video_source: YouTube URL or local video path
        highlight_duration: Duration in seconds for the short clip

    Returns:
        Dict with paths to generated files
    """
    logger.info(f"Generating shorts from: {video_source}")

    if validate_youtube_url(video_source):
        # YouTube URL mode
        video_id = get_youtube_video_id(video_source)
        if not video_id:
            return {"status": "error", "message": "Invalid YouTube URL"}

        slug = f"youtube_{video_id}"
    else:
        # Local file mode
        if not os.path.exists(video_source):
            return {"status": "error", "message": "Video file not found"}

        video_name = Path(video_source).stem
        slug = slugify(video_name)

    output_dir = OUTPUT_DIR / slug
    output_dir.mkdir(exist_ok=True)

    try:
        # Download/load video
        if validate_youtube_url(video_source):
            logger.info(f"Downloading YouTube video: {video_source}")
            video_path = output_dir / "source.mp4"
            download_youtube_video(video_source, str(video_path))
        else:
            video_path = Path(video_source)

        # Check Whisper availability
        if not WHISPER_AVAILABLE:
            logger.warning("Whisper not available. Install with: pip install openai-whisper")
            # Fallback: create short from middle
            return shorts_simple_extraction(
                str(video_path),
                output_dir,
                highlight_duration
            )

        # Extract audio
        audio_path = output_dir / "audio.wav"
        subprocess.run([
            "ffmpeg", "-y", "-i", str(video_path),
            "-vn", "-acodec", "pcm_s16le", "-ar", "16000",
            str(audio_path)
        ], check=True, capture_output=True)

        # Transcribe with Whisper
        logger.info("Transcribing audio with Whisper...")
        model = whisper.load_model(WHISPER_MODEL)
        result = model.transcribe(str(audio_path))

        # Find best highlight
        segments = result["segments"]
        highlight = find_best_highlight(segments, highlight_duration)

        # Extract clip
        short_path = output_dir / f"{slug}_short_cropped.mp4"
        extract_video_segment(
            str(video_path),
            highlight["start"],
            highlight["end"],
            str(short_path)
        )

        # Crop to 9:16
        final_short_path = output_dir / f"{slug}_short.mp4"
        crop_to_vertical(
            str(short_path),
            str(final_short_path)
        )

        # Get transcript for captions
        caption_path = output_dir / "captions.txt"
        caption_text = " ".join([
            seg["text"] for seg in segments
            if seg["start"] >= highlight["start"] and seg["end"] <= highlight["end"]
        ])
        caption_path.write_text(caption_text)

        # Clean up
        if os.path.exists(str(video_path)):
            os.unlink(str(video_path))
        if os.path.exists(str(audio_path)):
            os.unlink(str(audio_path))
        if os.path.exists(str(short_path)):
            os.unlink(str(short_path))

        return {
            "status": "success",
            "output_dir": str(output_dir),
            "final_video": str(final_short_path),
            "captions": str(caption_path),
            "highlight_range": f"{highlight['start']:.1f}s - {highlight['end']:.1f}s"
        }

    except Exception as e:
        logger.error(f"Error generating shorts: {e}")
        return {"status": "error", "message": str(e)}


# =============================================================================
# HELPER FUNCTIONS (Simplified implementations)
# =============================================================================

def generate_script(topic: str, style: str, length_minutes: int) -> str:
    """Generate a script for the topic (placeholder for LLM integration)"""
    # In real implementation, this would call an LLM API
    num_sections = length_minutes
    sections = []

    for i in range(1, num_sections + 1):
        sections.append(f"""
## Section {i}: {topic} - Part {i}

{topic} is fascinating topic that deserves attention. In this section, we'll explore
key aspects related to {topic} that everyone should know.

Did you know that {topic} has been around for quite some time? Many people find
learning about {topic} to be both educational and inspiring.

Let's dive into the details of {topic} and discover what makes it so special.
        """.strip())

    return f"# {topic}\n\n" + "\n\n".join(sections)


def split_script_into_segments(script: str) -> List[Dict]:
    """Split script into timed segments"""
    lines = [line.strip() for line in script.split("\n") if line.strip()]
    segments = []
    current_time = 0.0

    for line in lines:
        if line.startswith("#"):
            continue
        # Estimate 5 seconds per segment
        duration = 5.0
        segments.append({
            "text": line,
            "start": current_time,
            "end": current_time + duration
        })
        current_time += duration

    return segments


def extract_keyword(text: str) -> str:
    """Extract main keyword from text"""
    # Simple implementation - take first meaningful word
    words = text.split()
    if words:
        return words[0].lower()
    return ""


def find_best_highlight(segments: List[Dict], duration: int) -> Dict:
    """Find the most engaging segment from transcription"""
    # Simple implementation: take first viable segment
    total_duration = segments[-1]["end"] - segments[0]["start"]

    if total_duration <= duration:
        return {
            "start": segments[0]["start"],
            "end": segments[-1]["end"]
        }

    # Find first N seconds
    for i, seg in enumerate(segments):
        if seg["end"] - segments[0]["start"] >= duration:
            return {
                "start": segments[0]["start"],
                "end": seg["end"]
            }

    return {
        "start": segments[0]["start"],
        "end": segments[0]["start"] + duration
    }


def shorts_simple_extraction(
    video_path: str,
    output_dir: Path,
    duration: int
) -> Dict:
    """
    Simple short extraction without Whisper
    Extracts middle portion of video
    """
    try:
        # Get video duration
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        video_duration = float(result.stdout.strip())

        # Extract middle portion
        start_time = max(0, (video_duration - duration) / 2)

        temp_path = output_dir / "temp_short.mp4"
        extract_video_segment(video_path, start_time, start_time + duration, str(temp_path))

        # Crop to vertical
        final_path = output_dir / "video_short.mp4"
        crop_to_vertical(str(temp_path), str(final_path))

        os.unlink(str(temp_path))

        return {
            "status": "success",
            "output_dir": str(output_dir),
            "final_video": str(final_path),
            "note": "Simple extraction without AI transcription"
        }

    except Exception as e:
        logger.error(f"Simple extraction failed: {e}")
        return {"status": "error", "message": str(e)}


def download_youtube_video(url: str, output_path: str) -> str:
    """Download YouTube video (requires yt-dlp)"""
    try:
        cmd = [
            "yt-dlp", "-f", "best", "-o", output_path,
            "--merge-output-format", "mp4", url
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        logger.info(f"Downloaded YouTube video to: {output_path}")
        return output_path
    except FileNotFoundError:
        # Try as is (yt-dlp might have different name)
        alt_cmd = [
            "youtube-dl", "-f", "best", "-o", output_path, url
        ]
        try:
            subprocess.run(alt_cmd, check=True, capture_output=True)
            return output_path
        except FileNotFoundError:
            logger.error("yt-dlp or youtube-dl not found. Install with: pip install yt-dlp")
            raise
    except subprocess.CalledProcessError as e:
        logger.error(f"Download failed: {e.stderr.decode()}")
        raise


def extract_video_segment(
    video_path: str,
    start: float,
    end: float,
    output_path: str
) -> str:
    """Extract a segment from video"""
    duration = end - start
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start),
        "-i", video_path,
        "-t", str(duration),
        "-c", "copy",
        output_path
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


def crop_to_vertical(input_path: str, output_path: str) -> str:
    """Crop video to 9:16 vertical format"""
    # Smart crop: center the content
    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-vf", "crop=ih*9/16:ih:(iw-ih*9/16)/2:0",
        "-c:a", "copy",
        output_path
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Content Factory - Generate YouTube videos and Shorts"
    )

    parser.add_argument(
        "input",
        help="Topic for regular video, or YouTube URL/local file for Shorts"
    )
    parser.add_argument(
        "--shorts",
        action="store_true",
        help="Generate YouTube Shorts (vertical 9:16)"
    )
    parser.add_argument(
        "--style",
        choices=["documentary", "listicle", "tutorial", "casual"],
        default="documentary",
        help="Video style"
    )
    parser.add_argument(
        "--length",
        type=int,
        default=5,
        help="Video length in minutes (for regular videos)"
    )
    parser.add_argument(
        "--voice",
        help="TTS voice name"
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=60,
        help="Shorts duration in seconds (for shorts-from-long mode)"
    )

    args = parser.parse_args()

    if args.shorts or validate_youtube_url(args.input) or os.path.exists(args.input):
        # Shorts mode
        result = shorts_from_long_mode(args.input, args.duration)
    else:
        # Regular video mode
        result = regular_video_mode(
            args.input,
            args.style,
            args.length,
            args.voice
        )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()