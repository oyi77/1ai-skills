---
name: content-suite
description: Complete content creation ecosystem - planning, research, scripting, production, engagement. Supports multi-persona accounts with consistent characters.
version: 1.0.0
---
persona:
  name: "Domain Expert"
  title: "Master of Content Suite"
  expertise: ['Content Excellence', 'Best Practices', 'Professional Standards']
  philosophy: "Excellence is not a skill, it's an attitude."
  credentials: ['Industry leader', 'Practiced professional', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based', 'Customer focused']



# Content Suite - Master Content Ecosystem

End-to-end content pipeline with multi-persona support and cross-engagement.

## Components

### 1. Content Planner
Plan content calendar, themes, and posting schedule.
```bash
# Generate weekly content plan
python3 scripts/planner.py --niche motivation --days 7 --posts-per-day 3
```

### 2. Viral Researcher
Research trending topics, hooks, and viral patterns.
- Uses: kalodata, TikTok trends, competitor analysis
```bash
python3 scripts/researcher.py --platform tiktok --niche motivation --limit 20
```

### 3. Script Writer
Generate hooks, scripts, and captions.
- Uses: larry-playbook formulas
```bash
python3 scripts/script_writer.py --hook "landlord" --style storytelling
```

### 4. Storyboard Generator
Create visual storyboard for video production.
```bash
python3 scripts/storyboard.py --script "script.txt" --scenes 6
```

### 5. Video Producer
Generate videos with consistent characters.
- Uses: GeminiGen, Remotion, edge-tts
```bash
python3 scripts/producer.py --storyboard "storyboard.json" --character "avatar_01"
```

### 6. Buzzer System 🆕
Cross-engagement from multiple accounts.
```bash
python3 scripts/buzzer.py --target-post "url" --accounts 5 --action comment
```

### 7. Persona Manager 🆕
Manage multiple account personas.
```bash
python3 scripts/persona_manager.py --list
python3 scripts/persona_manager.py --create "Motivator_ID" --style motivational
```

### 8. Character Consistency 🆕
Maintain consistent avatars/characters across content.
```bash
python3 scripts/character.py --create "avatar_01" --style "anime girl, pink hair"
python3 scripts/character.py --generate "avatar_01" --scene "kitchen"
```

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                     CONTENT SUITE PIPELINE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. RESEARCH      →  kalodata + trend analysis                  │
│       ↓                                                          │
│  2. PLAN          →  content calendar + themes                   │
│       ↓                                                          │
│  3. SCRIPT        →  hooks + captions (larry-playbook)          │
│       ↓                                                          │
│  4. STORYBOARD    →  visual scenes + timing                     │
│       ↓                                                          │
│  5. CHARACTER     →  consistent avatar selection                 │
│       ↓                                                          │
│  6. PRODUCE       →  video generation (GeminiGen + Remotion)    │
│       ↓                                                          │
│  7. PERSONA       →  account-specific formatting                 │
│       ↓                                                          │
│  8. PUBLISH       →  PostBridge multi-platform                   │
│       ↓                                                          │
│  9. ENGAGE        →  buzzer cross-commenting                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Multi-Persona Architecture

Each account has unique:
- **Voice**: Writing style, emoji usage, slang
- **Character**: Consistent avatar/background
- **Niche focus**: Specific topic angle
- **Posting time**: Optimized for audience

```
personas/
├── motivator_id.json    # Indonesian motivational
├── tech_bro_en.json     # English tech content
├── beauty_id.json       # Indonesian beauty tips
├── finance_id.json      # Indonesian finance
└── lifestyle_id.json    # Indonesian lifestyle
```

## Character Consistency

Store base images for consistent look:
```
characters/
├── avatar_01/
│   ├── base.png         # Base character image
│   ├── style.json       # Style parameters
│   └── variations/      # Scene variations
├── avatar_02/
└── backgrounds/
    ├── kitchen.png
    ├── office.png
    └── outdoor.png
```

## Buzzer System

Cross-engagement strategy:
1. Account A posts content
2. Accounts B, C, D comment within 30 min
3. Account A replies to comments
4. Creates organic-looking engagement

```python
buzzer_config = {
    "delay_min": 5,      # Min delay between comments
    "delay_max": 30,     # Max delay
    "comment_styles": ["supportive", "question", "emoji"],
    "avoid_patterns": ["same IP", "same device", "identical text"]
}
```

## Dependencies

- content-generator (video production)
- larry-playbook (hook formulas)
- kalodata-* (viral research)
- postbridge-social-manager (publishing)
- geminigen-ai (image/video generation)
- remotion (captions)
- edge-tts (voiceover)
