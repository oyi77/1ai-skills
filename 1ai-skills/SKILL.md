# Larry Playbook — Viral TikTok Content Generator

**Skill Type:** Content Generation & Social Media Automation

**Version:** 2.0

**Author:** OpenClaw Agent (ai@openclaw.dev)

**Description:** Autonomous agent that learns and improves viral TikTok content over time using Oliver Henry's proven 500K+ views formula.

---

## Overview

Larry Playbook is a complete viral content generation system inspired by Oliver Henry's multi-million dollar case study.

**Proven Results (5 days, 2025):**
- 500K+ total TikTok views
- 234K views on top single post
- 4 posts with 100K+ views
- 108 paying subscribers
- MRR: $588/month
- Cost: ~$0.50/post (API calls)

### Core Philosophy

> "Every failure becomes a rule. Every success becomes a formula. The system compounds."

This system is NOT about:
- Asking ChatGPT for captions
- Generic motivational quotes
- AI art that looks fake
- Guessing what works

This IS about:
- Data-driven iteration
- Persistent memory and learning
- Locking down architecture
- Documenting everything
- Scaling what works

---

## Features

### 📊 Continuous Learning System
- **Hourly research** — Find trending TikTok content, viral hooks, winning formulas
- **Confidence-based generation** — Select content flow based on performance data (High/Medium/Low)
- **Multi-platform posting** — Post to all connected platforms via Post-Bridge
- **Feedback loop** — Track performance, update confidence levels, learn from failures

### 🎯 Viral Content Generation
- **6-Slide TikTok Slideshow** — Using Larry's proven 234K views formula
- **20+ Hook Templates** — Landlord + AI, Parent + AI, Roommate + AI, etc.
- **Locked Architecture** — Same room across all slides, different styles only
- **Story-Style Captions** — Natural app mentions with relevant hashtags

### 📱 Social Media Management
- **Post-Bridge Integration** — Upload drafts, add trending sounds, publish to TikTok
- **Multi-Platform Support** — Facebook (24 accounts), TikTok (1), Instagram, LinkedIn, X
- **Scheduling** — Optimal posting times based on audience timezone

### 🧠 Analytics & Tracking
- **Performance Metrics** — Views, engagement, MRR, conversion tracking
- **Hook Performance** — Which formulas work best (Landlord, Parent, etc.)
- **Confidence Evolution** — Automatic confidence adjustment based on success rate
- **Memory System** — Log all failures and successes for continuous improvement

---

## Installation

### Quick Start

```bash
# Install via ClawHub
clawhub install username-kamu/larry-playbook

# Or manual setup
git clone https://github.com/username-kamu/larry-playbook.git ~/.openclaw/workspace/skills/
```

### Environment Variables

```bash
# Required for content generation
export POST_BRIDGE_API_KEY="pb_live_xxxx"

# Optional for image generation (Larry's workflow uses OpenAI)
export OPENAI_API_KEY="sk-proj-xxxx"
```

### Quick Demo

Generate a single viral TikTok slideshow:
```bash
export POST_BRIDGE_API_KEY="pb_live_xxxx"

python3 skills/larry-playbook/larry-demo.py
```

### Continuous Mode

Run autonomous agent that learns and improves:
```bash
export POST_BRIDGE_API_KEY="pb_live_xxxx"

python3 skills/larry-playbook/larry-continuous-system.py
```

**What the system does:**
1. Every hour → Research trending content (TikTok, viral hooks)
2. On-demand → Generate viral slideshow based on research and confidence
3. On-demand → Post to all connected platforms via Post-Bridge
4. Continuous → Track performance, update confidence, learn from results

---

## The Viral Hook Formula

**Formula (234K views post):**
```
[Another person's problem] + [Doubt/Conflict] 
→ Showed them [AI Result]
→ They changed their mind / took action
```

**Why it works:**
- Creates curiosity (what happened?)
- Provides solution (AI showed them something cool)
- Generates trust (real person, not marketer)
- Triggers action (show YOUR landlord/mum/friend!)

**Working Examples:**

| Hook Type | Example | Views | Why |
|-----------|---------|-------|-------|
| ❌ Self-focused | "Why does my flat look like a student loan" | 905 | About YOU, nobody cares |
| ❌ Feature-focused | "See your room in 12+ styles before you commit" | 879 | Selling features, boring |
| ✅ **Third-party + AI** | "My landlord said I can't change anything so I showed her what AI thinks it could look like" | **234,000** | Relatable problem + cool solution |

---

## Content Architecture

### TikTok Slideshow Format
- **Exactly 6 slides** (TikTok's sweet spot)
- **Portrait (1024x1536)** for all images
- **2.5 seconds per slide** (15 seconds total)
- **Slide 1:** Hook with text overlay
- **Slide 2-6:** Same room, different styles only
- **Text overlay:** Large font, safe Y position (below status bar)
- **Duration:** Auto-advance (2-3 seconds per slide)

### Slide 1: The Hook
Must include:
- ✅ Third person with problem
- ✅ Doubt or conflict
- ✅ "Showed them AI" phrase
- ✅ Call to action (implicit or explicit)

---

## Usage

### Commands

#### Manual Mode
```bash
# Generate single viral TikTok slideshow
larry-playbook generate --room kitchen_small --hook landlord_kitchen

# Continuous mode (autonomous learning)
larry-playbook continuous
```

#### List Available Content Types
```bash
larry-playbook generate --list-types
```

#### Get System Status
```bash
larry-playbook status
```

---

## Memory System

### MEMORY.md Structure
```markdown
## Viral Performance

### Winning Hooks
- [Date] [Hook Type]: "[Hook text]" → [Views] views
  - Why worked: [Reason]
  - Caption used: [Caption]

### Losing Hooks
- [Date] [Hook Type]: "[Hook text]" → [Views] views
  - Why failed: [Reason]
  - Lesson learned: [Rule update]

### Content Rules
- Slide count: 6 slides (proven sweet spot)
- Resolution: 1024x1536 portrait
- Hook position: Slide 1, large font, safe Y position
- Caption length: 150-200 chars (optimal engagement)
- Hashtag count: Exactly 5

### Platform Performance
- TikTok: {"confidence": 0.8, "engagement_rate": 0.12}
- Facebook: {"confidence": 0.6, "engagement_rate": 0.08}
```

### Confidence Evolution

```
New hook tested → 5K views (success) → Confidence UP
↓
New hook fails → 3K views (failure) → Confidence DOWN
After 10 successes → Confidence maxed at 1.0x → Dominant flow
```

---

## Learning Loop

```
Generate Post → Observe Results (24-48h) → Update Rules → Generate Next Post
                                                              ↑
                                                    Repeat forever
```

---

## Troubleshooting

**Issue:** Low engagement rate
**Solution:** Improve caption quality, target better accounts

**Issue:** Hooks getting deleted
**Solution:** Avoid spam phrases, add more value, be relevant

---

## License

This skill is based on publicly shared case study by Oliver Henry.
Use and adapt freely. The real value is in:
- The data-driven iteration
- The persistent learning system
- The human-AI collaboration model

---

**Last Updated:** 2026-02-27  
**Version:** 2.0  
**Skill Type:** Content Generation & Social Media Automation  
**Author:** OpenClaw Agent
