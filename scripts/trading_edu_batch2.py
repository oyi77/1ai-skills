#!/usr/bin/env python3
"""Task 4: Scale trading edu +5 topics (Fibonacci, RSI, MA, RRR, Breakout)"""
import requests, os, random, subprocess
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta, timezone

PB_KEY = "pb_live_AFm842jzqKVNjREpJH8hTi"
PB_BASE = "https://api.post-bridge.com/v1"
H = {"Authorization": f"Bearer {PB_KEY}", "Content-Type": "application/json"}
ALGO_TEXT = [49814, 49811]
ALGO_MEDIA = [49810, 49663, 49661]
ALL = ALGO_TEXT + ALGO_MEDIA
OUT = "/home/openclaw/.openclaw/workspace/remix_factory/trading_edu/batch2"
os.makedirs(OUT, exist_ok=True)

COLORS = [('#1a1a2e','#e94560'),('#0f3460','#16213e'),('#1b1b2f','#e43f5a'),
          ('#162447','#1f4068'),('#1a1a2e','#533483'),('#0d1117','#e94560')]

TOPICS = [
    {
        "id": "fibonacci",
        "text_post": "📐 Fibonacci Retracement — Senjata Rahasia Trader Pro!\n\nLevel penting:\n🔹 38.2% — koreksi ringan (trend kuat)\n🔹 50.0% — level psikologis\n🔹 61.8% — GOLDEN RATIO (paling sering jadi turning point!)\n\nCara pakai: Tarik dari swing low ke swing high (uptrend) atau sebaliknya.\n\nEntry di 61.8% + konfirmasi candle = setup KILLER 🎯\n\n#fibonacci #trading #forex #xauusd #technicalanalysis #fyp",
        "carousel_slides": [
            {"text": "Fibonacci\nRetracement", "sub": "Senjata RAHASIA\ntrader pro!", "hook": "SWIPE →"},
            {"text": "38.2%", "sub": "Koreksi ringan\nTrend KUAT lanjut", "hook": "LEVEL #1"},
            {"text": "50.0%", "sub": "Level psikologis\nSering jadi battleground", "hook": "LEVEL #2"},
            {"text": "61.8%", "sub": "GOLDEN RATIO!\nPaling sering jadi\nturning point", "hook": "⭐ KEY"},
            {"text": "Entry di 61.8%\n+ Konfirmasi", "sub": "Tunggu candle konfirmasi\ndi golden ratio = KILLER setup", "hook": "SAVE 📌"},
        ],
        "narration": "Guys, kalo lo mau level up trading skills lo, wajib banget belajar Fibonacci Retracement. Ini tools yang paling sering dipake sama trader pro. Ada tiga level penting. Tiga puluh delapan koma dua persen, ini koreksi ringan, artinya trend masih kuat. Lima puluh persen, ini level psikologis. Dan yang paling penting, enam puluh satu koma delapan persen. Ini golden ratio! Paling sering jadi turning point. Cara pakainya, tarik dari swing low ke swing high kalo uptrend. Terus tunggu harga koreksi ke level enam puluh satu koma delapan. Kalo ada konfirmasi candle di situ, itu setup killer!",
        "video_caption": "📐 Fibonacci — Senjata Rahasia Trader Pro!\nGolden Ratio 61.8% = KILLER setup 🎯\n🔊 Narasi Bahasa Indonesia\n\n#fibonacci #trading #forex #xauusd #fyp",
    },
    {
        "id": "rsi",
        "text_post": "📊 RSI (Relative Strength Index) — Tau Kapan Market Overheated!\n\nRSI > 70 = OVERBOUGHT (market udah capek naik)\nRSI < 30 = OVERSOLD (market udah capek turun)\n\n⚠️ JANGAN langsung entry cuma karena RSI overbought/oversold!\nTunggu DIVERGENCE atau konfirmasi candle.\n\nRSI + Price Action = combo MEMATIKAN 💀\n\n#rsi #indicator #trading #forex #xauusd #technicalanalysis #fyp",
        "carousel_slides": [
            {"text": "RSI\nIndicator", "sub": "Tau kapan market\nOVERHEATED!", "hook": "SWIPE →"},
            {"text": "RSI > 70", "sub": "OVERBOUGHT!\nMarket udah capek naik\nPotensi turun", "hook": "🔴 JUAL?"},
            {"text": "RSI < 30", "sub": "OVERSOLD!\nMarket udah capek turun\nPotensi naik", "hook": "🟢 BELI?"},
            {"text": "JANGAN\nLangsung Entry!", "sub": "Tunggu DIVERGENCE\natau konfirmasi candle\nRSI = filter, bukan sinyal", "hook": "⚠️ PENTING"},
            {"text": "RSI + Price\nAction", "sub": "Combo MEMATIKAN!\nRSI buat filter\nCandle buat konfirmasi", "hook": "SAVE 📌"},
        ],
        "narration": "RSI atau Relative Strength Index, ini indikator favorit banyak trader. Konsepnya simpel. Kalo RSI di atas tujuh puluh, artinya market overbought, udah capek naik. Kalo di bawah tiga puluh, oversold, udah capek turun. Tapi ya jangan langsung entry cuma gara-gara RSI overbought atau oversold ya! Itu kesalahan pemula. Yang bener, tunggu divergence atau konfirmasi candle dulu. RSI itu filter, bukan sinyal. Kombinasi RSI sama price action, itu baru combo yang mematikan!",
        "video_caption": "📊 RSI — Tau Kapan Market Overheated!\nRSI + Price Action = combo MEMATIKAN 💀\n🔊 Narasi Bahasa Indonesia\n\n#rsi #trading #forex #xauusd #fyp",
    },
    {
        "id": "moving_average",
        "text_post": "📈 Moving Average — Indikator Paling SIMPLE tapi Efektif!\n\nMA 20 = trend pendek (scalping)\nMA 50 = trend menengah (swing)\nMA 200 = trend besar (posisi)\n\n💡 Golden Cross: MA 50 cross ATAS MA 200 = BULLISH!\n💀 Death Cross: MA 50 cross BAWAH MA 200 = BEARISH!\n\nHarga di ATAS MA = beli\nHarga di BAWAH MA = jual\n\n#movingaverage #trading #forex #indicator #xauusd #fyp",
        "carousel_slides": [
            {"text": "Moving\nAverage", "sub": "Indikator paling SIMPLE\ntapi EFEKTIF!", "hook": "SWIPE →"},
            {"text": "MA 20", "sub": "Trend PENDEK\nBuat scalping\n& day trading", "hook": "SHORT"},
            {"text": "MA 50", "sub": "Trend MENENGAH\nBuat swing trading\nPaling populer!", "hook": "MID"},
            {"text": "MA 200", "sub": "Trend BESAR\nInstitutional level\nKalo jebol = big move!", "hook": "LONG"},
            {"text": "Golden Cross\nvs Death Cross", "sub": "MA50 cross atas MA200 = BULL\nMA50 cross bawah MA200 = BEAR", "hook": "SAVE 📌"},
        ],
        "narration": "Moving Average, ini indikator yang paling simpel tapi efektif banget. Ada tiga yang harus lo tau. MA dua puluh buat trend pendek, cocok buat scalping. MA lima puluh buat trend menengah, ini yang paling populer. Dan MA dua ratus buat trend besar, ini yang dipake institusi. Nah yang seru, kalo MA lima puluh cross ke atas MA dua ratus, itu namanya Golden Cross, sinyal bullish kuat! Sebaliknya, Death Cross, sinyal bearish. Simple rule nya, harga di atas MA berarti beli, di bawah MA berarti jual.",
        "video_caption": "📈 Moving Average — Simple tapi EFEKTIF!\nGolden Cross vs Death Cross ⚔️\n🔊 Narasi Bahasa Indonesia\n\n#movingaverage #trading #forex #xauusd #fyp",
    },
    {
        "id": "risk_reward",
        "text_post": "⚖️ Risk Reward Ratio — Kunci PROFIT Jangka Panjang!\n\nMinimum RRR: 1:2\nArtinya: Risiko 100rb, target 200rb\n\nKenapa penting?\nDengan RRR 1:2, lo cuma perlu WIN RATE 40% buat PROFIT!\n\nContoh 10 trade:\n❌ 6 loss × 100rb = -600rb\n✅ 4 win × 200rb = +800rb\n💰 Net = +200rb PROFIT!\n\nMatematika > emosi. Selalu.\n\n#riskreward #trading #forex #riskmanagement #xauusd #fyp",
        "carousel_slides": [
            {"text": "Risk Reward\nRatio", "sub": "Kunci PROFIT\njangka panjang!", "hook": "SWIPE →"},
            {"text": "Minimum\n1:2", "sub": "Risiko 100rb\nTarget 200rb\nINI MINIMUM!", "hook": "ATURAN"},
            {"text": "Win Rate 40%\n= PROFIT!", "sub": "Dengan RRR 1:2\nCuma perlu menang\n4 dari 10 trade!", "hook": "MATH 🧮"},
            {"text": "Buktinya:", "sub": "6 loss × 100rb = -600rb\n4 win × 200rb = +800rb\nNet = +200rb!", "hook": "CONTOH"},
            {"text": "Matematika >\nEmosi", "sub": "SELALU hitung RRR\nsebelum entry.\nGak 1:2? SKIP.", "hook": "SAVE 📌"},
        ],
        "narration": "Risk Reward Ratio, ini kunci buat profit jangka panjang. Minimum yang harus lo pake, satu banding dua. Artinya, kalo lo risiko seratus ribu, target lo harus dua ratus ribu. Kenapa penting? Karena dengan RRR satu banding dua, lo cuma perlu win rate empat puluh persen buat profit! Coba hitung. Dari sepuluh trade, enam loss dikali seratus ribu, minus enam ratus ribu. Empat win dikali dua ratus ribu, plus delapan ratus ribu. Net nya? Plus dua ratus ribu! Profit meskipun lebih banyak loss nya. Matematika ngalahin emosi, selalu!",
        "video_caption": "⚖️ Risk Reward Ratio — Kunci PROFIT!\nWin rate 40% aja bisa CUAN 💰\n🔊 Narasi Bahasa Indonesia\n\n#riskreward #trading #riskmanagement #xauusd #fyp",
    },
    {
        "id": "breakout_trading",
        "text_post": "💥 Breakout Trading — Catch The BIG Move!\n\nBreakout = harga TEMBUS level penting (S/R, trendline, pattern)\n\n✅ REAL breakout: volume TINGGI, candle BESAR, close di LUAR level\n❌ FAKE breakout: volume RENDAH, candle kecil, balik masuk\n\nTips anti-fake:\n1. Tunggu candle CLOSE (jangan entry pas wick)\n2. Volume harus confirm\n3. Retest = entry TERBAIK!\n\n#breakout #trading #forex #xauusd #priceaction #fyp",
        "carousel_slides": [
            {"text": "Breakout\nTrading", "sub": "Catch the BIG move! 💥", "hook": "SWIPE →"},
            {"text": "Apa itu\nBreakout?", "sub": "Harga TEMBUS level penting\nS/R, trendline, pattern", "hook": "BASIC"},
            {"text": "REAL vs FAKE", "sub": "Real: volume tinggi, candle besar\nFake: volume rendah, balik masuk", "hook": "⚠️ HATI2"},
            {"text": "Tips Anti-Fake", "sub": "1. Tunggu candle CLOSE\n2. Volume harus confirm\n3. Retest = entry terbaik!", "hook": "💡 TIPS"},
            {"text": "Retest =\nEntry TERBAIK", "sub": "Harga breakout → balik test level\n→ Mantul = ENTRY!\nRisiko kecil, reward besar", "hook": "SAVE 📌"},
        ],
        "narration": "Breakout trading, ini cara buat nangkep pergerakan besar di market. Breakout itu ketika harga tembus level penting, bisa support resistance, trendline, atau pattern. Tapi hati-hati, banyak fake breakout! Cara bedainnya, real breakout itu volume tinggi, candle besar, dan close di luar level. Kalo volume rendah dan candle kecil, kemungkinan besar fake. Tips anti fake breakout, pertama tunggu candle close dulu, jangan entry pas masih wick. Kedua volume harus confirm. Dan yang ketiga, ini favorit gue, tunggu retest! Harga breakout terus balik test level, kalo mantul, itu entry terbaik! Risiko kecil, reward besar.",
        "video_caption": "💥 Breakout Trading — Catch The BIG Move!\nRetest = Entry TERBAIK 🎯\n🔊 Narasi Bahasa Indonesia\n\n#breakout #trading #forex #priceaction #xauusd #fyp",
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
    d.text((40,50), "\U0001f4ca @AlgoExpertHub", fill="#888", font=fs)
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
    all_posts = []
    for t in TOPICS:
        all_posts.append({"type":"text","id":t["id"],"caption":t["text_post"]})
        all_posts.append({"type":"carousel","id":t["id"],"slides":t["carousel_slides"],"caption":t.get("video_caption",t["text_post"])})
        all_posts.append({"type":"video","id":t["id"],"narration":t["narration"],"caption":t["video_caption"]})
    
    random.shuffle(all_posts)
    
    # Start 24h after batch1 (so they don't overlap)
    now = datetime.now(timezone.utc) + timedelta(hours=24)
    
    print(f"\U0001f3b2 BATCH 2 — RANDOMIZED: {len(all_posts)} posts")
    print("="*50)
    
    ok = 0
    for i, post in enumerate(all_posts):
        sched = (now + timedelta(minutes=90*i)).strftime("%Y-%m-%dT%H:%M:%SZ")
        wib = (now + timedelta(minutes=90*i, hours=7)).strftime("%d/%m %H:%M")
        pt = post["type"]
        pid = post["id"]
        
        print(f"\n[{i+1}/{len(all_posts)}] {wib} | {pt.upper():9} | {pid}")
        
        if pt == "text":
            r = requests.post(f"{PB_BASE}/posts", headers=H,
                json={"caption":post["caption"],"social_accounts":ALGO_TEXT,"scheduled_at":sched})
            if r.status_code in [200,201]:
                print(f"  \u2705 Text \u2192 2 accounts"); ok+=1
        
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
                    print(f"  \u2705 Carousel {len(mids)} slides \u2192 5 accounts"); ok+=1
        
        elif pt == "video":
            audio = os.path.join(OUT, f"{pid}_vo.mp3")
            subprocess.run(["edge-tts","--voice","id-ID-ArdiNeural","--rate=-3%",
                "--text",post["narration"],"--write-media",audio],
                capture_output=True, timeout=60)
            
            if os.path.exists(audio) and os.path.getsize(audio) > 1000:
                # Generate slides if not exist
                t = [x for x in TOPICS if x["id"]==pid][0]
                imgs = []
                for j, sl in enumerate(t["carousel_slides"]):
                    p = os.path.join(OUT, f"{pid}_c{j}.jpg")
                    if not os.path.exists(p):
                        create_slide(sl["text"], sl["sub"], sl["hook"], j+1, len(t["carousel_slides"]), p, j)
                    imgs.append(p)
                
                concat = os.path.join(OUT, f"{pid}_concat.txt")
                with open(concat,"w") as f:
                    for img in imgs:
                        f.write(f"file '{img}'\nduration 12\n")
                    f.write(f"file '{imgs[-1]}'\n")
                
                slideshow = os.path.join(OUT, f"{pid}_slide.mp4")
                subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",concat,
                    "-vf","scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:-1:-1:color=black,fps=25",
                    "-c:v","libx264","-pix_fmt","yuv420p","-t","60","-r","25",
                    "-preset","fast","-crf","23",slideshow], capture_output=True, timeout=120)
                
                final = os.path.join(OUT, f"{pid}_final.mp4")
                ad = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                    "-of","default=noprint_wrappers=1:nokey=1",audio],
                    capture_output=True, text=True, timeout=10)
                adur = float(ad.stdout.strip()) if ad.stdout.strip() else 60
                
                subprocess.run(["ffmpeg","-y","-stream_loop","-1","-i",slideshow,"-i",audio,
                    "-c:v","libx264","-preset","fast","-crf","23","-c:a","aac","-b:a","128k",
                    "-t",str(adur),"-map","0:v:0","-map","1:a:0","-pix_fmt","yuv420p",
                    "-shortest",final], capture_output=True, timeout=120)
                
                if os.path.exists(final) and os.path.getsize(final) > 10000:
                    mid = upload_media(final, "video/mp4")
                    if mid:
                        r = requests.post(f"{PB_BASE}/posts", headers=H,
                            json={"caption":post["caption"],"social_accounts":ALL,"media":[mid],"scheduled_at":sched})
                        if r.status_code in [200,201]:
                            print(f"  \u2705 Video+VO \u2192 5 accounts"); ok+=1
    
    print(f"\n{'='*50}")
    print(f"\U0001f3c1 BATCH 2 DONE: {ok}/{len(all_posts)} scheduled")
    print(f"\U0001f4c5 Starts 24h from now, every 90min over 22h")


if __name__ == "__main__":
    main()
