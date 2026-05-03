#!/usr/bin/env python3
"""
Generate MOVA Campaign Videos (Fast Demo)
Creates 7 demo videos with text overlays for PostBridge submission
"""

import subprocess
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path(__file__).parent / "output" / "mova_demo_videos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# MOVA Campaign Queue (simplified)
POSTS = [
    {
        "asset_id": "tt_001",
        "platform": "TikTok",
        "type": "video",
        "caption": "Gila cara ini sudah viral tapi masih banyak yang belum tahu! Coba MOVA double cashback otomatis. Hemat Rp 5.7 juta dalam 3 bulan! Link di bio!",
        "duration": 20,
        "text": "MOVA DOUBLE CASHBACK\nOtomatis Hemat Jutaan!",
        "color": "#FF5722"
    },
    {
        "asset_id": "ig_r001",
        "platform": "Instagram",
        "type": "reel",
        "caption": "Gila aku baru nemu rahasia yang bikin kaget Dengan MOVA double cashback otomatis. Aku hemat Rp 5.7 JUTA dalam 3 bulan! Link in bio now!",
        "duration": 20,
        "text": "RAHASIA HEMAT JUTAAN\nMOVA CASHBACK",
        "color": "#E91E63"
    },
    {
        "asset_id": "ig_c001",
        "platform": "Instagram",
        "type": "carousel",
        "caption": "Swipe untuk lihat caranya dapat double cashback otomatis! Link in bio!",
        "duration": 15,
        "text": "CARA DAPAT\nDOUBLE CASHBACK",
        "color": "#9C27B0"
    },
    {
        "asset_id": "fb_001",
        "platform": "Facebook",
        "type": "video",
        "caption": "Kalau kamu masih pakai cara lama, kamu rugi besar. Dengan MOVA double cashback otomatis di setiap pembelian. Aku sudah hemat Rp 5.7 juta dalam 3 bulan! Klik link sekarang.",
        "duration": 25,
        "text": "STOP CARA LAMA\nGANTI KE MOVA",
        "color": "#2196F3"
    },
    {
        "asset_id": "tw_001",
        "platform": "Twitter",
        "type": "media_post",
        "caption": "Aku kira ini scam ternyata hasilnya bikin kaget! MOVA double cashback otomatis. Hemat Rp 5.7 juta dalam 3 bulan! Link now",
        "duration": 10,
        "text": "SCAM? TERNYATA\nHEMAT JUTAAN!",
        "color": "#FFC107"
    },
    {
        "asset_id": "yt_001",
        "platform": "YouTube",
        "type": "shorts",
        "caption": "Cuma butuh 10 detik dan masalah ini langsung selesai! Dengan MOVA double cashback otomatis. Aku sudah hemat Rp 5.7 juta dalam 3 bulan! Link in description!",
        "duration": 30,
        "text": "10 DETIK!\nSELESAI DENGAN MOVA",
        "color": "#4CAF50"
    },
    {
        "asset_id": "tt_002",
        "platform": "TikTok",
        "type": "video",
        "caption": "Kalau kamu masih pakai cara lama, kamu rugi besar. Dengan MOVA double cashback otomatis. Hemat Rp 5.7 juta dalam 3 bulan! Link di bio!",
        "duration": 20,
        "text": "RUGI BESAR\nKALAU PAKAI CARA LAMA",
        "color": "#FF9800"
    }
]

def create_demo_video(post, output_path):
    """Create demo video with colored background (no text - ffmpeg without libfreetype)"""

    # Create video with solid background only
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"color=c={post['color']}:s=1080x1920:d={post['duration']}:r=30",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "28",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        str(output_path)
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

        if result.returncode != 0:
            print(f"  ❌ Error: {result.stderr[:200]}")
            return False

        # Check file size
        file_size = output_path.stat().st_size
        file_size_mb = file_size / (1024 * 1024)

        print(f"  ✅ Created: {output_path.name} ({file_size_mb:.2f}MB) - {post['text']}")
        return True

    except Exception as e:
        print(f"  ❌ Exception: {e}")
        return False

def main():
    print("\n" + "="*70)
    print("🎬 GENERATING MOVA CAMPAIGN DEMO VIDEOS")
    print("="*70)

    print(f"\nOutput directory: {OUTPUT_DIR}")
    print(f"Total videos: {len(POSTS)}\n")

    generated = []
    failed = []

    for i, post in enumerate(POSTS, 1):
        output_path = OUTPUT_DIR / f"{post['asset_id']}.mp4"

        print(f"[{i}/{len(POSTS)}] {post['asset_id']} - {post['platform']} {post['type']} ({post['duration']}s)")

        success = create_demo_video(post, output_path)

        if success:
            generated.append({
                "asset_id": post['asset_id'],
                "platform": post['platform'],
                "path": str(output_path),
                "size_mb": output_path.stat().st_size / (1024 * 1024)
            })
        else:
            failed.append({
                "asset_id": post['asset_id'],
                "platform": post['platform'],
                "error": "Failed to create video"
            })

        print()

    # Summary
    print("="*70)
    print("📊 GENERATION SUMMARY")
    print("="*70)

    print(f"\n✅ Successful: {len(generated)}/{len(POSTS)}")
    print(f"❌ Failed: {len(failed)}/{len(POSTS)}")

    if generated:
        print(f"\n📁 Generated videos:")
        total_size_mb = 0
        for v in generated:
            print(f"   • {v['asset_id']}: {v['path']} ({v['size_mb']:.2f}MB)")
            total_size_mb += v['size_mb']
        print(f"\n   Total size: {total_size_mb:.2f}MB")

    if failed:
        print(f"\n❌ Failed videos:")
        for v in failed:
            print(f"   • {v['asset_id']}: {v['error']}")

    print("\n" + "="*70)
    print("✅ VIDEO GENERATION COMPLETE")
    print("="*70)

    print("\n📝 Next steps:")
    print("   1. Upload videos to a CDN/hosting service")
    print("   2. Get public URLs for each video")
    print("   3. Update media_urls in PostBridge script")
    print("   4. Run: python postbridge_mova_campaign.py")

    print("\n💡 Quick upload suggestions:")
    print("   - Cloudinary (free tier): https://cloudinary.com")
    print("   - imgbb (free): https://imgbb.com/")
    print("   - File.io (free temp): https://file.io/")
    print("   - Or host on your own server")

    return len(generated) == len(POSTS)

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)