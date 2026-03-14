
import os
import requests
import base64
import time

NVIDIA_API_KEY = "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"
# SVD endpoint for NVIDIA NIM
# Usually it is /v1/genai/stabilityai/stable-video-diffusion
URL = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-video-diffusion"

headers = {
    "Authorization": f"Bearer {NVIDIA_API_KEY}",
    "Accept": "application/json",
}

payload = {
    "image": "https://docs.nvidia.com/cloud-functions/user-guide/_images/sdxl-text-to-image.png",
    "seed": 0,
    "cfg_scale": 1.8,
    "motion_bucket_id": 127
}

print("Testing NVIDIA SVD...")
try:
    response = requests.post(URL, headers=headers, json=payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ NVIDIA SVD endpoint is reachable!")
        # SVD usually returns a task ID or a base64 video
        print(response.json().keys())
    else:
        print(f"❌ Failed: {response.text[:200]}")
except Exception as e:
    print(f"❌ Error: {e}")
