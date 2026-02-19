"""
FFmpeg Editor - Advanced Video Editing Module

Provides comprehensive video editing capabilities using FFmpeg subprocess calls.
Supports trimming, text overlays, filters, transitions, audio mixing, and composition.
"""

import subprocess
import os
import tempfile
from dataclasses import dataclass
from typing import Optional
from enum import Enum


class Transition(Enum):
    """Video transition types"""

    FADE = "fade"
    DISSOLVE = "dissolve"
    SLIDE_LEFT = "slide_left"
    SLIDE_RIGHT = "slide_right"
    ZOOM_IN = "zoom_in"
    WIPE = "wipe"


class TextPosition(Enum):
    """Text positioning options"""

    TOP = "top"
    BOTTOM = "bottom"
    CENTER = "center"
    TOP_LEFT = "top_left"
    TOP_RIGHT = "top_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_RIGHT = "bottom_right"


@dataclass
class TextOverlay:
    """Text overlay configuration"""

    text: str
    position: TextPosition
    font_size: int = 24
    font_color: str = "white"
    background_color: Optional[str] = None
    start_time: float = 0
    duration: Optional[float] = None
    font: str = "Sans"


@dataclass
class FilterConfig:
    """Video filter configuration"""

    brightness: Optional[float] = None
    contrast: Optional[float] = None
    saturation: Optional[float] = None
    blur: Optional[int] = None
    vignette: bool = False
    grayscale: bool = False
    sepia: bool = False
    sharpness: Optional[float] = None
    gamma: Optional[float] = None


class FFmpegEditor:
    """Advanced video editing using FFmpeg subprocess calls"""

    def __init__(self, ffmpeg_path: str = "ffmpeg", ffprobe_path: str = "ffprobe"):
        """
        Initialize FFmpegEditor

        Args:
            ffmpeg_path: Path to ffmpeg binary (default: 'ffmpeg')
            ffprobe_path: Path to ffprobe binary (default: 'ffprobe')
        """
        self.ffmpeg = ffmpeg_path
        self.ffprobe = ffprobe_path

    def _run_ffmpeg(
        self, args: list, capture_output: bool = False
    ) -> subprocess.CompletedProcess:
        """Run ffmpeg command with arguments"""
        cmd = [self.ffmpeg] + args
        if capture_output:
            return subprocess.run(cmd, capture_output=True, text=True)
        return subprocess.run(cmd)

    def _get_video_duration(self, input_path: str) -> float:
        """Get video duration using ffprobe"""
        cmd = [
            self.ffprobe,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            input_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return float(result.stdout.strip()) if result.stdout.strip() else 0.0

    def _get_video_info(self, input_path: str) -> dict:
        """Get video information (resolution, fps, etc.)"""
        cmd = [
            self.ffprobe,
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height,r_frame_rate",
            "-of",
            "csv=s=,:p=0",
            input_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.stdout.strip():
            parts = result.stdout.strip().split(",")
            if len(parts) >= 3:
                fps_parts = parts[2].split("/")
                fps = (
                    float(fps_parts[0]) / float(fps_parts[1])
                    if len(fps_parts) == 2
                    else float(fps_parts[0])
                )
                return {"width": int(parts[0]), "height": int(parts[1]), "fps": fps}
        return {"width": 1920, "height": 1080, "fps": 30.0}

    # ============ CUTTING & TRIMMING ============

    def trim(
        self,
        input_path: str,
        output_path: str,
        start: float,
        duration: Optional[float] = None,
    ) -> str:
        """
        Trim video to specified start time and optional duration

        Args:
            input_path: Source video path
            output_path: Output video path
            start: Start time in seconds
            duration: Optional duration in seconds

        Returns:
            Output path on success
        """
        args = ["-y", "-ss", str(start)]
        if duration:
            args.extend(["-t", str(duration)])
        args.extend(["-i", input_path, "-c", "copy", output_path])
        self._run_ffmpeg(args)
        return output_path

    def cut_scenes(
        self, input_path: str, output_path: str, timestamps: list[tuple[float, float]]
    ) -> str:
        """
        Cut multiple scenes from video

        Args:
            input_path: Source video path
            output_path: Output video path
            timestamps: List of (start, end) tuples in seconds

        Returns:
            Output path on success
        """
        # Create concat demuxer file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            concat_file = f.name
            for start, end in timestamps:
                f.write(f"file '{input_path}'\n")
                f.write(f"inpoint {start}\n")
                f.write(f"outpoint {end}\n")

        try:
            args = [
                "-y",
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
            self._run_ffmpeg(args)
        finally:
            os.unlink(concat_file)
        return output_path

    # ============ SPEED & MOTION ============

    def change_speed(self, input_path: str, output_path: str, speed: float) -> str:
        """
        Change video playback speed

        Args:
            input_path: Source video path
            output_path: Output video path
            speed: Speed factor (2.0 = 2x faster, 0.5 = 2x slower)

        Returns:
            Output path on success
        """
        video_duration = self._get_video_duration(input_path)
        new_duration = video_duration / speed

        args = [
            "-y",
            "-i",
            input_path,
            "-filter:v",
            f"setpts={1 / speed}*PTS",
            "-filter:a",
            f"atempo={speed}",
            "-t",
            str(new_duration),
            output_path,
        ]
        self._run_ffmpeg(args)
        return output_path

    def slow_motion(
        self, input_path: str, output_path: str, factor: float = 2.0
    ) -> str:
        """
        Create slow motion effect

        Args:
            input_path: Source video path
            output_path: Output video path
            factor: Slow motion factor (default 2.0 = half speed)

        Returns:
            Output path on success
        """
        return self.change_speed(input_path, output_path, 1.0 / factor)

    # ============ TEXT & OVERLAYS ============

    def _get_text_position_coords(
        self,
        position: TextPosition,
        video_width: int,
        video_height: int,
        font_size: int,
    ) -> tuple:
        """Convert TextPosition to x,y coordinates"""
        margin = 20
        x, y = "0", "0"

        if position == TextPosition.TOP:
            x, y = "(w-tw)/2", str(margin)
        elif position == TextPosition.BOTTOM:
            x, y = "(w-tw)/2", f"h-th-{margin}"
        elif position == TextPosition.CENTER:
            x, y = "(w-tw)/2", "(h-th)/2"
        elif position == TextPosition.TOP_LEFT:
            x, y = str(margin), str(margin)
        elif position == TextPosition.TOP_RIGHT:
            x, y = f"w-tw-{margin}", str(margin)
        elif position == TextPosition.BOTTOM_LEFT:
            x, y = str(margin), f"h-th-{margin}"
        elif position == TextPosition.BOTTOM_RIGHT:
            x, y = f"w-tw-{margin}", f"h-th-{margin}"

        return x, y

    def add_text(
        self, input_path: str, output_path: str, overlays: list[TextOverlay]
    ) -> str:
        """
        Add text overlays to video

        Args:
            input_path: Source video path
            output_path: Output video path
            overlays: List of TextOverlay configurations

        Returns:
            Output path on success
        """
        video_info = self._get_video_info(input_path)
        width, height = video_info["width"], video_info["height"]

        # Build drawtext filters
        filter_parts = []

        for i, overlay in enumerate(overlays):
            x, y = self._get_text_position_coords(
                overlay.position, width, height, overlay.font_size
            )

            # Escape text for FFmpeg
            escaped_text = overlay.text.replace("'", "\\'").replace(":", "\\:")

            # Build drawtext filter
            drawtext = f"drawtext=text='{escaped_text}':fontsize={overlay.font_size}:fontcolor={overlay.font_color}"
            drawtext += f":x={x}:y={y}:font={overlay.font}"

            if overlay.background_color:
                drawtext += f":box=1:boxcolor={overlay.background_color}:boxborderw=10"

            if overlay.start_time > 0 or overlay.duration:
                # Enable text at start_time and disable after duration
                enable_expr = ""
                if overlay.start_time > 0:
                    enable_expr += f"gte(t,{overlay.start_time})"
                if overlay.duration:
                    end_time = overlay.start_time + overlay.duration
                    if enable_expr:
                        enable_expr += "*"
                    enable_expr += f"lt(t,{end_time})"
                drawtext += f":enable='{enable_expr}'"

            filter_parts.append(drawtext)

        # Chain all filters
        filter_chain = ";".join(filter_parts)

        args = [
            "-y",
            "-i",
            input_path,
            "-vf",
            filter_chain,
            "-c:a",
            "copy",
            output_path,
        ]
        self._run_ffmpeg(args)
        return output_path

    def add_subtitles(
        self, input_path: str, subtitle_path: str, output_path: str
    ) -> str:
        """
        Burn subtitles into video from SRT/VTT file

        Args:
            input_path: Source video path
            subtitle_path: Path to SRT or VTT subtitle file
            output_path: Output video path

        Returns:
            Output path on success
        """
        # Determine subtitle format
        ext = os.path.splitext(subtitle_path)[1].lower()
        if ext == ".srt":
            sub_codec = "srt"
        elif ext == ".vtt":
            sub_codec = "webvtt"
        else:
            sub_codec = "srt"

        args = [
            "-y",
            "-i",
            input_path,
            "-i",
            subtitle_path,
            "-c:s",
            sub_codec,
            "-c:a",
            "copy",
            output_path,
        ]
        self._run_ffmpeg(args)
        return output_path

    def add_watermark(
        self,
        input_path: str,
        watermark_path: str,
        output_path: str,
        position: str = "top_right",
        opacity: float = 0.5,
    ) -> str:
        """
        Add watermark/logo overlay

        Args:
            input_path: Source video path
            watermark_path: Path to watermark image (PNG with transparency)
            output_path: Output video path
            position: Position (top_left, top_right, bottom_left, bottom_right, center)
            opacity: Watermark opacity (0.0 to 1.0)

        Returns:
            Output path on success
        """
        # Position coordinates
        pos_coords = {
            "top_left": "10:10",
            "top_right": "W-w-10:10",
            "bottom_left": "10:H-h-10",
            "bottom_right": "W-w-10:H-h-10",
            "center": "(W-w)/2:(H-h)/2",
        }

        overlay_pos = pos_coords.get(position, pos_coords["top_right"])

        # Use colorchannelmixer to adjust opacity
        alpha = f"colorchannelmixer=aa={opacity}"

        args = [
            "-y",
            "-i",
            input_path,
            "-i",
            watermark_path,
            "-filter_complex",
            f"[1:v]{alpha},scale=120:-1[watermark];[0:v][watermark]overlay={overlay_pos}",
            "-c:a",
            "copy",
            output_path,
        ]
        self._run_ffmpeg(args)
        return output_path

    # ============ FILTERS & COLOR ============

    def apply_filters(
        self, input_path: str, output_path: str, filters: FilterConfig
    ) -> str:
        """
        Apply video filters

        Args:
            input_path: Source video path
            output_path: Output video path
            filters: FilterConfig with filter settings

        Returns:
            Output path on success
        """
        filter_parts = []

        # Brightness (-1 to 1)
        if filters.brightness is not None:
            filter_parts.append(f"eq=brightness={filters.brightness}")

        # Contrast (0 to 2)
        if filters.contrast is not None:
            if filter_parts:
                filter_parts[-1] += f":contrast={filters.contrast}"
            else:
                filter_parts.append(f"eq=contrast={filters.contrast}")

        # Saturation (0 to 3)
        if filters.saturation is not None:
            if filter_parts:
                filter_parts[-1] += f":saturation={filters.saturation}"
            else:
                filter_parts.append(f"eq=saturation={filters.saturation}")

        # Gamma
        if filters.gamma is not None:
            if filter_parts:
                filter_parts[-1] += f":gamma={filters.gamma}"
            else:
                filter_parts.append(f"eq=gamma={filters.gamma}")

        # Sharpness
        if filters.sharpness is not None:
            filter_parts.append(f"unsharp=5:5:{filters.sharpness}")

        # Blur
        if filters.blur is not None:
            filter_parts.append(f"boxblur=1r=1:blurradius={filters.blur}")

        # Grayscale
        if filters.grayscale:
            filter_parts.append("hue=s=0")

        # Sepia
        if filters.sepia:
            filter_parts.append(
                "colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.131:.534"
            )

        # Vignette
        if filters.vignette:
            filter_parts.append("vignette=angle=0.5")

        if not filter_parts:
            # No filters, just copy
            args = ["-y", "-i", input_path, "-c", "copy", output_path]
        else:
            filter_chain = ",".join(filter_parts)
            args = [
                "-y",
                "-i",
                input_path,
                "-vf",
                filter_chain,
                "-c:a",
                "copy",
                output_path,
            ]

        self._run_ffmpeg(args)
        return output_path

    def color_grade(
        self, input_path: str, output_path: str, preset: str = "cinematic"
    ) -> str:
        """
        Apply color grading presets

        Args:
            input_path: Source video path
            output_path: Output video path
            preset: Preset name (cinematic, warm, cool, vintage, B&W)

        Returns:
            Output path on success
        """
        presets = {
            "cinematic": "eq=contrast=1.1:brightness=-0.05:saturation=0.8:gamma=1.1",
            "warm": "eq=saturation=1.2:brightness=0.02:gamma=1.05",
            "cool": "eq=saturation=0.9:brightness=-0.02:gamma=0.95",
            "vintage": "colorchannelmixer=.9:.1:.1:.1:.9:.1:.1:.1:.8:eq=saturation=0.7:contrast=1.1",
            "B&W": "hue=s=0",
        }

        filter_expr = presets.get(preset.lower(), presets["cinematic"])

        args = ["-y", "-i", input_path, "-vf", filter_expr, "-c:a", "copy", output_path]
        self._run_ffmpeg(args)
        return output_path

    def add_vignette(
        self, input_path: str, output_path: str, intensity: float = 0.5
    ) -> str:
        """
        Add cinematic vignette effect

        Args:
            input_path: Source video path
            output_path: Output video path
            intensity: Vignette intensity (0.0 to 1.0)

        Returns:
            Output path on success
        """
        args = [
            "-y",
            "-i",
            input_path,
            "-vf",
            f"vignette=angle={intensity}",
            "-c:a",
            "copy",
            output_path,
        ]
        self._run_ffmpeg(args)
        return output_path

    # ============ TRANSITIONS ============

    def add_transition(
        self,
        clip1_path: str,
        clip2_path: str,
        output_path: str,
        transition: Transition = Transition.FADE,
        duration: float = 1.0,
    ) -> str:
        """
        Add transition between two video clips

        Args:
            clip1_path: First video clip
            clip2_path: Second video clip
            output_path: Output video path
            transition: Transition type
            duration: Transition duration in seconds

        Returns:
            Output path on success
        """
        # Get clip durations
        dur1 = self._get_video_duration(clip1_path)
        dur2 = self._get_video_duration(clip2_path)

        # Create transition filter
        if transition in (Transition.FADE, Transition.DISSOLVE):
            # Crossfade transition using fade
            filter_complex = (
                f"[0:v]trim=0:duration={dur1 - duration},setpts=PTS-STARTPTS[first];"
                f"[1:v]trim={duration}:duration={dur2},setpts=PTS-STARTPTS+({dur1 - duration})/TB[second];"
                f"[first][second]xfade=transition={transition.value}:duration={duration}:offset={dur1 - duration}[outv]"
            )
        elif transition == Transition.SLIDE_LEFT:
            filter_complex = (
                f"[0:v]trim=0:duration={dur1},setpts=PTS-STARTPTS[first];"
                f"[1:v]trim=0:duration={dur2},setpts=PTS-STARTPTS+{dur1}/TB,"
                f"crop=iw:ih:(oh-ih)/2:0,scale=iw:{self._get_video_info(clip1_path)['height']}[second];"
                f"[first][second]xfade=transition=slideleft:duration={duration}:offset={dur1 - duration}[outv]"
            )
        elif transition == Transition.SLIDE_RIGHT:
            filter_complex = (
                f"[0:v]trim=0:duration={dur1},setpts=PTS-STARTPTS[first];"
                f"[1:v]trim=0:duration={dur2},setpts=PTS-STARTPTS+{dur1}/TB[second];"
                f"[first][second]xfade=transition.slideright:duration={duration}:offset={dur1 - duration}[outv]"
            )
        elif transition == Transition.ZOOM_IN:
            filter_complex = (
                f"[0:v]trim=0:duration={dur1 - duration},setpts=PTS-STARTPTS[first];"
                f"[1:v]trim={duration}:duration={dur2},setpts=PTS-STARTPTS+({dur1 - duration})/TB,"
                f"scale=iw*1.5:ih*1.5[second];"
                f"[first][second]xfade=transition=zoomin:duration={duration}:offset={dur1 - duration}[outv]"
            )
        else:
            # Default fade
            filter_complex = (
                f"[0:v]trim=0:duration={dur1 - duration},setpts=PTS-STARTPTS[first];"
                f"[1:v]trim={duration}:duration={dur2},setpts=PTS-STARTPTS+({dur1 - duration})/TB[second];"
                f"[first][second]xfade=transition=fade:duration={duration}:offset={dur1 - duration}[outv]"
            )

        # For audio, just concatenate
        filter_complex += f";[0:a]atrim=0:duration={dur1}[a1];[1:a]atrim={duration}:duration={dur2}[a2];[a1][a2]acrossfade=d={duration}[outa]"

        args = [
            "-y",
            "-i",
            clip1_path,
            "-i",
            clip2_path,
            "-filter_complex",
            filter_complex,
            "-map",
            "[outv]",
            "-map",
            "[outa]",
            output_path,
        ]
        self._run_ffmpeg(args)
        return output_path

    def create_transition_sequence(
        self,
        clips: list[str],
        output_path: str,
        transition: Transition = Transition.FADE,
        transition_duration: float = 0.5,
    ) -> str:
        """
        Create video from multiple clips with transitions

        Args:
            clips: List of video clip paths
            output_path: Output video path
            transition: Transition type between clips
            transition_duration: Duration of each transition

        Returns:
            Output path on success
        """
        if not clips:
            raise ValueError("No clips provided")

        if len(clips) == 1:
            # Single clip, just copy
            args = ["-y", "-i", clips[0], "-c", "copy", output_path]
            self._run_ffmpeg(args)
            return output_path

        # Create concat file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            concat_file = f.name
            for clip in clips:
                f.write(f"file '{clip}'\n")

        try:
            # Use concat demuxer for simple concatenation first
            args = [
                "-y",
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
            self._run_ffmpeg(args)
        finally:
            os.unlink(concat_file)

        # If transition is needed, apply xfade
        # Full xfade would need complex filter graph

        return output_path

    # ============ AUDIO ============

    def add_music(
        self,
        input_path: str,
        music_path: str,
        output_path: str,
        volume: float = 0.3,
        fade_in: float = 2.0,
        fade_out: float = 2.0,
    ) -> str:
        """
        Add background music with fade in/out

        Args:
            input_path: Source video path
            music_path: Path to music/audio file
            output_path: Output video path
            volume: Music volume (0.0 to 1.0)
            fade_in: Fade in duration in seconds
            fade_out: Fade out duration in seconds

        Returns:
            Output path on success
        """
        video_duration = self._get_video_duration(input_path)

        # Build audio filter
        afilter = f"volume={volume}"

        if fade_in > 0:
            afilter = f"afade=t=in:st=0:d={fade_in}," + afilter

        if fade_out > 0:
            fade_out_start = max(0, video_duration - fade_out)
            afilter += f",afade=t=out:st={fade_out_start}:d={fade_out}"

        # Use filter_complex to mix original audio with new music
        args = [
            "-y",
            "-i",
            input_path,
            "-i",
            music_path,
            "-filter_complex",
            f"[1:a]{afilter}[music];[0:a][music]amix=inputs=2:duration=first:dropout_transition=0",
            "-map",
            "0:v",
            "-map",
            "[out]",
            "-shortest",
            output_path,
        ]
        self._run_ffmpeg(args)
        return output_path

    def add_sound_effect(
        self,
        input_path: str,
        sfx_path: str,
        output_path: str,
        timestamp: float,
        volume: float = 1.0,
    ) -> str:
        """
        Add sound effect at specific timestamp

        Args:
            input_path: Source video path
            sfx_path: Path to sound effect file
            output_path: Output video path
            timestamp: Timestamp in seconds where SFX should start
            volume: SFX volume (0.0 to 1.0)

        Returns:
            Output path on success
        """
        # Use filter_complex to delay and mix SFX
        delay_ms = int(timestamp * 1000)

        args = [
            "-y",
            "-i",
            input_path,
            "-i",
            sfx_path,
            "-filter_complex",
            f"[1:a]adelay={delay_ms}|{delay_ms},volume={volume}[sfx];[0:a][sfx]amix=inputs=2:duration=first[out]",
            "-map",
            "0:v",
            "-map",
            "[out]",
            "-shortest",
            output_path,
        ]
        self._run_ffmpeg(args)
        return output_path

    def mute_audio(self, input_path: str, output_path: str) -> str:
        """
        Remove audio track from video

        Args:
            input_path: Source video path
            output_path: Output video path

        Returns:
            Output path on success
        """
        args = ["-y", "-i", input_path, "-an", "-vc", "copy", output_path]
        self._run_ffmpeg(args)
        return output_path

    def extract_audio(self, input_path: str, output_path: str) -> str:
        """
        Extract audio to separate file

        Args:
            input_path: Source video path
            output_path: Output audio path (use .mp3, .wav, .aac extension)

        Returns:
            Output path on success
        """
        # Determine codec from extension
        ext = os.path.splitext(output_path)[1].lower()
        codec = "copy"
        if ext == ".mp3":
            codec = "libmp3lame"
        elif ext == ".wav":
            codec = "pcm_s16le"
        elif ext == ".aac":
            codec = "aac"

        args = ["-y", "-i", input_path, "-vn", "-acodec", codec, output_path]
        self._run_ffmpeg(args)
        return output_path

    # ============ COMPOSITION ============

    def resize(self, input_path: str, output_path: str, width: int, height: int) -> str:
        """
        Resize video to specific resolution

        Args:
            input_path: Source video path
            output_path: Output video path
            width: Target width
            height: Target height

        Returns:
            Output path on success
        """
        args = [
            "-y",
            "-i",
            input_path,
            "-vf",
            f"scale={width}:{height}",
            "-c:a",
            "copy",
            output_path,
        ]
        self._run_ffmpeg(args)
        return output_path

    def crop(
        self, input_path: str, output_path: str, x: int, y: int, width: int, height: int
    ) -> str:
        """
        Crop video to specific region

        Args:
            input_path: Source video path
            output_path: Output video path
            x: X coordinate of top-left corner
            y: Y coordinate of top-left corner
            width: Crop width
            height: Crop height

        Returns:
            Output path on success
        """
        args = [
            "-y",
            "-i",
            input_path,
            "-vf",
            f"crop={width}:{height}:{x}:{y}",
            "-c:a",
            "copy",
            output_path,
        ]
        self._run_ffmpeg(args)
        return output_path

    def convert_aspect_ratio(
        self, input_path: str, output_path: str, target_ratio: str
    ) -> str:
        """
        Convert video between aspect ratios

        Args:
            input_path: Source video path
            output_path: Output video path
            target_ratio: Target ratio (9:16, 16:9, 1:1, 4:3)

        Returns:
            Output path on success
        """
        video_info = self._get_video_info(input_path)
        orig_width = video_info["width"]
        orig_height = video_info["height"]

        # Parse target ratio
        ratio_parts = target_ratio.split(":")
        if len(ratio_parts) != 2:
            raise ValueError("Invalid ratio format. Use W:H (e.g., 9:16)")

        target_w, target_h = int(ratio_parts[0]), int(ratio_parts[1])
        target_ratio_val = target_w / target_h
        orig_ratio_val = orig_width / orig_height

        if abs(target_ratio_val - orig_ratio_val) < 0.01:
            # Same ratio, just copy
            args = ["-y", "-i", input_path, "-c", "copy", output_path]
            self._run_ffmpeg(args)
            return output_path

        if target_ratio_val > orig_ratio_val:
            # Target is wider, add letterbox (black bars top/bottom)
            new_height = int(orig_width / target_ratio_val)
            scale_filter = f"scale={orig_width}:{new_height},pad={orig_width}:{orig_height}:0:{(orig_height - new_height) // 2}:black"
        else:
            # Target is taller, add pillarbox (black bars left/right)
            new_width = int(orig_height * target_ratio_val)
            scale_filter = f"scale={new_width}:{orig_height},pad={new_width}:{orig_height}:{(new_width - orig_width) // 2}:0:black"

        args = [
            "-y",
            "-i",
            input_path,
            "-vf",
            scale_filter,
            "-c:a",
            "copy",
            output_path,
        ]
        self._run_ffmpeg(args)
        return output_path

    def picture_in_picture(
        self,
        main_path: str,
        pip_path: str,
        output_path: str,
        position: str = "bottom_right",
        size: float = 0.25,
    ) -> str:
        """
        Create picture-in-picture effect

        Args:
            main_path: Main video path
            pip_path: Picture-in-picture video path
            output_path: Output video path
            position: Position (top_left, top_right, bottom_left, bottom_right, center)
            size: Size as fraction of main video (0.25 = 1/4 size)

        Returns:
            Output path on success
        """
        # Position coordinates
        pos_map = {
            "top_left": "10:10",
            "top_right": "W-w-10:10",
            "bottom_left": "10:H-h-10",
            "bottom_right": "W-w-10:H-h-10",
            "center": "(W-w)/2:(H-h)/2",
        }

        pos = pos_map.get(position, pos_map["bottom_right"])

        # Scale PiP video and overlay
        filter_complex = f"[1:v]scale=iw*{size}:ih*{size}[pip];[0:v][pip]overlay={pos}"

        args = [
            "-y",
            "-i",
            main_path,
            "-i",
            pip_path,
            "-filter_complex",
            filter_complex,
            "-c:a",
            "copy",
            output_path,
        ]
        self._run_ffmpeg(args)
        return output_path

    def split_screen(
        self, clips: list[str], output_path: str, layout: str = "horizontal"
    ) -> str:
        """
        Create split screen video from multiple clips

        Args:
            clips: List of video clip paths (2 or 4 clips)
            output_path: Output video path
            layout: Layout type (horizontal, vertical, grid)

        Returns:
            Output path on success
        """
        if len(clips) < 2:
            raise ValueError("Need at least 2 clips for split screen")

        num_clips = len(clips)

        # Get info from first clip
        video_info = self._get_video_info(clips[0])
        base_width = video_info["width"]
        base_height = video_info["height"]

        if layout == "horizontal":
            # Side by side

            # Build hstack
            filter_parts = []
            for i, clip in enumerate(clips):
                filter_parts.append(f"[{i}:v]scale={base_width}:{base_height}[v{i}]")

            stack_inputs = "".join([f"[v{i}]" for i in range(num_clips)])
            filter_parts.append(f"{stack_inputs}hstack=inputs={num_clips}[outv]")

        elif layout == "vertical":
            # Stacked vertically

            filter_parts = []
            for i, clip in enumerate(clips):
                filter_parts.append(f"[{i}:v]scale={base_width}:{base_height}[v{i}]")

            stack_inputs = "".join([f"[v{i}]" for i in range(num_clips)])
            filter_parts.append(f"{stack_inputs}vstack=inputs={num_clips}[outv]")

        else:  # grid
            if num_clips not in (2, 4):
                raise ValueError("Grid layout supports 2 or 4 clips")

            half_w = base_width // 2
            half_h = base_height // 2

            filter_parts = []
            for i, clip in enumerate(clips):
                filter_parts.append(f"[{i}:v]scale={half_w}:{half_h}[v{i}]")

            if num_clips == 2:
                filter_parts.append("[v0][v1]hstack=inputs=2[v01];[v01]split2[outv]")
            else:
                filter_parts.append(
                    "[v0][v1]hstack=inputs=2[v01];[v2][v3]hstack=inputs=2[v23];[v01][v23]vstack=inputs=2[outv]"
                )

        filter_complex = ";".join(filter_parts)

        # Build input args
        input_args = []
        for clip in clips:
            input_args.extend(["-i", clip])

        args = (
            ["-y"]
            + input_args
            + [
                "-filter_complex",
                filter_complex,
                "-map",
                "[outv]",
                "-c:a",
                "copy",
                output_path,
            ]
        )
        self._run_ffmpeg(args)
        return output_path

    # ============ FORMATS ============

    def convert_format(
        self, input_path: str, output_path: str, format: str = "mp4"
    ) -> str:
        """
        Convert video between formats

        Args:
            input_path: Source video path
            output_path: Output video path
            format: Target format (mp4, mov, avi, webm, mkv)

        Returns:
            Output path on success
        """
        # Map format to codec
        codec_map = {
            "mp4": "libx264",
            "mov": "prores",
            "avi": "mpeg4",
            "webm": "libvpx-vp9",
            "mkv": "libx264",
        }

        codec = codec_map.get(format.lower(), "libx264")

        args = ["-y", "-i", input_path, "-c:v", codec, "-c:a", "copy", output_path]
        self._run_ffmpeg(args)
        return output_path

    def compress(self, input_path: str, output_path: str, crf: int = 23) -> str:
        """
        Compress video file

        Args:
            input_path: Source video path
            output_path: Output video path
            crf: Constant Rate Factor (0-51, lower = better quality, default 23)

        Returns:
            Output path on success
        """
        args = [
            "-y",
            "-i",
            input_path,
            "-c:v",
            "libx264",
            "-crf",
            str(crf),
            "-preset",
            "medium",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            output_path,
        ]
        self._run_ffmpeg(args)
        return output_path

    def generate_thumbnail(
        self, input_path: str, output_path: str, timestamp: float = 0
    ) -> str:
        """
        Generate thumbnail at specific time

        Args:
            input_path: Source video path
            output_path: Output image path (use .jpg or .png)
            timestamp: Timestamp in seconds

        Returns:
            Output path on success
        """
        args = [
            "-y",
            "-ss",
            str(timestamp),
            "-i",
            input_path,
            "-vframes",
            "1",
            "-q:v",
            "2",
            output_path,
        ]
        self._run_ffmpeg(args)
        return output_path

    def generate_gif(
        self,
        input_path: str,
        output_path: str,
        start: float,
        duration: float,
        fps: int = 10,
        width: int = 480,
    ) -> str:
        """
        Create GIF from video segment

        Args:
            input_path: Source video path
            output_path: Output GIF path
            start: Start time in seconds
            duration: Duration in seconds
            fps: GIF frame rate (default 10)
            width: GIF width (height auto-scaled)

        Returns:
            Output path on success
        """
        args = [
            "-y",
            "-ss",
            str(start),
            "-t",
            str(duration),
            "-i",
            input_path,
            "-vf",
            f"fps={fps},scale={width}:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
            "-loop",
            "0",
            output_path,
        ]
        self._run_ffmpeg(args)
        return output_path

    # ============ UTILITY METHODS ============

    def concatenate(
        self, clips: list[str], output_path: str, method: str = "concat"
    ) -> str:
        """
        Concatenate multiple video clips

        Args:
            clips: List of video clip paths
            output_path: Output video path
            method: Concatenation method (concat, ffmpeg)

        Returns:
            Output path on success
        """
        if len(clips) == 1:
            args = ["-y", "-i", clips[0], "-c", "copy", output_path]
            self._run_ffmpeg(args)
            return output_path

        # Create concat file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            concat_file = f.name
            for clip in clips:
                f.write(f"file '{os.path.abspath(clip)}'\n")

        try:
            args = [
                "-y",
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
            self._run_ffmpeg(args)
        finally:
            os.unlink(concat_file)

        return output_path

    def reverse(self, input_path: str, output_path: str) -> str:
        """
        Reverse video (play backwards)

        Args:
            input_path: Source video path
            output_path: Output video path

        Returns:
            Output path on success
        """
        args = [
            "-y",
            "-i",
            input_path,
            "-vf",
            "reverse",
            "-af",
            "areverse",
            output_path,
        ]
        self._run_ffmpeg(args)
        return output_path

    def loop(self, input_path: str, output_path: str, count: int = 2) -> str:
        """
        Loop video multiple times

        Args:
            input_path: Source video path
            output_path: Output video path
            count: Number of times to loop

        Returns:
            Output path on success
        """
        # Use concat to repeat
        clips = [input_path] * count
        return self.concatenate(clips, output_path)
