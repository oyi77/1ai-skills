# 🔥 AutoDroid Suite — Complete Android Automation

**Full-stack Android automation across 9 major platforms + device control + orchestrator.**

> Tested on Android 14 (Redmi 2409BRN2CY). **Production-ready.** **85+ commands.** **Zero dependencies** (pure Python).

---

## ⚡ Quick Start (2 minutes)

### 1️⃣ **Verify ADB is installed**
```bash
adb version  # should print version
adb devices   # should show connected device(s)
```

### 2️⃣ **Start Dashboard (Master Control)**
```bash
python3 autodroid-dashboard/scripts/autodroid_dashboard.py
# Opens: http://localhost:8800
```

### 3️⃣ **Click "Start All Agents" in Dashboard**
All 9 agents + services start automatically on ports 8765–8773.

### 4️⃣ **Test an Agent**
```bash
# In terminal or via curl:
curl -X POST http://localhost:8765/api/gemini/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello Gemini"}'

# Response:
{
  "ok": true,
  "response": "Hello! I'm Gemini...",
  "screenshot_path": "/path/to/screenshot.png"
}
```

---

## 📋 What's Included

### **9 Agent APIs** (REST + CLI)
```
Port 8765 → Gemini      (chat ✅, imagine ✅)
Port 8766 → TikTok      (upload, like, follow, etc.)
Port 8767 → Shopee      (search, buy, reviews, etc.)
Port 8768 → WhatsApp    (send, broadcast, etc.)
Port 8769 → Instagram   (post, like, follow, etc.)
Port 8770 → YouTube     (subscribe, like, comment, etc.)
Port 8771 → PlayStore   (install, uninstall, etc.)
Port 8772 → Device      (wifi, brightness, gps, etc. — pending)
Port 8773 → Grok        (chat ✅, imagine ✅)
Port 8800 → Dashboard   (orchestrator + UI)
```

### **85+ Commands**
- **Gemini**: 6 (chat, imagine, screenshot, status, open, server)
- **Grok**: 8 (chat, imagine, screenshot, status, open, scroll, server, login)
- **TikTok**: 15+ (upload, like, comment, follow, search, scroll, browse, etc.)
- **Instagram**: 16+ (post, like, comment, follow, dm, scroll, scroll-reels, etc.)
- **WhatsApp**: 14+ (send, broadcast, verify-otp, scroll-chat, etc.)
- **YouTube**: 12+ (subscribe, like, comment, play, search, etc.)
- **Shopee**: 14+ (search, product, cart, orders, reviews, etc.)
- **PlayStore**: 3 (install, search, uninstall)

---

## 🚀 Usage Modes

### **Mode 1: CLI (Direct)**
```bash
# Single command
python3 autodroid-gemini-agent/scripts/gemini_agent.py chat --prompt "test"

# Output:
{
  "ok": true,
  "response": "...",
  "attempt": 1
}
```

### **Mode 2: HTTP API (FastAPI)**
```bash
# Start server
python3 autodroid-gemini-agent/scripts/gemini_agent.py server
# Or:
python3 autodroid-gemini-agent/gemini_server.py

# Call via HTTP
curl -X POST http://localhost:8765/api/gemini/chat \
  -d '{"prompt": "test"}'
```

### **Mode 3: Dashboard (Web UI)**
```bash
# Master control panel
python3 autodroid-dashboard/scripts/autodroid_dashboard.py

# View: http://localhost:8800
# Features:
# - Start/stop/restart agents
# - Test endpoints in-dashboard
# - Real-time status
```

---

## 💡 Common Workflows

### **A. Content Generation (AI Images)**
```bash
# Generate 5 images with Gemini + Grok
python3 autodroid-gemini-agent/scripts/gemini_agent.py imagine --prompt "sunset mountain"
python3 autodroid-grok-agent/scripts/grok_agent.py imagine --prompt "sunset mountain"
```

### **B. Social Media Posting**
```bash
# Generate image + post to Instagram
python3 autodroid-gemini-agent/scripts/gemini_agent.py imagine --prompt "product photo"
# (saves to ~/.openclaw/workspace/downloads/grok_imagine_*.png)

python3 autodroid-instagram-agent/scripts/instagram_agent.py post \
  --caption "Check this out!" \
  --image /path/to/image.jpg
```

### **C. Multi-Platform Broadcasting**
```bash
# Broadcast to TikTok + Instagram + YouTube simultaneously
# (via dashboard "Start All" → manually trigger each)
```

### **D. Bot Automation (WhatsApp)**
```bash
# Send message to 50+ contacts
python3 autodroid-whatsapp-agent/scripts/whatsapp_agent.py broadcast \
  --phones "+62812345678,+62812345679,..." \
  --message "Hello from automation!"
```

---

## 🔧 Configuration

### **Multi-Device Support**
```bash
# List connected devices
adb devices
SGZTONV4OBL74TJZ         device
192.168.1.100:5555       device

# Run on specific device
python3 gemini_agent.py chat --prompt "test" --device SGZTONV4OBL74TJZ

# Or environment variable
export ANDROID_SERIAL="192.168.1.100:5555"
python3 gemini_agent.py chat --prompt "test"
```

### **Customize Timeouts**
```bash
# Default: 30s for chat, 60s for images
python3 gemini_agent.py chat --prompt "test" --timeout 60

# Long-running operations
python3 tiktok_agent.py upload --video /path/to/video.mp4 --timeout 300
```

### **Customize Keyboard (Fix Autocorrect)**
```bash
# If text input corrupted by keyboard predictive text:
adb shell settings set secure default_input_method \
  com.preff.kb.xm/com.preff.kb.LatinIME
# (Switch to Xiaomi keyboard, more reliable)
```

---

## 📊 Architecture

### **Agent Design Pattern**
```
[CLI/HTTP Request]
    ↓
[Agent Script (1000-1700 lines)]
    ├─ Parse arguments
    ├─ Initialize ADB connection
    ├─ Handle auth (login if needed)
    ├─ Execute command
    │  ├─ Screenshot
    │  ├─ Find UI element
    │  ├─ Tap/Type/Scroll
    │  ├─ Wait for response
    └─ Return JSON result
        ↓
[Screenshot + Data]
```

### **Shared Components (Duplicated per Agent)**
Each agent includes:
- **ADB wrapper** (`adb()`) — execute shell commands with retry logic
- **UI automation** (`find_node()`, `tap()`, `type_in_field()`) — element detection + interaction
- **Screenshot** (`screencap()`, `dump_ui()`) — screen capture + XML parsing
- **Natural behavior** (`natural_swipe()`, `natural_pause()`) — randomized delays/speed

### **Why Duplicated?**
- **Zero dependencies** — pure Python, no shared packages
- **Reliability** — each agent can run independently
- **Isolation** — agent failure doesn't affect others
- **Customization** — easy to modify per-agent behavior

---

## 🧪 Testing

### **Smoke Test (All Agents)**
```bash
#!/bin/bash
for port in 8765 8766 8767 8768 8769 8770 8771 8773; do
  echo "Testing port $port..."
  curl -s http://localhost:$port/health | jq '.'
done
```

### **Integration Test (Full Flow)**
```bash
# 1. Chat with Gemini
python3 autodroid-gemini-agent/scripts/gemini_agent.py \
  chat --prompt "Generate sunset image description"

# 2. Generate image
python3 autodroid-gemini-agent/scripts/gemini_agent.py \
  imagine --prompt "beautiful sunset over mountain"

# 3. Post to Instagram
python3 autodroid-instagram-agent/scripts/instagram_agent.py \
  post --caption "Sunset vibes" --image /path/to/image.jpg

# 4. Verify in Dashboard
curl http://localhost:8800/api/status | jq '.agents'
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `adb: command not found` | Install Android SDK Platform Tools |
| `Device not found` | Run `adb devices`, ensure device is connected/authorized |
| `Permission denied` | Enable USB debugging + authorize connection on device |
| `Timeout during operation` | Increase `--timeout N` or reduce device load |
| `Text input corrupted` | Switch keyboard: `adb shell settings set secure default_input_method com.preff.kb.xm/com.preff.kb.LatinIME` |
| `Instagram post failed` | Ensure image media included (`--image /path/to/image.jpg`) |
| `WhatsApp OTP not received` | Phone number format must be `+62...` (international) |

---

## 📈 Performance Tips

### **Reduce Latency**
```bash
# Disable animations (Developer Options → Animation scale = 0)
adb shell settings put global animator_duration_scale 0

# Use local TCP instead of USB
adb connect 192.168.1.100:5555

# Run agents in parallel (separate terminals)
python3 gemini_agent.py imagine --prompt "test1" &
python3 grok_agent.py imagine --prompt "test2" &
wait
```

### **Increase Reliability**
```bash
# Agents default to 3x retry with exponential backoff
# For critical operations, increase timeout
python3 tiktok_agent.py upload --timeout 600  # 10 minutes
```

---

## 📦 Deployment Options

### **Option 1: Local (Recommended)**
```bash
# Run on same machine as Android device (USB) or same network (ADB TCP)
python3 autodroid-dashboard/scripts/autodroid_dashboard.py
```

### **Option 2: Server (Single Machine)**
```bash
# Run agents as systemd services
# Create /etc/systemd/system/autodroid-dashboard.service:
[Unit]
Description=AutoDroid Dashboard
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/autodroid
ExecStart=/usr/bin/python3 autodroid-dashboard/scripts/autodroid_dashboard.py
Restart=always

[Install]
WantedBy=multi-user.target

# Start:
sudo systemctl start autodroid-dashboard
sudo systemctl enable autodroid-dashboard
```

### **Option 3: Docker**
```dockerfile
FROM python:3.9-slim
RUN apt-get update && apt-get install -y android-tools-adb
COPY . /app
WORKDIR /app
EXPOSE 8765-8800
CMD ["python3", "autodroid-dashboard/scripts/autodroid_dashboard.py"]
```

### **Option 4: Kubernetes (Not Recommended)**
❌ Kubernetes is unsuitable — requires persistent device connection.
Use **Option 1** (local) or **Option 2** (server) instead.

---

## 🔐 Security Considerations

### **Credentials**
- **Stored locally only** on Android device
- Never transmitted to external services
- No cloud sync or logging

### **Data Privacy**
- Screenshots cached in `~/.openclaw/workspace/downloads/`
- Delete after use if sensitive
- No personal data collected

### **Network Security**
- Dashboard/APIs listen on `localhost:8000-8800` by default
- **NOT exposed to internet** (unless explicitly configured)
- Use firewall to restrict access if needed

---

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| `SKILL.md` | Complete API reference + all commands |
| `README.md` | This file — quick start + overview |
| `autodroid-{agent}-agent/SKILL.md` | Agent-specific docs |
| `autodroid-{agent}-agent/references/` | UI coordinate maps + notes |

---

## 💬 Examples

### **Chat with Gemini**
```bash
python3 autodroid-gemini-agent/scripts/gemini_agent.py \
  chat --prompt "What is Python?" --timeout 30
```

### **Generate Image with Grok**
```bash
python3 autodroid-grok-agent/scripts/grok_agent.py \
  imagine --prompt "cat playing piano, cartoon style" --timeout 90
```

### **Post to Instagram**
```bash
python3 autodroid-instagram-agent/scripts/instagram_agent.py \
  post \
  --caption "My awesome post! #viral #trending" \
  --image /path/to/image.jpg
```

### **Auto-Install App**
```bash
python3 autodroid-playstore-agent/scripts/playstore_agent.py \
  install --app Instagram --timeout 120
```

### **Broadcast WhatsApp Message**
```bash
python3 autodroid-whatsapp-agent/scripts/whatsapp_agent.py \
  broadcast \
  --phones "+62812345678,+62812345679,+62812345680" \
  --message "Hello everyone!"
```

---

## 🎯 Next Steps

1. **Start Dashboard**: `python3 autodroid-dashboard/scripts/autodroid_dashboard.py`
2. **Click "Start All"** to launch all agents
3. **Test via Dashboard** UI or curl commands
4. **Customize** agents as needed (add new commands, adjust timeouts, etc.)
5. **Deploy** to production (server/docker if needed)

---

## 📞 Support

- **Issues?** Check the troubleshooting section above
- **ADB not working?** Verify with `adb devices`
- **Agent crashing?** Run with stderr: `python3 agent.py command 2>&1 | head -50`
- **Need modifications?** Edit agent script directly (self-contained, no dependencies)

---

**Version:** 1.0 (Production Ready)  
**Last Updated:** 2026-03-21  
**Total Agents:** 9 + Device + Dashboard  
**Total Commands:** 85+  
**Device Tested:** Redmi 2409BRN2CY (Android 14, 720x1640)
