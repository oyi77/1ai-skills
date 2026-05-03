#!/usr/bin/env python3
"""
Upload MOVA demo videos to file.io (free temporary hosting)
Supports video files
"""

import urllib.request
import urllib.parse
import json
import base64
from pathlib import Path

VIDEOS_DIR = Path(__file__).parent / "output" / "mova_demo_videos"
OUTPUT_FILE = Path(__file__).parent / "mova_video_urls.json"

# File.io API
FILEIO_API_KEY = "8af9af090dc96e01640ba68b246759ba"
FILEIO_API_URL = "https://file.io"

# BytePlus Seedance API
BYTEPLUS_API_KEY = "cac5cfc1-e30f-47bb-b8b8-e861ffda28ea"
BYTEPLUS_BASE_URL = "https://ark.ap-southeast.bytepluses.com/api/v3"

# PostBridge API
POST_BRIDGE_API_KEY = "pb_live_AFm842jzqKVNjREpJH8hTi"
POST_BRIDGE_BASE_URL = "https://api.post-bridge.com/v1"

# MOVA Campaign Queue
QUEUE_FILE = Path(__file__).parent.parent / "autopilot_affiliate_engine" / "postbridge_queue.json"

# Media URLs File
MEDIA_URLS_FILE = Path(__file__).parent / "media_urls_for_postbridge.json"

# Output Directory
OUTPUT_DIR = Path(__file__).parent / "output" / "mova_demo_videos"

# PostBridge Log File
LOG_FILE = Path(__file__).parent / "postbridge_submission_log.json"

# Function to upload video to file.io
def upload_to_fileio(video_path):
    """Upload video to file.io (free temp hosting)"""
    # Read video data
    with open(video_path, "rb") as f:
        video_data = f.read()

    # Base64 encode
    video_base64 = base64.b64encode(video_data).decode("utf-8")

    # Prepare API request
    url = FILEIO_API_URL

    payload = {
        "file": video_base64,
        "expires": "7d"  # 7 days expiry
    }

    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), method="POST")
    req.add_header("Content-Type", "application/json")

    ssl_context = ssl.create_default_context()

    try:
        with urllib.request.urlopen(req, context=ssl_context, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        return {"error": "HTTP Error", "message": error_body}
    except Exception as e:
        return {"error": "Exception", "message": str(e)}

def upload_all_videos():
    """Upload all 7 videos"""

    print("\n" + "="*70)
    print("📤 UPLOADING MOVA VIDEOS TO FILE.IO (Free 7d Hosting)")
    print("="*70)

    print(f"\nVideos directory: {VIDEOS_DIR}")
    print(f"Total videos: {len(list(VIDEOS_DIR.glob('*.mp4')))}\n")

    video_files = sorted(VIDEOS_DIR.glob("*.mp4"))

    results = {}
    successful = []
    failed = []

    for i, video_path in enumerate(video_files, 1):
        asset_id = video_path.stem
        file_size_mb = video_path.stat().st_size / (1024 * 1024)

        print(f"[{i}/{len(video_files)}] {asset_id}.mp4 ({file_size_mb:.2f}MB) ...", end=" ")

        result = upload_to_fileio(video_path)

        if result["success"]:
            url = result["url"]
            print(f"   ✅")
            print(f"   URL: {url}")
            results[asset_id] = url
            successful.append(asset_id)
        else:
            print(f"   ❌ {result['error']}")
            failed.append(asset_id)

        # Rate limiting
        if i < len(video_files):
            time.sleep(1)

    # Summary
    print("\n" + "="*70)
    print("📊 UPLOAD SUMMARY")
    print("="*70)

    print(f"\n✅ Successful: {len(successful)}/{len(video_files)}")
    print(f"❌ Failed: {len(failed)}/{len(video_files)}")

    if successful:
        print(f"\n📁 Uploaded URLs:")
        for asset_id in successful:
            print(f"   • {asset_id}: {results[asset_id]}")
        print(f"\n   Total size: {sum([results[v] for v in successful])}")

    if failed:
        print(f"\n❌ Failed uploads:")
        for asset_id in failed:
            print(f"   • {asset_id}")

    print(f"\n💾 Results saved to: {OUTPUT_FILE}")

    # Generate PostBridge media_urls dict
    print(f"\n" + "="*70)
    print("📋 FOR POSTBRIDGE SUBMISSION")
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