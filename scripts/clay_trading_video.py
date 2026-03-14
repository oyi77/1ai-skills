#!/usr/bin/env python3
"""
Clay/3D Trading Education Video Generator
Generates clay-style images → animates → posts to PostBridge
"""
import requests
import json
import os
import subprocess
import random
import base64
from datetime import datetime, timedelta, timezone
from PIL import Image, ImageDraw, ImageFont
import textwrap

XAI_KEY = "xai-Z0z54954ovqntReOTEHJdOBZpcu0Xu0Oao3TbltR1lOJux0IDKnWgNqcGW992WFkZZrK90UnKrDcF4b6"
PB_KEY = "pb_live_AFm842jzqKVNjREpJH8hTi"
PB_BASE = "https://api.post-bridge.com/v1"
OUT_DIR = "/home/openclaw/.openclaw/workspace/remix_factory/trading_edu"

os.makedirs(OUT_DIR, exist_ok=True)

# AlgoExpertHub accounts - crosspost to all
ALGO_ACCOUNTS_TEXT = [49814, 49811]  # Twitter, Threads
ALGO_ACCOUNTS_MEDIA = [49810, 49663, 49661]  # IG algoexperthub + TikTok bkjaya00 + IG bkjayautama

STYLES = [
    "claymation style, clay figurine characters, plasticine texture, stop-motion look, soft lighting, colorful",
    "3D cartoon style, Pixar-like characters, cute chibi proportions, vibrant colors, smooth rendering",
    "clay art style, handmade clay characters, warm colors, tactile texture, miniature scene, stop motion animation",
    "3D rendered cartoon, Disney-style cute characters, glossy finish, bright studio lighting, playful",
]

# Video lessons - each has 5 scenes
LESSONS = [
    {
        "id": "risk_mgmt",
        "title": "Risk Management 101",
        "caption": "🔴 STOP! Before you trade, learn this FIRST.\n\nRisk Management is the #1 skill every trader needs.\n\n💡 The 1% Rule can save your account.\n\n#trading #riskmanagement #forex #xauusd #education #tradingtips #fyp",
        "scenes": [
            {"prompt": "a cute {style} character sitting at a desk with multiple computer screens showing red charts going down, looking worried, dramatic lighting", 
             "text": "90% of Traders FAIL", "subtext": "Because of ONE thing..."},
            {"prompt": "a {style} character holding a golden shield with '1%' written on it, protecting a pile of gold coins from falling red arrows",
             "text": "The 1% Rule", "subtext": "Never risk more than 1% per trade"},
            {"prompt": "a {style} character calculating on a big calculator, with coins stacked neatly in organized rows, clean desk",
             "text": "$10,000 Account", "subtext": "= $100 Max Risk Per Trade"},
            {"prompt": "a {style} character with a stop sign, blocking a monster made of red candles from destroying a castle of gold",
             "text": "Always Use Stop Loss", "subtext": "Protect your capital FIRST"},
            {"prompt": "a {style} character standing confidently on top of a growing green chart mountain, holding a flag that says 'SURVIVE', sunrise behind",
             "text": "Survive First", "subtext": "Profits come to those who LAST"},
        ]
    },
    {
        "id": "candles",
        "title": "Candlestick Patterns",
        "caption": "🕯️ 5 Candlestick Patterns that ACTUALLY work!\n\nLearn to read price action like a PRO.\n\nSave this for your next trading session 📌\n\n#candlestick #priceaction #trading #forex #technicalanalysis #xauusd #fyp",
        "scenes": [
            {"prompt": "a cute {style} character as a teacher pointing at a giant glowing candlestick chart on a blackboard, classroom setting",
             "text": "Read the CANDLES", "subtext": "5 Patterns Every Trader Needs"},
            {"prompt": "a {style} character looking amazed at a giant green engulfing candle eating a small red candle, dramatic scene",
             "text": "1. Engulfing Pattern", "subtext": "Strong reversal signal"},
            {"prompt": "a {style} character poking a long pin bar candle that looks like a hammer, the candle bouncing off a floor",
             "text": "2. Pin Bar / Hammer", "subtext": "Price rejection = reversal"},
            {"prompt": "a {style} character standing between two identical candles (one green one red) with a tiny doji candle in the middle looking confused",
             "text": "3. Doji = Indecision", "subtext": "Market is thinking..."},
            {"prompt": "a {style} character wearing a graduation cap celebrating next to a chart showing perfect candle pattern entries with green arrows",
             "text": "Master These FIRST", "subtext": "Before any indicator"},
        ]
    },
    {
        "id": "psychology",  
        "title": "Trading Psychology",
        "caption": "🧠 Your BRAIN is your biggest enemy in trading.\n\n5 emotional traps that KILL your account.\n\nWhich one are YOU guilty of? 👇\n\n#tradingpsychology #forex #mindset #discipline #trading #xauusd #fyp",
        "scenes": [
            {"prompt": "a cute {style} character with an angel on one shoulder and a devil on the other, sitting in front of trading screens",
             "text": "Your Worst Enemy?", "subtext": "YOUR OWN BRAIN"},
            {"prompt": "a {style} character chasing a green rocket that's flying away, looking desperate, other characters watching calmly",
             "text": "1. FOMO", "subtext": "Chasing trades you missed"},
            {"prompt": "a {style} character angrily smashing keyboard with red charts everywhere, steam coming from head, coins falling",
             "text": "2. Revenge Trading", "subtext": "Emotion = Destruction"},
            {"prompt": "a {style} character meditating peacefully in the middle of chaotic red and green charts, zen garden around them",
             "text": "The Solution?", "subtext": "DISCIPLINE over emotion"},
            {"prompt": "a {style} character writing in a journal with a calm smile, organized desk, green profitable charts in background",
             "text": "Journal Everything", "subtext": "Data beats feelings. ALWAYS."},
        ]
    },
]


def generate_image(prompt, output_path):
    """Generate image using NVIDIA SDXL"""
    NVIDIA_KEY = "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"
    print(f"  🎨 Generating: {prompt[:60]}...")
    
    try:
        resp = requests.post(
            "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-xl",
            headers={
                "Authorization": f"Bearer {NVIDIA_KEY}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            json={
                "text_prompts": [{"text": prompt, "weight": 1}],
                "cfg_scale": 7,
                "sampler": "K_DPM_2_ANCESTRAL",
                "seed": random.randint(1, 999999),
                "steps": 30,
                "height": 1024,
                "width": 1024
            },
            timeout=120
        )
        
        if resp.status_code != 200:
            print(f"  ❌ API error: {resp.status_code} {resp.text[:200]}")
            return False
        
        data = resp.json()
        if "artifacts" in data and len(data["artifacts"]) > 0:
            img_bytes = base64.b64decode(data["artifacts"][0]["base64"])
            with open(output_path, "wb") as f:
                f.write(img_bytes)
            print(f"  ✅ Saved: {output_path} ({len(img_bytes)/1024:.0f}KB)")
            return True
        else:
            print(f"  ❌ No artifacts: {json.dumps(data)[:200]}")
            return False
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def add_text_overlay(img_path, text, subtext, output_path):
    """Add text overlay to image using PIL"""
    img = Image.open(img_path).convert("RGBA")
    # Resize to 1080x1920 (portrait 9:16)
    img = img.resize((1080, 1080), Image.LANCZOS)
    
    # Create portrait canvas
    canvas = Image.new("RGBA", (1080, 1920), (15, 15, 25, 255))
    # Place image in center-top
    canvas.paste(img, (0, 200))
    
    draw = ImageDraw.Draw(canvas)
    
    # Try to find a font
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    ]
    
    font_large = None
    font_small = None
    for fp in font_paths:
        if os.path.exists(fp):
            font_large = ImageFont.truetype(fp, 72)
            font_small = ImageFont.truetype(fp, 42)
            break
    
    if not font_large:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw semi-transparent overlay at bottom
    overlay = Image.new("RGBA", (1080, 500), (0, 0, 0, 180))
    canvas.paste(overlay, (0, 1420), overlay)
    draw = ImageDraw.Draw(canvas)
    
    # Main text
    lines = textwrap.wrap(text, width=20)
    y = 1460
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font_large)
        w = bbox[2] - bbox[0]
        draw.text(((1080 - w) / 2, y), line, fill=(255, 255, 255, 255), font=font_large)
        y += 85
    
    # Subtext
    if subtext:
        sub_lines = textwrap.wrap(subtext, width=35)
        y += 20
        for line in sub_lines:
            bbox = draw.textbbox((0, 0), line, font=font_small)
            w = bbox[2] - bbox[0]
            draw.text(((1080 - w) / 2, y), line, fill=(200, 200, 200, 255), font=font_small)
            y += 55
    
    # Top branding
    brand_font = font_small
    draw.text((40, 60), "📊 @AlgoExpertHub", fill=(255, 215, 0, 255), font=brand_font)
    
    canvas = canvas.convert("RGB")
    canvas.save(output_path, quality=95)
    return True


def create_video(lesson_dir, lesson_id, num_scenes=5):
    """Create 1-minute video from scene images using FFmpeg"""
    duration_per_scene = 12  # 12s × 5 = 60s
    
    # Build FFmpeg concat file
    concat_file = os.path.join(lesson_dir, "concat.txt")
    with open(concat_file, "w") as f:
        for i in range(num_scenes):
            img = os.path.join(lesson_dir, f"scene_{i}_final.jpg")
            if os.path.exists(img):
                f.write(f"file '{img}'\nduration {duration_per_scene}\n")
        # Last image needs to be listed again
        last = os.path.join(lesson_dir, f"scene_{num_scenes-1}_final.jpg")
        if os.path.exists(last):
            f.write(f"file '{last}'\n")
    
    output = os.path.join(lesson_dir, f"{lesson_id}_trading_edu.mp4")
    
    # Ken Burns effect with zoom
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_file,
        "-vf", f"scale=1080:1920,zoompan=z='min(zoom+0.0008,1.15)':d={duration_per_scene*25}:s=1080x1920:fps=25",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-t", "60",
        "-r", "25",
        "-preset", "fast", "-crf", "23",
        output
    ]
    
    # Simpler approach - just concat images as slideshow with fade
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_file,
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:-1:-1:color=black,fps=25",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-t", "60", "-r", "25",
        "-preset", "fast", "-crf", "23",
        output
    ]
    
    print(f"  🎬 Rendering video: {output}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    
    if result.returncode == 0 and os.path.exists(output):
        size = os.path.getsize(output) / 1024 / 1024
        print(f"  ✅ Video: {output} ({size:.1f}MB)")
        return output
    else:
        print(f"  ❌ FFmpeg failed: {result.stderr[-300:]}")
        return None


def upload_and_post(video_path, caption):
    """Upload to PostBridge and create crosspost"""
    H = {"Authorization": f"Bearer {PB_KEY}", "Content-Type": "application/json"}
    
    fname = os.path.basename(video_path)
    fsize = os.path.getsize(video_path)
    
    # Upload media
    print(f"  📤 Uploading {fname} ({fsize/1024/1024:.1f}MB)...")
    resp = requests.post(f"{PB_BASE}/media/create-upload-url", headers=H,
        json={"name": fname, "mime_type": "video/mp4", "size_bytes": fsize})
    
    if resp.status_code not in [200, 201]:
        print(f"  ❌ Upload URL failed: {resp.status_code} {resp.text[:200]}")
        # Fallback: post text-only to text accounts
        print(f"  📝 Falling back to text-only crosspost...")
        resp2 = requests.post(f"{PB_BASE}/posts", headers=H,
            json={"caption": caption, "social_accounts": ALGO_ACCOUNTS_TEXT})
        if resp2.status_code in [200, 201]:
            print(f"  ✅ Text crosspost: {resp2.json().get('id','?')[:8]}")
            return True
        return False
    
    data = resp.json()
    upload_url = data.get("upload_url") or data.get("url")
    media_id = data.get("media_id") or data.get("id")
    
    if upload_url:
        with open(video_path, "rb") as f:
            up = requests.put(upload_url, data=f, headers={"Content-Type": "video/mp4"})
        if up.status_code in [200, 201, 204]:
            print(f"  ✅ Uploaded! media_id={media_id}")
            # Crosspost to ALL algo accounts (text + media)
            all_accounts = ALGO_ACCOUNTS_TEXT + ALGO_ACCOUNTS_MEDIA
            resp3 = requests.post(f"{PB_BASE}/posts", headers=H,
                json={"caption": caption, "social_accounts": all_accounts, "media": [media_id]})
            if resp3.status_code in [200, 201]:
                print(f"  ✅ Crosspost to {len(all_accounts)} accounts: {resp3.json().get('id','?')[:8]}")
                return True
            else:
                print(f"  ❌ Post failed: {resp3.status_code} {resp3.text[:200]}")
    
    return False


def main():
    print("=" * 60)
    print("🎬 CLAY/3D TRADING EDUCATION VIDEO GENERATOR")
    print("=" * 60)
    
    for lesson in LESSONS:
        lid = lesson["id"]
        lesson_dir = os.path.join(OUT_DIR, lid)
        os.makedirs(lesson_dir, exist_ok=True)
        
        style = random.choice(STYLES)
        style_name = "Clay" if "clay" in style.lower() else "3D Cartoon"
        
        print(f"\n{'='*40}")
        print(f"📚 Lesson: {lesson['title']} ({style_name})")
        print(f"{'='*40}")
        
        # Generate 5 scene images
        scene_count = 0
        for i, scene in enumerate(lesson["scenes"]):
            img_path = os.path.join(lesson_dir, f"scene_{i}_raw.png")
            final_path = os.path.join(lesson_dir, f"scene_{i}_final.jpg")
            
            # Skip if already generated
            if os.path.exists(final_path) and os.path.getsize(final_path) > 10000:
                print(f"  Scene {i+1}: Already exists, skipping")
                scene_count += 1
                continue
            
            prompt = scene["prompt"].replace("{style}", style)
            
            if generate_image(prompt, img_path):
                if add_text_overlay(img_path, scene["text"], scene["subtext"], final_path):
                    scene_count += 1
                    print(f"  ✅ Scene {i+1}/5 complete")
            else:
                print(f"  ⚠️ Scene {i+1} failed, will use placeholder")
        
        if scene_count < 3:
            print(f"  ❌ Only {scene_count}/5 scenes generated, skipping video")
            continue
        
        # Create video
        video = create_video(lesson_dir, lid, len(lesson["scenes"]))
        
        if video:
            # Upload and crosspost
            upload_and_post(video, lesson["caption"])
        
        print(f"✅ Lesson '{lesson['title']}' DONE\n")
    
    print("\n" + "=" * 60)
    print("🏁 ALL TRADING EDUCATION VIDEOS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
