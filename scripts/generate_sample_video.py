#!/usr/bin/env python3
"""
Generate 1 Sample Video for Jendralbot - Test Run
Using BytePlus Seedance with API key from environment variables
"""

import asyncio
import os
import aiohttp
from pathlib import Path

# Get API key from environment
BYTEPLUS_API_KEY = os.getenv('BYTEPLUS_API_KEY')
if not BYTEPLUS_API_KEY:
    print("❌ ERROR: BYTEPLUS_API_KEY not found in environment")
    print("   Set with: export BYTEPLUS_API_KEY=your_key")
    exit(1)

print(f"✅ API Key found (masked): {BYTEPLUS_API_KEY[:8]}...{BYTEPLUS_API_KEY[-8:]}")

# BytePlus Seedance API configuration
BASE_URL = "https://ark.ap-southeast.bytepluses.com/api/v3"
CREATE_TASK_ENDPOINT = f"{BASE_URL}/contents/generations/tasks"
GET_TASK_ENDPOINT = f"{BASE_URL}/contents/generations/tasks"

# Sample product: Guru Pintar AI
SAMPLE_PRODUCT = {
    "name": "Guru Pintar AI",
    "price": "GRATIS",
    "link": "https://lynk.id/jendralbot/6821op5e24kn",
    "hook": "STOP! Konten manual makan waktu 4 jam per post!",
    "video_prompt": "Professional content creator working with AI technology, dark modern workspace, glowing screens showing AI interface, smooth motion, cinematic quality, TikTok viral style, 9:16 vertical format",
    "hashtag": "#AI #contentcreation #productivity #automation #FREE #tutorial"
}

async def create_byteplus_task(prompt, ratio="9:16"):
    """Create video generation task with BytePlus Seedance."""
    payload = {
        "model": "seedance-1-0-lite-t2v-250428",
        "content": [{"type": "text", "text": prompt}],
        "ratio": ratio
    }
    
    headers = {
        "Host": "ark.ap-southeast.bytepluses.com",
        "Authorization": f"Bearer {BYTEPLUS_API_KEY}",  # Add Bearer token!
        "Content-Type": "application/json"
    }
    
    print(f"\n📤 Sending request to: {CREATE_TASK_ENDPOINT}")
    print(f"   Headers: Authorization: Bearer {BYTEPLUS_API_KEY[:8]}...{BYTEPLUS_API_KEY[-8:]}")
    print(f"   Payload: model={payload['model']}, ratio={payload['ratio']}")
    
    async with aiohttp.ClientSession() as session:
        async with session.post(CREATE_TASK_ENDPOINT, json=payload, headers=headers) as resp:
            print(f"   Response status: {resp.status}")
            data = await resp.json()
            return data

async def get_byteplus_task(task_id):
    """Get task status and result from BytePlus Seedance."""
    url = f"{GET_TASK_ENDPOINT}/{task_id}"
    
    headers = {
        "Host": "ark.ap-southeast.bytepluses.com",
        "Authorization": f"Bearer {BYTEPLUS_API_KEY}"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            data = await resp.json()
            return data

async def generate_sample_video():
    """Generate 1 sample video using BytePlus Seedance."""

    print("="*80)
    print("🎬 SAMPLE VIDEO GENERATION TEST - WITH API KEY")
    print("="*80)
    print()
    print(f"Product: {SAMPLE_PRODUCT['name']}")
    print(f"Price: {SAMPLE_PRODUCT['price']}")
    print(f"Link: {SAMPLE_PRODUCT['link']}")
    print(f"Hook: {SAMPLE_PRODUCT['hook']}")
    print()
    print("="*80)

    # Build prompt
    full_prompt = f"""{SAMPLE_PRODUCT['video_prompt']}

Hook: {SAMPLE_PRODUCT['hook']}
Product: {SAMPLE_PRODUCT['name']}
Link: {SAMPLE_PRODUCT['link']}
Hashtag: {SAMPLE_PRODUCT['hashtag']}"""

    print("\n📝 Video Prompt:")
    print("-"*80)
    print(full_prompt)
    print("-"*80)

    try:
        print("\n🔄 Generating video with BytePlus Seedance...")
        print("   Model: seedance-1-0-lite-t2v-250428")
        print("   Ratio: 9:16 (vertical for TikTok/IG/YT)")
        print("   Expected time: ~20 seconds...")

        # Create task
        task_result = await create_byteplus_task(full_prompt, ratio="9:16")
        
        print(f"\n📭 Full response: {task_result}")

        if task_result.get("id"):
            task_id = task_result["id"]
            print(f"\n✅ Task created: {task_id}")
        elif task_result.get("error"):
            error = task_result.get("error", {})
            print(f"\n❌ API Error: Code={error.get('code')}, Message={error.get('message')}")
            print(f"   Request ID: {error.get('request_id')}")
            return {"success": False, "error": task_result}
        else:
            print(f"\n❌ Unexpected response: {task_result}")
            return {"success": False, "error": "Unexpected response"}

        # Poll for completion
        print("\n⏳ Polling for completion...")
        import time

        max_polls = 30
        poll_interval = 2

        for i in range(max_polls):
            await asyncio.sleep(poll_interval)
            
            status = await get_byteplus_task(task_id)
            task_status = status.get("status")
            
            if task_status == "succeeded":
                print(f"\n✅ Generation completed!")

                # Get video URL
                video_url = status.get("content", {}).get("video_url")
                print(f"   Video URL: {video_url}")

                # Download video
                print(f"\n📥 Downloading video...")

                # Use same headers with Bearer token
                download_headers = {
                    "Authorization": f"Bearer {BYTEPLUS_API_KEY}"
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(video_url, headers=download_headers) as resp:
                        print(f"   Download response: HTTP {resp.status}")
                        
                        if resp.status == 200:
                            video_data = await resp.read()

                            # Save to file
                            output_dir = Path.home() / ".openclaw" / "workspace" / "content" / "samples"
                            output_dir.mkdir(parents=True, exist_ok=True)

                            output_file = output_dir / "sample_video_9x16.mp4"
                            with open(output_file, "wb") as f:
                                f.write(video_data)

                            file_size = len(video_data) / (1024 * 1024)  # MB
                            print(f"\n✅ Video saved!")
                            print(f"   File: {output_file}")
                            print(f"   Size: {file_size:.2f} MB")

                            return {
                                "success": True,
                                "file_path": str(output_file),
                                "file_size_mb": file_size,
                                "video_url": video_url
                            }
                        else:
                            print(f"\n❌ Failed to download: HTTP {resp.status}")
                            # Try to read error body
                            error_body = await resp.text()
                            print(f"   Error body: {error_body}")
                            return {"success": False, "error": f"HTTP {resp.status}"}

            elif task_status == "failed":
                error_msg = status.get("error", {}).get("message", "Unknown error")
                error_code = status.get("error", {}).get("code", "Unknown")
                print(f"\n❌ Generation failed: Code={error_code}, Message={error_msg}")
                return {"success": False, "error": error_msg}

            else:
                progress = ((i + 1) / max_polls) * 100
                print(f"   Status: {task_status} ({progress:.0f}%)")

        print("\n❌ Timeout: Task did not complete in 60 seconds")
        return {"success": False, "error": "Timeout"}

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    try:
        result = asyncio.run(generate_sample_video())

        if result.get("success"):
            print("\n" + "="*80)
            print("✅ SUCCESS! Video generated")
            print("="*80)
            print(f"\nFile: {result['file_path']}")
            print(f"Size: {result['file_size_mb']:.2f} MB")
            print("\n📤 Ready to send to Telegram!")
            print("="*80)
            
            # Send to Telegram
            print("\n📱 Sending to Telegram...")
            from message import send_response
            
            try:
                message_result = send_response(
                    media_path=result['file_path'],
                    caption=f"✅ SAMPLE VIDEO GENERATED!\n\nProduct: {SAMPLE_PRODUCT['name']}\nSize: {result['file_size_mb']:.2f} MB\n\nFormat: 9:16 vertical\nPlatform: TikTok/IG Reels/YT Shorts\n\nFile: {result['file_path']}"
                )
                print("✅ Sent to Telegram!")
            except Exception as e:
                print(f"⚠️ Failed to send: {e}")
        else:
            print("\n" + "="*80)
            print("❌ FAILED")
            print("="*80)
            print(f"Error: {result.get('error')}")
            print("="*80)

    except KeyboardInterrupt:
        print("\n\n⚠️ Generation interrupted")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()