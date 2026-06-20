---
name: clay-art-video-generator
description: Generate viral short-form videos with clay art/plasticine stop-motion diorama visuals for TikTok, Reels, and
  Shorts. Supports story mode and product review mode with lighting presets, camera angles, and Indonesian overlays.
domain: content
tags:
- art
- clay
- content-creation
- digital-content
- generator
- media
- video
---

# CLAY ART VIDEO GENERATOR SKILL
## When to Use

**Trigger phrases:**
- "clay art video generator"
- "Help me with clay art video generator"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


## Deskripsi

Membuat video pendek viral dengan visual Clay Art / Plasticine Stop-Motion Diorama untuk:
- TikTok
- Instagram Reels  
- YouTube Shorts
- Shopee Video

## Mode Operasi

- Configure art, clay, domain, generator, relevant settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### MODE A - STORY MODE
Input: Judul, Topik, Nama tokoh, Kota, Peristiwa sejarah, Ide konten
Output: Video storytelling penuh dengan semua visual berupa clay sculpture

### MODE B - REVIEW MODE
Input: Review produk / menunjukkan barang fisik
Output: Video dengan produk realistis (bukan clay) di dalam clay environment

## Clay Master Formula (WAJIB)

Setiap prompt gambar mengikuti struktur berurutan:
```
[SUBJEK UTAMA]
clay art style, handmade plasticine sculpture, stop-motion animation aesthetic, polymer clay texture
visible fingerprint marks on clay, slightly imperfect handmade edges, smooth matte clay surface, rich saturated clay colors
[LIGHTING sesuai suasana]
[SUDUT KAMERA sesuai jenis scene]
diorama world, miniature scale feeling, whimsical and charming atmosphere
ultra detailed, 8k resolution, professional product photography, sharp focus on subject, soft bokeh background
```

## Lighting Options

- Siang → soft warm sunlight, gentle studio lighting, no harsh shadows
- Sore → warm golden hour lighting, long soft shadows, amber glow
- Malam → dramatic rim lighting, soft ambient clay glow, deep shadows
- Indoor → warm indoor lighting, soft diffused light, cozy atmosphere

## Camera Options

- Peta → top-down aerial view, birds eye perspective
- Bangunan → low angle hero shot, tilt-shift miniature effect
- Tokoh → medium close-up portrait, eye level, shallow depth of field
- Alam → wide establishing shot, panoramic view, foreground detail
- Close detail → extreme close-up macro shot, bokeh background

## Format Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 RINGKASAN PROYEK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Topik : [topik]
Gaya Visual : Clay Art / Plasticine Diorama
Durasi Target: [durasi]
Platform : [platform]
Tone : [tone]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎬 SCENE BREAKDOWN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SCENE 1 — [judul scene] | Durasi: [waktu]
📝 Narasi : [narrasi]
🖼 Visual : [deskripsi visual]
💬 Caption : [caption untuk scene]
🎨 Clay Prompt: "PROMPT LENGKAP"
📹 Animasi : [jenis animasi]

(Serial hingga scene 4-6)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎵 REKOMENDASI MUSIK & AUDIO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✏️ SKRIP NARASI LENGKAP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛠 PANDUAN PRODUKSI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Products Mapping untuk Jendralbot

- Configure art, clay, domain, generator, relevant settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Story Mode (FREE Products)
- Guru Pintar AI → Naskah clay mengajarkan AI
- Belanja Duit Balik → Clay character yang shopping dapat diskon

### Review Mode (Paid Products)
- Starter AI Content → Produk real dalam clay workspace
- Studio Marketplace Pro → Produk laptop/software di clay desk
- Mesin Cetak Kuliner → Clay kitchen dengan real food products
- AI Content Pro → Real app interface di clay device mockup

## Style Rules

- Configure art, clay, domain, generator, relevant settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Story Mode
- Dramatis
- Emosional  
- Edukatif
- Immersive

### Review Mode
- Hook kuat 3 detik pertama
- Relatable
- Soft selling
- CTA halus

## Implementation

Untuk produk-produk Jendralbot, kita akan menggunakan:
1. NVIDIA NIM untuk generate clay art images (dengan prompt clay)
2. BytePlus Seedance/Google Flow untuk video AI
3. Atau FFmpeg untuk stop-motion effect manual

## Contoh Hasil

```
TOPIK: Guru Pintar AI (GRATIS)
Gaya: Clay Art Story Mode
Scene:
SCENE 1 - Introduction (5s)
Narrasi: "Ada satu naskh berisi rahasia AI"
Visual: Clay book on desk, glowing aura
Clay Prompt: "clay art style, handmade plasticine book, stop-motion animation, soft indoor lighting, medium shot, diorama world, 8k resolution"

SCENE 2 - Character (8s)
Narrative: "Seekor clay character menemukannya"
Visual: Clay person opening book
Clay Prompt: "clay art style, handmade plasticine person character, stop-motion animation, warm indoor lighting, close-up, diorama world, 8k resolution"

... dst
```

## Penggunaan

```bash
# Generate video untuk product
python3 clay_generator.py --product guru_pintar_ai --mode story

# Generate review video untuk paid product
python3 clay_generator.py --product ai_content_pro --mode review

# Batch generate all products
python3 clay_generator.py --all
```

## Notes

- Produk REALISTIS untuk review mode - tidak jadi clay
- Environment bisa clay, produk tidak
- Logo, warna, kemasan produk harus ORIGINAL
- Fokus tajam pada produk di review mode
- Clay hanya untuk environment/background

## How to Use

1. Define content goal (traffic, engagement, conversion, brand awareness)
2. Research target audience pain points and search intent
3. Generate content using appropriate AI tools
4. Edit and humanize output for authenticity
5. Optimize for target platform (SEO, hashtags, format)
6. Schedule and distribute across channels
7. Measure performance and iterate

## When NOT to Use

- Task is about content strategy, not creation (use strategy skills)
- Task is about content distribution (use distribution skills)
- You need to analyze content performance (use analytics skills)
- Task is about content moderation (use moderation tools)
- You don't have content guidelines
- Task requires domain expertise (consult experts)


## Red Flags

- **AI-generated content sounds robotic**: Always run through humanizer before publishing
- **Engagement dropping week-over-week**: Content fatigue or algorithm change — vary formats
- **Duplicate content across platforms**: Adapt content per platform, don't just cross-post
- **No content calendar**: Sporadic posting kills audience retention
- **Ignoring analytics**: Content without measurement is just publishing, not marketing

## Verification

- Check readability score (target grade 8 or below for general audiences)
- Verify all images have alt text and proper dimensions per platform
- Confirm links work and point to correct destinations
- Test video/audio quality before publishing
- Validate content renders correctly on mobile devices

## Overview

> Section content — see SKILL.md body for full details.
