# ClawPaw/cua HTTP Bridge — Setup Guide

## What is cua?

`cua` = Claw Use Android CLI. Connects to ClawPaw APK running on the device via HTTP + Accessibility Service.

**Advantage over ADB:**
- No USB needed (WiFi)
- Text-based click (not coordinates)
- Flow engine (100ms poll, zero LLM per step)
- SMS, contacts, camera, TTS, clipboard, location
- Multi-device management

---

## Step 1: Install ClawPaw APK

Download dari: https://github.com/clawpaw/android/releases

```bash
# Install via ADB
adb install clawpaw.apk
```

Atau: transfer APK ke HP → install dari file manager.

---

## Step 2: Enable Accessibility Service

Di HP:
```
Settings → Accessibility → Installed Services → Claw Use → ON
```

Untuk MIUI/HyperOS:
```
Settings → Additional Settings → Accessibility → Installed Apps → Claw Use → ON
```

---

## Step 3: Install cua CLI (di server/laptop)

```bash
# npm (jika tersedia)
npm install -g claw-use-android-cli

# atau pip
pip install cua-android

# atau binary langsung dari releases
wget https://github.com/clawpaw/cua/releases/latest/download/cua-linux-x64 -O ~/.local/bin/cua
chmod +x ~/.local/bin/cua
```

---

## Step 4: Register Device

```bash
# Cari IP HP (lihat di ClawPaw app → main screen)
# Cari token (lihat di ClawPaw app → notification atau main screen)

cua add phone1 192.168.x.x <token>
cua devices  # verify
cua -d phone1 ping  # test connectivity
cua -d phone1 info  # check permissions
```

---

## Step 5: Configure Auto-Unlock (PIN)

```bash
cua config pin 123456   # simpan PIN sekali
# Setelah ini, semua command otomatis unlock dulu
```

---

## MIUI/HyperOS Extra Permissions

```bash
# Grant semua permissions otomatis (untuk MIUI phones)
cua -d phone1 setup-perms

# Manual jika auto gagal:
# Settings → Apps → Claw Use → App permissions → Enable all
# Settings → Apps → Claw Use → Autostart → ON
# Settings → Battery → Claw Use → No restrictions
```

---

## Verify Setup

```bash
cua status          # health dashboard
cua screen -c       # test a11y tree
cua screenshot      # test screenshot
cua lock && sleep 2 && cua unlock  # test auto-unlock
```

---

## Alternative: ADB-Only (tanpa ClawPaw)

Jika tidak mau install APK:
- Gunakan Mode 1 (ADB Direct) atau Mode 2 (Vision) dari SKILL.md
- `autodroid.py` tidak perlu ClawPaw sama sekali
