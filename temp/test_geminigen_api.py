#!/usr/bin/env python3
"""
Test GeminiGen API video generation
"""

import requests
import time
import json

# GeminiGen API configuration
API_KEY = "geminiai-04db42d9b996e147df5e33d8b7d42ac3"
API_BASE = "https://api.geminigen.ai/uapi/v1"

def test_video_generation():
    """Test video generation via GeminiGen API"""
    
    # Prepare request
    headers = {
        "x-api-key": API_KEY
    }
    
    data = {
        "prompt": "A rusty old wrench being restored to shiny new condition, satisfying ASMR process, timelapse transformation, workshop setting",
        "model": "grok-3",
        "resolution": "480p",
        "aspect_ratio": "portrait",
        "duration": "6",
        "mode": "custom"
    }
    
    print("🎬 Sending video generation request...")
    print(f"   Prompt: {data['prompt'][:50]}...")
    
    try:
        # Start video generation
        response = requests.post(
            f"{API_BASE}/video-gen/grok",
            headers=headers,
            data=data,
            timeout=30
        )
        
        print(f"\n📡 Response Status: {response.status_code}")
        print(f"📡 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Video generation started!")
            print(f"   UUID: {result.get('uuid')}")
            print(f"   Status: {result.get('status')}")
            
            # Poll for completion
            uuid = result.get('uuid')
            if uuid:
                print(f"\n⏳ Polling for completion...")
                for i in range(60):  # Max 5 minutes
                    time.sleep(5)
                    
                    poll_response = requests.get(
                        f"{API_BASE}/history/{uuid}",
                        headers=headers
                    )
                    
                    if poll_response.status_code == 200:
                        poll_result = poll_response.json()
                        status = poll_result.get('status')
                        percentage = poll_result.get('status_percentage', 0)
                        
                        print(f"   [{i+1}/60] Status: {status} ({percentage}%)")
                        
                        # Status: 1 = processing, 2 = completed, 3 = failed
                        if status == 2:
                            videos = poll_result.get('generated_video', [])
                            if videos:
                                video_url = videos[0].get('video_url') or videos[0].get('video_uri')
                                print(f"\n🎉 SUCCESS! Video URL:")
                                print(f"   {video_url}")
                                return video_url
                        elif status == 3:
                            print(f"\n❌ FAILED: {poll_result.get('error_message')}")
                            return None
                
                print(f"\n⏱️ Timeout after 5 minutes")
        else:
            print(f"\n❌ Request failed!")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"\n❌ Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_video_generation()
