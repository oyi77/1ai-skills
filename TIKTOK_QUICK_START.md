# TIKTOK QUICK START GUIDE

## Prerequisites
- TikTok account with active session
- TikTok username & password

## Step 1: Setup Credentials (5 minutes)

```bash
cd ~/.openclaw/workspace/skills/tiktok-automation

# Edit config.json
nano config.json
```

Add your credentials:
```json
{
  "credentials": {
    "username": "YOUR_USERNAME",
    "password": "YOUR_PASSWORD",
    "sessionFile": "tiktok-session.json"
  },
  "upload": {
    "defaultPrivacy": "public",
    "allowComments": true,
    "allowDuet": true,
    "allowStitch": true
  },
  "browser": {
    "headless": false,  // Set to true for production
    "timeout": 30000
  }
}
```

Save and exit (Ctrl+X, Y, Enter).

## Step 2: Test Manual Login (5 minutes)

Run the automation skill to test login:

```bash
# From tiktok-automation directory
./script.sh --video assets/sample-video.mp4 --caption "Test post"
```

Watch the browser open, login automatically, and verify everything works.

## Step 3: Generate Real Images (1-2 hours)

Option A: Use PIL (Python Image Library)

```bash
cd ~/.openclaw/workspace

# Create image generation script
cat scripts/generate_images_pil.py <<'EOF'
from PIL import Image, ImageDraw, ImageFont
import json
import os

# Load configs
config_dir = "generated_posts/visuals"
output_dir = "generated_posts/images"
os.makedirs(output_dir, exist_ok=True)

# Get all configs
configs = []
for filename in os.listdir(config_dir):
    if filename.endswith('.json'):
        with open(os.path.join(config_dir, filename)) as f:
            configs.append(json.load(f))

# Generate images
for config in configs:
    # Create image
    img = Image.new('RGB', (1080, 1350), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw text
    # ... PIL drawing code here ...
    
    # Save
    output_filename = filename.replace('.json', '.png')
    img.save(os.path.join(output_dir, output_filename))
    print(f"Generated: {output_filename}")

print(f"✅ Generated {len(configs)} images")
EOF

# Run it
python3 scripts/generate_images_pil.py
```

Option B: Manual Batch Generation (Faster)

Use batch image generation tools like:
- Canva Batch Create
- Adobe Photoshop Batch
- Online batch tools

Apply the visual configs to create 156 PNG images.

## Step 4: Run First Campaign (2-3 hours)

```bash
cd ~/.openclaw/workspace

# Test with 3 posts first
python3 scripts/multi_platform_poster.py --posts 3 --tiktok-only

# If successful, scale up
python3 scripts/multi_platform_poster.py --posts 10 --tiktok-only
```

Monitor the posts on TikTok, check performance in LYNK dashboard.

## Step 5: Scale to Full Automation (1-2 hours)

Once TikTok is working, scale to full posting:

```bash
# 18 posts/day (TikTok only)
python3 scripts/multi_platform_poster.py --posts 18 --tiktok-only

# Full multi-platform (54 posts/day)
python3 scripts/multi_platform_poster.py --posts 18
```

## Step 6: Launch Daemonic Execution

```bash
# Start continuous daemon
python3 scripts/multi_platform_poster.py --daemon

# Start LYNK monitor
python3 scripts/lynk_monitor.py --daemon --interval 60

# Revenue gap detector is already running via cron
```

---

## Troubleshooting

### Login Failed
- Check username/password in config.json
- Clear session: `rm tiktok-session.json`
- Try login manually first, then run automation

### Upload Failed
- Check video format (MP4, MOV)
- Verify file size < 287.6 MB
- Check internet connection

### TikTok Changed UI
- Run with `--update-selectors` flag to re-learn selectors

---

**Quick Setup Time:** 30 minutes → Test → 2-3 hours → Revenue in 24-72 hours

🔥