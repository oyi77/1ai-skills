#!/usr/bin/env python3
"""
Generate MOVA Campaign Videos using BytePlus Seedance API
Real AI-generated videos instead of solid color backgrounds
"""

import json
import urllib.request
import ssl
import time
from pathlib import Path

# Config
BYTEPLUS_API_KEY = "REDACTED_BYTEPLUS_API_KEY"
BYTEPLUS_BASE_URL = "https://ark.ap-southeast.bytepluses.com/api/v3"
SEEDANCE_MODEL = "seedance-1-0-lite-t2v-250428"

OUTPUT_DIR = Path(__file__).parent / "output" / "mova_seedance_videos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# MOVA Campaign Posts with prompts
POSTS = [
    {
        "asset_id": "tt_001",
        "platform": "TikTok",
        "type": "video",
        "prompt": "Shocked person discovering cashback savings on phone app, money floating around, viral TikTok style",
        "ratio": "9:16"
    },
    {
        "asset_id": "tt_002",
        "platform": "TikTok",
        "type": "video",
        "prompt": "Person frustrated with old payment methods, then happy discovering MOVA app with double cashback",
        "ratio": "9:16"
    },
    {
        "asset_id": "ig_r001",
        "platform": "Instagram",
        "type": "reel",
        "prompt": "First-person view counting cashback rewards on phone screen, excited reaction, Instagram Reels aesthetic",
        "ratio": "9:16"
    },
    {
        "asset_id": "ig_c001",
        "platform": "Instagram",
        "type": "carousel",
        "prompt": "Swipe through screens showing cashback increasing, smooth scroll animation, Instagram style",
        "ratio": "9:16"
    },
    {
        "asset_id": "fb_001",
        "platform": "Facebook",
        "type": "video",
        "prompt": "Professional person explaining on camera showing savings, friendly educational style, Facebook video",
        "ratio": "9:16"
    },
    {
        "asset_id": "tw_001",
        "platform": "Twitter",
        "type": "media_post",
        "prompt": "Surprised reaction showing savings, quick impact, Twitter/X style",
        "ratio": "9:16"
    },
    {
        "asset_id": "yt_001",
        "platform": "YouTube",
        "type": "shorts",
        "prompt": "Quick before-after showing savings transformation, YouTube Shorts format",
        "ratio": "9:16"
    }
]

def make_byteplus_request(method, path, body=None):
    """Make authenticated request to BytePlus API"""
    url = f"{BYTEPLUS_BASE_URL}{path}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {BYTEPLUS_API_KEY}",
    }

    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    ssl_context = ssl.create_default_context()

    try:
        with urllib.request.urlopen(req, context=ssl_context, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        return {"error": f"HTTP {e.code}", "message": error_body}
    except Exception as e:
        return {"error": "Exception", "message": str(e)}

def create_task(prompt, ratio="9:16"):
    """Create a video generation task. Returns task_id."""
    body = {
        "model": SEEDANCE_MODEL,
        "content": [{"type": "text", "text": prompt}],
        "ratio": ratio
    }

    result = make_byteplus_request("POST", "/contents/generations/tasks", body)

    if "error" in result:
        return None, result

    task_id = result.get("id")
    if not task_id:
        return None, {"error": "No task_id returned", "raw": result}

    return task_id, result

def poll_task(task_id, timeout=300, interval=3):
    """Poll task until completed or timeout (seconds). Returns task result."""
    deadline = time.time() + timeout

    while time.time() < deadline:
        result = make_byteplus_request("GET", f"/contents/generations/tasks/{task_id}")

        if "error" in result:
            time.sleep(interval)
            continue

        status = result.get("status", "")

        if status == "succeeded":
            return result
        elif status in ("failed", "cancelled"):
            error = result.get("error", {})
            return {
                "status": status,
                "error": error.get("message", "Unknown error")
            }

        time.sleep(interval)

    return {"status": "timeout", "message": f"Timed out after {timeout}s"}

def download_video(url, output_path):
    """Download video from URL"""
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            with open(output_path, "wb") as f:
                f.write(response.read())
        return True
    except Exception as e:
        return False

def generate_video(post):
    """Generate single video using BytePlus Seedance"""
    print(f"\n[{post['asset_id']}] Generating...")
    print(f"   Platform: {post['platform']} {post['type']}")
    print(f"   Prompt: {post['prompt'][:60]}...")

    # Create task
    task_id, result = create_task(post['prompt'], ratio=post['ratio'])

    if not task_id:
        print(f"   ❌ Failed to create task: {result}")
        return None, result

    print(f"   ✅ Task created: {task_id}")

    # Poll task
    print(f"   ⏳ Generating (this takes ~20s for lite model)...")
    task_result = poll_task(task_id, timeout=300, interval=3)

    if task_result.get("status") == "timeout":
        print(f"   ❌ Timeout: {task_result.get('message')}")
        return None, task_result

    if task_result.get("status") in ("failed", "cancelled"):
        print(f"   ❌ Generation failed: {task_result.get('error')}")
        return None, task_result

    # Get video URL
    task_content = task_result.get("content", {})
    video_url = task_content.get("video_url", "")

    if not video_url:
        print(f"   ❌ No video URL in response")
        return None, {"error": "No video_url in task result"}

    # Download video
    output_path = OUTPUT_DIR / f"{post['asset_id']}.mp4"
    print(f"   📥 Downloading to {output_path.name}...")

    downloaded = download_video(video_url, output_path)

    if not downloaded:
        print(f"   ❌ Failed to download video")
        return None, {"error": "Failed to download video"}

    # Get file info
    file_size = output_path.stat().st_size
    file_size_mb = file_size / (1024 * 1024)

    print(f"   ✅ Success! ({file_size_mb:.2f}MB)")

    return {
        "asset_id": post['asset_id'],
        "video_url": video_url,
        "local_path": str(output_path),
        "size_mb": file_size_mb,
        "task_id": task_id,
        "duration": task_result.get("duration"),
        "resolution": task_result.get("resolution")
    }, None

def main():
    print("\n" + "="*70)
    print("🎬 GENERATING MOVA VIDEOS WITH BYTEPLUS SEEDANCE AI")
    print("="*70)

    print(f"\nModel: {SEEDANCE_MODEL}")
    print(f"API: {BYTEPLUS_BASE_URL}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Total videos: {len(POSTS)}")

    print("\n⏱️  ETA: ~20s × 7 = ~2.5 minutes\n")

    generated = []
    failed = []

    for i, post in enumerate(POSTS, 1):
        print(f"\n[{i}/{len(POSTS)}]", end=" ")

        result, error = generate_video(post)

        if result:
            generated.append(result)
        else:
            failed.append({
                "asset_id": post['asset_id'],
                "platform": post['platform'],
                "error": error
            })

        # Rate limiting
        if i < len(POSTS):
            time.sleep(2)

    # Summary
    print("\n" + "="*70)
    print("📊 GENERATION SUMMARY")
    print("="*70)

    print(f"\n✅ Successful: {len(generated)}/{len(POSTS)}")
    print(f"❌ Failed: {len(failed)}/{len(POSTS)}")

    if generated:
        print(f"\n📁 Generated videos:")
        total_size_mb = 0
        for v in generated:
            print(f"   • {v['asset_id']}: {v['local_path']} ({v['size_mb']:.2f}MB)")
            print(f"     └─ Video URL: {v['video_url']}")
            total_size_mb += v['size_mb']
        print(f"\n   Total size: {total_size_mb:.2f}MB")

    if failed:
        print(f"\n❌ Failed videos:")
        for v in failed:
            print(f"   • {v['asset_id']}: {v['error']}")

    # Save URLs for PostBridge
    if generated:
        urls = {v['asset_id']: v['video_url'] for v in generated}

        urls_file = OUTPUT_DIR.parent / "mova_video_urls_seedance.json"
        with open(urls_file, "w") as f:
            json.dump(urls, f, indent=2)

        print(f"\n💾 Video URLs saved: {urls_file}")
        print(f"\n📋 Ready for PostBridge!")
        print(f"\nMEDIA_URLS = {json.dumps(urls, indent=2)}")

    print("\n" + "="*70)
    print("✅ GENERATION COMPLETE")
    print("="*70)

    return len(generated) == len(POSTS)

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)