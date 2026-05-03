"""TikTok platform integration for video posting."""

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional

from .base import Platform, PlatformSpec, PLATFORM_SPECS


def get_spec() -> PlatformSpec:
    return PLATFORM_SPECS[Platform.TIKTOK]


def post_video(
    video_path: str,
    access_token: str,
    title: str,
    description: str = "",
    tags: Optional[list[str]] = None,
    api_key: Optional[str] = None,
) -> Optional[str]:
    """Upload video to TikTok."""
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    with open(video_path, "rb") as f:
        video_data = f.read()

    url = "https://open.tiktokapis.com/v2/video/upload/"

    metadata = {
        "title": title[:150],
        "description": description,
        "privacy_level": "PUBLIC",
    }

    if tags:
        metadata["hashtags"] = json.dumps(
            [{"name": tag.replace("#", "")} for tag in tags]
        )

    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body_parts = []

    body_parts.append(f"--{boundary}\r\n".encode())
    body_parts.append(
        b'Content-Disposition: form-data; name="video"; filename="'
        + os.path.basename(video_path).encode()
        + b'"\r\n'
    )
    body_parts.append(b"Content-Type: video/mp4\r\n\r\n")
    body_parts.append(video_data)
    body_parts.append(b"\r\n")

    body_parts.append(f"--{boundary}\r\n".encode())
    body_parts.append(b'Content-Disposition: form-data; name="metadata"\r\n')
    body_parts.append(b"Content-Type: application/json\r\n\r\n")
    body_parts.append(json.dumps(metadata).encode())
    body_parts.append(b"\r\n")

    body_parts.append(f"--{boundary}--\r\n".encode())

    body = b"".join(body_parts)

    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    req.add_header("Authorization", f"Bearer {access_token}")

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))

        if result.get("data") and result["data"].get("video_id"):
            return result["data"]["video_id"]
        print(f"TikTok upload failed: {result}")
        return None
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"TikTok HTTP error: {e.code} - {error_body}")
        return None
    except Exception as e:
        print(f"TikTok upload error: {e}")
        return None


def post_video_simple(
    video_path: str,
    api_key: str,
    title: str,
    description: str = "",
    tags: Optional[list[str]] = None,
) -> Optional[str]:
    """Upload video to TikTok using API key."""
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    with open(video_path, "rb") as f:
        video_data = f.read()

    url = "https://open.tiktokapis.com/v2/video/upload/"

    metadata = {
        "title": title[:150],
        "description": description,
        "privacy_level": "PUBLIC",
    }

    if tags:
        metadata["hashtags"] = json.dumps(
            [{"name": tag.replace("#", "")} for tag in tags]
        )

    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body_parts = []

    body_parts.append(f"--{boundary}\r\n".encode())
    body_parts.append(
        b'Content-Disposition: form-data; name="video"; filename="'
        + os.path.basename(video_path).encode()
        + b'"\r\n'
    )
    body_parts.append(b"Content-Type: video/mp4\r\n\r\n")
    body_parts.append(video_data)
    body_parts.append(b"\r\n")

    body_parts.append(f"--{boundary}\r\n".encode())
    body_parts.append(b'Content-Disposition: form-data; name="metadata"\r\n')
    body_parts.append(b"Content-Type: application/json\r\n\r\n")
    body_parts.append(json.dumps(metadata).encode())
    body_parts.append(b"\r\n")

    body_parts.append(f"--{boundary}--\r\n".encode())

    body = b"".join(body_parts)

    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    req.add_header("Authorization", f"Bearer {api_key}")

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))

        if result.get("data") and result["data"].get("video_id"):
            return result["data"]["video_id"]
        print(f"TikTok upload failed: {result}")
        return None
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"TikTok HTTP error: {e.code} - {error_body}")
        return None
    except Exception as e:
        print(f"TikTok upload error: {e}")
        return None


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Upload video to TikTok")
    parser.add_argument("video_path", help="Path to the video file")
    parser.add_argument("access_token", help="TikTok access token")
    parser.add_argument("title", help="Video title")
    parser.add_argument("--description", "-d", help="Video description", default="")
    parser.add_argument("--tags", "-t", help="Hashtags (comma-separated)", default="")
    args = parser.parse_args()

    tags = args.tags.split(",") if args.tags else None
    video_id = post_video(
        args.video_path,
        args.access_token,
        args.title,
        args.description,
        tags,
    )
    if video_id:
        print(f"Uploaded successfully. Video ID: {video_id}")
    else:
        print("Upload failed")
