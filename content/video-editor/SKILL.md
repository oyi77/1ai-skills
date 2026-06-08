---
name: video-editor
description: Edit and enhance AI-generated videos using FFmpeg. Add captions, trim
  clips, merge videos, add audio, convert formats, and create professional video content
  for social media distribution.
persona: "name: \"Quentin Tarantino\"\n  title: \"Master of Cinematic Editing\"\n\
  \  expertise: [\"non-linear narrative\", \"rhythm and pacing\", \"visual composition\"\
  , \"tension building\"]\n  philosophy: \"I steal from every single movie ever made.\
  \ If people don't like that, then tough till, 'cause I steal from the best.\"\n\
  \  credentials:\n    - \"Two-time Academy Award winner (Pulp Fiction, Django Unchained)\"\
  \n    - \"Palme d'Or winner at Cannes Film Festival for Pulp Fiction\"\n    - \"\
  Revolutionized independent cinema with Reservoir Dogs\"\n    - \"Created iconic\
  \ visual language blending violence, humor, and pop culture\"\n  principles:\n \
  \   - \"Every cut matters - edit for rhythm, not just continuity\"\n    - \"Music\
  \ drives emotion - soundtrack shapes the viewer's experience\"\n    - \"Non-linear\
  \ storytelling creates mystery - play with time structure\"\n    - \"Close-ups reveal\
  \ truth - get intimate with character emotion\"\n    - \"Pacing builds tension -\
  \ know when to slow down, when to accelerate\"\n    - \"Visual composition is narrative\
  \ - every frame tells story\"\n    - \"Homage is creation - reference what you love,\
  \ make it yours\"\n"
domain: content
---


# Video Editor Skill

## Overview

Post-production video editing using FFmpeg automation. Enhance videos from `google-flow` and `grok-video-generation` with captions, audio, transitions, and format optimization for different platforms.

## When to Use

- Add captions/subtitles to videos
- Trim or cut video clips
- Merge multiple videos
- Add background music
- Convert video formats
- Optimize for platform specs
- Create video thumbnails
- Batch process videos

## FFmpeg Commands

- Configure audio, captions, clips, content, convert settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### 1. Add Captions/Subtitles
```bash
# Generate SRT file
cat > captions.srt << EOF
1
00:00:00,000 --> 00:00:03,000
Welcome to AI Video Tutorial

2
00:00:03,000 --> 00:00:06,000
Learn how to create amazing content
EOF

# Burn subtitles into video
ffmpeg -i input.mp4 -vf subtitles=captions.srt output.mp4
```

### 2. Trim Video
```bash
# Trim from 5s to 15s
ffmpeg -i input.mp4 -ss 00:00:05 -to 00:00:15 -c copy trimmed.mp4
```

### 3. Merge Videos
```bash
# Create file list
cat > filelist.txt << EOF
file 'video1.mp4'
file 'video2.mp4'
file 'video3.mp4'
EOF

# Concatenate
ffmpeg -f concat -safe 0 -i filelist.txt -c copy merged.mp4
```

### 4. Add Audio/Music
```bash
# Add background music
ffmpeg -i video.mp4 -i music.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest output.mp4

# Adjust audio volume
ffmpeg -i input.mp4 -af "volume=0.5" output.mp4
```

### 5. Convert Format
```bash
# MP4 to WebM
ffmpeg -i input.mp4 -c:v libvpx-vp9 -c:a libopus output.webm

# Optimize for Instagram (1080x1920, 9:16)
ffmpeg -i input.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" instagram.mp4

# Optimize for TikTok
ffmpeg -i input.mp4 -vf "scale=1080:1920" -c:v libx264 -preset slow -crf 22 tiktok.mp4
```

### 6. Create Thumbnail
```bash
# Extract frame at 3 seconds
ffmpeg -i video.mp4 -ss 00:00:03 -vframes 1 thumbnail.jpg
```

### 7. Add Watermark
```bash
# Add logo watermark
ffmpeg -i video.mp4 -i logo.png -filter_complex "overlay=W-w-10:H-h-10" watermarked.mp4
```

## Automation Examples

- Configure audio, captions, clips, content, convert settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Auto-Caption Generator
```javascript
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

async function addCaptions(videoPath, captionText) {
  // Generate SRT file
  const srtContent = generateSRT(captionText);
  await fs.writeFile('captions.srt', srtContent);
  
  // Add to video
  await execPromise(
    `ffmpeg -i ${videoPath} -vf subtitles=captions.srt output.mp4`
  );
  
  return 'output.mp4';
}

function generateSRT(text) {
  // Simple SRT generation
  return `1\n00:00:00,000 --> 00:00:05,000\n${text}\n`;
}
```

### Batch Processing
```javascript
async function batchOptimizeForPlatforms(videoPath) {
  const platforms = {
    instagram: '-vf "scale=1080:1920" -c:v libx264',
    tiktok: '-vf "scale=1080:1920" -c:v libx264 -preset slow',
    youtube: '-vf "scale=1920:1080" -c:v libx264',
    x: '-vf "scale=1280:720" -c:v libx264'
  };
  
  for (const [platform, params] of Object.entries(platforms)) {
    await execPromise(
      `ffmpeg -i ${videoPath} ${params} ${platform}.mp4`
    );
  }
}
```

## Platform Specifications

| Platform | Resolution | Aspect Ratio | Max Length | Format |
|----------|-----------|--------------|------------|--------|
| Instagram Feed | 1080x1080 | 1:1 | 60s | MP4 |
| Instagram Reels | 1080x1920 | 9:16 | 90s | MP4 |
| TikTok | 1080x1920 | 9:16 | 10min | MP4 |
| X | 1280x720 | 16:9 | 2:20 | MP4 |
| LinkedIn | 1920x1080 | 16:9 | 10min | MP4 |
| YouTube | 1920x1080 | 16:9 | Unlimited | MP4 |

---

**Related Skills**: `productivity/google-flow`, `content/grok-video-generation`, `marketing/social-media-upload`

## When NOT to Use

- When the content requires original research or primary source reporting
- When the output will be used in legally binding or regulatory contexts
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Content quality is not reviewed before publication or distribution
- Agent does not adapt tone and style for the target audience
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Content quality passes review before publication or distribution
- [ ] Tone and style are appropriate for the target audience
- [ ] All required outputs generated
- [ ] Success criteria met

