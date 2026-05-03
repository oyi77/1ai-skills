# AI Content Agency v2 - Sub-Skills Directory

## Purpose
Each sub-skill implements a specialized workflow from the 9-workflows blueprint.

## Directory Structure:

```
ai-content-agency-v2/
├── README.md
├── SKILL.md
├── workflows/       ← 9 workflow specs
├── sub-skills/     ← Individual skill implementations
│   ├── etika-makan/   ← Ideation & brainstorming
│   ├── makan-steak/    ← Detailing, POV, texture, storyboards
│   ├── makan-mie/    ← Production: production, rendering, stitching
│   └── ...
├── scripts/         ├── Implementation code
└── ...
```

## Individual Sub-Skills

### etika-makan (Creative Director Ideation)
**Purpose:** Generate 3 creative concepts + recommend workflow based on inputs
**Input:** Product info, target audience, stuck_on problem
**Output:** JSON with 3 ideas, hooks, recommended workflow

### makan-steak (Detailing & POV Production)
**Purpose:** Generate detailed production specs for each shot
**Input:** Concept, USP, sensory keywords, emotions, pain points
**Output:** Scene-by-scene directions, camera specs, storyboards

### makan-mie (Production & Stitching)
**Purpose:** Execute rendering, generate assets, composite final video
**Input:** Scripts, prompts, prompts, assets
**Output:** Final stitched video + voice + BGM layer, all tracks combined

## Usage Pattern

1. **Ideation Phase (etika-makan)**
   ```
   → User: "Ide konten untuk madu herbal"
   → Output: 3 concepts (herbal, what-if fusion, storytelling)
   → → Select best angle for workflow routing
   → Recommend workflow: "6" (Faceless Spiritual for spiritual mood, "7" for fusion twist)
   ```

2. **Production Phase (makan-steak + makan-mie)**
   ```
   → User: "Produksi POV Shots untuk madu herbal"
   → makan-steak: Scene-by-scene POV specs
   → makan-mie: Render, add transitions, stitch
   → Output: Final stitched TikTok video
   ```

---

## Installation Status

Each sub-skill should:
1. Have its own SKILL.md with specific instructions
2. Follow OpenClaw format (keywords, metadata, allowed-tools)
3. Connect to parent (ai-content-agency-v2)

---

## Skills Available

Parent Skill: ai-content-agency-v2
Location: /home/openclaw/.openclaw/workspace/skills/ai-content-agency-v2/

Ready for integrating specific workflow logic.