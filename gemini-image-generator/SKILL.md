# Gemini Image Generator Skill

## Overview

Generate professional posed product images using Gemini AI with optimized prompts for e-commerce and content creation.

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
