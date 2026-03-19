"""
Provider Chain — Full 9-video + 5-image fallback chain for Content Kingdom.

Video priority (1→9):
  1. byteplus   BytePlus Seedance
  2. xai        XAI Grok Aurora (via GeminiGen grok-3)
  3. laozhang   LaoZhang API
  4. evolink    EvoLink
  5. hypereal   Hypereal
  6. siliconflow SiliconFlow
  7. falai      Fal.ai Video
  8. kie        Kie.ai
  9. remotion   PIL/FFmpeg placeholder (always works)

Image priority (1→5):
  1. geminigen  GeminiGen nano-banana-pro
  2. nvidia     NVIDIA Flux
  3. replicate  Replicate
  4. falai      Fal.ai Image
  5. pil        PIL placeholder (always works)
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional

log = logging.getLogger("ContentKingdom.ProviderChain")

# ── Config root ──────────────────────────────────────────────────────────────
_SKILL_DIR = Path(__file__).parent.parent
_WS_DIR = _SKILL_DIR.parent.parent  # workspace/
_CFG_DIR = _WS_DIR / "config"


def _load_geminigen_key() -> str:
    try:
        cfg = json.loads((_CFG_DIR / "geminigen_api.json").read_text())
        return cfg.get("api_key", "")
    except Exception:
        return os.environ.get("GEMINIGEN_API_KEY", "")


def _env(key: str, fallback: str = "") -> str:
    return os.environ.get(key, fallback)


def _get_falai_key() -> str:
    """Fal.ai key — try multiple common env var names."""
    return (os.environ.get("FALAI_API_KEY")
            or os.environ.get("FAL_KEY")
            or os.environ.get("FAL_API_KEY")
            or "")


def _get_siliconflow_key() -> str:
    return (os.environ.get("SILICONFLOW_API_KEY")
            or os.environ.get("SILICON_API_KEY")
            or "")


def _get_replicate_key() -> str:
    return (os.environ.get("REPLICATE_API_TOKEN")
            or os.environ.get("REPLICATE_API_KEY")
            or "")


# ── Helper: HTTP GET/POST ────────────────────────────────────────────────────
def _http(url: str, method: str = "GET", data: bytes | None = None,
          headers: dict | None = None, timeout: int = 30) -> dict | None:
    req = urllib.request.Request(url, data=data, method=method)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except Exception as e:
        log.debug("HTTP %s %s failed: %s", method, url, e)
        return None


def _poll_geminigen(uuid: str, api_key: str, max_wait: int = 120) -> str | None:
    """Poll GeminiGen history endpoint until done. Returns URL or None."""
    url = f"https://api.geminigen.ai/uapi/v1/history/{uuid}"
    headers = {"x-api-key": api_key}
    deadline = time.time() + max_wait
    while time.time() < deadline:
        r = _http(url, headers=headers)
        if not r:
            time.sleep(5)
            continue
        status = r.get("data", {}).get("status") or r.get("status")
        if status == 2 or status == "completed":
            items = r.get("data", {}).get("items") or []
            if items:
                return items[0].get("url") or items[0].get("output_url")
            return r.get("data", {}).get("url")
        if status == 3 or status == "failed":
            log.warning("GeminiGen job failed: %s", r)
            return None
        time.sleep(5)
    log.warning("GeminiGen polling timeout (%ss)", max_wait)
    return None


# ════════════════════════════════════════════════════════════════════════════
# IMAGE PROVIDERS
# ════════════════════════════════════════════════════════════════════════════

def _img_geminigen(prompt: str, aspect: str = "9:16") -> str | None:
    """GeminiGen nano-banana-pro image."""
    key = _load_geminigen_key()
    if not key:
        log.info("Image: geminigen skipped — no API key")
        return None
    import sys
    sys.path.insert(0, str(_SKILL_DIR))
    try:
        from modules.geminigen_client import GeminiGenClient
        client = GeminiGenClient(api_key=key)
        url = client.generate_image_sync(
            prompt=prompt,
            aspect_ratio=aspect,
            style="Photorealistic",
            resolution="1K",
            timeout=90,
        )
        if url:
            log.info("Image: geminigen ✅ %s", url[:60])
        return url
    except Exception as e:
        log.warning("Image: geminigen failed: %s", e)
        return None


def _img_nvidia(prompt: str) -> str | None:
    """NVIDIA Flux image."""
    key = _env("NVIDIA_API_KEY")
    if not key:
        log.info("Image: nvidia skipped — no API key")
        return None
    try:
        url = "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux-dev"
        payload = json.dumps({"prompt": prompt, "width": 1024, "height": 1024,
                               "num_inference_steps": 30, "guidance": 3.5,
                               "seed": 42}).encode()
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        r = _http(url, "POST", payload, headers, timeout=60)
        if r and r.get("artifacts"):
            # Returns base64 — save to temp file
            import base64
            tmp = tempfile.mktemp(suffix=".jpg")
            with open(tmp, "wb") as f:
                f.write(base64.b64decode(r["artifacts"][0]["base64"]))
            log.info("Image: nvidia ✅ saved to %s", tmp)
            return tmp
    except Exception as e:
        log.warning("Image: nvidia failed: %s", e)
    return None


def _img_replicate(prompt: str) -> str | None:
    """Replicate image via REPLICATE_API_TOKEN."""
    key = _env("REPLICATE_API_TOKEN")
    if not key:
        log.info("Image: replicate skipped — no API key")
        return None
    try:
        payload = json.dumps({"version": "stability-ai/sdxl:39ed52f2319f9ee64ad4ccf29f5cbfc61c49b3f35a5a74bfc4accd46567b2a15",
                               "input": {"prompt": prompt}}).encode()
        headers = {"Authorization": f"Token {key}", "Content-Type": "application/json"}
        r = _http("https://api.replicate.com/v1/predictions", "POST", payload, headers, 30)
        if r and r.get("urls", {}).get("get"):
            # Poll
            get_url = r["urls"]["get"]
            for _ in range(20):
                time.sleep(5)
                res = _http(get_url, headers={"Authorization": f"Token {key}"})
                if res and res.get("status") == "succeeded" and res.get("output"):
                    url = res["output"][0] if isinstance(res["output"], list) else res["output"]
                    log.info("Image: replicate ✅ %s", url[:60])
                    return url
    except Exception as e:
        log.warning("Image: replicate failed: %s", e)
    return None


def _img_pexels(prompt: str) -> str | None:
    """Pexels stock photo — search by keywords extracted from prompt."""
    key = _env("PEXELS_API_KEY")
    if not key:
        log.info("Image: pexels skipped — no PEXELS_API_KEY")
        return None
    try:
        # Extract 2-3 keywords from prompt for search
        words = [w for w in prompt.lower().split() if len(w) > 4
                 and w not in ("dark","theme","black","background","premium","minimalist")][:3]
        query = "+".join(words) if words else "business+finance"
        url = f"https://api.pexels.com/v1/search?query={query}&per_page=3&orientation=portrait"
        headers = {"Authorization": key}
        r = _http(url, headers=headers, timeout=10)
        if r and r.get("photos"):
            photo = r["photos"][0]
            photo_url = photo.get("src", {}).get("large2x") or photo.get("src", {}).get("original")
            if photo_url:
                import urllib.request as _ur
                tmp = tempfile.mktemp(suffix=".jpg")
                _ur.urlretrieve(photo_url, tmp)
                log.info("Image: pexels ✅ %s → %s", query, tmp)
                return tmp
    except Exception as e:
        log.warning("Image: pexels failed: %s", e)
    return None


def _vid_pexels(prompt: str) -> str | None:
    """Pexels stock VIDEO — search by keywords from prompt."""
    key = _env("PEXELS_API_KEY")
    if not key:
        log.info("Video: pexels skipped — no PEXELS_API_KEY")
        return None
    try:
        words = [w for w in prompt.lower().split() if len(w) > 4
                 and w not in ("dark","theme","black","background","premium","cinematic")][:3]
        query = "+".join(words) if words else "business+technology"
        url = f"https://api.pexels.com/videos/search?query={query}&per_page=3&orientation=portrait&size=medium"
        headers = {"Authorization": key}
        r = _http(url, headers=headers, timeout=10)
        if r and r.get("videos"):
            video = r["videos"][0]
            # Get best portrait file
            files = sorted(video.get("video_files", []),
                           key=lambda f: f.get("height", 0), reverse=True)
            portrait = next((f for f in files if f.get("width", 999) < f.get("height", 0)), None)
            vid_url = (portrait or files[0]).get("link") if files else None
            if vid_url:
                import urllib.request as _ur
                tmp = tempfile.mktemp(suffix=".mp4")
                _ur.urlretrieve(vid_url, tmp)
                log.info("Video: pexels ✅ %s → %s", query, tmp)
                return tmp
    except Exception as e:
        log.warning("Video: pexels failed: %s", e)
    return None


def _img_falai(prompt: str) -> str | None:
    """Fal.ai image."""
    key = _get_falai_key()
    if not key:
        log.info("Image: falai skipped — no API key")
        return None
    try:
        payload = json.dumps({"prompt": prompt, "image_size": "portrait_4_3"}).encode()
        headers = {"Authorization": f"Key {key}", "Content-Type": "application/json"}  # noqa
        r = _http("https://queue.fal.run/fal-ai/fast-sdxl", "POST", payload, headers, 30)
        if r and r.get("request_id"):
            req_id = r["request_id"]
            for _ in range(24):
                time.sleep(5)
                res = _http(f"https://queue.fal.run/fal-ai/fast-sdxl/requests/{req_id}",
                            headers={"Authorization": f"Key {key}"})
                if res and res.get("images"):
                    url = res["images"][0]["url"]
                    log.info("Image: falai ✅ %s", url[:60])
                    return url
    except Exception as e:
        log.warning("Image: falai failed: %s", e)
    return None


def _img_pil_placeholder(prompt: str) -> str:
    """PIL placeholder — always works."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new("RGB", (1080, 1920), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Wrap text
        words = prompt[:120].split()
        lines, line = [], []
        for w in words:
            if len(" ".join(line + [w])) < 35:
                line.append(w)
            else:
                lines.append(" ".join(line))
                line = [w]
        if line:
            lines.append(" ".join(line))
        y = 900
        for l in lines[:6]:
            draw.text((50, y), l, fill=(255, 255, 255))
            y += 60
        tmp = tempfile.mktemp(suffix=".jpg")
        img.save(tmp, "JPEG", quality=90)
        log.info("Image: PIL placeholder ✅ %s", tmp)
        return tmp
    except Exception:
        # Absolute last resort — empty file
        tmp = tempfile.mktemp(suffix=".jpg")
        Path(tmp).write_bytes(b"")
        return tmp


# ════════════════════════════════════════════════════════════════════════════
# VIDEO PROVIDERS
# ════════════════════════════════════════════════════════════════════════════

def _vid_byteplus(prompt: str) -> str | None:
    """BytePlus Seedance T2V."""
    key = _env("BYTEPLUS_API_KEY")
    if not key:
        log.info("Video: byteplus skipped — no API key")
        return None
    try:
        base = "https://ark.ap-southeast.bytepluses.com/api/v3"
        models = ["seedance-1-0-lite-t2v-250428", "seedance-1-0-pro-250528",
                  "seedance-1-5-pro-251215"]
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        for model in models:
            payload = json.dumps({"model": model, "content": [{"type": "text", "text": prompt}],
                                   "aspect_ratio": "9:16", "duration": 6}).encode()
            r = _http(f"{base}/contents/generations/tasks", "POST", payload, headers, 30)
            if r and (r.get("id") or r.get("task_id")):
                task_id = r.get("id") or r.get("task_id")
                # Poll
                for _ in range(36):  # 3 min max
                    time.sleep(5)
                    res = _http(f"{base}/contents/generations/tasks/{task_id}", headers=headers)
                    if res:
                        status = res.get("status", "")
                        if status == "succeeded":
                            url = (res.get("content", {}).get("video_url")
                                   or res.get("video_url")
                                   or res.get("output", {}).get("url"))
                            if url:
                                log.info("Video: byteplus ✅ %s", url[:60])
                                return url
                        elif status in ("failed", "cancelled"):
                            break
        log.warning("Video: byteplus — no URL after polling")
    except Exception as e:
        log.warning("Video: byteplus failed: %s", e)
    return None


def _vid_xai_geminigen(prompt: str) -> str | None:
    """XAI Grok Aurora via GeminiGen grok-3."""
    key = _load_geminigen_key()
    if not key:
        log.info("Video: xai/geminigen skipped — no API key")
        return None
    try:
        import sys
        sys.path.insert(0, str(_SKILL_DIR))
        from modules.geminigen_client import GeminiGenClient
        client = GeminiGenClient(api_key=key)
        r = client.generate_video_grok(
            prompt=prompt,
            model="grok-3",
            aspect_ratio="portrait",   # 9:16 portrait; do NOT pass resolution
            duration=6,
        )
        if r and r.get("uuid"):
            url = _poll_geminigen(r["uuid"], key, max_wait=180)
            if url:
                log.info("Video: xai/geminigen ✅ %s", url[:60])
            return url
    except Exception as e:
        log.warning("Video: xai/geminigen failed: %s", e)
    return None


def _vid_siliconflow(prompt: str) -> str | None:
    """SiliconFlow video via API."""
    key = _get_siliconflow_key()
    if not key:
        log.info("Video: siliconflow skipped — no API key")
        return None
    try:
        payload = json.dumps({"model": "Wan2.1-T2V-14B",
                               "prompt": prompt,
                               "image_size": "832x480"}).encode()
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        r = _http("https://api.siliconflow.cn/v1/video/submit", "POST", payload, headers, 30)
        if r and r.get("requestId"):
            req_id = r["requestId"]
            for _ in range(36):
                time.sleep(5)
                res = _http(f"https://api.siliconflow.cn/v1/video/status",
                            "POST",
                            json.dumps({"requestId": req_id}).encode(),
                            headers)
                if res and res.get("status") == "Succeed":
                    url = res.get("results", {}).get("videos", [{}])[0].get("url")
                    if url:
                        log.info("Video: siliconflow ✅ %s", url[:60])
                        return url
                elif res and res.get("status") in ("Failed",):
                    break
    except Exception as e:
        log.warning("Video: siliconflow failed: %s", e)
    return None


def _vid_falai(prompt: str) -> str | None:
    """Fal.ai video (fast-animatediff)."""
    key = _get_falai_key()
    if not key:
        log.info("Video: falai skipped — no API key")
        return None
    try:
        payload = json.dumps({"prompt": prompt, "num_frames": 24}).encode()
        headers = {"Authorization": f"Key {key}", "Content-Type": "application/json"}
        r = _http("https://queue.fal.run/fal-ai/fast-animatediff", "POST", payload, headers, 30)
        if r and r.get("request_id"):
            req_id = r["request_id"]
            for _ in range(24):
                time.sleep(5)
                res = _http(f"https://queue.fal.run/fal-ai/fast-animatediff/requests/{req_id}",
                            headers={"Authorization": f"Key {key}"})
                if res and res.get("video", {}).get("url"):
                    url = res["video"]["url"]
                    log.info("Video: falai ✅ %s", url[:60])
                    return url
    except Exception as e:
        log.warning("Video: falai failed: %s", e)
    return None


def _vid_placeholder_ffmpeg(prompt: str) -> str | None:
    """Last resort: generate static-image video via FFmpeg."""
    try:
        img_path = _img_pil_placeholder(prompt)
        out = tempfile.mktemp(suffix=".mp4")
        cmd = [
            "ffmpeg", "-y", "-loop", "1", "-i", img_path,
            "-t", "6", "-vf", "scale=1080:1920",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", out
        ]
        result = subprocess.run(cmd, capture_output=True, timeout=30)
        if result.returncode == 0 and Path(out).exists():
            log.info("Video: ffmpeg placeholder ✅ %s", out)
            return out
    except Exception as e:
        log.warning("Video: ffmpeg placeholder failed: %s", e)
    return None


# ════════════════════════════════════════════════════════════════════════════
# PUBLIC API
# ════════════════════════════════════════════════════════════════════════════

def try_image_providers(prompt: str, aspect: str = "9:16") -> dict:
    """
    Try image providers in priority order. Returns:
      {"url": <url or path>, "provider": <name>}  on success
      {"url": None, "provider": None, "error": "all failed"}  on total failure

    Priority:
      1. GeminiGen (AI-generated, best quality)
      2. NVIDIA Flux (AI-generated)
      3. Replicate SDXL (AI-generated)
      4. Fal.ai (AI-generated)
      5. Pexels (stock photo — real content, much better than PIL)
      6. PIL placeholder (absolute last resort — never blocks pipeline)
    """
    chain = [
        ("geminigen", lambda: _img_geminigen(prompt, aspect)),
        ("nvidia",    lambda: _img_nvidia(prompt)),
        ("replicate", lambda: _img_replicate(prompt)),
        ("falai",     lambda: _img_falai(prompt)),
        ("pexels",    lambda: _img_pexels(prompt)),
        ("pil",       lambda: _img_pil_placeholder(prompt)),
    ]
    for name, fn in chain:
        log.info("Image: trying %s...", name)
        try:
            result = fn()
            if result:
                return {"url": result, "provider": name}
        except Exception as e:
            log.warning("Image: %s exception: %s", name, e)
    return {"url": None, "provider": None, "error": "all providers failed"}


def _vid_laozhang(prompt: str) -> str | None:
    """LaoZhang video via their API."""
    key = _env("LAOZHANG_API_KEY")
    if not key:
        log.info("Video: laozhang skipped — no API key")
        return None
    try:
        # LaoZhang uses OpenAI-compatible API format
        payload = json.dumps({"model": "sora", "prompt": prompt,
                               "size": "1080x1920", "duration": 6}).encode()
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        r = _http("https://api.laozhang.ai/v1/video/generate", "POST", payload, headers, 30)
        if r and (r.get("data", {}).get("id") or r.get("id")):
            task_id = r.get("data", {}).get("id") or r.get("id")
            for _ in range(36):
                time.sleep(5)
                res = _http(f"https://api.laozhang.ai/v1/video/task/{task_id}",
                            headers={"Authorization": f"Bearer {key}"})
                if res and res.get("data", {}).get("status") == "completed":
                    url = res["data"].get("video_url")
                    if url:
                        log.info("Video: laozhang ✅ %s", url[:60])
                        return url
    except Exception as e:
        log.warning("Video: laozhang failed: %s", e)
    return None


def _vid_evolink(prompt: str) -> str | None:
    """EvoLink video."""
    key = _env("EVOLINK_API_KEY")
    if not key:
        log.info("Video: evolink skipped — no API key")
        return None
    try:
        payload = json.dumps({"prompt": prompt, "duration": 6,
                               "aspect_ratio": "9:16"}).encode()
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        r = _http("https://api.evolink.ai/v1/video/create", "POST", payload, headers, 30)
        if r and r.get("task_id"):
            tid = r["task_id"]
            for _ in range(36):
                time.sleep(5)
                res = _http(f"https://api.evolink.ai/v1/video/status/{tid}",
                            headers={"Authorization": f"Bearer {key}"})
                if res and res.get("status") == "completed":
                    url = res.get("url")
                    if url:
                        log.info("Video: evolink ✅ %s", url[:60])
                        return url
    except Exception as e:
        log.warning("Video: evolink failed: %s", e)
    return None


def _vid_hypereal(prompt: str) -> str | None:
    """Hypereal video."""
    key = _env("HYPEREAL_API_KEY")
    if not key:
        log.info("Video: hypereal skipped — no API key")
        return None
    try:
        payload = json.dumps({"prompt": prompt, "resolution": "1080x1920",
                               "duration": 6}).encode()
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        r = _http("https://api.hypereal.ai/v1/generate", "POST", payload, headers, 30)
        if r and r.get("id"):
            tid = r["id"]
            for _ in range(36):
                time.sleep(5)
                res = _http(f"https://api.hypereal.ai/v1/status/{tid}",
                            headers={"Authorization": f"Bearer {key}"})
                if res and res.get("state") == "done":
                    url = res.get("video_url")
                    if url:
                        log.info("Video: hypereal ✅ %s", url[:60])
                        return url
    except Exception as e:
        log.warning("Video: hypereal failed: %s", e)
    return None


def _vid_kie(prompt: str) -> str | None:
    """Kie.ai video."""
    key = _env("KIE_API_KEY")
    if not key:
        log.info("Video: kie skipped — no API key")
        return None
    try:
        payload = json.dumps({"prompt": prompt, "aspect": "9:16",
                               "duration": 5}).encode()
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        r = _http("https://api.kie.ai/v1/video", "POST", payload, headers, 30)
        if r and r.get("uuid"):
            uuid = r["uuid"]
            for _ in range(36):
                time.sleep(5)
                res = _http(f"https://api.kie.ai/v1/video/{uuid}",
                            headers={"Authorization": f"Bearer {key}"})
                if res and res.get("status") == "done":
                    url = res.get("url")
                    if url:
                        log.info("Video: kie ✅ %s", url[:60])
                        return url
    except Exception as e:
        log.warning("Video: kie failed: %s", e)
    return None


def try_video_providers(prompt: str) -> dict:
    """
    Try video providers in priority order. Returns:
      {"url": <url or path>, "provider": <name>}  on success
      {"url": None, "provider": None, "error": "all failed"}  on total failure

    Priority (matches providers.ts):
      1. BytePlus Seedance  — best quality, commercial
      2. XAI/GeminiGen Grok — creative
      3. LaoZhang           — anime/stylized
      4. EvoLink            — versatile async
      5. Hypereal           — aspect ratio control
      6. SiliconFlow        — Wan2.1 model
      7. Fal.ai             — animatediff
      8. Kie.ai             — general
      9. Pexels Videos      — stock (real content, always works with key)
     10. FFmpeg placeholder — absolutely last resort (no API needed)
    """
    chain = [
        ("byteplus",    lambda: _vid_byteplus(prompt)),
        ("xai",         lambda: _vid_xai_geminigen(prompt)),
        ("laozhang",    lambda: _vid_laozhang(prompt)),
        ("evolink",     lambda: _vid_evolink(prompt)),
        ("hypereal",    lambda: _vid_hypereal(prompt)),
        ("siliconflow", lambda: _vid_siliconflow(prompt)),
        ("falai",       lambda: _vid_falai(prompt)),
        ("kie",         lambda: _vid_kie(prompt)),
        ("pexels",      lambda: _vid_pexels(prompt)),
        ("ffmpeg_placeholder", lambda: _vid_placeholder_ffmpeg(prompt)),
    ]
    for name, fn in chain:
        log.info("Video: trying %s...", name)
        try:
            result = fn()
            if result:
                return {"url": result, "provider": name}
        except Exception as e:
            log.warning("Video: %s exception: %s", name, e)
    return {"url": None, "provider": None, "error": "all providers failed"}
