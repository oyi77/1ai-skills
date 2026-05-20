#!/usr/bin/env python3
"""
ContentGenerator — Main orchestrator for content-generator skill.

Wires together: LLM storyboard → NVIDIA image → BytePlus video → FFmpeg loop
Implements Larry Playbook viral formula for TikTok 9:16 1-minute videos.

Usage:
    from generator import ContentGenerator
    gen = ContentGenerator()
    result = await gen.generate(
        prompt="Landlord won't let me renovate, showed her AI kitchen redesign",
        platform="tiktok",
        template="larry_viral"
    )
    print(result["video"])  # Path to output MP4
"""

import asyncio
import base64
import json
import os
import ssl
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional

# ── CONFIG ──────────────────────────────────────────────────────────────────
NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "")
BYTEPLUS_API_KEY = os.environ.get("BYTEPLUS_API_KEY", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

NVIDIA_LLM_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
NVIDIA_IMAGE_URL = "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.1-dev"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

FFMPEG = "/home/linuxbrew/.linuxbrew/bin/ffmpeg"

OUTPUT_DIR = Path("output/videos")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR = Path("output/images")
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# BytePlus provider instance (uses AIProvider abstraction)
_byteplus_provider = None


def _get_byteplus_provider():
    global _byteplus_provider
    if _byteplus_provider is None:
        from providers.byteplus import BytePlusProvider

        _byteplus_provider = BytePlusProvider()
    return _byteplus_provider


# ── LARRY PLAYBOOK VIRAL PARAMS ─────────────────────────────────────────────
LARRY_HOOK_FORMULA = """
You are a viral TikTok content expert using Larry's proven formula (234K views).

FORMULA: [Third-party person's problem] + [Doubt/conflict] → [Showed them AI result] → [They reacted/changed mind]

✅ GOOD hooks (use these patterns):
- "My landlord said I can't change anything so I showed her what AI thinks it could look like"
- "My mum was skeptical about AI until I showed her this kitchen redesign"
- "My flatmate thinks renovating is impossible, so I proved them wrong with AI"

❌ BAD hooks (never use):
- "I built an app that does X"
- "Check out this cool AI feature"
- "Download now for amazing results"

CAPTION FORMAT (story style):
[Hook context — 1 line]
[Their reaction when I showed them the AI result]
[Subtle CTA, max 5 hashtags]
Max 200 characters, natural tone (NOT marketing-speak).
"""

VIRAL_CONCEPTS = {
    "landlord_kitchen": {
        "hook": "My landlord said I can't change anything so I showed her what AI thinks our kitchen could look like",
        "prompt": "A cozy rental kitchen transformed by AI interior design, photorealistic, warm lighting, modern style, 9:16 portrait, cinematic",
        "hashtags": "#interiordesign #rental #AI #transformation #landlord",
    },
    "parent_bedroom": {
        "hook": "My mum was skeptical about AI interior design until I showed her what it could do to her bedroom",
        "prompt": "A bedroom transformation, before and after AI redesign, warm cozy atmosphere, modern minimalist, 9:16 portrait",
        "hashtags": "#bedroom #interiordesign #AI #transformation #homedesign",
    },
    "motivation": {
        "hook": "Your only competition is yesterday's you",
        "prompt": "Cinematic motivational scene, person achieving goals, sunrise golden hour, smooth camera movement, 9:16 portrait, viral aesthetic",
        "hashtags": "#motivation #mindset #success #growth #viral",
    },
    "money": {
        "hook": "Money follows action not wishes",
        "prompt": "Abstract wealth visualization, flowing golden particles, professional atmosphere, smooth motion, 9:16 portrait, cinematic",
        "hashtags": "#money #wealth #entrepreneur #success #mindset",
    },
    "product": {
        "hook": "Premium product showcase",
        "prompt": "Premium product on elegant surface, studio lighting, slow zoom, professional photography style, 9:16 portrait",
        "hashtags": "#product #premium #quality #lifestyle #trending",
    },
}


# ── HTTP HELPERS ─────────────────────────────────────────────────────────────
def _post(url: str, payload: dict, headers: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    ssl_ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, context=ssl_ctx, timeout=120) as r:
        return json.loads(r.read())


def _get(url: str, headers: dict) -> dict:
    req = urllib.request.Request(url, headers=headers, method="GET")
    ssl_ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, context=ssl_ctx, timeout=30) as r:
        return json.loads(r.read())


def _download(url: str, path: Path, headers: Optional[dict] = None) -> Path:
    req = urllib.request.Request(url, headers=headers or {})
    ssl_ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, context=ssl_ctx, timeout=120) as r:
        path.write_bytes(r.read())
    return path


# ── LLM: Generate viral content ──────────────────────────────────────────────
def generate_content(concept: str) -> dict:
    """Generate viral hook + video prompt + caption via LLM."""
    api_key = NVIDIA_API_KEY or GROQ_API_KEY
    if not api_key:
        # Fallback to preset concept
        return VIRAL_CONCEPTS.get(concept, VIRAL_CONCEPTS["motivation"])

    base = VIRAL_CONCEPTS.get(concept, VIRAL_CONCEPTS["motivation"])
    user_prompt = f"""Based on this concept: "{base["hook"]}"

Create JSON with:
- "hook": Punchy headline (max 80 chars), following Larry's formula
- "video_prompt": Cinematic Seedance prompt (60-100 words), 9:16 portrait, smooth camera
- "caption": Story-style caption (150-200 chars), natural tone, with emojis
- "hashtags": 5 relevant hashtags as string

Return ONLY valid JSON."""

    url = GROQ_URL if GROQ_API_KEY else NVIDIA_LLM_URL
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    payload = {
        "model": (
            "llama-3.3-70b-versatile" if GROQ_API_KEY else "meta/llama-3.3-70b-instruct"
        ),
        "messages": [
            {"role": "system", "content": LARRY_HOOK_FORMULA},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.85,
        "max_tokens": 600,
    }

    try:
        resp = _post(url, payload, headers)
        text = resp["choices"][0]["message"]["content"]
        start, end = text.find("{"), text.rfind("}") + 1
        if start >= 0 and end > start:
            result = json.loads(text[start:end])
            result.setdefault("hashtags", base["hashtags"])
            return result
    except Exception as e:
        print(f"  ⚠️  LLM error: {e} — using preset")

    return base


# ── NVIDIA: Generate image ────────────────────────────────────────────────────
def generate_image(prompt: str, output_path: Optional[Path] = None) -> Optional[Path]:
    """Generate image via NVIDIA NIM Flux 1.1. Returns path to saved JPEG."""
    if not NVIDIA_API_KEY:
        return None

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Accept": "application/json",
    }
    try:
        resp = _post(NVIDIA_IMAGE_URL, {"prompt": prompt}, headers)
        artifacts = resp.get("artifacts", [])
        if not artifacts or artifacts[0].get("finishReason") != "SUCCESS":
            return None

        b64 = artifacts[0].get("base64", "")
        if not b64:
            return None

        path = output_path or IMAGES_DIR / f"img_{int(time.time())}.jpg"
        path.write_bytes(base64.b64decode(b64))
        return path
    except Exception as e:
        print(f"  ⚠️  NVIDIA image error: {e}")
        return None


# ── BYTEPLUS: Generate video via AIProvider abstraction ──────────────────────
async def generate_video(
    prompt: str, ratio: str = "9:16", image_url: Optional[str] = None
) -> Optional[str]:
    """
    Generate video via BytePlus Seedance. Returns video URL.
    Delegates to BytePlusProvider from the providers module.
    """
    provider = _get_byteplus_provider()
    result = await provider.generate(
        prompt,
        image_url=image_url,
        ratio=ratio,
    )
    if result.success:
        return result.data.get("video_url")
    print(f"  ❌ BytePlus error: {result.metadata.get('error')}")
    return None

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {BYTEPLUS_API_KEY}",
    }

    # Build content array
    content = [{"type": "text", "text": prompt}]
    if image_url:
        content.append(
            {
                "type": "image_url",
                "image_url": {"url": image_url},
                "role": "first_frame",
            }
        )

    # Create task (no "resolution" — causes 400 on lite model)
    payload = {
        "model": SEEDANCE_MODEL,
        "content": content,
        "ratio": ratio,
    }

    try:
        resp = _post(
            f"{BYTEPLUS_BASE_URL}/contents/generations/tasks", payload, headers
        )
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else str(e)
        print(f"  ❌ BytePlus create task HTTP {e.code}: {body[:200]}")
        return None

    task_id = resp.get("id")
    if not task_id:
        print(f"  ❌ No task_id: {resp}")
        return None

    print(f"  📋 Task: {task_id}")

    # Poll
    deadline = time.time() + 300
    attempt = 0
    while time.time() < deadline:
        attempt += 1
        time.sleep(5)
        try:
            result = _get(
                f"{BYTEPLUS_BASE_URL}/contents/generations/tasks/{task_id}", headers
            )
        except Exception as e:
            print(f"  ⚠️  Poll error: {e}")
            continue

        status = result.get("status", "")
        print(f"  [{attempt:02d}] {status}")

        if status == "succeeded":
            return result.get("content", {}).get("video_url")
        elif status in ("failed", "cancelled"):
            err = result.get("error", {})
            print(f"  ❌ {status}: {err.get('message')} (code: {err.get('code')})")
            return None

    print("  ❌ Timeout")
    return None


# ── FFMPEG: Loop to 1 minute ─────────────────────────────────────────────────
def loop_to_minute(
    input_path: Path, output_path: Path, target_secs: int = 60, loops: int = 12
) -> Optional[Path]:
    """Loop clip to target_secs via FFmpeg -stream_loop. Returns output path."""
    cmd = [
        FFMPEG,
        "-stream_loop",
        str(loops),
        "-i",
        str(input_path),
        "-c",
        "copy",
        "-t",
        str(target_secs),
        "-y",
        str(output_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ❌ FFmpeg loop error: {result.stderr[-200:]}")
        return None
    return output_path


# ── FFMPEG: Compress for Telegram ────────────────────────────────────────────
def compress_video(
    input_path: Path, output_path: Path, crf: int = 28
) -> Optional[Path]:
    """Re-encode video with CRF for smaller filesize."""
    cmd = [
        FFMPEG,
        "-i",
        str(input_path),
        "-c:v",
        "libx264",
        "-crf",
        str(crf),
        "-preset",
        "fast",
        "-c:a",
        "copy",
        "-y",
        str(output_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ❌ FFmpeg compress error: {result.stderr[-200:]}")
        return None
    return output_path


# ── MAIN ORCHESTRATOR ─────────────────────────────────────────────────────────
class ContentGenerator:
    """
    Main content generator orchestrator.

    Pipeline:
      1. generate_content()  — LLM generates hook + video prompt + caption
      2. generate_image()    — NVIDIA Flux creates reference image (optional)
      3. generate_video()    — BytePlus Seedance T2V creates 5s clip
      4. loop_to_minute()    — FFmpeg loops 5s × 12 = 60s
      5. compress_video()    — FFmpeg CRF 28 compression (44MB → 8.6MB)
    """

    def __init__(self, config_path: str = "config.yaml"):
        self.output_dir = OUTPUT_DIR
        self.images_dir = IMAGES_DIR
        self.config_path = config_path

    async def generate(
        self,
        prompt: Optional[str] = None,
        concept: str = "motivation",
        platform: str = "tiktok",
        template: str = "larry_viral",
        ratio: str = "9:16",
        target_duration: int = 60,
        skip_image: bool = True,
        compress: bool = True,
        output_name: Optional[str] = None,
    ) -> dict:
        """
        Generate a TikTok viral video.

        Args:
            prompt: Custom prompt (overrides concept)
            concept: Preset concept key from VIRAL_CONCEPTS
            platform: Target platform (tiktok, youtube, etc.)
            template: Content template (larry_viral, ad_short, etc.)
            ratio: Video aspect ratio (9:16 for TikTok)
            target_duration: Target video duration in seconds (default 60)
            skip_image: Skip NVIDIA image generation step
            compress: Compress output video (CRF 28)
            output_name: Custom output filename stem

        Returns:
            dict with keys: video, image, hook, caption, hashtags, cost
        """
        ts = int(time.time())
        name = output_name or f"{concept}_{ts}"
        result = {"success": False, "concept": concept, "platform": platform}

        print(f"\n🚀 ContentGenerator — {template} / {concept} / {platform}")
        print("=" * 60)

        # ── Step 1: LLM content ──────────────────────────────────────
        print("\n🤖 Step 1: Generating viral content...")
        content = generate_content(concept)
        video_prompt = (
            prompt or content.get("video_prompt") or content.get("prompt", "")
        )
        result["hook"] = content.get("hook", "")
        result["caption"] = content.get("caption", "")
        result["hashtags"] = content.get("hashtags", "")
        print(f"  Hook: {result['hook'][:60]}")
        print(f"  Prompt: {video_prompt[:60]}...")

        # ── Step 2: Image (optional) ─────────────────────────────────
        if not skip_image:
            print("\n🎨 Step 2: Generating image...")
            img_path = generate_image(video_prompt, IMAGES_DIR / f"{name}.jpg")
            result["image"] = str(img_path) if img_path else None
            if img_path:
                print(f"  ✅ Image: {img_path} ({img_path.stat().st_size:,}B)")
        else:
            result["image"] = None

        # ── Step 3: Video (BytePlus Seedance) ───────────────────────
        print(f"\n🎬 Step 3: Generating video (ratio={ratio})...")
        video_url = generate_video(video_prompt, ratio=ratio)
        if not video_url:
            result["error"] = "Video generation failed"
            return result

        # ── Step 4: Download ─────────────────────────────────────────
        print(f"\n⬇️  Step 4: Downloading clip...")
        clip_path = OUTPUT_DIR / f"{name}_clip.mp4"
        _download(video_url, clip_path)
        clip_size = clip_path.stat().st_size
        print(
            f"  ✅ Clip: {clip_path} ({clip_size:,}B / {clip_size / 1024 / 1024:.1f}MB)"
        )

        # ── Step 5: Loop to target duration ─────────────────────────
        loops = target_duration // 5
        final_path = OUTPUT_DIR / f"{name}_looped.mp4"
        print(f"\n🔄 Step 5: Looping {loops}× to {target_duration}s...")
        looped = loop_to_minute(clip_path, final_path, target_duration, loops)
        if not looped:
            # Use raw clip as fallback
            final_path = clip_path
            print("  ⚠️  Loop failed — using raw clip")
        else:
            print(f"  ✅ Looped: {final_path.stat().st_size / 1024 / 1024:.1f}MB")

        # ── Step 6: Compress ─────────────────────────────────────────
        if compress:
            compressed_path = OUTPUT_DIR / f"{name}_final.mp4"
            print(f"\n📦 Step 6: Compressing (CRF 28)...")
            compressed = compress_video(final_path, compressed_path)
            if compressed:
                sz = compressed_path.stat().st_size
                print(f"  ✅ Compressed: {sz:,}B ({sz / 1024 / 1024:.1f}MB)")
                final_path = compressed_path
            else:
                print("  ⚠️  Compression failed — using uncompressed")

        result.update(
            {
                "success": True,
                "video": str(final_path),
                "video_url": video_url,
                "duration": target_duration,
                "ratio": ratio,
            }
        )

        print(f"\n✅ DONE — {final_path}")
        print("=" * 60)
        return result


# ── CLI WRAPPER ───────────────────────────────────────────────────────────────
async def main():
    import argparse

    parser = argparse.ArgumentParser(description="Content Generator")
    parser.add_argument(
        "--concept", default="motivation", choices=list(VIRAL_CONCEPTS.keys())
    )
    parser.add_argument("--prompt", default=None)
    parser.add_argument("--ratio", default="9:16")
    parser.add_argument("--duration", type=int, default=60)
    parser.add_argument("--no-compress", action="store_true")
    parser.add_argument("--with-image", action="store_true")
    args = parser.parse_args()

    gen = ContentGenerator()
    result = await gen.generate(
        prompt=args.prompt,
        concept=args.concept,
        ratio=args.ratio,
        target_duration=args.duration,
        skip_image=not args.with_image,
        compress=not args.no_compress,
    )

    print(json.dumps(result, indent=2))

    if result.get("success"):
        print(f"\n🎬 Video ready: {result['video']}")


if __name__ == "__main__":
    asyncio.run(main())
