# AutoDroid Flows — Ready-to-Use Automation Recipes

## Flow 1: BCA Balance Check

```python
# scripts/flow_bca_balance.py
import subprocess, sys, os

ADB = os.path.expanduser("~/.local/bin/adb")

def adb(cmd):
    return subprocess.run(f"{ADB} {cmd}", shell=True, capture_output=True, text=True).stdout

def screenshot(path="/tmp/bca_screen.png"):
    adb("shell screencap /sdcard/bca_screen.png")
    adb(f"pull /sdcard/bca_screen.png {path}")
    return path

# Step 1: Open BCA Mobile
adb("shell monkey -p com.bca -c android.intent.category.LAUNCHER 1")
import time; time.sleep(3)

# Step 2: Screenshot → analyze with image tool
img = screenshot()
print(f"Screenshot saved: {img}")
print("→ Use image tool to read screen, find balance or next action")
```

---

## Flow 2: WhatsApp Send Message

```bash
# Send via ADB intent (no app interaction needed)
adb shell am start -a android.intent.action.VIEW \
  -d "https://api.whatsapp.com/send?phone=628xxx&text=Hello%20from%20AI" \
  com.whatsapp

# Wait for app to open, then tap Send button
sleep 2
# Tap Send (adjust coordinates per screen size)
adb shell input tap 990 1850  # example for 1080x2400
```

---

## Flow 3: Screenshot + OCR Pipeline

```python
import subprocess, os

ADB = os.path.expanduser("~/.local/bin/adb")

def capture_and_analyze(save_path="/tmp/autodroid_screen.png"):
    """Take screenshot, return path for image tool analysis."""
    subprocess.run(f"{ADB} shell screencap /sdcard/auto_cap.png", shell=True)
    subprocess.run(f"{ADB} pull /sdcard/auto_cap.png {save_path}", shell=True)
    print(f"Screenshot: {save_path}")
    print("Next: use image tool to analyze")
    return save_path
```

---

## Flow 4: App Launch + Wait for Load

```python
import subprocess, time, os

ADB = os.path.expanduser("~/.local/bin/adb")

def launch_app_and_wait(package, wait=3):
    subprocess.run(
        f"{ADB} shell monkey -p {package} -c android.intent.category.LAUNCHER 1",
        shell=True, capture_output=True
    )
    time.sleep(wait)
    # Take screenshot to verify load
    subprocess.run(f"{ADB} shell screencap /sdcard/launch_verify.png", shell=True)
    subprocess.run(f"{ADB} pull /sdcard/launch_verify.png /tmp/launch_verify.png", shell=True)
    return "/tmp/launch_verify.png"
```

---

## Flow 5: Unlock Screen

```python
import subprocess, os

ADB = os.path.expanduser("~/.local/bin/adb")

def is_locked():
    out = subprocess.run(
        f"{ADB} shell dumpsys window | grep mCurrentFocus",
        shell=True, capture_output=True, text=True
    ).stdout
    return "StatusBar" in out or "Keyguard" in out

def unlock(pin=None):
    subprocess.run(f"{ADB} shell input keyevent 26", shell=True)  # POWER
    import time; time.sleep(0.5)
    subprocess.run(f"{ADB} shell input keyevent 82", shell=True)  # MENU/UNLOCK
    time.sleep(0.5)
    if pin:
        subprocess.run(f"{ADB} shell input text {pin}", shell=True)
        subprocess.run(f"{ADB} shell input keyevent 66", shell=True)  # ENTER
```

---

## Flow 6: Vision Tap (AI coordinates)

```python
"""
Use this when you don't know the coordinates.
Steps:
1. screenshot()
2. Pass to image tool: "Find [element]. Return center X,Y coordinates."
3. Parse X Y from response
4. tap(X, Y)
"""

import subprocess, os, re

ADB = os.path.expanduser("~/.local/bin/adb")

def tap(x, y):
    subprocess.run(f"{ADB} shell input tap {x} {y}", shell=True)

def parse_coordinates(ai_response: str):
    """Parse X,Y from image tool response."""
    match = re.search(r'(\d+)\s*,\s*(\d+)', ai_response)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None

# Example usage:
# img_path = screenshot()
# ai_response = image(img_path, "Find the Login button. Return X,Y center.")
# x, y = parse_coordinates(ai_response)
# if x: tap(x, y)
```
