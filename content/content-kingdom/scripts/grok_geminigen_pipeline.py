#!/usr/bin/env python3
"""
Grok-Api + GeminiGen End-to-End Demo
====================================
Demonstrates the full pipeline:
  1. Grok-Api generates video script + scene prompts (free LLM)
  2. GeminiGen generates images (nano-banana-pro)
  3. GeminiGen generates video scenes (grok-3)
  4. FFmpeg concatenates scenes into final video

Requires: Grok-Api server running at http://localhost:6969

Usage:
  python3 grok_geminigen_pipeline.py
  python3 grok_geminigen_pipeline.py --scene-chain 4scenes  # 4-scene chain
  python3 grok_geminigen_pipeline.py --image-only            # Image only
  python3 grok_geminigen_pipeline.py --skip-server-start     # Assume server running
"""

import argparse
import json
import subprocess
import shutil
import sys
import time
import tempfile
import os
import urllib.request
import urllib.error
from pathlib import Path
from subprocess import run

SKILL_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_DIR))

GROK_API_REPO = "/home/openclaw/.openclaw/workspace/projects/grok-api"


def check_ffmpeg() -> bool:
    return shutil.which("ffmpeg") is not None


def start_grok_server(port: int = 6969, workers: int = 1) -> bool:
    print(f"Checking Grok-Api server at http://localhost:{port}...")
    try:
        r = run(
            [
                "curl",
                "-s",
                "-o",
                "/dev/null",
                "-w",
                "%{http_code}",
                f"http://localhost:{port}/docs",
                "--max-time",
                "3",
            ],
            capture_output=True,
            text=True,
        )
        if r.stdout.strip() == "200":
            print("Server already running")
            return True
    except Exception:
        pass

    print(f"Starting Grok-Api server (port {port}, {workers} workers)...")
    proc = subprocess.Popen(
        [
            "/usr/bin/python3",
            "-m",
            "uvicorn",
            "api_server:app",
            "--host",
            "0.0.0.0",
            "--port",
            str(port),
            "--workers",
            str(workers),
        ],
        cwd=GROK_API_REPO,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid,
    )

    for i in range(15):
        time.sleep(1)
        try:
            r = run(
                [
                    "curl",
                    "-s",
                    "-o",
                    "/dev/null",
                    "-w",
                    "%{http_code}",
                    f"http://localhost:{port}/docs",
                    "--max-time",
                    "2",
                ],
                capture_output=True,
                text=True,
            )
            if r.stdout.strip() == "200":
                print(f"Server ready after {i + 1}s")
                return True
        except Exception:
            pass
    print("Server failed to start")
    return False


def grok_ask(message: str, model: str = "grok-3-fast", port: int = 6969) -> dict:
    payload = json.dumps(
        {
            "proxy": "none",
            "message": message,
            "model": model,
            "extra_data": {},
        }
    ).encode()
    r = run(
        [
            "curl",
            "-s",
            "-X",
            "POST",
            f"http://localhost:{port}/ask",
            "-H",
            "Content-Type: application/json",
            "-d",
            payload,
        ],
        capture_output=True,
        text=True,
    )
    try:
        return json.loads(r.stdout)
    except Exception:
        return {"status": "error", "error": r.stdout[:200]}


def geminigen_image(client, prompt: str) -> str:
    print(f"  Generating image: {prompt[:60]}...")
    resp = client.generate_image(
        prompt=prompt,
        model="nano-banana-pro",
        style="Photorealistic",
        output_format="jpeg",
        resolution="1K",
        aspect_ratio="4:5",
    )
    uuid = resp.get("uuid") or resp.get("id", "")
    if not uuid:
        return ""
    result = client.wait_for_completion(uuid, timeout=120)
    url = client.get_image_url(result)
    print(f"  Image ready: {url[:60]}...")
    return url


def geminigen_video(client, prompt: str, duration: int = 6) -> str:
    print(f"  Generating video: {prompt[:60]}...")
    resp = client.generate_video(prompt=prompt, duration=duration)
    uuid = resp.get("uuid") or resp.get("id", "")
    if not uuid:
        return ""
    result = client.wait_for_completion(uuid, timeout=300)
    url = client.get_video_url(result)
    print(f"  Video ready: {url[:60]}...")
    return url


def geminigen_extend_video(
    client, prompt: str, ref_history: str, ref_image_path: str
) -> str:
    print(f"  Extending video: {prompt[:60]}...")
    resp = client.generate_video_extend(
        prompt=prompt,
        ref_history=ref_history,
        ref_image_path=ref_image_path,
    )
    uuid = resp.get("uuid") or resp.get("id", "")
    if not uuid:
        return ""
    result = client.wait_for_completion(uuid, timeout=300)
    url = client.get_video_url(result)
    print(f"  Extended video ready: {url[:60]}...")
    return url


def geminigen_wait(client, uuid: str, timeout: int = 300) -> dict:
    start = time.time()
    while time.time() - start < timeout:
        result = client.poll(uuid)
        status = result.get("status", "").lower()
        if status in ("completed", "success", "done"):
            return result
        if status in ("failed", "error"):
            return {"error": f"Generation failed: {result.get('message', status)}"}
        time.sleep(5)
    return {"error": "Timeout waiting for generation"}


def download_file(url: str, path: Path) -> bool:
    try:
        urllib.request.urlretrieve(url, str(path))
        return True
    except Exception:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=60) as resp, open(path, "wb") as f:
                shutil.copyfileobj(resp, f)
            return True
        except Exception:
            return False


def extract_last_frame(video_path: Path, output_path: Path) -> bool:
    result = run(
        [
            "ffmpeg",
            "-sseof",
            "-1",
            "-i",
            str(video_path),
            "-frames:v",
            "1",
            "-f",
            "image2",
            str(output_path),
        ],
        capture_output=True,
    )
    return result.returncode == 0


def concatenate_videos(video_paths: list[Path], output_path: Path) -> bool:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        for vp in video_paths:
            f.write(f"file '{vp.absolute()}'\n")
        list_file = f.name

    result = run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            list_file,
            "-c",
            "copy",
            str(output_path),
        ],
        capture_output=True,
    )
    os.unlink(list_file)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="Grok-Api + GeminiGen Pipeline")
    parser.add_argument(
        "--scene-chain",
        choices=["1scene", "2scenes", "4scenes"],
        default="1scene",
        help="Number of video scenes",
    )
    parser.add_argument(
        "--image-only", action="store_true", help="Skip video generation"
    )
    parser.add_argument(
        "--skip-server-start",
        action="store_true",
        help="Assume Grok-Api server is running",
    )
    parser.add_argument("--port", type=int, default=6969, help="Grok-Api server port")
    args = parser.parse_args()

    scene_counts = {"1scene": 1, "2scenes": 2, "4scenes": 4}
    num_scenes = scene_counts[args.scene_chain]

    print(f"\n{'=' * 60}")
    print(f"GROK-API + GEMINIGEN END-TO-END PIPELINE")
    print(f"Scenes: {num_scenes} | Image only: {args.image_only}")
    print(f"{'=' * 60}\n")

    if not args.skip_server_start:
        if not start_grok_server(port=args.port):
            sys.exit(1)

    from modules.geminigen_client import GeminiGenClient

    gg_client = GeminiGenClient()

    print(f"\n[Step 1] Grok-Api: Generating script + scene prompts...")
    product = "AI Digital Tools untuk Bisnis Indonesia"
    prompt = (
        f"Write a {num_scenes * 6}-second motivational video script about {product}. "
        "Format: HOOK | BODY (3 key points) | CTA. "
        f"Then break it into exactly {num_scenes} scene prompts for AI video generation. "
        "Each scene prompt should be 60-100 words describing the visual scene. "
        "Return the script first, then scene prompts as a JSON array "
        '[{"scene": 1, "prompt": "..."}, ...]'
    )

    resp = grok_ask(prompt, model="grok-3-fast", port=args.port)
    if resp.get("status") != "success":
        print(f"Grok-Api failed: {resp.get('error')}")
        sys.exit(1)

    text = resp.get("response", "")
    print(f"Script received ({len(text)} chars)")

    import re

    scenes = []
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        try:
            scenes = json.loads(match.group())
        except Exception:
            scenes = []

    if not scenes:
        print("Warning: Could not parse scene prompts from response")
        scenes = [{"scene": 1, "prompt": text[:200]}]

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        print(f"\n[Step 2] GeminiGen: Generating {len(scenes)} scene image(s)...")
        image_urls = []
        for scene in scenes[:num_scenes]:
            url = geminigen_image(gg_client, scene.get("prompt", product))
            image_urls.append(url)

        if args.image_only:
            print("\n[Done] Image-only mode — skipping video generation")
            print(f"Images: {image_urls}")
            return

        print(f"\n[Step 3] GeminiGen: Generating {num_scenes} scene video(s)...")
        video_urls = []
        ref_history = None
        ref_image_path = None

        for i, (scene, img_url) in enumerate(zip(scenes[:num_scenes], image_urls)):
            if i == 0:
                video_url = geminigen_video(
                    gg_client,
                    scene.get("prompt", product),
                    duration=6,
                )
            else:
                img_path = tmp_path / f"ref_{i}.png"
                download_file(img_url, img_path)
                video_url = geminigen_extend_video(
                    gg_client,
                    scene.get("prompt", product),
                    ref_history=ref_history,
                    ref_image_path=str(img_path),
                )

            video_urls.append(video_url)

            vid_path = tmp_path / f"scene_{i}.mp4"
            download_file(video_url, vid_path)
            ref_image_path = tmp_path / f"lastframe_{i}.png"
            extract_last_frame(vid_path, ref_image_path)

            resp_data = gg_client.poll_by_url(video_url)
            ref_history = resp_data.get("id") or resp_data.get("uuid", "")

        print(f"\n[Step 4] FFmpeg: Concatenating {len(video_urls)} videos...")
        if len(video_urls) > 1:
            video_paths = [tmp_path / f"scene_{i}.mp4" for i in range(len(video_urls))]
            final_output = SKILL_DIR / "output" / f"final_video_{int(time.time())}.mp4"
            final_output.parent.mkdir(parents=True, exist_ok=True)
            ok = concatenate_videos(video_paths, final_output)
            if ok:
                print(f"Final video saved: {final_output}")
            else:
                print("FFmpeg concatenation failed")
                print(f"Individual videos: {video_urls}")
        else:
            single = tmp_path / "scene_0.mp4"
            final = SKILL_DIR / "output" / f"final_video_{int(time.time())}.mp4"
            final.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(single, final)
            print(f"Final video saved: {final}")

    print(f"\n{'=' * 60}")
    print("PIPELINE COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    if not check_ffmpeg():
        print("ERROR: ffmpeg not found. Install with: apt install ffmpeg")
        sys.exit(1)
    main()
