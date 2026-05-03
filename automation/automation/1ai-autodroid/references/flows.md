# AutoDroid Flows — Ready-to-Use Automation Recipes

## Flow 1: BCA Balance Check (ADB + Vision)

```python
# Usage: python3 skills/1ai-autodroid/scripts/autodroid.py launch com.bca
# Then: screenshot → image tool → read balance

import subprocess, time, os
ADB = os.path.expanduser("~/.local/bin/adb")

def run(cmd): return subprocess.run(f"{ADB} {cmd}", shell=True, capture_output=True, text=True).stdout

# 1. Launch BCA
run("shell monkey -p com.bca -c android.intent.category.LAUNCHER 1")
time.sleep(4)
# 2. Screenshot
run("shell screencap /sdcard/bca1.png") ; run("pull /sdcard/bca1.png /tmp/bca1.png")
print("Pass /tmp/bca1.png to image tool to read login screen")
# 3. Find PIN pad via uiautomator → tap PIN → screenshot balance page
```

**cua alternative (faster):**
```bash
cua launch com.bca
sleep 4
cua screen -c         # read login UI structure
cua click "m-BCA"     # or relevant text
cua flow '{
  "steps": [
    {"wait": "m-BCA", "then": "tap", "timeout": 10000},
    {"wait": "Beranda", "then": "none", "timeout": 15000}
  ]
}'
cua screenshot        # capture balance screen
```

---

## Flow 2: WhatsApp Send Message

**ADB Intent (no app interaction):**
```bash
adb shell am start -a android.intent.action.VIEW \
  -d "https://api.whatsapp.com/send?phone=628xxxxxxx&text=Halo%20dari%20AI" \
  com.whatsapp
sleep 2
# Tap Send button (find via vision or uiautomator)
python3 skills/1ai-autodroid/scripts/autodroid.py tap-text "Send"
```

**cua alternative:**
```bash
cua launch com.whatsapp
cua click "Search"
cua type "John"
sleep 1
cua click "John"
cua type "Hello from AI"
cua click "Send"
```

**cua SMS (no WhatsApp needed):**
```bash
cua sms send +628xxxxxxx "Hello from AI"
```

---

## Flow 3: Screenshot → OCR → Extract Data

```python
import subprocess, os
ADB = os.path.expanduser("~/.local/bin/adb")

def capture(save_path="/tmp/autodroid_screen.png"):
    subprocess.run(f"{ADB} shell screencap /sdcard/auto_cap.png", shell=True)
    subprocess.run(f"{ADB} pull /sdcard/auto_cap.png {save_path}", shell=True)
    return save_path

# Usage flow:
# 1. path = capture()
# 2. result = image(path, "Extract all text from this screenshot. Return as JSON.")
# 3. Parse result for: balance, name, transaction, etc.
```

---

## Flow 4: Smart App Automation (Vision Mode)

```python
import subprocess, os, re
ADB = os.path.expanduser("~/.local/bin/adb")

def tap(x, y):
    subprocess.run(f"{ADB} shell input tap {x} {y}", shell=True)

def capture(path="/tmp/autodroid_screen.png"):
    subprocess.run(f"{ADB} shell screencap /sdcard/cap.png && {ADB} pull /sdcard/cap.png {path}", shell=True)
    return path

def parse_xy(ai_response):
    m = re.search(r'(\d+)\s*[,x]\s*(\d+)', ai_response)
    return (int(m.group(1)), int(m.group(2))) if m else (None, None)

# Example:
# img = capture()
# response = image(img, "Find the 'Login' button. Return center as X,Y.")
# x, y = parse_xy(response)
# if x: tap(x, y)
```

---

## Flow 5: Screen Unlock

```python
import subprocess, os, time
ADB = os.path.expanduser("~/.local/bin/adb")

def is_locked():
    out = subprocess.run(f"{ADB} shell dumpsys window | grep mCurrentFocus",
                        shell=True, capture_output=True, text=True).stdout
    return "StatusBar" in out or "Keyguard" in out

def unlock(pin=None):
    subprocess.run(f"{ADB} shell input keyevent 26", shell=True)  # wake
    time.sleep(0.5)
    subprocess.run(f"{ADB} shell input keyevent 82", shell=True)  # unlock
    time.sleep(0.5)
    if pin:
        subprocess.run(f"{ADB} shell input text {pin}", shell=True)
        subprocess.run(f"{ADB} shell input keyevent 66", shell=True)  # ENTER

if is_locked():
    unlock("123456")
```

---

## Flow 6: TikTok Video Upload

```bash
# Via ADB intent: open TikTok upload screen
adb shell am start -n com.zhiliaoapp.musically/.main.activity.VideoUploadActivity

# Or via cua:
cua launch com.zhiliaoapp.musically
sleep 3
cua click "+"       # tap record/upload button
cua click "Upload"  # select upload tab
```

---

## Flow 7: Multi-Step App Flow (cua Flow Engine)

```bash
# Install app flow (MIUI)
cua flow '{
  "steps": [
    {"wait": "Lanjut Instal", "then": "tap", "timeout": 15000},
    {"wait": "Selesai", "then": "tap", "timeout": 60000, "optional": true}
  ]
}'

# Login flow (generic)
cua flow '{
  "steps": [
    {"wait": "Username", "then": "tap", "timeout": 5000},
    {"waitGone": "Username", "then": "none", "timeout": 3000},
    {"wait": "Password", "then": "tap", "timeout": 5000},
    {"wait": "Login", "then": "tap", "timeout": 5000},
    {"wait": "Beranda", "then": "none", "timeout": 20000}
  ]
}'
```

---

## Flow 8: Read Notifications

```bash
cua notifications
# Returns: [{app, title, text, timestamp}, ...]

# Then act on specific notification:
cua click "BCA Mobile"  # tap notification to open
```

---

## Flow 9: Camera Capture

```bash
# Take photo via cua
cua camera back 80 1080 /tmp/photo.jpg
# quality=80, maxWidth=1080, output=/tmp/photo.jpg

# Or via ADB:
adb shell am start -a android.media.action.STILL_IMAGE_CAMERA
sleep 2
adb shell input keyevent 27  # CAMERA shutter
sleep 1
adb shell screencap /sdcard/photo.png && adb pull /sdcard/photo.png /tmp/photo.png
```
