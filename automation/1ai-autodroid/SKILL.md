---
name: 1ai-autodroid
description: Full Android device control via ADB (USB/WiFi) + AI vision automation. Control real Android phones without root — screenshot, tap, swipe, type, open apps, read screen with uiautomator2, and run vision-driven automation (no DOM/accessibility labels needed). Use when user asks to: control Android phone, automate apps (BCA, WhatsApp, TikTok, etc.), take screenshot from phone, check bank balance via mobile app, send messages, click UI elements by description, or run any Android automation flow. Works with USB-connected devices (ADB authorized) and WiFi ADB. Combines best of android-adb (uiautomator), midscene-android-automation (vision), and claw-use-android (HTTP+CLI).
---

# 1ai-autodroid — Android AI Control

## Quick Start

```bash
# Check device connection
~/.local/bin/adb devices -l

# Screenshot
~/.local/bin/adb shell screencap /sdcard/screen.png
~/.local/bin/adb pull /sdcard/screen.png /tmp/screen.png

# Tap by coordinates
~/.local/bin/adb shell input tap X Y

# Swipe
~/.local/bin/adb shell input swipe x1 y1 x2 y2 300

# Type text
~/.local/bin/adb shell input text "hello"

# Press key
~/.local/bin/adb shell input keyevent 3   # HOME
~/.local/bin/adb shell input keyevent 4   # BACK
~/.local/bin/adb shell input keyevent 26  # POWER

# Open app by package
~/.local/bin/adb shell monkey -p com.bca -c android.intent.category.LAUNCHER 1
~/.local/bin/adb shell monkey -p com.whatsapp -c android.intent.category.LAUNCHER 1
```

---

## Core Workflow (Standard Flow)

1. **Screencap** → pull to `/tmp/screen.png`
2. **Analyze screenshot** → use `image` tool to identify UI elements + coordinates
3. **Execute action** → tap/swipe/type via ADB
4. **Repeat** until task complete
5. **Report** result to user

```bash
# Step 1+2 combined helper:
python3 skills/1ai-autodroid/scripts/autodroid.py screenshot
# → saves /tmp/autodroid_screen.png, prints coordinates guide

# Step 3: tap by vision description
python3 skills/1ai-autodroid/scripts/autodroid.py tap-vision "tombol login"
# → takes screenshot, uses AI to find element, taps it
```

---

## Vision Mode (AI-Driven, No Coordinates)

When you don't know the coordinates, use **vision mode**:

1. Take screenshot
2. Call `image` tool with prompt: `"Find the element: [description]. Return its center coordinates as X,Y"`
3. Parse response → extract X,Y
4. Execute ADB tap

This works for ANY app without needing app source code or accessibility labels.

---

## UIAutomator2 Mode (Structured UI)

For reliable, coordinate-independent automation:

```bash
# Install uiautomator2 on device (first time only)
pip install uiautomator2 -q
python3 -c "import uiautomator2 as u2; d = u2.connect(); d.app_start('com.bca')"

# Find element by text
python3 -c "
import uiautomator2 as u2
d = u2.connect()
d(text='Login').click()
d(resourceId='com.bca:id/password').set_text('mypassword')
d(text='Masuk').click()
"
```

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
| GoPay/Gojek | `com.gojek.app` |
| OVO | `ovo.id` |
| Dana | `com.dana` |

---

## Automation Flows

See `references/flows.md` for ready-to-use flows:
- BCA Balance Check
- WhatsApp Send Message
- TikTok Post Video
- Screenshot → OCR → Extract data

---

## ADB Path

```bash
ADB=~/.local/bin/adb   # installed this session
# OR if in PATH: adb
```

Add to `.bashrc`:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

---

## WiFi ADB (Wireless)

```bash
# Connect phone to same WiFi as server first
# Then enable WiFi debugging (Android 11+: no USB needed)
adb tcpip 5555
adb connect <PHONE_IP>:5555
adb devices  # verify connected
```

---

## Constraints & Safety

- **Never hardcode credentials** in scripts — always read from env or prompt
- **Confirm before sending payments** — any financial action requires explicit user approval
- **Screen may lock** — check if locked, unlock before automating:
  ```bash
  adb shell dumpsys window | grep mCurrentFocus
  # If "StatusBar" or "Keyguard" → screen locked
  adb shell input keyevent 82  # MENU = unlock
  ```
- **Rotation** — some apps respond to orientation:
  ```bash
  adb shell settings put system accelerometer_rotation 0
  adb shell settings put system user_rotation 0  # portrait
  ```
