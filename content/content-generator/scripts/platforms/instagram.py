"""Instagram platform integration for video posting."""

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional

from .base import Platform, PlatformSpec, PLATFORM_SPECS


def get_spec() -> PlatformSpec:
    return PLATFORM_SPECS[Platform.INSTAGRAM]


def post_video(
    video_path: str,
    access_token: str,
    caption: str = "",
    media_type: str = "REELS",
) -> Optional[str]:
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    with open(video_path, "rb") as f:
        video_data = f.read()

    init_url = "https://graph.instagram.com/v21.0/me/media"
    params = urllib.parse.urlencode(
        {
            "media_type": media_type,
            "video_url": "",
            "caption": caption,
            "access_token": access_token,
        }
    )

    init_req = urllib.request.Request(f"{init_url}?{params}", method="POST")
    try:
        with urllib.request.urlopen(init_req) as response:
            init_result = json.loads(response.read().decode("utf-8"))

        if "id" not in init_result:
            print(f"Instagram media creation failed: {init_result}")
            return None

        media_id = init_result["id"]
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"Instagram HTTP error: {e.code} - {error_body}")
        return None
    except Exception as e:
        print(f"Instagram error: {e}")
        return None

    upload_url = f"https://graph.instagram.com/v21.0/{media_id}"
    params = urllib.parse.urlencode({"access_token": access_token})

    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body_parts = []

    body_parts.append(f"--{boundary}\r\n".encode())
    body_parts.append(
        b'Content-Disposition: form-data; name="video"; filename="video.mp4"\r\n'
    )
    body_parts.append(b"Content-Type: video/mp4\r\n\r\n")
    body_parts.append(video_data)
    body_parts.append(b"\r\n")

    body_parts.append(f"--{boundary}--\r\n".encode())

    body = b"".join(body_parts)

    req = urllib.request.Request(f"{upload_url}?{params}", data=body, method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))

        if result.get("hache_error_code") == 0 or result.get("id"):
            return media_id
        print(f"Instagram upload status: {result}")
        return media_id
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"Instagram HTTP error: {e.code} - {error_body}")
        return media_id
    except Exception as e:
        print(f"Instagram upload error: {e}")
        return None


def post_video_simple(
    video_path: str,
    access_token: str,
    caption: str = "",
) -> Optional[str]:
    return post_video(video_path, access_token, caption)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Upload video to Instagram")
    parser.add_argument("video_path", help="Path to the video file")
    parser.add_argument("access_token", help="Instagram access token")
    parser.add_argument("caption", help="Video caption", default="")
    args = parser.parse_args()

    media_id = post_video(args.video_path, args.access_token, args.caption)
    if media_id:
        print(f"Uploaded successfully. Media ID: {media_id}")
    else:
        print("Upload failed")
