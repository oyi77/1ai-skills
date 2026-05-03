#!/usr/bin/env python3
"""
Auto Clipper Indonesia - OpenClaw Skill Wrapper (v2.0)
AI-powered video clipper for content creators

Features:
- AI-powered golden moment detection
- ViMax-inspired multi-agent framework
- Consistency Engine (v2.0): Maintain visual consistency across clips
- Storyboard Generator (v2.0): Auto-generate cinematic shot lists
- Quick storyboard generation for viral content

Basic Usage:
    from auto_clipper import AutoClipperSkill
    skill = AutoClipperSkill()
    results = skill.process_video("video.mp4")

v2.0 Features Usage:
    # Consistency Engine - Track visual consistency across clips
    from auto_clipper import ConsistencyEngine
    engine = ConsistencyEngine()
    engine.set_reference("reference_video.mp4")
    report = engine.check_consistency("clip_001.mp4")

    # Storyboard Generator - Create cinematic shot plans
    from auto_clipper import StoryboardGenerator
    generator = StoryboardGenerator()
    storyboard = generator.generate_short_form("hook_open", 30)

    # Quick Storyboard - One-line generation
    from auto_clipper import generate_quick_storyboard
    storyboard = generate_quick_storyboard("product_showcase", 15, "my_storyboard.json")
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Callable
from datetime import datetime

# Add core modules path
CORE_DIR = Path(__file__).parent / "core"
if CORE_DIR.exists():
    sys.path.insert(0, str(CORE_DIR))


class AutoClipperSkill:
    """
    Auto Clipper Indonesia - AI Video Clipper Skill

    Convert long videos into viral Shorts/TikToks/Reels
    with AI-powered golden moment detection.
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize Auto Clipper Skill

        Args:
            config: Optional configuration dictionary
        """
        # Load config from file or use provided
        config_path = Path(__file__).parent / "config.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                self.default_config = json.load(f).get('configuration', {})
        else:
            self.default_config = {
                'clip_duration': 30,
                'output_resolution': '720p',
                'whisper_model': 'base',
                'num_clips': 10,
                'add_subtitles': False,
                'output_format': 'mp4'
            }

        # Merge with provided config
        self.config = {**self.default_config, **(config or {})}

        # Initialize core components
        self._init_core()

        print(f"[AUTO-CLIPPER] Skill initialized")
        print(f"[AUTO-CLIPPER] Config: {self.config}")

    def _init_core(self):
        """Initialize core processing modules"""
        try:
            from video_analyzer import VideoAnalyzer
            from clip_engine import ClipEngine
            from reframe_engine import ReframeEngine
            from subtitle_engine import SubtitleEngine, SubtitleStyles

            self.analyzer = None
            self.clip_engine = ClipEngine()
            self.reframe_engine = ReframeEngine()
            self.subtitle_engine = SubtitleEngine()

            self.core_available = True
            print("[AUTO-CLIPPER] All core modules loaded successfully")

        except ImportError as e:
            self.core_available = False
            print(f"[AUTO-CLIPPER] WARNING: Core modules not available: {e}")
            print("[AUTO-CLIPPER] Run: pip install faster-whisper textblob vaderSentiment moviepy opencv-python")

    def analyze_video(
        self,
        video_path: str,
        num_clips: int = None,
        model_size: str = None,
        progress_callback: Callable[[float, str], None] = None
    ) -> List[Dict]:
        """
        Analyze video and detect golden moments

        Args:
            video_path: Path to video file
            num_clips: Number of moments to detect
            model_size: Whisper model size
            progress_callback: Progress callback function

        Returns:
            List of detected golden moments with scores
        """
        if not self.core_available:
            raise RuntimeError("Core modules not available. Install dependencies first.")

        if progress_callback:
            progress_callback(0.0, "Loading AI models...")

        # Initialize analyzer
        from video_analyzer import VideoAnalyzer

        model = model_size or self.config.get('whisper_model', 'base')
        num = num_clips or self.config.get('num_clips', 10)

        self.analyzer = VideoAnalyzer(model_size=model, device="cpu")

        if progress_callback:
            progress_callback(0.1, "Transcribing video...")

        try:
            self.analyzer.load_model()
        except Exception as e:
            raise RuntimeError(f"Failed to load AI model: {e}")

        # Run analysis
        if progress_callback:
            progress_callback(0.2, "Analyzing content...")

        moments = self.analyzer.find_golden_moments(
            video_path,
            progress_callback=lambda p: progress_callback(0.2 + p * 0.6, "Detecting golden moments...")
        )

        if progress_callback:
            progress_callback(0.95, f"Found {len(moments)} golden moments!")

        # Limit to requested number
        moments = moments[:num]

        if progress_callback:
            progress_callback(1.0, "Analysis complete!")

        print(f"[AUTO-CLIPPER] Analysis complete: {len(moments)} moments detected")
        return moments

    def process_video(
        self,
        video_path: str,
        num_clips: int = None,
        clip_duration: int = None,
        output_resolution: str = None,
        add_subtitles: bool = None,
        progress_callback: Callable[[float, str], None] = None
    ) -> Dict:
        """
        Full workflow: Analyze video → Detect moments → Process clips → Export

        Args:
            video_path: Path to video file
            num_clips: Number of clips to create
            clip_duration: Duration of each clip in seconds
            output_resolution: Output resolution (480p, 720p, 1080p)
            add_subtitles: Whether to add subtitles
            progress_callback: Progress callback function

        Returns:
            Complete workflow results with summary
        """
        if not self.core_available:
            raise RuntimeError("Core modules not available")

        num_clips = num_clips or self.config.get('num_clips', 10)
        clip_duration = clip_duration or self.config.get('clip_duration', 30)
        output_resolution = output_resolution or self.config.get('output_resolution', '720p')
        add_subtitles = add_subtitles if add_subtitles is not None else self.config.get('add_subtitles', False)

        import tempfile
        from core.workflow import WorkflowConfig, AutoClipperWorkflow

        # Setup config
        workflow_config = WorkflowConfig(
            whisper_model=self.config.get('whisper_model', 'base'),
            golden_moments_count=num_clips,
            clip_duration=clip_duration,
            output_resolution=output_resolution,
            add_subtitles=add_subtitles
        )

        # Create workflow
        workflow = AutoClipperWorkflow(workflow_config)

        if progress_callback:
            progress_callback(0.0, "Starting full workflow...")

        # Run full workflow
        summary = workflow.run_full_workflow(
            video_path,
            progress_callback=lambda p, msg: progress_callback(p, msg) if progress_callback else None
        )

        print(f"[AUTO-CLIPPER] Workflow complete: {summary['successful']}/{summary['clips_processed']} clips")

        return summary

    def process_clips(
        self,
        video_path: str,
        clips: List[Dict],
        output_resolution: str = None,
        add_subtitles: bool = False,
        progress_callback: Callable[[float, str], None] = None
    ) -> List[Dict]:
        """
        Process specific clips from video

        Args:
            video_path: Path to video file
            clips: List of clip dictionaries with 'start', 'end', 'text'
            output_resolution: Output resolution
            add_subtitles: Whether to add subtitles
            progress_callback: Progress callback

        Returns:
            List of processed clip results
        """
        if not self.core_available:
            raise RuntimeError("Core modules not available")

        import uuid
        from core.clip_engine import ClipEngine, ClipSegment
        from pathlib import Path

        output_resolution = output_resolution or self.config.get('output_resolution', '720p')
        results = []

        for i, clip in enumerate(clips):
            if progress_callback:
                progress_callback(i / len(clips), f"Processing clip {i+1}/{len(clips)}")

            try:
                # Create clip segment
                segment = ClipSegment(
                    clip_id=clip.get('clip_id', f"clip_{i+1:03d}"),
                    start_time=clip['start'],
                    end_time=clip['end'],
                    source_path=video_path
                )

                # Extract and process
                from core.workflow import TEMP_DIR, OUTPUT_DIR

                # Extract
                clip_output = self.clip_engine.extract_clip(
                    video_path,
                    clip['start'],
                    min(clip['end'], clip['start'] + self.config.get('clip_duration', 30))
                )

                # Reframe
                reframe_output = str(TEMP_DIR / f"temp_{segment.clip_id}.mp4")
                self.reframe_engine.smart_reframe(clip_output, reframe_output)

                # Clean up
                Path(clip_output).unlink(missing_ok=True)

                # Add subtitle if requested
                if add_subtitles and clip.get('text'):
                    final_output = str(OUTPUT_DIR / f"{segment.clip_id}_final.mp4")
                    self.subtitle_engine.add_simple_subtitles(
                        reframe_output,
                        clip['text'][:100],
                        0,
                        segment.duration,
                        final_output
                    )
                    Path(reframe_output).unlink(missing_ok=True)
                else:
                    final_output = str(OUTPUT_DIR / f"{segment.clip_id}.mp4")
                    Path(reframe_output).rename(final_output)

                # Get file info
                file_size = Path(final_output).stat().st_size / (1024 * 1024)

                results.append({
                    'clip_id': segment.clip_id,
                    'status': 'success',
                    'output_path': final_output,
                    'duration': segment.duration,
                    'size_mb': round(file_size, 2)
                })

            except Exception as e:
                results.append({
                    'clip_id': clip.get('clip_id', f"clip_{i+1}"),
                    'status': 'failed',
                    'error': str(e)
                })

        if progress_callback:
            progress_callback(1.0, f"Processed {len(results)} clips")

        return results

    def get_video_info(self, video_path: str) -> Dict:
        """
        Get video information

        Args:
            video_path: Path to video file

        Returns:
            Video metadata dictionary
        """
        if not self.core_available:
            raise RuntimeError("Core modules not available")

        return self.clip_engine.get_video_info(video_path)

    def export_subtitles(
        self,
        video_path: str,
        output_path: str = None,
        format: str = "srt"
    ) -> str:
        """
        Export video transcript as subtitle file

        Args:
            video_path: Path to video file
            output_path: Output file path
            format: Export format (srt, vtt)

        Returns:
            Path to exported subtitle file
        """
        if not self.core_available:
            raise RuntimeError("Core modules not available")

        if not self.analyzer:
            self.analyze_video(video_path)

        if format.lower() == "vtt":
            return self.analyzer.export_moments(output_path)
        else:
            # Generate SRT
            transcript = self.analyzer.transcribe(video_path)
            return self.analyzer.generate_srt(transcript, output_path)


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Auto Clipper Indonesia - AI Video Clipper (v2.0)"
    )
    parser.add_argument("--video", "-v", required=True, help="Path to video file")
    parser.add_argument("--clips", "-c", type=int, default=10, help="Number of clips")
    parser.add_argument("--duration", "-d", type=int, default=30, help="Clip duration in seconds")
    parser.add_argument("--resolution", "-r", default="720p", help="Output resolution")
    parser.add_argument("--subtitles", "-s", action="store_true", help="Add subtitles")
    parser.add_argument("--analyze", "-a", action="store_true", help="Analyze only")
    parser.add_argument("--output", "-o", help="Output directory")

    args = parser.parse_args()

    # Initialize skill
    skill = AutoClipperSkill()

    def progress(p, msg):
        print(f"[{int(p*100):3d}%] {msg}")

    # Run
    if args.analyze:
        moments = skill.analyze_video(args.video, args.clips, progress_callback=progress)
        print(f"\n✅ Found {len(moments)} golden moments:")
        for i, m in enumerate(moments[:10]):
            print(f"  {i+1}. [{m['start']:.0f}s-{m['end']:.0f}s] {m['text'][:50]}...")
    else:
        results = skill.process_video(
            args.video,
            num_clips=args.clips,
            clip_duration=args.duration,
            output_resolution=args.resolution,
            add_subtitles=args.subtitles,
            progress_callback=progress
        )
        print(f"\n✅ Complete! {results['successful']}/{results['clips_processed']} clips created")


# ============================================================================
# v2.0 ViMax Features Export
# ============================================================================

def _import_vimax_classes():
    """Lazy import v2.0 classes with fallback"""
    try:
        from core.consistency_engine import ConsistencyEngine as CE
        from core.storyboard_generator import (
            StoryboardGenerator as SG,
            generate_quick_storyboard as GQS
        )
        return CE, SG, GQS
    except ImportError as e:
        print(f"[WARNING] v2.0 ViMax features not available: {e}")
        print("[WARNING] Ensure core modules are in place: consistency_engine.py, storyboard_generator.py")
        return None, None, None


# Import v2.0 classes
ConsistencyEngine, StoryboardGenerator, _generate_quick_storyboard = _import_vimax_classes()


def generate_quick_storyboard(
    content_type: str = "hook_open",
    duration: float = 30,
    output_path: str = None
):
    """
    Quick storyboard generation (v2.0 ViMax feature)

    Generate a cinematic storyboard for viral content in one line.

    Args:
        content_type: Content type for shot planning
                      Options: 'hook_open', 'insight_explanation', 'emotional_peak',
                               'product_showcase', 'before_after'
        duration: Target duration in seconds (recommended: 15-60 for TikTok)
        output_path: Optional JSON output path for storyboard export

    Returns:
        Storyboard object with shot plans

    Examples:
        # Generate 30-second hook storyboard
        storyboard = generate_quick_storyboard("hook_open", 30)

        # Generate 15-second product showcase
        storyboard = generate_quick_storyboard("product_showcase", 15, "product_sb.json")

        # Generate insight explanation
        storyboard = generate_quick_storyboard("insight_explanation", 60)
        print(f"Generated {len(storyboard.clips)} shots")
        for shot in storyboard.clips:
            print(f"  - {shot.shot_id}: {shot.shot_type.value} ({shot.duration_seconds}s)")

    Supported Content Types:
        - hook_open: Attention-grabbing opener (ECU → POV → Medium)
        - insight_explanation: Educational delivery (Medium → Wide → CU)
        - emotional_peak: Emotion-focused (CU → Wide → CU)
        - product_showcase: Product commercial (Track → ECU → POV)
        - before_after: Transformation reveal (Wide → CU → Medium)
    """
    if _generate_quick_storyboard is None:
        raise ImportError(
            "v2.0 ViMax features not available. "
            "Ensure consistency_engine.py and storyboard_generator.py exist in core/ directory"
        )

    return _generate_quick_storyboard(content_type, duration, output_path)


__all__ = [
    # Main skill class
    'AutoClipperSkill',

    # v2.0 ViMax features
    'ConsistencyEngine',
    'StoryboardGenerator',
    'generate_quick_storyboard',
]


# Version info
__version__ = '2.0.0'
__vimax_version__ = '2.0'


if __name__ == "__main__":
    # Check if v2.0 features are available
    if ConsistencyEngine and StoryboardGenerator and generate_quick_storyboard:
        print("✅ v2.0 ViMax features loaded:")
        print("   - ConsistencyEngine")
        print("   - StoryboardGenerator")
        print("   - generate_quick_storyboard()")
    else:
        print("⚠️ v2.0 ViMax features not available")
        main()