---
name: vicestudio
description: Local-first AI voice studio for voice cloning, design, dubbing, dictation, and audiobook narration in 646 languages.
domain: content
category: content
tags: [voice-cloning, dubbing, transcription, audiobook, tts, local-first]
license: AGPL-3.0
author: oyi77
---
# VoiceStudio Skill

## Overview
VoiceStudio is an open-source, fully-local alternative to cloud-based voice synthesis platforms (e.g., ElevenLabs). It provides a professional suite for voice cloning, design, and dubbing, supporting 646 languages. Unlike basic TTS, VoiceStudio is a generative studio that allows users to clone a reference voice, design new voice identities from traits, and automate high-volume narration for audiobooks or video dubbing. It includes advanced audio processing capabilities such as Vocal Isolation and Speaker Diarization.

## When to Use
Use VoiceStudio when you need high-fidelity, private, and local-first speech synthesis or voice-to-voice translation.

**Trigger Phrases:**
- "clone this voice"
- "design a new voice"
- "dub this video into Spanish"
- "generate audiobook narration"
- "transcribe this audio locally"
- "dictate text to file"

**Concrete Use Cases:**
- **Voice Cloning:** Turning a short reference recording into a reusable voice profile for TTS.
- **Voice Design:** Creating a unique voice identity by adjusting traits (e.g., age, gender, tone).
- **Video Dubbing:** Translating video speech into another language while maintaining original timing and speaker identity.
- **Local Dictation:** Using the floating widget for secure, offline speech-to-text.
- **Batch Narration:** Generating long-form audiobooks from text scripts via queued jobs.

## When NOT to Use
- **Real-time Low-Latency Streaming:** While fast, the full generative pipeline is designed for studio production rather than ultra-low-latency conversational AI.
- **Cloud-only Workflows:** VoiceStudio is strictly local-first; it does not provide a hosted API for external apps (except for its own local API).
- **Non-Voice Audio:** It is a generative voice studio, not a general audio repair, spectral-repair, stem-mixer, or LUFS mastering suite. While it can isolate vocals and diarize speakers, it is not a denoiser or noise-removal tool.
- **Non-supported Hardware:** Requires modern OS (macOS 13.3+, Windows 10/11, Linux) and ideally a GPU for reasonable synthesis speeds.

## Workflow
1. **Install & Setup:** Install via Homebrew, Snap, or direct binary. Run the setup wizard to configure hardware acceleration (CUDA/MPS/Vulkan).
2. **Model Selection:** Use the Model Manager to download the desired engine (e.g., OmniVoice) and specific language packs.
3. **Voice Acquisition:** Either clone a voice from a reference WAV or use the Voice Design workspace to define traits.
4. **Content Generation:** Input text or upload video for dubbing. Configure timing, emotion, and target language.
5. **Export & Verify:** Generate the audio/video, preview via the built-in player, and export as WAV/MP3.

## Anti-Rationalization Table

| Rationalization | Reality |
| :--- | :--- |
| "I can just use a cloud TTS service for faster setup." | Cloud services risk data privacy and can be expensive for high-volume audiobook production. |
| "AGPL-3.0 only matters if I modify the source code." | AGPL-3.0 network use triggers source disclosure requirements for the combined work; read the license before embedding. |
| "Cloning a voice is always ethical if the source is public." | Voice cloning requires explicit consent; cloning without permission can violate personality rights and platform TOS. |

## Verification
- [ ] Install succeeds using `curl -fsSL https://voicestudio.sh/install | sh` or `brew install --cask debpalash/tap/voicestudio`.
- [ ] App launches and passes the initial hardware/GPU auto-detect check.
- [ ] Model Manager successfully downloads the default `VoiceStudio` (OmniVoice) engine.
- [ ] Voice cloning run produces a WAV file that exists, has non-zero length, and is not pure silence.
- [ ] Vocal Isolation on a mixed test file produces a separated vocal stem.
- [ ] Batch Queue accepts and completes a queued narration job.
- [ ] MCP server starts and a client can list its available tools (tool names are enumerated by the client from the running MCP server).
- [ ] Video dubbing generates a translated track that aligns with the original video timing.
- [ ] Local transcription (ASR) correctly identifies spoken text from a test WAV file.

## Attribution
- README.md: General purpose, install commands, and platform support.
- feature-catalog.md: Engine list, transcription providers, and core features (Vocal Isolation, MCP Server).
- audio-quality.md: Export precision, voice refinement, and signal checks.
- downloading-models.md: Hugging Face LFS/Xet logic and mirror endpoints.
- electron-dubbing.md: Dubbing workflow, timing strategies, and ASR behavior.

Upstream: `debpalash/VoiceStudio` (AGPL-3.0). No prose copied. Default engine is `k2-fsa/OmniVoice` (refer to `omnivoice` skill if available).

```bash
# Install VoiceStudio (macOS/Linux)
curl -fsSL https://voicestudio.sh/install | sh

# Or install via Homebrew (macOS)
brew tap debpalash/tap
brew trust --cask debpalash/tap/voicestudio
brew install --cask debpalash/tap/voicestudio

# Development from source
git clone https://github.com/debpalash/VoiceStudio.git
cd VoiceStudio
nix develop .#fhs && bun run dev
```

`brew install --cask debpalash/tap/voicestudio`

