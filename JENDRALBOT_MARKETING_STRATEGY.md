# JENDRALBOT MARKETING STRATEGY - Full Implementation Guide

📅 Date: 2026-03-07
👤 For: Andik Veris (jendralbot)
🎯 Objective: Fully automated marketing for 6 products on lynk.id/jendralbot

---

## 📦 PRODUCTS OVERVIEW

| Product | Price | Link | Category | Target |
|---------|-------|------|----------|--------|
| **Starter AI Content** | Rp 49.000 | [link](https://lynk.id/jendralbot/xlymwzj2jylv) | Entry Level | Beginners, students |
| **Studio Marketplace Pro** | Rp 75.000 | [link](https://lynk.id/jendralbot/emne05mm7v25) | Mid Tier | E-commerce sellers |
| **Mesin Cetak Kuliner** | Rp 75.000 | [link](https://lynk.id/jendralbot/kzryk28dxmpx) | Mid Tier | Restaurants, food sellers |
| **AI Content Pro** | Rp 89.000 | [link](https://lynk.id/jendralbot/d70eo2x45em5) | Premium | Advanced creators, businesses |
| **Guru Pintar AI** | FREE | [link](https://lynk.id/jendralbot/6821op5e24kn) | Training | Everyone |
| **Belanja Duit Balik** | FREE | [link](https://lynk.id/jendralbot/kkjk0mv1vg7o) | Cashback | Shoppers |

---

## 🎯 MARKETING STRATEGY

### Phase 1: Awareness & Lead Generation (Weeks 1-2)
**Focus:** Build audience, capture leads
**Free Products First**
- Guru Pintar AI → Lead magnet for AI learners
- Belanja Duit Balik → Lead magnet for shoppers

### Phase 2: Consideration (Weeks 3-4)
**Focus:** Show value, drive first sales
**Entry Level Product**
- Starter AI Content → First purchase (Rp 49k)
- Cross-sell FREE products to start conversation

### Phase 3: Conversion (Weeks 5-6+)
**Focus:** Upsell higher-ticket products
**Mid Tier & Premium**
- Studio Marketplace Pro → E-commerce (Rp 75k)
- Mesin Cetak Kuliner → Culinary (Rp 75k)
- AI Content Pro → Premium upsell (Rp 89k)

---

## 📱 PLATFORM STRATEGY

### Primary Platforms (80% effort)
```
TikTok (Viral)
├─ Content Type: Short-form videos (60s)
├─ Best Times: 07:00, 12:00, 18:00, 21:00
├─ Frequency: 2-3 posts/day
└─ Objective: Viral reach

Instagram (Visual)
├─ Content Type: Carousel (5-10 slides), Reels
├─ Best Times: 07:00, 12:00, 19:00
├─ Frequency: 2 posts/day
└─ Objective: Product showcase

LinkedIn (B2B)
├─ Content Type: Professional posts
├─ Best Times: 07:00, 12:00, 17:00
├─ Frequency: 1 post/day
└─ Objective: Business credibility
```

### Secondary Platforms (20% effort)
```
X (Twitter)
├─ Content Type: Threads, tweets
├─ Best Times: 09:00, 12:00, 15:00, 18:00
├─ Frequency: 3 posts/day
└─ Objective: Engagement & authority

YouTube (Shorts)
├─ Content Type: Short videos
├─ Best Times: 10:00, 14:00, 17:00
├─ Frequency: 1 post/day
└─ Objective: SEO discovery
```

---

## 🤖 FULL AUTOMATION WORKFLOW

### Step 1: Content Generation (Daily)

```bash
# Generate daily content plan
cd /home/openclaw/.openclaw/workspace
python3 scripts/jendralbot_content_generator.py

# Output: jendralbot_content_plan.json
# Contains: 84 pieces of content (14 per product)
```

**What it generates:**
- 42 TikTok video scripts
- 42 Instagram carousels (5 slides each)
- LinkedIn posts
- X threads (5 tweets each)
- YouTube Shorts scripts

### Step 2: Visual Content Creation

**A. TikTok Videos (content-generator skill)**
```bash
# Generate TikTok video from script
cd skills/content-generator
python3 scripts/generate_tiktok_viral.py --concept [product] --ratio 9:16

# Pipeline:
# LLM hook → NVIDIA Image → BytePlus Seedance (5s) → FFmpeg loop×12 → Compress → ~8.6MB MP4

# Cost: ~$0.03 per video
# Time: ~2-3 minutes
```

**B. Product Photos (gemini-image-generator skill)**
```bash
# Generate professional product images
cd skills/gemini-image-generator
python3 generate.py --prompt "[product description]" --style professional

# Use for:
# - Instagram posts
# - Product showcases
# - LinkedIn visuals
```

**C. Social Graphics (canva skill)**
```bash
# Create carousel & banner designs
cd skills/canva
python3 canva_cli.py --template instagram_post --product [product]

# Available templates:
# - Instagram post (1080x1080)
# - Carousel (multi-slide)
# - Banner (1080x1920)
```

### Step 3: Content Distribution (social-media-upload skill)

```python
# Browser automation for posting
# Platform workflows:
# TikTok: navigate → upload → add caption → post
# Instagram: navigate → select content → add caption → post
# LinkedIn: navigate → write post → upload media → post
# X: navigate → compose thread → post
```

**Example Schedule (Monday):**
```
07:00 → TikTok: AI Content Pro demo
09:00 → X: Thread about AI content
12:00 → Instagram: Studio Marketplace Pro carousel
14:00 → YouTube Shorts: AI Content Pro reel
17:00 → LinkedIn: B2B case study
18:00 → TikTok: FREE product teaser (Guru Pintar AI)
19:00 → Instagram: Mesin Cetak Kuliner showcase
21:00 → TikTok: Story format with emotional hook
```

### Step 4: Audience Building (social-media-engagement skill)

```python
# Daily engagement routine (30-60 min total)
# Can be automated with browser automation

For each platform (TikTok, Instagram, LinkedIn, X):
    1. Like 20 posts (relevant niche)
    2. Comment 5 posts (contextual, value-add)
    3. Follow 10 accounts (strategic)
    4. Reply to mentions/DMs (100% within 24h)

Platform-specific:
├─ TikTok: #AIcontent #AIindonesia #AIautomation
├─ Instagram: #ecommmerce #onlinestore #kuliner
├─ LinkedIn: #AIbusiness #digitaltransformation #automation
└─ X: Thread about product value, RT valuable content

Rate limits respected:
├─ TikTok: 200-300 likes/day
├─ Instagram: 100-200 likes/day
├─ LinkedIn: 100 likes/day
└─ X: 1000 likes/day
```

### Step 5: Lead Gen & Nurturing (email-marketing skill)

```python
# Email sequences for captured leads

Sequence 1: Welcome (FREE product leads)
Day 0:  Welcome + download link to FREE resource
Day 2:  Quick tip: How to get started
Day 5:  Special offer: 15% off Starter AI Content (24h)

Sequence 2: Post-Purchase (Paid product customers)
Day 0:  Thank you + receipt
Day 3:  Tutorial: Maximizing your purchase
Day 7:  Feedback request
Day 14: Upsell: Next tier product
Day 30:  Success story collection

Sequence 3: Re-engagement (Inactive leads)
Day 30+: Win back with exclusive discount
```

### Step 6: Performance Tracking (analytics-dashboard skill)

```bash
# Track metrics across platforms
# Daily automated report

Metrics to track:
├─ Views / Reach
├─ Engagement rate (likes, comments, shares, saves)
├─ Follower growth
├─ Click-through rate (bio links)
├─ Conversion (sales from affiliate links)
├─ DM leads (from CTAs)
├─ Email open & click rates

Platform-specific tools:
├─ TikTok Analytics (native)
├─ Instagram Insights (native)
├─ LinkedIn Analytics (native)
├─ X Analytics (native)
└─ LYNK Dashboard (affiliate revenue)
```

---

## 📅 DAILY AUTOMATION SCHEDULE

### Morning (06:00 - 08:00) - AUTOMATED
```bash
# 1. Generate today's content
python3 scripts/jendralbot_content_generator.py

# 2. Pick content from jendralbot_content_plan.json for today

# 3. Generate visuals (if needed)
# - TikTok videos: content-generator skill
# - Product photos: gemini-image-generator
# - Graphics: canva skill

# 4. Schedule posts
# - TikTok: 2-3 posts
# - Instagram: 2 posts
# - LinkedIn: 1 post
# - X: 3 posts
```

### Mid-Day (12:00 - 14:00) - AUTOMATED
```bash
# 5. Post scheduled content (social-media-upload skill)
# - Navigate platforms
# - Upload media
# - Add captions
# - Post

# 6. Engagement (social-media-engagement skill)
# - Like relevant posts
# - Comment value-add
# - Follow strategic accounts
```

### Evening (18:00 - 20:00) - HYBRID
```bash
# 7. Automated evening posts
# - TikTok: Night audience (story format)
# - Instagram: Prime time engagement

# 8. Manual check (2-3 min):
# - Reply to DMs
# - Check comments
# - Respond to mentions
```

### Night (20:00 - 22:00) - MANUAL (2-3 min)
```bash
# 9. Track revenue (lynk skill)
python3 skills/lynk/lynk.py track
# → Open LYNK dashboard
# → Input clicks & sales for each product
# → Save report automatically

# 10. View daily report
python3 skills/lynk/lynk.py report today
```

---

## 🎨 CONTENT TEMPLATES (Auto-Generated)

### TikTok Script Example (Starter AI Content)
```
🔥 STOP: Bingung mulai dari mana?

Problem: Bingung mulai dari mana
Ini bikin kamu frustrasi kan?

Solusinya: Starter AI Content
Support penuh

Dulu manual, sekarang otomatis
Coba 1 fitur, suka lanjut

💡 Link di bio atau comment 'MAU'
https://lynk.id/jendralbot/xlymwzj2jylv

#AIcontent #contentcreation #starter #AIindonesia #belajarAI
```

### Instagram Carousel Example (Studio Marketplace Pro)
```
Slide 1: 🚨 Problem? Editing lama
Kamu alamin ini?

Slide 2: 💡 Solusi: Studio Marketplace Pro
Cepat & praktis, Boost konversi, Jaminan kualitas

Slide 3: 🔥 Hasil: Dulu ribet, sekarang satu klik
https://lynk.id/jendralbot/emne05mm7v25

Slide 4: ⭐ Testimoni:
"Foto produk saya jadi super premium, konversi naik 300%!"
- Rina, Seller

Slide 5: 🎯 CTA: Tap link di bio!
Studio Marketplace Pro - Rp 75,000

#ecommerce #onlinestore #productphoto #marketplace #AIbusiness
```

### LinkedIn Post Example (AI Content Pro)
```
🎯 Transformasi Premium dengan AI Content Pro

Saya melihat banyak para business owners mengalami:

❌ Bikin konten manual lama
❌ Bakar budget desainer
❌ Competitor lebih cepat

Ini bikin mereka gak scale.

Solusinya?

📦 AI Content Pro
💰 Rp 89.000
🔗 https://lynk.id/jendralbot/d70eo2x45em5

Keunggulan:
✅ Otomatiskan konten

📊 "Saya hemat 80% waktu bikin konten. Sangat recommended!"
- Dian, Entrepreneur

Yang Anda dapatkan:
• Kualitas premium
• Save time 80%
• ROI tinggi

📲 Comment 'INFO' kalau mau detail lengkap

#AIcontent #professional #business #AIautomation #efficiency
```

---

## 💰 expected Outcomes (Weeks 1-4)

### Week 1: Awareness
- Content posted: 84 pieces (12/day × 7 days)
- Reach: 50K-100K (estimated)
- Followers gained: 500-1,000
- Leads captured: 50-100 (FREE product signups)
- Sales: 0-2 (warm-up phase)

### Week 2: Consideration
- Content posted: 84 pieces
- Reach: 100K-200K (viral multipliers kicking in)
- Followers gained: 1,000-2,000
- Leads captured: 100-200
- Sales: 3-7 (mainly Starter AI Content - Rp 49k)

### Week 3: Conversion
- Content posted: 84 pieces
- Reach: 200K-400K
- Followers gained: 2,000-5,000
- Sales: 8-15 (mix: Starter + mid-tier)

### Week 4: Scale
- Content posted: 84
- Reach: 400K-800K
- Followers gained: 5,000-10,000
- Sales: 15-30 (including premium products)

---

## 🔧 TOOLS & SKILLS USED

### Content Generation
- ✅ `jendralbot_content_generator.py` - Custom script, ready to use
- ✅ `content-generator` - TikTok video generation (NVIDIA + BytePlus)
- ✅ `gemini-image-generator` - Product photos
- ✅ `canva` - Social graphics
- ✅ `content-creator` - Browser-based content creation

### Distribution
- ✅ `social-media-upload` - Multi-platform posting (5 platforms)
- ✅ `tiktok-automation` - Specialized TikTok posting

### Engagement
- ✅ `social-media-engagement` - Automated like/comment/follow

### Lead Gen & Nurturing
- ✅ `email-marketing` - Newsletter & drip sequences

### Analytics
- ✅ `analytics-dashboard` - Multi-platform tracking
- ✅ `lynk` - Revenue tracking (already created)

---

## 📋 NEXT STEPS (Immediate Actions)

### 1. Setup & Configuration (Do Now)
```bash
# a. Check LYNK skill is ready
cd ~/.openclaw/workspace/skills/lynk
python3 lynk.py status

# b. Test content generator
cd /home/openclaw/.openclaw/workspace
python3 scripts/jendralbot_content_generator.py
# -> Output: jendralbot_content_plan.json

# c. Review content plan
cat jendralbot_content_plan.json | python3 -m json.tool | head -50
```

### 2. Day 1 Content Generation (Do Today)
```bash
# Generate today's visuals
# a. TikTok videos (1-2 products)
cd skills/content-generator
python3 scripts/generate_tiktok_viral.py --concept ai_content_pro --ratio 9:16

# b. Product photos (1-2 products)
cd skills/gemini-image-generator
python3 generate.py --prompt "AI Content Pro professional product photo"

# c. Social graphics
cd skills/canva
python3 canva_cli.py --template carousel --product starter_ai_content
```

### 3. Day 1 Posting (Do This Evening)
```bash
# Use browser automation or manual posting
# Platforms: TikTok, Instagram, LinkedIn

# a. TikTok first post (AI Content Pro demo)
# b. Instagram carousel (Starter AI Content)
# c. LinkedIn post (B2B case study)
```

### 4. Track Performance (Every Evening)
```bash
# LYNK revenue tracking
cd ~/.openclaw/workspace/skills/lynk
python3 lynk.py track
# -> Input today's clicks & sales from dashboard

python3 lynk.py report today
# -> View daily performance
```

---

## 🚀 SCALING UP (Weeks 2-4)

### Add Paid Ads (ads-manager skill)
```bash
# Research competitor ads
# Clone successful patterns
# Run small test budgets (Rp 100.000-300.000/day)

# Platforms:
# - Meta (FB+IG): Awareness & consideration
# - TikTok: Viral reach
# - Google Search: Intent-based traffic
```

### Expand Email List
```bash
# Add exit-intent popup on landing pages
# Add lead magnet to bio link
# Collect emails from DM leads
```

### Create Community
```bash
# WhatsApp group for customers
# Telegram channel for updates
# Discord for power users
```

---

## 📈 METRICS TO TRACK

### Content Performance
```
TikTok:
├─ Views per video (target: 10K+)
├─ Engagement rate (target: 5%+)
├─ Shares/virality (target: 100+ shares)
└─ Follower growth (target: 100+

Instagram:
├─ Reach (target: 5K+ per post)
├─ Engagement rate (target: 3%+)
├─ Saves (target: 50+ per carousel)
└─ Follower growth (target: 50+)/day

LinkedIn:
├─ Impressions (target: 2K+ per post)
├─ Engagement rate (target: 2%+)
└─ Connection requests (target: 20+)/day
```

### Revenue Performance
```
LYNK Dashboard:
├─ Clicks per product (target: 200+/day)
├─ Conversion rate (target: 3-5%)
├─ Revenue per product (track daily)
└─ Total revenue (track weekly)
```

---

## 🆘 TROUBLESHOOTING

### Video generation fails
```bash
# Check NVIDIA API key
echo $NVIDIA_API_KEY

# Check BytePlus API key
echo $BYTEPLUS_API_KEY

# Test video generation
cd skills/content-generator
python3 scripts/test_providers.py
```

### Browser automation fails
```bash
# Restart gateway
openclaw gateway restart

# Wait 30 seconds
sleep 30

# Try again
python3 scripts/post_to_tiktok.py
```

### Engagement low
```bash
# Review content quality
# - Hook strong?
# - Value clear?
# - CTA specific?

# Check posting times
# - During peak hours?
# - Consistent posting?

# Adjust hashtag strategy
# - Mix trending + niche?
# - Banned hashtags check?
```

---

## 📚 RESOURCES & FILES

### Key Scripts
```
/home/openclaw/.openclaw/workspace/
├── scripts/
│   ├── jendralbot_content_generator.py       # Main content planner
│   └── jendralbot_marketing_automation.py   # Full automation engine
└── skills/
    ├── lynk/                                # Revenue tracking
    ├── content-generator/                   # TikTok videos
    ├── gemini-image-generator/              # Product photos
    ├── canva/                               # Social graphics
    ├── social-media-upload/                 # Posting automation
    ├── social-media-engagement/             # Engagement automation
    ├── email-marketing/                     # Lead nurturing
    └── ads-manager/                         # Paid ads management
```

### Output Files
```
/home/openclaw/.openclaw/workspace/
├── jendralbot_content_plan.json             # 84 content pieces (7 days)
├── content_plan.json                        # Legacy plan
├── memory/2026-03-07.md                     # Today's notes
└── skills/lynk/data/lynk_*.json            # Revenue data
```

---

## ✅ DAILY CHECKLIST

Morning (Automated):
- [ ] Generate content from jendralbot_content_generator.py
- [ ] Generate visuals (if needed)
- [ ] Schedule 6-8 posts for the day

Mid-Day (Automated):
- [ ] Post scheduled content
- [ ] Run engagement routine (like/comment/follow)

Evening:
- [ ] Check and reply to DMs
- [ ] Respond to comments & mentions

Night (Manual - 2-3 min):
- [ ] Track LYNK revenue: `lynk track`
- [ ] View report: `lynk report today`
- [ ] Note learnings for tomorrow

---

## 🎯 SUCCESS CRITERIA

### Week 1
- [x] Content plan generated (84 pieces)
- [ ] First TikTok video posted
- [ ] First Instagram carousel posted
- [ ] First LinkedIn post shared
- [ ] 10+ followers gained
- [ ] LYNK skill configured & tested

### Week 2
- [ ] 100+ content pieces posted
- [ ] 500+ followers gained
- [ ] 50+ leads captured (FREE products)
- [ ] 3+ sales (Starter AI Content)
- [ ] Engagement rate 3%+ across platforms

### Week 4
- [ ] 400+ content pieces posted
- [ ] 2,000+ followers gained
- [ ] 200+ leads captured
- [ ] 20+ sales (mix of products)
- [ ] Revenue: Rp 500K-1M
- [ ] Paid ads campaign launched

---

**Created by:** OpenClaw AI
**For:** Andik Veris (Jendralbot)
**Date:** 2026-03-07
**Status:** ✅ Ready to execute

*Start today. Scale tomorrow. Win every day.* 💪🚀