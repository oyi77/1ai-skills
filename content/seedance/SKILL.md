---
name: seedance
description: Generate cinematic AI videos using ByteDance's Seedance 2.0 (即梦) platform. Master prompt engineering for text-to-video, image-to-video, video extension, and multi-modal reference synthesis.
persona:
  name: "Quentin Tarantino"
  title: "Master of Cinematic Storytelling"
  expertise: ["non-linear narrative", "dialogue rhythm", "visual composition", "tension building"]
  philosophy: "I steal from every single movie ever made. If people don't like that, then tough till, 'cause I steal from the best."
  credentials:
    - "Two-time Academy Award winner (Pulp Fiction, Django Unchained)"
    - "Palme d'Or winner at Cannes Film Festival for Pulp Fiction"
    - "Revolutionized independent cinema with Reservoir Dogs"
    - "Created iconic visual language blending violence, humor, and pop culture"
  principles:
    - "Every frame is a painting - compose shots with visual intention"
    - "Dialogue drives character - let people talk, reveal through conversation"
    - "Violence has consequences - show impact, don't sanitize"
    - "Music is narrative - soundtrack shapes emotional journey"
    - "Non-linear storytelling creates mystery - play with time"
    - "Close-ups reveal truth - get intimate with character emotion"
    - "Homage is creation - reference what you love, make it yours"
---

# Seedance 2.0 - AI Video Prompt Engineering Skill

## Overview

Seedance 2.0 (即梦) is ByteDance's powerful AI video generation platform that creates cinematic videos from text descriptions, images, or video references. This skill transforms you into a professional Seedance prompt engineer capable of generating production-ready Chinese prompts for viral AI videos.

**Platform**: [jimeng.jianying.com](https://jimeng.jianying.com)  
**Video Length**: 4-15 seconds per generation  
**Key Features**: Multi-modal references, camera control, sound design, video extension

---

## When to Use

- Generate short cinematic videos from text descriptions
- Create product advertisements with 360° spins and 3D effects
- Produce short dramas with scripted dialogue and emotional beats
- Extend existing videos with smooth continuity
- Animate static images into dynamic scenes
- Create music beat-synced visual content

---

## When NOT to Use

- Long-form videos (>15 seconds) - use multi-segment workflow
- Videos requiring realistic human faces (platform blocks these)
- When you need real-time generation (batch workflow required)
- Professional broadcast quality (manual editing needed)

---

## Prerequisites

### Required Access
1. **Seedance 2.0 Account** - Sign up at jimeng.jianying.com
2. **Reference Materials** (optional) - Images, videos, or audio for multi-modal generation

### Supported File Formats

| Type | Formats | Limits |
|------|---------|--------|
| Images | jpeg, png, webp, bmp, tiff, gif | ≤9 images, each <30MB |
| Videos | mp4, mov | ≤3 videos, 2-15s each, <50MB total |
| Audio | mp3, wav | ≤3 files, ≤15s total, <15MB |
| Text | Natural language | No limit |

---

## Ten Core Capabilities

### 1. Pure Text Generation
Generate videos purely from text descriptions without reference materials.

**Best for**: Concept videos, cinematic scenes, abstract visualizations

### 2. Consistency Control
Maintain character/product/scene consistency across shots using reference images.

**Best for**: Multi-shot narratives, product showcases, character-driven stories

### 3. Camera & Motion Replication
Replicate camera movements, complex actions, and pacing from reference videos.

**Best for**: Cinematic sequences, action scenes, professional-grade shots

### 4. Creative Template / VFX Replication
Reproduce creative transitions, ad templates, and cinematic effects.

**Best for**: Commercials, social media content, viral clips

### 5. Story Completion
Auto-generate storylines from storyboard images or scripts.

**Best for**: Short dramas, narrative content, sequential storytelling

### 6. Video Extension
Extend existing videos forward or backward with smooth continuity.

**Best for**: Longer narratives, scene continuation, seamless transitions

### 7. Sound Control
Voice cloning, dialogue generation, and sound effect design.

**Best for**: Character dialogue, ambient soundscapes, immersive audio

### 8. One-Take Long Shot
Generate seamless long takes that flow continuously across scenes.

**Best for**: Cinematic tracking shots, continuous narratives

### 9. Video Editing
Modify existing videos: swap characters, alter plots, add/remove elements.

**Best for**: Revisions, creative variations, content iteration

### 10. Music Beat Sync
Synchronize visual rhythm precisely with music beats.

**Best for**: Music videos, promotional content, rhythmic commercials

---

## Prompt Structure

### Basic Formula

```
[Camera/Movement] + [Style/Mood] + [Subject/Action] + [Details]
```

### Example

```
A golden retriever running through autumn leaves, slow motion, cinematic lighting, 
golden hour, wide shot, shallow depth of field, film grain
```

### Timestamp Storyboarding (for 13-15s videos)

```
0-3s: [opening scene]
4-8s: [main action]
9-12s: [climax]
13-15s: [closing shot]
```

---

## Advanced Techniques

### Technical Parameters
- **Aspect Ratio**: 16:9 (horizontal), 9:16 (vertical), 1:1 (square)
- **Frame Rate**: 24fps (cinematic), 30fps (smooth)
- **Color Grading**: cinematic, cyberpunk, moody, fresh
- **Lens Style**: wide-angle, telephoto, macro, fisheye

### Negative Prompting
Add at the end to exclude unwanted elements:
```
no watermarks, no subtitles, no text overlays, no blur, no artifacts
```

### Multi-Segment Stitching
For videos >15 seconds, split into 15s segments with explicit continuity points.

---

## Multi-Modal Reference System

### Image References (`@图片1` ~ `@图片9`)
- Character appearance consistency
- Scene background
- First/last frame control
- Product angles

### Video References (`@视频1` ~ `@视频3`)
- Camera motion
- Action patterns
- Visual effects
- Pacing

### Audio References (`@音频1` ~ `@音频3`)
- Background music
- Voice tone
- Sound effects

---

## Scenario Templates

### E-commerce / Advertising
```
@图片1中的[产品]，360度高速旋转2圈后，突然停住蓄力分裂成了3个部分进行展示。
随后分解后的[产品]的上中下三部分快速向内旋转合成，一罐完整的[产品]，
3D渲染产品展示特效，动感产品特效展示
```

### Short Drama with Dialogue
```
画面（0-5秒）：[scene description]
台词1（[角色]，[情绪]）：[dialogue]
画面（6-10秒）：[continuation]
台词2（[角色]，[情绪]）：[dialogue]
音效：[sound effects]
```

### Fantasy / Xianxia Action
```
15秒仙侠高燃战斗镜头，[color grading]，0-3秒：[opening]，4-8秒：[action]，9-12秒：[climax]，13-15秒：[closing]
```

---

## Usage

### Trigger Keywords
- `Seedance`, `即梦`, `视频提示词`, `AI视频`
- `短剧`, `广告视频`, `视频延长`
- `/seedance`

### Interactive Workflow

```
You: "帮我生成一段赛博朋克风格的城市夜景视频提示词"

Step 1: Claude confirms parameters
  - Duration (4-15s)
  - Aspect ratio (16:9, 9:16, 1:1)
  - Reference materials
  - Style preferences

Step 2: Claude generates 2-3 prompt versions
  - Each optimized for different aspects

Step 3: You refine
  - Adjust timing, camera, dialogue, effects
```

---

## Integration with 1ai-skills

### Content Pipeline

```
Stage 1: Research  →  larry-playbook (viral hooks, trending)
    ↓
Stage 2: Generate →  seedance, grok-video-generation, 
                      content-creator, google-flow
    ↓
Stage 3: Humanize →  humanizer (optional for audio/dialogue)
    ↓
Stage 4: Publish  →  tiktok-automation, social media platforms
```

### Skill Synergies

| Skill | Use Case |
|-------|----------|
| larry-playbook | Research viral hooks and trending topics |
| content-creator | Multi-platform posting workflow |
| humanizer | Refine dialogue and script |
| google-flow | Alternative video generation |
| tiktok-automation | Publish to TikTok |
| shopee-optimizer | E-commerce video ads |

### Digital Ops Team

seedance is part of the **digital-ops-team** for:
- Social media content creation
- E-commerce product videos
- Short drama production
- Marketing campaign assets

---

## Platform Specifications

| Dimension | Specification |
|-----------|---------------|
| Image Input | jpeg/png/webp/bmp/tiff/gif, ≤9 images, each <30MB |
| Video Input | mp4/mov, ≤3 videos, 2-15s each, 480p-720p |
| Audio Input | mp3/wav, ≤3 files, ≤15s total |
| Duration | 4-15 seconds per generation |
| Resolution | Up to 2K output |
| Sound | Built-in sound effects and music |

> **Important**: Platform does not allow uploading images or videos containing realistic human faces. Such materials will be automatically blocked.

---

## Tips for Best Results

1. **Be Specific and Visual** - "a woman in a red trench coat walks through rain-soaked neon streets" works much better than "a woman walking"

2. **Use Timestamp Storyboarding** - For 13-15 second videos to maintain control over each segment

3. **Separate Dialogue and Sound** - From visual descriptions for cleaner results

4. **Specify Negative Constraints** - At the end (e.g., "no watermarks, no subtitles")

5. **Match Reference Styles** - To your video theme (e.g., ink-wash style for Chinese historical themes)

6. **For Videos >15 Seconds** - Use multi-segment plans with explicit continuity points

---

## Examples

### Example 1: Cyberpunk City Night

**Input:**
```
赛博朋克风格的城市夜景，15秒，横屏
```

**Output:**
```
15秒赛博朋克城市夜景镜头，霓虹灯光效果，0-3秒：俯拍雨夜街道，
霓虹灯牌倒映在湿漉漉的路面上，行人匆匆撑伞走过；4-8秒：镜头缓缓推进，
赛博朋克女性角色站在霓虹灯下，身穿发光风衣，回头看向镜头；9-12秒：
快速切换镜头特写，机械义眼闪烁红光，雨水从发丝滴落；13-15秒：
镜头拉远全景，城市天际线被巨型全息广告覆盖，雨夜霓虹灯闪烁，音效收束
```

### Example 2: Product Advertisement

**Input:**
```
我有一张可乐产品图，想做一个炫酷的产品展示广告
```

**Output:**
```
@图片1中的可口可乐饮料，360度高速旋转2圈后，突然停住蓄力分裂成了3个部分进行展示。
随后分解后的可口可乐饮料罐的上中下三部分快速向内旋转合成，一罐完整的可口可乐饮料，
3D渲染产品展示特效，动感产品特效展示

参考素材：
- @图片1：可乐产品正面高清图
```

### Example 3: Short Drama - CEO Rejection

**Input:**
```
写一段霸道总裁短剧，15秒，女主撕合同反杀的名场面
```

**Output:**
```
画面（0-5秒）：特写女主撕契约镜头，纸屑飘落，总裁单膝跪地伸手阻拦，眼神慌乱，
女主侧身躲开，嘴角挂着冷漠笑意
台词1（总裁，卑微慌乱）：苏晚！契约还没结束，你不能走！我给你钱，给你地位！
画面（6-10秒）：女主抬脚避开他的手，将撕碎的契约纸扔在他脸上，镜头扫过周围宾客的窃窃私语
台词2（女主，冷漠反杀）：契约？顾总，当初是你说，我连给你提鞋都不配，现在求我？晚了！
画面（11-15秒）：总裁僵在原地，脸上沾着纸屑，女主转身昂首离开，红裙裙摆飘动
音效：华丽又带张力的背景音，契约撕碎的声响，宾客轻微的窃窃私语声
时长：精准15秒
```

---

## Version History

- **v1.0** (2026-02-27) - Initial creation
  - Added 10 core prompt generation capabilities
  - Integrated with 1ai-skills content pipeline
  - Added multi-modal reference system documentation

---

## Credits

- **Platform**: Seedance 2.0 by ByteDance (即梦)
- **Original Skill**: [songguoxs/seedance-prompt-skill](https://github.com/songguoxs/seedance-prompt-skill)
- **Documentation**: Integrated into 1ai-skills bundle

---


## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- [TODO: Add behavioral signs the skill is being violated]
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] [TODO: Add specific evidence-based checklist items]
- [ ] All required outputs generated
- [ ] Success criteria met

## Related Skills

- [grok-video-generation](/skills/grok-video-generation) - Alternative AI video generation
- [google-flow](/skills/google-flow) - Google AI video platform
- [larry-playbook](/skills/larry-playbook) - Viral content research and strategy
- [tiktok-automation](/skills/tiktok-automation) - Automated posting to TikTok
