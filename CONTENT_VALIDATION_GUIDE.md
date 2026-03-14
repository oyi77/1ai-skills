# CONTENT VALIDATION WORKFLOW - QUICK START

## Problem Solved ✅

**Anda:**
- AI generates 100 images/videos
- 70% are bad quality or "terlalu AI-lah"
- Wasted time & production cost

**Dengan Validation Workflow:**
- Generate 1 sample per product
- Review manual → ACC/EDIT/SKIP/REJECT
- Scale ONLY approved samples to 50-100 pieces
- Hanya quality content yang diposting! 🎯

---

## Cara Pakai (Step-by-Step)

### STEP 1: Generate Samples

```bash
# Request approval for content types
python3 scripts/content_validator.py

# This generates 1 sample automatically and shows:
# - Product info, Script, Visual breakdown
# - Quality checklist
# - Instructions for ACC/EDIT/SKIP/REJECT
```

**Yang dilakukan:**
- Sample yang di-generate tersimpan di: `content/samples/guru_pintar_ai_faceless_info_benefit_v1.txt`
- Status: ⚠️ PENDING
- Checklist: Semua item masih PENDING

---

### STEP 2: Review Sample

**Buka file sample:**
```
/home/openclaw/.openclaw/workspace/content/samples/guru_pintar_ai_faceless_info_benefit_v1.txt
```

**Checklist (Manual Review):**

| Quality Item | Check | Penjelasan |
|--------------|-------|------------|
| Image Quality | [ ] Clear & High Res | Apakah gambar/bluray clear? |
| Text Overlay | [ ] Visible & Readable | Apakah teks terbaca? |
| Hook Strength | [ ] Strong in 3s | Apakah hook menarik? |
| CTA Clarity | [ ] Clear at end | Apakah CTA jelas? |
| Brand Voice | [ ] Matches Jendralbot | Apakah tone sesuai? |

---

### STEP 3: Approve / Edit / Reject

**Option A: APPROVE (ACC)**
```bash
python3 scripts/content_validator.py --approve guru_pintar_ai_faceless_info_benefit_v1 ACC
```
**Result:** ✅ Ready untuk batch production (50-100 pieces)

---

**Option B: REQUEST EDIT**
```bash
python3 scripts/content_validator.py --approve guru_pintar_ai_faceless_info_benefit_v1 EDIT Text overlay perlu putih lebih terang
```
**Result:** 📝 Feedback tersimpan, akan di-regenerate sesuai

---

**Option C: SKIP**
```bash
# Tidak perlu command
# Langsung generate sample lain yang lebih baik
```
**Result:** ⏭️ Sample tetap PENDING, bisa di-review lain kali

---

**Option D: REJECT**
```bash
python3 scripts/content_validator.py --approve guru_pintar_ai_faceless_info_benefit_v1 REJECT
```
**Result:** ❌ Jangan di-scale, generate ulang dari awal

---

### STEP 4: Generate Batch Production

**Hanya setelah sample APPROVED:**

```bash
python3 scripts/content_validator.py --batch guru_pintar_ai faceless_info_benefit 50
```

**Apa yang terjadi:**
- Load sample approved: `guru_pintar_ai_faceless_info_benefit_v1`
- Generate 50 variations dari template ini
- Simpan ke queue untuk posting
- Siap di-schedule via PostBridge!

---

## File Structure

```
workspace/
├── content/
│   ├── samples/
│   │   ├── guru_pintar_ai_faceless_info_benefit_v1.txt    # Review ini!
│   │   ├── belanja_duit_balik_faceless_quick_tips_v1.txt
│   │   └── ai_content_pro_carousel_v1.txt
│   ├── approvals.json  # Status: APPROVED / REJECTED / PENDING
│   └── scheduled.json    # Batch queue (50-100 pieces)
│
└── scripts/
    └── content_validator.py  # Workflow runner
```

---

## Daily Workflow

### Hari 1 (Planning Phase)

```bash
# 1. Generate semua samples untuk bulan ini
python3 scripts/content_validator.py

# 2. Request review untuk semua content types
# (Auto-generates 1 sample per product)

# 3. List all samples
python3 scripts/content_validator.py --list
```

**Hasil:**
- 1-5 samples untuk review
- File tersimpan di `content/samples/`
- Status: ⚠️ PENDING

---

### Hari 1-3 (Review Phase)

```bash
# Review setiap sample secara manual:
# - Buka file content/samples/NAMA_SAMPLE.txt
# - Check quality checklist
# - Respon: ACC / EDIT / SKIP / REJECT

# Contoh approval:
python3 scripts/content_validator.py --approve guru_pintar_ai_faceless_info_benefit_v1 ACC
```

**Hasil:**
- Approved disimpan ke `content/approvals.json`
- Feedback tersimpan (kalau REJECT/EDIT)
- Siap untuk batch production

---

### Hari 3-7 (Production Phase)

```bash
# Generate batch dari approved samples:
python3 scripts/content_validator.py --batch guru_pintar_ai faceless_info_benefit 50
python3 scripts/content_validator.py --batch belanja_duit_balik faceless_quick_tips 50

# Result: 100 approved pieces ready to post!
```

**Hasil:**
- 50-100 pieces per product
- Semua approved
- Queue di `content/scheduled.json`

---

### Hari 7+ (Posting Phase)

- Postbridge mengambil dari `content/scheduled.json`
- Auto-post ke 5 platforms (TikTok, IG, YT, FB, X)
- 12-50 posts/hari!

---

## Benefits 🎯

### Tanpa Validation Workflow:
```
Generate 100 AI konten → 70 gak layak → Waste!
Delete 70 → Regenerate → Again 70 gak layak → Frustrasi! 😫
```

### Dengan Validation Workflow:
```
Generate 1 sample → Review ✅ → Scale ke 50 pieces
100% approved → Posting kualitas tinggi! 🚀
```

---

## Quality Checklist (Detail)

### ✅ Image Quality
- [ ] Clear, sharp, tidak blur
- [ ] High resolution (1080p+ for video)
- [ ] Colors natural, tidak weird AI artifacts
- [ ] Subject in focus
- [ ] No distorted faces/objects

### ✅ Text Overlay
- [ ] White/bright color (visible on any background)
- [ ] Bold, readable font
- [ ] Not too small (minimum 400px width)
- [ ] Positioned at visible area (center or bottom)
- [ ] Not overlapping with important visual elements

### ✅ Hook Strength (First 3 Seconds)
- [ ] Grabs attention immediately
- [ ] Not boring or generic
- [ ] Uses shocking number or statement
- [ ] Clear what the video is about
- [ ] Encourages viewer to stay

### ✅ CTA Clarity (Last 3 Seconds)
- [ ] Clear call-to-action
- [ ] Link URL visible & working
- [ ] Not too pushy or spammy
- [ ] Natural placement
- [ ] Easy to follow

### ✅ Brand Voice
- [ ] Tone consistent with Jendralbot brand
- [ ] Friendly yet professional
- [ ] Not robotic or awkward
- [ ] Matches platform expectation (TikTok energik, YT edukatif)
- [ ] Indonesian natural language

---

## Quick Commands Reference

```bash
# Setup workflow (generate samples)
python3 scripts/content_validator.py

# View all samples
python3 scripts/content_validator.py --list

# View pending reviews
python3 scripts/content_validator.py --pending

# Approve sample
python3 scripts/content_validator.py --approve <sample_id> ACC

# Request edit
python3 scripts/content_validator.py --approve <sample_id> EDIT [feedback]

# Reject sample
python3 scripts/content_validator.py --approve <sample_id> REJECT

# Generate batch (50 pieces)
python3 scripts/content_validator.py --batch <product> <content_type> 50

# Generate batch (100 pieces)
python3 scripts/content_validator.py --batch <product> <content_type> 100
```

---

## Example Full Month Workflow

### Week 1: Plan & Sample
```
Day 1: Plan entire month content strategy
Day 2-3: Generate 3 samples per product (15 samples total)
Day 3-5: Review & approve all 15 samples
```

### Week 2-3: Batch Production
```
Day 6-7: Generate batch 50 pieces per approved sample
         (15 approved × 50 = 750 pieces total)
Day 7-14: Schedule all 750 pieces across platforms
```

### Week 4: Posting & Optimization
```
Day 15-30: Auto-post 750 pieces across 5 platforms
Check: Performance metrics
Iterate: Adjust strategy based on data
```

**Total:** 750 quality posts in month 1! 🚀

---

## Summary

✅ **Quality Control:** Manual review before bulk production
✅ **Reduced Waste:** Only produce approved content
✅ **Faster Iteration:** Learn from approved templates
✅ **Consistent Quality:** Brand voice maintained across all posts
✅ **Scalable:** Approved template → 50-100 variations easily

**Result:** High-quality posts every day! 🎯

---

**READY TO START?**

```bash
# Step 1: Generate samples
python3 scripts/content_validator.py

# Step 2: Review & approve
# (Open content/samples/*.txt files)

# Step 3: Generate batch
python3 scripts/content_validator.py --batch [product] [type] 50

# Step 4: Post!
# (PostBridge auto-posts from scheduled queue)
```