---
name: content-factory
description: Use when building all-in-one YouTube content — full videos from prompts, vertical Shorts from text, or clipping long videos into Shorts. Uses free tools (ffmpeg, edge-tts, Pexels).
domain: content
author: oyi77
license: Apache-2.0
subdomain: content-creation
tags:
- youtube
- shorts
- video
- content-creation
- edge-tts
- ffmpeg
- pexels
- stock
version: 1.0.0
category: content
---

# Content Factory

All-in-one YouTube content generator using 100% free tools: `ffmpeg`, `edge-tts`, and Pexels stock. Three modes:

1. **Regular Video** — full YouTube videos from a text prompt
2. **Shorts from Scratch** — vertical (9:16) Shorts from text
3. **Shorts from Long** — clip long videos into Shorts

## When to Use

**Trigger phrases:**
- "content factory" · "make a YouTube video" · "make a Short"
- "video from script" · "vertical video from text"
- "clip this long video into Shorts"

**Use cases:**
- Faceless YouTube channels (news recap, listicles, explainers)
- Repurposing long streams/podcasts into Shorts
- Batch content for a content calendar

## When NOT to Use

- Talking-head or screen-recording — use `hyperframes-talking-head-recut`
- Legal / medical / financial content — human review required
- Live streams — use `hyperframes-general-video`
- When Pexels doesn't have your subject — switch to `image-gen` / `geminigen-ai` for custom visuals

## Setup

```bash
# Tools
sudo apt install -y ffmpeg python3-pip jq
pip install edge-tts requests

# Env
export PEXELS_API_KEY="..."       # free from https://www.pexels.com/api/

# Verify
ffmpeg -version | head -1 && edge-tts --list-voices | head -3 && echo "setup ok"
```

## Workflow

### Shared Pipeline

Every mode shares the same stages. Only the asset source differs.

```
script → TTS audio → visuals → concat → captions → export → verify
```

### 1. Write the script (one beat per scene)

Keep it tight. For 60 s of narration at ~150 wpm, target **~150 words**.

```bash
cat > script.txt <<'EOF'
Why do cats always sit in boxes?
It's about safety — an enclosed space cuts their visual field.
That means fewer threats to track, less mental load.
Predators can't sneak up from behind.
And boxes are warm — cats lose heat fast at rest.
So a box isn't just cute. It's a survival tool.
EOF
```

### 2. Generate narration with edge-tts

```bash
edge-tts --voice en-US-GuyNeural --text "$(cat script.txt)" --write-media narration.mp3
# Get word-level timestamps for captions
edge-tts --voice en-US-GuyNeural --text "$(cat script.txt)" --write-subtitles narration.vtt
```

Voice options: `en-US-GuyNeural`, `en-US-JennyNeural`, `en-GB-RyanNeural`, `id-ID-ArdiNeural`. List all with `edge-tts --list-voices`.

### 3. Fetch stock visuals per beat

```python
# fetch_pexels.py — one B-roll clip per script line
import os, requests, sys, json

KEY = os.environ["PEXELS_API_KEY"]
HEADERS = {"Authorization": KEY}

def search(query: str, orientation: str = "landscape") -> list[dict]:
    r = requests.get(
        "https://api.pexels.com/videos/search",
        headers=HEADERS,
        params={"query": query, "orientation": orientation, "per_page": 5},
    )
    r.raise_for_status()
    return r.json()["videos"]

def best_file(video: dict) -> str:
    # Highest-resolution SD file (cheaper download, good enough for 1080p export)
    files = [f for f in video["video_files"] if f["quality"] == "sd"]
    files.sort(key=lambda f: f["width"], reverse=True)
    return files[0]["link"]

if __name__ == "__main__":
    queries = [q.strip() for q in open(sys.argv[1]) if q.strip()]
    out = []
    for i, q in enumerate(queries):
        vids = search(q, "landscape")
        if not vids:
            print(f"[warn] no results for {q!r}", file=sys.stderr)
            continue
        url = best_file(vids[0])
        out.append(url)
        print(f"[fetch] {q} → {url}")
    json.dump(out, open("broll.json", "w"), indent=2)
```

For Shorts mode pass `orientation="portrait"`.

### 4. Concatenate visuals + narration

```bash
# Download B-roll
while read url; do
  i=$((i+1))
  curl -sSL "$url" -o "broll_$(printf %03d $i).mp4"
done < <(jq -r '.[]' broll.json)

# Normalize every clip to 1920x1080, 30 fps, and trim to a fixed slice
mkdir -p normalized
for f in broll_*.mp4; do
  ffmpeg -y -loglevel error -i "$f" \
    -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30" \
    -an -c:v libx264 -crf 20 -pix_fmt yuv420p "normalized/$f"
done

# Concat with the concat demuxer (requires identical codecs/resolution)
ls normalized/*.mp4 | sed "s/^/file '/;s/$/'/" > list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i list.txt -c copy broll_concat.mp4

# Mix in narration; trim/pad visuals to match narration length
DUR=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 narration.mp3)
ffmpeg -y -loglevel error -i broll_concat.mp4 -i narration.mp3 \
  -map 0:v -map 1:a -t "$DUR" \
  -c:v libx264 -crf 20 -c:a aac -b:a 192k \
  out_nocaptions.mp4
```

### 5. Burn in captions

```bash
# Convert VTT → ASS for styling, or use subtitles filter directly
ffmpeg -y -loglevel error -i out_nocaptions.mp4 \
  -vf "subtitles=narration.vtt:force_style='FontName=Arial Bold,FontSize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,MarginV=40'" \
  -c:v libx264 -crf 20 -c:a copy \
  out_final.mp4
```

### 6. Verify every output

```bash
ffprobe -v error -show_entries stream=codec_name,width,height,duration -of compact out_final.mp4
ffmpeg -nostats -i out_final.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2
```

Expect: video `1920x1080` (regular) or `1080x1920` (Shorts), H.264 + AAC, loudness **−14 LUFS ± 1**, peak ≤ −1.5 dBFS.

## Mode: Shorts from Scratch

Same pipeline with two differences:
- Visuals from Pexels use `orientation="portrait"`
- Normalize to `1080x1920`:

```bash
ffmpeg -y -loglevel error -i broll.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -an -c:v libx264 -crf 20 -pix_fmt yuv420p short_visual.mp4
```

Target duration: **≤60 s** for Shorts, ≤15 s for TikTok/Reels.

## Mode: Shorts from Long

```bash
# 1. Detect scene cuts (see auto-clipper skill for the full logic)
ffmpeg -i long.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null - 2>&1 | grep "pts_time" \
  | awk -F'pts_time:' '{print $2}' > cuts.txt

# 2. Pick the 3 highest-energy windows (manual or auto-clipper script)
# 3. Cut each into a 30–60 s vertical Short
ffmpeg -y -loglevel error -ss 120.5 -t 45 -i long.mp4 \
  -vf "crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920,fps=30" \
  -c:v libx264 -crf 20 -c:a aac -b:a 192k \
  short_001.mp4
```

The `crop=ih*9/16:ih:...` filter crops the horizontal video to a centered vertical slice. For talking-head footage where the subject is off-center, shift the x offset (3rd crop param).

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "One B-roll clip per video is fine" | Repetition kills retention. Aim for 1 clip per 3–5 s of narration. |
| "Skip verification, edge-tts is reliable" | Edge-tts rate-limits under load. Always probe the output. |
| "Auto-captions don't need styling" | Unstyled white text on white footage disappears. Use the `force_style` block. |
| "Reuse the same voice every time" | Rotate voices between videos to avoid a "same channel" feel. |
| "Pexels has everything" | It doesn't. For specific products/logos, generate with `image-gen` / `geminigen-ai`. |

## Verification

- [ ] `script.txt` < 200 words per minute of target video
- [ ] Narration duration matches target (±1 s)
- [ ] Every B-roll clip normalized to the target resolution and fps
- [ ] Concat demuxer file paths valid (absolute or `-safe 0`)
- [ ] Captions styled and readable on all footage
- [ ] Output probed with `ffprobe` (codec, dimensions, duration)
- [ ] Loudness normalized to −14 LUFS ± 1
- [ ] Contact sheet from final MP4 reviewed (sample every ~2 s)
