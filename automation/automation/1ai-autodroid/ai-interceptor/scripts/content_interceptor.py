"""
content_interceptor.py — PostBridge / Social Media Content Interceptor
=======================================================================
Specialized interceptor for social media content posting via PostBridge.

PRE hooks:
  - AI caption enhancement (hook + proof + CTA + hashtags)
  - Platform compliance (media required for Instagram/TikTok/YouTube)

POST hooks:
  - Verify post succeeded via API response (check status field)

ERROR hooks:
  - Missing media → auto-attach placeholder → retry
  - API rate limit → backoff → retry
"""

from __future__ import annotations

import logging
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from ai_interceptor import (
    AIInterceptor,
    ErrorHook,
    InterceptContext,
    PostHook,
    PreHook,
    call_llm,
    call_llm_json,
)

logger = logging.getLogger("content_interceptor")

# ---------------------------------------------------------------------------
# Platform media requirements (from TOOLS.md)
# ---------------------------------------------------------------------------
PLATFORM_REQUIRES_MEDIA: Dict[str, bool] = {
    "youtube": True,
    "instagram": True,
    "tiktok": True,
    "threads": False,
    "facebook": False,
    "twitter": False,
    "linkedin": False,
    "bluesky": False,
}

PLATFORM_VIDEO_ONLY: Set[str] = {"youtube"}
PLATFORM_NO_TEXT_ONLY: Set[str] = {"instagram", "tiktok", "youtube"}

# PostBridge account IDs by platform (from TOOLS.md)
YOUTUBE_ACCTS: Set[int] = {49678}
INSTAGRAM_ACCTS: Set[int] = {49682, 49676}
THREADS_ACCTS: Set[int] = {49683, 49680, 49677}
FACEBOOK_ACCTS: Set[int] = {49675, 49674, 49673, 49672}


def get_platform_for_account(account_id: int) -> str:
    if account_id in YOUTUBE_ACCTS:
        return "youtube"
    if account_id in INSTAGRAM_ACCTS:
        return "instagram"
    if account_id in THREADS_ACCTS:
        return "threads"
    if account_id in FACEBOOK_ACCTS:
        return "facebook"
    return "unknown"


# ---------------------------------------------------------------------------
# PRE hook: Caption enhancement
# ---------------------------------------------------------------------------
class EnhanceCaptionPreHook(PreHook):
    """Enhance captions with hook, proof, CTA, and hashtags via LLM."""

    name = "enhance_caption"

    # Platform-specific styles
    PLATFORM_STYLES: Dict[str, str] = {
        "tiktok": "TikTok style — short punchy hook, emojis, trending hashtags, viral CTA",
        "instagram": "Instagram style — aesthetic, story-driven, lifestyle hashtags",
        "youtube": "YouTube style — searchable keywords, value-driven description",
        "facebook": "Facebook style — conversational, shareable, community-focused",
        "threads": "Threads style — conversational, witty, relatable",
        "linkedin": "LinkedIn style — professional, insight-driven, industry hashtags",
    }

    def run(self, ctx: InterceptContext) -> InterceptContext:
        caption = ctx.kwargs.get("caption", ctx.kwargs.get("text", ""))
        if not caption:
            return ctx

        # Detect platform from accounts
        social_accounts = ctx.kwargs.get("social_accounts", [])
        platforms = set()
        for acct_id in (social_accounts if isinstance(social_accounts, list) else []):
            platforms.add(get_platform_for_account(int(acct_id)))

        platform_hint = ", ".join(p for p in platforms if p != "unknown") or "social media"
        style_hints = " | ".join(self.PLATFORM_STYLES.get(p, "") for p in platforms if p in self.PLATFORM_STYLES)

        llm_prompt = (
            f"You are a viral social media copywriter. Enhance this caption for {platform_hint}.\n"
            f"Requirements: strong hook (first line), social proof, clear CTA, relevant hashtags.\n"
            f"Style: {style_hints or 'engaging and viral'}\n"
            f"Keep under 500 characters total. Return ONLY the enhanced caption.\n\n"
            f"Original caption:\n{caption}"
        )

        enhanced = call_llm(llm_prompt)
        if enhanced and len(enhanced) <= 1000:
            ctx.log("caption_enhanced", {
                "original": caption[:100],
                "enhanced": enhanced[:100],
                "platforms": list(platforms),
            })
            # Update caption/text field
            if "caption" in ctx.kwargs:
                ctx.kwargs["caption"] = enhanced
            if "text" in ctx.kwargs:
                ctx.kwargs["text"] = enhanced
            logger.info("[CONTENT PRE] Caption enhanced for %s", platform_hint)
        return ctx


# ---------------------------------------------------------------------------
# PRE hook: Platform compliance validation
# ---------------------------------------------------------------------------
class PlatformCompliancePreHook(PreHook):
    """Validate platform requirements: media, format, etc."""

    name = "platform_compliance"

    def run(self, ctx: InterceptContext) -> InterceptContext:
        social_accounts = ctx.kwargs.get("social_accounts", [])
        media = ctx.kwargs.get("media", ctx.kwargs.get("media_ids", []))
        has_media = bool(media)
        media_type = ctx.kwargs.get("media_type", "unknown")

        removed_accounts = []
        valid_accounts = []

        for acct_id in (social_accounts if isinstance(social_accounts, list) else []):
            acct_id = int(acct_id)
            platform = get_platform_for_account(acct_id)

            # YouTube: requires video media
            if platform == "youtube":
                if not has_media or media_type == "image":
                    logger.warning("[CONTENT PRE] Removing YouTube account %d: requires video media", acct_id)
                    removed_accounts.append(acct_id)
                    continue

            # Instagram/TikTok: requires any media
            if platform in PLATFORM_NO_TEXT_ONLY:
                if not has_media:
                    logger.warning("[CONTENT PRE] Removing %s account %d: requires media", platform, acct_id)
                    removed_accounts.append(acct_id)
                    continue

            valid_accounts.append(acct_id)

        if removed_accounts:
            ctx.kwargs["social_accounts"] = valid_accounts
            ctx.kwargs["_removed_accounts"] = removed_accounts
            ctx.log("compliance_filter", {
                "removed": removed_accounts,
                "remaining": valid_accounts,
                "reason": "platform_media_requirement",
            })
            logger.info("[CONTENT PRE] Filtered %d accounts due to platform compliance", len(removed_accounts))

        # Warn if no accounts remain
        if not valid_accounts:
            logger.error("[CONTENT PRE] No valid accounts remaining after compliance filter!")
            ctx.kwargs["_no_valid_accounts"] = True

        return ctx


# ---------------------------------------------------------------------------
# POST hook: Verify post succeeded
# ---------------------------------------------------------------------------
class VerifyPostSuccessPostHook(PostHook):
    """Check API response to verify the post was successfully created."""

    name = "verify_post_success"

    def run(self, ctx: InterceptContext, output: Any) -> Tuple[float, Any]:
        if not isinstance(output, dict):
            logger.debug("[CONTENT POST] Output is not a dict, skipping verification")
            return 7.0, output

        # Check for success indicators
        status = output.get("status", "")
        post_id = output.get("id", output.get("post_id", ""))
        errors = output.get("errors", output.get("error", ""))

        if errors:
            ctx.log("post_failed", {"errors": str(errors)})
            logger.error("[CONTENT POST] Post has errors: %s", errors)
            return 2.0, output

        if post_id and (status in ["scheduled", "published", "pending", "success", "created"]):
            ctx.log("post_verified", {"status": status, "post_id": str(post_id)})
            logger.info("[CONTENT POST] Post verified: id=%s status=%s", post_id, status)
            return 9.0, output

        if status in ["failed", "error"]:
            ctx.log("post_failed", {"status": status})
            logger.error("[CONTENT POST] Post status: %s", status)
            return 1.0, output

        # Unknown status — moderate score
        logger.debug("[CONTENT POST] Unknown post status: %s", status)
        return 6.0, output


# ---------------------------------------------------------------------------
# ERROR hook: Missing media → attempt auto-attach
# ---------------------------------------------------------------------------
class MissingMediaErrorHook(ErrorHook):
    """When missing media error detected, attempt to find and attach media."""

    name = "missing_media_recovery"

    MEDIA_ERROR_KEYWORDS = [
        "no supported media",
        "media required",
        "missing media",
        "no media",
        "media not found",
    ]

    def run(self, ctx: InterceptContext, error: Exception) -> Optional[Any]:
        error_str = str(error).lower()

        if not any(kw in error_str for kw in self.MEDIA_ERROR_KEYWORDS):
            return None

        logger.warning("[CONTENT ERROR] Missing media error detected — attempting recovery")

        # Check if there's a default media path configured
        default_media = ctx.config.get("default_media_path", "")
        if not default_media:
            default_media = ctx.kwargs.get("_fallback_media", "")

        if default_media and Path(default_media).exists():
            ctx.kwargs["media"] = [default_media]
            ctx.kwargs["media_ids"] = []
            ctx.log("media_recovered", {"media_path": default_media})
            logger.info("[CONTENT ERROR] Attached fallback media: %s", default_media)
        else:
            # Remove accounts that require media
            social_accounts = ctx.kwargs.get("social_accounts", [])
            accounts_no_media_req = [
                a for a in social_accounts
                if get_platform_for_account(int(a)) not in PLATFORM_NO_TEXT_ONLY
            ]
            if accounts_no_media_req != social_accounts:
                ctx.kwargs["social_accounts"] = accounts_no_media_req
                ctx.log("accounts_filtered_no_media", {
                    "before": len(social_accounts),
                    "after": len(accounts_no_media_req),
                })
                logger.info("[CONTENT ERROR] Filtered to %d media-optional accounts", len(accounts_no_media_req))

        return None  # Let retry happen


# ---------------------------------------------------------------------------
# ERROR hook: Rate limit backoff
# ---------------------------------------------------------------------------
class RateLimitBackoffErrorHook(ErrorHook):
    """Handle API rate limit errors with exponential backoff."""

    name = "rate_limit_backoff"

    RATE_LIMIT_KEYWORDS = ["rate limit", "too many requests", "429", "quota exceeded"]

    def run(self, ctx: InterceptContext, error: Exception) -> Optional[Any]:
        error_str = str(error).lower()
        if not any(kw in error_str for kw in self.RATE_LIMIT_KEYWORDS):
            return None

        backoff = 5 * (2 ** ctx.attempt)  # 5s, 10s, 20s
        logger.warning("[CONTENT ERROR] Rate limit hit — backing off %ds", backoff)
        ctx.log("rate_limit_backoff", {"backoff_seconds": backoff, "attempt": ctx.attempt})
        time.sleep(backoff)
        return None  # Let retry happen


# ---------------------------------------------------------------------------
# Factory function
# ---------------------------------------------------------------------------
def create_content_interceptor(config_path: Optional[str] = None) -> AIInterceptor:
    """Create an AIInterceptor pre-loaded with content/PostBridge-specific hooks."""
    interceptor = AIInterceptor(config_path)

    skills = ["postbridge_post", "social_media_post", "content_post", "schedule_post"]
    for skill in skills:
        interceptor.register_pre_hook(skill, EnhanceCaptionPreHook())
        interceptor.register_pre_hook(skill, PlatformCompliancePreHook())
        interceptor.register_post_hook(skill, VerifyPostSuccessPostHook())
        interceptor.register_error_hook(skill, MissingMediaErrorHook())
        interceptor.register_error_hook(skill, RateLimitBackoffErrorHook())

    logger.info("Content interceptor initialized with PostBridge hooks")
    return interceptor


_content_interceptor: Optional[AIInterceptor] = None


def get_content_interceptor(config_path: Optional[str] = None) -> AIInterceptor:
    global _content_interceptor
    if _content_interceptor is None:
        _content_interceptor = create_content_interceptor(config_path)
    return _content_interceptor


if __name__ == "__main__":
    interceptor = create_content_interceptor()
    print("Content interceptor hooks:", list(interceptor._pre_hooks.keys()))
