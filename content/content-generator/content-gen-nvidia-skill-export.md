# Content Generation Skill with Multiprovider - Full Export

## 📋 Skill Metadata

```yaml
name: content-generator
description: Multi-step content generation workflow using Multiprovider API. Generates complete video content from text prompts: transcript/storyboard (LLM), images (character, product, background) via FLUX/Stable Diffusion, video generation via FFmpeg slideshow/zoom effects, and final video merging (30s-1min). Use when user wants automated video content creation with character, product, and scene generation. Requires NVIDIA API key and FFmpeg.
```

## 🎯 Complete Prompt for Skill Recreation

```
Create an AgentSkill called "content-generator" for automated video content generation with multi-provider support.

### Core Requirements:

1. **Multi-step Pipeline (7 Steps):**
   - Step 0: Generate transcript & storyboard using LLM (multi-provider)
   - Step 1: Generate character image (multi-provider)
   - Step 2: Generate product image (multi-provider)
   - Step 3: Generate background image (multi-provider)
   - Step 4: Generate video from images (image-to-video)
   - Step 5: Create frame transitions (frame-to-video)
   - Step 6: Merge final video (30-60 seconds)

2. **Provider Architecture:**

   **Image Generation Providers (Priority Order):**
   ```yaml
   providers:
     nvidia:
       name: "NVIDIA NIM"
       url: "https://ai.api.nvidia.com/v1"
       endpoint: "/genai/{model}"
       models: ["black-forest-labs/flux.1-dev", "flux.1-schnell", "stable-diffusion-3.5-large"]
       api_key_env: "NVIDIA_API_KEY"
       cost_per_1k_tokens: 0.05  # Relative cost
       quality: 9
       speed: 8
       reliability: 9
       fallback_to: ["replicate", "huggingface"]
     
     replicate:
       name: "Replicate"
       url: "https://api.replicate.com/v1"
       endpoint: "/predictions"
       models: ["stability-ai/stable-diffusion-3.5-large", "black-forest-labs/flux-dev", "meta-llama/llama-2-70b"]
       api_key_env: "REPLICATE_API_TOKEN"
       cost_per_1k_tokens: 0.08
       quality: 8
       speed: 7
       reliability: 9
       fallback_to: ["huggingface", "byteplus"]
     
     huggingface:
       name: "HuggingFace"
       url: "https://api-inference.huggingface.co"
       endpoint: "/models/{model}"
       models: ["stabilityai/stable-diffusion-3.5-large", "black-forest-labs/FLUX.1-dev", "openai/gpt-4o"]
       api_key_env: "HF_API_KEY"
       cost_per_1k_tokens: 0.01
       quality: 7
       speed: 6
       reliability: 8
       fallback_to: ["byteplus", "ollama_cloud"]
     
     ollama_cloud:
       name: "Ollama Cloud"
       url: "https://ollama.cloud/api"
       endpoint: "/generate"
       models: ["mistral:7b", "neural-chat", "llama2:70b"]
       api_key_env: "OLLAMA_CLOUD_API_KEY"
       cost_per_1k_tokens: 0.002
       quality: 6
       speed: 5
       reliability: 7
       fallback_to: ["huggingface"]
     
     byteplus:
       name: "BytePlus (ModelArk - Seedance)"
       url: "https://ark.ap-southeast.bytepluses.com/api/v3"
       endpoint: "/contents/generations/tasks"
       models: 
         - "seedance-1-5-pro-251215"      # NEW: Audio-video generation
         - "seedance-1-0-pro-250528"      # Image-to-video, text-to-video
         - "seedance-pro-fast"            # Fast variant
         - "seedance-1-0-lite-t2v"        # Lightweight text-to-video
         - "seedance-1-0-lite-i2v"        # Lightweight image-to-video
       api_key_env: "BYTEPLUS_API_KEY"
       cost_per_1k_tokens: 0.03
       quality: 9  # Updated: Seedance 1.5 is excellent
       speed: 9    # Very fast video generation
       reliability: 9
       capabilities:
         - text_to_video
         - image_to_video          # First frame only
         - image_to_video_advanced # First + last frame
         - reference_images_video  # Seedance 1.0 lite
         - draft_mode              # Quick preview (Seedance 1.5 Pro)
         - audio_generation        # Synchronized audio (Seedance 1.5 Pro)
         - multi_language_dialogue # 6+ languages
       fallback_to: ["nvidia", "replicate"]

   **LLM Providers (Priority Order):**
     xai:
       name: "XAI (Grok - Imagine Video)"
       url: "https://api.x.ai/v1"
       endpoint: "/videos/generations"
       models: ["grok-imagine-video"]  # Unified video model
       api_key_env: "XAI_API_KEY"
       cost_per_1k_tokens: 0.15  # Per-second pricing
       quality: 9  # High cinematic quality
       speed: 7    # Typical generation: several minutes
       reliability: 8
       capabilities:
         - text_to_video               # Text prompt → Video (1-15s)
         - image_to_video              # Still image → Animated (1-15s)
         - video_editing               # Edit existing video (up to 8.7s input)
         - gif_images_to_video         # Supports GIF input
         - base64_images               # Base64 encoded images
         - concurrent_requests         # AsyncClient support
         - custom_polling              # Manual polling control
       parameters:
         duration: [1, 15]              # seconds
         aspect_ratio: ["1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3"]
         resolution: ["480p", "720p"]   # (480p default, faster)
       fallback_to: ["byteplus", "groq"]
     
     groq:
       name: "Groq"
       url: "https://api.groq.com/openai/v1"
       endpoint: "/chat/completions"
       models: ["llama-3.3-70b-versatile", "mixtral-8x7b-32768", "gemma2-9b-it"]
       api_key_env: "GROQ_API_KEY"
       cost_per_1k_tokens: 0.07
       quality: 8
       speed: 10  # Fastest
       reliability: 9
       fallback_to: ["xai", "ollama_cloud"]
     
     nvidia_llm:
       name: "NVIDIA NIM LLM"
       url: "https://ai.api.nvidia.com/v1"
       endpoint: "/chat/completions"
       models: ["nvidia/nemotron-4-340b-instruct", "moonshotai/kimi-k2.5"]
       api_key_env: "NVIDIA_API_KEY"
       cost_per_1k_tokens: 0.10
       quality: 9
       speed: 4  # Slowest
       reliability: 7
       fallback_to: ["groq", "xai"]
   ```

3. **Provider Selection Strategy:**
   ```python
   class ProviderStrategy:
       def __init__(self):
           self.strategies = {
               "fast": ["groq", "byteplus", "replicate"],  # Speed priority
               "quality": ["nvidia", "xai", "huggingface"],  # Quality priority
               "cheap": ["ollama_cloud", "huggingface", "byteplus"],  # Cost priority
               "balanced": ["groq", "nvidia", "replicate"],  # Balance all
               "failsafe": ["nvidia", "replicate", "groq", "byteplus", "huggingface"]  # Max reliability
           }
       
       def select_provider(self, task_type, strategy="balanced"):
           # Returns ordered list of providers to try
           pass
       
       def fallback_chain(self, failed_provider):
           # Returns next provider in fallback chain
           pass
   ```

4. **Configuration System:**
   ```yaml
   # config.yaml
   content_generation:
     strategy: "balanced"  # fast, quality, cheap, balanced, failsafe
     
     image_generation:
       provider: "auto"  # auto-select or specific: nvidia, replicate, huggingface, byteplus, ollama_cloud
       fallback_enabled: true
       retry_count: 3
       timeout: 60
       use_cache: true  # Cache successful generations
       
       parameters:
         width: 1024
         height: 1024
         steps: 30
         cfg_scale: 3.5
     
     llm:
       provider: "auto"  # auto-select or specific: xai, groq, nvidia_llm, ollama_cloud
       fallback_enabled: true
       retry_count: 2
       timeout: 30
       temperature: 0.7
     
     video_processing:
       engine: "ffmpeg"
       bitrate: "8000k"
       codec: "libx264"
       framerate: 30
     
     cost_limits:
       max_per_generation: 1.0  # USD
       max_per_month: 100.0
       alert_at_percent: 80
   
   # Provider credentials
   providers:
     nvidia:
       api_key: "${NVIDIA_API_KEY}"
       enabled: true
     replicate:
       api_key: "${REPLICATE_API_TOKEN}"
       enabled: true
     huggingface:
       api_key: "${HF_API_KEY}"
       enabled: true
     xai:
       api_key: "${XAI_API_KEY}"
       enabled: true
     groq:
       api_key: "${GROQ_API_KEY}"
       enabled: true
     ollama_cloud:
       api_key: "${OLLAMA_CLOUD_API_KEY}"
       enabled: true
     byteplus:
       api_key: "${BYTEPLUS_API_KEY}"
       enabled: true
   
   # Image upload (ImgBB) - for image-to-video workflows
   image_upload:
     provider: "imgbb"              # Image hosting provider
     api_key: "${IMGBB_API_KEY}"    # https://imgbb.com/
     enabled: true
     auto_upload: true              # Auto-upload local images
     expiration: 2592000            # Keep uploaded images for 30 days (seconds)
     max_size: 32000000             # Max file size: 32 MB
     formats: ["jpg", "jpeg", "png", "gif", "webp", "bmp", "tiff"]
   ```

6. **Error Handling & Fallback Chain:**
   ```python
   class ProviderManager:
       def __init__(self, config):
           self.providers = self._load_providers(config)
           self.cost_tracker = CostTracker()
           self.cache = ProviderCache()
       
       async def generate_image(self, prompt, strategy="balanced"):
           """
           Try providers in order based on strategy.
           Falls back automatically on failure.
           """
           providers = self._get_provider_chain(task="image", strategy=strategy)
           
           for provider in providers:
               try:
                   if self.cache.has(prompt, provider):
                       return self.cache.get(prompt, provider)
                   
                   result = await provider.generate_image(prompt)
                   self.cost_tracker.log(provider, result['cost'])
                   
                   if self.cost_tracker.exceeds_limit():
                       raise CostLimitExceededError()
                   
                   self.cache.set(prompt, provider, result)
                   return result
               
               except Exception as e:
                   await self._log_failure(provider, e)
                   continue  # Try next provider
           
           raise AllProvidersFailedError(prompt)
       
       async def generate_transcript(self, prompt, strategy="balanced"):
           """Generate using LLM providers with fallback."""
           providers = self._get_provider_chain(task="llm", strategy=strategy)
           
           for provider in providers:
               try:
                   result = await provider.generate_text(prompt)
                   self.cost_tracker.log(provider, result['cost'])
                   return result
               except Exception as e:
                   await self._log_failure(provider, e)
                   continue
           
           raise AllProvidersFailedError(prompt)
   ```

7. **Output Structure:**
   ```
   output/
   ├── images/
   │   ├── character.png
   │   ├── product.png
   │   └── background.png
   ├── videos/
   │   ├── scene1_*.mp4
   │   ├── scene2_*.mp4
   │   └── scene3_*.mp4
   ├── final_video.mp4
   ├── metadata.json
   ├── provider_usage.json      # NEW: Track provider usage
   ├── cost_report.json         # NEW: Cost analysis
   └── cache/                   # NEW: Provider cache
       ├── image_hashes.db
       └── generation_logs.jsonl
   ```

8. **Technical Stack:**
   - Python 3.11+
   - urllib (no requests - environment limitation)
   - base64 (for image decoding)
   - json (API responses)
   - subprocess (FFmpeg execution)
   - pathlib (file operations)
   - **NEW: asyncio** (async provider calls)
   - **NEW: sqlite3** (caching & cost tracking)
   - **NEW: enum** (provider abstraction)

9. **Key Implementation Details:**
   - **Provider Abstraction:** Abstract base class `AIProvider` with concrete implementations
   - **Async Execution:** Use asyncio for parallel provider attempts and timeouts
   - **Cache Layer:** In-memory + SQLite persistent cache keyed by prompt hash
   - **Cost Tracking:** Real-time cost calculation with limit enforcement
   - **Fallback Logic:** Auto-switch to next provider on failure/timeout
   - **Configuration Loading:** YAML-based per-environment settings
   - **Health Checks:** Monitor provider availability before attempting requests
   - **Retry Strategy:** Exponential backoff with jitter per provider
   - **Use urllib.request** instead of requests (environment limitation)
   - Handle timeout gracefully across all providers
   - Base64 decode for image responses
   - Create portable FFmpeg solution
   - Auto-adjust video duration to 30-60 seconds

10. **Fallback Mechanisms:**
    - **Provider Chain:** If LLM fails → Try next provider in fallback chain
    - **Strategy-based Selection:** Choose provider based on speed/quality/cost goals
    - **Circuit Breaker:** Track provider failures, temporarily disable if exceeds threshold
    - **Cache Fallback:** Use cached results if all providers fail
    - **Manual Storyboard:** If all LLM providers fail, accept manual input
    - **Image Skip:** If image gen fails, continue with placeholder or retry with different provider
    - **Video Alternative:** If FFmpeg fails, return individual scene images
    - **Partial Success:** Return best effort output if some steps fail
    - **Cost Cutoff:** Auto-switch to cheaper provider if cost limit approaching

11. **Quality Settings (Provider-specific):**

    **Image Generation:**
    - NVIDIA: 1024x1024, steps=30, cfg_scale=3.5 (premium quality)
    - Replicate: 768x768, steps=25 (balanced)
    - HuggingFace: 512x512, steps=20 (fast)
    - BytePlus: 1024x1024, steps=30 (fast high-quality)
    - Ollama Cloud: 512x512, steps=15 (local fast)
    
    **LLM Generation:**
    - XAI (Grok): temperature=0.7, max_tokens=2000 (creative)
    - Groq: temperature=0.7, max_tokens=1500 (fast)
    - NVIDIA: temperature=0.5, max_tokens=1000 (conservative)
    - Ollama Cloud: temperature=0.7, max_tokens=800 (lightweight)
    
    **Video:**
    - Resolution: 1920x1080 (adaptive based on provider)
    - Framerate: 30fps
    - Codec: H.264
    - Bitrate: 8000k (adaptive based on content type)

### File Structure:
```
content-gen-multiprovider/
├── SKILL.md                         # Main documentation
├── README.md                        # Quick start guide
├── config.yaml                      # Configuration template
├── scripts/
│   ├── content_generator.py         # Main entry point
│   ├── provider_manager.py          # Provider abstraction & routing
│   ├── providers/
│   │   ├── __init__.py
│   │   ├── base.py                  # Abstract provider class
│   │   ├── nvidia.py                # NVIDIA NIM provider (images)
│   │   ├── replicate.py             # Replicate provider (images)
│   │   ├── huggingface.py           # HuggingFace provider (images)
│   │   ├── ollama_cloud.py          # Ollama Cloud provider (text/images)
│   │   ├── byteplus.py              # BytePlus provider (VIDEO + images)
│   │   └── xai.py                   # XAI/Grok VIDEO generation
│   ├── cache.py                     # Caching layer
│   ├── cost_tracker.py              # Cost tracking & limits
│   ├── fallback_strategy.py         # Fallback chain logic
│   ├── ffmpeg_processor.py          # Video processing
│   ├── image_uploader.py            # ImgBB image upload service
│   └── image_handler.py             # Image validation & conversion
├── references/
│   ├── nvidia-api.md                # NVIDIA NIM reference
│   ├── replicate-api.md             # Replicate reference
│   ├── huggingface-api.md           # HuggingFace reference
│   ├── ollama-cloud-api.md          # Ollama Cloud reference
│   ├── byteplus-api-detailed.md     # BytePlus detailed API docs
│   │   ├── seedance-1-5-pro.md      # Audio-video generation
│   │   ├── seedance-api.md          # Video gen endpoints
│   │   └── seedance-prompt-guide.md # Prompt optimization
│   ├── xai-video-api.md             # XAI Grok-Imagine-Video detailed docs
│   │   ├── text-to-video.md         # Text → Video
│   │   ├── image-to-video.md        # Image → Video (animation)
│   │   ├── video-editing.md         # Video → Edited Video
│   │   └── polling-strategy.md      # Async polling patterns
│   ├── imgbb-image-upload.md        # ImgBB API integration
│   │   ├── upload-methods.md        # Upload file/base64/URL
│   │   ├── image-validation.md      # Image checks & compression
│   │   └── image-to-video-workflow.md # ImgBB + Seedance/Grok chains
│   └── workflow.md                  # Detailed workflow guide
└── tests/
    ├── test_providers.py
    ├── test_fallback.py
    ├── test_cost_tracking.py
    └── test_e2e.py
```

### Usage Examples:

**Python API (Multi-provider):**
```python
from content_generator import ContentGenerator
from image_uploader import ImgBBUploader

# Initialize
generator = ContentGenerator(config="config.yaml", output_dir="output")
uploader = ImgBBUploader(api_key="YOUR_IMGBB_API_KEY")

# Strategy options: fast, quality, cheap, balanced, failsafe
final_video = generator.generate_complete_content(
    prompt="Create a 45-second smartwatch ad",
    theme="advertising",
    strategy="balanced"  # Uses balanced mix of quality/cost/speed
)

# IMAGE-TO-VIDEO WORKFLOW: Upload image + generate video
image_url = uploader.upload_file("./product.jpg", name="smartwatch")
video = generator.generate_with_image_to_video(
    prompt="Animate the smart watch with elegant hand gestures",
    image_url=image_url,
    video_provider="byteplus",
    model="seedance-1-5-pro-251215",
    duration=8
)

# ADVANCED: Generate character image → Upload → Create animation
character = generator.generate_image(
    prompt="Professional woman in tech company office",
    provider="nvidia"
)
char_url = uploader.upload_file(character["path"], name="character")

# Create first-frame to last-frame animation
first_frame_url = char_url
last_frame_url = uploader.upload_file("./character-smile.jpg", name="character-ending")

video = generator.generate_with_image_to_video(
    prompt="The character turns toward the camera and smiles",
    first_frame_url=first_frame_url,
    last_frame_url=last_frame_url,
    video_provider="byteplus",
    model="seedance-1-5-pro-251215"
)

# Monitor provider usage & costs
usage_stats = generator.get_provider_stats()
print(f"Cost this session: ${usage_stats['total_cost']:.2f}")
print(f"Providers used: {usage_stats['providers_used']}")
```

**Command Line (Multi-strategy):**
```bash
# Default balanced strategy
python3 scripts/content_generator.py \
    "Create an ad for a coffee shop" \
    --strategy balanced \
    --output ./output

# Fast strategy for quick generation
python3 scripts/content_generator.py \
    "Create an ad for a coffee shop" \
    --strategy fast \
    --output ./output

# Quality-focused strategy
python3 scripts/content_generator.py \
    "Create an ad for a coffee shop" \
    --strategy quality \
    --output ./output

# Cheap strategy to minimize costs
python3 scripts/content_generator.py \
    "Create an ad for a coffee shop" \
    --strategy cheap \
    --output ./output

# Failsafe strategy with maximum fallbacks
python3 scripts/content_generator.py \
    "Create an ad for a coffee shop" \
    --strategy failsafe \
    --output ./output

# Specific providers
python3 scripts/content_generator.py \
    "Create an ad for a coffee shop" \
    --image-provider nvidia \
    --llm-provider xai \
    --output ./output
```

**Environment Setup (All Providers):**
```bash
# Set provider API keys
export NVIDIA_API_KEY="nvapi-..."
export REPLICATE_API_TOKEN="r8_..."
export HF_API_KEY="hf_..."
export XAI_API_KEY="xai-..."
export GROQ_API_KEY="gsk_..."
export OLLAMA_CLOUD_API_KEY="..."
export BYTEPLUS_API_KEY="..."
export IMGBB_API_KEY="..."  # https://imgbb.com/api

# Run with all providers available
python3 scripts/content_generator.py "Your prompt" --strategy failsafe
```

**Image-to-Video Workflow (with ImgBB Upload):**
```bash
# Upload image and generate video
python3 scripts/content_generator.py \
    "Animate this image with cinematic camera movement" \
    --image-source ./my-photo.jpg \
    --llm-provider groq \
    --video-provider byteplus \
    --output ./output

# Or use pre-uploaded image URL
python3 scripts/content_generator.py \
    "Animate the landscape" \
    --image-url "https://example.com/landscape.jpg" \
    --video-provider xai \
    --output ./output
```

**Configuration File (config.yaml):**
```yaml
# See section 4 for full configuration
content_generation:
  strategy: "balanced"
  
  image_generation:
    provider: "auto"
    fallback_enabled: true
    
  llm:
    provider: "auto"
    fallback_enabled: true
  
  providers:
    nvidia:
      api_key: "${NVIDIA_API_KEY}"
      enabled: true
    replicate:
      api_key: "${REPLICATE_API_TOKEN}"
      enabled: true
    huggingface:
      api_key: "${HF_API_KEY}"
      enabled: true
    xai:
      api_key: "${XAI_API_KEY}"
      enabled: true
    groq:
      api_key: "${GROQ_API_KEY}"
      enabled: true
```

### Important Notes:

1. **Multi-Provider Architecture (Video + Images):**
   - **Image Providers:** NVIDIA, Replicate, HuggingFace, Ollama Cloud (traditional image-to-image)
   - **Video Providers:** BytePlus (Seedance), X.AI (Grok) - **Can generate videos directly!**
   - **Hybrid:** You can use image providers + video processing, OR use Seedance/Grok for end-to-end
   - **Recommendation:** Use BytePlus or X.AI for video generation (superior quality vs FFmpeg slideshow)

2. **BytePlus (Seedance) Advantages:**
   - **Native video generation** (not slideshow-based)
   - **Audio synthesis** (Seedance 1.5 Pro): Auto-generate dialogue, SFX, BGM
   - **Multi-language support:** 6+ languages with lip-sync
   - **Draft mode:** Quick preview at 1/3 cost
   - **Fast service tier:** 50% cost reduction with higher latency tolerance
   - **Image-to-video:** Multiple modes (first frame, first+last frame, reference images)

3. **X.AI (Grok-Imagine-Video) Advantages:**
   - **Cinematic quality:** High-fidelity, film-grade output
   - **Video editing:** Edit existing videos with natural language prompts
   - **Concurrent API:** Built-in async support for parallel requests
   - **Fast polling:** Optional manual control, max ~4min typical wait
   - **Aspect ratio flexibility:** 7 preset ratios including adaptive

4. **Provider-Specific Limitations:**
   - **NVIDIA:** Image-only, no video generation endpoint (404)
   - **Replicate:** Async polling required, rate-limited
   - **HuggingFace:** Rate-limited on free tier, no video support
   - **BytePlus:** Requires regional setup (Asia-Pacific), SDK installation
   - **X.AI (Grok):** Lower availability (Apollo users), higher costs
   - **Ollama Cloud:** Self-hosted variant, local-only mode available

5. **Async/Polling Patterns:**
   - **BytePlus:** Use task ID polling (`/contents/generations/tasks/{id}`)
   - **X.AI:** Start/get pattern with status enum (PENDING, DONE, EXPIRED)
   - **Both:** Can use callbacks for webhook notifications (BytePlus)

6. **Cost Analysis (Updated):**
   - **BytePlus Seedance:** ~$0.03-0.10/video (varies by duration, model tier)
   - **X.AI Grok:** Per-second pricing (~$0.5-2 per 10-second video depending on resolution)
   - **Fallback combo:** Image gen ($0.01-0.05) + FFmpeg processing (free) as backup

7. **Best Practices:**
   - Use BytePlus for production video content (best quality/price)
   - Use X.AI for cinematic branding/marketing (highest quality)
   - Use image providers + FFmpeg for cost-sensitive prototyping
   - Enable caching for prompts (70% API call reduction)
   - Test draft mode in BytePlus before final generation
   - Monitor both providers' service tiers (Seedance: default vs flex)
   - **Use ImgBB for image-to-video workflows** (automatic upload of local images)
   - Validate images before upload (size, format, dimensions)
   - Batch process multiple images for efficiency

### Documentation Requirements:

1. **SKILL.md:** Quick reference for AI agents
   - Quick start guide (all providers)
   - Available providers & models
   - Configuration (strategy, fallback)
   - Individual steps & customization
   - Provider-specific notes (IMAGE vs VIDEO)
   - Troubleshooting per provider
   
2. **README.md:** User-facing documentation
   - Installation steps
   - Multi-provider setup (6 APIs + documentation)
   - Usage examples (all strategies)
   - Output structure
   - Cost estimation (image vs video approach)
   - Common issues & solutions
   - When to use BytePlus vs X.AI

3. **config.yaml:** Configuration template
   - Per-provider settings
   - Strategy templates
   - Cost limits & alerts
   - Fallback chains
   - Environment variables

4. **references/byteplus-api-detailed.md:**
   - Complete Seedance API reference
   - Video generation endpoints
   - Polling patterns (task ID)
   - Parameter specifications
   - Audio synthesis options
   - Multi-language dialogue guide
   - Prompt engineering for video (camera, effects, sound)
   - Cost optimization (service tiers, draft mode)
   - SDK examples (Python, Go, Java)
   
5. **references/xai-video-api.md:**
   - Grok-Imagine-Video API reference
   - Text-to-video endpoint
   - Image-to-video (animation) endpoint
   - Video editing endpoint
   - Polling patterns (start/get)
   - Configuration options
   - Concurrent request handling (AsyncClient)
   - Response metadata (moderation, duration)
   - Limitations & constraints
   
6. **references/workflow.md:**
   - Multi-provider workflow explanation
   - Decision tree: When to use which provider
   - Fallback chain diagram
   - Hybrid approach (image gen + video gen)
   - Cost optimization strategies
   - Performance benchmarks (BytePlus vs X.AI vs FFmpeg)
   - Advanced audio/video integration
   - Extension possibilities

### Success Criteria:

1. ✅ Image generation works with all providers (NVIDIA, Replicate, HuggingFace, BytePlus)
2. ✅ LLM generation works with all providers (Groq, XAI, NVIDIA, Ollama Cloud)
3. ✅ Fallback chain auto-switches on provider failure
4. ✅ Cost tracking/limits enforcement working
5. ✅ Caching reduces redundant API calls
6. ✅ Strategy-based provider selection (fast/quality/cheap/balanced/failsafe)
7. ✅ All 7 pipeline steps functional with any provider combo
8. ✅ Output metadata includes provider usage stats
9. ✅ CLI supports all strategies and provider selection
10. ✅ Python API supports programmatic provider control
11. ✅ Circuit breaker prevents cascading failures
12. ✅ Configuration system supports YAML + environment variables
13. ✅ **Image upload (ImgBB) integration working**
14. ✅ **Image-to-video workflows supported** (local file → upload → generate video)
15. ✅ **Image validation and compression** implemented

### Testing Checklist:

**Provider Tests:**
- [ ] NVIDIA image generation works
- [ ] Replicate image generation works
- [ ] HuggingFace image generation works
- [ ] BytePlus image generation works
- [ ] Groq LLM generation works
- [ ] XAI (Grok) LLM generation works
- [ ] NVIDIA LLM generation works
- [ ] Ollama Cloud LLM generation works

**Fallback Chain Tests:**
- [ ] Fallback triggers on provider timeout
- [ ] Fallback triggers on API error (4xx/5xx)
- [ ] Fallback triggers on invalid API key
- [ ] Fallback chain exhaustion handled gracefully
- [ ] Circuit breaker activates after N failures

**Strategy Tests:**
- [ ] Fast strategy selects correct provider order
- [ ] Quality strategy selects correct provider order
- [ ] Cheap strategy selects correct provider order
- [ ] Balanced strategy selects correct provider order
- [ ] Failsafe strategy includes all providers

**Cache Tests:**
- [ ] Cache hits reduce API calls
- [ ] Cache miss triggers API call
- [ ] Cache invalidation works
- [ ] Cache database persists across runs

**Image Upload Tests (ImgBB):**
- [ ] Upload binary file works
- [ ] Upload base64-encoded image works
- [ ] Upload from URL works
- [ ] Image validation (size, format, dimensions)
- [ ] Compression triggers for oversized images
- [ ] API key validation
- [ ] Error handling for invalid images
- [ ] Expiration settings respected
- [ ] Multiple uploads in sequence

**Image-to-Video Tests:**
- [ ] BytePlus I2V (first frame) with uploaded image
- [ ] BytePlus I2V (first + last frame) with uploaded images
- [ ] X.AI image animation with uploaded image
- [ ] Image URL passed correctly to providers
- [ ] Aspect ratio preservation
- [ ] Video generation from uploaded image works
- [ ] Local file upload → video generation chain
- [ ] Batch image-to-video processing

**Cost Tracking Tests:**
- [ ] Cost calculation accurate per provider
- [ ] Monthly limit enforcement works
- [ ] Alerts trigger at 80% threshold
- [ ] Generation blocked when limit exceeded

**Integration Tests:**
- [ ] Full pipeline with NVIDIA images + Groq LLM
- [ ] Full pipeline with Replicate images + XAI LLM
- [ ] Full pipeline with HuggingFace images + Ollama LLM
- [ ] Full pipeline with fallback chain all the way
- [ ] Transcript generation works
- [ ] Character image generation works
- [ ] Product image generation works
- [ ] Background image generation works
- [ ] Video slideshow creation works
- [ ] Zoom effect video works
- [ ] Frame extraction works
- [ ] Video merging works
- [ ] Auto-adjust duration works
- [ ] Save metadata.json works
- [ ] Fallback mechanisms trigger properly

**CLI Tests:**
- [ ] `--strategy fast` works
- [ ] `--strategy quality` works
- [ ] `--strategy cheap` works
- [ ] `--strategy balanced` works
- [ ] `--strategy failsafe` works
- [ ] `--image-provider nvidia` works
- [ ] `--llm-provider groq` works
- [ ] Config file loading works
- [ ] Environment variables override config

**Output Tests:**
- [ ] Images saved correctly
- [ ] Videos saved correctly
- [ ] metadata.json contains provider info
- [ ] provider_usage.json tracks stats
- [ ] cost_report.json accurate

---

This skill should be production-ready for generating video content from text prompts using NVIDIA NIM API for images and Groq for LLM, with FFmpeg for video processing.
```

---

## 🖼️ ImgBB Image Upload Integration (for Image-to-Video)

**Official Docs:** https://api.imgbb.com/

### Why ImgBB for Image-to-Video?

BytePlus Seedance and X.AI Grok both support **image-to-video generation**. ImgBB provides:
- ✅ Free API with 32 MB upload limit per image
- ✅ Permanent and temporary URLs (configurable expiration)
- ✅ No authentication required per image (one API key handles all)
- ✅ Global CDN for fast image serving
- ✅ Support for multiple formats: JPG, PNG, GIF, WebP, BMP, TIFF, HEIC

### API Endpoint:

```
POST https://api.imgbb.com/1/upload
```

### Request Parameters:

```python
{
  "key": "YOUR_IMGBB_API_KEY",           # Required: API key
  "image": "<binary|base64|url>",        # Required: Image (local file, base64, or URL)
  "name": "my-image",                    # Optional: Custom name
  "expiration": 2592000                  # Optional: Auto-delete after N seconds (60-15552000)
}
```

### Upload Methods:

**Method 1: Binary File (Recommended for local files)**
```python
import requests

with open("landscape.jpg", "rb") as f:
    response = requests.post(
        "https://api.imgbb.com/1/upload",
        params={"key": "YOUR_IMGBB_API_KEY"},
        files={"image": f},
        data={"name": "landscape"}
    )
    
image_url = response.json()["data"]["url"]
print(f"Uploaded: {image_url}")
```

**Method 2: Base64 Encoding (for in-memory images)**
```python
import base64
import requests
from PIL import Image
from io import BytesIO

img = Image.open("photo.jpg")
buffer = BytesIO()
img.save(buffer, format="JPEG")
base64_image = base64.b64encode(buffer.getvalue()).decode()

response = requests.post(
    "https://api.imgbb.com/1/upload",
    params={"key": "YOUR_IMGBB_API_KEY"},
    data={"image": base64_image}
)

image_url = response.json()["data"]["url"]
```

**Method 3: Image URL (Direct reference)**
```python
response = requests.post(
    "https://api.imgbb.com/1/upload",
    params={"key": "YOUR_IMGBB_API_KEY"},
    data={
        "image": "https://example.com/existing-image.jpg",
        "name": "imported-image"
    }
)
```

**Method 4: Using urllib (No requests library)**
```python
import urllib.request
import urllib.parse
import base64
import json

with open("image.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

params = urllib.parse.urlencode({
    "key": "YOUR_IMGBB_API_KEY",
    "image": image_data
})

request = urllib.request.Request(
    f"https://api.imgbb.com/1/upload",
    data=params.encode(),
    method="POST"
)

with urllib.request.urlopen(request) as response:
    result = json.loads(response.read())
    image_url = result["data"]["url"]
```

### API Response:

```json
{
  "data": {
    "id": "2ndCYJK",
    "title": "landscape",
    "url_viewer": "https://ibb.co/2ndCYJK",
    "url": "https://i.ibb.co/xyz123/landscape.jpg",
    "display_url": "https://i.ibb.co/abc456/landscape.jpg",
    "width": "1920",
    "height": "1080",
    "size": "350000",
    "time": "1645000000",
    "expiration": "0",
    "image": {
      "filename": "landscape.jpg",
      "name": "landscape",
      "mime": "image/jpeg",
      "extension": "jpg",
      "url": "https://i.ibb.co/xyz123/landscape.jpg"
    },
    "thumb": {
      "filename": "landscape.jpg_thumb",
      "name": "landscape_thumb",
      "mime": "image/jpeg",
      "extension": "jpg",
      "url": "https://i.ibb.co/thumb123/landscape.jpg"
    }
  },
  "success": true,
  "status": 200
}
```

### Image Upload Service (Python Implementation):

```python
class ImgBBUploader:
    def __init__(self, api_key, auto_delete_days=30):
        self.api_key = api_key
        self.base_url = "https://api.imgbb.com/1/upload"
        self.expiration = auto_delete_days * 86400  # Convert to seconds
    
    def upload_file(self, file_path, name=None):
        """Upload local image file"""
        if not name:
            name = os.path.basename(file_path).split(".")[0]
        
        with open(file_path, "rb") as f:
            files = {"image": f}
            data = {
                "key": self.api_key,
                "name": name,
                "expiration": self.expiration
            }
            response = requests.post(self.base_url, files=files, data=data)
        
        result = response.json()
        if result["success"]:
            return result["data"]["url"]
        else:
            raise Exception(f"Upload failed: {result.get('error')}")
    
    def upload_base64(self, image_base64, name):
        """Upload base64-encoded image"""
        data = {
            "key": self.api_key,
            "image": image_base64,
            "name": name,
            "expiration": self.expiration
        }
        response = requests.post(self.base_url, data=data)
        
        result = response.json()
        if result["success"]:
            return result["data"]["url"]
        else:
            raise Exception(f"Upload failed: {result.get('error')}")
    
    def upload_url(self, image_url, name):
        """Reference existing image by URL"""
        data = {
            "key": self.api_key,
            "image": image_url,
            "name": name
        }
        response = requests.post(self.base_url, data=data)
        
        result = response.json()
        if result["success"]:
            return result["data"]["url"]
        else:
            raise Exception(f"Upload failed: {result.get('error')}")
```

### Integration with Image-to-Video Workflow:

```python
from image_uploader import ImgBBUploader
from content_generator import ContentGenerator

# Initialize
uploader = ImgBBUploader(api_key="YOUR_IMGBB_API_KEY")
generator = ContentGenerator(config="config.yaml")

# Workflow 1: Upload local image → Generate video with BytePlus
local_image_path = "./my-photo.jpg"
image_url = uploader.upload_file(local_image_path, name="vacation")

video = generator.generate_with_image_to_video(
    prompt="Smooth pan camera movement revealing the beach landscape",
    image_url=image_url,  # Now using uploaded URL
    video_provider="byteplus",
    model="seedance-1-5-pro-251215"
)

# Workflow 2: Generate image → Upload → Create video chain
character_image = generator.generate_image(
    prompt="A woman in business attire",
    provider="nvidia"
)
image_path = character_image["path"]
image_url = uploader.upload_file(image_path, name="character")

video = generator.generate_with_image_to_video(
    prompt="The character turns and smiles at the camera",
    image_url=image_url,
    video_provider="xai",
    model="grok-imagine-video",
    duration=8
)

# Workflow 3: Multiple image animation sequence
images = [
    "./scene1.jpg",
    "./scene2.jpg",
    "./scene3.jpg"
]

uploaded_urls = []
for img_path in images:
    url = uploader.upload_file(img_path, name=f"scene-{len(uploaded_urls)+1}")
    uploaded_urls.append(url)

# Generate videos from each uploaded image
videos = []
for url in uploaded_urls:
    video = generator.generate_with_image_to_video(
        prompt="Cinematic transition",
        image_url=url,
        video_provider="byteplus"
    )
    videos.append(video)

# Merge videos
final_video = generator.merge_videos(videos)
```

### Error Handling & Validation:

```python
class ImageValidator:
    SUPPORTED_FORMATS = ["jpg", "jpeg", "png", "gif", "webp", "bmp", "tiff"]
    MAX_SIZE = 32_000_000  # 32 MB
    
    @staticmethod
    def validate_file(file_path):
        """Validate local image file"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Image not found: {file_path}")
        
        # Check size
        size = os.path.getsize(file_path)
        if size > ImageValidator.MAX_SIZE:
            raise ValueError(f"Image too large: {size} > {ImageValidator.MAX_SIZE}")
        
        # Check format
        ext = file_path.split(".")[-1].lower()
        if ext not in ImageValidator.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {ext}")
        
        # Check dimensions (should be between 0.4-2.5 aspect ratio for Seedance)
        from PIL import Image
        img = Image.open(file_path)
        aspect = img.width / img.height
        if aspect < 0.4 or aspect > 2.5:
            raise ValueError(f"Invalid aspect ratio: {aspect} (must be 0.4-2.5)")
        
        # Check minimum dimensions
        if img.width < 300 or img.height < 300:
            raise ValueError("Image too small (min 300px)")
        
        return True
    
    @staticmethod
    def compress_if_needed(file_path, max_size=32_000_000):
        """Compress image if it exceeds max size"""
        from PIL import Image
        
        if os.path.getsize(file_path) <= max_size:
            return file_path
        
        img = Image.open(file_path)
        quality = 95
        while os.path.getsize(file_path) > max_size and quality > 10:
            img.save(file_path, quality=quality, optimize=True)
            quality -= 5
        
        return file_path
```

### ImgBB vs Direct URL Comparison:

| Feature | Direct URL | ImgBB Upload |
|---------|-----------|--------------|
| Setup | Immediate | Requires API key |
| Free Tier | ✅ Yes | ✅ Yes (100-200/day) |
| Authentication | ⚠️ Depends on origin | ✅ Single API key |
| Image Count | ⚠️ Varies by host | ✅ Unlimited |
| Reliability | ⚠️ Host-dependent | ✅ CDN-backed |
| Auto-deletion | ❌ No | ✅ Configurable |
| Local Files | ❌ Must host first | ✅ Direct upload |
| Use Case | Pre-hosted URLs | Local images → video |

### Configuration in config.yaml:

```yaml
image_upload:
  provider: "imgbb"
  api_key: "${IMGBB_API_KEY}"
  enabled: true
  
  # Auto-upload local images when referenced
  auto_upload: true
  
  # Clean up on expiration (days)
  expiration: 30
  
  # Max file size (bytes)
  max_size: 32000000
  
  # Supported formats
  formats:
    - jpg
    - jpeg
    - png
    - gif
    - webp
    - bmp
    - tiff
  
  # Validation
  validation:
    min_width: 300
    min_height: 300
    aspect_ratio_min: 0.4
    aspect_ratio_max: 2.5
```

### CLI Integration:

```bash
# Upload image and generate video in one command
python3 scripts/content_generator.py \
    --action image-to-video \
    --image-source ./landscape.jpg \
    --prompt "Smooth camera pan revealing the sunset" \
    --video-provider byteplus \
    --model seedance-1-5-pro-251215 \
    --auto-upload true \
    --output ./final_video.mp4

# Use pre-uploaded image URL
python3 scripts/content_generator.py \
    --action image-to-video \
    --image-url "https://i.ibb.co/xyz123/landscape.jpg" \
    --prompt "Cinematic drone shot rising above the mountains" \
    --video-provider xai \
    --duration 10 \
    --output ./final_video.mp4

# Batch process multiple local images
python3 scripts/content_generator.py \
    --action batch-image-to-video \
    --image-dir ./photos \
    --prompt "Smooth camera movement" \
    --video-provider byteplus \
    --output ./videos
```

---

### BytePlus ModelArk (Seedance Video Generation)

**Official Docs:** https://docs.byteplus.com/en/docs/ModelArk/1520757

#### Key Capabilities:
- **Seedance 1.5 Pro** (NEW): Joint audio-video generation with:
  - Multi-language dialogue (Mandarin, English, Japanese, Korean, Spanish, Indonesian)
  - Lip-sync precision at millisecond level
  - Automatic background music generation
  - Text-to-Video, Image-to-Video (first frame), Image-to-Video (first + last frame)
  
- **Seedance 1.0 Pro/Lite**: Time-tested models with:
  - Image-to-video with reference images
  - Configurable parameters (resolution, duration, aspect ratio)
  - Draft mode for quick preview (lower tokens)

#### API Endpoint:
```
POST https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks
```

#### Request Parameters:
```python
{
  "model": "seedance-1-5-pro-251215",  # or seedance-1-0-pro-250528, seedance-pro-fast
  "content": [
    {"type": "text", "text": "Your prompt here"},
    # Optional: Add images for image-to-video
    # {"type": "image_url", "image_url": {"url": "..."}, "role": "first_frame"}
  ],
  "resolution": "720p",      # 480p | 720p | 1080p
  "ratio": "16:9",           # 16:9 | 4:3 | 1:1 | 3:4 | 9:16 | 21:9 | adaptive
  "duration": 5,             # 2-12 seconds (Seedance 1.5: set to -1 for auto)
  "seed": -1,                # -1 for random
  "camera_fixed": false,     # Fix camera angle
  "watermark": false,        # Add BytePlus watermark
  "generate_audio": true,    # Seedance 1.5 Pro only: auto-generate audio
  "draft": false,            # Seedance 1.5 Pro: true for draft preview
  "service_tier": "default", # default (online) | flex (offline 50% cost)
  "execution_expires_after": 172800  # 48 hours default
}
```

#### Response:
```json
{"id": "cgt-2025-xxx-xxx"}  // Poll this task ID for results
```

#### Query Results:
```
GET https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks/{id}
```

#### Models Summary:
| Model | Type | Quality | Speed | Audio | Languages |
|-------|------|---------|-------|-------|-----------|
| seedance-1-5-pro-251215 | T2V, I2V-F, I2V-FL | 🌟🌟🌟 High | Fast | ✅ Sync | 6+ |
| seedance-1-0-pro-250528 | T2V, I2V-F, I2V-FL | 🌟🌟 Good | Normal | ❌ | 1 |
| seedance-pro-fast | T2V, I2V-F | 🌟🌟 Good | ⚡ Very Fast | ❌ | 1 |
| seedance-1-0-lite-t2v | T2V | 🌟 Fair | Fast | ❌ | 1 |
| seedance-1-0-lite-i2v | I2V-Ref | 🌟 Fair | Normal | ❌ | 1 |

#### Prompt Engineering Tips:
```
Subject + Movement + Environment + Camera Movement + Aesthetic + Sound

Example:
"A woman in a red dress dancing on a sunny beach with waves, 
 smooth pan camera movement, cinematic lighting, upbeat music --resolution 720p --duration 5"
```

#### SDK Installation:
```bash
# Python
pip install byteplus-python-sdk-v2

# Go  
go get -u github.com/byteplus-sdk/byteplus-go-sdk-v2

# Java (Maven)
# Add to pom.xml:
# <dependency>
#   <groupId>com.byteplus</groupId>
#   <artifactId>byteplus-java-sdk-v2-ark-runtime</artifactId>
#   <version>LATEST</version>
# </dependency>
```

---

### X.AI / Grok Imagine Video (Video Generation & Editing)

**Official Docs:** https://docs.x.ai/developers/model-capabilities/video/generation

#### Key Capabilities:
- **Video Generation**: Text-to-Video, Image-to-Video (animation), Video Editing
- **Async Polling**: Two-step process (start → poll)
- **Concurrent Requests**: AsyncClient support for parallel generations
- **Moderation**: Content policy enforcement + respect_moderation flag
- **High Quality**: Cinematic-grade output with strong scene preservation

#### API Endpoints:

**Start Generation (Async):**
```
POST https://api.x.ai/v1/videos/generations
```

**Check Status (Polling):**
```
GET https://api.x.ai/v1/videos/{request_id}
```

#### Text-to-Video Request:
```json
{
  "model": "grok-imagine-video",
  "prompt": "A glowing crystal-powered rocket launching from Mars",
  "duration": 10,              // 1-15 seconds
  "aspect_ratio": "16:9",      // 1:1 | 16:9 | 9:16 | 4:3 | 3:4 | 3:2 | 2:3
  "resolution": "720p"         // 480p (default) | 720p
}
```

#### Image-to-Video Request:
```json
{
  "model": "grok-imagine-video",
  "prompt": "Animate the clouds drifting and trees swaying",
  "image_url": "https://example.com/landscape.jpg",  // or data:image/jpeg;base64,...
  "duration": 12,
  "aspect_ratio": "16:9"
}
```

#### Video Editing Request:
```json
{
  "model": "grok-imagine-video",
  "prompt": "Give the woman a silver necklace",
  "video_url": "https://data.x.ai/docs/video-generation/portrait-wave.mp4",
  // Note: duration, aspect_ratio, resolution NOT supported for editing
  // Output retains input video's properties (capped at 720p)
}
```

#### Polling Strategy:
```
Status values: pending | done | expired

Response (when done):
{
  "status": "done",
  "video": {
    "url": "https://vidgen.x.ai/.../video.mp4",
    "duration": 8
  },
  "model": "grok-imagine-video",
  "respect_moderation": true
}
```

#### Response Details:
- **URL Expiration**: Temporary URLs (download/process immediately)
- **Duration**: Typical generation 2-4 minutes (depends on prompt complexity)
- **Moderation**: Check `respect_moderation` field (true = passed, false = filtered)
- **Max Input Video**: 8.7 seconds for editing operations

#### Configuration Reference:
| Parameter | Values | Notes |
|-----------|--------|-------|
| duration | 1-15s | Text/Image-to-video only |
| aspect_ratio | 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3 | Image defaults to input ratio |
| resolution | 480p, 720p | 480p default (faster) |
| model | grok-imagine-video | Current/only available model |

#### Python SDK Usage:
```python
import xai_sdk

client = xai_sdk.Client()

# Text-to-video
response = client.video.generate(
    prompt="A glowing crystal-powered rocket launching from Mars",
    model="grok-imagine-video",
    duration=10,
    aspect_ratio="16:9",
    resolution="720p"
)
print(response.url)

# With custom polling
from datetime import timedelta
response = client.video.generate(
    prompt="Epic cinematic drone shot",
    model="grok-imagine-video",
    duration=15,
    timeout=timedelta(minutes=15),  # Wait up to 15 min
    interval=timedelta(seconds=5)   # Check every 5s
)

# Concurrent requests
import asyncio
async def edit_concurrently():
    client = xai_sdk.AsyncClient()
    prompts = [
        "Give the woman a silver necklace",
        "Change outfit color to red",
        "Add a black hat"
    ]
    tasks = [
        client.video.generate(
            prompt=p,
            model="grok-imagine-video",
            video_url="https://example.com/video.mp4"
        )
        for p in prompts
    ]
    results = await asyncio.gather(*tasks)
    return results
```

#### Pricing:
- **Per-second billing**: Duration affects cost directly
- **Resolution**: 720p more expensive than 480p
- **Longer videos**: Increased cost but better output quality

#### Limitations:
- **Maximum Duration**: 15s (text/image), 8.7s (video editing)
- **URL Expiration**: Temporary (download immediately)
- **Resolutions**: 480p or 720p only
- **Moderation**: Subject to content policy review

---

### Supported Providers (6 Total)

| Provider | Type | Quality | Speed | Cost | Reliability | Fallback To |
|----------|------|---------|-------|------|-------------|------------|
| NVIDIA NIM | Image | 🌟🌟🌟 9/10 | 8/10 | $$$ | 9/10 | Replicate |
| Replicate | Image | 🌟🌟 8/10 | 7/10 | $$ | 9/10 | HuggingFace |
| HuggingFace | Image | 🌟 7/10 | 6/10 | $ | 8/10 | BytePlus |
| **BytePlus** | **VIDEO** 🎬 | 🌟🌟🌟 9/10 | 🌟🌟 8/10 | $$ | 🌟🌟🌟 9/10 | X.AI |
| **X.AI (Grok)** | **VIDEO** 🎬 | 🌟🌟🌟 9/10 | 7/10 | $$$ | 8/10 | BytePlus |
| Groq | LLM | 🌟🌟 8/10 | 🌟🌟🌟 10/10 | $$ | 9/10 | Ollama |
| Ollama Cloud | Both | 🌟 6/10 | 5/10 | $ | 7/10 | HuggingFace |

**KEY INSIGHT:** BytePlus & X.AI are **primary video generators** (not image generators). They can replace the entire FFmpeg pipeline with native, high-quality video output!

### Provider API Keys Required:

```bash
# Image Providers
NVIDIA_API_KEY="nvapi-..."          # https://ai.nvidia.com
REPLICATE_API_TOKEN="r8_..."        # https://replicate.com
HF_API_KEY="hf_..."                 # https://huggingface.co
BYTEPLUS_API_KEY="..."              # https://byteplus.com

# LLM Providers
GROQ_API_KEY="gsk_..."              # https://console.groq.com
XAI_API_KEY="xai-..."               # https://console.x.ai
OLLAMA_CLOUD_API_KEY="..."          # https://ollama.cloud
```

### Strategy Reference:

| Strategy | Best For | Provider Order |
|----------|----------|-----------------|
| **fast** | Quick iteration, prototyping | Groq → BytePlus → Replicate |
| **quality** | Final output, premium content | NVIDIA → XAI → Replicate |
| **cheap** | Cost-sensitive, research | Ollama Cloud → HuggingFace → BytePlus |
| **balanced** | Production, general use | Groq → NVIDIA → Replicate |
| **failsafe** | Max reliability, guaranteed output | All 7 providers in fallback chain |

### Models Available:

**IMAGE Generation (per provider):**
- NVIDIA: `black-forest-labs/flux.1-dev`, `flux.1-schnell`, `stable-diffusion-3.5-large`
- Replicate: `stability-ai/stable-diffusion-3.5-large`, `black-forest-labs/flux-dev`
- HuggingFace: `stabilityai/stable-diffusion-3.5-large`, `black-forest-labs/FLUX.1-dev`
- Ollama Cloud: Standard models via ollama library

**VIDEO Generation (NATIVE):** ✨ NEW
- **BytePlus/Seedance:** 
  - `seedance-1-5-pro-251215` ⭐ (Audio-video generation, multi-language, lip-sync)
  - `seedance-1-0-pro-250528` (Fast, image-to-video)
  - `seedance-pro-fast` (Ultra-fast variant)
  - `seedance-1-0-lite-t2v` (Lightweight text-to-video)
  - `seedance-1-0-lite-i2v` (Lightweight image-to-video)
- **X.AI/Grok:**
  - `grok-imagine-video` (Text-to-video, image-to-video, video editing)

**LLM (per provider):**
- Groq: `llama-3.3-70b-versatile`, `mixtral-8x7b-32768`, `gemma2-9b-it`
- NVIDIA: `nvidia/nemotron-4-340b-instruct`, `moonshotai/kimi-k2.5`
- Ollama Cloud: `mistral:7b`, `neural-chat`, `llama2:70b`

### Configuration Template:

```yaml
content_generation:
  strategy: "balanced"  # fast | quality | cheap | balanced | failsafe
  
  image_generation:
    provider: "auto"    # auto | nvidia | replicate | huggingface | byteplus | ollama_cloud
    fallback_enabled: true
    retry_count: 3
    cache_enabled: true
  
  llm:
    provider: "auto"    # auto | groq | xai | nvidia_llm | ollama_cloud
    fallback_enabled: true
    retry_count: 2
    temperature: 0.7
  
  cost_limits:
    max_per_generation: 1.0   # USD
    max_per_month: 100.0      # USD
    alert_at_percent: 80
  
  providers:
    nvidia:
      api_key: "${NVIDIA_API_KEY}"
      enabled: true
    replicate:
      api_key: "${REPLICATE_API_TOKEN}"
      enabled: true
    huggingface:
      api_key: "${HF_API_KEY}"
      enabled: true
    byteplus:
      api_key: "${BYTEPLUS_API_KEY}"
      enabled: true
    xai:
      api_key: "${XAI_API_KEY}"
      enabled: true
    groq:
      api_key: "${GROQ_API_KEY}"
      enabled: true
    ollama_cloud:
      api_key: "${OLLAMA_CLOUD_API_KEY}"
      enabled: true
```

### Typical Costs per Generation:

**Image-only approach** (image gen + FFmpeg):
- Fast strategy: $0.01 - $0.03
- Cheap strategy: $0.02 - $0.08
- Balanced strategy: $0.05 - $0.15
- Quality strategy: $0.08 - $0.25

**Video-native approach** (BytePlus/X.AI):
- **BytePlus Seedance 1.5 Pro:** $0.05 - $0.20 per video (5-12s, includes audio)
- **BytePlus Seedance 1.0/Lite:** $0.02 - $0.10 per video (fast, image-to-video)
- **X.AI Grok-Imagine:** $0.50 - $3.00 per video (10-15s, cinema-grade)
- **BytePlus Draft Mode:** 1/3 cost of standard (preview before final)

**Recommendation:**
- Use **BytePlus for production** (best quality/price balance)
- Use **X.AI for premium branding** (highest cinematic quality)
- Use image-based fallback for cost-sensitive or prototyping scenarios

---

**Export Date:** 2026-02-19
**Skill Version:** 2.1 (Multi-provider + Image Upload)
**Status:** ✅ Architecture Designed | ✅ ImgBB Integration Added | ⏳ Implementation Ready

### 📸 Image Upload Service Summary:

**ImgBB Integration Features:**
- Free image hosting with 32 MB per file limit
- 100-200 uploads per day on free tier
- Automatic expiration (configurable, default 30 days)
- Support for JPG, PNG, GIF, WebP, BMP, TIFF formats
- Global CDN for fast image serving
- No CORS issues (cross-origin friendly)

**Image-to-Video Workflows Enabled:**
1. Local image file → Upload to ImgBB → Generate video with BytePlus/X.AI
2. Generated image (from NVIDIA/Replicate) → Upload → Create animation
3. Multiple images → Batch upload → Sequential video generation
4. First-frame + Last-frame → Advanced image-to-video in Seedance 1.5 Pro

**Key Classes:**
- `ImgBBUploader`: Handle image uploads (binary, base64, URL)
- `ImageValidator`: Validate file size, format, dimensions, aspect ratio
- `ImageHandler`: Convert formats, compress if needed, validate before upload

**CLI Commands:**
```bash
# Single image-to-video
python3 scripts/content_generator.py \
    --action image-to-video \
    --image-source ./photo.jpg \
    --prompt "Animate with camera movement" \
    --video-provider byteplus

# Batch process multiple images
python3 scripts/content_generator.py \
    --action batch-image-to-video \
    --image-dir ./photos \
    --prompt "Cinematic transition" \
    --video-provider byteplus
```
