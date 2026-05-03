"""YouTube platform integration for video posting."""

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional

from .base import Platform, PlatformSpec, PLATFORM_SPECS


def get_spec() -> PlatformSpec:
    return PLATFORM_SPECS[Platform.YOUTUBE]


def post_video(
    video_path: str,
    access_token: str,
    title: str,
    description: str = "",
    tags: Optional[list[str]] = None,
    category_id: str = "22",
    privacy_status: str = "public",
) -> Optional[str]:
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    with open(video_path, "rb") as f:
        video_data = f.read()

    metadata = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or [],
            "categoryId": category_id,
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False,
        },
    }

    boundary = "-------314159265358979323846"
    body_parts = []

    body_parts.append(f"--{boundary}\r\n".encode())
    body_parts.append(b'Content-Type: application/json; charset="UTF-8"\r\n\r\n')
    body_parts.append(json.dumps(metadata).encode())
    body_parts.append(b"\r\n")

    body_parts.append(f"--{boundary}\r\n".encode())
    body_parts.append(
        b"Content-Type: video/mp4\r\nContent-Transfer-Encoding: binary\r\n\r\n"
    )
    body_parts.append(video_data)
    body_parts.append(b"\r\n")

    body_parts.append(f"--{boundary}--\r\n".encode())

    body = b"".join(body_parts)

    upload_url = "https://www.googleapis.com/upload/youtube/v3/videos"
    params = urllib.parse.urlencode(
        {"part": "snippet,status", "uploadType": "multipart"}
    )
    url = f"{upload_url}?{params}"

    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", f"multipart/related; boundary={boundary}")
    req.add_header("Authorization", f"Bearer {access_token}")

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))

        if result.get("id"):
            return result["id"]
        print(f"YouTube upload failed: {result}")
        return None
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"YouTube HTTP error: {e.code} - {error_body}")
        return None
    except Exception as e:
        print(f"YouTube upload error: {e}")
        return None


def post_video_simple(
    video_path: str,
    api_key: str,
    title: str,
    description: str = "",
    tags: Optional[list[str]] = None,
) -> Optional[str]:
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    with open(video_path, "rb") as f:
        video_data = f.read()

    metadata = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or [],
            "categoryId": "22",
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        },
    }

    boundary = "-------314159265358979323846"
    body_parts = []

    body_parts.append(f"--{boundary}\r\n".encode())
    body_parts.append(b'Content-Type: application/json; charset="UTF-8"\r\n\r\n')
    body_parts.append(json.dumps(metadata).encode())
    body_parts.append(b"\r\n")

    body_parts.append(f"--{boundary}\r\n".encode())
    body_parts.append(
        b"Content-Type: video/mp4\r\nContent-Transfer-Encoding: binary\r\n\r\n"
    )
    body_parts.append(video_data)
    body_parts.append(b"\r\n")

    body_parts.append(f"--{boundary}--\r\n".encode())

    body = b"".join(body_parts)

    upload_url = "https://www.googleapis.com/upload/youtube/v3/videos"
    params = urllib.parse.urlencode(
        {"part": "snippet,status", "uploadType": "multipart"}
    )
    url = f"{upload_url}?{params}"

    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", f"multipart/related; boundary={boundary}")
    req.add_header("Authorization", f"Bearer {api_key}")

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))

        if result.get("id"):
            return result["id"]
        print(f"YouTube upload failed: {result}")
        return None
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"YouTube HTTP error: {e.code} - {error_body}")
        return None
    except Exception as e:
        print(f"YouTube upload error: {e}")
        return None


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Upload video to YouTube")
    parser.add_argument("video_path", help="Path to the video file")
    parser.add_argument("access_token", help="YouTube access token")
    parser.add_argument("title", help="Video title")
    parser.add_argument("--description", "-d", help="Video description", default="")
    parser.add_argument("--tags", "-t", help="Tags (comma-separated)", default="")
    parser.add_argument(
        "--privacy",
        "-p",
        choices=["public", "private", "unlisted"],
        default="public",
        help="Privacy status",
    )
    args = parser.parse_args()

    tags = args.tags.split(",") if args.tags else None
    video_id = post_video(
        args.video_path,
        args.access_token,
        args.title,
        args.description,
        tags,
        privacy_status=args.privacy,
    )
    if video_id:
        print(f"Uploaded successfully. Video ID: {video_id}")
    else:
        print("Upload failed")
