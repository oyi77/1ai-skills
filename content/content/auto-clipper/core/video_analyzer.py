"""
Auto Clipper Indonesia - Video Analyzer
AI-powered video analysis for golden moment detection
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# AI Libraries (with fallback)
try:
    from faster_whisper import WhisperModel
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    print("[WARNING] faster-whisper not installed. Run: pip install faster-whisper")

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False
    print("[WARNING] textblob not installed. Run: pip install textblob")

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    VADER_AVAILABLE = True
except ImportError:
    VADER_AVAILABLE = False
    print("[WARNING] vaderSentiment not installed. Run: pip install vaderSentiment")

# Settings - Self-contained for standalone skill
import os
from pathlib import Path
from datetime import datetime

# Default settings
TRANSCRIPTION_MODEL = "base"
WHISPER_LANGUAGE = "id"
GOLDEN_MOMENT_COUNT = 10
silicon_threshold = 0.5

# Create temp directory
TEMP_DIR = Path(__file__).parent.parent / "temp"
TEMP_DIR.mkdir(exist_ok=True)

import logging
logger = logging.getLogger(__name__)


class VideoAnalyzer:
    """
    AI Video Analyzer - Transcribe and detect golden moments
    """

    def __init__(self, model_size: str = TRANSCRIPTION_MODEL, device: str = "cpu"):
        """
        Initialize the video analyzer

        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
            device: Processing device (cpu or cuda)
        """
        self.model_size = model_size
        self.device = device
        self.model = None
        self.analyzer = None
        self.clips = []

        logger.info(f"Initializing VideoAnalyzer with {model_size} model on {device}")

    def load_model(self):
        """Load Whisper model and sentiment analyzer"""
        if not WHISPER_AVAILABLE:
            raise ImportError("faster-whisper not installed")

        logger.info(f"Loading Whisper {self.model_size} model...")
        self.model = WhisperModel(
            self.model_size,
            device=self.device,
            compute_type="int8"  # Optimize for CPU
        )
        logger.info("Whisper model loaded successfully")

        # Initialize sentiment analyzers
        if VADER_AVAILABLE:
            self.analyzer = SentimentIntensityAnalyzer()
            logger.info("VADER sentiment analyzer loaded")

        if TEXTBLOB_AVAILABLE:
            logger.info("TextBlob available for additional analysis")

        return self

    def unload_model(self):
        """Unload models to free memory"""
        self.model = None
        self.analyzer = None
        logger.info("Models unloaded to free memory")

    def transcribe(self, video_path: str, progress_callback=None) -> List[Dict]:
        """
        Transcribe video audio to text with timestamps

        Args:
            video_path: Path to video file
            progress_callback: Optional callback function (progress_0_to_1)

        Returns:
            List of transcription segments with timestamps
        """
        if not self.model:
            self.load_model()

        video_path = Path(video_path)
        if not video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")

        logger.info(f"Transcribing: {video_path.name}")

        try:
            # Run transcription
            segments, info = self.model.transcribe(
                str(video_path),
                language=WHISPER_LANGUAGE,
                beam_size=5,
                vad_filter=True,  # Voice activity detection
                vad_parameters=dict(
                    min_silence_duration_ms=500,
                    speech_pad_ms=400
                )
            )

            # Convert to list
            transcript = []
            for segment in segments:
                segment_data = {
                    'id': len(transcript),
                    'start': segment.start,
                    'end': segment.end,
                    'text': segment.text.strip(),
                    'words': []
                }

                # Add word-level timestamps if available
                if hasattr(segment, 'words') and segment.words:
                    segment_data['words'] = [
                        {
                            'word': word.word,
                            'start': word.start,
                            'end': word.end,
                            'probability': word.probability
                        }
                        for word in segment.words
                    ]

                transcript.append(segment_data)

            logger.info(f"Transcription complete: {len(transcript)} segments")

            if progress_callback:
                progress_callback(1.0)

            return transcript

        except Exception as e:
            logger.error(f"Transcription error: {e}")
            raise

    def analyze_sentiment(self, text: str) -> Dict:
        """
        Analyze sentiment of text

        Args:
            text: Text to analyze

        Returns:
            Sentiment scores (compound, pos, neg, neu)
        """
        if not self.analyzer:
            if VADER_AVAILABLE:
                self.analyzer = SentimentIntensityAnalyzer()
            else:
                return {'compound': 0.0, 'pos': 0.0, 'neg': 0.0, 'neu': 1.0}

        scores = self.analyzer.polarity_scores(text)
        return scores

    def detect_hooks(self, transcript: List[Dict], window_size: int = 5) -> List[Dict]:
        """
        Detect potential hook moments (high energy, early in segment)

        Args:
            transcript: List of transcription segments
            window_size: Seconds before/after to measure energy

        Returns:
            List of detected hooks with scores
        """
        hooks = []

        for segment in transcript:
            text = segment.get('text', '')
            if len(text) < 10:  # Skip very short segments
                continue

            # Skip first 3 seconds (intro often low energy)
            if segment['start'] < 3:
                continue

            # Analyze sentiment
            sentiment = self.analyze_sentiment(text)

            # Calculate hook score
            # Higher score for: emotional words, exclamation, questions
            hook_score = sentiment['compound']

            # Bonus for question marks (engagement)
            if '?' in text:
                hook_score += 0.2

            # Bonus for exclamation (enthusiasm)
            if '!' in text:
                hook_score += 0.1

            # Bonus for "you/your" (personalization)
            if any(word in text.lower() for word in ['you', 'your', 'ini', 'kamu']):
                hook_score += 0.1

            hooks.append({
                'type': 'hook',
                'start': segment['start'],
                'end': segment['end'],
                'duration': segment['end'] - segment['start'],
                'text': text[:100] + '...' if len(text) > 100 else text,
                'score': hook_score,
                'sentiment': sentiment
            })

        return hooks

    def detect_insights(self, transcript: List[Dict]) -> List[Dict]:
        """
        Detect insight/knowledge-drop moments (informative, valuable)

        Args:
            transcript: List of transcription segments

        Returns:
            List of detected insights with scores
        """
        insights = []

        # Keywords that indicate valuable content
        insight_keywords = [
            'caranya', 'cara', 'tips', 'Rahasia', 'rahasia',
            'jangan', 'jangan lupa', 'penting', 'perlu',
            'trik', 'strategi', 'formula', 'metode',
            'belajar', 'tahu', 'mengerti', 'paham',
            'materi', 'contoh', 'case', 'studi',
            'hasil', 'perform', 'berhasil', 'sukses',
            'uang', 'duit', 'income', 'revenue', 'duit',
            'bisa', 'mampu', 'mendapat', 'dapat'
        ]

        for segment in transcript:
            text = segment.get('text', '').lower()
            if len(text) < 15:
                continue

            # Check for insights
            keyword_matches = sum(1 for kw in insight_keywords if kw in text)
            sentiment = self.analyze_sentiment(text)

            # Calculate insight score
            insight_score = (keyword_matches * 0.1) + (sentiment['compound'] * 0.3)

            if insight_score > 0.2:
                insights.append({
                    'type': 'insight',
                    'start': segment['start'],
                    'end': segment['end'],
                    'duration': segment['end'] - segment['start'],
                    'text': segment['text'][:100] + '...' if len(segment['text']) > 100 else segment['text'],
                    'score': insight_score,
                    'sentiment': sentiment
                })

        return insights

    def detect_emotional_peaks(self, transcript: List[Dict]) -> List[Dict]:
        """
        Detect emotional peaks (high sentiment variance)

        Args:
            transcript: List of transcription segments

        Returns:
            List of emotional peaks with scores
        """
        peaks = []

        for segment in transcript:
            text = segment.get('text', '')
            if len(text) < 10:
                continue

            sentiment = self.analyze_sentiment(text)

            # Detect peaks (high emotion)
            if abs(sentiment['compound']) > 0.5:
                peaks.append({
                    'type': 'emotional',
                    'start': segment['start'],
                    'end': segment['end'],
                    'duration': segment['end'] - segment['start'],
                    'text': text[:100] + '...' if len(text) > 100 else text,
                    'score': abs(sentiment['compound']),
                    'sentiment': sentiment
                })

        return peaks

    def find_golden_moments(self, video_path: str, progress_callback=None) -> List[Dict]:
        """
        Main function: Find golden moments in video

        Args:
            video_path: Path to video file
            progress_callback: Optional callback

        Returns:
            List of golden moments sorted by score
        """
        logger.info(f"Finding golden moments in: {video_path}")

        # Progress: 20% - Transcribing
        if progress_callback:
            progress_callback(0.2)

        # Step 1: Transcribe
        transcript = self.transcribe(video_path, progress_callback=lambda p: progress_callback(0.2 + p * 0.4))

        if not transcript:
            logger.warning("No transcription result")
            return []

        # Progress: 60% - Analyzing hooks
        if progress_callback:
            progress_callback(0.6)

        # Step 2: Detect hooks
        hooks = self.detect_hooks(transcript)
        logger.info(f"Detected {len(hooks)} hooks")

        # Progress: 70% - Analyzing insights
        if progress_callback:
            progress_callback(0.7)

        # Step 3: Detect insights
        insights = self.detect_insights(transcript)
        logger.info(f"Detected {len(insights)} insights")

        # Progress: 80% - Analyzing peaks
        if progress_callback:
            progress_callback(0.8)

        # Step 4: Detect emotional peaks
        peaks = self.detect_emotional_peaks(transcript)
        logger.info(f"Detected {len(peaks)} emotional peaks")

        # Progress: 90% - Combining and ranking
        if progress_callback:
            progress_callback(0.9)

        # Step 5: Combine all moments
        all_moments = hooks + insights + peaks

        # Remove duplicates (overlapping segments)
        unique_moments = []
        used_ranges = []

        for moment in sorted(all_moments, key=lambda x: x['score'], reverse=True):
            start = moment['start']
            end = min(moment['end'], start + 30)  # Max 30 seconds

            # Check for overlap
            overlap = False
            for used_start, used_end in used_ranges:
                if not (start > used_end or end < used_start):
                    overlap = True
                    break

            if not overlap:
                unique_moments.append(moment)
                used_ranges.append((start, end))

            if len(unique_moments) >= GOLDEN_MOMENT_COUNT:
                break

        # Sort by score
        unique_moments.sort(key=lambda x: x['score'], reverse=True)

        # Calculate final scores and add metadata
        for i, moment in enumerate(unique_moments):
            moment['rank'] = i + 1
            moment['clip_id'] = f"clip_{i+1:03d}"

        # Progress: 100%
        if progress_callback:
            progress_callback(1.0)

        logger.info(f"Found {len(unique_moments)} golden moments")

        self.clips = unique_moments
        return unique_moments

    def export_moments(self, output_path: str = None) -> str:
        """
        Export golden moments to a text file

        Args:
            output_path: Path to output file

        Returns:
            Path to exported file
        """
        if not self.clips:
            raise ValueError("No moments to export. Run find_golden_moments first.")

        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = TEMP_DIR / f"golden_moments_{timestamp}.txt"

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("AUTO CLIPPER INDONESIA - GOLDEN MOMENTS REPORT\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Total moments detected: {len(self.clips)}\n")
            f.write(f"Report generated: {datetime.now()}\n\n")

            for clip in self.clips:
                f.write(f"\n--- Clip #{clip['clip_id']} ---\n")
                f.write(f"Type: {clip['type']}\n")
                f.write(f"Time: {clip['start']:.1f}s - {clip['end']:.1f}s\n")
                f.write(f"Duration: {clip['duration']:.1f}s\n")
                f.write(f"Score: {clip['score']:.3f}\n")
                f.write(f"Text: {clip['text']}\n")

        logger.info(f"Moments exported to: {output_path}")
        return str(output_path)

    def get_summary(self) -> Dict:
        """
        Get analysis summary

        Returns:
            Summary dictionary
        """
        if not self.clips:
            return {'status': 'No analysis run', 'clips': 0}

        types_count = {}
        total_duration = 0

        for clip in self.clips:
            types_count[clip['type']] = types_count.get(clip['type'], 0) + 1
            total_duration += clip['duration']

        return {
            'total_clips': len(self.clips),
            'types': types_count,
            'total_duration': total_duration,
            'avg_score': sum(c['score'] for c in self.clips) / len(self.clips),
            'top_type': max(types_count.items(), key=lambda x: x[1])[0] if types_count else None
        }


# Standalone test function
if __name__ == "__main__":
    print("=" * 60)
    print("AUTO CLIPPER INDONESIA - VIDEO ANALYZER TEST")
    print("=" * 60)

    # Check dependencies
    print("\nChecking dependencies:")
    print(f"  faster-whisper: {'✅' if WHISPER_AVAILABLE else '❌'}")
    print(f"  textblob: {'✅' if TEXTBLOB_AVAILABLE else '❌'}")
    print(f"  vaderSentiment: {'✅' if VADER_AVAILABLE else '❌'}")

    if not WHISPER_AVAILABLE:
        print("\n[ERROR] Please install faster-whisper first:")
        print("  pip install faster-whisper")
        exit(1)

    # Initialize analyzer
    print("\nInitializing analyzer...")
    analyzer = VideoAnalyzer(model_size="base", device="cpu")

    try:
        # Load model
        print("Loading Whisper model (base, int8)...")
        analyzer.load_model()
        print("✅ Model loaded!")

        # Test with sample video
        test_video = input("\nEnter video path (or press Enter to skip): ").strip()

        if test_video and os.path.exists(test_video):
            print(f"\nAnalyzing: {test_video}")

            def progress(p):
                print(f"Progress: {int(p * 100)}%", end="\r")

            # Find golden moments
            moments = analyzer.find_golden_moments(test_video, progress)

            print(f"\n✅ Analysis complete!")
            print(f"Found {len(moments)} golden moments:\n")

            for i, moment in enumerate(moments[:10]):
                print(f"  {i+1}. [{moment['start']:.0f}s - {moment['end']:.0f}s] "
                      f"[{moment['type']}] score={moment['score']:.2f}")
                print(f"     \"{moment['text'][:60]}...\"")

            # Export
            export_path = analyzer.export_moments()
            print(f"\n📄 Report exported to: {export_path}")

            # Summary
            summary = analyzer.get_summary()
            print(f"\n📊 Summary: {summary}")

        else:
            print("\n[INFO] No video provided. Analyzer ready for use.")
            print("Usage:")
            print("  analyzer = VideoAnalyzer()")
            print("  analyzer.load_model()")
            print("  moments = analyzer.find_golden_moments('video.mp4')")

    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
    finally:
        analyzer.unload_model()
        print("\n✅ Analyzer test complete")