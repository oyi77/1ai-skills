# TikTok Automation Skill 🎵

**Production-ready** automation untuk TikTok content posting & management.

## 🎯 Features

- **Auto-login** dengan session persistence
- **Content upload** (video, caption, hashtags)
- **Dynamic element detection** - adaptif terhadap class name changes
- **Selector learning** - save successful selectors ke `selectors.json`
- **Fallback mechanism** - retry dengan alternative selectors
- **Progress tracking** - real-time status updates

## 📦 Files

```
tiktok-automation/
├── SKILL.md              # This file
├── script.sh             # Main automation (cross-platform)
├── script.ps1            # Windows PowerShell version
├── selectors.json        # Learned element selectors
├── config.json           # Configuration (credentials, settings)
└── assets/
    └── sample-video.mp4  # Test video
```

## 🔧 Setup

### 1. Configure Credentials

Edit `config.json`:
```json
{
  "credentials": {
    "username": "your-tiktok-username",
    "password": "your-password",
    "sessionFile": "tiktok-session.json"
  },
  "upload": {
    "defaultPrivacy": "public",
    "allowComments": true,
    "allowDuet": true,
    "allowStitch": true
  },
  "browser": {
    "headless": false,
    "timeout": 30000
  }
}
```

### 2. Run the Skill

```bash
# Basic upload (Linux/macOS)
./script.sh --video path/to/video.mp4 --caption "My video"

# With hashtags
./script.sh --video path/to/video.mp4 --caption "Check this" --tags "#viral #fyp"

# Update selectors (re-learning mode)
./script.sh --update-selectors
```

**Windows (PowerShell):**
```powershell
.\script.ps1 -Video "path\to\video.mp4" -Caption "My video"
```

## 🔄 How It Works

### Flow:
1. **Load session** - Check for existing TikTok session
2. **Login if needed** - Auto-login with credentials
3. **Navigate to upload** - Go to upload page
4. **Dynamic detection** - Find upload button using multiple strategies:
   - Try learned selectors from `selectors.json`
   - Fallback to text/role-based detection
   - Fallback to structure-based detection
5. **Upload video** - Drag & drop or file input
6. **Add metadata** - Caption, hashtags, settings
7. **Publish** - Submit and confirm
8. **Save selectors** - Update `selectors.json` with successful selectors

### Selector Learning:

Every successful element interaction is saved:
```json
{
  "uploadButton": {
    "selector": "[data-e2e='upload-btn']",
    "method": "dataAttribute",
    "confidence": 1.0,
    "lastUsed": "2026-02-18T22:00:00Z",
    "fallbacks": [
      {"selector": "button[type='file']", "method": "css"},
      {"text": "Upload", "method": "text"}
    ]
  }
}
```

## 🛠️ Troubleshooting

### TikTok Changed Their UI Again?

Run with `--update-selectors` flag to re-learn element locations.

### Login Failed?

- Check credentials in `config.json`
- Clear session file: delete `tiktok-session.json`
- Try manual login first, then run skill

### Upload Stuck?

- Check video format (MP4, MOV, WebM)
- Ensure file size < 287.6 MB
- Verify internet connection

## 📊 Logs

All actions logged to:
- Console output (real-time)
- `tiktok-automation.log` (persistent)

## ⚠️ Warnings

- **Rate limiting**: Don't upload too frequently (max 10 videos/hour)
- **Terms of Service**: Use responsibly, follow TikTok's ToS
- **Account safety**: Consider using a burner account for automation

## 🚀 Next Steps

Planned improvements:
- [ ] Schedule posts for optimal timing
- [ ] Analytics tracking (views, likes, shares)
- [ ] Bulk upload from folder
- [ ] Auto-generate captions with AI
- [ ] Cross-post to Instagram Reels & YouTube Shorts

---
**Berkah Karya** ⚡ | Part of 1ai-skills collection
