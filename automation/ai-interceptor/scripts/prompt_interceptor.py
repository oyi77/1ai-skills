"""
prompt_interceptor.py — AI Generation Prompt Quality Interceptor
================================================================
Specialized interceptor for AI generation prompts (image/video/audio).

PRE hooks:
  - Rewrite raw prompts to cinematic/professional quality
  - Language normalization (Indonesian → English for global models)
  - Negative prompt generation

POST hooks:
  - Quality scoring of generated output
  - Style consistency check

ERROR hooks:
  - Prompt simplification on content policy violations
  - Format normalization on parsing errors
"""

from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Optional, Tuple

from ai_interceptor import (
    AIInterceptor,
    ErrorHook,
    InterceptContext,
    PostHook,
    PreHook,
    call_llm,
    call_llm_json,
)

logger = logging.getLogger("prompt_interceptor")

# ---------------------------------------------------------------------------
# Prompt enhancement templates per generation type
# ---------------------------------------------------------------------------
ENHANCEMENT_TEMPLATES: Dict[str, str] = {
    "kling_i2v": (
        "You are a professional AI video prompt engineer. Transform this input into a cinematic "
        "video generation prompt for Kling AI. Include: camera movement (dolly/pan/zoom), "
        "lighting quality, motion speed, scene atmosphere, visual style. "
        "Max 200 characters. Return ONLY the enhanced prompt in English."
    ),
    "kling_t2v": (
        "Transform this into a cinematic text-to-video prompt for Kling AI. "
        "Include: scene setting, character action, camera work, lighting, mood. "
        "Max 200 characters. Return ONLY the enhanced prompt in English."
    ),
    "flow_i2v": (
        "Transform this into a professional image-to-video prompt for Flow AI. "
        "Focus on: smooth motion, dynamic movement, visual continuity. "
        "Max 150 characters. Return ONLY the enhanced prompt in English."
    ),
    "pixverse_i2v": (
        "Transform this into a high-fidelity video prompt for PixVerse. "
        "Emphasize: detailed motion, stable video, high resolution quality. "
        "Max 200 characters. Return ONLY the enhanced prompt in English."
    ),
    "image_gen": (
        "Transform this into a professional image generation prompt. "
        "Include: style (photorealistic/artistic), lighting, composition, quality modifiers. "
        "Max 300 characters. Return ONLY the enhanced prompt in English."
    ),
    "default": (
        "You are a prompt engineering expert. Rewrite this prompt to be more specific, "
        "detailed, and effective for AI generation. Include relevant quality modifiers. "
        "Return ONLY the improved prompt in English."
    ),
}

# Cinematic quality modifiers
CINEMATIC_MODIFIERS: List[str] = [
    "cinematic lighting",
    "professional quality",
    "4K resolution",
    "smooth motion",
    "golden hour",
    "depth of field",
    "film grain",
]

# Example transformations
EXAMPLES: Dict[str, Tuple[str, str]] = {
    "wanita jalan di taman": (
        "wanita jalan di taman",
        "elegant woman in flowing dress walking through Japanese zen garden, cinematic lighting, smooth dolly shot, golden hour, 4K quality, shallow depth of field",
    ),
    "mobil di jalan": (
        "mobil di jalan",
        "sleek sports car cruising on coastal highway at dusk, cinematic tracking shot, dynamic lighting, lens flare, professional cinematography",
    ),
}


# ---------------------------------------------------------------------------
# PRE hook: Cinematic prompt rewriter
# ---------------------------------------------------------------------------
class CinematicPromptPreHook(PreHook):
    """Rewrite raw prompts to cinematic/professional quality."""

    name = "cinematic_rewrite"

    def run(self, ctx: InterceptContext) -> InterceptContext:
        prompt = ctx.kwargs.get("prompt", "")
        if not prompt:
            return ctx

        # Check if already high quality (has quality modifiers)
        quality_indicators = ["cinematic", "4k", "professional", "lighting", "dolly", "pan", "zoom"]
        already_enhanced = sum(1 for ind in quality_indicators if ind.lower() in prompt.lower()) >= 2

        if already_enhanced:
            logger.debug("[PROMPT PRE] Prompt already has quality modifiers, skipping enhancement")
            return ctx

        template = ENHANCEMENT_TEMPLATES.get(ctx.skill_type, ENHANCEMENT_TEMPLATES["default"])
        llm_prompt = f"{template}\n\nOriginal: {prompt}"

        enhanced = call_llm(llm_prompt)
        if enhanced and 10 < len(enhanced) <= 500:
            ctx.log("prompt_rewritten", {
                "original": prompt,
                "enhanced": enhanced,
                "skill_type": ctx.skill_type,
            })
            ctx.kwargs["prompt"] = enhanced
            logger.info("[PROMPT PRE] Rewritten: '%s' → '%s'", prompt[:60], enhanced[:60])
        return ctx


# ---------------------------------------------------------------------------
# PRE hook: Language normalization (Indonesian → English)
# ---------------------------------------------------------------------------
class LanguageNormalizationPreHook(PreHook):
    """Detect Indonesian prompts and translate to English for global models."""

    name = "language_normalize"

    # Common Indonesian words as detection heuristic
    INDONESIAN_WORDS = {
        "wanita", "pria", "anak", "gadis", "pemuda", "orang",
        "berjalan", "berlari", "duduk", "berdiri", "tersenyum",
        "di", "dengan", "yang", "dan", "atau", "dalam", "pada",
        "taman", "jalan", "rumah", "kota", "pantai", "gunung",
        "malam", "siang", "pagi", "sore", "langit", "hujan",
    }

    def _is_indonesian(self, text: str) -> bool:
        words = set(re.sub(r"[^a-zA-Z\s]", "", text.lower()).split())
        matches = words & self.INDONESIAN_WORDS
        return len(matches) >= 2

    def run(self, ctx: InterceptContext) -> InterceptContext:
        prompt = ctx.kwargs.get("prompt", "")
        if not prompt or not self._is_indonesian(prompt):
            return ctx

        llm_prompt = (
            "Translate this Indonesian AI generation prompt to English. "
            "Keep visual descriptors precise. Return ONLY the English translation.\n\n"
            f"Indonesian: {prompt}"
        )
        translated = call_llm(llm_prompt)
        if translated:
            ctx.log("language_translated", {"original": prompt, "translated": translated})
            ctx.kwargs["prompt"] = translated
            ctx.kwargs["_original_prompt_language"] = "id"
            logger.info("[PROMPT PRE] Translated ID→EN: %s → %s", prompt[:50], translated[:50])
        return ctx


# ---------------------------------------------------------------------------
# PRE hook: Negative prompt generation
# ---------------------------------------------------------------------------
class NegativePromptPreHook(PreHook):
    """Auto-generate negative prompts to avoid common quality issues."""

    name = "negative_prompt"

    DEFAULT_NEGATIVES: Dict[str, str] = {
        "kling_i2v": "blurry, shaky, low quality, pixelated, watermark, text overlay, duplicate frames",
        "kling_t2v": "blurry, distorted, unnatural motion, low quality, artifacts",
        "image_gen": "blurry, low quality, watermark, ugly, deformed, artifacts, noise",
        "default": "low quality, blurry, artifacts, watermark, distorted",
    }

    def run(self, ctx: InterceptContext) -> InterceptContext:
        # Only add negative prompt if not already set
        if ctx.kwargs.get("negative_prompt"):
            return ctx

        neg_prompt = self.DEFAULT_NEGATIVES.get(ctx.skill_type, self.DEFAULT_NEGATIVES["default"])
        ctx.kwargs["negative_prompt"] = neg_prompt
        ctx.log("negative_prompt_added", {"negative_prompt": neg_prompt})
        logger.debug("[PROMPT PRE] Added negative prompt for %s", ctx.skill_type)
        return ctx


# ---------------------------------------------------------------------------
# POST hook: Quality scoring of generated output
# ---------------------------------------------------------------------------
class ContentQualityScoringPostHook(PostHook):
    """Score generated content quality via LLM analysis."""

    name = "content_quality_score"

    SCORE_PROMPTS: Dict[str, str] = {
        "kling_i2v": "Rate this AI-generated video result on cinematic quality, motion smoothness, and visual appeal",
        "image_gen": "Rate this AI-generated image on composition, lighting, detail quality, and overall aesthetics",
        "default": "Rate this AI generation result on overall quality, accuracy to prompt, and professional appearance",
    }

    def run(self, ctx: InterceptContext, output: Any) -> Tuple[float, Any]:
        # If output contains a URL or file path, we can analyze it
        output_str = str(output)
        score_context = self.SCORE_PROMPTS.get(ctx.skill_type, self.SCORE_PROMPTS["default"])

        # Extract generation metadata for scoring
        generation_info = {}
        if isinstance(output, dict):
            generation_info = {
                "status": output.get("status", ""),
                "task_id": output.get("task_id", output.get("id", "")),
                "url": output.get("url", output.get("video_url", output.get("image_url", ""))),
            }

        if not generation_info.get("url") and not generation_info.get("task_id"):
            # Can't score without output reference
            return 7.0, output

        prompt_used = ctx.kwargs.get("prompt", "")
        llm_prompt = (
            f"{score_context} for prompt: '{prompt_used[:100]}'. "
            f"Output info: {str(generation_info)[:200]}. "
            f"Return JSON: {{\"score\": <0-10>, \"reason\": \"brief\", \"issues\": [\"...\"] }}"
        )

        data = call_llm_json(llm_prompt)
        score = float(data.get("score", 7.0))
        reason = data.get("reason", "")
        issues = data.get("issues", [])

        ctx.log("content_quality", {"score": score, "reason": reason, "issues": issues})
        logger.info("[PROMPT POST] Content quality: %.1f/10 — %s", score, reason)

        # Attach score metadata to output
        if isinstance(output, dict):
            output["_quality_score"] = score
            output["_quality_reason"] = reason
            if issues:
                output["_quality_issues"] = issues

        return score, output


# ---------------------------------------------------------------------------
# ERROR hook: Content policy violation → simplify prompt
# ---------------------------------------------------------------------------
class ContentPolicyErrorHook(ErrorHook):
    """Handle content policy violations by simplifying the prompt."""

    name = "content_policy_simplify"

    POLICY_KEYWORDS = [
        "content policy",
        "violation",
        "inappropriate",
        "not allowed",
        "cannot generate",
        "rejected",
        "nsfw",
        "banned",
    ]

    def run(self, ctx: InterceptContext, error: Exception) -> Optional[Any]:
        error_str = str(error).lower()
        if not any(kw in error_str for kw in self.POLICY_KEYWORDS):
            return None

        prompt = ctx.kwargs.get("prompt", "")
        if not prompt:
            return None

        llm_prompt = (
            "This AI generation prompt was rejected due to content policy. "
            "Rewrite it to be completely safe, family-friendly, and policy-compliant "
            "while preserving the core visual concept. "
            "Return ONLY the safe rewritten prompt.\n\n"
            f"Original: {prompt}"
        )
        safe_prompt = call_llm(llm_prompt)
        if safe_prompt:
            ctx.kwargs["prompt"] = safe_prompt
            ctx.log("prompt_policy_sanitized", {"original": prompt, "safe": safe_prompt})
            logger.info("[PROMPT ERROR] Sanitized policy-violating prompt: %s → %s", prompt[:50], safe_prompt[:50])

        return None  # Let retry happen with sanitized prompt


# ---------------------------------------------------------------------------
# ERROR hook: Prompt variation on quality failure
# ---------------------------------------------------------------------------
class PromptVariationErrorHook(ErrorHook):
    """Generate prompt variations on quality failures to try different approaches."""

    name = "prompt_variation"

    def run(self, ctx: InterceptContext, error: Exception) -> Optional[Any]:
        prompt = ctx.kwargs.get("prompt", "")
        if not prompt or ctx.attempt < 1:
            return None

        variation_styles = [
            "more dramatic and cinematic",
            "minimalist and clean",
            "vibrant and colorful",
            "dark and moody",
            "bright and uplifting",
        ]

        style = variation_styles[min(ctx.attempt - 1, len(variation_styles) - 1)]
        llm_prompt = (
            f"Create a variation of this AI generation prompt with a {style} style. "
            f"Keep the core subject. Return ONLY the new prompt.\n\nOriginal: {prompt}"
        )
        variation = call_llm(llm_prompt)
        if variation:
            ctx.kwargs["prompt"] = variation
            ctx.log("prompt_variation", {"original": prompt, "variation": variation, "style": style})
            logger.info("[PROMPT ERROR] Using %s variation: %s", style, variation[:60])

        return None  # Let retry happen


# ---------------------------------------------------------------------------
# Factory function
# ---------------------------------------------------------------------------
def create_prompt_interceptor(config_path: Optional[str] = None) -> AIInterceptor:
    """Create an AIInterceptor pre-loaded with prompt-specific hooks."""
    interceptor = AIInterceptor(config_path)

    skills = [
        "kling_i2v", "kling_t2v", "flow_i2v", "pixverse_i2v",
        "image_gen", "stable_diffusion", "midjourney",
        "grok_video", "sora_video",
    ]
    for skill in skills:
        interceptor.register_pre_hook(skill, LanguageNormalizationPreHook())
        interceptor.register_pre_hook(skill, CinematicPromptPreHook())
        interceptor.register_pre_hook(skill, NegativePromptPreHook())
        interceptor.register_post_hook(skill, ContentQualityScoringPostHook())
        interceptor.register_error_hook(skill, ContentPolicyErrorHook())
        interceptor.register_error_hook(skill, PromptVariationErrorHook())

    logger.info("Prompt interceptor initialized with cinematic hooks for %d skills", len(skills))
    return interceptor


_prompt_interceptor: Optional[AIInterceptor] = None


def get_prompt_interceptor(config_path: Optional[str] = None) -> AIInterceptor:
    global _prompt_interceptor
    if _prompt_interceptor is None:
        _prompt_interceptor = create_prompt_interceptor(config_path)
    return _prompt_interceptor


if __name__ == "__main__":
    # Demo: show enhancement
    interceptor = create_prompt_interceptor()

    @interceptor.intercept(skill_type="kling_i2v")
    def mock_kling(prompt: str, input_image: str = "") -> dict:
        return {"status": "submitted", "task_id": "demo_123", "prompt_used": prompt}

    result = mock_kling(prompt="wanita jalan di taman", input_image="photo.jpg")
    print("Result:", result)
