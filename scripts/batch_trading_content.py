#!/usr/bin/env python3
"""
Batch Trading Content Generator — 30 days × 5 posts/day = 150 posts
Uses GeminiGen Grok3 + Edge-TTS + FFmpeg + PostBridge

Usage:
  python3 scripts/batch_trading_content.py --days 1-5        # Generate day 1-5
  python3 scripts/batch_trading_content.py --days 1-30 --schedule  # Generate + schedule all
  python3 scripts/batch_trading_content.py --days 1 --preview     # Preview day 1 only
"""

import os, json, sys, ssl, time, subprocess, asyncio, urllib.request, urllib.error, base64
from pathlib import Path
from datetime import datetime, timedelta, timezone

FFMPEG = "/usr/bin/ffmpeg"
OUTPUT_BASE = Path("/home/openclaw/.openclaw/workspace/output/trading_30days")
OUTPUT_BASE.mkdir(parents=True, exist_ok=True)

CTX = ssl.create_default_context()
NVIDIA_KEY = os.environ.get("NVIDIA_API_KEY", "")
PB_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
PB_BASE = "https://api.post-bridge.com/v1"

# Account IDs for trading content
ALGO_ACCOUNTS = {
    "video": [49816, 49810, 49811, 49814],  # YT, IG, Threads, Twitter
    "image": [49810, 49811, 49814],          # IG, Threads, Twitter (no YT for images)  
    "text":  [49811, 49814],                  # Threads, Twitter only
}

# Prime times UTC (WIB = UTC+7)
PRIME_TIMES_UTC = ["00:00", "05:00", "08:00", "11:00", "14:00"]
# Corresponds to WIB: 07:00, 12:00, 15:00, 18:00, 21:00

# VO voice
VOICE = "id-ID-ArdiNeural"

# Load content plan
with open("/home/openclaw/.openclaw/workspace/config/trading_content_30days.json") as f:
    PLAN = json.load(f)


# ─── Video prompt templates per post type ───
def get_video_prompt(theme, subtopic):
    """Generate video prompt for a trading topic."""
    return f"3D clay style animation about {theme} - {subtopic}, trading chart elements, professional financial education style, cinematic lighting, dark moody background with gold and green accents, smooth camera movement"


def get_image_prompt(theme, subtopic):
    """Generate image prompt for carousel slide."""
    return f"Professional trading infographic about {subtopic}, clean dark theme with gold accents, trading chart elements, modern financial education design, 1080x1080, high quality"


# ─── VO Script Templates ───
VO_TEMPLATES = {
    0: "Selamat pagi trader! Hari ini kita bahas tentang {theme}. {subtopic_detail}",
    1: "Lunch break? Sambil makan, yuk belajar tentang {subtopic_detail}",
    2: "Sesi Asia udah tutup. Waktunya review: {subtopic_detail}",
    3: "Sore ini kita lanjut bahas {theme}. {subtopic_detail}",
    4: "Sebelum tidur, tips terakhir hari ini: {subtopic_detail}",
}

VO_DETAILS = {
    "Stop Loss Basics": [
        "Stop loss itu ibarat sabuk pengaman di mobil. Kamu gak mau naik mobil tanpa sabuk pengaman kan?",
        "Kenapa wajib pasang stop loss? Karena market bisa bergerak melawan kamu kapan saja. Tanpa stop loss, satu trade bisa habiskan semua modal.",
        "Rule emas: stop loss maksimal satu sampai dua persen dari total modal. Kalau modal sepuluh juta, SL maksimal seratus sampai dua ratus ribu.",
        "Mental stop itu bohong. Kamu bilang akan cut loss di harga tertentu, tapi begitu harga sampai, kamu malah berharap balik. Pasang SL di platform!",
        "Quiz: Di mana kamu pasang stop loss? Di bawah support terdekat untuk buy, di atas resistance untuk sell. Jangan terlalu dekat, kasih ruang bernafas.",
    ],
    "Risk Management 101": [
        "Risk management adalah fondasi trading. Tanpa ini, sebagus apapun strategi kamu, tetap akan bangkrut.",
        "Rasio risk reward minimal satu banding dua. Artinya kalau kamu siap rugi seratus ribu, target profit minimal dua ratus ribu.",
        "Position sizing itu kunci. Jangan trading dengan lot besar hanya karena merasa yakin. Konsistensi lot lebih penting.",
        "Tujuan utama bukan profit besar, tapi menjaga akun tetap hidup. Account preservation nomor satu.",
        "Checklist sebelum entry: Sudah tentukan SL? R:R minimal satu banding dua? Risiko maksimal dua persen? Kalau belum, jangan entry.",
    ],
    "Candlestick Patterns": [
        "Candlestick patterns itu bahasa market. Kalau kamu bisa baca, kamu bisa prediksi pergerakan harga selanjutnya.",
        "Engulfing pattern itu salah satu yang paling kuat. Candle besar yang menelan candle sebelumnya. Sinyal reversal yang sangat reliable.",
        "Hammer muncul di bottom, shooting star di top. Keduanya punya shadow panjang yang menunjukkan rejection dari level tertentu.",
        "Morning star dan evening star itu pola tiga candle. Butuh konfirmasi tapi akurasinya sangat tinggi.",
        "Quiz: Apa perbedaan doji dan spinning top? Doji bodynya hampir nol, spinning top bodynya kecil tapi masih ada.",
    ],
    "Support & Resistance": [
        "Support dan resistance itu fondasi technical analysis. Tanpa ini, kamu trading buta.",
        "S R flip zone itu ketika support yang di-break berubah jadi resistance, dan sebaliknya. Level ini sangat kuat untuk entry.",
        "Round numbers seperti 2000, 2050, 2100 sering jadi level psikologis. Banyak order menumpuk di level ini.",
        "Analisis multi-timeframe: identifikasi S R di daily dulu, lalu zoom in ke H4 dan H1 untuk entry presisi.",
        "Strategi: Buy di support dengan SL di bawah, sell di resistance dengan SL di atas. Simple tapi effective.",
    ],
    "Fibonacci Retracement": [
        "Fibonacci retracement dipakai trader profesional di seluruh dunia. Level-levelnya bukan kebetulan, ini matematika.",
        "Level terpenting: tiga puluh delapan koma dua, lima puluh, dan enam puluh satu koma delapan. Golden ratio ada di enam puluh satu koma delapan.",
        "Cara tarik fibonacci: dari swing low ke swing high untuk uptrend, kebalikannya untuk downtrend.",
        "Fibonacci plus support resistance itu combo mematikan. Kalau keduanya bertemu di satu level, itu high probability zone.",
        "Golden ratio enam puluh satu koma delapan persen itu angka ajaib. Di alam, di arsitektur, dan di trading. Harga sangat sering bounce dari level ini.",
    ],
}


def get_vo_text(theme, subtopic_idx, subtopic):
    """Get voiceover text for a post."""
    details = VO_DETAILS.get(theme, None)
    if details and subtopic_idx < len(details):
        template = VO_TEMPLATES.get(subtopic_idx, "{subtopic_detail}")
        return template.format(theme=theme, subtopic_detail=details[subtopic_idx])
    # Fallback: generate from subtopic
    templates_fallback = [
        f"Halo trader! Hari ini kita bahas {subtopic}. Ini penting banget buat perjalanan trading kamu.",
        f"Yuk pelajari tentang {subtopic}. Banyak trader gagal karena mengabaikan hal ini.",
        f"Tips sore ini tentang {subtopic}. Catat dan praktekkan di akun demo kamu.",
        f"Malam ini kita bahas {subtopic}. Ilmu yang bisa mengubah cara kamu trading.",
        f"Sebelum tidur, ingat: {subtopic}. Save post ini dan baca lagi besok pagi sebelum trading.",
    ]
    return templates_fallback[subtopic_idx % 5]


def get_caption(theme, subtopic, day_num):
    """Generate caption for post."""
    hashtags = "#TradingTips #BelajarTrading #ForexIndonesia #TradingEducation #AlgoExpertHub #XAUUSD #GoldTrading #RiskManagement #TradingPsychology #BerkahKarya"
    
    captions = [
        f"📊 Day {day_num} — {theme}\n\n💡 {subtopic}\n\nSave & Share kalau bermanfaat! 📌\n\n{hashtags}",
        f"🔥 {theme}\n\n{subtopic}\n\nComment '📈' kalau mau belajar lebih dalam!\n\n{hashtags}",
        f"💰 Tips Trading Hari Ini\n\n{subtopic}\n\nTag teman trader kamu! 🏷️\n\n{hashtags}",
        f"🎯 {subtopic}\n\nPart of {theme} series\n\nFollow @algoexperthub untuk tips daily! ✅\n\n{hashtags}",
        f"⚡ Quick Tip: {subtopic}\n\nSeries: {theme} (Day {day_num}/30)\n\nSave untuk referensi! 📌\n\n{hashtags}",
    ]
    return captions[hash(subtopic) % 5]


async def generate_vo(text, output_path):
    """Generate voiceover."""
    import edge_tts
    comm = edge_tts.Communicate(text, VOICE, rate="+5%")
    await comm.save(output_path)
    return output_path


def generate_image(prompt, output_path):
    """Generate image via NVIDIA Flux."""
    url = "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.1-dev"
    data = json.dumps({"prompt": prompt}).encode()
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {NVIDIA_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    })
    try:
        resp = urllib.request.urlopen(req, context=CTX, timeout=120)
        result = json.loads(resp.read())
        img_bytes = base64.b64decode(result["artifacts"][0]["base64"])
        with open(output_path, "wb") as f:
            f.write(img_bytes)
        return True
    except Exception as e:
        print(f"    Image gen failed: {e}")
        return False


def image_to_video(image_path, vo_path, output_path):
    """Convert image + VO to video with Ken Burns effect."""
    # Get VO duration
    result = subprocess.run([FFMPEG, "-i", vo_path, "-f", "null", "-"], capture_output=True, text=True, timeout=10)
    vo_dur = 5.0
    for line in result.stderr.split("\n"):
        if "Duration:" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
            vo_dur = float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])
    
    frames = int(vo_dur * 24) + 24
    cmd = [
        FFMPEG, "-y", "-loop", "1", "-i", image_path, "-i", vo_path,
        "-c:v", "libx264", "-preset", "fast",
        "-vf", f"scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,zoompan=z='min(zoom+0.0005,1.15)':d={frames}:s=1080x1920",
        "-c:a", "aac", "-b:a", "192k",
        "-t", str(vo_dur + 0.5),
        "-pix_fmt", "yuv420p", "-r", "24",
        "-shortest",
        output_path
    ]
    subprocess.run(cmd, capture_output=True, timeout=120)
    return os.path.exists(output_path)


def upload_and_schedule(video_path, caption, schedule_time, accounts, is_video=True):
    """Upload to PostBridge and schedule."""
    headers = {"Authorization": f"Bearer {PB_KEY}", "Content-Type": "application/json"}
    
    mime = "video/mp4" if is_video else "image/jpeg"
    fname = os.path.basename(video_path)
    fsize = os.path.getsize(video_path)
    
    # Get upload URL
    data = json.dumps({"name": fname, "mime_type": mime, "size_bytes": fsize}).encode()
    req = urllib.request.Request(f"{PB_BASE}/media/create-upload-url", data=data, headers=headers)
    resp = urllib.request.urlopen(req, context=CTX, timeout=15)
    result = json.loads(resp.read())
    upload_url = result.get("upload_url", "")
    media_id = result.get("id", "")
    
    # Upload
    with open(video_path, "rb") as f:
        file_data = f.read()
    put_req = urllib.request.Request(upload_url, data=file_data, method="PUT")
    put_req.add_header("Content-Type", mime)
    urllib.request.urlopen(put_req, context=CTX, timeout=300)
    
    # Schedule
    post_data = json.dumps({
        "caption": caption,
        "social_accounts": accounts,
        "media": [media_id],
        "scheduled_at": schedule_time,
    }).encode()
    post_req = urllib.request.Request(f"{PB_BASE}/posts", data=post_data, headers=headers)
    post_resp = urllib.request.urlopen(post_req, context=CTX, timeout=30)
    post_result = json.loads(post_resp.read())
    return post_result.get("id", "unknown")


async def generate_day(day_num, start_date, schedule=False):
    """Generate all 5 posts for a day."""
    topic = PLAN["topics"][day_num - 1]
    theme = topic["theme"]
    subtopics = topic["subtopics"]
    
    day_dir = OUTPUT_BASE / f"day_{day_num:02d}_{theme.lower().replace(' ', '_')}"
    day_dir.mkdir(parents=True, exist_ok=True)
    
    # Calculate schedule date
    post_date = start_date + timedelta(days=day_num - 1)
    
    print(f"\n{'='*60}")
    print(f"📅 DAY {day_num}/30 — {theme}")
    print(f"   Date: {post_date.strftime('%Y-%m-%d')} ({post_date.strftime('%A')})")
    print(f"{'='*60}")
    
    results = []
    
    for post_idx, subtopic in enumerate(subtopics):
        print(f"\n  --- Post {post_idx+1}/5: {subtopic} ---")
        
        # Determine post type: posts 0,3 = video, posts 1,2 = image+VO, post 4 = text
        if post_idx in (0, 3):
            post_type = "video"
        elif post_idx in (1, 2):
            post_type = "image_video"  # Image → video with Ken Burns + VO
        else:
            post_type = "image_video"  # All get image+VO for better engagement
        
        # 1. Generate VO
        vo_text = get_vo_text(theme, post_idx, subtopic)
        vo_path = str(day_dir / f"post_{post_idx+1}_vo.mp3")
        await generate_vo(vo_text, vo_path)
        print(f"    ✅ VO generated")
        
        # 2. Generate image
        img_prompt = get_image_prompt(theme, subtopic)
        img_path = str(day_dir / f"post_{post_idx+1}_img.jpg")
        if generate_image(img_prompt, img_path):
            print(f"    ✅ Image generated")
        else:
            print(f"    ⚠️ Image failed, using fallback")
            # Create simple text image as fallback
            continue
        
        # 3. Create video from image + VO
        video_path = str(day_dir / f"post_{post_idx+1}_final.mp4")
        if image_to_video(img_path, vo_path, video_path):
            print(f"    ✅ Video assembled")
        else:
            print(f"    ❌ Video assembly failed")
            continue
        
        # 4. Generate caption
        caption = get_caption(theme, subtopic, day_num)
        
        # 5. Schedule if requested
        post_time_utc = PRIME_TIMES_UTC[post_idx]
        schedule_dt = f"{post_date.strftime('%Y-%m-%d')}T{post_time_utc}:00.000Z"
        
        if schedule:
            try:
                accounts = ALGO_ACCOUNTS["video"]
                post_id = upload_and_schedule(video_path, caption, schedule_dt, accounts)
                print(f"    ✅ Scheduled: {schedule_dt} → {post_id}")
                results.append({"post_id": post_id, "time": schedule_dt, "status": "scheduled"})
            except Exception as e:
                print(f"    ❌ Schedule failed: {e}")
                results.append({"status": "failed", "error": str(e)})
        else:
            print(f"    📋 Ready (not scheduled): {schedule_dt}")
            results.append({"video": video_path, "time": schedule_dt, "status": "ready"})
        
        time.sleep(2)  # Rate limit
    
    # Save day summary
    summary = {
        "day": day_num,
        "theme": theme,
        "date": post_date.strftime("%Y-%m-%d"),
        "posts": results,
        "generated_at": datetime.now().isoformat()
    }
    with open(str(day_dir / "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    
    return summary


async def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", default="1", help="Day range: '1' or '1-5' or '1-30'")
    parser.add_argument("--schedule", action="store_true", help="Upload and schedule to PostBridge")
    parser.add_argument("--preview", action="store_true", help="Preview plan only")
    parser.add_argument("--start-date", default=None, help="Start date YYYY-MM-DD (default: tomorrow)")
    args = parser.parse_args()
    
    # Parse day range
    if "-" in args.days:
        start, end = map(int, args.days.split("-"))
    else:
        start = end = int(args.days)
    
    # Start date
    if args.start_date:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    else:
        start_date = datetime.now() + timedelta(days=1)
    
    total_days = end - start + 1
    total_posts = total_days * 5
    
    print(f"🎬 TRADING CONTENT BATCH GENERATOR")
    print(f"   Days: {start}-{end} ({total_days} days, {total_posts} posts)")
    print(f"   Start date: {start_date.strftime('%Y-%m-%d')}")
    print(f"   Schedule: {'YES' if args.schedule else 'NO (generate only)'}")
    
    if args.preview:
        for day_num in range(start, end + 1):
            topic = PLAN["topics"][day_num - 1]
            post_date = start_date + timedelta(days=day_num - 1)
            print(f"\n📅 Day {day_num} ({post_date.strftime('%Y-%m-%d %A')}) — {topic['theme']}")
            for i, sub in enumerate(topic["subtopics"]):
                wib_time = ["07:00", "12:00", "15:00", "18:00", "21:00"][i]
                print(f"   {wib_time} WIB | {sub}")
        return
    
    all_results = []
    for day_num in range(start, end + 1):
        result = await generate_day(day_num, start_date, schedule=args.schedule)
        all_results.append(result)
        print(f"\n✅ Day {day_num} complete!")
    
    # Final summary
    print(f"\n{'='*60}")
    print(f"🏁 BATCH COMPLETE: {len(all_results)} days, {len(all_results)*5} posts")
    scheduled = sum(1 for d in all_results for p in d.get("posts",[]) if p.get("status") == "scheduled")
    print(f"   Scheduled: {scheduled}")
    print(f"   Output: {OUTPUT_BASE}")
    print(f"{'='*60}")


if __name__ == "__main__":
    asyncio.run(main())
