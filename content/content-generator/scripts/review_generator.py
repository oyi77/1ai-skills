"""
Review Generator — Product review videos in real-world locations
Creates authentic, candid-feeling review content
Dimensions: Product × Location × Review Style
"""

import os, json, base64, io, time, asyncio
import urllib.request
import subprocess
from PIL import Image

NVIDIA_KEY   = os.environ.get("NVIDIA_API_KEY")
BYTEPLUS_KEY = os.environ.get("BYTEPLUS_API_KEY")
GROQ_KEY     = os.environ.get("GROQ_API_KEY")
BYTEPLUS_BASE = "https://ark.ap-southeast.bytepluses.com/api/v3"
FFMPEG = "/home/linuxbrew/.linuxbrew/bin/ffmpeg"


# ─── LOCATION LIBRARY ─────────────────────────────────────────────────
LOCATIONS = {
    "mobil": {
        "label": "🚗 Dalam Mobil",
        "desc": "Lagi nyetir / nunggu / parkir",
        "scene_prompt": (
            "inside a car, driver seat, dashboard visible in background, "
            "sunlight through windshield, realistic car interior, "
            "steering wheel slightly visible, Indonesian urban street view outside window"
        ),
        "lighting": "natural car window light, slight warm afternoon sun",
        "mood": "casual, spontaneous, on-the-go",
        "review_context": "lagi di dalam mobil, baru beli / abis ngantor / stuck macet",
    },
    "kampus": {
        "label": "🏫 Di Kampus",
        "desc": "Kantin kampus, lorong, taman kampus",
        "scene_prompt": (
            "university campus outdoor, sitting on bench or campus cafeteria, "
            "college buildings in background, books or laptop on table, "
            "Indonesian university campus atmosphere, warm daylight"
        ),
        "lighting": "outdoor natural daylight, campus environment",
        "mood": "energetic, youthful, relatable student life",
        "review_context": "lagi di kampus, di antara kuliah atau di kantin",
    },
    "warung": {
        "label": "☕ Di Warung",
        "desc": "Warung kopi, warteg, warung pinggir jalan",
        "scene_prompt": (
            "Indonesian warung kopi or small roadside cafe, "
            "traditional wooden table, plastic chairs, "
            "warung signage and local snacks visible in background, "
            "warm incandescent light, authentic Indonesian street food atmosphere"
        ),
        "lighting": "warm tungsten warung lighting, cozy intimate",
        "mood": "relatable, everyday, grounded, authentic",
        "review_context": "lagi nongkrong di warung kopi atau makan siang di warteg",
    },
    "rumah_dapur": {
        "label": "🏠 Di Dapur Rumah",
        "desc": "Dapur rumahan yang real, bukan studio",
        "scene_prompt": (
            "authentic Indonesian home kitchen, tiled walls, gas stove visible, "
            "kitchen utensils hanging, home cooking atmosphere, "
            "warm fluorescent kitchen lighting, realistic Indonesian household"
        ),
        "lighting": "indoor kitchen fluorescent light, warm homey",
        "mood": "homey, practical, trusted, everyday use",
        "review_context": "lagi masak atau ngemil di dapur rumah",
    },
    "kamar": {
        "label": "🛏️ Di Kamar",
        "desc": "Kamar tidur, unboxing santai",
        "scene_prompt": (
            "cozy Indonesian bedroom, bed with pillows in background, "
            "fairy lights or desk lamp, slight messy real-life bedroom, "
            "phone charger and stuff on bedside table, intimate casual setting"
        ),
        "lighting": "soft bedroom lamp light, cozy warm glow",
        "mood": "intimate, honest, late night review, casual",
        "review_context": "lagi santai di kamar, unboxing atau nyoba produk baru",
    },
    "gym": {
        "label": "🏋️ Di Gym",
        "desc": "Gym / fitness center / outdoor workout",
        "scene_prompt": (
            "gym or fitness center background, workout equipment visible, "
            "gym mirrors, motivational atmosphere, "
            "Indonesian gym setting, post-workout or pre-workout scene"
        ),
        "lighting": "bright gym overhead lighting, energetic",
        "mood": "energetic, motivational, health-focused, active",
        "review_context": "habis workout atau sebelum latihan di gym",
    },
    "outdoor": {
        "label": "🌿 Outdoor / Taman",
        "desc": "Taman kota, depan kampus, pinggir jalan",
        "scene_prompt": (
            "outdoor park or green space in Indonesian city, "
            "trees and benches, natural surroundings, "
            "golden hour or midday natural light, "
            "casual outdoor setting"
        ),
        "lighting": "golden hour sunlight or natural daylight, outdoor warmth",
        "mood": "fresh, natural, healthy, outdoor lifestyle",
        "review_context": "lagi jalan-jalan atau duduk di taman",
    },
    "minimarket": {
        "label": "🛒 Di Minimarket",
        "desc": "Alfamart, Indomaret, abis checkout",
        "scene_prompt": (
            "Indonesian minimarket or convenience store exterior, "
            "Alfamart or Indomaret storefront, product shelves slightly visible, "
            "fluorescent store lighting, busy Indonesian street in background"
        ),
        "lighting": "bright convenience store lighting",
        "mood": "spontaneous, impulse buy, relatable daily life",
        "review_context": "baru beli di Alfamart atau Indomaret, langsung nyoba",
    },
    "cafe": {
        "label": "☕ Di Cafe",
        "desc": "Cafe hits, kafe aesthetic, coffee shop",
        "scene_prompt": (
            "trendy Indonesian cafe interior, aesthetically pleasing background, "
            "wooden furniture, coffee cups on table, soft ambient lighting, "
            "plants and modern cafe decor, hipster coffee shop vibes"
        ),
        "lighting": "warm cafe ambient lighting, aesthetic moody",
        "mood": "aesthetic, lifestyle, aspirational but accessible",
        "review_context": "lagi nongkrong atau WFH di cafe",
    },
    "kantor": {
        "label": "💼 Di Kantor",
        "desc": "Meja kerja, ruang meeting, lobby kantor",
        "scene_prompt": (
            "Indonesian office desk environment, laptop and work papers visible, "
            "office cubicle or open workspace background, "
            "professional but relaxed atmosphere, desk items and monitor visible"
        ),
        "lighting": "office overhead lighting, professional",
        "mood": "professional, productive, work-life balance",
        "review_context": "lagi di kantor, pas break atau habis meeting",
    },
}

# ─── REVIEW STYLES ────────────────────────────────────────────────────
REVIEW_STYLES = {
    "jujur":     {"label": "😤 Review Jujur", "tone": "honest, direct, no sugarcoat, share pros AND cons"},
    "excited":   {"label": "🔥 Excited / Hype", "tone": "very enthusiastic, amazed, can't stop talking about it"},
    "santai":    {"label": "😎 Santai / Chill", "tone": "casual, low-key, like telling a friend, not salesy"},
    "compare":   {"label": "⚖️ Banding Kompetitor", "tone": "compare with competitor, why this one wins"},
    "cerita":    {"label": "📖 Cerita Pengalaman", "tone": "storytelling, personal experience, relatable journey"},
}


# ─── PROMPT BUILDER ───────────────────────────────────────────────────
def build_review_image_prompt(product_desc: str, category: str,
                               location_key: str, with_person: bool = True) -> str:
    loc = LOCATIONS[location_key]
    hr_suffix = (
        ", hyperrealistic photography, ultra detailed, 8K, "
        "professional yet candid style, Sony A7III 35mm f/1.8, "
        "natural authentic moment, film grain"
    )

    if with_person:
        return (
            f"candid lifestyle photo, person holding {product_desc}, "
            f"{loc['scene_prompt']}, "
            f"{loc['lighting']}, "
            f"natural authentic review moment, not posed, "
            f"product clearly visible in hand"
            + hr_suffix
        )
    else:
        return (
            f"{product_desc} placed naturally in scene, "
            f"{loc['scene_prompt']}, "
            f"{loc['lighting']}, "
            f"product in natural environment, lifestyle flat lay"
            + hr_suffix
        )


def build_review_anim_prompt(location_key: str, review_style: str) -> str:
    loc = LOCATIONS[location_key]
    style_tone = REVIEW_STYLES.get(review_style, {}).get("tone", "natural")
    return (
        f"natural hand movement holding product, "
        f"{loc['mood']} atmosphere, "
        f"subtle ambient movement in background, "
        f"authentic candid feel, not staged, "
        f"cinematic slow motion, {loc['lighting']}"
    )


# ─── REVIEW SCRIPT GENERATOR ─────────────────────────────────────────
def generate_review_script(product_desc: str, category: str,
                             location_key: str, review_style: str,
                             duration: int = 30) -> dict:
    """Generate natural Indonesian review VO script"""
    loc   = LOCATIONS[location_key]
    style = REVIEW_STYLES.get(review_style, REVIEW_STYLES["santai"])

    word_count = int(duration * 2.5)  # ~2.5 kata/detik natural speech

    prompt = f"""Kamu content creator Indonesia yang lagi bikin video review produk.

Lokasi: {loc['label']} — {loc['review_context']}
Produk: {product_desc} (kategori: {category})
Gaya review: {style['label']} — {style['tone']}
Durasi target: {duration} detik (~{word_count} kata)

Buat script review yang:
1. Opening hook yang langsung menarik (1-2 kalimat, sesuai lokasi)
2. Perkenalkan produk dengan natural (bukan iklan banget)
3. Pengalaman / kesan pertama
4. Highlight 2-3 poin penting
5. Kesimpulan singkat + subtle CTA

PENTING:
- Bahasa Indonesia casual, seperti ngobrol sama teman
- Sesuaikan dengan suasana lokasi ({loc['desc']})
- Jangan terlalu formal atau kaku
- Boleh ada filler words yang natural (eh, jadi, nah, gitu)
- Jangan kayak iklan TV

Respond ONLY JSON:
{{
  "hook": "kalimat pembuka 1-2 detik pertama",
  "script": "full script {duration} detik",
  "key_points": ["poin 1", "poin 2", "poin 3"],
  "cta": "call to action penutup yang natural"
}}"""

    # Use NVIDIA LLM (always available) — fallback to Groq if key exists
    if GROQ_KEY:
        llm_url = "https://api.groq.com/openai/v1/chat/completions"
        llm_model = "llama-3.3-70b-versatile"
        llm_auth = f"Bearer {GROQ_KEY}"
    else:
        llm_url = "https://integrate.api.nvidia.com/v1/chat/completions"
        llm_model = "meta/llama-3.3-70b-instruct"
        llm_auth = f"Bearer {NVIDIA_KEY}"

    payload = json.dumps({
        "model": llm_model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 800, "temperature": 0.8
    }).encode()

    try:
        req = urllib.request.Request(
            llm_url, data=payload,
            headers={"Authorization": llm_auth, "Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
            content = data["choices"][0]["message"]["content"].strip()
            content = content.replace("```json", "").replace("```", "").strip()
            return json.loads(content)
    except Exception as e:
        return {
            "hook": f"Eh, lagi {loc['review_context']}, cobain nih {product_desc}!",
            "script": f"Jadi gue lagi {loc['review_context']}, terus nyobain {product_desc} ini. Jujur ya, kesan pertama gue lumayan impressed. {product_desc} ini emang worth it sih.",
            "key_points": ["Kualitas bagus", "Harga worth it", "Recommended"],
            "cta": "Kalau penasaran cek aja di bio ya!"
        }


# ─── FULL REVIEW PIPELINE ────────────────────────────────────────────
async def generate_review_video(
    product_image: str,
    product_desc: str,
    category: str,
    location_key: str,
    review_style: str = "santai",
    duration: int = 30,
    output_dir: str = "/home/openclaw/.openclaw/workspace/output/reviews",
    chat_id: str = "review"
) -> dict:
    """Full pipeline: image → animate → VO → compose"""
    import sys; sys.path.insert(0, os.path.dirname(__file__))
    from bgm_manager import download_bgm, mix_bgm, get_mood

    os.makedirs(output_dir, exist_ok=True)
    project = f"{category}_{location_key}_{int(time.time())}"
    loc = LOCATIONS[location_key]

    print(f"\n🎬 Review Video: {product_desc}")
    print(f"   📍 Lokasi : {loc['label']}")
    print(f"   🎭 Style  : {REVIEW_STYLES[review_style]['label']}")
    print(f"   ⏱️  Durasi : {duration}s")

    # Step 1: Generate review image
    print("\n🖼️  Step 1: Generating review scene image...")
    img_prompt = build_review_image_prompt(product_desc, category, location_key)
    img_path   = os.path.join(output_dir, f"{project}_scene.jpg")

    # Use SD3 for person scenes
    url = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-3-medium"
    headers = {"Authorization": f"Bearer {NVIDIA_KEY}", "Content-Type": "application/json", "Accept": "application/json"}
    payload = json.dumps({"prompt": img_prompt}).encode()
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.loads(resp.read())
    decoded = base64.b64decode(data.get("image", ""))
    with open(img_path, "wb") as f:
        f.write(decoded)
    print(f"   ✅ Scene image: {img_path} ({len(decoded)//1024}KB)")

    # Step 2: Generate review script
    print("\n✍️  Step 2: Writing review script...")
    script = generate_review_script(product_desc, category, location_key, review_style, duration)
    print(f"   Hook: {script['hook'][:60]}...")
    print(f"   Script: {script['script'][:80]}...")

    # Step 3: Generate voiceover
    print("\n🎙️  Step 3: Generating voiceover...")
    import edge_tts
    vo_path = os.path.join(output_dir, f"{project}_vo.mp3")
    voice   = "id-ID-ArdiNeural" if review_style in ("excited", "compare") else "id-ID-GadisNeural"
    communicate = edge_tts.Communicate(script["script"], voice, rate="+8%")
    await communicate.save(vo_path)
    print(f"   ✅ VO generated ({voice})")

    # Step 4: Animate scene with I2V
    print("\n🎬 Step 4: Animating scene (I2V)...")
    anim_prompt = build_review_anim_prompt(location_key, review_style)

    # Pre-crop to 9:16 so Seedance doesn't flip/transform the source image
    _img = Image.open(img_path).convert("RGB")
    _W, _H = _img.size
    _tw, _th = 720, 1280
    _scale = _th / _H
    _nw = int(_W * _scale)
    _scaled = _img.resize((_nw, _th), Image.LANCZOS)
    _left = max(0, (_nw - _tw) // 2)
    _cropped = _scaled.crop((_left, 0, _left + _tw, _th))
    _buf = io.BytesIO()
    _cropped.save(_buf, format="JPEG", quality=95)
    img_b64 = base64.b64encode(_buf.getvalue()).decode()

    i2v_payload = json.dumps({
        "model": "seedance-1-0-pro-i2v-250528",
        "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}, "role": "first_frame"},
            {"type": "text", "text": anim_prompt}
        ],
        "duration": 5, "seed": -1
        # ratio omitted — image already is 9:16
    }).encode()

    i2v_headers = {"Authorization": f"Bearer {BYTEPLUS_KEY}", "Content-Type": "application/json"}
    req = urllib.request.Request(f"{BYTEPLUS_BASE}/contents/generations/tasks",
                                  data=i2v_payload, headers=i2v_headers, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        task_id = json.loads(resp.read()).get("id")
    print(f"   Task: {task_id}")

    # Poll I2V
    raw_video = None
    for i in range(60):
        time.sleep(5)
        req = urllib.request.Request(f"{BYTEPLUS_BASE}/contents/generations/tasks/{task_id}",
                                      headers=i2v_headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            status_data = json.loads(resp.read())
        status = status_data.get("status")
        if status == "succeeded":
            raw_video = os.path.join(output_dir, f"{project}_raw.mp4")
            urllib.request.urlretrieve(status_data["content"]["video_url"], raw_video)
            print(f"   ✅ Animation done!")
            break
        elif status in ("failed", "cancelled"):
            print(f"   ❌ I2V failed, using static image")
            break
        if i % 3 == 0:
            print(f"   [{(i+1)*5}s] {status}...")

    # Step 5: Loop video to match VO duration + compose
    print("\n✂️  Step 5: Composing final video...")
    final_path = os.path.join(output_dir, f"{project}_FINAL.mp4")

    if raw_video:
        # Loop animated clip to match duration
        looped = os.path.join(output_dir, f"{project}_looped.mp4")
        subprocess.run([FFMPEG, "-y", "-stream_loop", "-1", "-i", raw_video,
                        "-t", str(duration), "-c", "copy", looped], capture_output=True)
        source_video = looped
    else:
        # Use static image as video
        source_video = os.path.join(output_dir, f"{project}_static.mp4")
        subprocess.run([FFMPEG, "-y", "-loop", "1", "-i", img_path, "-t", str(duration),
                        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black",
                        "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p", source_video],
                       capture_output=True)

    # Compose: video + VO
    composed = os.path.join(output_dir, f"{project}_composed.mp4")
    subprocess.run([
        FFMPEG, "-y", "-i", source_video, "-i", vo_path,
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "128k",
        "-t", str(duration), "-shortest", "-pix_fmt", "yuv420p", composed
    ], capture_output=True)

    # Step 6: Add BGM
    print("\n🎵 Step 6: Adding background music...")
    bgm_mood = f"{loc['mood'].split(',')[0]} {category}"
    bgm_path = download_bgm(bgm_mood)
    mix_bgm(composed, bgm_path, final_path, bgm_volume=0.12)

    size_mb = os.path.getsize(final_path) / 1024 / 1024
    print(f"\n🎉 REVIEW VIDEO DONE!")
    print(f"   📹 {final_path} ({size_mb:.1f} MB)")

    return {
        "final_video": final_path,
        "scene_image": img_path,
        "script": script,
        "location": loc["label"],
        "review_style": review_style,
        "duration": duration,
        "project": project
    }


# ─── WIZARD MESSAGES ──────────────────────────────────────────────────
def build_location_message() -> tuple[str, list]:
    text = (
        "📍 *Pilih lokasi review!*\n\n"
        "Dimana produk ini mau di-review?\n"
        "Lokasi yang real = konten yang lebih relatable! 🔥"
    )
    buttons = []
    items = list(LOCATIONS.items())
    for i in range(0, len(items), 2):
        row = []
        for key, loc in items[i:i+2]:
            row.append({"text": loc["label"], "callback_data": f"review:loc:{key}"})
        buttons.append(row)
    return text, buttons


def build_style_message() -> tuple[str, list]:
    text = (
        "🎭 *Pilih gaya review-nya!*\n\n"
        "Mau reviewnya kedengeran kayak gimana?"
    )
    buttons = []
    for key, style in REVIEW_STYLES.items():
        buttons.append([{"text": style["label"], "callback_data": f"review:style:{key}"}])
    return text, buttons


def build_duration_message() -> tuple[str, list]:
    text = "⏱️ *Durasi video?*"
    buttons = [[
        {"text": "📱 15 detik", "callback_data": "review:dur:15"},
        {"text": "🎬 30 detik", "callback_data": "review:dur:30"},
        {"text": "🎵 60 detik", "callback_data": "review:dur:60"},
    ]]
    return text, buttons


if __name__ == "__main__":
    # Test script generation only
    script = generate_review_script(
        "Es Teh Indonesia", "minuman", "warung", "jujur", 30
    )
    print("Hook:", script["hook"])
    print("Script:", script["script"])
    print("CTA:", script["cta"])
