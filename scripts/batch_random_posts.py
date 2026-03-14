#!/usr/bin/env python3
"""
Batch random trading education posts
5 topics × 3 formats (text, carousel, video) = 15 posts, RANDOMIZED schedule
"""
import requests, json, os, random, base64, subprocess
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta, timezone

PB_KEY = "pb_live_AFm842jzqKVNjREpJH8hTi"
PB_BASE = "https://api.post-bridge.com/v1"
H = {"Authorization": f"Bearer {PB_KEY}", "Content-Type": "application/json"}

ALGO_TEXT = [49814, 49811]
ALGO_MEDIA = [49810, 49663, 49661]
ALL = ALGO_TEXT + ALGO_MEDIA

OUT = "/home/openclaw/.openclaw/workspace/remix_factory/trading_edu/batch"
os.makedirs(OUT, exist_ok=True)

COLORS = [('#1a1a2e','#e94560'),('#0f3460','#16213e'),('#1b1b2f','#e43f5a'),
          ('#162447','#1f4068'),('#1a1a2e','#533483'),('#0d1117','#e94560')]

TOPICS = [
    {
        "id": "support_resistance",
        "text_post": "📈 Support & Resistance — PONDASI trading!\n\nSupport = level dimana BUYER masuk 🟢\nResistance = level dimana SELLER masuk 🔴\n\nPro tip: Kalo support JEBOL, dia jadi resistance!\n\nIni aja udah cukup buat profit.\n\n#supportresistance #trading #forex #xauusd #priceaction #fyp",
        "carousel_slides": [
            {"text": "Support &\nResistance", "sub": "PONDASI trading yang\nWAJIB kamu kuasai", "hook": "SWIPE →"},
            {"text": "Support 🟢", "sub": "Level dimana BUYER masuk\nHarga mentul ke atas", "hook": "BASIC"},
            {"text": "Resistance 🔴", "sub": "Level dimana SELLER masuk\nHarga ditolak turun", "hook": "BASIC"},
            {"text": "Support JEBOL?", "sub": "Dia BERUBAH jadi Resistance!\nDan sebaliknya.", "hook": "PRO TIP"},
            {"text": "Ini Aja Cukup\nBuat Profit", "sub": "Gak perlu indikator ribet.\nMaster S/R = Master Market.", "hook": "SAVE 📌"},
        ],
        "narration": "Oke guys, kali ini gue mau bahas yang paling basic tapi paling penting di trading. Support dan Resistance. Support itu level dimana buyer masuk. Jadi harga nyentuh level ini, terus mental ke atas. Resistance kebalikannya, level dimana seller masuk, harga ditolak turun. Nah yang keren, kalo support jebol, dia berubah jadi resistance. Dan sebaliknya. Ini konsep yang simpel banget tapi powerful. Banyak trader profit cuma pake support resistance doang, tanpa indikator ribet.",
        "video_caption": "📈 Support & Resistance — PONDASI trading!\n\nKonsep simpel tapi POWERFUL 💰\n🔊 Narasi Bahasa Indonesia\n\n#supportresistance #trading #forex #xauusd #fyp",
    },
    {
        "id": "trading_session",
        "text_post": "⏰ 3 Sesi Trading — Kapan waktu TERBAIK?\n\n🌏 Asia (07:00-16:00 WIB): Tenang, range kecil\n🇪🇺 London (14:00-23:00 WIB): VOLATIL, trend mulai\n🇺🇸 New York (20:00-05:00 WIB): PALING VOLATIL\n\n💡 Best entry: London+NY overlap 20:00-23:00 WIB\n\n#tradingsession #forex #xauusd #waktutrading #fyp",
        "carousel_slides": [
            {"text": "Kapan Waktu\nTERBAIK Trading?", "sub": "3 sesi yang WAJIB kamu tau", "hook": "SWIPE →"},
            {"text": "🌏 Sesi Asia", "sub": "07:00-16:00 WIB\nTenang, range kecil", "hook": "SESI #1"},
            {"text": "🇪🇺 Sesi London", "sub": "14:00-23:00 WIB\nVOLATIL! Trend mulai", "hook": "SESI #2"},
            {"text": "🇺🇸 Sesi New York", "sub": "20:00-05:00 WIB\nPALING VOLATIL", "hook": "SESI #3"},
            {"text": "Best Entry\nXAUUSD?", "sub": "London + NY Overlap\n20:00-23:00 WIB\nGOLDEN HOURS!", "hook": "GOLDEN ⭐"},
        ],
        "narration": "Pernah gak sih lo trading tapi market datar banget? Gak gerak-gerak? Nah itu karena lo trading di waktu yang salah! Market itu punya tiga sesi. Pertama sesi Asia, jam tujuh pagi sampe empat sore. Ini sepi, range kecil. Kedua sesi London, jam dua siang sampe sebelas malem. Nah ini mulai rame. Ketiga sesi New York, jam delapan malem sampe subuh. Ini yang paling gila! Dan golden hours nya? Overlap London sama New York, jam delapan sampe sebelas malem WIB!",
        "video_caption": "⏰ Golden Hours XAUUSD: 20:00-23:00 WIB 🔥\n🔊 Narasi Bahasa Indonesia\n\n#tradingsession #forex #xauusd #fyp",
    },
    {
        "id": "lot_size",
        "text_post": "🧮 Cara Hitung Lot Size:\n\nRumus: Lot = (Modal × Risiko%) ÷ (SL pips × Nilai pip)\n\nContoh: Modal 10jt, risiko 1%, SL 20 pips\n= 100rb ÷ (20 × 10rb) = 0.5 lot\n\nJANGAN nebak lot size. HITUNG!\n\n#lotsize #trading #forex #riskmanagement #fyp",
        "carousel_slides": [
            {"text": "Cara Hitung\nLot Size", "sub": "Yang BENAR dan AMAN", "hook": "SWIPE →"},
            {"text": "RUMUS:", "sub": "Lot = (Modal × Risiko%)\n÷ (SL pips × Nilai pip)", "hook": "HAFAL INI"},
            {"text": "Contoh:", "sub": "Modal: Rp 10 Juta\nRisiko: 1% = Rp 100.000\nStop Loss: 20 pips", "hook": "PRAKTEK"},
            {"text": "= 0.5 Lot", "sub": "100.000 ÷ (20 × 10.000)\nITU lot size yang AMAN!", "hook": "JAWABAN"},
            {"text": "JANGAN\nNebak!", "sub": "Nebak = gambling.\nHitung = bisnis.", "hook": "SAVE 📌"},
        ],
        "narration": "Guys, satu hal yang sering banget disepelein. Lot size! Banyak yang asal buka posisi, nebak-nebak aja lotnya. Padahal ada rumusnya. Lot size sama dengan modal kali persen risiko, dibagi stop loss dalam pips dikali nilai pip. Modal sepuluh juta, risiko satu persen berarti seratus ribu, stop loss dua puluh pips. Hasilnya nol koma lima lot. Gampang kan? Jangan pernah nebak. Nebak itu gambling, hitung itu bisnis.",
        "video_caption": "🧮 Cara Hitung Lot Size!\nNebak = gambling. Hitung = bisnis 💼\n🔊 Narasi Bahasa Indonesia\n\n#lotsize #trading #riskmanagement #fyp",
    },
    {
        "id": "trend_following",
        "text_post": "📊 The Trend Is Your Friend!\n\n📈 Higher High + Higher Low = UPTREND\n📉 Lower High + Lower Low = DOWNTREND\n➡️ Flat = SIDEWAYS (jangan trading!)\n\nJANGAN PERNAH lawan trend!\n\n#trendfollowing #trading #forex #priceaction #xauusd #fyp",
        "carousel_slides": [
            {"text": "The Trend Is\nYour Friend", "sub": "Sampai dia BUKAN\nfriend lagi!", "hook": "SWIPE →"},
            {"text": "📈 UPTREND", "sub": "Higher High + Higher Low\nPuncak MAKIN TINGGI", "hook": "NAIK"},
            {"text": "📉 DOWNTREND", "sub": "Lower High + Lower Low\nLembah MAKIN RENDAH", "hook": "TURUN"},
            {"text": "➡️ SIDEWAYS", "sub": "Datar gak jelas arah\nJANGAN TRADING!", "hook": "SKIP!"},
            {"text": "JANGAN Lawan\nTrend!", "sub": "Simple? Yes.\nProfitable? SANGAT.", "hook": "SAVE 📌"},
        ],
        "narration": "The trend is your friend! Tapi banyak yang malah lawan trend. Cara baca trend gampang. Kalo puncak makin tinggi dan lembah makin tinggi, itu uptrend. Kebalikannya downtrend. Dan kalo datar? Sideways, jangan trading! Aturan emasnya simpel. Jangan pernah lawan trend. Trade searah trend aja. Ini yang bikin banyak trader profit konsisten.",
        "video_caption": "📊 Jangan pernah LAWAN trend!\nSimple tapi PROFITABLE 💰\n🔊 Narasi Bahasa Indonesia\n\n#trendfollowing #trading #priceaction #xauusd #fyp",
    },
    {
        "id": "money_management",
        "text_post": "💰 Money Management Rules:\n\n✅ Max 2% risiko per hari\n✅ Max 3 trade per hari\n✅ Loss 2× berturut → STOP\n✅ Target 5%/bulan = LUAR BIASA\n\nCompounding 5%/bulan:\n10 juta → 18 juta setahun!\n\n#moneymanagement #trading #forex #discipline #fyp",
        "carousel_slides": [
            {"text": "Money\nManagement", "sub": "Bukan berapa UNTUNG\nTapi berapa GAK RUGI", "hook": "SWIPE →"},
            {"text": "Max 2% Risiko\nPer Hari", "sub": "Total semua posisi\nMAKSIMAL 2% modal", "hook": "ATURAN #1"},
            {"text": "Max 3 Trade\nPer Hari", "sub": "Kualitas > Kuantitas\nOvertrading = bunuh diri pelan", "hook": "ATURAN #2"},
            {"text": "Loss 2× ?\nSTOP.", "sub": "Tutup chart. Besok lagi.\nEmosi udah gak stabil.", "hook": "ATURAN #3"},
            {"text": "5% Per Bulan\n= HEBAT", "sub": "10 juta → 18 juta setahun!\nSabar = kaya.", "hook": "SAVE 📌"},
        ],
        "narration": "Money management bukan soal berapa kamu untung. Tapi berapa kamu gak rugi! Aturan pertama, maksimal dua persen risiko per hari. Aturan kedua, maksimal tiga trade per hari. Kualitas lebih penting dari kuantitas. Aturan ketiga, kalo udah loss dua kali berturut, stop! Tutup chart, besok lagi. Dan target realistis? Lima persen per bulan. Modal sepuluh juta di-compounding, setahun jadi delapan belas juta. Sabar itu kaya bro!",
        "video_caption": "💰 Money Management yang bikin SURVIVE!\n🔊 Narasi Bahasa Indonesia\n\n#moneymanagement #trading #discipline #xauusd #fyp",
    },
]


def create_slide(text, sub, hook, num, total, path, ci=0):
    bg, acc = COLORS[ci % len(COLORS)]
    W, HI = 1080, 1350
    img = Image.new("RGB", (W, HI), bg)
    d = ImageDraw.Draw(img)
    fp = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    fp2 = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    fb = ImageFont.truetype(fp, 72) if os.path.exists(fp) else ImageFont.load_default()
    fs = ImageFont.truetype(fp, 36) if os.path.exists(fp) else fb
    fh = ImageFont.truetype(fp, 32) if os.path.exists(fp) else fb
    fsub = ImageFont.truetype(fp2, 40) if os.path.exists(fp2) else fb
    d.rectangle([(0,0),(W,8)], fill=acc)
    if hook:
        bb = d.textbbox((0,0), hook, font=fh)
        hw = bb[2]-bb[0]+40
        d.rounded_rectangle([(W-hw-30,40),(W-30,40+bb[3]-bb[1]+20)], radius=12, fill=acc)
        d.text((W-hw-10,45), hook, fill="white", font=fh)
    d.text((40,50), "📊 @AlgoExpertHub", fill="#888", font=fs)
    lines = text.split("\n")
    th = len(lines)*85
    y = HI//2 - th//2 - 60
    for l in lines:
        bb = d.textbbox((0,0),l,font=fb); tw=bb[2]-bb[0]
        d.text(((W-tw)//2,y),l,fill="white",font=fb); y+=85
    y+=30
    for l in sub.split("\n"):
        bb = d.textbbox((0,0),l,font=fsub); tw=bb[2]-bb[0]
        d.text(((W-tw)//2,y),l,fill="#ccc",font=fsub); y+=55
    cnt = f"{num}/{total}"
    bb = d.textbbox((0,0),cnt,font=fs); tw=bb[2]-bb[0]
    d.text(((W-tw)//2,HI-80),cnt,fill="#555",font=fs)
    d.rectangle([(0,HI-8),(W,HI)], fill=acc)
    img.save(path, quality=95)


def upload_media(filepath, mime="image/jpeg"):
    fn = os.path.basename(filepath)
    fz = os.path.getsize(filepath)
    r = requests.post(f"{PB_BASE}/media/create-upload-url", headers=H,
        json={"name":fn,"mime_type":mime,"size_bytes":fz})
    if r.status_code not in [200,201]: return None
    d = r.json()
    url = d.get("upload_url") or d.get("url")
    mid = d.get("media_id") or d.get("id")
    with open(filepath,"rb") as f:
        requests.put(url, data=f, headers={"Content-Type":mime})
    return mid


def main():
    # Build all posts
    all_posts = []
    for t in TOPICS:
        all_posts.append({"type":"text","id":t["id"],"caption":t["text_post"]})
        all_posts.append({"type":"carousel","id":t["id"],"slides":t["carousel_slides"],"caption":t.get("video_caption",t["text_post"])})
        all_posts.append({"type":"video","id":t["id"],"narration":t["narration"],"caption":t["video_caption"]})
    
    random.shuffle(all_posts)
    
    print(f"🎲 RANDOMIZED: {len(all_posts)} posts")
    print("="*50)
    
    now = datetime.now(timezone.utc)
    ok = 0
    
    for i, post in enumerate(all_posts):
        sched = (now + timedelta(minutes=90*i)).strftime("%Y-%m-%dT%H:%M:%SZ")
        wib = (now + timedelta(minutes=90*i, hours=7)).strftime("%H:%M")
        pt = post["type"]
        pid = post["id"]
        
        print(f"\n[{i+1}/{len(all_posts)}] {wib} WIB | {pt.upper():9} | {pid}")
        
        if pt == "text":
            r = requests.post(f"{PB_BASE}/posts", headers=H,
                json={"caption":post["caption"],"social_accounts":ALGO_TEXT,"scheduled_at":sched})
            if r.status_code in [200,201]:
                print(f"  ✅ Text → 2 accounts"); ok+=1
        
        elif pt == "carousel":
            mids = []
            for j, sl in enumerate(post["slides"]):
                p = os.path.join(OUT, f"{pid}_c{j}.jpg")
                create_slide(sl["text"], sl["sub"], sl["hook"], j+1, len(post["slides"]), p, j)
                mid = upload_media(p)
                if mid: mids.append(mid)
            if mids:
                r = requests.post(f"{PB_BASE}/posts", headers=H,
                    json={"caption":post["caption"],"social_accounts":ALL,"media":mids,"scheduled_at":sched})
                if r.status_code in [200,201]:
                    print(f"  ✅ Carousel {len(mids)} slides → 5 accounts"); ok+=1
        
        elif pt == "video":
            audio = os.path.join(OUT, f"{pid}_vo.mp3")
            subprocess.run(["edge-tts","--voice","id-ID-ArdiNeural","--rate=-3%",
                "--text",post["narration"],"--write-media",audio],
                capture_output=True, timeout=60)
            
            if os.path.exists(audio) and os.path.getsize(audio) > 1000:
                # Create slideshow from carousel images
                concat = os.path.join(OUT, f"{pid}_concat.txt")
                imgs = [os.path.join(OUT, f"{pid}_c{j}.jpg") for j in range(5)]
                imgs = [x for x in imgs if os.path.exists(x)]
                if not imgs:
                    # Generate carousel images first
                    t = [x for x in TOPICS if x["id"]==pid][0]
                    for j, sl in enumerate(t["carousel_slides"]):
                        p = os.path.join(OUT, f"{pid}_c{j}.jpg")
                        create_slide(sl["text"], sl["sub"], sl["hook"], j+1, len(t["carousel_slides"]), p, j)
                    imgs = [os.path.join(OUT, f"{pid}_c{j}.jpg") for j in range(5)]
                    imgs = [x for x in imgs if os.path.exists(x)]
                
                with open(concat,"w") as f:
                    for img in imgs:
                        f.write(f"file '{img}'\nduration 12\n")
                    if imgs:
                        f.write(f"file '{imgs[-1]}'\n")
                
                slideshow = os.path.join(OUT, f"{pid}_slide.mp4")
                subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",concat,
                    "-vf","scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:-1:-1:color=black,fps=25",
                    "-c:v","libx264","-pix_fmt","yuv420p","-t","60","-r","25",
                    "-preset","fast","-crf","23",slideshow], capture_output=True, timeout=120)
                
                final = os.path.join(OUT, f"{pid}_final.mp4")
                subprocess.run(["ffmpeg","-y","-stream_loop","-1","-i",slideshow,"-i",audio,
                    "-c:v","libx264","-preset","fast","-crf","23","-c:a","aac","-b:a","128k",
                    "-map","0:v:0","-map","1:a:0","-pix_fmt","yuv420p","-shortest",final],
                    capture_output=True, timeout=120)
                
                if os.path.exists(final) and os.path.getsize(final) > 10000:
                    mid = upload_media(final, "video/mp4")
                    if mid:
                        r = requests.post(f"{PB_BASE}/posts", headers=H,
                            json={"caption":post["caption"],"social_accounts":ALL,"media":[mid],"scheduled_at":sched})
                        if r.status_code in [200,201]:
                            print(f"  ✅ Video+VO → 5 accounts"); ok+=1
                        else:
                            print(f"  ❌ Post: {r.status_code}")
                    else:
                        print("  ❌ Upload failed, text fallback")
                        requests.post(f"{PB_BASE}/posts", headers=H,
                            json={"caption":post["caption"],"social_accounts":ALGO_TEXT,"scheduled_at":sched})
                        ok+=1
    
    print(f"\n{'='*50}")
    print(f"🏁 DONE: {ok}/{len(all_posts)} posts scheduled")
    print(f"📅 Every 90 min over next {len(all_posts)*90//60} hours")


if __name__ == "__main__":
    main()
