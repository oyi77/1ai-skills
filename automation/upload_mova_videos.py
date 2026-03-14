#!/usr/bin/env python3
"""
Upload MOVA demo videos to CDN
Use imgbb or free hosting for public URLs
"""

import urllib.request
import urllib.parse
import json
from pathlib import Path

IMGBB_API_KEY = "8af9af090dc96e01640ba68b246759ba"
VIDEOS_DIR = Path(__file__).parent / "output" / "mova_demo_videos"
OUTPUT_FILE = Path(__file__).parent / "mova_video_urls.json"

def upload_to_imgbb(video_path):
    """Upload video to imgbb"""

    # Read video data
    with open(video_path, "rb") as f:
        video_data = f.read()

    # Prepare API request
    url = "https://api.imgbb.com/1/upload"

    data = {
        "key": IMGBB_API_KEY
    }

    # Encode video as base64
    import base64
    video_base64 = base64.b64encode(video_data).decode("utf-8")
    data["image"] = video_base64

    encoded_data = urllib.parse.urlencode(data).encode("utf-8")

    req = urllib.request.Request(url, data=encoded_data, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))

        if result.get("success"):
            return {
                "success": True,
                "url": result["data"]["url"],
                "direct_url": result["data"]["url"],
                "display_url": result["data"]["display_url"],
                "delete_url": result["data"]["delete_url"]
            }
        else:
            return {
                "success": False,
                "error": result.get("error", {}).get("message", "Unknown error")
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def upload_all_videos():
    """Upload all 7 videos"""

    print("\n" + "="*70)
    print("📤 UPLOADING MOVA VIDEOS TO IMGBB")
    print("="*70)

    print(f"\nVideos directory: {VIDEOS_DIR}")
    print(f"Total videos: {len(list(VIDEOS_DIR.glob('*.mp4')))}]\n")

    video_files = sorted(VIDEOS_DIR.glob("*.mp4"))

    results = {}
    successful = []
    failed = []

    for i, video_path in enumerate(video_files, 1):
        asset_id = video_path.stem
        file_size_mb = video_path.stat().st_size / (1024 * 1024)

        print(f"[{i}/{len(video_files)}] {asset_id}.mp4 ({file_size_mb:.2f}MB) ...", end=" ")

        result = upload_to_imgbb(video_path)

        if result["success"]:
            url = result["url"]
            print(f"✅")
            print(f"   URL: {url}")
            results[asset_id] = url
            successful.append(asset_id)
        else:
            print(f"❌ {result['error']}")
            failed.append(asset_id)

        # Rate limiting
        if i < len(video_files):
            import time
            time.sleep(1)

    # Save results
    with open(OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=2)

    # Summary
    print("\n" + "="*70)
    print("📊 UPLOAD SUMMARY")
    print("="*70)
    print(f"\n✅ Successful: {len(successful)}/{len(video_files)}")
    print(f"❌ Failed: {len(failed)}/{len(video_files)}")

    if successful:
        print(f"\n📁 Uploaded URLs:")
        for asset_id in successful:
            print(f"   {asset_id}: {results[asset_id]}")

    if failed:
        print(f"\n❌ Failed uploads:")
        for asset_id in failed:
            print(f"   {asset_id}")

    print(f"\n💾 Results saved to: {OUTPUT_FILE}")

    # Generate PostBridge media_urls dict
    print(f"\n" + "="*70)
    print(f"📋 FOR POSTBRIDGE SUBMISSION")
    print("="*70)
    print(f"\nMEDIA_URLS = {json.dumps(results, indent=2)}\n")

    with open(Path(__file__).parent / "media_urls_for_postbridge.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"📄 Simplified file: media_urls_for_postbridge.json")

    print("\n" + "="*70)
    print("✅ UPLOAD COMPLETE")
    print("="*70)

    print("\n🚀 Next: Run PostBridge submission:")
    print("   python postbridge_mova_campaign.py")

    return len(successful) == len(video_files)

if __name__ == "__main__":
    success = upload_all_videos()
    exit(0 if success else 1)