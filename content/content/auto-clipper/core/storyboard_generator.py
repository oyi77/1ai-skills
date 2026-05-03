"""
Auto Clipper Indonesia - Storyboard Generator
Inspired by ViMax - Auto-generate shot lists and cinematographic planning
"""

import json
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ShotType(Enum):
    """Cinematic shot types"""
    WIDE = "wide"           # Establishing shot
    MEDIUM = "medium"       # Character from waist up
    CLOSE_UP = "close_up"   # Face only
    EXTREME_CLOSE_UP = "ecu"  # Details (eyes, hands)
    POV = "pov"             # Point of view
    OVER_SHOULDER = "os"    # Over shoulder
    LOW_ANGLE = "low"       # Low angle (empowering)
    HIGH_ANGLE = "high"     # High angle (vulnerable)
    DRONE = "drone"         # Aerial shot
    TRACKING = "tracking"   # Moving shot


class CameraMovement(Enum):
    """Camera movement types"""
    STATIC = "static"
    PAN_LEFT = "pan_left"
    PAN_RIGHT = "pan_right"
    TILT_UP = "tilt_up"
    TILT_DOWN = "tilt_down"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"
    DOLLY_IN = "dolly_in"
    DOLLY_OUT = "dolly_out"
    TRACK = "track"
    CRANE = "crane"


@dataclass
class ShotPlan:
    """Individual shot plan"""
    shot_id: str
    shot_type: ShotType
    duration_seconds: float
    start_time: float
    end_time: float
    camera_movement: CameraMovement = CameraMovement.STATIC
    description: str = ""
    visual_goal: str = ""
    audio_notes: str = ""
    transition_to_next: str = "cut"  # cut, dissolve, wipe, fade
    technical_notes: str = ""


@dataclass
class Storyboard:
    """Complete storyboard for video production"""
    storyboard_id: str
    title: str
    source_content: str
    clips: List[ShotPlan] = field(default_factory=list)
    total_duration: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    style: str = "natural"
    resolution: str = "720p"
    aspect_ratio: str = "9:16"


class StoryboardGenerator:
    """
    Storyboard Generator - Auto-generate shot lists and cinematography plans

    Features:
    - Analyze content and generate shot plans
    - Apply cinematographic principles
    - Match shots to content type (hook, insight, emotion)
    - Generate TikTok/Shorts-optimized storyboards
    - Export to JSON for integration with video tools
    """

    def __init__(self):
        """Initialize storyboard generator"""
        self.shot_library = self._build_shot_library()
        print("[STORYBOARD] Generator initialized")

    def _build_shot_library(self) -> Dict:
        """Build library of shot templates"""
        return {
            'hook_open': {
                'shots': [
                    {'type': ShotType.EXTREME_CLOSE_UP, 'duration': 3, 'movement': CameraMovement.ZOOM_IN},
                    {'type': ShotType.POV, 'duration': 5, 'movement': CameraMovement.STATIC},
                    {'type': ShotType.MEDIUM, 'duration': 10, 'movement': CameraMovement.STATIC},
                ],
                'style': 'attention-grabbing',
                'transition': 'quick_cut'
            },
            'insight_explanation': {
                'shots': [
                    {'type': ShotType.MEDIUM, 'duration': 8, 'movement': CameraMovement.STATIC},
                    {'type': ShotType.WIDE, 'duration': 5, 'movement': CameraMovement.PAN_RIGHT},
                    {'type': ShotType.CLOSE_UP, 'duration': 10, 'movement': CameraMovement.ZOOM_IN},
                    {'type': ShotType.MEDIUM, 'duration': 7, 'movement': CameraMovement.STATIC},
                ],
                'style': 'educational',
                'transition': 'smooth'
            },
            'emotional_peak': {
                'shots': [
                    {'type': ShotType.CLOSE_UP, 'duration': 5, 'movement': CameraMovement.STATIC},
                    {'type': ShotType.WIDE, 'duration': 8, 'movement': CameraMovement.DOLLY_OUT},
                    {'type': ShotType.CLOSE_UP, 'duration': 7, 'movement': CameraMovement.ZOOM_IN},
                ],
                'style': 'emotional',
                'transition': 'dissolve'
            },
            'product_showcase': {
                'shots': [
                    {'type': ShotType.MEDIUM, 'duration': 5, 'movement': CameraMovement.TRACK},
                    {'type': ShotType.EXTREME_CLOSE_UP, 'duration': 4, 'movement': CameraMovement.STATIC},
                    {'type': ShotType.POV, 'duration': 6, 'movement': CameraMovement.STATIC},
                    {'type': ShotType.WIDE, 'duration': 5, 'movement': CameraMovement.DOLLY_IN},
                ],
                'style': 'commercial',
                'transition': 'quick_cut'
            },
            'before_after': {
                'shots': [
                    {'type': ShotType.WIDE, 'duration': 4, 'movement': CameraMovement.STATIC},
                    {'type': ShotType.CLOSE_UP, 'duration': 3, 'movement': CameraMovement.ZOOM_IN},
                    {'type': ShotType.MEDIUM, 'duration': 5, 'movement': CameraMovement.STATIC},
                    {'type': ShotType.CLOSE_UP, 'duration': 8, 'movement': CameraMovement.ZOOM_IN},
                ],
                'style': 'transformative',
                'transition': 'wipe'
            }
        }

    def generate_from_content(
        self,
        content_type: str,
        total_duration: float = 30,
        aspect_ratio: str = "9:16"
    ) -> Storyboard:
        """
        Generate storyboard from content type

        Args:
            content_type: Type of content (hook_open, insight_explanation, etc.)
            total_duration: Target total duration
            aspect_ratio: Video aspect ratio (9:16, 16:9, 1:1)

        Returns:
            Complete Storyboard object
        """
        # Get shot template
        template = self.shot_library.get(content_type, self.shot_library['hook_open'])
        shots_template = template['shots']

        # Calculate timing
        total_shot_time = sum(s['duration'] for s in shots_template)
        time_multiplier = total_duration / total_shot_time if total_shot_time > 0 else 1.0

        # Generate shots
        storyboard_id = f"sb_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        clips = []

        current_time = 0.0
        for i, shot_template in enumerate(shots_template):
            duration = shot_template['duration'] * time_multiplier
            clip = ShotPlan(
                shot_id=f"shot_{i+1:03d}",
                shot_type=shot_template['type'],
                duration_seconds=duration,
                start_time=current_time,
                end_time=current_time + duration,
                camera_movement=shot_template['movement'],
                description=self._get_shot_description(shot_template['type']),
                visual_goal=self._get_visual_goal(shot_template['type'], content_type),
                transition_to_next="cut" if i < len(shots_template) - 1 else "end"
            )
            clips.append(clip)
            current_time += duration

        return Storyboard(
            storyboard_id=storyboard_id,
            title=f"{content_type.replace('_', ' ').title()} Storyboard",
            source_content=content_type,
            clips=clips,
            total_duration=current_time,
            style=template['style'],
            aspect_ratio=aspect_ratio
        )

    def generate_short_form(
        self,
        content_type: str,
        duration: float = 30
    ) -> Storyboard:
        """
        Generate TikTok-style short form storyboard

        Optimized for:
        - Fast-paced editing
        - Attention-grabbing openings
        - Mobile-first viewing
        """
        # Adjust for short form
        if duration <= 15:
            # Very short - focus on hook + single message
            template_name = 'hook_open'
            multiplier = 0.8
        elif duration <= 30:
            # Standard short
            template_name = content_type if content_type in self.shot_library else 'hook_open'
            multiplier = 1.0
        else:
            # Extended - add buffer shots
            template_name = content_type if content_type in self.shot_library else 'insight_explanation'
            multiplier = 1.2

        storyboard = self.generate_from_content(template_name, duration * multiplier, "9:16")

        # Optimize for short form
        for clip in storyboard.clips:
            # Accelerate transitions
            if clip.transition_to_next != "end":
                clip.transition_to_next = "quick_cut" if duration < 30 else "cut"

            # Add energy to camera movements
            if clip.camera_movement == CameraMovement.STATIC and duration < 30:
                if clip.shot_type in [ShotType.EXTREME_CLOSE_UP, ShotType.CLOSE_UP]:
                    clip.camera_movement = CameraMovement.ZOOM_IN
                elif clip.shot_type == ShotType.WIDE:
                    clip.camera_movement = CameraMovement.DOLLY_IN

        # Trim to exact duration
        actual_duration = sum(c.duration_seconds for c in storyboard.clips)
        if actual_duration > duration:
            # Remove from last clip
            excess = actual_duration - duration
            storyboard.clips[-1].duration_seconds -= excess
            storyboard.clips[-1].end_time -= excess
            storyboard.total_duration = duration

        return storyboard

    def generate_from_script(
        self,
        script: str,
        style: str = "natural",
        duration_per_shot: float = 5.0
    ) -> Storyboard:
        """
        Generate storyboard from script text

        Args:
            script: Script/screenplay text
            style: Visual style (natural, dramatic, energetic)
            duration_per_shot: Average seconds per shot

        Returns:
            Storyboard based on script analysis
        """
        # Simple script analysis - split by sentences/paragraphs
        segments = [s.strip() for s in script.split('.') if s.strip()]
        num_shots = min(len(segments), int(60 / duration_per_shot))  # Max 1 min or 12 shots

        storyboard_id = f"sb_script_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        clips = []

        current_time = 0.0
        for i in range(num_shots):
            segment = segments[i]
            shot_type = self._infer_shot_from_text(segment)
            clip = ShotPlan(
                shot_id=f"shot_{i+1:03d}",
                shot_type=shot_type,
                duration_seconds=duration_per_shot,
                start_time=current_time,
                end_time=current_time + duration_per_shot,
                camera_movement=CameraMovement.STATIC,
                description=f"Scene: {segment[:50]}...",
                visual_goal=self._get_visual_goal(shot_type, "script"),
                transition_to_next="cut" if i < num_shots - 1 else "end"
            )
            clips.append(clip)
            current_time += duration_per_shot

        return Storyboard(
            storyboard_id=storyboard_id,
            title="Script-Based Storyboard",
            source_content=script[:200] + "...",
            clips=clips,
            total_duration=current_time,
            style=style
        )

    def _infer_shot_from_text(self, text: str) -> ShotType:
        """Infer shot type from text content"""
        text_lower = text.lower()

        # Keywords indicating specific shots
        if any(w in text_lower for w in ['reveal', 'overview', 'scene', 'setting', 'place']):
            return ShotType.WIDE
        elif any(w in text_lower for w in ['face', 'emotion', 'feeling', 'reaction']):
            return ShotType.CLOSE_UP
        elif any(w in text_lower for w in ['detail', 'focus', 'specifically']):
            return ShotType.EXTREME_CLOSE_UP
        elif any(w in text_lower for w in ['behind', 'perspective', 'view']):
            return ShotType.POV
        elif any(w in text_lower for w in ['above', 'looking down']):
            return ShotType.HIGH_ANGLE
        elif any(w in text_lower for w in ['upward', 'empowering']):
            return ShotType.LOW_ANGLE
        else:
            return ShotType.MEDIUM

    def _get_shot_description(self, shot_type: ShotType) -> str:
        """Get description for shot type"""
        descriptions = {
            ShotType.WIDE: "Establishing shot - shows environment and context",
            ShotType.MEDIUM: "Standard character shot - waist up",
            ShotType.CLOSE_UP: "Face focus - captures emotion and expression",
            ShotType.EXTREME_CLOSE_UP: "Detail focus - eyes, hands, small elements",
            ShotType.POV: "Point of view - viewer perspective",
            ShotType.OVER_SHOULDER: "Over shoulder - shows character interaction",
            ShotType.LOW_ANGLE: "Low angle - empowering/subject dominance",
            ShotType.HIGH_ANGLE: "High angle - vulnerable/overwhelmed",
            ShotType.DRONE: "Aerial view - grand scale",
            ShotType.TRACKING: "Moving shot - follows action"
        }
        return descriptions.get(shot_type, "Standard shot")

    def _get_visual_goal(self, shot_type: ShotType, context: str) -> str:
        """Get visual goal based on shot type and context"""
        goals = {
            (ShotType.WIDE, "hook_open"): "Show scale and importance",
            (ShotType.CLOSE_UP, "hook_open"): "Create intimacy and connection",
            (ShotType.MEDIUM, "insight_explanation"): "Clear explanation delivery",
            (ShotType.CLOSE_UP, "insight_explanation"): "Emphasize key points",
            (ShotType.WIDE, "emotional_peak"): "Show scope of emotion",
            (ShotType.CLOSE_UP, "emotional_peak"): "Capture raw emotion",
            (ShotType.MEDIUM, "product_showcase"): "Show product in context",
            (ShotType.EXTREME_CLOSE_UP, "product_showcase"): "Highlight details",
        }
        return goals.get((shot_type, context), "Support content delivery")

    def export_storyboard(self, storyboard: Storyboard, output_path: str = None) -> str:
        """Export storyboard to JSON"""
        data = {
            'storyboard_id': storyboard.storyboard_id,
            'title': storyboard.title,
            'source_content': storyboard.source_content,
            'total_duration': storyboard.total_duration,
            'style': storyboard.style,
            'aspect_ratio': storyboard.aspect_ratio,
            'created_at': storyboard.created_at.isoformat(),
            'shots': [
                {
                    'shot_id': shot.shot_id,
                    'shot_type': shot.shot_type.value,
                    'duration_seconds': shot.duration_seconds,
                    'start_time': shot.start_time,
                    'end_time': shot.end_time,
                    'camera_movement': shot.camera_movement.value,
                    'description': shot.description,
                    'visual_goal': shot.visual_goal,
                    'transition_to_next': shot.transition_to_next
                }
                for shot in storyboard.clips
            ]
        }

        if output_path is None:
            output_path = f"storyboard_{storyboard.storyboard_id}.json"

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"[STORYBOARD] Exported: {output_path}")
        return output_path

    def import_storyboard(self, input_path: str) -> Storyboard:
        """Import storyboard from JSON"""
        with open(input_path, 'r') as f:
            data = json.load(f)

        clips = []
        for shot_data in data.get('shots', []):
            clip = ShotPlan(
                shot_id=shot_data['shot_id'],
                shot_type=ShotType(shot_data['shot_type']),
                duration_seconds=shot_data['duration_seconds'],
                start_time=shot_data['start_time'],
                end_time=shot_data['end_time'],
                camera_movement=CameraMovement(shot_data['camera_movement']),
                description=shot_data.get('description', ''),
                visual_goal=shot_data.get('visual_goal', ''),
                transition_to_next=shot_data.get('transition_to_next', 'cut')
            )
            clips.append(clip)

        return Storyboard(
            storyboard_id=data['storyboard_id'],
            title=data['title'],
            source_content=data.get('source_content', ''),
            clips=clips,
            total_duration=data.get('total_duration', 0),
            style=data.get('style', 'natural'),
            aspect_ratio=data.get('aspect_ratio', '9:16')
        )

    def print_storyboard(self, storyboard: Storyboard):
        """Pretty print storyboard"""
        print(f"\n{'='*60}")
        print(f"STORYBOARD: {storyboard.title}")
        print(f"{'='*60}")
        print(f"ID: {storyboard.storyboard_id}")
        print(f"Style: {storyboard.style} | Duration: {storyboard.total_duration:.1f}s | {storyboard.aspect_ratio}")
        print(f"{'-'*60}")

        for shot in storyboard.clips:
            print(f"\n[{shot.shot_id}] {shot.shot_type.value.upper()}")
            print(f"  Time: {shot.start_time:.1f}s - {shot.end_time:.1f}s ({shot.duration_seconds:.1f}s)")
            print(f"  Camera: {shot.camera_movement.value}")
            print(f"  Goal: {shot.visual_goal}")
            print(f"  → Next: {shot.transition_to_next}")

        print(f"\n{'='*60}")
        print(f"TOTAL SHOTS: {len(storyboard.clips)} | DURATION: {storyboard.total_duration:.1f}s")
        print(f"{'='*60}\n")


# Quick function for CLI usage
def generate_quick_storyboard(
    content_type: str = "hook_open",
    duration: float = 30,
    output_path: str = None
) -> Storyboard:
    """Quick storyboard generation"""
    generator = StoryboardGenerator()
    storyboard = generator.generate_short_form(content_type, duration)

    if output_path:
        generator.export_storyboard(storyboard, output_path)

    return storyboard


if __name__ == "__main__":
    print("=" * 60)
    print("AUTO CLIPPER INDONESIA - STORYBOARD GENERATOR")
    print("Inspired by ViMax Multi-Agent Framework")
    print("=" * 60)

    generator = StoryboardGenerator()

    # Generate example storyboards
    print("\n📋 Generating example storyboards...\n")

    # Hook storyboard
    hook_sb = generator.generate_short_form("hook_open", 15)
    print("🎯 15-second HOOK storyboard:")
    generator.print_storyboard(hook_sb)

    # Insight storyboard
    insight_sb = generator.generate_short_form("insight_explanation", 30)
    print("\n💡 30-second INSIGHT storyboard:")
    generator.print_storyboard(insight_sb)

    # Product storyboard
    product_sb = generator.generate_short_form("product_showcase", 30)
    print("\n🛒 30-second PRODUCT storyboard:")
    generator.print_storyboard(product_sb)

    # Export to JSON
    print("\n📁 Exporting storyboards to JSON...")
    generator.export_storyboard(hook_sb, "storyboard_hook.json")
    generator.export_storyboard(insight_sb, "storyboard_insight.json")
    print("✅ Generated: storyboard_hook.json, storyboard_insight.json")

    print("\n✅ Storyboard Generator ready!")
    print("\nUsage:")
    print("  from core.storyboard_generator import generate_quick_storyboard")
    print("  sb = generate_quick_storyboard('hook_open', 30)")
    print("  sb = generate_quick_storyboard('product_showcase', 15)")