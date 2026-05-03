"""
BGM Manager — Auto background music for generated videos
Matches music mood to content style/category
Sources: Pixabay Audio API (free, no key needed for basic)
"""

import os, json, subprocess, urllib.request, urllib.parse
import urllib.error

FFMPEG  = "/home/linuxbrew/.linuxbrew/bin/ffmpeg"
BGM_DIR = "/home/openclaw/.openclaw/workspace/output/bgm_library"
os.makedirs(BGM_DIR, exist_ok=True)

# Mood mapping: category+style → music mood keyword
MOOD_MAP = {
    ("minuman", "dark_moody"):   "cinematic dramatic",
    ("minuman", "clean_white"):  "upbeat fresh",
    ("minuman", "luxury"):       "elegant luxury piano",
    ("minuman", "splash"):       "energetic upbeat",
    ("minuman", "lifestyle"):    "chill relaxed",
    ("makanan", "dark_moody"):   "cinematic dramatic",
    ("makanan", "clean_white"):  "light positive",
    ("makanan", "lifestyle"):    "acoustic warm",
    ("beauty",  "dark_moody"):   "elegant dark",
    ("beauty",  "luxury"):       "luxury soft piano",
    ("beauty",  "lifestyle"):    "soft positive",
    ("elektronik", "dark_moody"):"futuristic tech",
    ("elektronik", "clean_white"):"modern minimal",
    ("fashion", "dark_moody"):   "cinematic fashion",
    ("fashion", "lifestyle"):    "trendy upbeat",
    ("suplemen", "dark_moody"):  "powerful motivational",
    ("suplemen", "lifestyle"):   "motivational energetic",
}

DEFAULT_MOODS = {
    "dark_moody":   "cinematic dramatic",
    "clean_white":  "light upbeat",
    "luxury":       "elegant luxury",
    "splash":       "energetic",
    "lifestyle":    "chill positive",
}

# Pixabay audio search
PIXABAY_API = "https://pixabay.com/api/videos/music/"


def get_mood(category: str, style: str) -> str:
    return MOOD_MAP.get((category, style)) or DEFAULT_MOODS.get(style, "cinematic")


def download_bgm(mood: str, duration: int = 60) -> str:
    """Download a royalty-free BGM track matching the mood"""
    # Check cache first
    cache_key = mood.replace(" ", "_")
    cached = os.path.join(BGM_DIR, f"{cache_key}.mp3")
    if os.path.exists(cached):
        print(f"  🎵 BGM from cache: {cache_key}")
        return cached

    print(f"  🎵 Searching BGM for: '{mood}'...")

    # Try Pixabay audio API (no key needed for basic)
    try:
        query = urllib.parse.quote(mood)
        url = f"https://pixabay.com/api/?key=47852694-a2e9a9e1b3f6e7c5d8a4b3f2e&q={query}&media_type=music&per_page=5"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            hits = data.get("hits", [])
            if hits:
                # Pick first result
                audio_url = hits[0].get("audio", {}).get("url") or hits[0].get("previewURL", "")
                if audio_url:
                    urllib.request.urlretrieve(audio_url, cached)
                    print(f"  ✅ BGM downloaded: {os.path.basename(cached)}")
                    return cached
    except Exception as e:
        print(f"  ⚠️ Pixabay failed: {e}")

    # Fallback: generate simple ambient tone with FFmpeg
    print(f"  🎹 Generating ambient tone as fallback...")
    return _generate_ambient_tone(mood, cached, duration)


def _generate_ambient_tone(mood: str, out_path: str, duration: int = 60) -> str:
    """Generate simple ambient audio using FFmpeg sine waves"""
    # Different tones per mood feel
    if "dramatic" in mood or "dark" in mood:
        freq, freq2 = 80, 120      # Deep, ominous
        vol = 0.08
    elif "luxury" in mood or "elegant" in mood:
        freq, freq2 = 220, 330     # Soft, warm
        vol = 0.05
    elif "energetic" in mood or "motivational" in mood:
        freq, freq2 = 440, 660     # Bright, punchy
        vol = 0.10
    elif "chill" in mood or "relaxed" in mood:
        freq, freq2 = 174, 261     # Calm, soothing
        vol = 0.06
    else:
        freq, freq2 = 261, 392     # Neutral
        vol = 0.07

    cmd = [
        FFMPEG, "-y",
        "-f", "lavfi",
        "-i", f"sine=frequency={freq}:duration={duration}",
        "-f", "lavfi",
        "-i", f"sine=frequency={freq2}:duration={duration}",
        "-filter_complex",
        f"[0:a]volume={vol}[a1];[1:a]volume={vol*0.6}[a2];[a1][a2]amix=inputs=2[out]",
        "-map", "[out]",
        "-c:a", "mp3", "-b:a", "128k",
        out_path
    ]
    subprocess.run(cmd, capture_output=True)
    print(f"  ✅ Ambient tone generated")
    return out_path


def has_audio_stream(video_path: str) -> bool:
    """Check if video has an audio stream"""
    probe_cmd = [
        "/home/linuxbrew/.linuxbrew/bin/ffprobe",
        "-v", "quiet", "-print_format", "json", "-show_streams", video_path
    ]
    result = subprocess.run(probe_cmd, capture_output=True, text=True)
    try:
        streams = json.loads(result.stdout).get("streams", [])
        return any(s.get("codec_type") == "audio" for s in streams)
    except:
        return False


def get_duration(video_path: str) -> float:
    probe_cmd = [
        "/home/linuxbrew/.linuxbrew/bin/ffprobe",
        "-v", "quiet", "-print_format", "json", "-show_format", video_path
    ]
    result = subprocess.run(probe_cmd, capture_output=True, text=True)
    return float(json.loads(result.stdout).get("format", {}).get("duration", 30))


def mix_bgm(video_path: str, bgm_path: str, output_path: str,
            bgm_volume: float = 0.15, fade_out: int = 3) -> str:
    """
    Mix BGM into video.
    Handles both: video WITH audio (VO) and WITHOUT audio (Seedance output).
    - If video has VO → BGM at low volume (0.15) mixed with VO
    - If video has NO audio → BGM as sole audio at higher volume (0.25)
    """
    dur = get_duration(video_path)
    has_vo = has_audio_stream(video_path)
    fade_start = max(0, dur - fade_out)

    if has_vo:
        # Mix BGM under existing VO
        audio_filter = (
            f"[1:a]volume={bgm_volume},"
            f"afade=t=out:st={fade_start}:d={fade_out}[bgm];"
            "[0:a][bgm]amix=inputs=2:duration=first:weights=1 1[aout]"
        )
        cmd = [
            FFMPEG, "-y",
            "-i", video_path,
            "-stream_loop", "-1", "-i", bgm_path,
            "-filter_complex", audio_filter,
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-t", str(dur), output_path
        ]
    else:
        # No existing audio — BGM as sole audio
        audio_filter = (
            f"[1:a]volume={bgm_volume * 1.5},"
            f"afade=t=in:st=0:d=1,"
            f"afade=t=out:st={fade_start}:d={fade_out}[aout]"
        )
        cmd = [
            FFMPEG, "-y",
            "-i", video_path,
            "-stream_loop", "-1", "-i", bgm_path,
            "-filter_complex", audio_filter,
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-t", str(dur), output_path
        ]

    result = subprocess.run(cmd, capture_output=True)
    if result.returncode == 0:
        print(f"  ✅ BGM mixed ({'with VO' if has_vo else 'no VO'}): {os.path.basename(output_path)}")
        return output_path
    else:
        print(f"  ⚠️ BGM mix failed: {result.stderr.decode()[-200:]}")
        return video_path


def add_bgm_to_video(video_path: str, category: str, style: str) -> str:
    """One-shot: detect mood → download BGM → mix → return final path"""
    mood = get_mood(category, style)
    bgm  = download_bgm(mood)
    out  = video_path.replace(".mp4", "_bgm.mp4")
    return mix_bgm(video_path, bgm, out)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        video = sys.argv[1]
        cat   = sys.argv[2] if len(sys.argv) > 2 else "minuman"
        style = sys.argv[3] if len(sys.argv) > 3 else "dark_moody"
        result = add_bgm_to_video(video, cat, style)
        print(f"Output: {result}")
