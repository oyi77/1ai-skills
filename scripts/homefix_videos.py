#!/usr/bin/env python3
"""
Generate 3 sample videos for HomeFix Indonesia - Vinyl Floor Tiles
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

# HomeFix Vinyl Floor Tiles concepts
HOMEFIX_CONCEPTS = {
    "homefix_before_after": {
        "prompt": "Vinyl floor tiles before and after transformation, old worn floor vs new vinyl tiles, realistic lighting, 9:16 portrait, home interior renovation",
        "hashtags": "#vinylfloor #homeimprovement #renovation #flooring #transformation",
        "caption": "Before & After! Vinyl tiles makeover 🏠 #vinylfloor #renovation",
    },
    "homefix_installation": {
        "prompt": "Person installing vinyl floor tiles, professional installation process, smooth motion, 9:16 portrait, home renovation video",
        "hashtags": "#vinylfloor #diy #homereno #flooring #installation",
        "caption": "Easy DIY installation! Vinyl tiles 🛠️ #vinylfloor #diy",
    },
    "homefix_showcase": {
        "prompt": "Beautiful living room with premium vinyl floor tiles, modern interior design, warm lighting, 9:16 portrait, real estate video",
        "hashtags": "#vinylfloor #homedesign #interior #livingroom #flooring",
        "caption": "Premium vinyl tiles transform your home ✨ #vinylfloor #homedesign",
    },
}

async def generate_homefix_videos():
    """Generate 3 videos for HomeFix Indonesia"""

    gen = ContentGenerator()

    results = []

    for concept_name, concept in HOMEFIX_CONCEPTS.items():
        print(f"\n{'='*60}")
        print(f"Generating: {concept_name}")
        print(f"{'='*60}")

        try:
            # Generate video using the concept
            result = await gen.generate(
                prompt=concept["prompt"],
                platform="tiktok",
                template="larry_viral",
                target_duration=15,  # 15 seconds
                skip_image=False,
            )

            video_path = result.get("video")

            if video_path and Path(video_path).exists():
                print(f"✅ Success: {video_path}")
                print(f"   Caption: {concept['caption']}")

                results.append({
                    "concept": concept_name,
                    "video": video_path,
                    "caption": concept["caption"],
                    "hashtags": concept["hashtags"],
                })
            else:
                print(f"❌ Failed: No video generated")

        except Exception as e:
            print(f"❌ Error: {e}")

    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Total generated: {len(results)}/{len(HOMEFIX_CONCEPTS)}")

    if results:
        print(f"\nVideos:")
        for r in results:
            print(f"  • {r['concept']}: {r['video']}")

        # Save summary
        summary_file = Path("/home/openclaw/.openclaw/workspace/output/homefix_videos_summary.json")
        import json
        with open(summary_file, 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"\nSummary saved to: {summary_file}")

        return results
    else:
        print("\n❌ No videos generated successfully")
        return None

if __name__ == '__main__':
    print("🎬 Generating 3 sample videos for HomeFix Indonesia")
    print("   Product: Vinyl Floor Tiles (1 pack)")
    print("   Target: TikTok 9:16, 15 seconds\n")

    results = asyncio.run(generate_homefix_videos())

    if results:
        print(f"\n✅ All videos ready for HomeFix Indonesia outreach!")
    else:
        print(f"\n❌ Video generation failed")
        sys.exit(1)
