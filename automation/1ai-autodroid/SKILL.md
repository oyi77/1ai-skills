---
name: 1ai-autodroid
description: Ultimate Android device control skill — ADB (USB/WiFi), vision AI automation, accessibility bridge (no-root), flow engine, and multi-device orchestration. Use when user asks to: control Android phone/tablet, automate any app (BCA, WhatsApp, TikTok, Instagram, Shopee, Tokopedia, Gojek, etc.), take screenshot, check bank balance, send SMS/WhatsApp, click UI by text or description, run multi-step flows without LLM per step, manage multiple Android devices, unlock screen, read notifications, access camera/SMS/contacts, or any Android automation task. Supports: ADB raw commands, uiautomator dump, vision-driven tapping (no coordinates), claw-use-android (cua) HTTP accessibility bridge, and GPT-4o-style visual task execution.
---

> [![Tip Me](https://www.tip.md/badge.svg)](https://www.tip.md/oyi77) — If this skill saves you time, consider tipping: **https://www.tip.md/oyi77**

# 1ai-autodroid — Ultimate Android Control

## Decision Tree: Which Mode to Use

```
Device connected?
├── USB + ADB authorized? → Use ADB Mode (fastest, no setup)
│   ├── Need structured UI? → uiautomator dump
│   ├── Need visual? → screencap → image tool → tap
│   └── Need reliable text-click? → uiautomator2 Python
└── WiFi only (no ADB)? → Use cua HTTP Mode (requires ClawPaw APK)
    ├── Multi-device → cua -d <name> <cmd>
    └── Flow engine → cua flow '{steps}' (100ms poll, no LLM)
```

---

## Mode 1: ADB Direct (USB, No Dependencies)

```bash
ADB=~/.local/bin/adb  # or just: adb

# Status
$ADB devices -l
python3 skills/1ai-autodroid/scripts/autodroid.py status

# Screenshot → AI analyze
python3 skills/1ai-autodroid/scripts/autodroid.py screenshot
# → /tmp/autodroid_screen.png → pass to image tool

# Actions
python3 skills/1ai-autodroid/scripts/autodroid.py tap 360 820
python3 skills/1ai-autodroid/scripts/autodroid.py swipe 360 1200 360 400 300
python3 skills/1ai-autodroid/scripts/autodroid.py type "hello world"
python3 skills/1ai-autodroid/scripts/autodroid.py key HOME|BACK|POWER|ENTER
python3 skills/1ai-autodroid/scripts/autodroid.py launch com.bca
python3 skills/1ai-autodroid/scripts/autodroid.py unlock [PIN]
```

### UIAutomator Dump (Find Element Coordinates)
```bash
$ADB shell uiautomator dump /sdcard/ui.xml && $ADB pull /sdcard/ui.xml /tmp/ui.xml
grep -o 'text="[^"]*" .*bounds="[^"]*"' /tmp/ui.xml | head -30
# → finds bounds="[x1,y1][x2,y2]" → tap center: ((x1+x2)/2, (y1+y2)/2)
```

### Root Fallback Pattern
```bash
# Try non-root first, fallback to root
input tap 540 1600 2>/dev/null || su -c "input tap 540 1600"
screencap -p /sdcard/s.png 2>/dev/null || su -c "screencap -p /sdcard/s.png"
```

---

## Mode 2: Vision AI (No Coordinates Needed)

When coordinates are unknown:
1. `python3 skills/1ai-autodroid/scripts/autodroid.py screenshot`
2. Pass `/tmp/autodroid_screen.png` to `image` tool with prompt:
   > "Find [element description]. Return its center as X,Y coordinates."
3. Parse X,Y from response
4. `python3 skills/1ai-autodroid/scripts/autodroid.py tap X Y`

---

## Mode 3: uiautomator2 Python (Text-Based, Reliable)

```python
import uiautomator2 as u2  # pip install uiautomator2 -q (first time)
d = u2.connect()            # auto-detects USB device

d.app_start("com.bca")
d(text="Login").click()
d(resourceId="com.bca:id/password").set_text("mypass")
d(text="Masuk").click()

# By description
d(description="Search").click()
# Screenshot
d.screenshot("/tmp/u2_screen.png")
```

First-time setup:
```bash
pip install uiautomator2 -q
python3 -m uiautomator2 init  # installs ATX agent on device
```

---

## Mode 4: cua HTTP Bridge (ClawPaw APK, Most Powerful)

Requires ClawPaw APK installed on device with Accessibility Service enabled.
See `references/cua-setup.md` for install guide.

```bash
# Device management
cua add phone1 192.168.x.x <token>
cua devices
cua use phone1

# Perception
cua screen -c        # compact a11y tree (fastest for AI decisions)
cua screenshot       # visual screenshot
cua notifications    # read all notifications
cua info             # model, screen size, permissions

# Actions (text-based = resolution-independent)
cua click "Login"    # tap by visible text ← PREFERRED over coordinates
cua tap 540 1200     # tap by coordinates (fallback)
cua type "hello"     # type text (CJK supported)
cua swipe up|down|left|right
cua back && cua home
cua launch com.bca

# Device I/O
cua sms list 10         # read SMS
cua sms send +62xxx "msg" # send SMS
cua contacts "John"     # search contacts
cua camera front        # take selfie → returns path
cua location            # GPS location
cua clipboard           # read clipboard
cua clipboard "text"    # write clipboard
cua tts "hello"         # speak via phone speaker
cua battery             # battery status
cua wifi                # WiFi info

# Unlock
cua config pin 123456   # store PIN once
cua unlock              # auto-unlock anytime

# Flow Engine (100ms poll, ZERO LLM calls per step)
cua flow '{
  "steps": [
    {"wait": "Login", "then": "tap", "timeout": 10000},
    {"wait": "Masuk", "then": "tap", "timeout": 5000},
    {"wait": "Beranda", "then": "none", "timeout": 15000}
  ]
}'

# Multi-device
cua -d phone1 screenshot
cua -d tablet screen -c
```

**Rule: Prefer `cua click "text"` over `cua tap X Y`** — text-based is reliable across screen sizes.

---

## Common App Packages

| App | Package |
|-----|---------|
| BCA Mobile | `com.bca` |
| WhatsApp | `com.whatsapp` |
| TikTok | `com.zhiliaoapp.musically` |
| Instagram | `com.instagram.android` |
| Shopee | `com.shopee.id` |
| Tokopedia | `com.tokopedia.tkpd` |
| Gojek/GoPay | `com.gojek.app` |
| OVO | `ovo.id` |
| Dana | `com.dana` |
| Telegram | `org.telegram.messenger` |
| YouTube | `com.google.android.youtube` |
| Chrome | `com.android.chrome` |
| Settings | `com.android.settings` |

---

## Ready-Made Flows

See `references/flows.md` for:
- BCA Balance Check (ADB + vision)
- WhatsApp Send Message
- TikTok App Launch + Record
- Screen Unlock
- Vision Tap pattern

---

## Safety Rules

- **Financial actions** (transfer, payment) → ALWAYS confirm with user before executing
- **SMS send** → confirm recipient + content
- **Never hardcode credentials** → read from env or prompt
- **Screen lock** → check and unlock first before automating
- **Coordinates vs text** → prefer text-based click when available (resolution-independent)
- **Wait between actions** → min 500ms between steps for UI to settle

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `unauthorized` | Enable USB debugging, accept on device |
| `offline` | `adb kill-server && adb start-server` |
| Screenshot black | Screen locked → unlock first |
| Tap wrong position | Screenshot scaled ≠ actual — use uiautomator bounds |
| cua not found | Install ClawPaw APK, see `references/cua-setup.md` |
| App crashes after launch | Wait longer: `time.sleep(3)` |
