"""ImgBB image uploader for hosting images."""

import base64
import json
import os
import urllib.parse
import urllib.request
from typing import Optional


def upload_image(
    image_path: str, api_key: str, name: Optional[str] = None
) -> Optional[str]:
    """Upload image to ImgBB."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    url = "https://api.imgbb.com/1/upload"
    params = urllib.parse.urlencode(
        {
            "key": api_key,
            "image": image_data,
            "name": name or os.path.basename(image_path),
        }
    )

    data = params.encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))

        if result.get("success"):
            return result["data"]["url"]
        print(f"ImgBB upload failed: {result.get('error', {}).get('message')}")
        return None
    except Exception as e:
        print(f"ImgBB upload error: {e}")
        return None


def upload_from_base64(
    base64_data: str, api_key: str, name: Optional[str] = None
) -> Optional[str]:
    """Upload image to ImgBB from base64 data."""
    url = "https://api.imgbb.com/1/upload"
    params = urllib.parse.urlencode(
        {
            "key": api_key,
            "image": base64_data,
            "name": name or "uploaded_image",
        }
    )

    data = params.encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))

        if result.get("success"):
            return result["data"]["url"]
        print(f"ImgBB upload failed: {result.get('error', {}).get('message')}")
        return None
    except Exception as e:
        print(f"ImgBB upload error: {e}")
        return None


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Upload image to ImgBB")
    parser.add_argument("image_path", help="Path to the image file")
    parser.add_argument("api_key", help="ImgBB API key")
    parser.add_argument("--name", "-n", help="Optional name for the image")
    args = parser.parse_args()

    url = upload_image(args.image_path, args.api_key, args.name)
    if url:
        print(f"Uploaded: {url}")
    else:
        print("Upload failed")
