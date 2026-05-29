---
name: content-validation-workflow
description: Content Workflow: Generate Sample → Human Review → Batch Production. Use when relevant to this domain.
---

# Content Workflow: Generate Sample → Human Review → Batch Production

## Apa Ini?

Workflow untuk memastikan kualitas konten sebelum diproduksi dalam batch besar. 

**Masalah:** AI generated image/video kadang:
- Kelihatan AI banget
- Tidak sesuai brand voice
- Quality rendah
- Timing tidak pas
- Caption terasa robot

**Solusi:** Generate 1 sample per product → Review manual → Approval → Lalu batch production

---

## Workflow

```
1. PLAN (Month plan created)
   ↓
2. SAMPLE GENERATION (1 sample per content type)
   ↓
3. VALIDATION (Human review via chat)
   ├─ APPROVE → Generate batch (50-100 pieces)
   └─ REJECT → Edit & Regenerate 1 sample
   ↓
4. BATCH PRODUCTION (Approved samples × 50x scale)
   ↓
5. SCHEDULE (Post content via PostBridge)
```

---

## Quality Checklist

Sebelum approve konten, cek:

### ✅ Image Quality (Static)
- [ ] Clear, high resolution
- [ ] Text readable (if any text overlay)
- [ ] Colors match brand (Jendralbot colors)
- [ ] Not too "AI-looking" (unnatural textures)
- [ ] Subject in focus
- [ ] Composition balanced

### ✅ Video Quality (Faceless)
- [ ] Smooth motion (not glitchy)
- [ ] Text overlay visible & readable
- [ ] Voice over clear (no robotic distortion)
- [ ] Music volume appropriate (30-40% of voice)
- [ ] Timing aligns with audio cues
- [ ] Hook visible in first 3 seconds
- [ ] CTA clear at end

### ✅ Content Quality (All types)
- [ ] Hook strong (first 3 seconds grabs attention)
- [ ] Message clear (not confusing)
- [ ] Tone matches platform (TikTok: energetic, YouTube: educational)
- [ ] CTA natural (pushy at the end, not throughout)
- [ ] Hashtag relevant & trending
- [ ] Caption length appropriate (not too long)

### ✅ Brand Consistency
- [ ] Voice consistent with previous posts
- [ ] Product info accurate
- [ ] URLs correct & working
- [ ] Hashtag strategy followed
- [ ] Emojis match tone

---

## Tool Functions

- Configure batch, content, domain, generate, human settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### 1. generate_sample(product, content_type, variant=1)

Generate 1 sample content for review.

**Input:**
- `product`: Product key (e.g., "guru_pintar_ai")
- `content_type`: Content type (e.g., "faceless_info_benefit")
- `variant`: Variant ID (default: 1)

**Output:**
- Script + visual breakdown + voice over text + music suggestion
- Quality checklist pre-filled with "⚠️ PENDING REVIEW"

**Example:**
```python
generate_sample("guru_pintar_ai", "faceless_info_benefit", v1)
# Returns:
{
  "script": "...",
  "visual_plan": "...",
  "checklist": {
    "image_quality": "⚠️ PENDING",
    "text_overlay": "⚠️ PENDING",
    "hook_strength": "⚠️ PENDING",
    "cta_clarity": "⚠️ PENDING"
  }
}
```

### 2. request_approval(product, content_type, variant, sample_output)

Send sample content to human for review.

**Input:**
- `product`: Product key
- `content_type`: Content type
- `variant`: Variant ID
- `sample_output`: Generated content to review

**Output:**
- Approval request message
- Checklist for manual review

**Example:**
```python
request_approval("guru_pintar_ai", "faceless_info_benefit", v1, sample)
# Sends message:
"SAMP KONTEN: Guru Pintar AI - Faceless Info Benefit v1

Review quality sebelum batch production:

✅ Image Quality: [ ] CLEAR & HIGH RES
✅ Text Overlay: [ ] Visible & Readable
✅ Hook Strength: [ ] Strong in first 3s
✅ CTA Clarity: [ ] Clear at end

Respon:
- 'ACC' → TOLAK batch production sekarang
- 'EDIT: [instruksi]' → Regulate sampel
- 'SKIP' → Skip ke sampel lain"

```

### 3. save_approval(product, content_type, variant, status, feedback="")

Save approval status to file.

**Input:**
- `product`: Product key
- `content_type`: Content type
- `variant`: Variant ID
- `status`: "APPROVED" | "REJECTED" | "PENDING"
- `feedback`: Human feedback text

**Output:**
- Save to `content_approvals.json`

**Example:**
```python
save_approval("guru_pintar_ai", "faceless_info_benefit", v1, "APPROVED", "Good, text overlay readable")
# Saves to file:
{
  "guru_pintar_ai_faceless_info_benefit_v1": {
    "status": "APPROVED",
    "feedback": "Good, text overlay readable",
    "timestamp": "2026-03-07 21:15:00"
  }
}
```

### 4. generate_batch_from_approved(product, content_type, quantity=50)

Generate batch content FROM APPROVED samples.

**Input:**
- `product`: Product key
- `content_type`: Content type
- `quantity`: Batch size (default: 50)

**Output:**
- Generate `quantity` variants of APPROVED content
- Save to scheduled content queue

**Example:**
```python
generate_batch_from_approved("guru_pintar_ai", "faceless_info_benefit", 50)
# Result:
- 50 approved faceless videos ready for posting
- Saved to scheduled_content.json
```

---

## File Structure

```
~/.openclaw/workspace/
├── content/
│   ├── samples/              # Review samples (1 per content type)
│   │   ├── guru_pintar_ai_faceless_info_benefit_v1.txt
│   │   ├── belanja_duit_balik_faceless_quick_tips_v1.txt
│   │   └── ...
│   ├── samples_approved.json  # Approval status
│   ├── scheduled_content.json # Queue for posting
│   └── posted_content.json   # History
│
└── scripts/
    └── content_validator_workflow.py  # Main workflow script
```

---

## Usage Example

```python
# STEP 1: Generate 1 sample per product
samples = []
for product in ["guru_pintar_ai", "belanja_duit_balik"]:
    sample = generate_sample(product, "faceless_info_benefit", v1)
    samples.append((product, sample))

# STEP 2: Request approval for each
for product, sample in samples:
    request_approval(product, "faceless_info_benefit", v1, sample)
    # Wait for human response...

# STEP 3: After approval, generate batch
approved_products = load_approved_samples()
for product in approved_products:
    generate_batch_from_approved(product, "faceless_info_benefit", 50)

# STEP 4: Schedule all approved content
schedule_all_approved()
```

---

## Quality Metrics

When reviewing samples, look for:

### 🔥 Green Flag (APPROVE)
- Natural voice (not robotic)
- Clear, readable text
- Strong hook in first 3 seconds
- Professional quality image/video
- On-brand tone
- Clear CTA at end

### ⚠️ Yellow Flag (REQUEST EDITS)
- Minor text issues (typo, spacing)
- Slight audio balance issues
- Small timing adjustments needed
- Hashtag improvements

### 🔴 Red Flag (REJECT)
- Obvious AI artifacts/generation errors
- Unreadable text (blurry, wrong colors)
- Weak/missing hook
- Confusing message
- Robot voice
- Wrong product URL/info

---

## Human Review Process

- Configure batch, content, domain, generate, human settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### When receiving sample review request:

1. **Review the content**
   - Read script for tone & clarity
   - Check visual plan (text overlays, b-roll)
   - Imagine final result

2. **Check against Quality Checklist**
   - Image/Video quality
   - Text readability
   - Hook strength
   - CTA clarity
   - Brand consistency

3. **Make decision**
   - **ACC** → Approved for batch production
   - **EDIT: [instruksi]** → Regenerate with specific feedback
   - **SKIP** → Move to next sample (keep pending)

4. **Feedback format**
   - Be specific: "Text too dark, make white"
   - Be actionable: "Hook needs to be more energetic"
   - Avoid vague feedback: "Change the vibe"

---

## Batch Production Strategy

- Configure batch, content, domain, generate, human settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### For Month 1 (Foundation Phase):
- Generate 3 samples per product (variations)
- Review all 3 samples
- Choose best 2 per product
- Generate batch: Best sample × 20-30 pieces

### For Month 2+ (Scale Phase):
- Generate 1 sample per content type
- Quick review (since quality known)
- Generate batch: Approved sample × 50-100 pieces

### Quality vs Quantity:
- **Quality first**: Better to post 10 great posts than 50 mediocre posts
- **Scale later**: Once quality benchmark established, can safely scale

---

## Integration with Workflow

This validator integrates with:

- **content-creator**: Generate initial content
- **content-generator**: Create AI videos from scripts
- **tiktok-automation**: Post approved content to TikTok
- **post-bridge-social-manager**: Post to all 5 platforms

---

## Key Features

✅ Quality control before bulk production
✅ Human-in-the-loop approval process
✅ Version control (approved samples saved)
✅ Rejection history (learn from rejected samples)
✅ Batch scaling from approved templates
✅ Reduced waste (no posting bad content)

---

## Why This Matters

**Without validator:**
- Generate 100 videos → 70 bad quality → Waste
- Delete 70 videos → Redo entire generation
- Timeline delays + frustration

**With validator:**
- Generate 3 samples → Review → Approve 2
- Scale 2 approved samples to 100 pieces
- 100 quality videos → Better engagement → Higher ROI

---

## Summary

**This workflow ensures:**
1. ✅ Quality before quantity
2. ✅ Human approval before AI production
3. ✅ Reduced waste & rework
4. ✅ Consistent brand quality
5. ✅ Faster iteration (learn from approved samples)

**Result:** 100+ quality posts/month instead of 1000+ bad posts/month

---

**Implementation Priority: HIGH**
**Why:** Prevent wasted production time & effort

## How to Use

1. Understand the requirement and existing codebase patterns
2. Design the solution with error handling and testability in mind
3. Implement incrementally with tests for each change
4. Verify against expected outcomes (manual and automated)
5. Document usage, edge cases, and integration points
6. Review with team before merging to shared branches

## Red Flags

- **Skipping tests to ship faster**: Untested code breaks in production when you least expect it
- **No error handling in production code**: Unhandled errors crash services and lose user data
- **Hardcoded configuration values**: Hardcoded values prevent environment switching and leak secrets
- **Ignoring security implications**: Missing input validation, auth bypasses, and injection vulnerabilities
- **Over-engineering simple solutions**: Premature abstraction adds complexity without proportional benefit

## Verification

- All tests pass after code changes (unit, integration, e2e as appropriate)
- Error handling covers documented failure modes and edge cases
- Configuration uses environment variables or config files, not hardcoded values
- Security-sensitive code (auth, payments, API) has explicit review
- Code follows project conventions (naming, patterns, structure)
