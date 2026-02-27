"""
Hyperrealistic Defaults — Global Settings
Updated: 2026-02-27
Apply these to ALL future video/image generation projects.
"""

# ─── IMAGE GENERATION (NVIDIA Flux) ──────────────────────────────────
IMAGE_QUALITY_SUFFIX = (
    ", hyperrealistic, photorealistic, shot on Sony A7III, 85mm f/1.8 lens, "
    "8K ultra detailed, RAW photo, professional photography, sharp focus, "
    "cinematic color grading, film grain, ultra high resolution"
)

IMAGE_NEGATIVE = (
    "cartoon, anime, illustration, painting, drawing, CGI, 3D render, "
    "blurry, low quality, watermark, text, logo, oversaturated, fake"
)

# Best model for photorealistic
# ⚠️ Flux.1-dev → CONTENT_FILTERED for human portrait scenes
# Use SD3 Medium for scenes with people, Flux for objects/abstract
IMAGE_MODEL_ABSTRACT = "black-forest-labs/flux.1-dev"          # Objects, abstract, no people
IMAGE_MODEL_PORTRAIT  = "stabilityai/stable-diffusion-3-medium"  # Scenes with people/faces
IMAGE_MODEL = IMAGE_MODEL_PORTRAIT  # Default: SD3 (safer for human scenes)

# API response format differs:
# Flux → response["artifacts"][0]["base64"]
# SD3  → response["image"]

def enhance_image_prompt(prompt: str) -> str:
    """Append hyperrealistic suffix to any image prompt."""
    return prompt.rstrip("., ") + IMAGE_QUALITY_SUFFIX


# ─── VIDEO GENERATION (BytePlus Seedance) ────────────────────────────
# Pro model = significantly higher quality than Lite
VIDEO_MODEL_T2V = "seedance-1-0-pro-250528"      # Text-to-Video Pro
VIDEO_MODEL_I2V = "seedance-1-0-pro-i2v-250528"  # Image-to-Video Pro
VIDEO_MODEL_I2V_FALLBACK = "seedance-1-0-lite-i2v-250428"  # Fallback if Pro unavailable

VIDEO_ANIM_SUFFIX = (
    ", ultra smooth cinematic motion, photorealistic movement, "
    "professional camera work, shallow depth of field, natural lighting"
)

def enhance_anim_prompt(prompt: str) -> str:
    """Append hyperrealistic animation suffix to I2V prompt."""
    return prompt.rstrip("., ") + VIDEO_ANIM_SUFFIX


# ─── VOICEOVER (Edge TTS) ────────────────────────────────────────────
# Natural-sounding Indonesian voices
VOICE_ID = "id-ID-GadisNeural"       # Female, warm (default)
VOICE_MALE = "id-ID-ArdiNeural"      # Male alternative
VOICE_RATE = "+5%"                    # Slightly faster = more natural


# ─── FFMPEG / POST-PROCESSING ────────────────────────────────────────
# Higher quality encoding
VIDEO_CRF = 18          # Lower = better quality (was 22)
VIDEO_PRESET = "slow"   # Better compression quality (was "fast")
VIDEO_BITRATE = "4M"    # Higher bitrate for detail retention

# Color grading preset (cinematic)
COLOR_GRADE = "curves=vintage"


# ─── PROMPT TEMPLATES (Scene-type based) ─────────────────────────────
SCENE_PROMPTS = {
    "creator_desk_night": (
        "young asian male content creator sitting at desk late at night, "
        "tired but focused expression, MacBook Pro screen glow illuminating face, "
        "messy desk with sticky notes and coffee cup, bokeh background, "
        "moody blue-orange lighting, ultra detailed skin texture"
    ),
    "hands_keyboard": (
        "close-up of hands typing on mechanical keyboard, "
        "video editing timeline visible on monitor, coffee steam rising, "
        "dramatic side lighting, shallow depth of field f/1.4, "
        "ultra detailed finger texture, cinematic color grade"
    ),
    "creator_upload": (
        "young asian content creator smiling looking at smartphone, "
        "instagram/tiktok upload complete screen visible, "
        "warm golden hour window light, natural skin tone, "
        "candid moment, Sony A7IV 85mm portrait, film grain"
    ),
    "product_shot": (
        "professional product photography, studio lighting setup, "
        "white cyclorama background, reflection surface, "
        "ultra sharp focus, commercial grade photo, 8K resolution"
    ),
}


# ─── USAGE EXAMPLE ───────────────────────────────────────────────────
"""
from hyperrealistic_defaults import enhance_image_prompt, enhance_anim_prompt, IMAGE_MODEL, VIDEO_MODEL_I2V

# Generate image
prompt = enhance_image_prompt("creator at desk at night, tired eyes, laptop glow")
# → "creator at desk at night, tired eyes, laptop glow, hyperrealistic, photorealistic, 
#    shot on Sony A7III, 85mm f/1.8 lens, 8K ultra detailed..."

# Generate I2V
anim = enhance_anim_prompt("slow breathing movement, laptop screen flickering")
# → "slow breathing movement, laptop screen flickering, ultra smooth cinematic motion,
#    photorealistic movement, professional camera work..."

# Use Pro model
model = VIDEO_MODEL_I2V  # "seedance-1-0-pro-i2v-250528"
"""
