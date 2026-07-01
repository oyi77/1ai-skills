---
name: b-roll-finder
description: >
  Find relevant B-roll and stock footage by analyzing script content with semantic search. Match video
  meaning to text instead of random selection. Use when sourcing stock footage, finding B-roll clips,
  or matching visuals to narration.
domain: content
tags:
  - video
  - semantic-search
  - b-roll
  - stock-footage
  - ai
---
# B-Roll Finder

## When to Use

**Trigger phrases:**
- "find B-roll" · "stock footage for this script" · "match videos to narration"
- "relevant footage" · "B-roll selection" · "visual content for this script"
- "find clips that match" · "video search by meaning" · "semantic video search"

**Use cases:**
- YouTube video production — find B-roll that matches narration
- Documentary creation — source relevant footage for each section
- Marketing video assembly — match visuals to ad copy
- Tutorial video creation — find screen recordings / demos
- Social media content — quick visual matching

**When NOT to use:**
- When you have pre-selected footage
- When random stock footage is acceptable
- For custom-shot video (use a camera)

---

## Overview

Semantic video matching analyzes the meaning of your script/narration and finds stock footage clips that visually match each section. Instead of random keyword search, it understands context — "a person struggling with spreadsheets" matches footage of frustrated office workers, not just "spreadsheet" keyword hits.

## Process

1. **Input script** — Provide narration text, article, or section-by-section breakdown
2. **Semantic analysis** — Extract key visual concepts from each section
3. **Search stock libraries** — Query Pexels, Pixabay, or custom libraries with semantic matches
4. **Rank results** — Score clips by relevance to narration meaning
5. **Select and download** — Pick best matches, trim to section length
6. **Assemble** — Use [video-editor](../video-editor/SKILL.md) to combine B-roll with voiceover

## API Example (Pexels)

```bash
# Search by semantic concept
curl "https://api.pexels.com/videos/search?query=person+frustrated+at+computer&per_page=10" \
  -H "Authorization: $PEXELS_API_KEY" | jq '.videos[].video_files[] | select(.quality=="sd") | .link'
```

## Workflow with faceless-youtube

```
Script → b-roll-finder (match visuals) → video-editor (assemble) → faceless-youtube (upload)
```

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Random stock footage works" | Random clips feel disconnected. Semantic matching makes B-roll feel intentional and professional. |
| "Keywords are enough" | "Office" returns generic results. "Person overwhelmed by data" returns specific, relevant footage. |
| "Skip B-roll, just use talking head" | B-roll increases retention by 20-40%. Every section needs visual variety. |

## Verification

- [ ] Each script section has matching B-roll selected
- [ ] Clips are relevant to narration meaning, not just keywords
- [ ] Clip durations match section lengths
- [ ] Resolution is consistent (720p minimum)
- [ ] Clips downloaded and ready for assembly
