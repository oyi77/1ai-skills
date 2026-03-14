"""
Auto Clipper Indonesia - Subtitle Engine
Subtitle generation, styling, and hardcoding
"""

import os
import subprocess
import logging
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass

# Settings
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils.config import (
    SUBTITLE_FONT_FAMILY, SUBTITLE_FONT_SIZE, SUBTITLE_FONT_COLOR,
    SUBTITLE_STROKE_COLOR, SUBTITLE_STROKE_WIDTH, SUBTITLE_POSITION,
    TEMP_DIR, OUTPUT_DIR
)
from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class SubtitleStyle:
    """Subtitle styling configuration"""
    font: str = SUBTITLE_FONT_FAMILY
    size: int = SUBTITLE_FONT_SIZE
    color: str = SUBTITLE_FONT_COLOR
    stroke_color: str = SUBTITLE_STROKE_COLOR
    stroke_width: int = SUBTITLE_STROKE_WIDTH
    position: str = SUBTITLE_POSITION
    x_offset: int = 0
    y_offset: int = 0
    bold: bool = False
    italic: bool = False
    shadow: bool = True
    shadow_color: str = "black"
    shadow_offset: int = 2


class SubtitleEngine:
    """
    Subtitle Engine - Generate, style, and burn subtitles into video
    """

    def __init__(self):
        """Initialize the subtitle engine"""
        self.ffmpeg_available = self._check_ffmpeg()
        self.styles = {}
        self.default_style = SubtitleStyle()

        logger.info(f"SubtitleEngine initialized (FFmpeg: {'✅' if self.ffmpeg_available else '❌'})")

    def _check_ffmpeg(self) -> bool:
        """Check if FFmpeg is available"""
        try:
            result = subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def generate_srt(
        self,
        transcript: List[Dict],
        output_path: str = None
    ) -> str:
        """
        Generate SRT subtitle file from transcript

        Args:
            transcript: List of transcript segments
            output_path: Output SRT file path

        Returns:
            Path to SRT file
        """
        if output_path is None:
            output_path = TEMP_DIR / f"subtitles.srt"

        output_path = Path(output_path)

        with open(output_path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(transcript, 1):
                start = self._format_time_srt(segment['start'])
                end = self._format_time_srt(segment['end'])
                text = segment.get('text', '').strip()

                f.write(f"{i}\n")
                f.write(f"{start} --> {end}\n")
                f.write(f"{text}\n\n")

        logger.info(f"SRT generated: {output_path}")
        return str(output_path)

    def _format_time_srt(self, seconds: float) -> str:
        """Format seconds to SRT time format (00:00:00,000)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)

        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    def generate_vtt(
        self,
        transcript: List[Dict],
        output_path: str = None
    ) -> str:
        """
        Generate WebVTT subtitle file from transcript

        Args:
            transcript: List of transcript segments
            output_path: Output VTT file path

        Returns:
            Path to VTT file
        """
        if output_path is None:
            output_path = TEMP_DIR / f"subtitles.vtt"

        output_path = Path(output_path)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("WEBVTT\n\n")

            for i, segment in enumerate(transcript, 1):
                start = self._format_time_vtt(segment['start'])
                end = self._format_time_vtt(segment['end'])
                text = segment.get('text', '').strip()

                f.write(f"{i}\n")
                f.write(f"{start} --> {end}\n")
                f.write(f"{text}\n\n")

        logger.info(f"VTT generated: {output_path}")
        return str(output_path)

    def _format_time_vtt(self, seconds: float) -> str:
        """Format seconds to VTT time format (00:00:00.000)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)

        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"

    def burn_subtitles(
        self,
        video_path: str,
        subtitle_path: str,
        output_path: str = None,
        style: SubtitleStyle = None
    ) -> str:
        """
        Burn subtitles into video using FFmpeg

        Args:
            video_path: Source video path
            subtitle_path: SRT/VTT subtitle file path
            output_path: Output video path
            style: Subtitle style configuration

        Returns:
            Path to output video
        """
        if not self.ffmpeg_available:
            raise RuntimeError("FFmpeg not available")

        if style is None:
            style = self.default_style

        if output_path is None:
            output_path = OUTPUT_DIR / f"{Path(video_path).stem}_subtitled.mp4"

        output_path = Path(output_path)

        # Build subtitle filter
        subtitle_filter = f"subtitles={subtitle_path}"

        if style.stroke_width > 0:
            subtitle_filter += f":force_style='FontName={style.font},FontSize={style.size},PrimaryColour=&H{self._color_to_ass(style.color)},OutlineColour=&H{self._color_to_ass(style.stroke_color)},Outline={style.stroke_width},BorderStyle=3'"

        cmd = [
            'ffmpeg', '-y',
            '-i', str(video_path),
            '-vf', subtitle_filter,
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            '-c:a', 'copy',
            '-movflags', '+faststart',
            str(output_path)
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Subtitles burned: {output_path}")
            return str(output_path)
        except subprocess.CalledProcessError as e:
            logger.error(f"Subtitle burning failed: {e}")
            raise

    def burn_custom_subtitles(
        self,
        video_path: str,
        subtitles: List[Dict],
        output_path: str = None,
        style: SubtitleStyle = None
    ) -> str:
        """
        Burn custom subtitles (from list) into video

        Args:
            video_path: Source video path
            subtitles: List of subtitle dicts with 'text', 'start', 'end'
            output_path: Output video path
            style: Subtitle style configuration

        Returns:
            Path to output video
        """
        if not self.ffmpeg_available:
            raise RuntimeError("FFmpeg not available")

        if style is None:
            style = self.default_style

        if output_path is None:
            output_path = OUTPUT_DIR / f"{Path(video_path).stem}_subtitled.mp4"

        # Generate SRT first
        srt_path = self.generate_srt(subtitles)

        # Burn subtitles
        return self.burn_subtitles(video_path, srt_path, output_path, style)

    def add_simple_subtitles(
        self,
        video_path: str,
        text: str,
        start_time: float,
        end_time: float,
        output_path: str = None,
        font_size: int = 28,
        font_color: str = "white",
        stroke_color: str = "black",
        stroke_width: int = 2,
        position: str = "bottom"
    ) -> str:
        """
        Add simple text subtitle to video

        Args:
            video_path: Source video path
            text: Subtitle text
            start_time: Start time in seconds
            end_time: End time in seconds
            output_path: Output video path
            font_size: Font size
            font_color: Font color
            stroke_color: Outline color
            stroke_width: Outline width
            position: Text position

        Returns:
            Path to output video
        """
        if not self.ffmpeg_available:
            raise RuntimeError("FFmpeg not available")

        if output_path is None:
            output_path = OUTPUT_DIR / f"{Path(video_path).stem}_subtitle.mp4"

        # Clean text for FFmpeg
        text_escaped = text.replace("'", "\\'").replace(":", "\\:").replace("\n", " ")

        # Get video dimensions for positioning
        width, height = 1080, 1920  # 9:16

        # Calculate position
        if position == "bottom":
            y_pos = height - font_size * 2
        elif position == "top":
            y_pos = font_size
        else:
            y_pos = height // 2

        # Build drawtext filter
        drawtext_filter = (
            f"drawtext=text='{text_escaped}':"
            f"fontcolor={font_color}:"
            f"fontsize={font_size}:"
            f"x=(w-text_w)/2:"
            f"y={y_pos}:"
            f"borderw={stroke_width}:"
            f"bordercolor={stroke_color}:"
            f"enable='between(t,{start_time},{end_time})'"
        )

        cmd = [
            'ffmpeg', '-y',
            '-i', str(video_path),
            '-vf', drawtext_filter,
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            '-c:a', 'copy',
            '-movflags', '+faststart',
            str(output_path)
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Simple subtitle added: {output_path}")
            return str(output_path)
        except subprocess.CalledProcessError as e:
            logger.error(f"Simple subtitle failed: {e}")
            raise

    def _color_to_ass(self, color: str) -> str:
        """
        Convert color name to ASS/SSA format

        Args:
            color: Color name (white, black, red, etc.)

        Returns:
            ASS color string
        """
        color_map = {
            'white': '&H00FFFFFF',
            'black': '&H00000000',
            'yellow': '&H00FFFF00',
            'red': '&H000000FF',
            'green': '&H0000FF00',
            'blue': '&H00FF0000',
            'cyan': '&H00FFFF00',
            'magenta': '&H00FF00FF',
        }
        return color_map.get(color.lower(), '&H00FFFFFF')

    def create_style(self, name: str, style: SubtitleStyle):
        """
        Create a named subtitle style

        Args:
            name: Style name
            style: SubtitleStyle configuration
        """
        self.styles[name] = style
        logger.info(f"Subtitle style '{name}' created")

    def apply_style(self, name: str) -> SubtitleStyle:
        """Get a named subtitle style"""
        return self.styles.get(name, self.default_style)


# Predefined styles
class SubtitleStyles:
    """Predefined subtitle styles"""

    @staticmethod
    def clean() -> SubtitleStyle:
        """Clean, minimal subtitles"""
        return SubtitleStyle(
            font="Arial",
            size=24,
            color="white",
            stroke_color="black",
            stroke_width=2,
            position="bottom"
        )

    @staticmethod
    def bold() -> SubtitleStyle:
        """Bold, attention-grabbing subtitles"""
        return SubtitleStyle(
            font="Arial Bold",
            size=32,
            color="yellow",
            stroke_color="black",
            stroke_width=3,
            position="bottom",
            bold=True
        )

    @staticmethod
    def social() -> SubtitleStyle:
        """Social media optimized subtitles (larger)"""
        return SubtitleStyle(
            font="Arial",
            size=36,
            color="white",
            stroke_color="black",
            stroke_width=4,
            position="bottom",
            shadow=True,
            shadow_color="black"
        )

    @staticmethod
    def tiktok() -> SubtitleStyle:
        """TikTok-specific subtitle style"""
        return SubtitleStyle(
            font="Montserrat Bold",
            size=40,
            color="white",
            stroke_color="black",
            stroke_width=5,
            position="top"
        )


# Standalone test function
if __name__ == "__main__":
    print("=" * 60)
    print("AUTO CLIPPER INDONESIA - SUBTITLE ENGINE TEST")
    print("=" * 60)

    engine = SubtitleEngine()

    if not engine.ffmpeg_available:
        print("\n[ERROR] FFmpeg not found!")
        exit(1)

    print(f"\nFFmpeg available: {'✅' if engine.ffmpeg_available else '❌'}")

    # Test with sample subtitle
    print("\n🧪 Testing SRT generation...")
    sample_transcript = [
        {'start': 0.0, 'end': 5.0, 'text': 'Halo selamat datang di channel ini!'},
        {'start': 5.0, 'end': 10.0, 'text': 'Hari ini kita akan belajar sesuatu yang amazing.'},
        {'start': 10.0, 'end': 15.0, 'text': 'Jangan lupa subscribe dan like ya!'},
    ]

    srt_path = engine.generate_srt(sample_transcript)
    print(f"✅ SRT generated: {srt_path}")

    print("\n🧪 Testing VTT generation...")
    vtt_path = engine.generate_vtt(sample_transcript)
    print(f"✅ VTT generated: {vtt_path}")

    print("\n✅ SubtitleEngine test complete")
    print("\nUsage examples:")
    print("  # Generate SRT from transcript")
    print("  srt = engine.generate_srt(transcript)")
    print("")
    print("  # Burn subtitles into video")
    print("  output = engine.burn_subtitles('video.mp4', 'subs.srt')")
    print("")
    print("  # Add simple text subtitle")
    print("  output = engine.add_simple_subtitles('video.mp4', 'Check this out!', 5, 10)")