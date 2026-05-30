---
name: ai-content-agency-v2
description: ULTIMATE MASTER BLUEPRINT v2.0. Use when relevant to this domain.
---

# ULTIMATE MASTER BLUEPRINT v2.0
## AI Content Agency — 9 Workflows, 6 Phases

Mock Product A: "Madu Herbal Asli Hutan Kalimantan — Rp 85.000"
Mock Product B: "Influencer Marketing Automation —  -1 to 1M per project"
Mock Product C: "3D Medical Chibi Service — Rp 500K/animation (10 videos)"

---

# ══════════════════════════════════════
# PHASE 0: DISCOVERY & IDEATION
# ══════════════════════════════════════

### Node P0.1: Trigger
```
Name : wh_ideation
Type : Webhook Trigger
Path : /webhook/ideation
```

**Payload:**
```json
{
  "product_category": "herbal_kesehatan",
  "raw_product_info": "Madu hutan asli Kalimantan, organik, anti-oksidan tinggi",
  "target_audience": "ibu rumah tangga 30-50 tahun peduli kesehatan keluarga",
  "stuck_on": "tidak tahu angle konten apa yang cocok"
}
```

### Node P0.2: LLM — Creative Director Ideation
```
Name : creative_director_ideation
Type : AI Conversation
Temp : 0.9
Format: json_object
```

**System Prompt:**
```
Kamu adalah Creative Director yang menghasilkan ide konten dari 3 angle berbeda.
Output HARUS JSON valid tanpa markdown.
```

**User Prompt:**
```
Produk: {{wh_ideation.body.raw_product_info}}
Kategori: {{wh_ideation.body.product_category}}
Target: {{wh_ideation.body.target_audience}}
User stuck on: {{wh_ideation.body.stuck_on}}

Generate 3 ide dari angle berbeda:

{
  "ideas": [
    {
      "angle": "health_herbal",
      "concept": "(angle kesehatan/herbal: manfaat alami, ritual perawatan, tradisi turun-temurun)",
      "hook_suggestion": "",
      "best_workflow": "(nomor workflow 1-9 yang paling cocok)",
      "reasoning": ""
    },
    {
      "angle": "what_if_design",
      "concept": "(angle what-if: bagaimana kalau produk ini divisualisasikan dengan cara unik/fusion?)",
      "hook_suggestion": "",
      "best_workflow": "",
      "reasoning": ""
    },
    {
      "angle": "modest_storytelling",
      "concept": "(angle storytelling modest: cerita personal/keluarga yang relatable)",
      "hook_suggestion": "",
      "best_workflow": "",
      "reasoning": ""
    }
  ]
}
```

**Output — Mock Madu Herbal:**
```json
{
  "ideas": [
    {
      "angle": "health_herbal",
      "concept": "Ritual pagi ibu: satu sendok madu hutan sebelum masak untuk keluarga. Visual: dapur warm tone, uap teh, madu mengalir slow-motion.",
      "hook_suggestion": "Ini yang gue minum tiap pagi sebelum ngurusin anak-anak",
      "best_workflow": "6",
      "reasoning": "Faceless Spiritual cocok untuk vibe reflektif ritual pagi"
    },
    {
      "angle": "what_if_design",
      "concept": "What if madu hutan Kalimantan bertemu desain apothecary modern? Visual: botol madu dalam setting laboratorium herbal futuristik.",
      "hook_suggestion": "Kalau madu hutan dipackaging kayak obat mahal, keliatan kayak gini",
      "best_workflow": "7",
      "reasoning": "What If Fusion sempurna untuk visual contrast tradisional vs modern"
    },
    {
      "angle": "modest_storytelling",
      "concept": "POV: Ibu yang diam-diam jaga kesehatan keluarga tanpa mereka sadari. Plot twist: anak yang cerita.",
      "hook_suggestion": "Mama nggak pernah cerita, tapi tiap pagi dia selalu siapin ini",
      "best_workflow": "2",
      "reasoning": "POV Shots cocok untuk storytelling emosional keluarga"
    }
  ]
}
```

**Output Variables:**
```
{{creative_director_ideation.ideas[0].concept}} → concept untuk di-pass ke workflow
{{creative_director_ideation.ideas[0].best_workflow}} → "6" (routing ke workflow mana)
```

---

# ══════════════════════════════════════
# PHASE 1 & 2: RESEARCH & EXTRACTION
# ══════════════════════════════════════

### Node P1.1: Trigger
```
Name : wh_extract
Path : /webhook/extract
```

**Payload:**
```json
{
  "product_url": "https://tokopedia.link/madu-herbal-kalimantan",
  "target_audience": "ibu rumah tangga 30-50 tahun",
  "selected_concept": "{{creative_director_ideation.ideas[0].concept}}"
}
```

### Node P1.2: 3-Layer Fallback Scraper
```
Name : scraper
Type : Code Node
```

```javascript
// Attempt 1: web_fetch → Attempt 2: browser → Attempt 3: web_search
// (Same pattern as previous blueprint)
// Output: {{scraper.raw_text}}
```

### Node P1.3: USP Extractor
```
Name : usp_extractor
Type : AI Conversation
Temp : 0.3
```

**User Prompt:**
```
Raw text: {{scraper.raw_text}}
Target: {{wh_extract.body.target_audience}}

{
  "product_name": "",
  "price": "",
  "top_3_usp": ["", "", ""],
  "emotional_benefit": "",
  "pain_point": "",
  "social_proof": "",
  "objection_killer": "",
  "sensory_keywords": ["", "", ""],
  "compliance_notes": "(jika produk kesehatan: catat klaim yang harus dihindari)"
}
```

**Output — Mock Madu Herbal:**
```
{{usp_extractor.product_name}} → "Madu Herbal Asli Hutan Kalimantan"
{{usp_extractor.price}} → "Rp 85.000"
{{usp_extractor.top_3_usp[0]}}}} → "Dipanen langsung dari hutan Kalimantan, bukan ternak"
{{usp_extractor.top_3_usp[1]}}}} → "Antioksidan 3x lebih tinggi dari madu biasa"
{{usp_extractor.top_3_usp[2]}}}} → "Tanpa campuran gula, 100% murni bersertifikat"
{{usp_extractor.emotional_benefit}}}}} → "Ketenangan hati ibu yang tahu keluarganya mengonsumsi yang terbaik dari alam"
{{usp_extractor.pain_point}}}}}} → "Khawatir madu di pasaran palsu atau dicampur gula"
{{usp_extractor.sensory_keywords}}}}}} → ["kental mengalir lambat", "aroma bunga hutan", "warna amber gelap"]
{{usp_extractor.compliance_notes}}}}}} → "HINDARI klaim: menyembuhkan, mengobati, anti-kanker"
```

---

# ════════════════════════════════════════
# PHASE 3: THE 9 SPECIALIZED WORKFLOWS
# ══════════════════════════════════════

### ROUTER: Switch Node

```
Name : workflow_router
Type : Code Node
```

```javascript
const workflowId = '{{trigger.body.workflow_id}}'; // "1" sampai "9"

const routes = {
  "1": "/webhook/wf-detailing",
  "2": "/webhook/wf-pov",
  "3": "/webhook/wf-storyboard",
  "4": "/webhook/wf-livehost",
  "5": "/webhook/wf-imageprompt",
  "6": "/webhook/wf-faceless-spiritual",
  "7": "/webhook/wf-whatif-fusion",
  "8": "/webhook/wf-3d-medical",
  "9": "/webhook/wf-clay-video"
};

return { target_webhook: routes[workflowId] || routes["1"], workflow_id: workflow_id };
```

**Setiap Workflow menerima payload standar:**
```json
{
  "workflow_id": "6",
  "concept": "{{selected_concept}}",
  "product_name": "{{usp_extractor.product_name}}",
  "price": "{{usp_extractor.price}}",
  "top_3_usp": "{{usp_extractor.top_3_usp}}",
  "emotional_benefit": "{{usp_extractor.emotional_benefit}}",
  "pain_point": "{{usp_extractor.pain_point}}",
  "sensory_keywords": "{{usp_extractor.sensory_keywords}}",
  "compliance_notes": "{{usp_extractor.compliance_notes}}",
  "target_audience": "ibu rumah tangga 30-50 tahun",
  "aspectRatio": "9:16",
  "language": "Indonesian"
}
```

---

## WF 1-5: DAPUR PRODUKSI UMUM

(System prompts identik dengan Master Blueprint v1 — gunakan file sebelumnya. Ringkasan upgrade yang sudah aktif:)

| WF | Upgrade Aktif |
|----|--------------|
| 1. Detailing | Sensory & Texture Mapping per shot |
| 2. POV Shots | Micro-Expressions & Body Language per segment |
| 3. Storyboard | 3-Second Retention Rule + Text Overlay Strategy |
| 4. Live Host | FOMO Stacking 4-layer + Troll Handling 5 tipe |
| 5. Image Prompt | Camera Specs & Lighting Exactness (lens, f-stop, color temp) |

---

## WF 6: FACELESS SPIRITUAL (NEW — DEEP SPEC)

- Configure agency, blueprint, content, domain, master settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Node W6.2: LLM

```
Name : llm_faceless
Temp : 0.6
Format: json_object
Max : 4096
```

**System Prompt:**
```
Kamu adalah Penulis Konten Reflektif Spiritual untuk TikTok faceless content.

## IDENTITAS KONTEN
Gaya: puitis, reflektif, tenang, penuh makna
Visual: tanpa wajah (hands only, nature, product close-up, atmospheric)
Audio: voiceover naratif dengan pacing sangat lambat dan bernapas

## ATURAN SSML UNTUK ELEVENLABS (KRITIS)
Narasi HARUS menggunakan SSML markup agar ElevenLabs menghasilkan voiceover yang bernapas natural.

WAJIB GUNAKAN:
- <break time="0.8s"/> setelah setiap kalimat pendek
- <break time="1.2s"/> setelah kalimat emosional/reflektif
- <break time="1.5s"/> sebelum reveal produk
- <break time="0.5s"/> antara frasa dalam 1 kalimat panjang

CONTOH BENAR:
"Ada hal-hal yang nggak bisa dibeli.<break time='1.2s'/>Tapi bisa dijaga.<break time='0.8s'/>Kayak warisan.<break time='0.5s'/>Kayak tradisi.<break time='1.5s'/>Dan ini, adalah cara gue menjaganya."

CONTOH SALAH:
"Ada hal-hal yang nggak bisa dibeli. Tapi bisa dijaga. Kayak warisan. Kayak tradisi. Dan ini adalah cara gue menjaganya."
(Tanpa break = robot, rushed, kehilangan feel spiritual)

## ATURAN BAHASA
- Kalimat pendek, 5-10 kata per kalimat
- Metafor alam dan waktu ("seperti sungai yang mengalir", "turun-temurun")
- Nada: bijaksana tapi humble, bukan menggurui
- JANGAN: bahasa iklan, CTA agresif, klaim kesehatan
- CTA harus subtle: "Link ada di bawah, kalau kamu juga ingin menjaga."
```

**User Prompt:**
```
Produk: {{wf_trigger.body.product_name}} — {{wf_trigger.body.price}}
Konsep: {{wf_trigger.body.concept}}
USP: {{wf_trigger.body.top_3_usp}}
Emosi: {{wf_trigger.body.emotional_benefit}}
Sensory: {{wf_trigger.body.sensory_keywords}}
Target: {{wf_trigger.body.target_audience}}

{
  "content_type": "faceless_spiritual",
  "total_duration_seconds": 30,
  "scenes": [
    {
      "scene_number": 1,
      "phase": "OPENING_REFLECTION",
      "duration_seconds": 8,
      "visual_direction": "(faceless: hands, nature, texture — sangat deskriptif)",
      "narration_ssml": "(WAJIB pakai <break time/> tags)",
      "mood_lighting": "",
      "ambient_sound": "",
      "camera_movement": ""
    }
  ]
}
```

---

## WF 7: WHAT IF FUSION (NEW — DEEP SPEC)

- Configure agency, blueprint, content, domain, master settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Node W7.2: LLM

```
Name : llm_whatif
Temp : 0.85
Format: json_object
```

**System Prompt:**
```
Kamu adalah Konseptor Visual "What If" — spesialis membuat konten yang mengeksplorasi pertanyaan "Bagaimana kalau [produk ini] bertemu [elemen tak terduga]?"

## FORMAT WAJIB: 4-SCENE CAROUSEL
Setiap output HARUS mengikuti alur 4 scene ini:

Scene 1 — BASE: Tampilkan produk asli apa adanya dalam konteks normalnya
Scene 2 — ELEMENT: Perkenalkan elemen fusion (budaya, era, material, gaya)
Scene 3 — FUSION: Gabungkan produk + elemen menjadi visual baru yang stunning
Scene 4 — DETAIL: Macro close-up detail hasil fusion yang paling menarik

## ATURAN KREATIVITAS
- Fusion harus SURPRISING tapi masuk akal (bukan random absurd)
- Elemen fusion bisa: era waktu, budaya, material, genre seni, teknologi
- Contoh: "What if madu hutan Kalimantan dikemas dalam apothecary Victorian?"
- Contoh: "What if minyak pusaka dijual di laboratorium futuristik Wakanda?"
- Produk asli HARUS tetap dikenali — jangan transform sampai hilang identitas
- Visual description harus sangat detail untuk AI image generation

## ATURAN HOOK
Hook HARUS format: "What if [produk] [versi fusion]?"
Contoh: "What if madu hutan Kalimantan dijual di apothecary Victorian?"
```

**User Prompt:**
```
Produk: {{wf_trigger.body.product_name}} — {{wf_trigger.body.price}}
USP: {{wf_trigger.body.top_3_usp}}
Sensory: {{wf_trigger.body.sensory_keywords}}
Konsep awal: {{wf_trigger.body.consep}}
Buat 2 variasi What If Fusion, masing-masing 4-scene carousel:

{
  "whatif_variants": [
    {
      "variant_name": "",
      "hook": "What if [produk] [fusion element]?",
      "fusion_element": "",
      "scenes": [
        {
          "scene": "BASE",
          "duration_seconds": 5,
          "visual_prompt": "(detail untuk AI image generation, English, 80-120 words)",
          "text_overlay": "",
          "transition": ""
        },
        {
          "scene": "ELEMENT",
          "duration_seconds":  5,
          "visual_prompt": "",
          "text_overlay": "",
          "transition": ""
        },
        {
          "scene": "FUSION",
          "duration_seconds": 8,
          "visual_prompt": "",
          "text_overlay": "",
          "transition": ""
        },
        {
          "scene": "DETAIL",
          "duration_seconds": 7,
          "visual_prompt": "",
          "text_overlay": "",
          "transition": ""
        }
      ],
      "narration_script": "",
      "bgm_mood": ""
    }
  ]
}
```

---

## WF 8: 3D MEDICAL — COMPLIANCE MODE (NEW — DEEP SPEC)

- Configure agency, blueprint, content, domain, master settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Node W8.2: LLM

```
Name : llm_3dmedical
Temp : 0.5
Format: json_object
```

**System Prompt:**
```
Kamu adalah Kreator Konten 3D CGI Chibi untuk produk kesehatan/herbal di TikTok.

## VISUAL STYLE: 3D CHIBI CGI
- Karakter: 3D chibi (kepala besar, badan kecil, mata besar ekspresif)
- Environment: 3D rendered, warna pastel cerah, rounded shapes
- Produk: TETAP REALISTIS (bukan chibi) — ini kunci credibility)
- Mixing: karakter chibi berinteraksi dengan produk realistis

## COMPLIANCE MODE: ANTI-BANNED TIKTOK (KRITIS)

- Configure agency, blueprint, content, domain, master settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results

### KATA TERLARANG → PENGGANTI WAJIB:
| JANGAN PERNAH GUNAKAN | GUNAKAN INI |
|------------------------|-------------|
| obat | perawatan alami |
| menyembuhkan | membantu merawat |
| mengobati | menjaga |
| sembuh | terasa lebih nyaman |
| sakit | kurang nyaman |
| penyakit | kondisi |
| khasiat | manfaat yang dirasakan |
| anti-kanker | kaya antioksidan alami |
| menurunkan gula darah | mendukung keseimbangan tubuh |
| menyembuhkan batuk | membantu melegakan tenggorokan |
| obat tradisional | ramuan warisan |
| suplemen | pendamping gaya hidup sehat |
| dosis | takaran yang disarankan |
| efek samping | hal yang perlu diperhatikan |
| anti-kanker | kaya antioksidan alami |
| minyak pusaka | dos 150mg (TIDAK over 150mg per hari) |

### COMPLIANCE CHECK WAJIB:
Sebelum output, scan seluruh narasi dan pastikan:
1. TIDAK ADA satupun kata dari kolom "JANGAN" di atas
2. Semua klaim bersifat PENGALAMAN PERSONAL ("gue ngerasa...", "gue ngerasa...")
3. Tidak ada janji kesembuhan
4. Tidak ada angka medis tanpa sumber
5. Sertakan disclaimer_note: "Bukan pengganti saran medis profesional"

claim_level HARUS: "descriptive_comfort_only"
```

**User Prompt:**
```
Produk: {{wf_trigger.body.product_name}} — {{wf_trigger.body.price}}
USP: {{wf_trigger.body.top_3_usp}}
Emosi: {{wf_trigger.body.emotional_benefit}}
Pain Point: {{wf_trigger.body.pain_point}}
Compliance Notes: {{wf_trigger.body.compliance_notes}}
Target: {{wf_trigger.body.target_audience}}

{
  "content_type": "3d_medical_chibi",
  "claim_level": "descriptive_comfort_only",
  "disclaimer_note": "Bukan pengganti saran medis profesional",
  "scenes": [
    {
      "scene_number": 1,
      "duration_seconds": 5,
      "chibi_action": "(apa yang karakter chibi lakukan)",
      "product_appearance": "(produk realistis, BUKAN chibi)",
      "narration": "(WAJIB compliance-safe language)",
      "visual_3d_prompt": "(English, untuk 3D render)",
      "compliance_check": "PASS/FAIL + catatan"
    }
  ],
  "full_narration_compiled": "(semua narasi digabung, sudah compliance-safe)",
  "compliance_scan_result": {
    "banned_words_found": [],
    "status": "CLEAN"
  }
}
```

---

## WF 9: CLAY VIDEO AI — STRICT MODE (NEW — DEEP SPEC)

- Configure agency, blueprint, content, domain, master settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Node W9.2: LLM

```
Name : llm_clay
Temp : 0.7
Format: json_object
```

**System Prompt:**
```
Kamu adalah Art Director spesialis Clay Art / Claymation / Plasticine Animation untuk konten TikTok.

## CLAY MASTER FORMULA (WAJIB SETIAP SCENE)

- Configure agency, blueprint, content, domain, master settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### TEKSTUR SIDIK JARI (Fingerprint Texture)
Setiap elemen clay HARUS memiliki visible fingerprint impressions — ini yang membedakan clay art dari 3D render biasa.
- Karakter: permukaan tidak mulus, ada bekas tekanan jari
- Environment: tanah, pohon, rumah — semua dari clay dengan tekstur handmade
- Warna: slightly uneven, seperti hand-mixed clay

### DIORAMA WORLD
Seluruh dunia dalam video adalah miniatur diorama clay:
- Background: clay landscape dengan horizon yang terlihat ujung mejanya
- Skala: semua terlihat seperti meja diorama yang bisa dipegang tangan
- Lighting: dramatic studio lighting dari atas, seperti menerangi diorama di meja

### ATURAN KETAT PRODUK:
⚠️ JIKA VIDEO ADALAH REVIEW/SHOWCASE PRODUK:
- Produk WAJIB realistis (foto/render realistis) — BUKAN clay
- Hanya ENVIRONMENT dan KARAKTER yang clay
- Produk muncul sebagai "benda nyata di dunia clay"
- Ini menciptakan kontras visual yang kuat dan menjaga kredibilitas produk
- Ini menciptakan kontras visual yang kuat dan menjaga kredibilitas produk

⚠️ JIKA VIDEO ADALAH PURE ENTERTAINMENT:
- Boleh semua clay termasuk versi clay produk
- Tapi tetap harus ada 1 scene produk realistis di akhir
- Ini menciptakan kontras visual yang kuat dan menjaga kredibilitas produk

### CLAY COLOR PALETTE
- Warm tones: terracotta, mustard, sage, cream
- Aksen: muted red, dusty blue
- HINDARI: neon, chrome, metallic (tidak cocok clay aesthetic)
```

**User Prompt:**
```
Produk: {{wf_trigger.body.product_name}} — {{wf_trigger.body.price}}
USP: {{wf_trigger.body.top_3_usp}}
Sensory: {{wf_trigger.body.sensory_keywords}}
Content purpose: "product_review" atau "entertainment"
Target: {{wf_trigger.body.target_audience}}

{
  "content_type": "clay_video_ai",
  "content_purpose": "product_review",
  "product_render_mode": "realistic (BUKAN clay)",
  "scenes": [
    {
      "scene_number": 1,
      "duration_seconds": 0,
      "clay_world_description": "(diorama environment, WAJIB fingerprint texture)",
      "clay_character_action": "(apa yang karakter clay melakukan apa)",
      "product_appearance": "(REALISTIS jika review, clay jika entertainment)",
      "narration": "",
      "visual_prompt_for_ai": "(English, detail clay texture, diorama, lighting)",
      "camera_movement": ""
    }
  ],
  "clay_color_palette": ["", "", ""],
  "diorama_description": ""
}
```

**Output — Mock Minyak Pusaka (Clay Review):**
```json
{
  "scenes": [
    {
      "scene_number": 1,
      "clay_world_description": "Diorama ruangan Jawa dari clay — dinding clay dengan tekstur sidik jari visible, lantai clay terracotta, jendela kecil clay dengan cahaya warm masuk. Skala miniatur di atas meja.",
      "clay_character_action": "Karakter clay pria tua Jawa (blangkon, batik) duduk bersila di depan keris clay di atas meja kecil",
      "product_appearance": "REALISTIS: botol minyak pusaka foto-realistis berdiri di samping — kontras kuat dengan dunia clay di sekitarnya",
      "narration": "Di dunia yang serba instan, ada yang masih merawat dengan cara lama.",
      "visual_prompt_for_ai": "Claymation diorama scene, miniature Javanese room made of plasticine clay with visible fingerprint textures on every surface. Small clay figure of elderly Javanese man in clay batik sitting cross-legged. REALISTIC photographic bottle of herbal oil placed in the clay world creating strong contrast. Warm dramatic overhead studio lighting illuminating the diorama. Shallow depth of field. Terracotta and mustard color palette. Stop-motion aesthetic.",
      "camera_movement": "slow orbit around diorama, 3%"
    }
  ],
  "clay_color_palette": ["terracotta", "mustard", "sage green"],
  "diiorama_description": "Miniatur ruangan empu keris Jawa, lengkap dengan clay anvil, clay keris collection di dinding, dan satu botol minyak pusaka REALISTIS sebagai focal point"
}
```

---

# ══════════════════════════════════════════
# PHASE 4: PRODUCTION & HITL
# ══════════════════════════════════════

### Node P4.1: Vision QC
(Same as Master Blueprint v1 — GPT-4o Vision, 7 criteria, min score 8.3)
```
{{vision_qc.qc_status}} → "PASS"/"FAIL"
```

### Node P4.2: Telegram HITL Gate

**Payload:**
```json
{
  "chat_id": "{{ENV.TELEGRAM_CHAT_ID}}",
  "text": "🎬 REVIEW — {{usp_extractor.product_name}}\nWorkflow: {{workflow_router.workflow_id}}\n\n🪝 HOOK:\n\"{{viral_editor.hook_terbaik}}\"\n\n📜 SCRIPT:\n{{viral_editor.full_final_script}}\n\n⭐ Score: {{viral_editor.viral_score}}/10",
  "reply_markup": {
    "inline_keyboard": [
      { "text": "🟢 Approve & Render", "callback_data": "approve_{{JOB_ID}}"},
      { "text": "🟡 Revisi Hook", "callback_data": "revise_hook_{{JOB_ID}}"},
      { "text": "🔴 Batalkan", "callback_data": "cancel_{{JOB_ID}}"}
    ]
  }
}
```

### Node P4.3: Prompt Engineer → Google Flow Protocol
(Same as v1 — buat prompt Google Flow protocol)

### Node P4.4: Iterator → Parallel Kling + ElevenLabs

**SSML Handling untuk WF 6 (Faceless Spiritual):**

Jika `workflow_id === "6"`, narration sudah mengandung SSML tags.
ElevenLabs menerima SSML secara native — langsung kirim `narration_ssml` field tanpa strip tags.

```javascript
// Iterator code — detect SSML
const isSSML = scene.narration_ssml && scene.narration_ssml.includes('<break');
const speechText = isSSML ? scene.narration_ssml : scene.direct_speech;
const useSSML = isSSML;

// ElevenLabs payload adjustment
elevenlabs_payload: {
    text: speechText,
    model_id: "eleven_multilingual_v2",
    // ElevenLabs auto-detects SSML tags in text
}
```

---

# ════════════════════════════════════════
# PHASE 5: FINAL MILE (AUTO-STITCHING)
# ════════════════════════════════════

### Node P5.1: Creatomate — WITH BGM LAYER

```
Name : creatomate_stitch
Type : HTTP Request
Method : POST
URL : https://api.creatomate.com/v1/renders
```

**Payload — 4 Video + 4 Audio + 1 BGM Track:**

```json
{
  "output_format": "mp4",
  "width": 1080,
  "height":  1920,
  "frame_rate": 30,
  "elements": [
    {
      "type": "composition",
      "track": 1,
      "elements": [
        {
          "type": "video",
          "track": 1,
          "source": "{{kling_poller.video_urls[0]}}",
          "time": 0,
          "duration": {{durations[0]}},
          "volume": "0%",
          "fit": "cover"
        },
        {
          "type": "video",
          "track": 2,
          "source": "{{kling_poller.video_urls[1]}}",
          "time": {{durations[0]}},
          "duration": {{durations[1]}},
          "volume": "0%",
          "fit": "cover"
        },
        {
          "type": "video",
          "track":  1,
          "source": "{{kling_poller.video_urls[2]}}",
          "times: {{durations[0] + durations[1]}},
          "duration": {{durations[2]}},
          "volume": "0%",
          "fit": "cover"
        },
        {
          "type": "video",
          "track": 1,
          "source": "{{kling_poller.video_urls[3]}}",
          "times: {{durations[0] + durations[1] + durations[2]}},
          "duration": {{durations[3]}},
          "volume": "0%",
          "fit": "cover"
        },
        {
          "type": "audio",
          "track": 2,
          "source": "{{audio_urls[0]}}",
          "time": 0,
          "duration": {{durations[0]}",
          "volume": "100%"
        },
        {
          "type": "audio",
          "track": 2,
          "source": "{{audio_urls[1]}}",
          "time": {{durations[0]}},",
          "duration": {{durations[1]}},
          "volume": "100%"
        },
        {
          "type": "audio",
          "track": 2,
          "source": "{{audio_urls[2]}}",
          "time": {{durations[0] + durations[1] + durations[2]}},
          "duration": {{durations[2]}},
          "volume": "100%"
        },
        {
          "type": "audio",
          "track": 3,
          "source": "{{ENV.BGM_URL}}",
          "time": 0,
          "duration": "end",
          "volume": "8%",
          "audio_fade_in": 2,
          "audio_fade_out": 3
        }
      ]
    }
  ]
}
```

---

## VARIABLES FLOW MAP (End-to-End)

```
PHASE 0 → PHASE 1-2:
{{creative_director_ideation.ideas[0].concept}} → {{wh_extract.body.selected_concept}}
{{creative_director_ideation.ideas[0].best_workflow}} → {{workflow_router.workflow_id}}

PHASE 1-2 → PHASE 3 (ALL 9 WORKFLOWS):
{{usp_extractor.product_name}} → {{wf_trigger.body.product_name}}
{{usp_extractor.price}} → {{wf_trigger.body.price}}
{{usp_extractor.top_3_usp}}}} → {{wf_trigger.body.top_3_usp}}
{{usp_extractor.emotional_benefit}} → {{wf_trigger.body.emotional_benefit}}
{{usp_extractor.pain_point}}}} → {{wf_trigger.body.sensory_keywords}}
{{usp_extractor.compliance_notes}} → {{wf_trigger.body.compliance_notes}}

PHASE 3 → PHASE 4:
{{llm_[workflow].output.scenes}} → {{viral_editor.input}}
{{viral_editor.full_final_script}} → {{telegram_hitl.text}}
{{viral_editor.hook_terbaik}} → {{telegram_hitl.hook_terbaik}}

PHASE 4 → PHASE 5:
{{prompt_engineer.render_scenes}} → {{scene_iterator.input}}
{{scene_iterator.tasks[N]}} → {{kling_render.payload}} + {{elevenlabs_tts.payload}}
{{kling_poller.video_urls}} → {{creatomate_stitch.video_sources}}
{{elevenlabs_tts.audio_files}} → {{creatomate_stitch.audio_sources}}

PHASE 5 → OUTPUT:
{{creatomate_stitch.output.url}} → final video URL
→ auto-save ke Notion/GSheets
→ notify ke Telegram
```

---

# RULES
- JSON Sanitizer WAJIB setelah setiap LLM Node
- WF 6 narasi WAJIB pakai SSML breaks — tanpa ini voiceover terdengar rushed
- WF 8 compliance check WAJIB — 1 kata terlarang = auto-revise sebelum output
- WF 9 produk WAJIB realistis jika content_purpose = "product_review"
- Creatomate video volume SELALU 0%, audio voice SELUU 100%, BGM SELU 8%

---

**Skill Location:** skills/ai-content-agency-v2/SKILL.md
**Installed:** NOW ✅

**Documentation:** Full workflows above ready to use
**Status:** Ready to integrate with 9 specialized workflows for TikTok/YouTube automation

## How to Use

1. Define campaign objective and target KPIs
2. Set up tracking and attribution (UTMs, pixels, events)
3. Create campaign assets (copy, creatives, landing pages)
4. Launch with small budget for testing
5. Monitor metrics daily, optimize underperformers
6. Scale winners, pause losers, document learnings

## When NOT to Use

- Task is about sales, not marketing (use sales skills)
- Task is about product development (use product skills)
- You need to analyze marketing data (use analytics skills)
- Task is about customer support (use support skills)
- You don't have marketing assets
- Task requires legal review (consult legal)


## Red Flags

- **Metrics declining 3+ days**: Investigate funnel leaks or audience fatigue
- **Ad spend with zero conversions**: Pause and review targeting/creative
- **Email open rates below 15%**: Subject lines or sender reputation issue
- **Bounce rate above 70%**: Landing page mismatch or slow load times
- **Attribution gaps**: Missing UTM parameters or broken tracking pixels

## Verification

- Run A/B test with control group before full rollout
- Verify tracking pixels fire correctly on all conversion pages
- Check UTM parameters parse correctly in analytics dashboard
- Confirm email deliverability via seed list test
- Validate landing page speed (target < 3s load time)
