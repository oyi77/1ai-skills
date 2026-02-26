# Content Generator — Provider Status

_Last Updated: 2026-02-27_

## ✅ WORKING PROVIDERS

### NVIDIA NIM — Image Generation
- **Status:** ✅ FIXED & WORKING
- **Endpoint:** `POST https://ai.api.nvidia.com/v1/genai/{provider}/{model-id}`
- **Working model:** `black-forest-labs/flux.1-dev`
- **Payload:** `{"prompt": "..."}` — minimal, NO `num_images`, NO `seed: null`
- **Response format:** `{"artifacts": [{"finishReason": "SUCCESS", "base64": "...", "seed": 123}]}`
- **Output:** base64 JPEG (~91KB for typical image)
- **File:** `scripts/providers/nvidia.py` — UPDATED

**What was wrong:**
- Endpoint was `integrate.api.nvidia.com/v1/images/generation/` → 404
- Fixed to `ai.api.nvidia.com/v1/genai/` pattern
- `num_images: 1` in payload → 422 Unprocessable Entity
- Fixed: only send `prompt`, add optional params only if explicitly set

---

### BytePlus Seedance — Video Generation
- **Status:** ✅ FIXED & WORKING
- **Base URL:** `https://ark.ap-southeast.bytepluses.com/api/v3`
- **Create task:** `POST /contents/generations/tasks`
- **Get task:** `GET /contents/generations/tasks/{task_id}`
- **Working model:** `seedance-1-0-lite-t2v-250428`
- **Request body:**
  ```json
  {
    "model": "seedance-1-0-lite-t2v-250428",
    "content": [{"type": "text", "text": "prompt..."}],
    "ratio": "16:9"
  }
  ```
- **Response:** `{"id": "cgt-xxxxx"}` → poll until `status="succeeded"` → `content.video_url`
- **Avg generation time:** ~20 seconds (lite model)
- **Output:** MP4 video, 720p, 5s default
- **File:** `scripts/providers/byteplus.py` — REWRITTEN

**What was wrong:**
- Old code used `open.byteplusapi.com` → 400 (wrong endpoint, AWS-style API)
- Old code used `/videoextraction/v1/generation/` → 500 (not the right product)
- Fixed: Use `ark.ap-southeast.bytepluses.com/api/v3` with task-based API
- `resolution` parameter → 400 (not valid for lite model) — removed from default payload
- The API is **async**: create task → poll → download video URL

---

## ⏳ PENDING PROVIDERS

### Ollama Cloud — LLM
- **Status:** ⏳ PENDING (API key known, base URL unknown)
- **API key:** `9ff4521cc25e4d81a15950c8a798c68a.zA2f6_Et22Gxt4CmmqXi7Cc8`
- **Current provider file:** `scripts/providers/ollama.py` — base_url set to `https://api.ollama.com`
- **TODO:** Test `https://api.ollama.com` with API key, confirm working
- **File:** `scripts/providers/ollama.py` — partially fixed (localhost → cloud URL)

---

## ✅ TESTED PIPELINE

**Date:** 2026-02-27
**Result:** WORKING — video sent to Telegram (msgId: 2569)

**Steps:**
1. NVIDIA NIM Flux 1.1 → 91KB JPEG image (91,053 bytes)
2. BytePlus Seedance T2V → 2.5MB MP4 video (5s, 720p, 16:9)
   - Task: `cgt-20260227070906-c6jdx`
   - Time: ~20 seconds
3. Downloaded video to `/tmp/seedance_video.mp4`
4. Sent to Telegram chat `228956686`

**Prompt used:**
```
A premium gold coffee cup on a sleek black table, warm morning sunlight streaming through a cafe window, steam rising, professional photography, cinematic 4K quality
```

---

## KNOWN LIMITATIONS

- **FFmpeg text overlay:** Not built with libfreetype — no text on videos
- **BytePlus `resolution` param:** Not valid for `seedance-1-0-lite-t2v` model
- **BytePlus video URL expiry:** Signed URL expires in 86400s (24h) — download immediately
- **NVIDIA image:** Returns base64 JPEG (not URL) — need to save locally or upload for I2V
- **XAI credits:** Exhausted, do not use

## INTEGRATION STATUS

| Component | Status |
|-----------|--------|
| `scripts/providers/nvidia.py` | ✅ Fixed |
| `scripts/providers/byteplus.py` | ✅ Rewritten |
| `scripts/providers/ollama.py` | ⚠️ Partial fix |
| `scripts/providers/groq.py` | Unknown (not tested) |
| `scripts/providers/xai.py` | ❌ No credits |
| `scripts/cli.py` | Not updated (still references old provider format) |
| `scripts/generator.py` | Missing (referenced in SKILL.md) |

## NEXT STEPS

1. **Create `generator.py`** — the main orchestrator referenced in SKILL.md (missing)
2. **Test Ollama Cloud** — verify `https://api.ollama.com` with API key
3. **Update `cli.py`** — add BytePlus as video provider option
4. **Install FFmpeg with libfreetype** — for text overlays
5. **I2V pipeline** — use NVIDIA image → upload to temp hosting → BytePlus I2V
6. **9:16 vertical video** — current output is 16:9; TikTok needs 9:16
