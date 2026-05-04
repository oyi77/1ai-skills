#!/usr/bin/env python3
import requests
import os

def create_hf_space():
    token = os.environ.get('HF_TOKEN')
    if not token:
        print("NEED: export HF_TOKEN='your_token'")
        print("GET: https://huggingface.co/settings/tokens")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "name": "1ai-skills",
        "sdk": "static",
        "license": "mit",
        "description": "139 world-class AI skills featuring Black Edge intelligence",
        "tags": ["ai", "skills", "trading", "agents"]
    }
    
    response = requests.post(
        "https://huggingface.co/api/repos/create",
        headers=headers,
        json=data
    )
    
    if response.status_code == 200:
        print("SUCCESS: Hugging Face Space created!")
        print(f"URL: https://huggingface.co/spaces/oyi77/1ai-skills")
        return True
    else:
        print(f"Error: {response.text}")
        return False

if __name__ == "__main__":
    create_hf_space()
