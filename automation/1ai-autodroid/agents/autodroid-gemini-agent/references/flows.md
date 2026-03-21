# Gemini Android App — Verified UI Flows

Package: `com.google.android.apps.bard`
Tested: Android 14, Redmi 2409BRN2CY, 720x1640, app version ~2026-03

## Critical Rules

1. **Wake**: `adb shell input keyevent 224` (WAKEUP). Never use keyevent 26 (it toggles).
2. **Swipe unlock**: `adb shell input swipe 360 1400 360 700`
3. **Screenshot**: `adb exec-out screencap -p > file.png` — faster, no tmp file
4. **Type**: word by word, `adb shell input text <word>` + keyevent SPACE
5. **Always new chat** before sending — avoids context pollution

## Flow: CHAT

```
1. launch app (monkey -p com.google.android.apps.bard -c LAUNCHER 1)
   sleep 3
2. dismiss_onboarding() — tap any of: Skip, Got it, Lewati, Lanjutkan, Allow
3. tap "Chat baru" button (top bar) — wait 1.5s
4. wait for "Minta Gemini" input field in UI dump
5. tap input field center (316, 1370 default)
   sleep 1
6. type_words(prompt) — word by word
   sleep 0.5
7. tap "Kirim" button by label — fallback: tap (648, 963)
8. poll UI dump every 2s for response text (up to 45s)
   - collect all text nodes > 15 chars
   - exclude UI_NOISE set
   - return first 3 joined
9. wake + screenshot → gemini_chat.png
10. return JSON {response, device, screenshot_path}
```

## Flow: IMAGE GENERATION

```
1. launch app (monkey)
   sleep 3
2. dismiss_onboarding()
3. tap "🖼️ Buat Gambar" shortcut at (193, 668)
   sleep 1
4. tap "Deskripsikan gambar Anda" input at (316, 1445)
   sleep 0.5
5. type_words(prompt)
   sleep 0.5
6. tap "Kirim" button — fallback (648, 963)
7. sleep 25 (generation takes ~15-25s)
8. wake device
9. dump UI → find "Gambar yang dibuat 1" node
10. tap image node → full screen viewer opens
11. find "Download gambar" node → tap it
    sleep 3
12. query MediaStore: content://media/external/images/media
    → get latest entry with date_added > ts_before
    → adb pull <path> <local_out>
13. screenshot screen
14. return JSON {image_path, screenshot_path, device, prompt}
```

## Actual UI Nodes (verified from uiautomator dump)

### Home screen (Gemini chat list):
```
'Buka sidebar'         [0,76][112,172]
'Gemini'               [289,94][423,154]
'Chat baru'            [424,76][520,172]
'🖼️ Buat Gambar'       [40,620][346,717]    center: (193, 668)
'🎸 Buat musik'        [40,733][312,830]
'✨ Buat hariku...'    [40,846][593,943]
'Minta Gemini'         [36,1315][596,1426]  center: (316, 1370)
'Kirim'                [600,915][696,1011]  center: (648, 963)  ← when keyboard open
```

### Image generation screen:
```
'Deskripsikan gambar Anda'  [36, ~1430][596, ~1480]  center: (316, 1445)
'Kirim'                     send button — right side of input bar
```

### Chat response screen:
```
'Gambar yang dibuat 1'  [32,558][688,915]  (bounds vary)
'Download gambar'       [516,1404][612,1500]  center: (564, 1452)
```

## MediaStore Query for Saved Image

```bash
adb shell content query \
  --uri content://media/external/images/media \
  --projection "_id:_display_name:_data:date_added"
# Parse lines: date_added=<ts>, _data=<path>
# Filter: ts > ts_before_generation
# Pull latest: adb pull <path> <local>
```

## Screen Timeout

Set to 10 minutes to prevent sleep during automation:
```bash
adb shell settings put system screen_off_timeout 600000
```
