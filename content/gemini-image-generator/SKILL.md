---
name: gemini-image-generator
description: Use when generating professional posed product images for e-commerce using Gemini AI with optimized prompts
persona:
  name: "Ansel Adams"
  title: "Master of Visual Composition"
  expertise: ["lighting mastery", "golden hour timing", "composition mathematics", "technical precision"]
  philosophy: "You don't take a photograph, you make it."
  credentials:
    - "Developed the Zone System for precise exposure control"
    - "Yosemite National Park's most celebrated photographer"
    - "National Medal of Arts recipient from President Jimmy Carter"
    - "Co-founded Group f/64 defining purist photography"
  principles:
    - "Lighting is everything - approach light as a sculptor approaches clay"
    - "Composition is mathematics - apply the rule of thirds and golden ratio"
    - "Timing is non-negotiable - wait for the perfect golden hour"
    - "Technical precision first - master ISO, aperture, shutter speed trios"
    - "Every image tells a story - don't just document, narrate visually"
    - "Simplicity creates impact - remove distracting elements ruthlessly"
    - "Technical limitations define creativity - work within constraints to innovate"
---

# Gemini Image Generator Skill

## Overview

Generate professional posed product images using Gemini AI with optimized prompts for e-commerce and content creation.

## When to Use

- When you need to create product images with model poses for e-commerce
- When preparing TikTok/social media content featuring products
- When you have product images and need them "modeled" without hiring photographers
- When batch-generating multiple product variations

## When NOT to Use

- When you need photorealistic human faces (AI limitations)
- When legal compliance requires real photography
- When the product requires accurate color representation (AI may shift colors)
- When generating trademarked brand items

## Quick Reference

```bash
# Generate prompt
python prompt_optimizer.py --category fashion --product "white dress"

# Full workflow
python workflow_runner.py --pose pose.jpg --product dress.jpg --category fashion
```

## Common Mistakes

- Using low-resolution input images (results will be blurry)
- Not specifying lighting setup in prompts (inconsistent results)
- Skipping the ChatGPT video step (misses viral content optimization)
- Ignoring TikTok AI disclosure requirements

## Workflow

```
Input: Pose Model + Product Image
    ↓
Gemini Link (c7150b8213a4) → AI Image Generation
    ↓
Output: Multiple Posed Product Images
    ↓
ChatGPT → Video Scene Generation
    ↓
TikTok Content (compliant)
```

## Quick Start

### 1. Prepare Images
- **Pose Model**: Reference pose image (person/model)
- **Product**: Product image to integrate
- **Format**: JPG/PNG, any size (Rasio 9:16 recommended)

### 2. Generate Instruction

Use the prompt optimizer:
```python
python prompt_optimizer.py --category fashion --style minimal --product "white dress"
```

### 3. Run in Gemini

1. Open: https://gemini.google.com/share/c7150b8213a4
2. Upload pose model image
3. Upload product image
4. Paste generated instruction
5. Generate images

### 4. Download Results
- Gemini generates 4-8 variations
- Download all to output folder
- Next: Send to ChatGPT for video scenes

## Usage

### Command Line
```bash
# Generate instruction only
python prompt_optimizer.py --category fashion --product "summer dress"

# Full workflow (with browser automation)
python workflow_runner.py --pose pose.jpg --product dress.jpg --category fashion
```

### Python API
```python
from prompt_optimizer import generate_instruction

instruction = generate_instruction(
    category="fashion",
    product_name="summer dress",
    style="minimal",
    lighting="soft"
)
print(instruction)
```

## Categories

Available templates:
- `fashion` - Clothing, accessories
- `electronics` - Gadgets, devices
- `food` - Culinary, beverages
- `beauty` - Cosmetics, skincare
- `home` - Furniture, decor

## Output Format

**REFINER PRODUKSI Template:**
```
REFINER PRODUKSI: [Environment] | Rasio: 9:16 | Lighting: [Setup] | Intruksi tambahan: [Detail]
```

## Configuration

Edit `config.yaml`:
```yaml
gemini:
  shared_link: "https://gemini.google.com/share/c7150b8213a4"
  output_ratio: "9:16"
  
categories:
  fashion:
    environments: ["clean white studio", "minimal gray", "premium lifestyle"]
    lighting: ["soft diffused", "studio lighting", "natural daylight"]
    
defaults:
  ratio: "9:16"
  style: "premium"
  lighting: "soft diffused"
```

## Integration

### Next Step: ChatGPT Video Generation
Send Gemini output to ChatGPT with:
```
Generate video scene descriptions from these images. 
Style: TikTok viral, 15-30 seconds, hook in first 3 seconds.
```

### TikTok Compliance
- Disclosure: "AI-generated content"
- Label videos appropriately
- Follow community guidelines

## Files

- `SKILL.md` - This documentation
- `prompt_optimizer.py` - Generate optimal prompts
- `browser_helper.py` - Browser automation
- `workflow_runner.py` - Full pipeline
- `config.yaml` - Configuration
- `templates/` - Category templates

## License

MIT - Free for personal and commercial use.
