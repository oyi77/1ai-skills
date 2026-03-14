"""
Auto Clipper Indonesia - Reframe Engine
9:16 vertical video reframe with object/face tracking
"""

import os
import subprocess
import logging
from pathlib import Path
from typing import Tuple, Optional, List, Dict

# Settings
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils.config import (
    ASPECT_RATIO_WIDTH, ASPECT_RATIO_HEIGHT, OUTPUT_DIR
)
from utils.logger import get_logger

logger = get_logger(__name__)

# Track if OpenCV is available
try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    print("[WARNING] opencv-python not installed. Run: pip install opencv-python")


class ReframeEngine:
    """
    9:16 Video Reframe Engine
    Auto-crop videos to vertical format with object/face tracking
    """

    def __init__(self):
        """Initialize the reframe engine"""
        self.ffmpeg_available = self._check_ffmpeg()
        self.opencv_available = OPENCV_AVAILABLE
        self.tracker = None

        logger.info(f"ReframeEngine initialized (FFmpeg: {'✅' if self.ffmpeg_available else '❌'}, "
                   f"OpenCV: {'✅' if self.opencv_available else '❌'})")

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

    def get_output_resolution(self, target_width: int = ASPECT_RATIO_WIDTH) -> Tuple[int, int]:
        """Get output resolution dimensions based on target width"""
        # 9:16 aspect ratio
        target_height = int(target_width * (16 / 9))
        return target_width, target_height

    def simple_center_crop(self, video_path: str, output_path: str = None) -> str:
        """
        Simple center crop to 9:16

        Args:
            video_path: Source video path
            output_path: Output video path

        Returns:
            Path to output video
        """
        if not self.ffmpeg_available:
            raise RuntimeError("FFmpeg not available")

        if output_path is None:
            output_path = str(OUTPUT_DIR / f"{Path(video_path).stem}_center.mp4")

        width, height = self.get_output_resolution(1080)

        cmd = [
            'ffmpeg', '-y',
            '-i', str(video_path),
            '-vf', f'crop=iw:{height}:(iw-{width})/2:0,scale={width}:{height}',
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-c:a', 'copy',
            str(output_path)
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Center crop saved: {output_path}")
            return output_path
        except subprocess.CalledProcessError as e:
            logger.error(f"Center crop failed: {e}")
            raise

    def smart_reframe(
        self,
        video_path: str,
        subject_position: Tuple[int, int] = None,
        output_path: str = None,
        tracking_enabled: bool = False
    ) -> str:
        """
        Smart reframe to 9:16 with optional subject tracking

        Args:
            video_path: Source video path
            subject_position: Initial subject position (x, y) - center if None
            output_path: Output video path
            tracking_enabled: Enable face/object tracking

        Returns:
            Path to output video
        """
        if not self.ffmpeg_available:
            raise RuntimeError("FFmpeg not available")

        if output_path is None:
            output_path = str(OUTPUT_DIR / f"{Path(video_path).stem}_smart.mp4")

        output_width, output_height = self.get_output_resolution(1080)

        if tracking_enabled and self.opencv_available:
            # Use smart tracking
            return self._smart_reframe_with_tracking(
                video_path, output_path, output_width, output_height
            )

        # Use center crop with slight offset optimization
        return self._optimized_center_crop(
            video_path, output_path, output_width, output_height
        )

    def _optimized_center_crop(
        self,
        video_path: str,
        output_path: str,
        output_width: int,
        output_height: int
    ) -> str:
        """Optimized center crop that maintains most action"""

        # Calculate crop dimensions
        # Scale to height first (9:16 requires height as base)
        cmd = [
            'ffmpeg', '-y',
            '-i', str(video_path),
            '-vf', (
                f"scale={output_width}:{output_height}:force_original_aspect_ratio=decrease,"
                f"pad={output_width}:{output_height}:(ow-iw)/2:(oh-ih)/2"
            ),
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-movflags', '+faststart',
            str(output_path)
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Smart reframe saved: {output_path}")
            return output_path
        except subprocess.CalledProcessError as e:
            logger.error(f"Smart reframe failed: {e}")
            raise

    def _smart_reframe_with_tracking(
        self,
        video_path: str,
        output_path: str,
        output_width: int,
        output_height: int
    ) -> str:
        """
        Smart reframe with face/object tracking using OpenCV

        This is a simplified version - full implementation would
        analyze the entire video first to determine crop positions
        """

        if not self.opencv_available:
            logger.warning("OpenCV not available, using center crop")
            return self._optimized_center_crop(video_path, output_path, output_width, output_height)

        # Try to detect face/important regions
        cap = cv2.VideoCapture(video_path)

        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Sample frames to find best crop position
        sample_frames = []
        sample_indices = [0, frame_count // 4, frame_count // 2, 3 * frame_count // 4, frame_count - 1]

        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

        best_y_offset = 0  # Default center

        for idx in sample_indices:
            if idx >= frame_count:
                continue

            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read(cap)

            if ret and face_cascade is not None:
                try:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(
                        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
                    )

                    if len(faces) > 0:
                        # Use average face position
                        avg_y = sum(f[1] + f[3] // 2 for f in faces) // len(faces)
                        best_y_offset = avg_y - output_height // 2

                        # Clamp to valid range
                        best_y_offset = max(0, min(best_y_offset, original_height - output_height))
                        break
                except Exception:
                    pass

        cap.release()

        # Build FFmpeg command with best crop position
        cmd = [
            'ffmpeg', '-y',
            '-i', str(video_path),
            '-vf', (
                f"crop={output_width}:{output_height}:(iw-{output_width})/2:"
                f"{best_y_offset},scale={output_width}:{output_height}"
            ),
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-movflags', '+faststart',
            str(output_path)
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Tracking reframe saved: {output_path}")
            return output_path
        except subprocess.CalledProcessError as e:
            logger.error(f"Tracking reframe failed: {e}")
            # Fallback to center crop
            return self._optimized_center_crop(video_path, output_path, output_width, output_height)

    def add_subtitles(
        self,
        video_path: str,
        subtitle_text: str,
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
        Add subtitle to video

        Args:
            video_path: Source video path
            subtitle_text: Text to display
            start_time: Start time in seconds
            end_time: End time in seconds
            output_path: Output video path
            font_size: Font size
            font_color: Font color
            stroke_color: Outline color
            stroke_width: Outline width
            position: Text position (bottom, top, center)

        Returns:
            Path to output video
        """
        if not self.ffmpeg_available:
            raise RuntimeError("FFmpeg not available")

        if output_path is None:
            output_path = str(OUTPUT_DIR / f"{Path(video_path).stem}_subtitled.mp4")

        # Escape special characters for FFmpeg
        subtitle_escaped = subtitle_text.replace("'", "\\'").replace(":", "\\:").replace("\n", " ")

        # Get video dimensions
        width, height = self.get_output_resolution(1080)

        # Calculate position
        if position == "bottom":
            y_offset = height - font_size - 20
        elif position == "top":
            y_offset = 20
        else:
            y_offset = height // 2 - font_size // 2

        # Build subtitle filter
        subtitle_filter = (
            f"drawtext=text='{subtitle_escaped}':"
            f"fontcolor={font_color}:"
            f"fontsize={font_size}:"
            f"x=(w-text_w)/2:"
            f"y={y_offset}:"
            f"borderw={stroke_width}:"
            f"bordercolor={stroke_color}:"
            f"enable='between(t,{start_time},{end_time})'"
        )

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
            logger.info(f"Subtitle added: {output_path}")
            return output_path
        except subprocess.CalledProcessError as e:
            logger.error(f"Subtitle failed: {e}")
            raise

    def process_clip(
        self,
        video_path: str,
        start_time: float,
        end_time: float,
        output_path: str = None,
        subtitle: str = None,
        subtitle_position: str = "bottom"
    ) -> Dict:
        """
        Process a complete clip: extract + reframe + optional subtitle

        Args:
            video_path: Source video path
            start_time: Start time in seconds
            end_time: End time in seconds
            output_path: Output video path
            subtitle: Optional subtitle text
            subtitle_position: Subtitle position

        Returns:
            Processing result dictionary
        """
        if not self.ffmpeg_available:
            raise RuntimeError("FFmpeg not available")

        from core.clip_engine import ClipEngine, ClipSegment
        from pathlib import Path
        import uuid

        if output_path is None:
            output_path = str(OUTPUT_DIR / f"clip_{uuid.uuid4().hex[:8]}.mp4")

        try:
            # Step 1: Extract clip
            clip_engine = ClipEngine()
            clip_output = str(TEMP_DIR / f"temp_clip_{uuid.uuid4().hex[:8]}.mp4")

            extracted = clip_engine.extract_clip(
                video_path=video_path,
                start_time=start_time,
                end_time=end_time,
                output_path=clip_output
            )

            # Step 2: Reframe to 9:16
            reframe_output = str(TEMP_DIR / f"temp_reframe_{uuid.uuid4().hex[:8]}.mp4")
            reframed = self.smart_reframe(extracted, reframe_output)

            # Step 3: Add subtitle if provided
            if subtitle:
                final_output = str(OUTPUT_DIR / Path(output_path).name)
                self.add_subtitles(
                    reframed,
                    subtitle,
                    0,  # Subtitle already in extracted clip timeline
                    end_time - start_time,
                    final_output,
                    position=subtitle_position
                )
                # Clean up temp_reframe
                Path(reframed).unlink(missing_ok=True)
            else:
                # Rename to final output
                final_output = output_path
                Path(reframed).rename(final_output)

            # Clean up temp_clip
            Path(extracted).unlink(missing_ok=True)

            # Get file size
            file_size = Path(final_output).stat().st_size / (1024 * 1024)

            result = {
                'status': 'success',
                'output_path': final_output,
                'start_time': start_time,
                'end_time': end_time,
                'duration': end_time - start_time,
                'size_mb': round(file_size, 2),
                'subtitle_added': subtitle is not None
            }

            logger.info(f"Clip processed: {final_output} ({file_size:.2f} MB)")
            return result

        except Exception as e:
            logger.error(f"Clip processing failed: {e}")
            return {
                'status': 'failed',
                'error': str(e),
                'output_path': None
            }


# Standalone test function
if __name__ == "__main__":
    print("=" * 60)
    print("AUTO CLIPPER INDONESIA - REFRAME ENGINE TEST")
    print("=" * 60)

    engine = ReframeEngine()

    if not engine.ffmpeg_available:
        print("\n[ERROR] FFmpeg not found!")
        exit(1)

    print(f"\nFFmpeg available: {'✅' if engine.ffmpeg_available else '❌'}")
    print(f"OpenCV available: {'✅' if engine.opencv_available else '❌'}")

    test_video = input("\nEnter video path (or press Enter to skip): ").strip()

    if test_video and os.path.exists(test_video):
        print(f"\nTesting with: {test_video}")

        # Test center crop
        print("\n📐 Testing center crop...")
        output = engine.simple_center_crop(
            test_video,
            str(OUTPUT_DIR / "test_center.mp4")
        )
        print(f"✅ Center crop: {output}")

        # Test smart reframe
        print("\n🧠 Testing smart reframe...")
        output = engine.smart_reframe(
            test_video,
            str(OUTPUT_DIR / "test_smart.mp4")
        )
        print(f"✅ Smart reframe: {output}")

        # Test subtitle
        print("📝 Testing subtitle...")
        output = engine.add_subtitles(
            test_video,
            "Test subtitle from Auto Clipper Indonesia!",
            5, 15,
            str(OUTPUT_DIR / "test_subtitle.mp4")
        )
        print(f"✅ Subtitle added: {output}")

    else:
        print("\n[INFO] No video provided. Engine ready for use.")
        print("Usage:")
        print("  engine = ReframeEngine()")
        print("  output = engine.simple_center_crop('video.mp4', 'output.mp4')")
        print("  output = engine.smart_reframe('video.mp4', 'output.mp4')")

    print("\n✅ ReframeEngine test complete")