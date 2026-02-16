# Gemini Image Generator Skill

Quick reference for generating posed product images.

## Quick Start

### 1. Generate Instruction

```bash
# Fashion product
python prompt_optimizer.py --category fashion --product "white dress"

# Electronics
python prompt_optimizer.py --category electronics --product "wireless earbuds"

# Food  
python prompt_optimizer.py --category food --product "organic coffee"
```

### 2. Use in Gemini

1. Open: https://gemini.google.com/share/c7150b8213a4
2. Upload **pose model image**
3. Upload **product image**
4. Paste instruction
5. Generate

### 3. Workflow Automation

```bash
# Single image
python workflow_runner.py --pose model.jpg --product item.jpg -c fashion -n "Product Name"

# Batch process all in folder
python workflow_runner.py --batch -c fashion

# List pending jobs
python workflow_runner.py --list
```

## Categories

- `fashion` - Clothing, apparel, accessories
- `electronics` - Gadgets, devices, tech
- `food` - Culinary, beverages, ingredients  
- `beauty` - Cosmetics, skincare
- `home` - Furniture, decor, lifestyle

## Folder Structure

```
gemini-image-generator/
├── input/          # Place images here
├── output/         # Generated instructions saved here
├── templates/      # Category templates
├── prompt_optimizer.py
├── workflow_runner.py
├── config.yaml
└── SKILL.md
```

## Next Step

After Gemini generates images:
1. Download all variations
2. Send to ChatGPT for video scene generation
3. Create TikTok content (use AI disclosure)

---
**Link**: https://gemini.google.com/share/c7150b8213a4
