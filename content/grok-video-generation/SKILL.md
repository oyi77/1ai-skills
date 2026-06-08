---
name: grok-video-generation
description: Generate AI videos using Grok Imagine powered by Aurora AI. Create short
  videos from text prompts or animate still images with synchronized audio. Requires
  Super Grok subscription.
persona: "|\n  name: \"Steven Spielberg\"\n    title: \"Master of Cinematic Wonder\"\
  \n    expertise: [\"emotional storytelling\", \"visual spectacle\", \"audience empathy\"\
  , \"blockbuster pacing\"]\n    philosophy: \"The delicate balance of mentoring someone\
  \ is not creating them in your own image, but giving them the opportunity to create\
  \ themselves.\"\n    credentials:\n      - \"Three-time Academy Award winner (Schindler's\
  \ List, Saving Private Ryan)\"\n      - \"Directed Jaws, E.T., Jurassic Park, Indiana\
  \ Jones franchise\"\n      - \"Highest-grossing director of all time with $10+ billion\
  \ box office\"\n      - \"Co-founded DreamWorks Studios, revolutionized blockbuster\
  \ filmmaking\"\n    principles:\n      - \"Emotion first - make the audience feel\
  \ before they think\"\n      - \"Show wonder - capture the awe in characters' faces,\
  \ let audience mirror it\"\n      - \"Pacing builds tension - know when to slow\
  \ down, when to accelerate\"\n      - \"Visual storytelling - let images carry narrative\
  \ weight\"\n      - \"Empathy is universal - find the human story in every spectacle\"\
  \n      - \"Technical mastery serves story - effects enhance, never replace emotion\"\
  \n      - \"Casting is 80% of directing - right actor makes everything easier\"\n"
domain: content
---



# Grok Video Generation Skill

## Overview

Grok Imagine is X.AI's video generation feature powered by the proprietary Aurora AI engine. Create cinematic short videos (6-10 seconds) from text prompts or animate still images, complete with synchronized audio including speech, sound effects, and ambient sound.

**Access**: Grok mobile app (iOS/Android)  
**Model**: Aurora AI (autoregressive mixture-of-experts)  
**Launch**: October 2025 (initially for Super Grok subscribers)  
**Video Length**: 6-10 seconds  
**Key Feature**: Synchronized audio generation

## When to Use

- Generate short video clips from text descriptions
- Animate still images into dynamic videos
- Create viral-ready content for X (Twitter) platform
- Produce videos with synchronized audio (speech, SFX, ambient)
- Quick video prototyping and concept visualization
- Social media content creation
- Marketing and advertising short-form videos

## When NOT to Use

- Long-form videos (>10 seconds) - use `productivity/google-flow` for stitching
- Videos requiring precise editing control
- When you don't have Super Grok subscription
- Professional production-quality videos requiring manual editing

---

## Prerequisites

- Python 3.10+ or Node.js 18+
- API credentials configured in `.env`
- Network access to target services
- Understanding of animate, audio, aurora, create, from concepts


### Required Access

1. **Super Grok Subscription** (paid tier)
   - Video generation requires Super Grok
   - Image generation available with X Premium
   - Early access via waitlist

2. **Grok Mobile App**
   - Download from App Store (iOS) or Google Play (Android)
   - Ensure latest version installed
   - Login with X account

3. **Active X Account**
   - Required for authentication
   - Integration with X platform for sharing

---

## Complete Video Generation Workflow

Step-by-step grok-video-generation execution process.

**Step 1: Configure** — Set up targets and parameters in config file.

**Step 2: Execute** — Run the grok-video-generation workflow with configured inputs.

**Step 3: Review** — Analyze outputs and iterate on configuration.

**Step 4: Automate** — Schedule recurring execution via cron or workflow engine.


### Step 1: Configure
Set up targets and parameters in config file.

### Step 2: Execute
Run the grok-video-generation workflow with configured inputs.

### Step 3: Review
Analyze outputs and iterate on configuration.

### Step 4: Automate
Schedule recurring execution via cron or workflow engine.


### Method 1: Text-to-Video

**Step 1: Open Grok App**
```
1. Launch Grok mobile app
2. Login with X account credentials
3. Navigate to main interface
```

**Step 2: Access Imagine Feature**
```
1. Look for "Imagine" button/icon
2. Tap to open video generation interface
3. Select "Video" mode (if not default)
```

**Step 3: Enter Text Prompt**
```
1. Tap the prompt input field
2. Type detailed description of desired video
3. Include specifics:
   - Scene description
   - Subject/characters
   - Camera angles/movement
   - Visual style
   - Motion/action
   - Audio elements (optional)
```

**Example Prompts**:
```
"A golden retriever running through a sunlit meadow, slow motion, cinematic"

"Close-up of ocean waves crashing on rocks at sunset, dramatic lighting, ambient ocean sounds"

"Time-lapse of a flower blooming, macro photography, soft background music"

"Aerial view of a winding mountain road with a red car driving, sweeping camera movement"

"Neon-lit cyberpunk city street at night, rain falling, futuristic atmosphere"
```

**Step 4: Select Generation Mode**

Choose from available modes:

| Mode | Description | Best For |
|------|-------------|----------|
| **Normal** | Balanced, realistic content | General purpose, professional content |
| **Fun** | Creative, dynamic, playful | Social media, entertainment |
| **Custom** | Precise adjustments, fine control | Specific requirements, brand content |
| **Spicy** | Provocative content (may have limitations) | Edgy content (use responsibly) |

**Step 5: Generate Video**
```
1. Review prompt and settings
2. Tap "Generate" button
3. Wait for processing (typically seconds)
4. Aurora AI creates video variations
```

**Step 6: Review and Select**
```
1. View generated video options
2. Play each variation
3. Check video quality, motion, audio sync
4. Select preferred version
```

**Step 7: Download or Share**
```
1. Tap download icon to save locally
2. Or tap share icon for X integration
3. Video saved to device gallery
4. Ready for use in other apps
```

---

### Method 2: Image-to-Video

**Step 1: Prepare Source Image**
```
- Use high-quality still image
- Clear subject/composition
- Good lighting and resolution
- Supported formats: JPG, PNG
```

**Step 2: Access Imagine Feature**
```
1. Open Grok app
2. Tap "Imagine" button
3. Select "Image-to-Video" mode
```

**Step 3: Upload Image**
```
1. Tap upload/camera icon
2. Select image from gallery
3. Or capture new photo
4. Confirm image selection
```

**Step 4: Add Animation Prompt (Optional)**
```
1. Describe desired motion/animation
2. Example: "Gentle camera zoom in"
3. Example: "Subject turns head slowly"
4. Example: "Background elements move subtly"
```

**Step 5: Generate Animated Video**
```
1. Tap "Generate" button
2. Aurora AI analyzes image
3. Creates animated video
4. Adds synchronized audio if applicable
```

**Step 6: Download Result**
```
1. Review animated video
2. Download to device
3. Share to X or other platforms
```

---

## Prompt Engineering Best Practices

- Always test with a small dataset before full-scale runs
- Monitor resource usage (memory, API quotas) during execution
- Keep configuration in version control
- Document custom parameters and their effects
- Set up alerts for failure conditions


### Effective Prompt Structure

```
[Subject] + [Action] + [Setting] + [Camera Work] + [Style] + [Audio]
```

**Example Breakdown**:
```
Subject: "A majestic eagle"
Action: "soaring through the sky"
Setting: "above snow-capped mountains at dawn"
Camera Work: "tracking shot, smooth movement"
Style: "cinematic, epic, high contrast"
Audio: "wind sounds, ambient nature"

Full Prompt: "A majestic eagle soaring through the sky above snow-capped mountains at dawn, tracking shot with smooth camera movement, cinematic epic style with high contrast, wind sounds and ambient nature audio"
```

### Prompt Tips

1. **Be Specific**
   - ❌ "A car driving"
   - ✅ "A red sports car driving on a coastal highway at sunset, aerial view"

2. **Include Motion Details**
   - Describe movement: "slow motion", "fast-paced", "gentle drift"
   - Camera movement: "pan left", "zoom in", "tracking shot", "static"

3. **Specify Visual Style**
   - Lighting: "golden hour", "dramatic shadows", "soft diffused light"
   - Mood: "cinematic", "dreamy", "energetic", "serene"
   - Color: "vibrant colors", "muted tones", "black and white"

4. **Audio Guidance**
   - Speech: "narrator voice", "dialogue"
   - Sound effects: "footsteps", "wind", "water flowing"
   - Music: "upbeat background music", "ambient soundscape"

5. **Technical Specs**
   - Quality: "high quality", "4K", "photorealistic"
   - Frame rate: "smooth motion", "cinematic 24fps feel"

### Prompt Examples by Category

**Nature/Landscape**:
```
"Waterfall cascading into a crystal-clear pool, surrounded by lush tropical vegetation, slow motion, morning mist, ambient water sounds"

"Northern lights dancing across the Arctic sky, time-lapse, vibrant greens and purples, serene atmosphere"
```

**Product/Commercial**:
```
"Luxury watch rotating on a pedestal, studio lighting with dramatic shadows, close-up macro shot, elegant presentation"

"Smartphone floating in mid-air with holographic interface elements appearing, futuristic tech aesthetic, clean white background"
```

**Action/Dynamic**:
```
"Skateboarder performing a kickflip in slow motion, urban skate park setting, golden hour lighting, energetic vibe"

"Formula 1 car speeding around a racetrack corner, low angle tracking shot, motion blur on background, engine roar audio"
```

**Abstract/Artistic**:
```
"Colorful paint droplets falling into water, creating mesmerizing patterns, macro photography, slow motion, vibrant colors"

"Geometric shapes morphing and transforming, neon colors, dark background, electronic music ambience"
```

---

## Key Features & Capabilities

- Configure animate, audio, aurora, create, from settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### 1. Synchronized Audio Generation

**Unique Advantage**: Unlike many AI video tools, Grok Imagine generates synchronized audio automatically.

**Audio Types**:
- **Speech**: Dialogue, narration, voiceovers
- **Sound Effects**: Footsteps, ambient noise, object interactions
- **Music**: Background music, atmospheric soundscapes
- **Environmental**: Wind, water, traffic, nature sounds

**Audio Control**:
```
Prompt: "...with upbeat background music"
Prompt: "...ambient forest sounds only"
Prompt: "...narrator explaining the scene"
Prompt: "...no audio, silent video"
```

### 2. Realistic Physics & Motion

**Aurora AI Capabilities**:
- Movie-quality physics simulations
- Realistic object interactions
- Natural movement synthesis
- Environmental effects (wind, water, gravity)
- Accurate lighting and shadows

**Motion Examples**:
- Cloth/fabric movement
- Liquid dynamics (water, paint)
- Particle effects (smoke, dust)
- Character animation
- Vehicle physics

### 3. Fast Generation Speed

**Performance**:
- Generation time: Seconds (not minutes)
- Real-time or near-real-time processing
- Multiple variations simultaneously
- Efficient Aurora engine

### 4. Multi-Style Generation

**Style Options**:
- Photorealistic
- Cinematic
- Animated/cartoon
- Artistic/painterly
- Documentary
- Sci-fi/futuristic
- Vintage/retro

### 5. X Platform Integration

**Seamless Sharing**:
- Direct post to X (Twitter)
- Optimized for social media
- Viral content creation
- Easy distribution

---

## Creating Longer Videos

- Configure animate, audio, aurora, create, from settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Limitation
Grok Imagine generates 6-10 second clips. For longer videos, use stitching techniques.

### Method: Video Stitching with FFmpeg

**Step 1: Generate Multiple Clips**
```
1. Create sequence of related prompts
2. Generate each clip separately
3. Download all clips to device
4. Transfer to computer for stitching
```

**Example Sequence**:
```
Clip 1: "Opening shot: Aerial view of a beach at sunrise"
Clip 2: "Medium shot: Waves rolling onto the shore"
Clip 3: "Close-up: Seashell on the sand with foam approaching"
Clip 4: "Wide shot: Seagulls flying over the ocean"
Clip 5: "Final shot: Sun fully risen, beach panorama"
```

**Step 2: Stitch with FFmpeg**
```bash
# Create file list
cat > filelist.txt << EOF
file 'grok-clip-1.mp4'
file 'grok-clip-2.mp4'
file 'grok-clip-3.mp4'
file 'grok-clip-4.mp4'
file 'grok-clip-5.mp4'
EOF

# Concatenate videos
ffmpeg -f concat -safe 0 -i filelist.txt -c copy beach-sequence.mp4

# Result: ~30-50 second video (5 clips × 6-10s each)
```

**Step 3: Add Transitions (Optional)**
```bash
# Add crossfade transitions between clips
ffmpeg -i grok-clip-1.mp4 -i grok-clip-2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=5.5[v]" \
  -map "[v]" output.mp4
```

---

## Integration with Other Skills

- Configure animate, audio, aurora, create, from settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Send via Telegram
```javascript
// Generate video with Grok → Download → Send
async function grokToTelegram(prompt, chatId) {
  // 1. Generate video in Grok app (manual)
  // 2. Download to device
  // 3. Transfer to computer
  // 4. Send via Telegram skill
  
  const videoPath = '/path/to/downloaded/grok-video.mp4';
  // await sendTelegramVideo(chatId, videoPath);
}
```

### Combine with Google Flow
```
Strategy: Use both tools for different purposes
- Grok: Quick 6-10s clips with audio
- Google Flow: Longer narrative videos
- Stitch together for comprehensive content
```

### Social Media Workflow
```
1. Generate video with Grok Imagine
2. Download to device
3. Edit/enhance if needed
4. Post to X directly (native integration)
5. Cross-post to other platforms
```

---

## Comparison with Other Tools

| Feature | Grok Imagine | Google Flow | Sora (OpenAI) |
|---------|--------------|-------------|---------------|
| **Video Length** | 6-10 seconds | ~5-10 seconds | Up to 60 seconds |
| **Audio** | ✅ Synchronized | ❌ No audio | ❌ No audio |
| **Access** | Mobile app | Web browser | Limited access |
| **Cost** | Super Grok subscription | Credits (20/video) | Waitlist/expensive |
| **Speed** | Seconds | 60-90 seconds | Minutes |
| **Platform** | X integration | Standalone | Standalone |
| **Image-to-Video** | ✅ Yes | ❌ No (separate mode) | ✅ Yes |

**When to Use Grok**:
- Need synchronized audio
- Quick generation required
- X platform content
- Mobile-first workflow
- Short viral clips

**When to Use Google Flow**:
- Web-based workflow preferred
- More control over prompts
- Integration with Google ecosystem
- Longer video via stitching

---

## Troubleshooting

- Configure animate, audio, aurora, create, from settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Common Issues

**Issue**: "Super Grok subscription required"
- **Cause**: Video generation needs paid tier
- **Solution**: Upgrade to Super Grok subscription

**Issue**: Video generation fails
- **Cause**: Prompt too vague or complex
- **Solution**: Simplify prompt, be more specific

**Issue**: Poor video quality
- **Cause**: Unclear prompt or low-quality source image
- **Solution**: Refine prompt with more details, use high-res images

**Issue**: Audio not synchronized
- **Cause**: Complex audio requirements
- **Solution**: Simplify audio description in prompt

**Issue**: Generation takes too long
- **Cause**: Server load or network issues
- **Solution**: Wait and retry, check internet connection

**Issue**: Cannot download video
- **Cause**: Storage permission or space issues
- **Solution**: Grant app permissions, free up device storage

**Issue**: Video doesn't match prompt
- **Cause**: Aurora AI interpretation differs
- **Solution**: Regenerate with more explicit prompt

---

## Best Practices

- Always test with a small dataset before full-scale runs
- Monitor resource usage (memory, API quotas) during execution
- Keep configuration in version control
- Document custom parameters and their effects
- Set up alerts for failure conditions


### 1. Prompt Optimization
- Start simple, add details iteratively
- Test different phrasings
- Use reference styles ("like a movie trailer", "documentary style")
- Specify what you DON'T want if needed

### 2. Quality Control
- Generate multiple variations
- Review all options before selecting
- Check audio sync carefully
- Verify motion is smooth

### 3. Workflow Efficiency
- Save successful prompts for reuse
- Build a prompt library by category
- Batch similar content generation
- Plan sequences before generating

### 4. Content Strategy
- Optimize for X platform (short, engaging)
- Consider viral potential
- Use trending topics/styles
- Test different generation modes

### 5. Resource Management
- Monitor subscription usage
- Download important videos immediately
- Organize saved videos by project
- Delete unused generations

---

## Use Cases

- Configure animate, audio, aurora, create, from settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Marketing & Advertising
```
- Product demos (6-10s)
- Brand storytelling clips
- Social media ads
- Teaser videos
- Announcement clips
```

### Content Creation
```
- B-roll footage
- Transition clips
- Background videos
- Intro/outro sequences
- Visual effects
```

### Education
```
- Concept visualization
- Quick explainers
- Demonstration clips
- Attention-grabbing intros
```

### Entertainment
```
- Memes and viral content
- Music video snippets
- Comedy sketches
- Artistic projects
```

---

## Future Developments

**Expected Enhancements** (post-October 2025):
- Longer video generation (>10 seconds)
- More generation modes
- Enhanced audio control
- Better image-to-video quality
- Web interface option
- API access for developers
- Advanced editing features

---


## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Video output does not meet platform specifications for resolution or format
- Agent skips quality review before final render
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Output meets target platform specifications for resolution and format
- [ ] Quality review is completed before final render
- [ ] All required outputs generated
- [ ] Success criteria met

## Related Skills

- `productivity/google-flow` - Alternative video generation (Google Veo)
- `content/gemini-image-generator` - Static image generation
- `marketing/content-creator` - Content strategy and planning
- `marketing/ads-manager` - Advertising campaign integration
- **FFmpeg** - Video stitching and editing
- **Telegram Integration** - Video distribution

---

## URL & Resources

| Resource | Link |
|----------|------|
| Grok App (iOS) | App Store search "Grok" |
| Grok App (Android) | Google Play search "Grok" |
| X.AI Website | https://x.ai |
| X Platform | https://x.com |
| Super Grok Info | Check X.AI website for pricing |

---

**Last Updated**: 2026-02-17  
**Status**: ⏳ Launching October 2025  
**Access**: Super Grok subscription required  
**Model**: Aurora AI (autoregressive mixture-of-experts)  
**Key Feature**: Synchronized audio generation
