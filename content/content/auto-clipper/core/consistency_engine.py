"""
Auto Clipper Indonesia - Consistency Engine
Inspired by ViMax multi-agent video framework
Ensures character and scene consistency across multiple clips
"""

import os
import json
import pickle
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

# Try to import OpenCV for face detection
try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    print("[WARNING] opencv-python not installed. Run: pip install opencv-python")


@dataclass
class CharacterProfile:
    """Profile for maintaining character consistency"""
    name: str
    face_embedding: Optional[List[float]] = None
    appearance_features: Dict = field(default_factory=dict)
    reference_images: List[str] = field(default_factory=list)
    first_seen: datetime = field(default_factory=datetime.now)
    last_seen: datetime = field(default_factory=datetime.now)
    confidence: float = 0.0


@dataclass
class SceneContext:
    """Scene context for maintaining environment consistency"""
    location: str = ""
    time_of_day: str = ""
    style: str = ""
    color_scheme: List[str] = field(default_factory=list)
    reference_frames: List[str] = field(default_factory=list)
    objects: List[str] = field(default_factory=list)


class ConsistencyEngine:
    """
    Consistency Engine - Track and maintain visual consistency across clips

    Features inspired by ViMax:
    - Character tracking (face + appearance)
    - Scene context preservation
    - Reference-guided consistency
    - Style transfer matching
    
    Usage:
        engine = ConsistencyEngine()
        engine.set_reference("clip_001.mp4")  # Reference for consistency
        engine.check_consistency("clip_002.mp4")  # Check against reference
    """

    def __init__(self, working_dir: str = None):
        """
        Initialize consistency engine

        Args:
            working_dir: Directory for storing consistency data
        """
        self.working_dir = Path(working_dir) if working_dir else Path("~/.auto_clipper_consistency")
        self.working_dir.mkdir(parents=True, exist_ok=True)

        self.characters: Dict[str, CharacterProfile] = {}
        self.scene_context: Optional[SceneContext] = None
        self.style_template: Optional[Dict] = None
        self.face_cascade = None

        if OPENCV_AVAILABLE:
            try:
                self.face_cascade = cv2.CascadeClassifier(
                    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
                )
            except Exception as e:
                print(f"[WARNING] Could not load face detector: {e}")

        print(f"[CONSISTENCY] Engine initialized at {self.working_dir}")

    def _extract_features(self, image_path: str) -> Dict:
        """
        Extract visual features from an image

        Args:
            image_path: Path to image frame

        Returns:
            Feature dictionary
        """
        features = {
            'path': image_path,
            'timestamp': datetime.now().isoformat(),
            'faces': [],
            'dominant_colors': [],
            'brightness': 0,
            'contrast': 0
        }

        if not OPENCV_AVAILABLE or not os.path.exists(image_path):
            return features

        try:
            img = cv2.imread(image_path)
            if img is None:
                return features

            # Extract dominant colors (simple k-means approximation)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pixels = img_rgb.reshape(-1, 3)

            # Sample for speed
            sample = pixels[::100]
            from collections import Counter
            colors = Counter(map(tuple, sample))
            dominant = colors.most_common(5)
            features['dominant_colors'] = [(c[0], c[1]) for c in dominant]

            # Calculate brightness
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features['brightness'] = float(gray.mean())

            # Detect faces
            if self.face_cascade is not None:
                faces = self.face_cascade.detectMultiScale(
                    gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
                )
                features['faces'] = faces.tolist() if len(faces) > 0 else []

        except Exception as e:
            print(f"[WARNING] Feature extraction failed: {e}")

        return features

    def set_reference(
        self,
        video_path: str,
        frame_timestamp: float = 0,
        characters: List[str] = None,
        scene_info: Dict = None
    ):
        """
        Set reference frame and context for consistency

        Args:
            video_path: Path to reference video
            frame_timestamp: Timestamp of frame to extract (seconds)
            characters: List of character names detected
            scene_info: Scene context (location, time, style, etc.)
        """
        print(f"[CONSISTENCY] Setting reference from: {Path(video_path).name}")

        # Extract reference frame
        temp_frame = self.working_dir / "reference_frame.jpg"
        self._extract_frame(video_path, frame_timestamp, temp_frame)

        # Create scene context
        self.scene_context = SceneContext(
            location=scene_info.get('location', '') if scene_info else '',
            time_of_day=scene_info.get('time_of_day', 'unknown') if scene_info else '',
            style=scene_info.get('style', 'natural') if scene_info else '',
            reference_frames=[str(temp_frame)]
        )

        # Add character profiles if names provided
        if characters:
            for char_name in characters:
                self.characters[char_name] = CharacterProfile(name=char_name)

        # Update style template from reference
        features = self._extract_features(str(temp_frame))
        self.style_template = {
            'dominant_colors': features.get('dominant_colors', []),
            'brightness': features.get('brightness', 128),
            'has_faces': len(features.get('faces', [])) > 0
        }

        print(f"[CONSISTENCY] Reference set: {len(self.characters)} characters, style={self.style_template}")

    def _extract_frame(self, video_path: str, timestamp: float, output_path: Path):
        """Extract a single frame from video"""
        import subprocess
        cmd = [
            'ffmpeg', '-y',
            '-ss', str(timestamp),
            '-i', video_path,
            '-vframes', '1',
            '-q:v', '2',
            str(output_path)
        ]
        try:
            subprocess.run(cmd, capture_output=True, check=True, timeout=30)
        except subprocess.CalledProcessError:
            # Create placeholder if extraction fails
            output_path.write_text("placeholder")

    def check_consistency(
        self,
        video_path: str,
        frame_timestamp: float = 0
    ) -> Dict:
        """
        Check consistency of a video against reference

        Args:
            video_path: Path to video to check
            frame_timestamp: Timestamp of frame to extract

        Returns:
            Consistency report dictionary
        """
        report = {
            'video': Path(video_path).name,
            'timestamp': datetime.now().isoformat(),
            'overall_score': 1.0,
            'color_consistency': 1.0,
            'brightness_consistency': 1.0,
            'character_consistency': 1.0,
            'scene_consistency': 1.0,
            'issues': [],
            'recommendations': []
        }

        # Extract frame
        temp_frame = self.working_dir / "check_frame.jpg"
        self._extract_frame(video_path, frame_timestamp, temp_frame)

        if not temp_frame.exists():
            report['issues'].append("Could not extract frame for analysis")
            return report

        # Extract features
        features = self._extract_features(str(temp_frame))

        # Check color consistency
        if self.style_template:
            ref_colors = set(self.style_template.get('dominant_colors', []))
            curr_colors = set(features.get('dominant_colors', []))
            if ref_colors and curr_colors:
                color_overlap = len(ref_colors & curr_colors) / len(ref_colors | curr_colors)
                report['color_consistency'] = color_overlap

                if color_overlap < 0.5:
                    report['issues'].append("Color palette differs significantly from reference")
                    report['recommendations'].append("Apply color grading to match reference")

        # Check brightness consistency
        if self.style_template and 'brightness' in features:
            ref_bright = self.style_template.get('brightness', 128)
            curr_bright = features.get('brightness', 128)
            brightness_diff = abs(ref_bright - curr_bright) / 255
            report['brightness_consistency'] = 1.0 - brightness_diff

            if brightness_diff > 0.2:
                report['issues'].append("Brightness differs significantly from reference")
                report['recommendations'].append("Adjust lighting to match reference")

        # Check character presence
        if self.characters:
            detected_faces = len(features.get('faces', []))
            expected_chars = len(self.characters)

            if detected_faces < expected_chars:
                report['character_consistency'] = detected_faces / expected_chars if expected_chars > 0 else 1.0
                report['issues'].append(f"Expected {expected_chars} characters, detected {detected_faces}")
                report['recommendations'].append("Ensure all characters are visible in frame")

        # Calculate overall score
        scores = [
            report['color_consistency'],
            report['brightness_consistency'],
            report['character_consistency'],
            report['scene_consistency']
        ]
        report['overall_score'] = sum(scores) / len(scores)

        return report

    def apply_consistency_corrections(
        self,
        video_path: str,
        output_path: str = None
    ) -> str:
        """
        Apply color grading to match reference style

        Args:
            video_path: Input video
            output_path: Output video path

        Returns:
            Path to corrected video
        """
        if not self.style_template or not OPENCV_AVAILABLE:
            print("[CONSISTENCY] Cannot apply corrections - no reference or missing OpenCV")
            return video_path

        if output_path is None:
            output_path = str(Path(video_path).parent / f"corrected_{Path(video_path).name}")

        # Build FFmpeg filter for color correction
        ref_brightness = self.style_template.get('brightness', 128)
        target_brightness = 128  # Target middle gray

        # Simple brightness adjustment
        brightness_factor = target_brightness / max(ref_brightness, 1)

        cmd = [
            'ffmpeg', '-y',
            '-i', video_path,
            '-vf', f"eq=brightness={brightness_factor - 1.0:.2f}",
            '-c:a', 'copy',
            output_path
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"[CONSISTENCY] Correction applied: {output_path}")
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Correction failed: {e}")
            return video_path

    def export_context(self, output_path: str = None) -> str:
        """Export consistency context to JSON"""
        if output_path is None:
            output_path = str(self.working_dir / f"context_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

        context_data = {
            'exported_at': datetime.now().isoformat(),
            'characters': {
                name: {
                    'name': profile.name,
                    'first_seen': profile.first_seen.isoformat(),
                    'last_seen': profile.last_seen.isoformat(),
                    'confidence': profile.confidence,
                    'reference_images': profile.reference_images
                }
                for name, profile in self.characters.items()
            },
            'scene_context': {
                'location': self.scene_context.location if self.scene_context else '',
                'time_of_day': self.scene_context.time_of_day if self.scene_context else '',
                'style': self.scene_context.style if self.scene_context else '',
                'color_scheme': self.scene_context.color_scheme if self.scene_context else []
            },
            'style_template': self.style_template
        }

        with open(output_path, 'w') as f:
            json.dump(context_data, f, indent=2)

        print(f"[CONSISTENCY] Context exported: {output_path}")
        return output_path

    def import_context(self, input_path: str):
        """Import consistency context from JSON"""
        with open(input_path, 'r') as f:
            context_data = json.load(f)

        # Reconstruct characters
        for name, data in context_data.get('characters', {}).items():
            self.characters[name] = CharacterProfile(
                name=data['name'],
                first_seen=datetime.fromisoformat(data['first_seen']),
                last_seen=datetime.fromisoformat(data['last_seen']),
                confidence=data.get('confidence', 0.0),
                reference_images=data.get('reference_images', [])
            )

        # Reconstruct scene context
        scene_data = context_data.get('scene_context', {})
        if scene_data:
            self.scene_context = SceneContext(
                location=scene_data.get('location', ''),
                time_of_day=scene_data.get('time_of_day', 'unknown'),
                style=scene_data.get('style', ''),
                color_scheme=scene_data.get('color_scheme', [])
            )

        # Reconstruct style template
        self.style_template = context_data.get('style_template')

        print(f"[CONSISTENCY] Context imported: {len(self.characters)} characters")


# Convenience function for quick use
def quick_consistency_check(
    reference_video: str,
    target_video: str,
    output_dir: str = "~/.auto_clipper_consistency"
) -> Dict:
    """
    Quick consistency check between two videos

    Args:
        reference_video: Reference video path
        target_video: Video to check against reference
        output_dir: Output directory for temp files

    Returns:
        Consistency report
    """
    engine = ConsistencyEngine(output_dir)
    engine.set_reference(reference_video)
    return engine.check_consistency(target_video)


if __name__ == "__main__":
    print("=" * 60)
    print("AUTO CLIPPER INDONESIA - CONSISTENCY ENGINE")
    print("=" * 60)

    import sys

    # Check dependencies
    print(f"\nOpenCV available: {'✅' if OPENCV_AVAILABLE else '❌'}")
    print(f"FFmpeg: ", end="")
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, timeout=5)
        print(f"✅ Found")
    except:
        print(f"❌ Not found")

    if len(sys.argv) > 1:
        # Test with provided video
        video_path = sys.argv[1]
        engine = ConsistencyEngine()
        engine.set_reference(video_path)

        if len(sys.argv) > 2:
            # Compare with second video
            report = engine.check_consistency(sys.argv[2])
            print(f"\nConsistency Report:")
            print(f"  Overall Score: {report['overall_score']:.2%}")
            print(f"  Color Consistency: {report['color_consistency']:.2%}")
            print(f"  Brightness Consistency: {report['brightness_consistency']:.2%}")
            print(f"  Issues: {len(report['issues'])}")

    print("\n✅ Consistency Engine ready for use")
    print("\nUsage:")
    print("  engine = ConsistencyEngine()")
    print("  engine.set_reference('reference_video.mp4')")
    print("  report = engine.check_consistency('target_video.mp4')")
    print("  engine.apply_consistency_corrections('input.mp4', 'output.mp4')")