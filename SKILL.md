# Larry Playbook — Viral TikTok Content Generator

Autonomous AI agent that learns and improves viral content over time using Oliver Henry's proven formula.

**Proven Results (5 days,2025):**
- 500K+ total TikTok views
- 234K views on top single post
- 4 posts with 100K+ views
- 108 paying subscribers
- MRR: $588/month

---

## Quick Start

### Prerequisites
- **OpenAI API key** (optional) for image generation
  ```bash
  export OPENAI_API_KEY="sk-proj-xxxx"
  ```

### Usage

**Generate a single viral TikTok slideshow:**
```bash
# Manual mode
larry-playbook generate --room kitchen_small --hook landlord_kitchen

# Continuous mode (autonomous)
export POST_BRIDGE_API_KEY="pb_live_xxxx"

larry-playbook continuous
```

---

## The Viral Hook Formula

**Formula (234K views post):**
```
[Another person's problem] + [Doubt/Conflict] 
→ Showed them AI Result
→ They changed their mind / took action
```

**Why it works:**
- Creates curiosity (what happened?)
- Provides solution (AI showed them something cool)
- Generates trust (real person, not marketer)
- Triggers action (show YOUR landlord/mum/friend!)

**Working Examples:**

| Hook Type | Example | Views |
|-----------|---------|-------|
| ✅ **Third-party + AI** | "My landlord said I can't change anything so I showed her what AI thinks it could look like" | **234,000** |
| ❌ Self-focused | "Why does my flat look like a student loan" | 905 |
| ❌ Feature-focused | "See your room in 12+ styles before you commit" | 879 |

---

## Content Architecture

### TikTok Slideshow
- **Exactly 6 slides** (TikTok's sweet spot)
- **Portrait (1024x1536)** for all images
- **2.5 seconds per slide** (15 seconds total)
- **Slide 1:** Hook with text overlay
- **Slide 2-6:** Same room, different styles

### Slide 1: The Hook
Must include:
- ✅ Third person with problem
- ✅ Doubt or conflict
- ✅ "Showed them AI" phrase
- ✅ Call to action (implicit or explicit)

---

## Available Commands

### `larry-playbook generate`
Generate a single 6-slide viral TikTok slideshow.

**Options:**
- `--room <type>`: Room type (kitchen_small, living_room_cozy, bedroom_minimal, studio_apartment)
- `--hook <type>`: Hook type (landlord_kitchen, parent_bedroom, roommate_living, landlord_kitchen)

**Example:**
```bash
larry-playbook generate --room kitchen_small --hook landlord_kitchen
```

### `larry-playbook continuous`
Run autonomous agent that learns and improves over time.

**Features:**
- Hourly research of trending content
- Confidence-based content generation
- Automatic posting to connected platforms
- Performance tracking and rule updates

**Setup:**
```bash
export POST_BRIDGE_API_KEY="pb_live_xxxx"

larry-playbook continuous
```

---

## Hook Templates

### Landlord + AI Room Design
```
My landlord said I can't change anything, so I showed her what AI thinks our rental kitchen could look like 🏠

She was honestly SHOCKED!
```

### Parent + AI Transformation
```
My dad thought I was crazy for using AI to redesign our bedroom, but this AI design completely changed his mind 🛏️

Now he's showing it off!
```

### Roommate + AI Suggestion
```
My roommate thinks our living room is too small for an island, so I showed her what AI suggests: a space-efficient layout 🗺️

She actually wants to build it now!
```

---

## Confidence-Based Flow Selection

| Confidence | Flow | Priority | Description |
|-----------|-------|------------|-------------|
| **High (0.8+)** | Larry Slideshow | 1 | Proven 500K+ views formula |
| **Medium (1.5)** | Viral Image Posting | 2 | Tested moderate concepts |
| **Low (1.0)** | Simple Caption Posting | 3 | New untested ideas |

System automatically selects flow based on performance data and learns from failures.

---

## Output Structure

When generating content, system creates:

```
~/.openclaw/workspace/output/larry_slideshows/
├── <room>_slideshow.mp4    ← 6-slide viral video
└── content.json             ← Caption and hashtags

~/.openclaw/workspace/memory/
├── SYSTEM_MEMORY.json        ← Performance tracking
└── logs/                   ← Daily activity logs
```

---

## Performance Tracking

System automatically logs:
- Total posts generated
- Views per post (estimated based on engagement)
- Hook performance by type (which formula works best)
- Confidence level evolution
- Success/failure rates

---

## License

Based on Oliver Henry's public case study.
Use and adapt freely. The real value is in the data-driven iteration, not the specific hooks.

**Core Principle:**
> "Every failure becomes a rule. Every success becomes a formula. The system compounds."
