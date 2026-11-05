---
name: omnivoice
description: Use when synthesizing multilingual speech, cloning a voice from short reference audio, or designing a voice from attribute descriptions with the offline OmniVoice toolkit.
domain: content
category: content
tags: [tts, voice-cloning, speech-synthesis, multilingual, offline, diffusion]
license: Apache-2.0
author: oyi77
---

# OmniVoice Skill

## Overview

OmniVoice (`k2-fsa/OmniVoice`, Apache-2.0, README read 2026-11-05) is an offline-capable zero-shot text-to-speech toolkit built on a diffusion language-model-style architecture supporting 600+ languages. One pretrained checkpoint (`k2-fsa/OmniVoice`) serves three generation modes through the same `model.generate()` call: voice cloning from 3-10 seconds of reference audio (`ref_audio` plus optional `ref_text`, auto-transcribed via Whisper when omitted), voice design from a comma-separated attribute string (`instruct="female, low pitch, british accent"`, no reference audio), and auto voice with no prompt at all. Output is a list of `np.ndarray` at 24 kHz. It runs on NVIDIA CUDA, Apple Silicon `mps`, Intel Arc `xpu`, and CPU, with streaming-style low real-time factor, non-verbal tags (`[laughter]`, `[sigh]`), pinyin tone and CMU-dict pronunciation control, and three CLI entry points (`omnivoice-demo` Gradio web UI, `omnivoice-infer` single item, `omnivoice-infer-batch` multi-GPU batch).

## When to Use

**Trigger phrases:**
- "omnivoice voice cloning"
- "omnivoice-infer"
- "zero-shot TTS offline"
- "voice design instruct"

**Use cases:**
- Short-form narration cloned from a 3-10 second reference clip
- Multilingual dubbing where the reference and target share a language
- Voice prototyping from attribute descriptions with no reference audio

## When NOT to Use

- Cloning a voice without the speaker's consent — the upstream disclaimer prohibits unauthorized voice cloning, impersonation, fraud, and scams; voice data is biometric data under regimes such as GDPR and BIPA.
- Expecting accent-free cross-lingual cloning — when reference audio and target speech differ in language, output carries the reference language's accent.
- Reference clips far outside 3-10 seconds — longer audio slows inference and may degrade cloning quality.
- Very short clips (1-2 seconds) with no reference audio — the model does not reliably generate them; provide reference audio.
- Voice design outside Chinese and English — the model is trained on voice cloning primarily and voice design on Chinese and English only, so other languages may be unstable.
- Trusting raw numerals — pass `normalize_text=True` (requires `pip install "omnivoice[tn]"`) or expand "123" to words yourself.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Zero-shot means no training and no stored voice data" | Inference extracts a speaker prompt you can save (`my_voice.pt`); store prompt files as securely as the reference audio. |
| "Offline means it is automatically safe" | Pretrained weights and prompt files can carry voice identity; handle them under the same consent and retention rules as recordings. |
| "Cross-lingual cloning keeps the target accent" | It does not; output carries the reference audio's language accent, so match reference language to target language. |
| "Voice design works in every language" | Voice design is trained on Chinese and English data only and may be unstable in low-resource languages; cloning is the most stable mode. |
| "Short text always renders fine" | Clips of 1-2 seconds without reference audio are unreliable; add reference audio or lengthen the text. |

## Verification

- [ ] `pip install omnivoice` completes without errors
- [ ] `omnivoice-demo --help` prints its options
- [ ] `omnivoice-infer --help` prints its flags (read exact flag names from this output before scripting further invocations)
- [ ] `omnivoice-demo --ip 0.0.0.0 --port 8001` launches the local Gradio web UI
- [ ] `omnivoice-infer --model k2-fsa/OmniVoice --text "This is test for text to speech." --ref_audio ref.wav --ref_text "Transcription reference audio." --output hello.wav` writes `hello.wav`
- [ ] `omnivoice-infer --model k2-fsa/OmniVoice --text "This is test for text to speech." --instruct "male, British accent" --output hello.wav` writes `hello.wav`
- [ ] `omnivoice-infer --model k2-fsa/OmniVoice --text "This is a test for text speech." --output hello.wav` writes `hello.wav` in auto-voice mode

## Workflow

1. Install PyTorch for your device, then install with `pip install omnivoice`
2. Pick a mode: cloning (`--ref_audio` plus optional `--ref_text`), design (`--instruct`), or auto (neither)
3. Run one `omnivoice-infer` invocation or one `model.generate()` call and inspect the WAV output
4. For repeat use, save the clone prompt once and reload it instead of re-transcribing

## Implementation

```python
from omnivoice import OmniVoice
import soundfile as sf
import torch

model = OmniVoice.from_pretrained(
    "k2-fsa/OmniVoice",
    device_map="cuda:0",
    dtype=torch.float16,
)
# Apple Silicon: device_map="mps". Intel Arc: device_map="xpu".

audio = model.generate(
    text="Hello, this is a test of zero-shot voice cloning.",
    ref_audio="ref.wav",
    ref_text="Transcription of the reference audio.",
)
sf.write("out.wav", audio[0], 24000)

prompt = model.create_voice_clone_prompt(
    ref_audio="ref.wav", ref_text="Transcription of the reference audio."
)
prompt.save("my_voice.pt")

from omnivoice import VoiceClonePrompt

prompt = VoiceClonePrompt.load("my_voice.pt")
audio = model.generate(text="Hello again!", voice_clone_prompt=prompt)
sf.write("out2.wav", audio[0], 24000)
```
