#!/usr/bin/env python3
"""
TikTok Viral Video Generator — 9:16 Portrait, 1-minute videos

Pipeline:
1. Generate viral headline & caption using NVIDIA LLM
2. Generate 5-10s video with BytePlus Seedance (9:16 ratio)
3. Loop video to 60 seconds using FFmpeg
4. Send to Telegram for review

Viral parameters from Larry Playbook:
- Headline: Bold, punchy (2-3 lines, max 80 chars)
- Duration: 5-10s (looped to 60s)
- Aspect ratio: 9:16 (1080x1920)
- Caption: Engaging with emojis (150-200 chars)
- Hashtags: 5 relevant tags
"""

import argparse
import base64
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.request
import subprocess
from pathlib import Path
from typing import Optional

# ── CONFIG ──────────────────────────────────────────────────────────────────
NVIDIA_API_KEY = "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"
BYTEPLUS_API_KEY = "cac5cfc1-e30f-47bb-b8b8-e861ffda28ea"

NVIDIA_LLM_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
BYTEPLUS_BASE_URL = "https://ark.ap-southeast.bytepluses.com/api/v3"
SEEDANCE_MODEL = "seedance-1-0-lite-t2v-250428"

OUTPUT_DIR = Path("/tmp/tiktok_viral")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FFMPEG_BIN = "/home/linuxbrew/.linuxbrew/bin/ffmpeg"

# ── VIRAL PARAMETERS (from Larry Playbook) ────────────────────────────────
VIRAL_CONCEPTS = {
    "motivation": {
        "base_idea": "Motivational quote about overcoming yesterday's self",
        "hashtags": "#motivation #mindset #success #growth #viral #inspiration",
    },
    "money": {
        "base_idea": "Money follows action not wishes, powerful money quote",
        "hashtags": "#money #wealth #financialfreedom #entrepreneur #success #mindset",
    },
    "success": {
        "base_idea": "1 year can completely change your life, success story",
        "hashtags": "#transformation #success #glowup #motivation #viral #1year",
    },
    "growth": {
        "base_idea": "Discomfort is the price of growth, push through struggle",
        "hashtags": "#growth #mindset #motivation #success #viral #discomfort",
    },
    "productivity": {
        "base_idea": "5am morning habit that changed my life, productivity tip",
        "hashtags": "#5am #productivity #habits #success #morningroutine #lifehack",
    },
}

# ── HELPERS ──────────────────────────────────────────────────────────────────
def post_json(url, payload, headers):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    ssl_ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, context=ssl_ctx, timeout=120) as r:
        return json.loads(r.read())

def get_json(url, headers):
    req = urllib.request.Request(url, headers=headers, method="GET")
    ssl_ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, context=ssl_ctx, timeout=30) as r:
        return json.loads(r.read())

def download_file(url, path, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    ssl_ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, context=ssl_ctx, timeout=120) as r:
        with open(path, "wb") as f:
            f.write(r.read())

# ── STEP 1: NVIDIA LLM — Generate Viral Content ──────────────────────
def generate_viral_content(niche: str) -> dict:
    """Generate viral headline, prompt, and caption using NVIDIA LLM."""
    print(f"\n🤖 Step 1: Generating viral content for '{niche}'...")

    concept = VIRAL_CONCEPTS.get(niche, VIRAL_CONCEPTS["motivation"])
    base_idea = concept["base_idea"]
    hashtags = concept["hashtags"]

    prompt = f"""You are a TikTok viral content expert. Generate viral content based on this idea:

Idea: {base_idea}

Create JSON with these fields:
- "headline": Bold, punchy headline (2-3 lines, max 80 chars total)
- "video_prompt": Cinematic video prompt for Seedance (60-100 words, 9:16 portrait, viral aesthetic, smooth camera movements)
- "caption": Engaging caption (150-200 characters) for TikTok with emojis
- "hook": First 3-5 words to grab attention instantly

Return ONLY valid JSON, no extra text."""

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
    }

    payload = {
        "model": "meta/llama-3.3-70b-instruct",
        "messages": [
            {"role": "system", "content": "You are a viral TikTok content creator. Always respond with valid JSON only."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.9,
        "max_tokens": 500,
    }

    try:
        resp = post_json(NVIDIA_LLM_URL, payload, headers)
        content_text = resp["choices"][0]["message"]["content"]

        # Extract JSON from response
        start = content_text.find("{")
        end = content_text.rfind("}") + 1
        if start >= 0 and end > start:
            content_text = content_text[start:end]

        content = json.loads(content_text)
        content["hashtags"] = hashtags
        content["niche"] = niche

        print(f"  ✅ Headline: {content.get('headline', '?')[:60]}")
        print(f"  ✅ Hook: {content.get('hook', '?')[:40]}")
        print(f"  ✅ Caption: {content.get('caption', '?')[:60]}")
        return content

    except Exception as e:
        print(f"  ❌ LLM error: {e}")
        # Fallback
        return {
            "headline": base_idea[:50].upper(),
            "video_prompt": f"Cinematic {base_idea}, 9:16 portrait, viral style, smooth camera",
            "caption": f"{base_idea}. Viral! {hashtags}",
            "hook": base_idea.split()[0].upper(),
            "hashtags": hashtags,
            "niche": niche,
        }


# ── STEP 2: BYTEPLUS SEEDANCE — Generate Video ───────────────────────────
def generate_video(prompt: str, ratio: str = "9:16") -> dict:
    """Generate video using BytePlus Seedance."""
    print(f"\n🎬 Step 2: Generating video via BytePlus Seedance ({ratio})...")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {BYTEPLUS_API_KEY}",
    }

    # Create task
    payload = {
        "model": SEEDANCE_MODEL,
        "content": [{"type": "text", "text": prompt}],
        "ratio": ratio,
    }

    try:
        resp = post_json(
            f"{BYTEPLUS_BASE_URL}/contents/generations/tasks",
            payload,
            headers,
        )
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else str(e)
        print(f"  ❌ Create task HTTP {e.code}: {body}")
        return None

    task_id = resp.get("id")
    if not task_id:
        print(f"  ❌ No task_id returned: {resp}")
        return None

    print(f"  📋 Task created: {task_id}")

    # Poll for result
    print("  ⏳ Polling for result (max 5 min)...")
    deadline = time.time() + 300
    attempt = 0
    while time.time() < deadline:
        attempt += 1
        time.sleep(5)

        try:
            result = get_json(
                f"{BYTEPLUS_BASE_URL}/contents/generations/tasks/{task_id}",
                headers,
            )
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8") if e.fp else str(e)
            print(f"  ⚠️  Poll HTTP {e.code}: {body}")
            continue
        except Exception as e:
            print(f"  ⚠️  Poll error: {e}")
            continue

        status = result.get("status", "")
        print(f"  [{attempt:02d}] status={status}")

        if status == "succeeded":
            content = result.get("content", {})
            video_url = content.get("video_url", "")
            duration = result.get("duration", 5)
            print(f"  ✅ Video URL: {video_url[:60]}...")
            print(f"  ✅ Duration: {duration}s")
            return {
                "task_id": task_id,
                "video_url": video_url,
                "duration": duration,
                "result": result,
            }
        elif status in ("failed", "cancelled"):
            error = result.get("error", {})
            print(f"  ❌ Task {status}: {error.get('message', 'unknown')} (code: {error.get('code', 'N/A')})")
            return None

    print("  ❌ Timeout waiting for video")
    return None


# ── STEP 3: LOOP TO 1 MINUTE (FFmpeg) ─────────────────────────────────
def loop_to_minute(input_path: Path, output_path: Path) -> bool:
    """Loop video to exactly 60 seconds using FFmpeg."""
    print(f"\n🔄 Step 3: Looping video to 1 minute...")

    # Get original duration
    cmd = [
        FFMPEG_BIN,
        "-i", str(input_path),
        "-f", "null", "-",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    # Extract duration from stderr (FFmpeg outputs to stderr)
    duration_line = None
    for line in result.stderr.split("\n"):
        if "Duration:" in line:
            duration_line = line
            break

    if not duration_line:
        print(f"  ❌ Could not get duration")
        return False

    # Parse "Duration: HH:MM:SS.ms"
    dur_str = duration_line.split("Duration:")[1].split(",")[0].strip()
    h, m, s = dur_str.split(":")
    original_duration = float(h) * 3600 + float(m) * 60 + float(s)
    print(f"  📊 Original duration: {original_duration:.2f}s")

    # Calculate how many loops needed (12 for 5s video)
    loops = int(60 / original_duration)
    print(f"  🔄 Loops needed: {loops}x")

    # Loop using FFmpeg stream loop
    cmd = [
        FFMPEG_BIN,
        "-stream_loop", str(loops),
        "-i", str(input_path),
        "-c", "copy",
        "-t", "60",  # Exactly 60 seconds
        "-y",  # Overwrite
        str(output_path),
    ]

    print(f"  ⚙️  Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"  ✅ Looped video: {output_path} ({size_mb:.2f} MB)")
        return True
    else:
        print(f"  ❌ FFmpeg error: {result.stderr}")
        return False


# ── STEP 4: SEND TO TELEGRAM ─────────────────────────────────────────────
def send_telegram(video_path: Path, content: dict) -> bool:
    """Send video to Telegram with caption."""
    print(f"\n📱 Step 4: Sending to Telegram...")

    caption = f"""🎬 TikTok Viral Video

{content.get('headline', '')}

{content.get('caption', '')}

{content.get('hashtags', '')}
"""

    # Note: We use the message tool from the session, not subprocess
    # Return metadata for the session to use
    meta = {
        "video_path": str(video_path),
        "caption": caption,
        "headline": content.get("headline"),
        "hook": content.get("hook"),
    }

    with open(OUTPUT_DIR / "telegram_meta.json", "w") as f:
        json.dump(meta, f, indent=2)

    print(f"  📦 Video ready: {video_path} ({video_path.stat().st_size:,} bytes)")
    print(f"  ℹ️  Meta: {OUTPUT_DIR}/telegram_meta.json")
    return True


# ── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Generate TikTok viral video")
    parser.add_argument("--niche", choices=list(VIRAL_CONCEPTS.keys()),
                        default="motivation", help="Viral content niche")
    parser.add_argument("--ratio", default="9:16", help="Video aspect ratio (default: 9:16)")
    parser.add_argument("--skip-loop", action="store_true",
                        help="Skip looping to 1 minute (use original duration)")
    parser.add_argument("--skip-telegram", action="store_true",
                        help="Skip sending to Telegram")
    args = parser.parse_args()

    print("=" * 70)
    print("🚀 TIKTOK VIRAL VIDEO GENERATOR")
    print("=" * 70)
    print(f"Niche: {args.niche}")
    print(f"Ratio: {args.ratio}")
    print()

    # Step 1: Generate viral content
    content = generate_viral_content(args.niche)

    # Step 2: Generate video
    video_result = generate_video(content["video_prompt"], args.ratio)
    if not video_result:
        print("\n💥 Pipeline failed at video generation step")
        sys.exit(1)

    # Download video
    video_url = video_result["video_url"]
    temp_video = OUTPUT_DIR / f"{args.niche}_temp.mp4"
    download_file(video_url, temp_video)

    size_mb = temp_video.stat().st_size / (1024 * 1024)
    print(f"  ✅ Downloaded: {temp_video} ({size_mb:.2f} MB)")

    # Step 3: Loop to 1 minute
    if not args.skip_loop:
        final_video = OUTPUT_DIR / f"{args.niche}_1min.mp4"
        if not loop_to_minute(temp_video, final_video):
            print("\n💥 Pipeline failed at looping step")
            sys.exit(1)
    else:
        final_video = temp_video

    # Step 4: Send to Telegram
    if not args.skip_telegram:
        send_telegram(final_video, content)

    # Summary
    print("\n" + "=" * 70)
    print("✅ PIPELINE COMPLETE!")
    print(f"   Video: {final_video}")
    print(f"   Headline: {content.get('headline', '')}")
    print(f"   Hook: {content.get('hook', '')}")
    print(f"   Hashtags: {content.get('hashtags', '')}")
    print("=" * 70)

    # Write result
    result = {
        "video_path": str(final_video),
        "headline": content.get("headline"),
        "hook": content.get("hook"),
        "caption": content.get("caption"),
        "hashtags": content.get("hashtags"),
        "niche": args.niche,
        "ratio": args.ratio,
        "duration_seconds": 60 if not args.skip_loop else video_result["duration"],
        "task_id": video_result["task_id"],
    }

    with open(OUTPUT_DIR / "result.json", "w") as f:
        json.dump(result, f, indent=2)
    print(f"   Result: {OUTPUT_DIR}/result.json")


if __name__ == "__main__":
    main()
