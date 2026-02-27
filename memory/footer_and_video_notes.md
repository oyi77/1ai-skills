# NOTES: Footer Structure & Video Generation

**Last Updated**: 2026-02-28

---

## 📋 Footer Structure (Dari berkahkarya.org)

### Main Page Footer Components:

**1. Brand Section**
- Logo: Berkah Karya
- Tagline: "Membantu Brand Anda Tumbuh Lewat Strategi Digital yang Terbukti"

**2. Quick Links**
- Home
- Services
- Portfolio
- Pricing
- About

**3. Contact Information**
- Phone: +62 857-3274-0006
- Email: info@berkahkarya.org
- Website: berkahkarya.org

**4. Social Media Links**
- Instagram
- TikTok
- Facebook
- LinkedIn

**5. Copyright Section**
- "© 2026 Berkah Karya. All rights reserved."

**6. Design Notes**
- Footer background: Dark color (#0f172a or similar)
- Text color: White/light gray (#f8fafc)
- Links color: White with hover effect
- Social icons: Font Awesome or custom SVG icons
- Responsive: Stack vertically on mobile, horizontal on desktop

---

## 🎨 Design Patterns (Dari berkahkarya.org)

### Colors:
- Primary: #3b82f6 (Blue)
- Secondary: #1e40af (Dark Blue)
- Background: #0f172a (Dark Navy)
- Text: #f8fafc (White)
- Hover: #60a5fa (Lighter Blue)

### Typography:
- Headings: Poppins, 600-700
- Body: Poppins, 300-400
- Links: Poppins, 500

### Spacing:
- Section padding: 4rem top/bottom
- Footer padding: 3rem top/bottom
- Link spacing: 1.5rem

---

## 📹 VIDEO GENERATION NOTES

### Current Portfolio (3 Videos):

**1. Before & After Transformation**
- File: motivation_1772208104_final.mp4
- Size: 1.8MB
- Concept: Transformasi lantai lama ke vinyl tiles baru
- Tags: #vinylfloor #renovation

**2. Premium Showcase**
- File: motivation_1772208521_final.mp4
- Size: 1.9MB
- Concept: Living room mewah dengan vinyl tiles premium
- Tags: #vinylfloor #homedesign

**3. Installation Process**
- File: motivation_1772210602_final.mp4
- Size: 1.4MB
- Concept: Tutorial instalasi vinyl tiles profesional
- Tags: #vinylfloor #diy

### Quality Notes (UNTUK PERBAIKAN):
- Videos kelihatan "AI banget" (dari feedback user)
- Masalah yang terdeteksi:
  - Motion tidak natural
  - Lighting aneh
  - Texture terlihat plastik
  - Gerakan kasar
  - Over-sharp

### REKOMENDASI PERBAIKAN:

**Positive Prompt (Untuk Video Lebih Natural):**
- "Realistic video of vinyl floor tile installation in Indonesian home, natural motion, professional filming, cinematic lighting, consistent texture"
- "Before & After transformation of old floor to new vinyl tiles in Indonesian living room, smooth camera motion, realistic shadows, high quality photography"
- "Professional vinyl floor tile showcase in modern Indonesian living room, natural ambient lighting, smooth camera pan, realistic materials"

**Negative Prompt (HINDARI AI ARTIFACTS):**
- "no plastic skin texture, no oversharpen, no morphing artifacts, no flickering, no warped motion, no distorted hands, no artificial lighting, no unrealistic reflections"
- "no AI generation artifacts, no low quality, no pixelation, no frame drops, no color grading issues"
- "no cartoonish, no fake, no generated-looking, no unnatural, no glossy plastic look"

**Parameter Settings:**
- Duration: 15 detik (TikTok format)
- Resolution: 1080x1920 (9:16 portrait)
- Frame rate: 30fps
- Bitrate: Medium (untuk menghindari over-sharp)
- Quality: Hyperrealistic

### VARIASI ALTERNATIF (2-3 versi):

**Versi 1 - Slow Motion:**
- Duration: 15 detik
- Motion: 0.5x speed (slow motion)
- Fokus: Detail vinyl tiles texture

**Versi 2 - Normal Motion:**
- Duration: 15 detik
- Motion: 1.0x speed (normal)
- Fokus: Natural camera movement

**Versi 3 - Cinematic:**
- Duration: 15 detik
- Motion: 1.2x speed (slightly fast)
- Fokus: Smooth camera pan, professional look

---

## 🔧 TECHNICAL SETTINGS

### Video Generation Tools:
- Image: NVIDIA Flux.1-dev
- Video: BytePlus Seedance Pro I2V
- Audio: Edge TTS (id-ID-GadisNeural)
- Compose: FFmpeg

### Current Issues:
- Transitions: Kasar (tidak ada crossfade)
- Motion: Tidak natural
- Lighting: Terlalu terang/aneh
- Texture: Terlihat plastik

### FIXES NEEDED:
1. Tambah crossfade transitions (FFmpeg xfade filter)
2. Kurangi bitrate untuk menghindari over-sharp
3. Tambah color grading yang lebih natural
4. Gunakan ambient lighting yang realistis
5. Tambah noise/grain untuk mengurangi "AI banget" look

---

## 📊 NEXT STEPS (UNTUK VIDEO PERBAIKAN)

### Langkah 1: Generate Ulang Videos
- Gunakan prompt berbeda untuk masing-masing video
- Tambah negative prompt yang kuat
- Sesuaikan parameter (bitrate, quality settings)
- Waktu: 10-15 menit per video

### Langkah 2: Fix Transitions
- Tambah crossfade antar loop
- Gunakan FFmpeg xfade filter
- Durasi transition: 0.5-1 detik

### Langkah 3: Color Grading
- Tambah color grading yang natural
- Kurangi contrast (hindari over-sharp)
- Sesuaikan brightness yang realistis

### Langkah 4: Test & Validasi
- Test di desktop dan mobile
- Cek apakah "AI banget" look sudah berkurang
- Minta feedback dari user
- Sesuaikan prompt berdasarkan feedback

---

## 📝 TASK LIST (PRIORITY)

### HIGH PRIORITY (SEKARANG):
- [ ] Fix footer tiktok-agency.html (samakan dengan main page)
- [ ] Generate ulang 3 videos dengan prompt lebih natural
- [ ] Tambah crossfade transitions
- [ ] Test videos dan validasi

### MEDIUM PRIORITY:
- [ ] Buat 2-3 variasi alternatif per video
- [ ] Tambah color grading
- [ ] Optimize untuk mobile (9:16 TikTok format)
- [ ] Test pada berbagai perangkat

### LOW PRIORITY:
- [ ] Buat thumbnails untuk YouTube/TikTok
- [ ] Buat short clips untuk Instagram Reels
- [ ] Buat landscape version untuk Facebook
- [ ] Test A/B dengan berbagai prompt

---

## 🎯 SUCCESS CRITERIA

### Video Natural (Bukan "AI Banget"):
- [ ] Motion natural dan tidak kasar
- [ ] Lighting realistis dan konsisten
- [ ] Texture tidak terlihat plastik
- [ ] Tidak ada artefak AI (morphing, flickering, dll)
- [ ] Transisi smooth dan tidak abrupt

### Footer Rapi & Konsisten:
- [ ] Layout sama dengan main page
- [ ] Typography sama (Poppins)
- [ ] Warna sama (dark background, white text)
- [ ] Spacing sama (padding, margins)
- [ ] Mobile-friendly (stack vertical)

### Website Fully Functional:
- [ ] Semua video akses publik
- [ ] Tidak ada error 404
- [ ] Tidak ada error 403
- [ ] Responsive di desktop dan mobile
- [ ] Contact form berfungsi

---

## 💡 NOTES PENTING

### 1. FOOTER CONSISTENCY
- Wajib sama persis dengan main page (berkahkarya.org)
- Layout: Brand section, Quick links, Contact, Social media, Copyright
- Desain: Dark background, white text, blue hover effects
- Responsive: Mobile vertical stack, desktop horizontal

### 2. VIDEO NATURAL LOOK
- Gunakan prompt yang fokus ke realism (bukan AI-generated look)
- Tambah negative prompt yang kuat
- Parameter: Low bitrate, natural lighting, smooth motion
- Transitions: Crossfade (bukan abrupt cuts)

### 3. TESTING & VALIDASI
- Test semua link (incognito mode)
- Test semua video (desktop dan mobile)
- Test form submission
- Cek semua error (console logs)
- Minta feedback dari user

---

**Last Updated**: 2026-02-28
**Status**: Ready for next steps
**Priority**: Footer fix → Video regeneration → Testing & validation
