#!/usr/bin/env python3
"""
Multi-Stage I2V Video Generator — Larry Playbook Advanced Pipeline

Workflow based on proven viral formula:
1. Generate 6 images (NVIDIA Flux)
2. Generate video DARI tiap image (BytePlus Seedance I2V) → 6 videos
3. Ambil FRAME TERAKHIR dari tiap video → 6 frames
4. Dari 6 frame, generate 5 SCENE video (I2V lagi) → 5 videos
5. Stitch semua jadi 25 detik continuous → final video

Output: 25-second TikTok 9:16 viral video with smooth scene transitions.

Usage:
    python3 multi_stage_i2v.py --room kitchen_small --hook landlord_kitchen
"""

import argparse
import base64
import json
import os
import ssl
import subprocess
import time
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from typing import List, Optional, Dict

# ── CONFIG ────────────────────────────────────────────────────────────
NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "")
BYTEPLUS_API_KEY = os.environ.get("BYTEPLUS_API_KEY", "")

NVIDIA_IMAGE_URL = "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.1-dev"
BYTEPLUS_BASE_URL = "https://ark.ap-southeast.bytepluses.com/api/v3"
SEEDANCE_MODEL = "seedance-1-0-lite-t2v-250428"

FFMPEG = "/home/linuxbrew/.linuxbrew/bin/ffmpeg"

OUTPUT_DIR = Path("/tmp/multi_stage_i2v")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── LARRY PLAYBOOK CONCEPTS ─────────────────────────────────────────────
ROOMS = {
    "kitchen_small": "cozy rental kitchen, small apartment, budget friendly, L-shaped layout, minimal counter space",
    "kitchen_cozy": "warm welcoming kitchen, open layout, natural light, island counter, pendant lighting",
    "living_room_cozy": "comfortable living room, sectional sofa, warm colors, low coffee table, woven rug, plants",
    "bedroom_minimal": "minimalist bedroom, clean lines, neutral colors, platform bed, simple nightstand, large window",
}

HOOK_TEMPLATES = {
    "landlord_kitchen": "My landlord said I can't change anything, so I showed her what AI thinks our kitchen could look like",
    "parent_bedroom": "My mum was skeptical about AI interior design until I showed her this bedroom transformation",
    "roommate_living": "My flatmate thinks this style is impossible, so I proved them wrong with this AI living room design",
}


# ── HTTP HELPERS ─────────────────────────────────────────────────────
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
        path.write_bytes(r.read())
    return path


# ── STEP 1: GENERATE 6 IMAGES (NVIDIA FLUX) ───────────────────
def generate_stage1_images(room_desc: str) -> List[Path]:
    """Generate 6 images of the same room with NVIDIA Flux."""
    print(f"\n🎨 STEP 1: Generating 6 images (NVIDIA Flux)...")
    print(f"  Room: {room_desc[:50]}...")

    images = []
    for i in range(6):
        print(f"  [{i+1}/6] Generating image...")

        # Different style for each image
        styles = [
            "modern minimalist with clean white walls and natural wood furniture",
            "cozy warm tones with soft lighting and beige walls",
            "bold statement walls in deep blue or emerald green",
            "scandinavian light with white furniture and pale wood floors",
            "industrial chic with exposed brick and metal accents",
            "contemporary luxury with marble surfaces and gold accents",
        ]
        style = styles[i % len(styles)]

        prompt = f"""
        Photorealistic interior photo: {room_desc}
        Style: {style}
        High quality, professional photography, soft natural lighting
        Vertical orientation (9:16 portrait), 1080x1920
        Cinematic composition, wide angle view
        """.strip()

        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {NVIDIA_API_KEY}",
                "Accept": "application/json",
            }
            resp = post_json(NVIDIA_IMAGE_URL, {"prompt": prompt}, headers)

            artifacts = resp.get("artifacts", [])
            if not artifacts or artifacts[0].get("finishReason") != "SUCCESS":
                print(
                    f"    ❌ Failed: {artifacts[0].get('finishReason') if artifacts else 'No artifacts'}"
                )
                continue

            b64 = artifacts[0].get("base64", "")
            if not b64:
                print(f"    ❌ No base64 data")
                continue

            # Save image
            img_path = OUTPUT_DIR / f"stage1_img_{i+1:02d}.jpg"
            img_path.write_bytes(base64.b64decode(b64))

            size_kb = img_path.stat().st_size / 1024
            print(f"    ✅ Saved: {size_kb:.0f}KB")
            images.append(img_path)

        except Exception as e:
            print(f"    ❌ Error: {e}")

    print(f"\n✅ Generated {len(images)}/6 images")
    return images


# ── STEP 2: GENERATE VIDEO DARI IMAGE (I2V) ─────────────────────
def generate_stage2_videos(images: List[Path]) -> List[Dict]:
    """Generate video DARI tiap image via BytePlus Seedance I2V."""
    print(f"\n🎬 STEP 2: Generating videos FROM images (I2V)...")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {BYTEPLUS_API_KEY}",
    }

    videos = []
    for i, img_path in enumerate(images):
        print(f"\n  [{i+1}/6] Processing image: {img_path.name}")

        # Upload image to temp host (0x0.st for I2V)
        try:
            with open(img_path, "rb") as f:
                img_data = f.read()
            img_b64 = base64.b64encode(img_data).decode("utf-8")

            # Upload to 0x0.st
            upload_url = f"https://0x0.st"
            upload_data = urllib.parse.urlencode({"file": img_b64}).encode("utf-8")
            upload_req = urllib.request.Request(
                upload_url,
                data=upload_data,
                method="POST",
                headers={"Content-Type": "multipart/form-data"},
            )
            with urllib.request.urlopen(upload_req, timeout=60) as r:
                img_url = r.read().decode("utf-8").strip()

            print(f"    📤 Uploaded: {img_url[:60]}...")

        except Exception as e:
            print(f"    ⚠️  Upload failed: {e} — skipping")
            continue

        # Create task with image
        content = [
            {"type": "image_url", "image_url": {"url": img_url}, "role": "first_frame"},
            {
                "type": "text",
                "text": "Cinematic room tour, smooth camera movement, professional lighting",
            },
        ]

        payload = {
            "model": SEEDANCE_MODEL,
            "content": content,
            "ratio": "9:16",
        }

        try:
            resp = post_json(
                f"{BYTEPLUS_BASE_URL}/contents/generations/tasks",
                payload,
                headers,
            )
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8") if e.fp else str(e)
            print(f"    ❌ Create task HTTP {e.code}: {body[:200]}")
            continue

        task_id = resp.get("id")
        if not task_id:
            print(f"    ❌ No task_id: {resp}")
            continue

        print(f"    📋 Task: {task_id}")

        # Poll
        deadline = time.time() + 300
        attempt = 0
        video_url = None
        while time.time() < deadline:
            attempt += 1
            time.sleep(5)

            try:
                result = get_json(
                    f"{BYTEPLUS_BASE_URL}/contents/generations/tasks/{task_id}",
                    headers,
                )
            except Exception as e:
                print(f"    ⚠️  Poll error: {e}")
                continue

            status = result.get("status", "")
            print(f"    [{attempt:02d}] {status}")

            if status == "succeeded":
                video_url = result.get("content", {}).get("video_url", "")
                duration = result.get("duration", 5)
                print(f"    ✅ Video: {duration}s, {video_url[:60]}...")
                break
            elif status in ("failed", "cancelled"):
                err = result.get("error", {})
                print(f"    ❌ {status}: {err.get('message')}")
                break

        if not video_url:
            print(f"    ⚠️  Timeout — skipping")
            continue

        # Download video
        vid_path = OUTPUT_DIR / f"stage2_vid_{i+1:02d}.mp4"
        try:
            download_file(video_url, vid_path)
            size_mb = vid_path.stat().st_size / (1024 * 1024)
            print(f"    ⬇️  Downloaded: {size_mb:.2f}MB")

            videos.append(
                {
                    "path": str(vid_path),
                    "duration": result.get("duration", 5),
                    "video_url": video_url,
                }
            )

        except Exception as e:
            print(f"    ❌ Download error: {e}")

    print(f"\n✅ Generated {len(videos)}/6 videos")
    return videos


# ── STEP 3: EXTRACT FRAME TERAKHIR DARI VIDEO ─────────────────────
def extract_stage3_last_frames(videos: List[Dict]) -> List[Path]:
    """Extract last frame from each video using FFmpeg."""
    print(f"\n📷 STEP 3: Extracting last frame from {len(videos)} videos...")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {BYTEPLUS_API_KEY}",
    }

    frames = []
    for i, vid_info in enumerate(videos):
        vid_path = Path(vid_info["path"])
        print(f"\n  [{i+1}/6] Processing: {vid_path.name}")

        # Extract last frame
        frame_path = OUTPUT_DIR / f"stage3_frame_{i+1:02d}.jpg"

        cmd = [
            FFMPEG,
            "-sseof",
            "+fast",
            "-i",
            str(vid_path),
            "-frames:v",
            "1",
            "-q:v",
            "2",
            "-update",
            "1",
            str(frame_path),
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"    ❌ FFmpeg error: {result.stderr[-200:]}")
            continue

        size_kb = frame_path.stat().st_size / 1024
        print(f"    ✅ Frame: {size_kb:.0f}KB")
        frames.append(frame_path)

    print(f"\n✅ Extracted {len(frames)} last frames")
    return frames


# ── STEP 4: GENERATE 5 SCENE VIDEO DARI FRAME ──────────────────────
def generate_stage4_scenes(frames: List[Path]) -> List[Dict]:
    """Generate 5 scene videos FROM last frames via BytePlus I2V."""
    print(f"\n🎬 STEP 4: Generating 5 scene videos FROM last frames (I2V)...")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {BYTEPLUS_API_KEY}",
    }

    scenes = []
    for i in range(5):
        print(f"\n  [{i+1}/5] Generating scene...")

        # Use frame from stage 3
        frame_idx = i % len(frames)
        frame_path = frames[frame_idx]
        print(f"    Using frame: {frame_path.name}")

        # Upload frame to temp host
        try:
            with open(frame_path, "rb") as f:
                frame_data = f.read()
            frame_b64 = base64.b64encode(frame_data).decode("utf-8")

            upload_url = f"https://0x0.st"
            upload_data = urllib.parse.urlencode({"file": frame_b64}).encode("utf-8")
            upload_req = urllib.request.Request(
                upload_url,
                data=upload_data,
                method="POST",
                headers={"Content-Type": "multipart/form-data"},
            )
            with urllib.request.urlopen(upload_req, timeout=60) as r:
                img_url = r.read().decode("utf-8").strip()

            print(f"    📤 Uploaded: {img_url[:60]}...")

        except Exception as e:
            print(f"    ⚠️  Upload failed: {e} — skipping")
            continue

        # Create scene prompt
        scene_prompts = [
            "Smooth camera movement from left to right, revealing details",
            "Subtle zoom in towards center focus point",
            "Pan from right to left with slow motion effect",
            "Wide angle sweep from above showing entire room",
            "Rotating perspective around center of room",
        ]
        scene_prompt = scene_prompts[i]

        content = [
            {"type": "image_url", "image_url": {"url": img_url}, "role": "first_frame"},
            {
                "type": "text",
                "text": f"Cinematic room tour. {scene_prompt}. Professional lighting, smooth transitions",
            },
        ]

        payload = {
            "model": SEEDANCE_MODEL,
            "content": content,
            "ratio": "9:16",
            "duration": 5,  # 5s per scene
        }

        try:
            resp = post_json(
                f"{BYTEPLUS_BASE_URL}/contents/generations/tasks",
                payload,
                headers,
            )
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8") if e.fp else str(e)
            print(f"    ❌ Create task HTTP {e.code}: {body[:200]}")
            continue

        task_id = resp.get("id")
        if not task_id:
            print(f"    ❌ No task_id: {resp}")
            continue

        print(f"    📋 Task: {task_id}")

        # Poll
        deadline = time.time() + 300
        attempt = 0
        video_url = None
        while time.time() < deadline:
            attempt += 1
            time.sleep(5)

            try:
                result = get_json(
                    f"{BYTEPLUS_BASE_URL}/contents/generations/tasks/{task_id}",
                    headers,
                )
            except Exception as e:
                print(f"    ⚠️  Poll error: {e}")
                continue

            status = result.get("status", "")
            print(f"    [{attempt:02d}] {status}")

            if status == "succeeded":
                video_url = result.get("content", {}).get("video_url", "")
                print(f"    ✅ Scene video: {video_url[:60]}...")
                break
            elif status in ("failed", "cancelled"):
                err = result.get("error", {})
                print(f"    ❌ {status}: {err.get('message')}")
                break

        if not video_url:
            print(f"    ⚠️  Timeout — skipping")
            continue

        # Download scene video
        scene_path = OUTPUT_DIR / f"stage4_scene_{i+1:02d}.mp4"
        try:
            download_file(video_url, scene_path)
            size_mb = scene_path.stat().st_size / (1024 * 1024)
            print(f"    ⬇️  Downloaded: {size_mb:.2f}MB")

            scenes.append(
                {
                    "path": str(scene_path),
                    "duration": result.get("duration", 5),
                    "video_url": video_url,
                }
            )

        except Exception as e:
            print(f"    ❌ Download error: {e}")

    print(f"\n✅ Generated {len(scenes)}/5 scene videos")
    return scenes


# ── STEP 5: STITCH SEMUA JADI 25 DETIK ───────────────────────────
def stitch_stage5_final(videos: List[Dict], output_path: Path) -> bool:
    """Stitch all videos together into 25-second continuous video."""
    print(f"\n🎞 STEP 5: Stitching {len(videos)} videos → 25 seconds...")

    # Create concat file
    concat_file = OUTPUT_DIR / "concat.txt"
    with open(concat_file, "w") as f:
        for vid in videos:
            f.write(f"file '{vid['path']}'\n")

    # 25 seconds / 5 videos = 5 seconds each (approx)
    target_duration = 25

    cmd = [
        FFMPEG,
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_file),
        "-c:v",
        "libx264",
        "-c:a",
        "copy",
        "-preset",
        "fast",
        "-crf",
        "28",
        "-t",
        str(target_duration),
        "-pix_fmt",
        "yuv420p",
        "-r",
        "24",
        "-y",
        str(output_path),
    ]

    print(f"  ⚙️  Running FFmpeg...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"  ❌ FFmpeg error: {result.stderr[-500:]}")
        return False

    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"  ✅ Final: {output_path.name} ({size_mb:.2f}MB)")

    # Verify duration
    cmd_verify = [
        FFMPEG,
        "-i",
        str(output_path),
        "-f",
        "null",
        "-",
    ]
    verify = subprocess.run(cmd_verify, capture_output=True, text=True)

    for line in verify.stderr.split("\n"):
        if "Duration:" in line:
            dur_str = line.split("Duration:")[1].split(",")[0].strip()
            print(f"  ⏱️  Duration: {dur_str}")
            break

    return True


# ── MAIN ───────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Multi-Stage I2V Video Generator — Larry Playbook Advanced Pipeline"
    )
    parser.add_argument("--room", required=True, choices=list(ROOMS.keys()))
    parser.add_argument(
        "--hook", default="landlord_kitchen", choices=list(HOOK_TEMPLATES.keys())
    )
    parser.add_argument(
        "--skip-stage1", action="store_true", help="Skip image generation"
    )
    parser.add_argument(
        "--skip-stage2", action="store_true", help="Skip I2V from images"
    )
    parser.add_argument(
        "--skip-stage3", action="store_true", help="Skip last frame extraction"
    )
    parser.add_argument(
        "--skip-stage4", action="store_true", help="Skip scene generation"
    )
    parser.add_argument(
        "--skip-stage5", action="store_true", help="Skip final stitching"
    )
    args = parser.parse_args()

    print("=" * 70)
    print("🚀 MULTI-STAGE I2V VIDEO GENERATOR")
    print("=" * 70)
    print(f"Room: {args.room}")
    print(f"Hook: {args.hook}")
    print()

    stage1_images = None
    stage2_videos = None
    stage3_frames = None
    stage4_scenes = None

    # STEP 1: Generate 6 images
    if not args.skip_stage1:
        stage1_images = generate_stage1_images(ROOMS[args.room])
        if len(stage1_images) < 6:
            print("\n💥 Not enough images — cannot continue")
            return
    else:
        # Find existing images if skipped
        stage1_images = sorted(OUTPUT_DIR.glob("stage1_img_*.jpg"))[:6]

    # STEP 2: Generate videos FROM images
    if not args.skip_stage2:
        stage2_videos = generate_stage2_videos(stage1_images)
        if len(stage2_videos) < 6:
            print("\n💥 Not enough videos — cannot continue")
            return
    else:
        stage2_videos = sorted(OUTPUT_DIR.glob("stage2_vid_*.mp4"))[:6]

    # STEP 3: Extract last frames
    if not args.skip_stage3:
        stage3_frames = extract_stage3_last_frames(stage2_videos)
        if len(stage3_frames) < 6:
            print("\n💥 Not enough frames — cannot continue")
            return
    else:
        stage3_frames = sorted(OUTPUT_DIR.glob("stage3_frame_*.jpg"))[:6]

    # STEP 4: Generate 5 scene videos
    if not args.skip_stage4:
        stage4_scenes = generate_stage4_scenes(stage3_frames)
        if len(stage4_scenes) < 5:
            print("\n💥 Not enough scenes — cannot continue")
            return
    else:
        stage4_scenes = sorted(OUTPUT_DIR.glob("stage4_scene_*.mp4"))[:5]

    # STEP 5: Stitch final video
    if not args.skip_stage5:
        output_path = OUTPUT_DIR / f"larry_{args.room}_{args.hook}_final.mp4"
        stitch_stage5_final(stage4_scenes, output_path)

    # Summary
    print("\n" + "=" * 70)
    print("✅ PIPELINE COMPLETE!")
    print("=" * 70)
    print(f"   Images: {len(stage1_images) if stage1_images else 'skipped'}")
    print(f"   Stage2 Videos: {len(stage2_videos) if stage2_videos else 'skipped'}")
    print(f"   Stage3 Frames: {len(stage3_frames) if stage3_frames else 'skipped'}")
    print(f"   Stage4 Scenes: {len(stage4_scenes) if stage4_scenes else 'skipped'}")
    print(f"   Final: {output_path}")
    print()
    print("📊 WORKFLOW:")
    print("   1. 6 images → 6 videos (I2V)")
    print("   2. 6 videos → 6 last frames")
    print("   3. 6 frames → 5 scene videos (I2V)")
    print("   4. 5 scenes → 25s final video")
    print("=" * 70)

    # Save result
    result = {
        "room": args.room,
        "hook": args.hook,
        "stage1_images": [str(p) for p in (stage1_images or [])],
        "stage2_videos": [str(p) for p in (stage2_videos or [])],
        "stage3_frames": [str(p) for p in (stage3_frames or [])],
        "stage4_scenes": [str(p) for p in (stage4_scenes or [])],
    }

    result_file = OUTPUT_DIR / "pipeline_result.json"
    with open(result_file, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\n💾 Saved: {result_file}")


if __name__ == "__main__":
    main()
