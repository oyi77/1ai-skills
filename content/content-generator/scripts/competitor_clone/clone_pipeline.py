"""
Competitor Clone Pipeline — Main Orchestrator
Full pipeline: Video In → Scene Analysis → Better Images → Better Video + VO Out

Usage:
    python clone_pipeline.py --video /path/to/competitor.mp4 --category minuman
    python clone_pipeline.py --url https://tiktok.com/... --category beauty
"""

import os, sys, json, base64, io, time, subprocess, asyncio
import urllib.request, urllib.error
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from scene_extractor import extract_scenes, extract_audio, get_video_info
from scene_analyzer import analyze_scene, transcribe_audio, improve_script
# Smart routing helpers (defined in this file below)

NVIDIA_KEY   = os.environ.get("NVIDIA_API_KEY")
BYTEPLUS_KEY = os.environ.get("BYTEPLUS_API_KEY")
GROQ_KEY     = os.environ.get("GROQ_API_KEY")
BYTEPLUS_BASE = "https://ark.ap-southeast.bytepluses.com/api/v3"
FFMPEG = "/home/linuxbrew/.linuxbrew/bin/ffmpeg"


# ─── STEP 1: DOWNLOAD VIDEO (if URL) ─────────────────────────────────
def download_video(url: str, output_dir: str) -> str:
    """Download video from TikTok/Instagram/YouTube using yt-dlp"""
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "competitor_video.mp4")
    print(f"  📥 Downloading: {url[:60]}...")
    cmd = [
        "yt-dlp", "-f", "best[ext=mp4]/best",
        "--no-playlist", "-o", out_path, url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0 and os.path.exists(out_path):
        size_mb = os.path.getsize(out_path) / 1024 / 1024
        print(f"  ✅ Downloaded: {out_path} ({size_mb:.1f} MB)")
        return out_path
    else:
        raise Exception(f"Download failed: {result.stderr[-300:]}")


# ─── STEP 2: GENERATE BETTER IMAGE PER SCENE ─────────────────────────
def detect_scene_type(analysis: dict) -> str:
    """
    Returns: 'product_only' | 'model_only' | 'product_with_model' | 'other'
    """
    scene_type = analysis.get("scene_type", "")
    has_person  = analysis.get("has_person", False)
    has_product = analysis.get("has_product", True)

    if scene_type == "product_with_model" or (has_person and has_product):
        return "product_with_model"
    elif scene_type in ("model_only", "talking_head") or (has_person and not has_product):
        return "model_only"
    elif scene_type == "product_only" or (has_product and not has_person):
        return "product_only"
    return "other"


def build_upgrade_prompt(analysis: dict, scene_type: str) -> str:
    """Build the best prompt based on scene type"""
    base = analysis.get("upgrade_prompt", "hyperrealistic commercial product shot, 8K, cinematic")
    mood  = analysis.get("mood", "professional")
    style = analysis.get("visual_style", "dark_moody")
    palette = analysis.get("color_palette", "dark, dramatic")

    hr_suffix = (
        ", hyperrealistic photography, ultra detailed, 8K, "
        "professional commercial quality, sharp focus, film grain"
    )

    if scene_type == "product_only":
        return (
            f"{base}, no people, product focus, "
            f"{mood} mood, {palette} color palette"
            + hr_suffix
            + ", Canon EOS R5 100mm macro, studio strobe lighting"
        )
    elif scene_type == "model_only":
        person_desc = analysis.get("person_description", "person in stylish outfit")
        return (
            f"professional lifestyle photography, {person_desc}, "
            f"{mood} mood, {base}, natural authentic expression"
            + hr_suffix
            + ", Sony A7III 85mm f/1.4, bokeh background"
        )
    elif scene_type == "product_with_model":
        person_desc = analysis.get("person_description", "stylish person")
        product_desc = analysis.get("product_description", "the product")
        return (
            f"professional commercial photography, {person_desc} holding or using {product_desc}, "
            f"natural interaction with product, {mood} mood, {palette} color palette, "
            f"lifestyle product advertisement"
            + hr_suffix
            + ", Sony A7III 50mm f/1.8, natural studio lighting"
        )
    else:
        return base + hr_suffix


def generate_better_image(upgrade_prompt: str, scene_id: int, output_dir: str,
                           scene_type: str = "product_only") -> str:
    """
    Generate hyperrealistic upgraded image for a scene.
    Smart model routing:
    - product_only      → Flux.1-dev (best for objects)
    - model_only        → SD3 Medium (handles people)
    - product_with_model → SD3 Medium (people + product)
    - other             → Flux first, fallback SD3
    """
    out_path = os.path.join(output_dir, f"scene_{scene_id:02d}_upgraded.jpg")
    if os.path.exists(out_path):
        print(f"    Scene {scene_id}: Image exists ✅")
        return out_path

    needs_person = scene_type in ("model_only", "product_with_model")

    def _call_flux(prompt):
        url = "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.1-dev"
        headers = {"Authorization": f"Bearer {NVIDIA_KEY}", "Content-Type": "application/json", "Accept": "application/json"}
        payload = json.dumps({"prompt": prompt}).encode()
        req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = json.loads(resp.read())
        art = data.get("artifacts", [{}])[0]
        if art.get("finishReason") == "CONTENT_FILTERED":
            return None
        return base64.b64decode(art.get("base64", ""))

    def _call_sd3(prompt):
        url = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-3-medium"
        headers = {"Authorization": f"Bearer {NVIDIA_KEY}", "Content-Type": "application/json", "Accept": "application/json"}
        payload = json.dumps({"prompt": prompt}).encode()
        req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = json.loads(resp.read())
        return base64.b64decode(data.get("image", ""))

    try:
        if needs_person:
            print(f"    Scene {scene_id}: [{scene_type}] → SD3 Medium")
            decoded = _call_sd3(upgrade_prompt)
        else:
            print(f"    Scene {scene_id}: [{scene_type}] → Flux.1-dev")
            decoded = _call_flux(upgrade_prompt)
            if decoded is None or len(decoded) < 10000:
                print(f"    Scene {scene_id}: Flux filtered → fallback SD3")
                decoded = _call_sd3(upgrade_prompt)

        if not decoded or len(decoded) < 10000:
            raise Exception("Image too small or empty")

        with open(out_path, "wb") as f:
            f.write(decoded)
        print(f"    Scene {scene_id}: ✅ ({len(decoded)//1024} KB)")
        return out_path

    except Exception as e:
        print(f"    Scene {scene_id}: ❌ Failed — {e}")
        return None


# ─── STEP 3: ANIMATE SCENE (I2V) ─────────────────────────────────────
def prepare_image_for_i2v(image_path: str) -> bytes:
    """
    Pre-crop image to exact 9:16 portrait (720x1280) BEFORE sending to I2V.
    Prevents Seedance from doing its own flip/rotate when given a square image.
    """
    img = Image.open(image_path).convert("RGB")
    W, H = img.size
    target_w, target_h = 720, 1280
    scale = target_h / H
    new_w = int(W * scale)
    img_scaled = img.resize((new_w, target_h), Image.LANCZOS)
    left = max(0, (new_w - target_w) // 2)
    img_cropped = img_scaled.crop((left, 0, left + target_w, target_h))
    buf = io.BytesIO()
    img_cropped.save(buf, format="JPEG", quality=95)
    return buf.getvalue()


def submit_i2v(image_path: str, anim_prompt: str, duration: int = 5) -> str:
    """Submit I2V task to BytePlus Seedance Pro"""
    # Pre-crop to 9:16 so Seedance doesn't flip/transform the source image
    img_bytes = prepare_image_for_i2v(image_path)
    img_b64 = base64.b64encode(img_bytes).decode()

    payload = json.dumps({
        "model": "seedance-1-0-pro-i2v-250528",
        "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}, "role": "first_frame"},
            {"type": "text", "text": anim_prompt}
        ],
        "duration": min(duration, 10),
        "seed": -1
        # ratio omitted — image already is 9:16
    }).encode()

    headers = {"Authorization": f"Bearer {BYTEPLUS_KEY}", "Content-Type": "application/json"}
    req = urllib.request.Request(
        f"{BYTEPLUS_BASE}/contents/generations/tasks",
        data=payload, headers=headers, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
        return result.get("id")
    except Exception as e:
        print(f"    I2V submit failed: {e}")
        return None


def poll_i2v(task_id: str, scene_id: int, duration: float, output_dir: str) -> str:
    """Poll I2V task and download result"""
    headers = {"Authorization": f"Bearer {BYTEPLUS_KEY}"}
    out_tmp = os.path.join(output_dir, f"scene_{scene_id:02d}_anim_raw.mp4")
    out_path = os.path.join(output_dir, f"scene_{scene_id:02d}_animated.mp4")

    for i in range(72):  # max 6 minutes
        time.sleep(5)
        try:
            req = urllib.request.Request(
                f"{BYTEPLUS_BASE}/contents/generations/tasks/{task_id}",
                headers=headers
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
            status = data.get("status")
            if (i+1) % 3 == 0:
                print(f"    Scene {scene_id}: I2V [{(i+1)*5}s] {status}")
            if status == "succeeded":
                video_url = data["content"]["video_url"]
                urllib.request.urlretrieve(video_url, out_tmp)
                # Loop to target duration
                cmd = [FFMPEG, "-y", "-stream_loop", "-1", "-i", out_tmp,
                       "-t", str(duration), "-c", "copy", out_path]
                subprocess.run(cmd, capture_output=True)
                print(f"    Scene {scene_id}: Animated ✅")
                return out_path
            elif status in ["failed", "cancelled"]:
                print(f"    Scene {scene_id}: I2V failed ❌")
                return None
        except Exception as e:
            print(f"    Scene {scene_id}: Poll error {e}")
    return None


# ─── STEP 4: GENERATE VOICEOVER ──────────────────────────────────────
async def generate_voiceover(text: str, scene_id: int, output_dir: str) -> str:
    """Generate Indonesian voiceover with Edge TTS"""
    import edge_tts
    out_path = os.path.join(output_dir, f"vo_{scene_id:02d}.mp3")
    voice = "id-ID-GadisNeural"
    communicate = edge_tts.Communicate(text, voice, rate="+5%")
    await communicate.save(out_path)
    return out_path


# ─── STEP 5: COMPOSE SCENE (video + VO) ──────────────────────────────
def compose_scene(video_path: str, audio_path: str, duration: float,
                  scene_id: int, output_dir: str) -> str:
    """Merge animated video with voiceover"""
    out_path = os.path.join(output_dir, f"scene_{scene_id:02d}_composed.mp4")
    cmd = [
        FFMPEG, "-y",
        "-i", video_path,
        "-i", audio_path,
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "128k",
        "-t", str(duration), "-shortest",
        "-pix_fmt", "yuv420p",
        out_path
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode == 0:
        return out_path
    print(f"  Compose error: {result.stderr.decode()[-200:]}")
    return None


# ─── STEP 6: FINAL STITCH ────────────────────────────────────────────
def stitch_final(composed_paths: list, output_dir: str, project_name: str) -> str:
    """Concatenate all composed scenes into final video"""
    list_file = os.path.join(output_dir, "concat_list.txt")
    with open(list_file, "w") as f:
        for p in composed_paths:
            f.write(f"file '{p}'\n")

    final = os.path.join(output_dir, f"{project_name}_FINAL.mp4")
    cmd = [
        FFMPEG, "-y",
        "-f", "concat", "-safe", "0", "-i", list_file,
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "128k",
        "-pix_fmt", "yuv420p",
        final
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode == 0:
        size_mb = os.path.getsize(final) / 1024 / 1024
        print(f"\n🎉 FINAL VIDEO: {final} ({size_mb:.1f} MB)")
        return final
    else:
        print(f"Stitch error: {result.stderr.decode()[-300:]}")
        return None


# ─── MAIN PIPELINE ────────────────────────────────────────────────────
async def run_pipeline(
    video_path: str = None,
    video_url: str = None,
    category: str = "minuman",
    project_name: str = "competitor_clone",
    output_base: str = "/home/openclaw/.openclaw/workspace/output/competitor_clones"
):
    print("=" * 60)
    print("🕵️  COMPETITOR CLONE PIPELINE")
    print("=" * 60)

    output_dir = os.path.join(output_base, project_name)
    os.makedirs(output_dir, exist_ok=True)

    # ── Download if URL ──
    if video_url and not video_path:
        video_path = download_video(video_url, output_dir)

    if not video_path or not os.path.exists(video_path):
        raise Exception("No valid video path provided")

    # ── Extract scenes ──
    print("\n📽️  Step 1: Extracting scenes...")
    scenes = extract_scenes(video_path, output_dir)
    n = len(scenes)
    print(f"  Total scenes: {n}")

    # ── Extract audio ──
    print("\n🎙️  Step 2: Extracting audio...")
    audio_path = extract_audio(video_path, output_dir)

    # ── Transcribe ──
    original_script = ""
    if audio_path:
        original_script = transcribe_audio(audio_path)

    # ── Analyze scenes ──
    print(f"\n🧠 Step 3: Analyzing {n} scenes with AI...")
    analyses = []
    for scene in scenes:
        print(f"  Analyzing Scene {scene['id']}...")
        analysis = analyze_scene(scene, category)
        scene["analysis"] = analysis
        analyses.append((scene, analysis))
        print(f"    Type: {analysis.get('scene_type')} | Style: {analysis.get('visual_style')} | Mood: {analysis.get('mood')}")

    # ── Improve script ──
    print("\n✍️  Step 4: Rewriting VO script (better than competitor)...")
    improved = improve_script(original_script, analyses, category, GROQ_KEY)
    scripts = {s["scene"]: s["vo"] for s in improved.get("improved_script", [])}
    print(f"  Hook strategy: {improved.get('hook_analysis', 'N/A')[:80]}")
    print(f"  Overall: {improved.get('overall_strategy', 'N/A')[:80]}")

    # ── Generate images ──
    print(f"\n🖼️  Step 5: Generating upgraded images ({n} scenes)...")
    image_paths = {}
    for scene, analysis in analyses:
        sid = scene["id"]
        stype = detect_scene_type(analysis)
        upgrade_prompt = build_upgrade_prompt(analysis, stype)
        print(f"  Scene {sid} type: [{stype}]")
        img_path = generate_better_image(upgrade_prompt, sid, output_dir, stype)
        image_paths[sid] = img_path or scene["keyframe"]  # Fallback to original keyframe

    # ── Submit I2V tasks ──
    print(f"\n🎬 Step 6: Submitting I2V animation tasks...")
    i2v_tasks = {}
    for scene, analysis in analyses:
        sid = scene["id"]
        if image_paths.get(sid):
            anim_prompt = analysis.get("upgrade_animation", "cinematic slow motion, professional camera movement")
            task_id = submit_i2v(image_paths[sid], anim_prompt, min(int(scene["duration"]), 10))
            if task_id:
                i2v_tasks[sid] = (task_id, scene["duration"])
                print(f"  Scene {sid}: Task submitted ✅ ({task_id})")

    # ── Generate VOs ──
    print(f"\n🎙️  Step 7: Generating voiceovers...")
    vo_paths = {}
    for scene, _ in analyses:
        sid = scene["id"]
        vo_text = scripts.get(sid, f"Produk terbaik untuk kamu. Scene {sid}.")
        vo_path = await generate_voiceover(vo_text, sid, output_dir)
        vo_paths[sid] = vo_path
        print(f"  Scene {sid} VO: {vo_text[:60]}... ✅")

    # ── Poll I2V ──
    print(f"\n⏳ Step 8: Polling I2V results...")
    animated_paths = {}
    for sid, (task_id, duration) in i2v_tasks.items():
        anim_path = poll_i2v(task_id, sid, duration, output_dir)
        animated_paths[sid] = anim_path

    # ── Compose scenes ──
    print(f"\n🎞️  Step 9: Composing scenes...")
    composed = []
    for scene, _ in analyses:
        sid = scene["id"]
        vid = animated_paths.get(sid) or image_paths.get(sid)
        vo  = vo_paths.get(sid)
        if vid and vo:
            # If it's an image (not video), convert to short video first
            if vid.endswith(".jpg") or vid.endswith(".png"):
                img_vid = os.path.join(output_dir, f"scene_{sid:02d}_static.mp4")
                subprocess.run([
                    FFMPEG, "-y", "-loop", "1", "-i", vid,
                    "-t", str(scene["duration"]),
                    "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
                    img_vid
                ], capture_output=True)
                vid = img_vid

            c = compose_scene(vid, vo, scene["duration"], sid, output_dir)
            if c:
                composed.append(c)
                print(f"  Scene {sid} ✅")

    # ── Final stitch ──
    print(f"\n✂️  Step 10: Stitching final video...")
    final = stitch_final(composed, output_dir, project_name)

    # ── Save report ──
    report = {
        "project": project_name,
        "category": category,
        "original_script": original_script,
        "improved_script": improved.get("improved_script", []),
        "strategy": improved.get("overall_strategy", ""),
        "scenes": [
            {
                "id": s["id"],
                "duration": s["duration"],
                "original_keyframe": s["keyframe"],
                "upgraded_image": image_paths.get(s["id"]),
                "analysis": s["analysis"],
                "vo": scripts.get(s["id"], "")
            }
            for s, _ in analyses
        ],
        "final_video": final
    }
    report_path = os.path.join(output_dir, "clone_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\n📊 Report saved: {report_path}")

    return {
        "final_video": final,
        "scenes": analyses,
        "image_paths": image_paths,
        "report": report_path,
        "output_dir": output_dir
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", help="Path to local video file")
    parser.add_argument("--url", help="URL to download (TikTok/IG/YT)")
    parser.add_argument("--category", default="minuman", help="Product category")
    parser.add_argument("--name", default="clone_project", help="Project name")
    args = parser.parse_args()

    asyncio.run(run_pipeline(
        video_path=args.video,
        video_url=args.url,
        category=args.category,
        project_name=args.name
    ))
