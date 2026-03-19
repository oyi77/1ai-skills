"""
Multi-provider media generator with fallback chain.

Image: NVIDIA (Flux) -> Gemini (nano-banana-pro) -> BytePlus (Seedance still)
Video: Gemini (GenAI) -> BytePlus (Seedance)

Each provider is tried in order. On failure, falls back to next.
"""
import json
import logging
import os
import ssl
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional

log = logging.getLogger("ContentKingdom.MediaGen")

WORKSPACE = Path("/home/openclaw/.openclaw/workspace")


# -- API Keys -----------------------------------------------------------------
def _env(key: str, fallback: str = "") -> str:
    return os.environ.get(key, fallback)


def _nvidia_key() -> str:
    return _env("NVIDIA_API_KEY",
                "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")


def _gemini_key() -> str:
    return _env("GEMINI_API_KEY",
                "AIzaSyAy2BsciB9KFy67qVx-8MLvu3ZvdBKCCww")


def _byteplus_key() -> str:
    return _env("BYTEPLUS_API_KEY",
                "cac5cfc1-e30f-47bb-b8b8-e861ffda28ea")


# -- NVIDIA Image Generation ---------------------------------------------------
def generate_image_nvidia(prompt: str, output_path: str,
                          model: str = "black-forest-labs/flux.1-dev") -> bool:
    """Generate image via NVIDIA NIM API (Flux)."""
    api_key = _nvidia_key()
    if not api_key:
        log.warning("NVIDIA: no API key")
        return False

    url = f"https://ai.api.nvidia.com/v1/genai/{model}"
    payload = json.dumps({
        "prompt": prompt,
        "cfg_scale": 5,
        "aspect_ratio": "9:16",
        "output_format": "png",
    }).encode()

    req = urllib.request.Request(url, data=payload, method="POST", headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    })

    try:
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
            data = json.loads(resp.read())
            artifacts = data.get("artifacts", [])
            if artifacts:
                import base64
                img_data = base64.b64decode(artifacts[0].get("base64", ""))
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                Path(output_path).write_bytes(img_data)
                log.info("NVIDIA: image saved to %s", output_path)
                return True
            log.warning("NVIDIA: no artifacts in response")
            return False
    except Exception as e:
        log.warning("NVIDIA: %s", e)
        return False


# -- Gemini Image Generation (nano-banana-pro) ---------------------------------
def generate_image_gemini(prompt: str, output_path: str) -> bool:
    """Generate image via Gemini (nano-banana-pro script)."""
    script = WORKSPACE / "skills" / "nano-banana-pro" / "scripts" / "generate_image.py"
    if not script.exists():
        log.warning("Gemini: script not found at %s", script)
        return False

    api_key = _gemini_key()
    env = {**os.environ, "GEMINI_API_KEY": api_key}

    try:
        result = subprocess.run(
            ["uv", "run", str(script),
             "--prompt", prompt,
             "--filename", output_path,
             "--resolution", "1K"],
            capture_output=True, text=True, timeout=120,
            env=env, cwd=str(script.parent)
        )
        if result.returncode == 0 and Path(output_path).exists():
            log.info("Gemini: image saved to %s", output_path)
            return True
        log.warning("Gemini: exit %d: %s", result.returncode, result.stderr[:200])
        return False
    except Exception as e:
        log.warning("Gemini: %s", e)
        return False


# -- BytePlus Video Generation (Seedance) --------------------------------------
def generate_video_byteplus(prompt: str, output_path: str,
                            model: str = "seedance-1-0-lite-t2v-250428") -> bool:
    """Generate video via BytePlus Seedance API."""
    api_key = _byteplus_key()
    if not api_key:
        log.warning("BytePlus: no API key")
        return False

    base_url = "https://ark.ap-southeast.bytepluses.com/api/v3"
    payload = json.dumps({
        "model": model,
        "content": [{"type": "text", "text": prompt}],
    }).encode()

    req = urllib.request.Request(
        f"{base_url}/contents/generations/tasks",
        data=payload, method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        })

    try:
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            data = json.loads(resp.read())
            task_id = data.get("id") or data.get("data", {}).get("id")
            if not task_id:
                log.warning("BytePlus: no task_id: %s", str(data)[:200])
                return False

        # Poll for completion (max 5 min)
        for _ in range(60):
            time.sleep(5)
            poll_req = urllib.request.Request(
                f"{base_url}/contents/generations/tasks/{task_id}",
                headers={"Authorization": f"Bearer {api_key}"})
            with urllib.request.urlopen(poll_req, timeout=15, context=ctx) as resp:
                result = json.loads(resp.read())
                status = (result.get("status")
                          or result.get("data", {}).get("status", ""))
                if status == "succeeded":
                    outputs = (result.get("output", {}).get("video_urls", [])
                               or result.get("data", {}).get("output", {}).get("video_urls", []))
                    if outputs:
                        dl_req = urllib.request.Request(outputs[0])
                        with urllib.request.urlopen(dl_req, timeout=60, context=ctx) as dl:
                            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                            Path(output_path).write_bytes(dl.read())
                        log.info("BytePlus: video saved to %s", output_path)
                        return True
                    log.warning("BytePlus: succeeded but no video URL")
                    return False
                elif status in ("failed", "cancelled"):
                    log.warning("BytePlus: task %s", status)
                    return False

        log.warning("BytePlus: timeout waiting for task %s", task_id)
        return False
    except Exception as e:
        log.warning("BytePlus: %s", e)
        return False


# -- Gemini Video Generation ---------------------------------------------------
def generate_video_gemini(prompt: str, output_path: str) -> bool:
    """Generate video via Gemini API (experimental, limited)."""
    # Gemini doesn't natively support video file output yet via REST
    # Placeholder for when it does. Falls through to BytePlus.
    log.info("Gemini video: not yet supported natively, falling back")
    return False


# -- Public API: Fallback Chains -----------------------------------------------

def generate_image(prompt: str, output_path: str) -> dict:
    """
    Image fallback chain: NVIDIA -> Gemini -> (skip BytePlus for images).
    Returns dict with success, provider, path.
    """
    chains = [
        ("nvidia", lambda: generate_image_nvidia(prompt, output_path)),
        ("gemini", lambda: generate_image_gemini(prompt, output_path)),
    ]

    for provider, fn in chains:
        log.info("Image: trying %s...", provider)
        try:
            if fn():
                return {"success": True, "provider": provider,
                        "path": output_path, "type": "image"}
        except Exception as e:
            log.warning("Image: %s failed: %s", provider, e)

    return {"success": False, "provider": None, "path": None,
            "type": "image", "error": "all providers failed"}


def generate_video(prompt: str, output_path: str) -> dict:
    """
    Video fallback chain: Gemini -> BytePlus (Seedance).
    Returns dict with success, provider, path.
    """
    chains = [
        ("gemini", lambda: generate_video_gemini(prompt, output_path)),
        ("byteplus", lambda: generate_video_byteplus(prompt, output_path)),
    ]

    for provider, fn in chains:
        log.info("Video: trying %s...", provider)
        try:
            if fn():
                return {"success": True, "provider": provider,
                        "path": output_path, "type": "video"}
        except Exception as e:
            log.warning("Video: %s failed: %s", provider, e)

    return {"success": False, "provider": None, "path": None,
            "type": "video", "error": "all providers failed"}


def generate_media(prompt: str, output_dir: str, index: int = 0,
                   media_type: str = "image", platform: str = "all") -> dict:
    """
    Generate media with full fallback chain.
    Video platforms (tiktok, youtube) get video.
    Image platforms (ig, fb, threads) get image.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    VIDEO_PLATFORMS = {"tiktok", "youtube", "reels"}

    if media_type == "video" or platform.lower() in VIDEO_PLATFORMS:
        out = str(Path(output_dir) / f"video_{index:02d}_{platform}.mp4")
        return generate_video(prompt, out)
    else:
        out = str(Path(output_dir) / f"image_{index:02d}_{platform}.png")
        return generate_image(prompt, out)
