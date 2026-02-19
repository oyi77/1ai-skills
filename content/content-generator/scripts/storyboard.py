"""Storyboard templates for video generation."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class StoryboardScene:
    """Represents a single scene in a storyboard."""

    scene_number: int
    duration_seconds: float
    description: str
    visual_prompt: str
    audio_description: Optional[str] = None
    text_overlay: Optional[str] = None
    camera_movement: Optional[str] = None  # e.g., "zoom_in", "pan_left", "static"
    transition: Optional[str] = None  # e.g., "fade", "cut", "dissolve"


@dataclass
class StoryboardTemplate:
    """Pre-defined storyboard template for video generation."""

    name: str
    description: str
    total_duration_seconds: float
    scenes: list[StoryboardScene] = field(default_factory=list)
    suggested_aspect_ratio: str = "16:9"  # e.g., "16:9", "9:16", "1:1"
    suggested_style: Optional[str] = (
        None  # e.g., "cinematic", "animated", "live_action"
    )


def get_template(template_name: str) -> Optional[StoryboardTemplate]:
    """Get a storyboard template by name.

    Args:
        template_name: Name of the template to retrieve.

    Returns:
        The StoryboardTemplate if found, None otherwise.
    """
    templates = {
        "ad_short": _create_ad_short_template(),
        "product_showcase": _create_product_showcase_template(),
        "storytelling": _create_storytelling_template(),
        "tutorial": _create_tutorial_template(),
    }
    return templates.get(template_name.lower())


def list_templates() -> list[str]:
    """List all available template names.

    Returns:
        List of template names.
    """
    return ["ad_short", "product_showcase", "storytelling", "tutorial"]


def _create_ad_short_template() -> StoryboardTemplate:
    """Create a short advertisement template (15-30 seconds)."""
    scenes = [
        StoryboardScene(
            scene_number=1,
            duration_seconds=3.0,
            description="Opening hook - attention grabber",
            visual_prompt="Bold, eye-catching visual with motion",
            audio_description="Upbeat music starts",
            text_overlay="Attention-grabbing headline",
            camera_movement="zoom_in",
            transition="fade_in",
        ),
        StoryboardScene(
            scene_number=2,
            duration_seconds=5.0,
            description="Problem statement",
            visual_prompt="Relatable problem scenario",
            audio_description="Narrator explains the problem",
            text_overlay="Problem statement text",
            camera_movement="static",
            transition="cut",
        ),
        StoryboardScene(
            scene_number=3,
            duration_seconds=5.0,
            description="Product/service introduction",
            visual_prompt="Showcase the product or service",
            audio_description="Presentation of solution",
            text_overlay="Product name and tagline",
            camera_movement="pan_right",
            transition="dissolve",
        ),
        StoryboardScene(
            scene_number=4,
            duration_seconds=5.0,
            description="Benefits highlight",
            visual_prompt="Demonstrate key benefits",
            audio_description="Narrator highlights benefits",
            text_overlay="Benefit points",
            camera_movement="tracking",
            transition="cut",
        ),
        StoryboardScene(
            scene_number=5,
            duration_seconds=2.0,
            description="Call to action",
            visual_prompt="Strong closing visual",
            audio_description="Music peaks, call to action",
            text_overlay="CTA with link",
            camera_movement="static",
            transition="fade_out",
        ),
    ]

    return StoryboardTemplate(
        name="ad_short",
        description="Short advertisement template (15-30 seconds) with hook, problem, solution, benefits, and CTA",
        total_duration_seconds=20.0,
        scenes=scenes,
        suggested_aspect_ratio="16:9",
        suggested_style="cinematic",
    )


def _create_product_showcase_template() -> StoryboardTemplate:
    """Create a product showcase template (30-60 seconds)."""
    scenes = [
        StoryboardScene(
            scene_number=1,
            duration_seconds=2.0,
            description="Title card",
            visual_prompt="Clean product name display",
            audio_description="Soft music begins",
            text_overlay="Product name",
            camera_movement="static",
            transition="fade_in",
        ),
        StoryboardScene(
            scene_number=2,
            duration_seconds=6.0,
            description="Product reveal - wide shot",
            visual_prompt="Full product in context",
            audio_description="Music builds",
            camera_movement="reveal",
            transition="dissolve",
        ),
        StoryboardScene(
            scene_number=3,
            duration_seconds=8.0,
            description="Feature 1 demonstration",
            visual_prompt="Close-up of feature 1 in use",
            audio_description="Narrator explains feature",
            text_overlay="Feature name",
            camera_movement="macro",
            transition="cut",
        ),
        StoryboardScene(
            scene_number=4,
            duration_seconds=8.0,
            description="Feature 2 demonstration",
            visual_prompt="Close-up of feature 2 in use",
            audio_description="Narrator explains feature",
            text_overlay="Feature name",
            camera_movement="macro",
            transition="cut",
        ),
        StoryboardScene(
            scene_number=5,
            duration_seconds=8.0,
            description="Feature 3 demonstration",
            visual_prompt="Close-up of feature 3 in use",
            audio_description="Narrator explains feature",
            text_overlay="Feature name",
            camera_movement="macro",
            transition="cut",
        ),
        StoryboardScene(
            scene_number=6,
            duration_seconds=4.0,
            description="Lifestyle/context shot",
            visual_prompt="Product in real-world use",
            audio_description="Music swells",
            text_overlay="Use case tagline",
            camera_movement="tracking",
            transition="dissolve",
        ),
        StoryboardScene(
            scene_number=7,
            duration_seconds=3.0,
            description="Closing shot",
            visual_prompt="Product with logo",
            audio_description="Music resolves",
            text_overlay="Logo and CTA",
            camera_movement="zoom_out",
            transition="fade_out",
        ),
    ]

    return StoryboardTemplate(
        name="product_showcase",
        description="Product showcase template (30-60 seconds) with features, lifestyle shots, and CTA",
        total_duration_seconds=39.0,
        scenes=scenes,
        suggested_aspect_ratio="16:9",
        suggested_style="product_photography",
    )


def _create_storytelling_template() -> StoryboardTemplate:
    """Create a storytelling/narrative template (60-120 seconds)."""
    scenes = [
        StoryboardScene(
            scene_number=1,
            duration_seconds=5.0,
            description="Opening - establish setting",
            visual_prompt="Wide establishing shot",
            audio_description="Atmospheric music, ambient sounds",
            camera_movement="drone_overview",
            transition="fade_in",
        ),
        StoryboardScene(
            scene_number=2,
            duration_seconds=10.0,
            description="Introduce protagonist",
            visual_prompt="Character introduction",
            audio_description="Character-focused music",
            text_overlay="Character name or role",
            camera_movement="tracking",
            transition="cut",
        ),
        StoryboardScene(
            scene_number=3,
            duration_seconds=15.0,
            description="Challenge/problem arises",
            visual_prompt="Obstacle or challenge",
            audio_description="Tension builds in music",
            text_overlay="Challenge statement",
            camera_movement="close_up",
            transition="dissolve",
        ),
        StoryboardScene(
            scene_number=4,
            duration_seconds=20.0,
            description="Journey/attempt to overcome",
            visual_prompt="Action sequence or struggle",
            audio_description="Dynamic music, sound effects",
            camera_movement="dynamic",
            transition="quick_cuts",
        ),
        StoryboardScene(
            scene_number=5,
            duration_seconds=10.0,
            description="Turning point",
            visual_prompt="Key moment of realization",
            audio_description="Music shift - hope",
            text_overlay="Key insight",
            camera_movement="slow_motion",
            transition="slow_dissolve",
        ),
        StoryboardScene(
            scene_number=6,
            duration_seconds=15.0,
            description="Resolution",
            visual_prompt="Problem solved, success",
            audio_description="Triumphant music",
            camera_movement="pull_back",
            transition="dissolve",
        ),
        StoryboardScene(
            scene_number=7,
            duration_seconds=5.0,
            description="Closing message",
            visual_prompt="Final emotional image",
            audio_description="Music softens",
            text_overlay="Message or brand statement",
            camera_movement="static",
            transition="fade_out",
        ),
    ]

    return StoryboardTemplate(
        name="storytelling",
        description="Narrative storytelling template (60-120 seconds) with character, conflict, and resolution",
        total_duration_seconds=80.0,
        scenes=scenes,
        suggested_aspect_ratio="16:9",
        suggested_style="cinematic",
    )


def _create_tutorial_template() -> StoryboardTemplate:
    """Create a tutorial/how-to template (45-180 seconds)."""
    scenes = [
        StoryboardScene(
            scene_number=1,
            duration_seconds=3.0,
            description="Intro - what you'll learn",
            visual_prompt="Preview of final result",
            audio_description="Upbeat tutorial music",
            text_overlay="Tutorial title",
            camera_movement="static",
            transition="fade_in",
        ),
        StoryboardScene(
            scene_number=2,
            duration_seconds=5.0,
            description="Overview of steps",
            visual_prompt="List or roadmap visualization",
            audio_description="Brief overview narration",
            text_overlay="Step 1, 2, 3...",
            camera_movement="static",
            transition="cut",
        ),
        StoryboardScene(
            scene_number=3,
            duration_seconds=15.0,
            description="Step 1 - prerequisite/setup",
            visual_prompt="Show setup or prerequisite",
            audio_description="Step 1 explanation",
            text_overlay="Step 1: [action]",
            camera_movement="screen_record",
            transition="cut",
        ),
        StoryboardScene(
            scene_number=4,
            duration_seconds=20.0,
            description="Step 2 - main action",
            visual_prompt="Main tutorial action",
            audio_description="Step 2 explanation",
            text_overlay="Step 2: [action]",
            camera_movement="screen_record",
            transition="cut",
        ),
        StoryboardScene(
            scene_number=5,
            duration_seconds=15.0,
            description="Step 3 - continuation",
            visual_prompt="Continue tutorial",
            audio_description="Step 3 explanation",
            text_overlay="Step 3: [action]",
            camera_movement="screen_record",
            transition="cut",
        ),
        StoryboardScene(
            scene_number=6,
            duration_seconds=10.0,
            description="Step 4 - final step",
            visual_prompt="Final step completion",
            audio_description="Step 4 explanation",
            text_overlay="Step 4: [action]",
            camera_movement="screen_record",
            transition="cut",
        ),
        StoryboardScene(
            scene_number=7,
            duration_seconds=5.0,
            description="Result showcase",
            visual_prompt="Show the completed result",
            audio_description="Success music",
            text_overlay="Success message",
            camera_movement="zoom",
            transition="dissolve",
        ),
        StoryboardScene(
            scene_number=8,
            duration_seconds=3.0,
            description="Tips and common mistakes",
            visual_prompt="Quick tips display",
            audio_description="Tips narration",
            text_overlay="Tip: ...",
            camera_movement="static",
            transition="cut",
        ),
        StoryboardScene(
            scene_number=9,
            duration_seconds=2.0,
            description="Outro with CTA",
            visual_prompt="Call to action",
            audio_description="Thanks and CTA",
            text_overlay="Subscribe/Learn more",
            camera_movement="static",
            transition="fade_out",
        ),
    ]

    return StoryboardTemplate(
        name="tutorial",
        description="Tutorial/how-to template (45-180 seconds) with clear steps, tips, and CTA",
        total_duration_seconds=78.0,
        scenes=scenes,
        suggested_aspect_ratio="16:9",
        suggested_style="screen_record",
    )
