#!/usr/bin/env python3
"""
Generate the 3rd video for HomeFix - Installation concept
"""

import asyncio
import sys
from pathlib import Path

# Add skills to path
sys.path.insert(0, '/home/openclaw/.openclaw/workspace/skills/content-generator/scripts')
sys.path.insert(0, '/home/openclaw/.openclaw/workspace/skills/1ai-skills/content/content-generator/scripts')

try:
    from generator import ContentGenerator
except:
    print("Error importing ContentGenerator")
    sys.exit(1)

async def generate_installation_video():
    """Generate installation video for HomeFix"""

    gen = ContentGenerator()

    concept = {
        "prompt": "Person installing vinyl floor tiles, professional installation process, smooth motion, 9:16 portrait, home renovation video, clear visibility of tile placement",
        "hashtags": "#vinylfloor #diy #homereno #flooring #installation",
        "caption": "Easy DIY installation! Vinyl tiles 🛠️ #vinylfloor #diy",
    }

    print(f"\n{'='*60}")
    print("Generating: homefix_installation")
    print(f"{'='*60}")

    try:
        result = await gen.generate(
            prompt=concept["prompt"],
            platform="tiktok",
            template="larry_viral",
            target_duration=15,
            skip_image=False,
        )

        video_path = result.get("video")

        if video_path and Path(video_path).exists():
            print(f"✅ Success: {video_path}")
            print(f"   Caption: {concept['caption']}")

            # Upload to Drive
            import subprocess
            upload_cmd = [
                'gog', 'drive', 'upload', video_path,
                '--parent', '1WZ5nVhee4nlAtvb83VmCEBRtaEAS8tv2',
                '--account', 'muchammadizzuddin@gmail.com'
            ]
            subprocess.run(upload_cmd, capture_output=True, text=True)

            return video_path
        else:
            print(f"❌ Failed: No video generated")
            return None

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == '__main__':
    print("🎬 Generating 3rd video: homefix_installation")

    result = asyncio.run(generate_installation_video())

    if result:
        print(f"\n✅ Video ready and uploaded to Drive!")
    else:
        print(f"\n❌ Video generation failed")
        sys.exit(1)
