"""
Auto Clipper Indonesia - Main Workflow
End-to-end workflow orchestration (Analyze → Clip → Reframe → Export)
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass
from datetime import datetime

# Core modules
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.video_analyzer import VideoAnalyzer
from core.clip_engine import ClipEngine, ClipSegment
from core.reframe_engine import ReframeEngine
from core.subtitle_engine import SubtitleEngine, SubtitleStyle
from utils.config import OUTPUT_DIR, TEMP_DIR
from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class WorkflowConfig:
    """Workflow configuration"""
    # Analysis settings
    whisper_model: str = "base"
    whisper_device: str = "cpu"
    golden_moments_count: int = 10

    # Clip settings
    clip_duration: int = 30
    output_resolution: str = "720p"
    output_format: str = "mp4"

    # Subtitle settings
    add_subtitles: bool = False
    subtitle_style: SubtitleStyle = None

    # Distribution settings (future)
    export_only: bool = True  # If True, don't delete temp files


class AutoClipperWorkflow:
    """
    Main workflow orchestrator for Auto Clipper Indonesia

    Flow:
    1. Analyze video → transcribe + detect golden moments
    2. Generate clips → extract segments from video
    3. Reframe clips → convert to 9:16 vertical
    4. Add subtitles → burn-in subtitles (optional)
    5. Export clips → save to output directory
    """

    def __init__(self, config: WorkflowConfig = None):
        """Initialize workflow with optional configuration"""
        self.config = config or WorkflowConfig()
        self.video_analyzer = None
        self.clip_engine = ClipEngine()
        self.reframe_engine = ReframeEngine()
        self.subtitle_engine = SubtitleEngine()
        self.clips = []
        self.results = []

        logger.info("AutoClipperWorkflow initialized")

    def analyze(
        self,
        video_path: str,
        progress_callback: Callable[[float, str], None] = None
    ) -> List[Dict]:
        """
        Step 1: Analyze video and detect golden moments

        Args:
            video_path: Path to video file
            progress_callback: Callback function (progress, status_message)

        Returns:
            List of detected golden moments
        """
        logger.info(f"Starting analysis: {video_path}")

        if progress_callback:
            progress_callback(0.05, "Initializing analyzer...")

        # Initialize analyzer
        self.video_analyzer = VideoAnalyzer(
            model_size=self.config.whisper_model,
            device=self.config.whisper_device
        )

        if progress_callback:
            progress_callback(0.1, "Loading AI models...")

        try:
            self.video_analyzer.load_model()
        except ImportError as e:
            logger.error(f"Failed to load analyzer: {e}")
            raise RuntimeError(
                "AI dependencies not installed. Run:\n"
                "pip install faster-whisper textblob vaderSentiment"
            )

        if progress_callback:
            progress_callback(0.2, "Transcribing audio...")

        # Transcribe video
        transcript = self.video_analyzer.transcribe(
            video_path,
            progress_callback=lambda p: progress_callback(0.2 + p * 0.3, "Transcribing audio...")
        )

        if progress_callback:
            progress_callback(0.5, "Detecting golden moments...")

        # Detect golden moments
        golden_moments = self.video_analyzer.find_golden_moments(
            video_path,
            progress_callback=lambda p: progress_callback(0.5 + p * 0.4, "Analyzing content...")
        )

        if progress_callback:
            progress_callback(0.95, "Analysis complete!")

        # Store results
        self.clips = golden_moments

        # Export analysis report
        report_path = self.video_analyzer.export_moments()
        logger.info(f"Analysis report: {report_path}")

        if progress_callback:
            progress_callback(1.0, f"Found {len(golden_moments)} golden moments")

        return golden_moments

    def process_clips(
        self,
        video_path: str,
        clip_indices: List[int] = None,
        progress_callback: Callable[[float, str], None] = None
    ) -> List[Dict]:
        """
        Step 2-4: Process clips (extract + reframe + optional subtitle)

        Args:
            video_path: Source video path
            clip_indices: List of clip indices to process (None = all)
            progress_callback: Callback function

        Returns:
            List of processing results
        """
        if not self.clips:
            raise RuntimeError("No clips to process. Run analyze() first.")

        # Filter clips to process
        if clip_indices is None:
            clips_to_process = self.clips
        else:
            clips_to_process = [self.clips[i] for i in clip_indices if i < len(self.clips)]

        if progress_callback:
            progress_callback(0.0, f"Processing {len(clips_to_process)} clips...")

        results = []

        # Process each clip
        for i, clip in enumerate(clips_to_process):
            clip_progress = i / len(clips_to_process)

            if progress_callback:
                progress_callback(
                    clip_progress,
                    f"Processing clip {i+1}/{len(clips_to_process)}: {clip['clip_id']}"
                )

            try:
                # Extract clip segment
                start_time = clip['start']
                end_time = min(clip['end'], start_time + self.config.clip_duration)

                clip_segment = ClipSegment(
                    clip_id=clip['clip_id'],
                    start_time=start_time,
                    end_time=end_time,
                    source_path=video_path
                )

                if progress_callback:
                    progress_callback(
                        clip_progress + 0.1,
                        f"Extracting clip {i+1}..."
                    )

                # Extract clip
                clip_output = self.clip_engine.extract_clip(
                    video_path=video_path,
                    start_time=start_time,
                    end_time=end_time
                )

                if progress_callback:
                    progress_callback(
                        clip_progress + 0.3,
                        f"Converting to 9:16 vertical..."
                    )

                # Reframe to 9:16
                reframe_output = str(TEMP_DIR / f"temp_{clip['clip_id']}_9x16.mp4")
                # Smart reframe (with tracking if OpenCV available)
                self.reframe_engine.smart_reframe(
                    clip_output,
                    reframe_output
                )

                # Clean up extracted clip
                Path(clip_output).unlink(missing_ok=True)

                # Add subtitle if configured
                final_output = str(OUTPUT_DIR / f"{clip['clip_id']}_final.mp4")

                if self.config.add_subtitles and self.config.subtitle_style:
                    if progress_callback:
                        progress_callback(
                            clip_progress + 0.6,
                            f"Adding subtitles..."
                        )

                    # Generate subtitle from clip text
                    subtitle_text = clip.get('text', '')[:100]

                    self.subtitle_engine.add_simple_subtitles(
                        reframe_output,
                        subtitle_text,
                        0,
                        end_time - start_time,
                        final_output,
                        font_size=self.config.subtitle_style.size,
                        font_color=self.config.subtitle_style.color,
                        stroke_color=self.config.subtitle_style.stroke_color,
                        stroke_width=self.config.subtitle_style.stroke_width,
                        position=self.config.subtitle_style.position
                    )

                    # Clean up reframe
                    Path(reframe_output).unlink(missing_ok=True)
                else:
                    # Just rename
                    Path(reframe_output).rename(final_output)

                # Calculate duration and size
                file_size = Path(final_output).stat().st_size / (1024 * 1024)

                result = {
                    'clip_id': clip['clip_id'],
                    'status': 'success',
                    'output_path': final_output,
                    'start_time': start_time,
                    'end_time': end_time,
                    'duration': end_time - start_time,
                    'size_mb': round(file_size, 2),
                    'original_text': clip.get('text', '')[:100]
                }

                results.append(result)
                logger.info(f"Clip {clip['clip_id']}: ✅ ({file_size:.2f} MB)")

            except Exception as e:
                logger.error(f"Clip {clip['clip_id']}: ❌ {e}")
                results.append({
                    'clip_id': clip['clip_id'],
                    'status': 'failed',
                    'error': str(e)
                })

        # Final progress
        if progress_callback:
            progress_callback(1.0, f"Processed {len(results)} clips")

        self.results = results

        # Summary
        successful = sum(1 for r in results if r['status'] == 'success')
        logger.info(f"Workflow complete: {successful}/{len(results)} clips successful")

        return results

    def run_full_workflow(
        self,
        video_path: str,
        progress_callback: Callable[[float, str], None] = None
    ):
        """
        Run complete workflow: Analyze → Process all clips

        Args:
            video_path: Path to source video
            progress_callback: Callback function

        Returns:
            Workflow results dictionary
        """
        logger.info(f"Starting full workflow: {video_path}")

        workflow_start = datetime.now()

        # Step 1: Analyze
        if progress_callback:
            progress_callback(0.0, "Analyzing video...")

        golden_moments = self.analyze(video_path, progress_callback)

        if progress_callback:
            progress_callback(0.3, "Processing clips...")

        # Step 2: Process all clips
        results = self.process_clips(video_path, progress_callback=progress_callback)

        # Calculate summary
        workflow_duration = (datetime.now() - workflow_start).total_seconds()

        summary = {
            'video_path': video_path,
            'video_name': Path(video_path).name,
            'moments_detected': len(golden_moments),
            'clips_processed': len(results),
            'successful': sum(1 for r in results if r['status'] == 'success'),
            'failed': sum(1 for r in results if r['status'] == 'failed'),
            'total_duration_seconds': workflow_duration,
            'results': results,
            'timestamp': datetime.now().isoformat()
        }

        logger.info(f"Full workflow complete in {workflow_duration:.1f}s")
        logger.info(f"Summary: {summary['successful']}/{summary['clips_processed']} successful")

        if progress_callback:
            progress_callback(1.0, f"Complete! {summary['successful']} clips ready")

        return summary

    def cleanup(self):
        """Clean up temporary files"""
        import shutil

        # Clean temp directory
        if TEMP_DIR.exists():
            for file in TEMP_DIR.iterdir():
                try:
                    if file.is_file():
                        file.unlink()
                    elif file.is_dir():
                        shutil.rmtree(file)
                except Exception as e:
                    logger.warning(f"Failed to clean {file}: {e}")

        logger.info("Cleanup complete")

    def export_report(self, output_path: str = None) -> str:
        """Export workflow report"""
        if not self.results:
            raise RuntimeError("No results to export. Run workflow first.")

        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = OUTPUT_DIR / f"workflow_report_{timestamp}.txt"

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("AUTO CLIPPER INDONESIA - WORKFLOW REPORT\n")
            f.write("=" * 60 + "\n\n")

            f.write(f"Timestamp: {datetime.now()}\n")
            f.write(f"Clips Processed: {len(self.results)}\n")
            f.write(f"Successful: {sum(1 for r in self.results if r['status'] == 'success')}\n")
            f.write(f"Failed: {sum(1 for r in self.results if r['status'] == 'failed')}\n\n")

            for result in self.results:
                f.write("-" * 40 + "\n")
                f.write(f"Clip: {result.get('clip_id', 'N/A')}\n")
                f.write(f"Status: {result.get('status', 'N/A')}\n")

                if result['status'] == 'success':
                    f.write(f"Output: {result.get('output_path', 'N/A')}\n")
                    f.write(f"Duration: {result.get('duration', 0):.1f}s\n")
                    f.write(f"Size: {result.get('size_mb', 0):.2f} MB\n")
                    f.write(f"Text: {result.get('original_text', '')[:50]}...\n")
                else:
                    f.write(f"Error: {result.get('error', 'Unknown')}\n")

            f.write("\n" + "=" * 60 + "\n")
            f.write("Report generated by Auto Clipper Indonesia\n")

        logger.info(f"Report exported: {output_path}")
        return str(output_path)


# Convenience function for simple usage
def quick_process(
    video_path: str,
    num_clips: int = 10,
    progress_callback: Callable[[float, str], None] = None
) -> Dict:
    """
    Quick workflow - analyze and export top clips

    Args:
        video_path: Path to video
        num_clips: Number of clips to export
        progress_callback: Progress callback

    Returns:
        Workflow results
    """
    config = WorkflowConfig(
        golden_moments_count=num_clips,
        clip_duration=30,
        output_resolution="720p"
    )

    workflow = AutoClipperWorkflow(config)
    return workflow.run_full_workflow(video_path, progress_callback)


# Standalone test function
if __name__ == "__main__":
    print("=" * 60)
    print("AUTO CLIPPER INDONESIA - WORKFLOW TEST")
    print("=" * 60)

    test_video = input("\nEnter video path (or press Enter to skip): ").strip()

    if test_video and os.path.exists(test_video):
        print(f"\nTesting with: {test_video}")

        def progress(p, msg):
            print(f"[{int(p * 100):3d}%] {msg}")

        print("\n🚀 Starting full workflow...")

        try:
            results = quick_process(
                test_video,
                num_clips=5,
                progress_callback=progress
            )

            print(f"\n✅ Workflow complete!")
            print(f"   Clips: {results['clips_processed']}")
            print(f"   Successful: {results['successful']}")
            print(f"   Failed: {results['failed']}")
            print(f"   Time: {results['total_duration_seconds']:.1f}s")

            for r in results['results'][:3]:
                print(f"   - {r['clip_id']}: {r.get('size_mb', 0)} MB")

        except RuntimeError as e:
            print(f"\n[ERROR] {e}")

    else:
        print("\n[INFO] No video provided.")
        print("\nUsage:")
        print("  from core.workflow import quick_process, AutoClipperWorkflow")
        print("")
        print("  # Quick mode (uses defaults)")
        print("  results = quick_process('video.mp4', num_clips=10)")
        print("")
        print("  # Full workflow with custom config")
        print("  config = WorkflowConfig(clip_duration=45, output_resolution='1080p')")
        print("  workflow = AutoClipperWorkflow(config)")
        print("  results = workflow.run_full_workflow('video.mp4')")

    print("\n✅ Workflow test complete")