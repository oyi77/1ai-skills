"""
Veris Design System — Extracted from Veris (Ads Master, 10+ years) training session.
Enforces dark theme, minimalist aesthetic, Instagram-first approach.

Design principles:
- Pure black background (#000000) — no exceptions
- High contrast white text — nothing below 60% opacity
- Three-zone vertical layout: Hook / Body / CTA
- No vibrant colors, no emoji in visuals
- Minimalist premium aesthetic — less is more
- Instagram-first sizing, then adapt for other platforms
"""

from __future__ import annotations

# ── Color Palette ─────────────────────────────────────────────────────────────

VERIS_PALETTE = {
    "bg_primary": "#000000",  # Pure black — mandatory background
    "bg_secondary": "#000020",  # Very dark navy — secondary backgrounds
    "text_primary": "#FFFFFF",  # Pure white — headlines & primary copy
    "text_secondary": "#808080",  # Mid-grey — supporting text
    "accent_trust": "#202040",  # Dark indigo — trust signals, borders
    "accent_urgency": "#200000",  # Very dark red — urgency, scarcity
    "accent_soft": "#606080",  # Muted slate — decorative elements
}

# ── Canvas Formats ─────────────────────────────────────────────────────────────

VERIS_FORMATS = {
    "instagram_portrait": {"width": 1024, "height": 1280, "ratio": "4:5"},  # PRIMARY
    "instagram_feed": {"width": 800, "height": 800, "ratio": "1:1"},
    "tiktok": {"width": 1080, "height": 1920, "ratio": "9:16"},
}

# ── Three-Zone Layout ─────────────────────────────────────────────────────────

VERIS_LAYOUT = {
    "hook_zone": "top 20-30%",  # Headline — first thing eyes land on
    "body_zone": "middle 40-50%",  # Product detail — builds desire
    "cta_zone": "bottom 20-30%",  # Action button — converts
}

# ── Platform Priority (Veris approach) ────────────────────────────────────────

PLATFORM_PRIORITY = [
    "instagram",  # PRIMARY — where ads convert
    "facebook",  # SECONDARY — older audience
    "threads",  # TERTIARY — IG companion
    "tiktok",  # QUATERNARY — volume play
]

# ── Prompt Builders ───────────────────────────────────────────────────────────


def build_veris_prompt(
    product_name: str,
    hook_text: str,
    style: str = "Photorealistic",
) -> dict:
    """
    Build a GeminiGen API-compatible prompt following Veris design principles.

    Args:
        product_name: The product being promoted (e.g. "Guru Pintar AI")
        hook_text: The attention-grabbing headline (e.g. "Bisa Cuan Rp 1 Juta/Hari?")
        style: GeminiGen style parameter (default: "Photorealistic")

    Returns:
        dict ready to unpack into GeminiGenClient.generate_image(**payload)
    """
    prompt = f"""Professional dark themed product promotional image.
Pure black background (#000000). White bold text overlay.
Three-section vertical layout:
- Top: Hook headline "{hook_text}" in large bold white text
- Middle: Product description for {product_name}
- Bottom: CTA box with bordered frame, price and action button
Minimalist, premium aesthetic. No vibrant colors. No emoji.
Instagram-ready vertical format. High contrast. Clean modern sans-serif typography."""

    return {
        "prompt": prompt,
        "model": "nano-banana-pro",
        "aspect_ratio": "3:4",
        "style": style,
        "output_format": "png",
        "resolution": "1K",
    }


def build_video_prompt(
    product_name: str,
    hook: str,
    duration: int = 6,
) -> dict:
    """
    Build a GeminiGen Grok video prompt following Veris design principles.

    Args:
        product_name: The product being promoted
        hook: Opening hook text shown on screen
        duration: Video duration in seconds (default: 6)

    Returns:
        dict ready to unpack into GeminiGenClient.generate_video_grok(**payload)
    """
    prompt = f"""Professional product showcase video for {product_name}.
Dark theme, modern tech aesthetic.
Opening: Bold text "{hook}" appears on black background.
Middle: Product features shown with smooth transitions.
Ending: CTA with product name and price.
Clean, premium, no flashy effects."""

    return {
        "prompt": prompt,
        "model": "grok-3",
        "resolution": "480p",
        "aspect_ratio": "portrait",
        "duration": duration,
        "mode": "custom",
    }


def veris_prompt_for_platform(
    product_name: str,
    hook_text: str,
    platform: str = "instagram",
    style: str = "Photorealistic",
) -> dict:
    """
    Build a Veris prompt tailored for a specific platform format.

    Args:
        product_name: Product being promoted
        hook_text: Hook headline
        platform: Target platform ("instagram", "tiktok", "facebook", etc.)
        style: Image generation style

    Returns:
        GeminiGen API payload dict with platform-appropriate aspect_ratio
    """
    platform = platform.lower()
    payload = build_veris_prompt(product_name, hook_text, style)

    # Override aspect ratio based on platform
    if platform in ("tiktok", "youtube", "reels"):
        payload["aspect_ratio"] = "9:16"
    elif platform in ("instagram", "facebook", "threads"):
        payload["aspect_ratio"] = "3:4"  # 4:5 portrait — Instagram sweet spot
    # 1:1 square: keep default 3:4 (GeminiGen will crop; IG square can use portrait)

    return payload
