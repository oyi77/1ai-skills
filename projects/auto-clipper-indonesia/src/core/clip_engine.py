"""
Auto Clipper Indonesia - Clip Engine
Video clipping and processing using FFmpeg
"""

import os
import subprocess
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

# Settings
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils.config import (
    DEFAULT_OUTPUT_FORMAT, DEFAULT_OUTPUT_RESOLUTION, DEFAULT_BITRATE,
    ASPECT_RATIO_WIDTH, ASPECT_RATIO_HEIGHT, OUTPUT_DIR, TEMP_DIR
)
from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class ClipSegment:
    """Represents a video clip to be extracted"""
    clip_id: str
    start_time: float  # seconds
    end_time: float    # seconds
    source_path: str
    output_path: str = ""

    @property
    def duration(self) -> float:
        return self.end_time - self.start_time


class ClipEngine:
    """
    Video clipping engine using FFmpeg
    """

    def __init__(self):
        """Initialize the clip engine"""
        self.ffmpeg_available = self._check_ffmpeg()
        self.output_format = DEFAULT_OUTPUT_FORMAT
        self.output_resolution = DEFAULT_OUTPUT_RESOLUTION
        self.bitrate = DEFAULT_BITRATE

        logger.info(f"ClipEngine initialized (FFmpeg: {'✅' if self.ffmpeg_available else '❌'})")

    def _check_ffmpeg(self) -> bool:
        """Check if FFmpeg is available"""
        try:
            result = subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                version = result.stdout.split('\n')[0]
                logger.info(f"FFmpeg found: {version}")
                return True
        except (subprocess.SubprocessError, FileNotFoundError):
            pass

        logger.warning("FFmpeg not found - please install FFmpeg")
        return False

    def get_video_info(self, video_path: str) -> Dict:
        """
        Get video information

        Args:
            video_path: Path to video file

        Returns:
            Video metadata dictionary
        """
        if not self.ffmpeg_available:
            raise RuntimeError("FFmpeg not available")

        video_path = Path(video_path)
        if not video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")

        cmd = [
            'ffprobe', '-v', 'quiet', '-print_format', 'json',
            '-show_format', '-show_streams', str(video_path)
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

            if result.returncode != 0:
                raise RuntimeError(f"ffprobe failed: {result.stderr}")

            import json
            data = json.loads(result.stdout)

            # Extract video stream info
            video_stream = None
            audio_stream = None

            for stream in data.get('streams', []):
                if stream.get('codec_type') == 'video':
                    video_stream = stream
                elif stream.get('codec_type') == 'audio':
                    audio_stream = stream

            # Get duration
            duration = float(data.get('format', {}).get('duration', 0))
            if video_stream and 'duration' in video_stream:
                duration = float(video_stream['duration'])

            info = {
                'path': str(video_path),
                'filename': video_path.name,
                'format': data.get('format', {}).get('format_name', 'unknown'),
                'size_bytes': int(data.get('format', {}).get('size', 0)),
                'size_mb': round(int(data.get('format', {}).get('size', 0)) / (1024 * 1024), 2),
                'duration_seconds': duration,
                'duration_formatted': self._format_duration(duration),
                'width': int(video_stream.get('width', 0)) if video_stream else 0,
                'height': int(video_stream.get('height', 0)) if video_stream else 0,
                'fps': self._parse_fps(video_stream.get('r_frame_rate', '0/0')) if video_stream else 0,
                'codec': video_stream.get('codec_name', 'unknown') if video_stream else 'none',
                'has_audio': audio_stream is not None,
                'audio_codec': audio_stream.get('codec_name', 'none') if audio_stream else 'none',
                'bit_rate': int(data.get('format', {}).get('bit_rate', 0))
            }

            logger.info(f"Video info: {info['width']}x{info['height']}, {info['duration_formatted']}")
            return info

        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            raise

    def _format_duration(self, seconds: float) -> str:
        """Format duration in human-readable format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)

        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        return f"{minutes}:{secs:02d}"

    def _parse_fps(self, fps_str: str) -> float:
        """Parse FPS from fraction string"""
        try:
            num, den = fps_str.split('/')
            return round(int(num) / int(den), 2)
        except (ValueError, ZeroDivisionError):
            return 0.0

    def extract_clip(
        self,
        video_path: str,
        start_time: float,
        end_time: float,
        output_path: str = None,
        output_resolution: str = None,
        output_format: str = None,
        progress_callback=None
    ) -> str:
        """
        Extract a single clip from video

        Args:
            video_path: Source video path
            start_time: Start time in seconds
            end_time: End time in seconds
            output_path: Output file path (auto-generated if None)
            output_resolution: Output resolution (720p, 1080p)
            output_format: Output format (mp4, mov)
            progress_callback: Progress callback function

        Returns:
            Path to extracted clip
        """
        if not self.ffmpeg_available:
            raise RuntimeError("FFmpeg not available")

        video_path = Path(video_path)

        # Set defaults
        if output_format is None:
            output_format = self.output_format
        if output_resolution is None:
            output_resolution = self.output_resolution

        # Generate output path if not provided
        if output_path is None:
            output_path = OUTPUT_DIR / f"{video_path.stem}_clip_{int(start_time)}s.mp4"

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Calculate resolution
        width, height = self._get_output_resolution(output_resolution)

        duration = end_time - start_time

        logger.info(f"Extracting clip: {start_time:.1f}s - {end_time:.1f}s ({duration:.1f}s)")

        # Build FFmpeg command
        cmd = [
            'ffmpeg', '-y',  # Overwrite output
            '-ss', str(start_time),
            '-i', str(video_path),
            '-t', str(duration),
            '-vf', f'scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2',
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-b:v', self.bitrate,
            '-c:a', 'aac',
            '-b:a', '128k',
            '-movflags', '+faststart',
            str(output_path)
        ]

        try:
            # Run FFmpeg
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            # Parse progress
            duration_sec = duration
            while True:
                line = process.stderr.readline()
                if not line and process.poll() is not None:
                    break

                # Parse time
                if 'time=' in line:
                    try:
                        time_str = line.split('time=')[1].split()[0]
                        current_time = self._parse_timecode(time_str)
                        progress = min(current_time / duration_sec, 1.0)
                        if progress_callback:
                            progress_callback(progress)
                    except (ValueError, IndexError):
                        pass

            # Check result
            if process.returncode != 0:
                raise RuntimeError(f"FFmpeg failed with code {process.returncode}")

            logger.info(f"Clip saved: {output_path}")
            return str(output_path)

        except Exception as e:
            logger.error(f"Clip extraction failed: {e}")
            raise

    def _get_output_resolution(self, resolution: str) -> Tuple[int, int]:
        """Get output resolution dimensions"""
        if resolution == '1080p':
            return 1080, 1920
        elif resolution == '720p':
            return 720, 1280
        elif resolution == '480p':
            return 480, 854
        else:
            return 720, 1280  # Default to 720p

    def _parse_timecode(self, time_str: str) -> float:
        """Parse FFmpeg timecode string to seconds"""
        try:
            parts = time_str.split(':')
            return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
        except (ValueError, IndexError):
            return 0.0

    def extract_multiple_clips(
        self,
        video_path: str,
        clips: List[ClipSegment],
        output_resolution: str = None,
        output_format: str = None,
        progress_callback=None
    ) -> List[Dict]:
        """
        Extract multiple clips from video

        Args:
            video_path: Source video path
            clips: List of ClipSegment objects
            output_resolution: Output resolution
            output_format: Output format
            progress_callback: Progress callback

        Returns:
            List of extraction results
        """
        if not clips:
            logger.warning("No clips to extract")
            return []

        logger.info(f"Extracting {len(clips)} clips from {Path(video_path).name}")

        results = []

        for i, clip in enumerate(clips):
            # Calculate progress
            overall_progress = (i / len(clips))

            def clip_progress(p):
                if progress_callback:
                    progress_callback(overall_progress + p / len(clips))

            try:
                # Generate output path
                output_path = str(OUTPUT_DIR / f"{Path(video_path).stem}_{clip.clip_id}.{output_format or self.output_format}")

                # Extract clip
                extracted_path = self.extract_clip(
                    video_path=video_path,
                    start_time=clip.start_time,
                    end_time=clip.end_time,
                    output_path=output_path,
                    output_resolution=output_resolution,
                    progress_callback=clip_progress
                )

                # Get file size
                file_size = Path(extracted_path).stat().st_size / (1024 * 1024)

                results.append({
                    'clip_id': clip.clip_id,
                    'status': 'success',
                    'output_path': extracted_path,
                    'start_time': clip.start_time,
                    'end_time': clip.end_time,
                    'duration': clip.duration,
                    'size_mb': round(file_size, 2),
                    'error': None
                })

                logger.info(f"Clip {clip.clip_id}: ✅ ({file_size:.2f} MB)")

            except Exception as e:
                logger.error(f"Clip {clip.clip_id}: ❌ {e}")
                results.append({
                    'clip_id': clip.clip_id,
                    'status': 'failed',
                    'output_path': None,
                    'start_time': clip.start_time,
                    'end_time': clip.end_time,
                    'duration': clip.duration,
                    'size_mb': 0,
                    'error': str(e)
                })

        # Final progress
        if progress_callback:
            progress_callback(1.0)

        # Summary
        successful = sum(1 for r in results if r['status'] == 'success')
        failed = len(results) - successful

        logger.info(f"Extraction complete: {successful}/{len(results)} successful, {failed} failed")

        return results

    def extract_video_frame(
        self,
        video_path: str,
        timestamp: float,
        output_path: str = None
    ) -> str:
        """
        Extract a single frame from video

        Args:
            video_path: Path to video
            timestamp: Time in seconds
            output_path: Output image path

        Returns:
            Path to extracted frame
        """
        if not self.ffmpeg_available:
            raise RuntimeError("FFmpeg not available")

        if output_path is None:
            output_path = TEMP_DIR / f"frame_{int(timestamp)}.jpg"

        output_path = Path(output_path)

        cmd = [
            'ffmpeg', '-y',
            '-ss', str(timestamp),
            '-i', str(video_path),
            '-vframes', '1',
            '-q:v', '2',
            str(output_path)
        ]

        try:
            subprocess.run(cmd, capture_output=True, check=True, timeout=30)
            logger.info(f"Frame extracted: {output_path}")
            return str(output_path)
        except subprocess.CalledProcessError as e:
            logger.error(f"Frame extraction failed: {e}")
            raise


# Standalone test function
if __name__ == "__main__":
    print("=" * 60)
    print("AUTO CLIPPER INDONESIA - CLIP ENGINE TEST")
    print("=" * 60)

    engine = ClipEngine()

    if not engine.ffmpeg_available:
        print("\n[ERROR] FFmpeg not found!")
        print("Please install FFmpeg and add to PATH")
        print("Download: https://ffmpeg.org/download.html")
        exit(1)

    # Test with sample video
    test_video = input("\nEnter video path (or press Enter to skip): ").strip()

    if test_video and os.path.exists(test_video):
        print(f"\nTesting with: {test_video}")

        # Get video info
        print("\n📹 Video Info:")
        info = engine.get_video_info(test_video)
        for key, value in info.items():
            if key not in ['path']:
                print(f"  {key}: {value}")

        # Extract test clip
        print("\n📎 Extracting test clip (30s)...")
        clip_path = engine.extract_clip(
            test_video,
            start_time=0,
            end_time=30,
            output_path=str(OUTPUT_DIR / "test_clip.mp4"),
            progress_callback=lambda p: print(f"  Progress: {int(p * 100)}%", end="\r")
        )
        print(f"\n✅ Clip saved: {clip_path}")

        # Test frame extraction
        print("\n🖼️ Extracting test frame...")
        frame_path = engine.extract_video_frame(test_video, 10)
        print(f"✅ Frame saved: {frame_path}")

    else:
        print("\n[INFO] No video provided. Engine ready for use.")
        print("Usage:")
        print("  engine = ClipEngine()")
        print("  info = engine.get_video_info('video.mp4')")
        print("  clip = engine.extract_clip('video.mp4', 0, 30, 'output.mp4')")

    print("\n✅ ClipEngine test complete")