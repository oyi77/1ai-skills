---
name: video-semantic-match
description: Find relevant video clips by analyzing script content using semantic search. Match video meaning to text instead
  of random selection. Use when sourcing B-roll, stock footage, or relevant visual content for narration.
domain: content
tags:
- video
- semantic-search
- ai
- matching
- b-roll
- stock-footage
---

# Video Semantic Match

Find relevant video clips by analyzing script content using semantic search and similarity matching. Match video meaning to text instead of random selection for more engaging content.

**Source:** [MoneyPrinterTurbo-Extended](https://github.com/Asad-Ismail/MoneyPrinterTurbo-Extended)

## When to Use

**Trigger phrases:**
- "Find relevant footage for this script"
- "Match videos to narration semantically"
- "Select B-roll that matches the content"
- "Discover appropriate stock footage"
- "Analyze video-text relevance"

**Use cases:**
- YouTube video production
- Documentary creation
- Marketing video assembly
- Tutorial video creation
- Social media content
- Educational content

**When NOT to use:**
- When you have pre-selected footage
- When random stock footage is acceptable
- When manual curation is preferred
- For custom-shot video

## How It Works

### Traditional (Random)
```
Script: "AI is transforming healthcare"
        ↓
Random keyword: ["ai", "healthcare"]
        ↓
Random result from stock library
        ↓
❌ May show: generic tech office, unrelated hospital
```

### Semantic Match (This Skill)
```
Script: "AI is transforming healthcare"
        ↓
Semantic analysis: [medical AI, diagnosis, patient care, technology]
        ↓
Similarity search across video embeddings
        ↓
✅ Shows: AI medical imaging, robotic surgery, digital health records
```

## Installation

```bash
# Core dependencies
pip install sentence-transformers torch numpy scikit-learn

# Video analysis (optional)
pip install opencv-python pillow

# Stock API access
pip install pexels-api pixabay-api unsplash-api
```

## Quick Start

### Basic Semantic Matching

```python
from semantic_video_matcher import VideoMatcher

# Initialize matcher
matcher = VideoMatcher(
    model_name="all-MiniLM-L6-v2",  # Fast, good quality
    device="cuda"  # or "cpu"
)

# Your script
script = """
Artificial intelligence is revolutionizing healthcare. 
Doctors now use AI to analyze medical images faster than ever.
Machine learning algorithms detect diseases early.
"""

# Find relevant videos from Pexels
videos = matcher.find_matching_videos(
    text=script,
    source="pexels",
    top_k=5,
    min_similarity=0.6
)

# Results with relevance scores
for video in videos:
    print(f"{video['score']:.2f}: {video['title']} - {video['url']}")
```

### Multi-Source Search

```python
# Search across multiple stock libraries
videos = matcher.find_matching_videos(
    text=script,
    sources=["pexels", "pixabay", "unsplash"],
    top_k=10,
    filters={
        "orientation": "landscape",
        "min_duration": 5,  # seconds
        "max_duration": 30
    }
)
```

## Configuration

### Similarity Models

| Model | Speed | Quality | Size | Use Case |
|-------|-------|---------|------|----------|
| `all-MiniLM-L6-v2` | Fast | Good | 80MB | Production, real-time |
| `all-mpnet-base-v2` | Medium | Better | 420MB | High-quality matching |
| `multi-qa-mpnet-base-dot-v1` | Medium | Best | 420MB | Q&A, complex queries |

```python
# Change model
matcher = VideoMatcher(model_name="all-mpnet-base-v2")
```

### Matching Strategies

#### 1. Sentence-Level Matching
Match each sentence to individual clips:

```python
matcher.match_by_sentences(
    script=script,
    min_similarity=0.65,
    clips_per_sentence=2
)
```

#### 2. Paragraph-Level Matching
Match full paragraphs to longer clips:

```python
matcher.match_by_paragraphs(
    script=script,
    min_similarity=0.6,
    clips_per_paragraph=3
)
```

#### 3. Keyword-Enhanced Matching
Combine semantic + keyword matching:

```python
matcher.match_hybrid(
    script=script,
    keywords=["ai", "healthcare", "technology"],
    semantic_weight=0.7,  # 70% semantic, 30% keyword
    keyword_weight=0.3
)
```

## Advanced Features

### Thumbnail Analysis

```python
from semantic_video_matcher import ThumbnailMatcher

# Initialize with vision model
thumb_matcher = ThumbnailMatcher(
    text_model="all-MiniLM-L6-v2",
    vision_model="clip-vit-base-patch32"
)

# Match script to video thumbnails
videos = thumb_matcher.match_with_thumbnails(
    text=script,
    source="pexels",
    analyze_thumbnails=True,
    thumbnail_weight=0.3  # 70% text, 30% visual
)
```

### Custom Video Library

```python
# Index your own video library
matcher.index_custom_library(
    video_dir="stock_footage/",
    metadata_file="videos.json",
    extract_thumbnails=True
)

# Search custom library
videos = matcher.find_matching_videos(
    text=script,
    source="custom",
    top_k=5
)
```

### Scene-by-Scene Matching

```python
# Match each scene to appropriate footage
script_scenes = [
    {"narration": "AI is changing healthcare", "duration": 5},
    {"narration": "Doctors analyze medical images", "duration": 8},
    {"narration": "Early disease detection", "duration": 6}
]

matched_scenes = []
for scene in script_scenes:
    videos = matcher.find_matching_videos(
        text=scene["narration"],
        source="pexels",
        top_k=3,
        duration_range=(scene["duration"] - 2, scene["duration"] + 2)
    )
    matched_scenes.append({
        "scene": scene,
        "videos": videos
    })
```

## Stock API Setup

### Pexels

```bash
# Get free API key: https://www.pexels.com/api/
export PEXELS_API_KEY=your_key_here
```

```python
from pexels_api import Pexels
matcher = VideoMatcher(pexels_key=os.getenv("PEXELS_API_KEY"))
```

### Pixabay

```bash
# Get free API key: https://pixabay.com/api/docs/
export PIXABAY_API_KEY=your_key_here
```

### Custom Sources

```python
class CustomVideoSource:
    def search(self, query, top_k=10):
        """Implement your own video search."""
        # Search internal library, s3 bucket, etc.
        return videos

matcher.register_source("internal", CustomVideoSource())
```

## Complete Pipeline Example

```python
import json
from semantic_video_matcher import VideoMatcher

def generate_video_from_script(script_path, output_path):
    """Complete workflow: script → matched footage → video."""
    
    # 1. Load script
    with open(script_path) as f:
        script_data = json.load(f)
    
    # 2. Initialize matcher
    matcher = VideoMatcher(
        model_name="all-mpnet-base-v2",
        pexels_key=os.getenv("PEXELS_API_KEY"),
        device="cuda"
    )
    
    # 3. Match each scene
    video_plan = []
    for scene in script_data["scenes"]:
        videos = matcher.find_matching_videos(
            text=scene["narration"],
            source="pexels",
            top_k=3,
            filters={
                "orientation": "landscape",
                "min_duration": scene["duration"],
                "quality": "hd"
            }
        )
        
        # Select best match
        best_match = videos[0] if videos else None
        
        video_plan.append({
            "scene_id": scene["id"],
            "narration": scene["narration"],
            "video_url": best_match["url"] if best_match else None,
            "similarity": best_match["score"] if best_match else 0,
            "duration": scene["duration"]
        })
    
    # 4. Save video plan
    with open(output_path, "w") as f:
        json.dump(video_plan, f, indent=2)
    
    return video_plan

# Usage
plan = generate_video_from_script("script.json", "video_plan.json")
print(f"Matched {len(plan)} scenes with avg similarity: {sum(s['similarity'] for s in plan) / len(plan):.2f}")
```

## Quality Metrics

### Relevance Score Interpretation

| Score | Meaning | Action |
|-------|---------|--------|
| 0.8+ | Excellent match | Use confidently |
| 0.6-0.8 | Good match | Review manually |
| 0.4-0.6 | Weak match | Consider alternatives |
| <0.4 | Poor match | Re-query or manual select |

### Benchmarking

```python
# Test matching quality
test_cases = [
    {"text": "AI healthcare", "expected": ["hospital", "medical", "doctor"]},
    {"text": "machine learning", "expected": ["code", "algorithm", "data"]},
    {"text": "climate change", "expected": ["environment", "nature", "pollution"]}
]

for case in test_cases:
    videos = matcher.find_matching_videos(case["text"], top_k=5)
    # Check if expected keywords appear in top results
    scores = matcher.evaluate_matches(videos, case["expected"])
    print(f"{case['text']}: {scores['precision']:.2f} precision")
```

## Integration with Other Skills

### Content Production Pipeline

1. `skill://content-planner-auto` → Generate script
2. **This skill** → Find matching footage
3. `skill://voice-chatterbox-tts` → Generate narration
4. `skill://remotion` → Compose video
5. `skill://video-editor` → Final polish

### YouTube Automation

1. `skill://larry-playbook` → Viral content strategy
2. `skill://content-generator` → Script generation
3. **This skill** → Semantic video matching
4. `skill://youtube-factory` → Upload & optimize

### Marketing Content

1. `skill://viral-marketing` → Campaign planning
2. **This skill** → Brand-relevant footage
3. `skill://content-factory` → Multi-platform adaptation
4. `skill://analytics-dashboard` → Performance tracking

## Troubleshooting

### Low similarity scores across all results

```python
# Try different model
matcher = VideoMatcher(model_name="all-mpnet-base-v2")

# Or expand query with synonyms
from semantic_video_matcher import expand_query
expanded = expand_query("AI healthcare")  # → ["artificial intelligence", "medical AI", "health technology"]
```

### API rate limits

```python
# Implement caching
matcher.enable_cache(cache_dir=".video_cache")

# Or batch requests
all_queries = [scene["text"] for scene in scenes]
results = matcher.batch_search(all_queries, delay=1.0)  # 1s between requests
```

### Irrelevant results

```python
# Use negative keywords
videos = matcher.find_matching_videos(
    text="AI in healthcare",
    exclude_keywords=["war", "violence", "politics"],
    min_similarity=0.7  # Raise threshold
)
```

## Performance

| Operation | Time (CPU) | Time (GPU) |
|-----------|------------|------------|
| Encode query | 50ms | 10ms |
| Search 10K videos | 200ms | 50ms |
| Thumbnail analysis | +500ms | +100ms |
| Full pipeline (5 scenes) | ~3s | ~1s |

**Optimization:**
- Cache embeddings: 10x faster repeated searches
- Batch processing: 3x faster for multiple queries
- GPU: 4-5x faster than CPU

## Verification Checklist

- [ ] sentence-transformers installed
- [ ] Test model loads successfully
- [ ] Pexels/Pixabay API key configured
- [ ] Basic text encoding works
- [ ] Video search returns results
- [ ] Similarity scores reasonable (>0.5 for relevant)
- [ ] Thumbnail analysis works (optional)

## Related Skills

- `skill://content-generator` — Script generation for videos
- `skill://voice-chatterbox-tts` — Narration audio
- `skill://remotion` — Video composition
- `skill://video-editor` — Video editing
- `skill://youtube-factory` — YouTube upload automation
- `skill://content-factory` — Multi-platform content

## Overview

> Section content — see SKILL.md body for full details.
