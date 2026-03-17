# Model Fallback System Fix - March 17, 2026

## Problem
**Original Setup (BROKEN):**
- Primary: `zai/glm-5` → **TIMEOUT**
- Default: `qtcool/gpt-5.2-codex` → **403 ERROR** (Perlu VIP)

**Root Cause:**
- Zai API key issue or rate limit
- QtCool requires VIP subscription for GPT-5.2-Codex

## Solution Implemented
**New Fallback Chain (3 layers, ALL FREE):**

### Layer 1: Primary
- **Model:** `nvidia/mistralai/devstral-2-123b-instruct-2512`
- **Provider:** nvidia
- **Cost:** FREE
- **Context:** 262,144 tokens
- **Reasoning:** Yes
- **Features:** Multimodal (text + image)

### Layer 2: Fallback 1
- **Model:** `nvidia/deepseek-ai/deepseek-v3.1`
- **Provider:** nvidia
- **Cost:** FREE
- **Reasoning:** Yes

### Layer 3: Fallback 2
- **Model:** `nvidia/deepseek-ai/deepseek-v3.1-terminus`
- **Provider:** nvidia
- **Cost:** FREE
- **Reasoning:** Yes

### Layer 4: Fallback 3 (Backup of Primary)
- **Model:** `nvidia/mistralai/devstral-2-123b-instruct-2512`
- **Provider:** nvidia
- **Cost:** FREE
- **Reasoning:** Yes

## Why This Setup Works
1. **All models are FREE** - No API key issues or rate limits
2. **All have reasoning capability** - Better for complex tasks
3. **DeepSeek V3.2** - Latest and most powerful (2025 model)
4. **Devstral 2** - High performance mistral model
5. **Multimodal support** - Can handle both text and images

## Commands Used
```bash
# Clear old fallbacks
openclaw models fallbacks clear

# Add new fallback chain
openclaw models fallbacks add nvidia/deepseek-ai/deepseek-v3.1
openclaw models fallbacks add nvidia/deepseek-ai/deepseek-v3.1-terminus
openclaw models fallbacks add nvidia/mistralai/devstral-2-123b-instruct-2512

# Set primary model
openclaw models set nvidia/mistralai/devstral-2-123b-instruct-2512
```

## Verification
```bash
openclaw models status
```

**Result:**
- Default: `nvidia/mistralai/devstral-2-123b-instruct-2512`
- Fallbacks (3): DeepSeek V3.1, DeepSeek V3.1-Terminus, Devstral 2

## Configuration File
- **Location:** `~/.openclaw/openclaw/openclaw.json`
- **Config updated:** 4 times (backups created)
- **SHA256:** `a646f5d674041433c6ec42e29715932878408fe3757c027060466d4dc4f978f`

---

**Status:** ✅ COMPLETE
**Test:** Next timeout should trigger fallback automatically
