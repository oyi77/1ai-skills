"""
Batch Generator — Generate multiple variations simultaneously
Submit all I2V tasks at once → parallel rendering → collect results
Modes:
  - style_sweep: same product, all 5 styles
  - format_sweep: same product+style, all 4 formats
  - custom: specific list of (category, style, format)
"""

import os, json, asyncio, time, base64, io
import urllib.request
import subprocess
from PIL import Image

NVIDIA_KEY = os.environ.get("NVIDIA_API_KEY")
BYTEPLUS_KEY = os.environ.get("BYTEPLUS_API_KEY")
BYTEPLUS_BASE = "https://ark.ap-southeast.bytepluses.com/api/v3"
FFMPEG = "/home/linuxbrew/.linuxbrew/bin/ffmpeg"

import sys

sys.path.insert(0, os.path.dirname(__file__))
from prompt_library import get_prompt, STYLES, FORMATS
from cost_dashboard import log_cost, estimate_generation_cost


def estimate_batch(image_path: str, variations: list) -> dict:
    """Show cost estimate before running batch"""
    total_usd = 0
    breakdown = []
    for cat, style, fmt in variations:
        est = estimate_generation_cost(fmt)
        total_usd += est["total_usd"]
        breakdown.append({"style": style, "format": fmt, "cost": est["total_usd"]})
    return {
        "count": len(variations),
        "total_usd": round(total_usd, 4),
        "total_idr": round(total_usd * 16300),
        "breakdown": breakdown,
    }


def generate_image_for_batch(prompt: str, model: str, idx: int, output_dir: str) -> str:
    """Generate single image for batch"""
    out_path = os.path.join(output_dir, f"batch_{idx:02d}_img.jpg")
    if os.path.exists(out_path):
        return out_path

    if "sd3" in model or "stable-diffusion-3" in model:
        url = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-3-medium"
        key = "image"
    else:
        url = "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.1-dev"
        key = None

    headers = {
        "Authorization": f"Bearer {NVIDIA_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = json.dumps({"prompt": prompt}).encode()

    try:
        req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = json.loads(resp.read())

        artifact = data.get("artifacts", [{}])[0] if not key else {}
        b64 = data.get("image") if key else artifact.get("base64", "")
        finish_rsn = artifact.get("finishReason", "")

        # Flux content-filter: returns 6KB black image + finishReason=CONTENT_FILTERED
        # OR image is suspiciously tiny (<10KB decoded) — fallback to SD3
        is_filtered = (
            finish_rsn == "CONTENT_FILTERED"
            or (b64 and len(base64.b64decode(b64)) < 10_000)
            or not b64
        )

        if is_filtered:
            print(f"    ⚠️  Flux filtered ({finish_rsn or 'tiny'}) → SD3 fallback")
            url2 = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-3-medium"
            req2 = urllib.request.Request(
                url2, data=payload, headers=headers, method="POST"
            )
            with urllib.request.urlopen(req2, timeout=90) as resp2:
                data2 = json.loads(resp2.read())
            b64 = data2.get("image", "")

        decoded = base64.b64decode(b64)
        with open(out_path, "wb") as f:
            f.write(decoded)
        log_cost("nvidia_flux", "batch_image")
        return out_path
    except Exception as e:
        print(f"  Batch img {idx} error: {e}")
        return None


def prepare_image_for_i2v(image_path: str) -> bytes:
    """
    Pre-crop image to 9:16 portrait (720x1280) using center-crop.
    Prevents Seedance I2V from doing its own flip/rotate/transform
    when converting a square (1024x1024) image to portrait ratio.
    Returns JPEG bytes ready for base64 encoding.
    """
    img = Image.open(image_path).convert("RGB")
    W, H = img.size
    target_w, target_h = 720, 1280

    # Scale so height fills target_h
    scale = target_h / H
    new_w = int(W * scale)
    img_scaled = img.resize((new_w, target_h), Image.LANCZOS)

    # Center-crop width
    left = max(0, (new_w - target_w) // 2)
    img_cropped = img_scaled.crop((left, 0, left + target_w, target_h))

    buf = io.BytesIO()
    img_cropped.save(buf, format="JPEG", quality=95)
    return buf.getvalue()


def submit_i2v_batch(image_path: str, anim_prompt: str, duration: int = 5) -> str:
    """Submit I2V task, return task_id"""
    # Pre-crop to exact 9:16 so Seedance doesn't flip/transform the image
    img_bytes = prepare_image_for_i2v(image_path)
    img_b64 = base64.b64encode(img_bytes).decode()

    payload = json.dumps(
        {
            "model": "seedance-1-0-lite-i2v-250428",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"},
                    "role": "first_frame",
                },
                {"type": "text", "text": anim_prompt},
            ],
            "duration": min(duration, 10),
            "seed": -1,
            # ratio removed — image already is 9:16
        }
    ).encode()

    headers = {
        "Authorization": f"Bearer {BYTEPLUS_KEY}",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(
        f"{BYTEPLUS_BASE}/contents/generations/tasks",
        data=payload,
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read()).get("id")
    except Exception as e:
        print(f"  I2V submit error: {e}")
        return None


def poll_all_tasks(task_map: dict, output_dir: str, timeout: int = 300) -> dict:
    """
    Poll multiple I2V tasks simultaneously.
    task_map: {idx: (task_id, duration)}
    Returns: {idx: video_path}
    """
    results = {}
    pending = dict(task_map)
    start_time = time.time()
    headers = {"Authorization": f"Bearer {BYTEPLUS_KEY}"}

    print(f"  ⏳ Polling {len(pending)} I2V tasks...")
    while pending and (time.time() - start_time) < timeout:
        time.sleep(5)
        done = []
        for idx, (task_id, duration) in pending.items():
            try:
                req = urllib.request.Request(
                    f"{BYTEPLUS_BASE}/contents/generations/tasks/{task_id}",
                    headers=headers,
                )
                with urllib.request.urlopen(req, timeout=15) as resp:
                    data = json.loads(resp.read())
                status = data.get("status")
                if status == "succeeded":
                    vid_url = data["content"]["video_url"]
                    tmp_path = os.path.join(output_dir, f"batch_{idx:02d}_raw.mp4")
                    out_path = os.path.join(output_dir, f"batch_{idx:02d}_video.mp4")
                    urllib.request.urlretrieve(vid_url, tmp_path)
                    # Loop to target duration
                    subprocess.run(
                        [
                            FFMPEG,
                            "-y",
                            "-stream_loop",
                            "-1",
                            "-i",
                            tmp_path,
                            "-t",
                            str(duration),
                            "-c",
                            "copy",
                            out_path,
                        ],
                        capture_output=True,
                    )
                    results[idx] = out_path
                    log_cost("byteplus_lite", f"batch_i2v_{idx}")
                    print(f"    Variation {idx} ✅")
                    done.append(idx)
                elif status in ("failed", "cancelled"):
                    print(f"    Variation {idx} ❌ {status}")
                    done.append(idx)
            except Exception as e:
                print(f"    Poll error {idx}: {e}")
        for idx in done:
            pending.pop(idx, None)

    if pending:
        print(f"  ⏰ Timeout: {len(pending)} tasks incomplete")
    return results


async def run_batch(
    image_path: str,
    category: str,
    product_desc: str,
    output_dir: str,
    mode: str = "style_sweep",  # style_sweep | format_sweep | custom
    custom_variations: list = None,  # [(cat, style, fmt), ...]
    chat_id: str = "batch",
    dry_run: bool = False,
) -> dict:
    """
    Main batch runner.
    Returns dict with all generated file paths.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Build variation list
    if mode == "style_sweep":
        variations = [(category, style, "foto") for style in STYLES.keys()]
    elif mode == "format_sweep":
        variations = [
            (category, "dark_moody", fmt)
            for fmt in FORMATS.keys()
            if fmt != "tiktok_60s"
        ]
    else:
        variations = custom_variations or []

    # Estimate
    estimate = estimate_batch(image_path, variations)
    print(
        f"\n📦 Batch: {estimate['count']} variations | Est cost: ${estimate['total_usd']} (~Rp {estimate['total_idr']:,})"
    )

    if dry_run:
        return {"estimate": estimate, "variations": variations}

    # Step 1: Generate all images (sequential — API limit)
    print(f"\n🖼️  Generating {len(variations)} images...")
    images = {}
    for i, (cat, style, fmt) in enumerate(variations):
        config = get_prompt(cat, style, fmt, product_desc)
        img_path = generate_image_for_batch(
            config["image_prompt"], config["image_model"], i, output_dir
        )
        images[i] = {
            "image": img_path,
            "config": config,
            "variation": (cat, style, fmt),
        }
        print(f"  [{i+1}/{len(variations)}] {style} ✅")

    # Step 2: Submit all I2V tasks at once
    print(f"\n🎬 Submitting {len(images)} I2V tasks (parallel)...")
    task_map = {}
    for i, data in images.items():
        if data["image"]:
            task_id = submit_i2v_batch(data["image"], data["config"]["i2v_prompt"])
            if task_id:
                task_map[i] = (task_id, 5)
                print(f"  Variation {i+1}: Task {task_id} ✅")

    # Step 3: Poll all simultaneously
    video_results = poll_all_tasks(task_map, output_dir)

    # Step 4: Build summary
    results = []
    for i, data in images.items():
        cat, style, fmt = data["variation"]
        results.append(
            {
                "idx": i + 1,
                "style": style,
                "format": fmt,
                "image": data["image"],
                "video": video_results.get(i),
                "status": "✅" if video_results.get(i) else "❌",
            }
        )

    success = sum(1 for r in results if r["video"])
    print(f"\n✅ Batch complete! {success}/{len(variations)} successful")

    # Save manifest
    manifest = os.path.join(output_dir, "batch_manifest.json")
    with open(manifest, "w") as f:
        json.dump({"results": results, "estimate": estimate}, f, indent=2)

    return {
        "results": results,
        "success": success,
        "total": len(variations),
        "estimate": estimate,
        "manifest": manifest,
        "output_dir": output_dir,
    }


def build_batch_options_message(category: str) -> tuple[str, list]:
    """Show batch options to user before running"""
    text = (
        f"🚀 *Batch Generation*\n\n"
        f"Mau generate variasi apa?\n\n"
        f"• *Style Sweep* — Foto yang sama dalam 5 style berbeda\n"
        f"• *Format Sweep* — 1 style dalam 3 format (Foto, 15s, 30s)\n\n"
        f"Pilih mode:"
    )
    buttons = [
        [
            {
                "text": "🎨 Style Sweep (5 variasi)",
                "callback_data": f"batch:style:{category}",
            },
            {
                "text": "📐 Format Sweep (3 variasi)",
                "callback_data": f"batch:format:{category}",
            },
        ],
        [{"text": "❌ Batal", "callback_data": "batch:cancel"}],
    ]
    return text, buttons


if __name__ == "__main__":
    # Quick cost estimate
    variations = [(c, s, "foto") for s in STYLES for c in ["minuman"]]
    est = estimate_batch(None, variations)
    print("Style sweep estimate:", est)
