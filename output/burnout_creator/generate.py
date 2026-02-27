#!/usr/bin/env python3
"""
Burnout Creator - AI Video Generator
Generates 45-second TikTok video (1080x1920, 9:16)
"""

import os, json, base64, time, subprocess, asyncio, sys
import urllib.request, urllib.error

NVIDIA_KEY = os.environ.get("NVIDIA_API_KEY")
BYTEPLUS_KEY = os.environ.get("BYTEPLUS_API_KEY")
BYTEPLUS_BASE = "https://ark.ap-southeast.bytepluses.com/api/v3"
FFMPEG = "/home/linuxbrew/.linuxbrew/bin/ffmpeg"
OUT = "/home/openclaw/.openclaw/workspace/output/burnout_creator"
os.makedirs(f"{OUT}/clips", exist_ok=True)
os.makedirs(f"{OUT}/audio", exist_ok=True)
os.makedirs(f"{OUT}/images", exist_ok=True)

SCENES = [
    {
        "id": 1, "duration": 6, "type": "i2v",
        "prompt": "close-up creator at desk at night, tired eyes, laptop glow, messy handwritten notes scattered, cinematic moody lighting, shallow depth of field, 9:16 vertical, cinematic",
        "anim_prompt": "slow subtle breathing movement, laptop screen flickering gently, papers slightly rustling, cinematic slow motion",
        "text": "Pengen konsisten… tapi badan nolak.",
        "vo": "Ada fase… di mana kamu pengen konsisten upload… tapi badan kamu nolak."
    },
    {
        "id": 2, "duration": 7, "type": "i2v",
        "prompt": "hands typing on keyboard editing video timeline on laptop screen, coffee cup steaming nearby, dramatic dark moody lighting, cinematic shallow depth of field, 9:16 vertical",
        "anim_prompt": "fingers typing quickly on keyboard, steam rising from coffee cup, timeline scrubbing fast, dramatic slow motion cinematic",
        "text": "Kamu bukan malas.\nKamu capek.",
        "vo": "Kamu bukan malas. Kamu capek. Capek mikirin ide, capek edit, capek ngulang dari nol… tiap hari."
    },
    {
        "id": 3, "duration": 7, "type": "motion",
        "text": "Masalahnya:\nSISTEM.",
        "vo": "Sampai akhirnya aku sadar… masalahnya bukan di niat. Masalahnya: sistemnya gak ada."
    },
    {
        "id": 4, "duration": 10, "type": "motion_screen",
        "texts": ["Auto cut silence ✂️", "Auto subtitle 📝", "Script struktur 🤖"],
        "vo": "Sejak aku pakai AI buat potong bagian jeda, auto subtitle, dan bantu bikin struktur script… aku balik bisa upload lagi."
    },
    {
        "id": 5, "duration": 9, "type": "i2v",
        "prompt": "young creator smiling slightly looking at phone, upload button being tapped, warm golden morning light, hopeful cinematic mood, shallow depth of field, 9:16 vertical",
        "anim_prompt": "gentle smile growing, hand tapping phone screen, soft morning light rays, hopeful cinematic movement",
        "text": "Bukan lebih kuat.\nLebih ringan.",
        "vo": "Bukan karena aku jadi lebih kuat… tapi karena kerjaanku jadi lebih ringan."
    },
    {
        "id": 6, "duration": 6, "type": "motion_end",
        "text": "Mau workflow\n+ toolsnya?\n→ Cek Bio",
        "vo": "Kalau kamu creator dan kamu lagi di fase itu… tenang. Kamu cuma butuh sistem."
    }
]


# ─── STEP 1: VOICEOVER ───────────────────────────────────────────────
async def generate_voiceover():
    import edge_tts
    print("\n🎙️ Generating voiceovers...")
    voice = "id-ID-GadisNeural"  # Indonesian female voice
    for s in SCENES:
        out_path = f"{OUT}/audio/vo_{s['id']}.mp3"
        if os.path.exists(out_path):
            print(f"  [Scene {s['id']}] Already exists, skip.")
            continue
        communicate = edge_tts.Communicate(s["vo"], voice, rate="+5%")
        await communicate.save(out_path)
        print(f"  [Scene {s['id']}] ✅ {out_path}")


# ─── STEP 2: GENERATE AI IMAGES ──────────────────────────────────────
def generate_image(scene):
    out_path = f"{OUT}/images/scene_{scene['id']}.jpg"
    if os.path.exists(out_path):
        print(f"  [Scene {scene['id']}] Image exists, skip.")
        return out_path
    url = "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.1-dev"
    headers = {
        "Authorization": f"Bearer {NVIDIA_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = json.dumps({"prompt": scene["prompt"]}).encode()
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.loads(resp.read())
        img_b64 = data["artifacts"][0]["base64"]
        with open(out_path, "wb") as f:
            f.write(base64.b64decode(img_b64))
    print(f"  [Scene {scene['id']}] ✅ Image: {out_path}")
    return out_path


# ─── STEP 3: I2V VIA BYTEPLUS ────────────────────────────────────────
def submit_i2v(scene, image_path):
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    payload = json.dumps({
        "model": "seedance-1-0-lite-i2v-250428",
        "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}, "role": "first_frame"},
            {"type": "text", "text": scene["anim_prompt"]}
        ],
        "duration": 5,
        "ratio": "9:16",
        "seed": -1
    }).encode()
    headers = {"Authorization": f"Bearer {BYTEPLUS_KEY}", "Content-Type": "application/json"}
    req = urllib.request.Request(f"{BYTEPLUS_BASE}/contents/generations/tasks", data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())
    task_id = result.get("id")
    print(f"  [Scene {scene['id']}] I2V task submitted: {task_id}")
    return task_id


def poll_i2v(task_id, scene_id, duration):
    headers = {"Authorization": f"Bearer {BYTEPLUS_KEY}"}
    out_tmp = f"{OUT}/clips/scene_{scene_id}_raw.mp4"
    out_path = f"{OUT}/clips/scene_{scene_id}_video.mp4"
    for i in range(60):
        time.sleep(5)
        req = urllib.request.Request(f"{BYTEPLUS_BASE}/contents/generations/tasks/{task_id}", headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
        status = data.get("status")
        print(f"  [Scene {scene_id}] [{(i+1)*5}s] {status}")
        if status == "succeeded":
            video_url = data["content"]["video_url"]
            urllib.request.urlretrieve(video_url, out_tmp)
            # Loop/extend to target duration
            cmd = [FFMPEG, "-y", "-stream_loop", "-1", "-i", out_tmp,
                   "-t", str(duration), "-c", "copy", out_path]
            subprocess.run(cmd, capture_output=True)
            print(f"  [Scene {scene_id}] ✅ Video: {out_path}")
            return out_path
        elif status in ["failed", "cancelled"]:
            raise Exception(f"I2V failed scene {scene_id}")
    raise Exception(f"I2V timeout scene {scene_id}")


# ─── STEP 4: MOTION GRAPHICS ─────────────────────────────────────────
def create_motion_scene(scene):
    out_path = f"{OUT}/clips/scene_{scene['id']}_video.mp4"
    if os.path.exists(out_path):
        print(f"  [Scene {scene['id']}] Motion exists, skip.")
        return out_path
    dur = scene["duration"]
    sid = scene["id"]

    if sid == 3:
        # Dramatic kinetic typography: black bg, bold white text fades in
        text1 = "Masalahnya:"
        text2 = "SISTEM."
        cmd = [
            FFMPEG, "-y",
            "-f", "lavfi",
            "-i", f"color=c=0x0a0a0a:size=1080x1920:duration={dur}:rate=30",
            "-vf",
            (
                f"drawtext=text='{text1}':fontcolor=white:fontsize=72:x=(w-text_w)/2:y=(h/2)-120"
                f":alpha='if(lt(t,1),0,if(lt(t,2),t-1,1))':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf,"
                f"drawtext=text='{text2}':fontcolor=0xFFD700:fontsize=120:x=(w-text_w)/2:y=(h/2)+20"
                f":alpha='if(lt(t,2),0,if(lt(t,3),t-2,1))':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf,"
                f"drawtext=text='Masalahnya\\:':fontcolor=0xffffff:fontsize=72:x=(w-text_w)/2:y=(h/2)-120"
                f":alpha='if(lt(t,1),0,if(lt(t,2),t-1,1))':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            ),
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            out_path
        ]

        # Simpler approach: use ffmpeg drawtext with fade-in
        cmd = [
            FFMPEG, "-y",
            "-f", "lavfi",
            "-i", f"color=c=0x080808:size=1080x1920:duration={dur}:rate=30",
            "-vf",
            (
                "drawtext=text='Masalahnya\\:':fontcolor=white:fontsize=80"
                ":x=(w-text_w)/2:y=(h/2-180)"
                ":alpha='if(lt(t\\,1)\\,0\\,if(lt(t\\,2)\\,t-1\\,1))',"
                "drawtext=text='SISTEM.':fontcolor=0xFFD700:fontsize=140"
                ":x=(w-text_w)/2:y=(h/2-20)"
                ":alpha='if(lt(t\\,2)\\,0\\,if(lt(t\\,3)\\,t-2\\,1))'"
            ),
            "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-pix_fmt", "yuv420p",
            out_path
        ]

    elif sid == 4:
        # Screen record mockup: dark bg, sequential text appearing like UI
        cmd = [
            FFMPEG, "-y",
            "-f", "lavfi",
            "-i", f"color=c=0x111111:size=1080x1920:duration={dur}:rate=30",
            "-vf",
            (
                # Header
                "drawtext=text='AI Workflow':fontcolor=0x4FC3F7:fontsize=56"
                ":x=(w-text_w)/2:y=200"
                ":alpha='if(lt(t\\,0.5)\\,0\\,if(lt(t\\,1.5)\\,t-0.5\\,1))',"
                # Item 1
                "drawtext=text='✂  Auto cut silence':fontcolor=white:fontsize=52"
                ":x=120:y=500"
                ":alpha='if(lt(t\\,1.5)\\,0\\,if(lt(t\\,2.5)\\,t-1.5\\,1))',"
                # Item 2
                "drawtext=text='📝  Auto subtitle':fontcolor=white:fontsize=52"
                ":x=120:y=650"
                ":alpha='if(lt(t\\,3.5)\\,0\\,if(lt(t\\,4.5)\\,t-3.5\\,1))',"
                # Item 3
                "drawtext=text='🤖  Script struktur':fontcolor=white:fontsize=52"
                ":x=120:y=800"
                ":alpha='if(lt(t\\,5.5)\\,0\\,if(lt(t\\,6.5)\\,t-5.5\\,1))',"
                # Bottom tag
                "drawtext=text='Upload lagi. ✅':fontcolor=0x81C784:fontsize=60"
                ":x=(w-text_w)/2:y=1400"
                ":alpha='if(lt(t\\,7.5)\\,0\\,if(lt(t\\,8.5)\\,t-7.5\\,1))'"
            ),
            "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-pix_fmt", "yuv420p",
            out_path
        ]

    elif sid == 6:
        # End card: clean minimal with glow effect
        cmd = [
            FFMPEG, "-y",
            "-f", "lavfi",
            "-i", f"color=c=0x0d0d0d:size=1080x1920:duration={dur}:rate=30",
            "-vf",
            (
                "drawtext=text='Mau workflow':fontcolor=white:fontsize=72"
                ":x=(w-text_w)/2:y=(h/2-220)"
                ":alpha='if(lt(t\\,0.5)\\,0\\,if(lt(t\\,1.5)\\,t-0.5\\,1))',"
                "drawtext=text='+ toolsnya?':fontcolor=white:fontsize=72"
                ":x=(w-text_w)/2:y=(h/2-100)"
                ":alpha='if(lt(t\\,0.8)\\,0\\,if(lt(t\\,1.8)\\,t-0.8\\,1))',"
                "drawtext=text='→ Cek Bio':fontcolor=0xFFD700:fontsize=96"
                ":x=(w-text_w)/2:y=(h/2+80)"
                ":alpha='if(lt(t\\,2)\\,0\\,if(lt(t\\,3)\\,t-2\\,1))'"
            ),
            "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-pix_fmt", "yuv420p",
            out_path
        ]

    subprocess.run(cmd, capture_output=True, check=True)
    print(f"  [Scene {sid}] ✅ Motion graphic: {out_path}")
    return out_path


# ─── STEP 5: ADD VOICEOVER + CAPTION TO CLIP ─────────────────────────
def compose_scene(scene, video_path):
    """Overlay VO audio + on-screen caption text on video clip"""
    audio_path = f"{OUT}/audio/vo_{scene['id']}.mp3"
    out_path = f"{OUT}/clips/scene_{scene['id']}_composed.mp4"
    if os.path.exists(out_path):
        print(f"  [Scene {scene['id']}] Composed exists, skip.")
        return out_path
    dur = scene["duration"]

    # Caption text
    caption = scene.get("text", "")
    caption_lines = caption.replace("\n", " | ") if caption else ""
    caption_safe = caption.replace("'", "\\'").replace(":", "\\:").replace("\n", " ") if caption else ""

    # Base command: combine video + audio
    if caption_safe:
        vf = (
            f"scale=1080:1920:force_original_aspect_ratio=decrease,"
            f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,"
            f"drawtext=text='{caption_safe}'"
            f":fontcolor=white:fontsize=58"
            f":x=(w-text_w)/2:y=h-280"
            f":borderw=4:bordercolor=black@0.8"
            f":alpha='if(lt(t\\,0.3)\\,0\\,if(lt(t\\,0.8)\\,t/0.5\\,1))'"
        )
    else:
        vf = (
            "scale=1080:1920:force_original_aspect_ratio=decrease,"
            "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black"
        )

    cmd = [
        FFMPEG, "-y",
        "-i", video_path,
        "-i", audio_path,
        "-vf", vf,
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        "-t", str(dur),
        "-shortest",
        "-pix_fmt", "yuv420p",
        out_path
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        print(f"  [Scene {scene['id']}] FFmpeg error: {result.stderr.decode()[-500:]}")
        raise Exception("compose failed")
    print(f"  [Scene {scene['id']}] ✅ Composed: {out_path}")
    return out_path


# ─── STEP 6: FINAL CONCATENATION ─────────────────────────────────────
def concatenate_scenes(composed_paths):
    """Join all scene clips into final video"""
    list_file = f"{OUT}/concat_list.txt"
    with open(list_file, "w") as f:
        for p in composed_paths:
            f.write(f"file '{p}'\n")
    out_path = f"{OUT}/burnout_creator_FINAL.mp4"
    cmd = [
        FFMPEG, "-y",
        "-f", "concat", "-safe", "0",
        "-i", list_file,
        "-c:v", "libx264", "-preset", "fast", "-crf", "22",
        "-c:a", "aac", "-b:a", "128k",
        "-pix_fmt", "yuv420p",
        out_path
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        print(f"Concat error: {result.stderr.decode()[-1000:]}")
        raise Exception("concat failed")
    size_mb = os.path.getsize(out_path) / 1024 / 1024
    print(f"\n🎉 FINAL VIDEO: {out_path} ({size_mb:.1f} MB)")
    return out_path


# ─── MAIN ─────────────────────────────────────────────────────────────
async def main():
    print("=" * 60)
    print("🎬 BURNOUT CREATOR - AI VIDEO GENERATOR")
    print("=" * 60)

    # Step 1: Voiceover
    await generate_voiceover()

    # Step 2: Generate AI images + submit I2V tasks (parallel-ish)
    i2v_scenes = [s for s in SCENES if s["type"] == "i2v"]
    i2v_tasks = {}

    print("\n🖼️  Generating AI images...")
    for scene in i2v_scenes:
        img_path = generate_image(scene)
        task_id = submit_i2v(scene, img_path)
        i2v_tasks[scene["id"]] = (task_id, scene["duration"])

    # Step 3: Create motion graphics while I2V renders
    print("\n✏️  Creating motion graphics...")
    motion_scenes = [s for s in SCENES if s["type"] in ("motion", "motion_screen", "motion_end")]
    for scene in motion_scenes:
        create_motion_scene(scene)

    # Step 4: Poll I2V results
    print("\n⏳ Polling I2V results...")
    i2v_video_paths = {}
    for scene in i2v_scenes:
        tid, dur = i2v_tasks[scene["id"]]
        path = poll_i2v(tid, scene["id"], dur)
        i2v_video_paths[scene["id"]] = path

    # Step 5: Compose each scene (add VO + captions)
    print("\n🎙️  Composing scenes...")
    composed = []
    for scene in SCENES:
        if scene["type"] == "i2v":
            vpath = i2v_video_paths[scene["id"]]
        else:
            vpath = f"{OUT}/clips/scene_{scene['id']}_video.mp4"
        composed_path = compose_scene(scene, vpath)
        composed.append(composed_path)

    # Step 6: Concatenate
    print("\n🔗 Concatenating all scenes...")
    final = concatenate_scenes(composed)

    print("\n✅ ALL DONE!")
    print(f"📹 Final video: {final}")
    print(f"📐 Resolution: 1080x1920 (9:16)")
    print(f"⏱️  Duration: ~45 seconds")

asyncio.run(main())
