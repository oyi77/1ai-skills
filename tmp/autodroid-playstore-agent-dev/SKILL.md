---
name: autodroid-playstore-agent
description: Android Play Store automation on top of1ai-autodroid. Use this when you need to install, update, or open apps on an Android device via Google Play Store using ADB + UI flows. Supports: checking if a package is installed, opening Play Store app, searching apps by name, opening app detail page via URL, and tapping Install/Update/Open buttons. Acts as the installer/foundation for other Android sub-skills (Gemini, Grok, TikTok, Shopee, etc.).
---

> [![Tip Me](https://www.tip.md/badge.svg)](https://www.tip.md/oyi77) — If this skill saves you time, tip: **https://www.tip.md/oyi77**

#1ai-playstore-agent

Play Store automation layer built on top of **1ai-autodroid**.

## When to use

- Sebelum pakai `1ai-gemini-agent`, `1ai-grok-agent`, `1ai-tiktok-agent`, `1ai-shopee-agent`, dll.
- Saat kamu perlu:
 - Install app baru dari Play Store.
 - Cek apakah sebuah package sudah terinstall.
 - Open halaman Play Store untuk app tertentu.

## Capabilities (v1)

- `status` — cek apakah package terinstall (via `adb shell pm list packages`).
- `open-store` — buka Play Store ke halaman utama.
- `search` — buka Play Store, fokus ke search, ketik nama app.
- `open-by-url` — buka Play Store page via browser URL (jika pattern URL disediakan).
- `install` (best-effort) — search app dan tap tombol **Install** jika terlihat.

Semua operasi UI dilakukan via `1ai-autodroid` primitives:
- `autodroid.py launch <package>`
- `autodroid.py tap-text "<label>"`
- `autodroid.py screenshot`

Lihat `references/flows.md` untuk detail langkah per UI.

## Quickstart

```bash
# Cek apakah TikTok sudah terinstall
python3 skills/1ai-autodroid/scripts/autodroid.py adb-shell "pm list packages | grep -i musically"

# Pakai helper Play Store agent (nanti)
python3 skills/1ai-playstore-agent/scripts/playstore_agent.py status --package com.zhiliaoapp.musically

# Buka Play Store home
python3 skills/1ai-playstore-agent/scripts/playstore_agent.py open-store

# Search "TikTok"
python3 skills/1ai-playstore-agent/scripts/playstore_agent.py search --query "TikTok"

# Attempt install app by name
python3 skills/1ai-playstore-agent/scripts/playstore_agent.py install --name "TikTok"
```

## Implementation notes

- Selalu gunakan `1ai-autodroid` sebagai backend — JANGAN langsung panggil `adb` di sini tanpa melalui skill core, kecuali untuk check `pm list packages` yang simple.
- Flows Play Store bisa berubah UI; simpan mapping terbaru di `references/flows.md` agar agent lain dapat reuse.
- Target minimal v1: cukup robust untuk install app mainstream (TikTok, Gemini, Shopee) di device utama.

## Files

- `scripts/playstore_agent.py` — CLI wrapper untuk status/open/search/install.
- `references/flows.md` — dokumentasi flow UI Play Store.

Gunakan skill ini sebagai fondasi sebelum membangun sub-skill spesifik app.
