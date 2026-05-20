#!/usr/bin/env python3
"""Automated Hugging Face Space Creator
Run: python3 submit_to_huggingface.py"""

import requests
import json
import os
import subprocess


def create_hf_space():
    """Create Hugging Face Space for 1ai-skills"""

    # Get token from user or env
    token = os.environ.get("HF_TOKEN")
    if not token:
        print("❌ Need Hugging Face token")
        print("Get one at: https://huggingface.co/settings/tokens")
        print("Then run: export HF_TOKEN='your_token'")
        return False

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Create space
    data = {
        "name": "1ai-skills",
        "sdk": "static",
        "license": "mit",
        "description": "139 world-class AI skills featuring Black Edge intelligence",
        "tags": ["ai", "skills", "trading", "agents"],
    }

    response = requests.post(
        "https://huggingface.co/api/repos/create", headers=headers, json=data
    )

    if response.status_code == 200:
        print("✅ Hugging Face Space created!")
        print(f"URL: https://huggingface.co/spaces/oyi77/1ai-skills")

        # Push files
        subprocess.run(
            ["git", "push", "https://huggingface.co/spaces/oyi77/1ai-skills"]
        )

        return True
    else:
        print(f"❌ Error: {response.text}")
        return False


if __name__ == "__main__":
    create_hf_space()
