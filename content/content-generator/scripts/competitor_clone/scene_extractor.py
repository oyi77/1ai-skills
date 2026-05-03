"""
Scene Extractor — Detect & extract scenes from competitor video
Uses FFmpeg scene detection to find natural cut points
"""

import os, subprocess, json, shutil
from pathlib import Path

FFMPEG = "/home/linuxbrew/.linuxbrew/bin/ffmpeg"
FFPROBE = "/home/linuxbrew/.linuxbrew/bin/ffprobe"


def get_video_info(video_path: str) -> dict:
    """Get video duration, fps, resolution"""
    cmd = [
        FFPROBE, "-v", "quiet", "-print_format", "json",
        "-show_streams", "-show_format", video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    
    video_stream = next((s for s in data["streams"] if s["codec_type"] == "video"), {})
    duration = float(data["format"].get("duration", 0))
    fps_str = video_stream.get("r_frame_rate", "30/1")
    fps_num, fps_den = fps_str.split("/")
    fps = float(fps_num) / float(fps_den)
    
    return {
        "duration": duration,
        "fps": fps,
        "width": video_stream.get("width", 1080),
        "height": video_stream.get("height", 1920),
        "has_audio": any(s["codec_type"] == "audio" for s in data["streams"])
    }


def extract_scenes(video_path: str, output_dir: str, threshold: float = 0.3) -> list:
    """
    Detect scene changes and extract keyframe per scene.
    Returns list of scene dicts with timestamp + frame path.
    """
    os.makedirs(output_dir, exist_ok=True)
    frames_dir = os.path.join(output_dir, "keyframes")
    os.makedirs(frames_dir, exist_ok=True)

    info = get_video_info(video_path)
    duration = info["duration"]
    print(f"  📹 Video: {duration:.1f}s, {info['width']}x{info['height']}, {info['fps']:.1f}fps")

    # Step 1: Detect scene timestamps using FFmpeg scene filter
    print("  🔍 Detecting scene boundaries...")
    scene_cmd = [
        FFMPEG, "-i", video_path,
        "-vf", f"select='gt(scene,{threshold})',showinfo",
        "-vsync", "vfr",
        "-f", "null", "-"
    ]
    result = subprocess.run(scene_cmd, capture_output=True, text=True)
    
    # Parse timestamps from stderr
    scene_times = [0.0]  # Always start with 0
    for line in result.stderr.split("\n"):
        if "pts_time:" in line and "showinfo" in line:
            try:
                pts = float(line.split("pts_time:")[1].split()[0])
                if pts > 0.5:  # Ignore tiny scenes
                    scene_times.append(round(pts, 2))
            except:
                pass

    # If very few scenes detected, add manual splits every N seconds
    if len(scene_times) < 3:
        print(f"  ⚠️ Only {len(scene_times)} scenes detected. Adding time-based splits...")
        interval = min(5.0, duration / 4)
        t = interval
        while t < duration - 1:
            if not any(abs(t - st) < 1.0 for st in scene_times):
                scene_times.append(round(t, 2))
            t += interval

    scene_times = sorted(set(scene_times))
    scene_times.append(duration)  # Add end
    print(f"  ✅ Found {len(scene_times)-1} scenes")

    # Step 2: Extract keyframe image per scene + clip per scene
    scenes = []
    for i, start in enumerate(scene_times[:-1]):
        end = scene_times[i + 1]
        scene_dur = round(end - start, 2)
        if scene_dur < 0.5:
            continue

        mid = start + scene_dur / 2  # Middle of scene for keyframe

        # Extract keyframe image
        frame_path = os.path.join(frames_dir, f"scene_{i+1:02d}.jpg")
        frame_cmd = [
            FFMPEG, "-y", "-ss", str(mid), "-i", video_path,
            "-vframes", "1", "-q:v", "2",
            "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black",
            frame_path
        ]
        subprocess.run(frame_cmd, capture_output=True)

        # Extract scene clip
        clip_path = os.path.join(output_dir, f"scene_{i+1:02d}_original.mp4")
        clip_cmd = [
            FFMPEG, "-y", "-ss", str(start), "-i", video_path,
            "-t", str(scene_dur), "-c", "copy", clip_path
        ]
        subprocess.run(clip_cmd, capture_output=True)

        scenes.append({
            "id": i + 1,
            "start": start,
            "end": end,
            "duration": scene_dur,
            "keyframe": frame_path,
            "clip": clip_path,
            "analysis": None,  # To be filled by analyzer
        })
        print(f"    Scene {i+1}: {start:.1f}s → {end:.1f}s ({scene_dur:.1f}s) ✅")

    # Save scene manifest
    manifest = os.path.join(output_dir, "scenes.json")
    with open(manifest, "w") as f:
        json.dump({"video": video_path, "info": info, "scenes": scenes}, f, indent=2)

    return scenes


def extract_audio(video_path: str, output_dir: str) -> str:
    """Extract audio track from competitor video"""
    audio_path = os.path.join(output_dir, "competitor_audio.mp3")
    cmd = [
        FFMPEG, "-y", "-i", video_path,
        "-vn", "-acodec", "mp3", "-ar", "16000", "-ac", "1",
        audio_path
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode == 0 and os.path.exists(audio_path):
        print(f"  ✅ Audio extracted: {audio_path}")
        return audio_path
    return None


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        video = sys.argv[1]
        out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/scenes_test"
        scenes = extract_scenes(video, out)
        print(f"\nExtracted {len(scenes)} scenes")
