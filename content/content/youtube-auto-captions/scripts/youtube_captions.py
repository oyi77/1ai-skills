#!/usr/bin/env python3
"""Fetch YouTube auto-captions and output as SRT, VTT, or plain text."""

import argparse
import os
import re
import sys

from youtube_transcript_api import YouTubeTranscriptApi


OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output"
)


# ---------------------------------------------------------------------------
# Video ID extraction
# ---------------------------------------------------------------------------

def extract_video_id(url_or_id: str) -> str:
    """Return a YouTube video ID from a URL or bare ID string."""
    patterns = [
        r"(?:youtube\.com/watch\?.*v=)([A-Za-z0-9_-]{11})",
        r"(?:youtu\.be/)([A-Za-z0-9_-]{11})",
        r"(?:youtube\.com/embed/)([A-Za-z0-9_-]{11})",
        r"(?:youtube\.com/v/)([A-Za-z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    # Assume bare video ID
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url_or_id):
        return url_or_id
    raise ValueError(f"Could not extract video ID from: {url_or_id}")


# ---------------------------------------------------------------------------
# Timestamp helpers
# ---------------------------------------------------------------------------

def _seconds_to_srt_ts(seconds: float) -> str:
    """Convert seconds to SRT timestamp HH:MM:SS,mmm."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds - int(seconds)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _seconds_to_vtt_ts(seconds: float) -> str:
    """Convert seconds to VTT timestamp HH:MM:SS.mmm."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds - int(seconds)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def format_srt(transcript: list[dict]) -> str:
    lines: list[str] = []
    for i, entry in enumerate(transcript, start=1):
        start = entry["start"]
        end = start + entry.get("duration", 0)
        lines.append(str(i))
        lines.append(f"{_seconds_to_srt_ts(start)} --> {_seconds_to_srt_ts(end)}")
        lines.append(entry["text"])
        lines.append("")
    return "\n".join(lines)


def format_vtt(transcript: list[dict]) -> str:
    lines: list[str] = ["WEBVTT", ""]
    for entry in transcript:
        start = entry["start"]
        end = start + entry.get("duration", 0)
        lines.append(f"{_seconds_to_vtt_ts(start)} --> {_seconds_to_vtt_ts(end)}")
        lines.append(entry["text"])
        lines.append("")
    return "\n".join(lines)


def format_text(transcript: list[dict]) -> str:
    return "\n".join(entry["text"] for entry in transcript)


FORMATTERS = {
    "srt": format_srt,
    "vtt": format_vtt,
    "text": format_text,
}

FORMAT_EXT = {
    "srt": ".srt",
    "vtt": ".vtt",
    "text": ".txt",
}


# ---------------------------------------------------------------------------
# Translation via OmniRoute LLM
# ---------------------------------------------------------------------------

def translate_text(text: str, target_lang: str) -> str:
    """Translate the full caption text using the local OmniRoute LLM."""
    from openai import OpenAI

    client = OpenAI(
        base_url="http://localhost:20128/v1",
        api_key="omniroute",
    )

    response = client.chat.completions.create(
        model="auto",
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are a professional translator. Translate the following "
                    f"subtitle text into language code '{target_lang}'. "
                    f"Preserve all timestamp lines and numbering exactly as-is. "
                    f"Only translate the spoken-text lines."
                ),
            },
            {"role": "user", "content": text},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch YouTube captions and output as SRT, VTT, or plain text."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="YouTube video URL")
    group.add_argument("--video-id", help="YouTube video ID (11 characters)")
    parser.add_argument(
        "--format",
        choices=["srt", "vtt", "text"],
        default="srt",
        help="Output format (default: srt)",
    )
    parser.add_argument(
        "--translate",
        metavar="LANG",
        help="Translate captions to the given language code (e.g. 'id' for Indonesian)",
    )

    args = parser.parse_args()

    # Resolve video ID
    video_id = args.video_id if args.video_id else extract_video_id(args.url)

    # Fetch transcript
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as exc:
        print(f"Error fetching transcript: {exc}", file=sys.stderr)
        sys.exit(1)

    # Format
    formatter = FORMATTERS[args.format]
    output = formatter(transcript)

    # Optionally translate
    if args.translate:
        try:
            output = translate_text(output, args.translate)
        except Exception as exc:
            print(f"Warning: translation failed ({exc}), using original text.", file=sys.stderr)

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Write to file
    ext = FORMAT_EXT[args.format]
    lang_suffix = f"_{args.translate}" if args.translate else ""
    filename = f"{video_id}{lang_suffix}{ext}"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"Saved to {filepath}", file=sys.stderr)

    # Print to stdout
    print(output)


if __name__ == "__main__":
    main()
