"""Facebook platform integration for video posting."""

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional

from .base import Platform, PlatformSpec, PLATFORM_SPECS


def get_spec() -> PlatformSpec:
    return PLATFORM_SPECS[Platform.FACEBOOK]


def post_video(
    video_path: str,
    access_token: str,
    page_id: str,
    title: str = "",
    description: str = "",
    published: bool = True,
) -> Optional[str]:
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    with open(video_path, "rb") as f:
        video_data = f.read()

    url = f"https://graph.facebook.com/v21.0/{page_id}/videos"

    metadata = {
        "title": title,
        "description": description,
        "published": published,
        "access_token": access_token,
    }

    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body_parts = []

    body_parts.append(f"--{boundary}\r\n".encode())
    body_parts.append(
        b'Content-Disposition: form-data; name="file"; filename="video.mp4"\r\n'
    )
    body_parts.append(b"Content-Type: video/mp4\r\n\r\n")
    body_parts.append(video_data)
    body_parts.append(b"\r\n")

    for key, value in metadata.items():
        body_parts.append(f"--{boundary}\r\n".encode())
        body_parts.append(
            f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode()
        )
        body_parts.append(f"{value}\r\n".encode())

    body_parts.append(f"--{boundary}--\r\n".encode())

    body = b"".join(body_parts)

    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))

        if result.get("id"):
            return result["id"]
        print(f"Facebook upload failed: {result}")
        return None
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"Facebook HTTP error: {e.code} - {error_body}")
        return None
    except Exception as e:
        print(f"Facebook upload error: {e}")
        return None


def post_video_simple(
    video_path: str,
    access_token: str,
    page_id: str,
    title: str = "",
    description: str = "",
) -> Optional[str]:
    return post_video(video_path, access_token, page_id, title, description)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Upload video to Facebook")
    parser.add_argument("video_path", help="Path to the video file")
    parser.add_argument("access_token", help="Facebook access token")
    parser.add_argument("page_id", help="Facebook page ID")
    parser.add_argument("title", help="Video title", default="")
    parser.add_argument("--description", "-d", help="Video description", default="")
    args = parser.parse_args()

    video_id = post_video(
        args.video_path,
        args.access_token,
        args.page_id,
        args.title,
        args.description,
    )
    if video_id:
        print(f"Uploaded successfully. Video ID: {video_id}")
    else:
        print("Upload failed")
