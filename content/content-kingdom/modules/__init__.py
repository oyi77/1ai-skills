"""
Content Kingdom modules package.
Public surface hides the underlying source (autopilot_affiliate_engine, eddie-agent, etc.).
"""

from .base import BaseModule, load_config
from .persona_manager import PersonaManager
from .content_planner import ContentPlanner
from .quality_gate import QualityGate
from .analytics_engine import AnalyticsEngine
from .comment_manager import CommentManager
from .engagement_engine import EngagementEngine
from .content_repurposer import ContentRepurposer
from .trend_scanner import TrendScanner

# v2.0: Veris Design System + GeminiGen API client
from .veris_design import (
    VERIS_PALETTE,
    VERIS_FORMATS,
    VERIS_LAYOUT,
    PLATFORM_PRIORITY,
    build_veris_prompt,
    build_video_prompt,
    veris_prompt_for_platform,
)
from .geminigen_client import GeminiGenClient

try:
    from .postbridge_publisher import PostBridgePublisher
except ImportError:
    PostBridgePublisher = None  # type: ignore[assignment,misc]

try:
    from .orchestrator import Orchestrator
except ImportError:
    Orchestrator = None  # type: ignore[assignment,misc]

from .media_generator import generate_image, generate_video, generate_media
from .video_producer import VideoProducer

# v2.0: Learning Engine (self-improving)
from .learning_engine import (
    capture_feedback,
    capture_trainer_session,
    capture_performance,
    add_rule,
    get_active_rules,
    get_design_guidelines,
    get_copy_guidelines,
    build_prompt_with_learnings,
    get_top_performing_patterns,
    get_learning_stats,
    bootstrap_veris,
)
from .chat_learning_hook import (
    process_user_feedback,
    process_trainer_input,
    is_known_trainer,
    KNOWN_TRAINERS,
)

__all__ = [
    # Core
    "BaseModule",
    "load_config",
    # Content modules
    "PersonaManager",
    "ContentPlanner",
    "QualityGate",
    "AnalyticsEngine",
    "CommentManager",
    "EngagementEngine",
    "ContentRepurposer",
    "TrendScanner",
    # Publishing
    "PostBridgePublisher",
    "Orchestrator",
    # Media generation (legacy fallback chain)
    "generate_image",
    "generate_video",
    "generate_media",
    # v2.0: Veris Design System
    "VERIS_PALETTE",
    "VERIS_FORMATS",
    "VERIS_LAYOUT",
    "PLATFORM_PRIORITY",
    "build_veris_prompt",
    "build_video_prompt",
    "veris_prompt_for_platform",
    # v2.0: GeminiGen API client
    "GeminiGenClient",
    # v2.0: Learning Engine (self-improving)
    "capture_feedback",
    "capture_trainer_session",
    "capture_performance",
    "add_rule",
    "get_active_rules",
    "get_design_guidelines",
    "get_copy_guidelines",
    "build_prompt_with_learnings",
    "get_top_performing_patterns",
    "get_learning_stats",
    "bootstrap_veris",
    # v2.0: Chat Learning Hook
    "process_user_feedback",
    "process_trainer_input",
    "is_known_trainer",
    "KNOWN_TRAINERS",
    # v2.0: Video Producer (replaces 4 deprecated skills)
    "VideoProducer",
]
