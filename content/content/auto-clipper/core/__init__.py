"""
Auto Clipper Indonesia - Core Modules
AI-powered video processing with ViMax-inspired enhancements
"""

# Video Analysis
from .video_analyzer import VideoAnalyzer

# Video Processing
from .clip_engine import ClipEngine, ClipSegment

# 9:16 Reframing
from .reframe_engine import ReframeEngine

# Subtitle System
from .subtitle_engine import SubtitleEngine, SubtitleStyle, SubtitleStyles

# Workflow Orchestration
from .workflow import AutoClipperWorkflow, WorkflowConfig, quick_process

# === VI-MAX INSPIRED ENHANCEMENTS ===

# Consistency Engine - Track character/scene across clips
from .consistency_engine import ConsistencyEngine, CharacterProfile, SceneContext

# Storyboard Generator - Auto-generate shot lists and cinematography
from .storyboard_generator import (
    StoryboardGenerator,
    Storyboard,
    ShotPlan,
    ShotType,
    CameraMovement,
    generate_quick_storyboard
)

__all__ = [
    # Core
    'VideoAnalyzer',
    'ClipEngine',
    'ClipSegment',
    'ReframeEngine',
    'SubtitleEngine',
    'SubtitleStyle',
    'SubtitleStyles',
    'AutoClipperWorkflow',
    'WorkflowConfig',
    'quick_process',

    # ViMax-Inspired
    'ConsistencyEngine',
    'CharacterProfile',
    'SceneContext',
    'StoryboardGenerator',
    'Storyboard',
    'ShotPlan',
    'ShotType',
    'CameraMovement',
    'generate_quick_storyboard'
]

__version__ = "2.0.0"  # Upgraded with ViMax features