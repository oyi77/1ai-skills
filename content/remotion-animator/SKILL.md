---
name: remotion-animator
description: Remotion Animator - SKILL.md. Use when relevant to this domain.
---

# Remotion Animator - SKILL.md

> Powerful animation creation using Remotion (React-based)
> Superior to FFmpeg for dynamic, programmatic animations

---

## Overview

**What It Is:**
Remotion Animator skill for creating stunning animations programmatically using React and Remotion framework.

**Why Remotion > FFmpeg:**
- Programmatic control (code animations, not timeline drag-and-drop)
- React component system (reusable, composable)
- Precision timing (exact frames, easing, sequencing)
- Type-safe animations (TypeScript/JavaScript)
- Hot-reload during development (instant preview)
- Export to multiple formats (MP4, GIF, WebM)
- Better quality (vector rendering, crisp text)

**Best For:**
- Kinetic typography (text animations)
- Motion graphics (shapes, gradients, transitions)
- Product showcases (3D rotation, feature highlights)
- Social media templates (TikTok, Reels, YouTube Shorts)
- Data visualizations (animated charts, stats)
- Logo animations (reveal, morph, rotate)

---

## Installation

```bash
# Step 1: Install Node.js 18+ (if not already installed)
node --version  # Should be 18.0.0 or higher

# Step 2: Create Remotion project
npx create-video@latest remotion-project

# Step 3: Navigate to project
cd remotion-project

# Step 4: Copy skill files to project root
cp -r ~/.openclaw/workspace/skills/remotion-animator/* .

# Step 5: Install dependencies
npm install

# Step 6: Run preview (dev mode)
npm run dev
```

**What Gets Installed:**
- `remotion` (^4.0.0) - Core Remotion library
- `@remotion/cli` (^4.0.0) - Command-line tools
- `remotion.config.js` - Project configuration
- Skill files: templates, scripts, utilities

---

## Usage

- Configure animator, domain, relevant, remotion, skill settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Quick Start (3 Commands)

```bash
# 1. Preview animation in browser
npm run dev
# Opens: http://localhost:3000

# 2. Render to MP4
npm run build
# Creates: out/video.mp4

# 3. Render specific composition
npx remotion render <composition-name>
```

### Skill Commands

```bash
# Create animation from template
python3 create_animation.py --template kinetic_typo --text "Hello World"

# Render animation to video
python3 render_animation.py --input animation.json --output video.mp4

# Batch render multiple animations
python3 batch_render.py --config animations.json

# Preview animation in browser
python3 preview_animation.py --input animation.json

# Optimize video for file size
python3 optimize_video.py --input video.mp4 --output video_optimized.mp4
```

---

## Animation Types

- Configure animator, domain, relevant, remotion, skill settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### 1. Kinetic Typography
**Description:** Animated text with multiple fonts, sizes, transitions

**Use Cases:**
- Video intros
- Quote animations
- Headline reveals
- Social media hooks

**Templates:**
- `word-by-word` - Text appears word by word
- `scale-in` - Text scales from center
- `slide-up` - Text slides up from bottom
- `gradient-reveal` - Text with gradient fill animation
- `typewriter` - Typewriter effect

**Example:**
```json
{
  "type": "kinetic_typo",
  "text": "Viral Content Strategy",
  "animation": "scale-in",
  "duration": 3,
  "fontSize": 80,
  "fontWeight": 800,
  "colors": ["#FF6B6B", "#4ECDC4"]
}
```

---

### 2. Product Showcase
**Description:** 3D rotation, feature highlights, close-ups

**Use Cases:**
- Product reveals
- Feature demonstrations
- Comparison videos
- Before/after showcases

**Templates:**
- `3d-rotate` - 360° product rotation
- `feature-highlight` - Animated callout boxes
- `zoom-in` - Smooth zoom to product
- `splitscreen` - Side-by-side comparison
- `multi-angle` - Multiple camera angles

**Example:**
```json
{
  "type": "product_showcase",
  "image": "product.png",
  "animation": "3d-rotate",
  "rotation_degrees": 360,
  "duration": 8,
  "caption": "AI Creative Tools - IDR 75K"
}
```

---

### 3. Data Visualization
**Description:** Animated charts, stats, infographics

**Use Cases:**
- Growth statistics
- Financial charts
- Achievement reveals
- Comparison graphs

**Templates:**
- `bar-chart-growth` - Bar chart growing from 0 to target
- `counter` - Number counting up (0 → 10,000)
- `progress-bar` - Progress bar filling
- `pie-chart` - Rotating pie chart
- `stat-cards` - Animated stat cards

**Example:**
```json
{
  "type": "data_viz",
  "animation": "counter",
  "start": 0,
  "end": 10000,
  "duration": 5,
  "format": "IDR #,###"
}
```

---

### 4. Logo Animation
**Description:** Professional logo reveals for brands

**Use Cases:**
- Video intros
- Brand reveals
- Channel branding
- Transition animations

**Templates:**
- `path-draw` - SVG path draws itself
- `scale-fade` - Logo scales in while fading
- `rotate-in` - Logo rotates from center
- `glow-effect` - Logo with animated glow
- `gradient-bg` - Animated gradient background

**Example:**
```json
{
  "type": "logo_reveal",
  "image": "logo.svg",
  "animation": "path-draw",
  "duration": 5,
  "glow": true
}
```

---

### 5. Social Media Templates
**Description:** Optimized for TikTok/Reels aspect ratios

**Use Cases:**
- TikTok videos
- Instagram Reels
- YouTube Shorts
- Twitter video posts

**Features:**
- 9:16 aspect ratio (vertical video)
- Safe zones for text/captions
- Beat-synced transitions
- Trending audio support
- Caption integration

**Templates:**
- `tiktok-intro` - 3-second intro for TikTok
- `reels-hook` - 5-second hook for Reels
- `youtube-shorts` - 15-second YouTube Short
- `thread-clip` - Short clip for Twitter

**Example:**
```json
{
  "type": "social_post",
  "platform": "tiktok",
  "template": "tiktok-intro",
  "text": "Viral Content Strategy",
  "duration": 3
}
```

---

## Advanced Features

- Configure animator, domain, relevant, remotion, skill settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Composition Sequencing

**Description:** Combine multiple animations into one video

**Example:**
```javascript
// compositions.json
{
  "sequence": [
    { "composition": "intro", "duration": 3 },
    { "composition": "main", "duration": 10 },
    { "composition": "outro", "duration": 2 }
  ]
}
```

### Beat Sync

**Description:** Animate to music beats

**Example:**
```javascript
{
  "audio": "music.mp3",
  "beats": [
    { "time": 0.5, "action": "scale-in" },
    { "time": 1.2, "action": "fade-in" },
    { "time": 2.8, "action": "transition" }
  ]
}
```

### Custom Easing

**Description:** Control animation timing with easing functions

**Easings:**
- `linear` - Constant speed
- `easeIn` - Slow start, fast end
- `easeOut` - Fast start, slow end
- `easeInOut` - Slow start and end
- `elastic` - Bouncy effect
- `back` - Overshoot effect

### Color Schemes

**Presets:**
- `light` - White background, dark text
- `dark` - Dark background, light text
- `custom` - Custom color palette

**Example:**
```json
{
  "scheme": "custom",
  "background": "#1a1a2e",
  "text": "#ffffff",
  "accent": "#4ECDC4"
}
```

---

## Output Formats

- Configure animator, domain, relevant, remotion, skill settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Video Formats
| Format | Codec | Quality | File Size | Best For |
|--------|-------|---------|-----------|---------|
| MP4 | H.264 | High | Medium | All platforms |
| WebM | VP9 | High | Low | Web, social media |
| MOV | ProRes | Very High | Large | Professional editing |
| GIF | Limited colors | Low | Medium | Simple animations |

### Resolutions
| Resolution | Dimensions | Platform | Use Case |
|-----------|-----------|----------|----------|
| 720p | 1280x720 | Instagram, Facebook | Horizontal video |
| 1080p | 1920x1080 | YouTube | HD video |
| 1080x1920 | 1920x1080 | TikTok, Reels | Vertical video |
| 4K | 3840x2160 | Professional | High-end production |

### Frame Rates
| Frame Rate | Best For |
|-----------|----------|
| 24fps | Cinematic content |
| 30fps | Standard (most social media) |
| 60fps | Smooth motion, gaming content |

---

## Comparison: Remotion vs FFmpeg

| Feature | Remotion | FFmpeg |
|---------|----------|---------|
| Flexibility | 10/10 | 3/10 |
| Ease of Use | 8/10 | 4/10 |
| Power | 9/10 | 5/10 |
| Speed | 6/10 | 8/10 |
| Quality | 10/10 | 7/10 |
| Maintainability | 9/10 | 4/10 |
| Ecosystem | 9/10 | 8/10 |

**When to Use Remotion:**
- Complex animations (multiple elements, layers)
- Programmatic control (data-driven animations)
- React-based workflows
- Need for flexibility/change
- Typography-heavy content
- Brand consistency (reusable components)

**When to Use FFmpeg:**
- Simple cuts/trims
- Batch processing large files
- Fast prototyping
- Hardware acceleration needed
- Very long videos (10+ minutes)

---

## Script Reference

- Configure animator, domain, relevant, remotion, skill settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### create_animation.py
```bash
# Create animation from template
python3 create_animation.py --template kinetic_typo --text "Hello World" --duration 5

# Options:
--template <template_name>    # Animation template to use
--text <text>                 # Text content
--duration <seconds>           # Animation duration
--colors <color1,color2>       # Color palette
--output <file.json>          # Output JSON config
```

### render_animation.py
```bash
# Render animation to video
python3 render_animation.py --input animation.json --output video.mp4

# Options:
--input <file.json>            # Animation config JSON
--output <file.mp4>            # Output video file
--format <mp4|webm|mov>       # Output format
--resolution <720p|1080p|4k>     # Resolution
--fps <24|30|60>              # Frame rate
--optimize                     # Optimize for file size
```

### batch_render.py
```bash
# Batch render multiple animations
python3 batch_render.py --config animations.json

# Options:
--config <file.json>           # Batch config JSON
--parallel <count>             # Parallel renders
--output-dir <directory>        # Output directory
```

### preview_animation.py
```bash
# Preview animation in browser
python3 preview_animation.py --input animation.json

# Options:
--input <file.json>            # Animation config JSON
--port <port>                 # Dev server port (default: 3000)
```

### optimize_video.py
```bash
# Optimize video for file size
python3 optimize_video.py --input video.mp4 --output video_optimized.mp4

# Options:
--input <file.mp4>            # Input video file
--output <file.mp4>           # Output video file
--quality <1-100>            # Quality setting (100 = max)
--max-size <MB>               # Max file size
```

---

## File Structure

```
skills/remotion-animator/
├── SKILL.md                   # This file
├── skill.json                 # Skill metadata
├── templates/                  # Animation templates
│   ├── kinetic_typo.js
│   ├── product_showcase.js
│   ├── data_viz.js
│   ├── logo_reveal.js
│   └── social_post.js
├── scripts/                   # Python scripts
│   ├── create_animation.py
│   ├── render_animation.py
│   ├── batch_render.py
│   ├── preview_animation.py
│   └── optimize_video.py
├── utilities/                 # Helper functions
│   ├── easing.js
│   ├── colors.js
│   └── audio.js
└── examples/                  # Example animations
    ├── simple_text.json
    ├── counter.json
    └── product_rotation.json
```

---

## Examples

- Configure animator, domain, relevant, remotion, skill settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Example 1: Kinetic Typography

**Config:**
```json
{
  "type": "kinetic_typo",
  "text": "Viral Content Strategy",
  "animation": "scale-in",
  "duration": 3,
  "fontSize": 80,
  "fontWeight": 800,
  "colors": ["#FF6B6B", "#4ECDC4"]
}
```

**Result:** 3-second text scale animation with gradient background

---

### Example 2: Counter Animation

**Config:**
```json
{
  "type": "data_viz",
  "animation": "counter",
  "start": 0,
  "end": 10000,
  "duration": 5,
  "format": "IDR #,###"
}
```

**Result:** 5-second counter animation from 0 to 10,000 IDR

---

### Example 3: Product Rotation

**Config:**
```json
{
  "type": "product_showcase",
  "image": "product.png",
  "animation": "3d-rotate",
  "rotation_degrees": 360,
  "duration": 8,
  "caption": "AI Creative Tools - IDR 75K"
}
```

**Result:** 8-second 360° product rotation with caption

---

## Learning Resources

- Configure animator, domain, relevant, remotion, skill settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Official Documentation
- Remotion Docs: https://www.remotion.dev/docs
- Remotion Examples: https://www.remotion.dev/examples
- Community Discord: https://discord.gg/7dWjXQp

### Tutorials
1. **Remotion for React Developers** (official)
2. **Kinetic Typography Tutorial** (YouTube)
3. **Motion Graphics with Remotion** (freeCodeCamp)

### Tips
1. **Start Simple:** Text animation first, then add complexity
2. **Use Hot Reload:** `npm run dev` for instant preview
3. **Easing Matters:** Right easing makes animations feel natural
4. **Composition Over Composition:** Build complex videos from simple parts
5. **Test Early:** Render short previews often

---

## Troubleshooting

- Configure animator, domain, relevant, remotion, skill settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Common Issues

**Issue:** Animation not rendering
**Solution:** Check Node.js version (18+), reinstall dependencies

**Issue:** Output video is black
**Solution:** Check composition name, verify component is exported

**Issue:** File size too large
**Solution:** Use optimize_video.py script, lower resolution or frame rate

**Issue:** Text is blurry
**Solution:** Use vector fonts (SVG), increase resolution to 1080p+

**Issue:** Export is slow
**Solution:** Enable hardware acceleration (check FFmpeg config)

---

## Best Practices

1. **Plan Before Coding:** Sketch animation, break into components
2. **Use Easing:** Right easing = natural feel
3. **Test Multiple Resolutions:** Ensure works at 720p and 1080p+
4. **Optimize Early:** Don't wait until final render to optimize
5. **Version Control:** Keep templates in git for versioning
6. **Document Your Animations:** Comment complex animations
7. **Reuse Components:** Build library of reusable animation components
8. **Preview Often:** Use dev mode for instant feedback

---

**Skill Version:** 1.0.0
**Last Updated:** March 17, 2026
**Author:** Vilona (BerkahKarya AI)

---

*Ready to create stunning animations with Remotion!* 🚀

## How to Use

1. Define content goal (traffic, engagement, conversion, brand awareness)
2. Research target audience pain points and search intent
3. Generate content using appropriate AI tools
4. Edit and humanize output for authenticity
5. Optimize for target platform (SEO, hashtags, format)
6. Schedule and distribute across channels
7. Measure performance and iterate

## Red Flags

- **AI-generated content sounds robotic**: Always run through humanizer before publishing
- **Engagement dropping week-over-week**: Content fatigue or algorithm change — vary formats
- **Duplicate content across platforms**: Adapt content per platform, don't just cross-post
- **No content calendar**: Sporadic posting kills audience retention
- **Ignoring analytics**: Content without measurement is just publishing, not marketing

## Verification

- Check readability score (target grade 8 or below for general audiences)
- Verify all images have alt text and proper dimensions per platform
- Confirm links work and point to correct destinations
- Test video/audio quality before publishing
- Validate content renders correctly on mobile devices
