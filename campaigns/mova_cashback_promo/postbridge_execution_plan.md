# PostBridge Upload & Scheduling Execution Plan

## Campaign Details
**Campaign Name:** MOVA Cashback Promo - Mar 2026
**Primary Link:** https://lynk.id/jendralbot/kkjk0mv1vg7o
**WhatsApp:** 628551180009
**Contact Script:** "Halo Admin saya sudah baca panduan dan ingin join Grup Edukasi MOVA dengan Mak Niluh"

---

## Phase 1: Asset Preparation

### Step 1.1: Generate Media Assets
**Status:** ⏳ Pending (requires POST AI or video generator)

**Assets Needed:**
```
✅ TikTok Video 1 (Before After) - 30s
✅ TikTok Video 2 (Secret Hack) - 25s
✅ TikTok Video 3 (UGC Testimonial) - 28s
✅ Instagram Reel (Before After) - 30s
✅ YouTube Shorts (Before After) - 30s
✅ Instagram Carousel (6 slides) - Complete set
✅ Facebook Ad Image 1 (Problem-Solution) - 4:5 ratio
✅ Instagram Ad Image 2 (Benefit-Focused) - 1:1 ratio
✅ Twitter/X Image (Urgency) - 4:5 ratio
```

**Asset Location:** `/home/openclaw/.openclaw/workspace/campaigns/mova_cashback_promo/assets/`

**File Naming:**
```
Videos:
  /videos/tiktok/tt_before_after_001.mp4
  /videos/tiktok/tt_secret_hack_002.mp4
  /videos/tiktok/tt_ugc_testimonial_003.mp4
  /videos/instagram/ig_reel_001.mp4
  /videos/youtube/yt_shorts_001.mp4

Carousels:
  /carousels/instagram/ig_carousel_001_slide1.jpg
  /carousels/instagram/ig_carousel_001_slide2.jpg
  [...slides 3-6]

Images:
  /images/ads/fb_ad_problem_solution.jpg
  /images/ads/ig_ad_benefit_focused.jpg
  /images/ads/tw_ad_urgency.jpg
```

---

## Phase 2: PostBridge Setup

### Step 2.1: Create Campaign
1. Login to PostBridge dashboard
2. Navigate to Campaigns section
3. Click "Create New Campaign"
4. Fill in details:
   - **Campaign Name:** MOVA Cashback Promo - Mar 2026
   - **Primary Link:** https://lynk.id/jendralbot/kkjk0mv1vg7o
   - **Platforms:** TikTok, Instagram, Facebook, Twitter, YouTube
   - **Campaign Type:** Promotion (Product awareness)
   - **Budget:** [Optional - if running paid ads]
   - **Start Date:** 2026-03-05
   - **End Date:** 2026-03-11 (7-day campaign)

### Step 2.2: Configure Tracking
- **UTM Parameters:**
  ```
  utm_source=postbridge
  utm_campaign=mova_cashback_march2026
  utm_medium=[platform_specific]
  utm_content=[content_type]
  ```

- **Tracking Link Format:**
  ```
  https://lynk.id/jendralbot/kkjk0mv1vg7o?utm_source=postbridge&utm_campaign=mova_cashback_march2026&utm_medium=tiktok&utm_content=video_001
  ```

---

## Phase 3: Content Upload & Scheduling

### Day 1 (2026-03-05)

#### Morning (8:00 - 9:00 AM) - ±30min randomization

**Post 1: TikTok - Video Concept 1 (Before After)**
- **Asset:** `/videos/tiktok/tt_before_after_001.mp4`
- **Caption:** Use `tt_001` from captions_variations.json
- **Hook:** "Gila... cara ini sudah viral tapi masih banyak yang belum tahu!"
- **Hashtags:** #cashback #doublecashback #mova #fyp #viral
- **CTA:** "Link di bio, cek sekarang sebelum kehabisan!"
- **Tracking Link:** https://lynk.id/jendralbot/kkjk0mv1vg7o?utm_source=postbridge&utm_campaign=mova_cashback_march2026&utm_medium=tiktok&utm_content=video_001
- **Scheduled Time:** 2026-03-05 08:15 (randomized)

**Post 2: Instagram Story - Carousel Slide 1-2**
- **Asset:** `/carousels/instagram/ig_carousel_001_slide1.jpg` + slide2
- **Caption:** Short (Story format) - "Swipe untuk lihat full story! 👉"
- **Hashtags:** #cashbackviral #doublecashback #mova
- **CTA:** "Swipe up! Link di bio"
- **Scheduled Time:** 2026-03-05 08:30 (randomized)

#### Afternoon (1:00 - 2:00 PM) - ±30min randomization

**Post 3: Instagram Feed - Carousel Full (6 slides)**
- **Asset:** All 6 carousel slides
- **Caption:** Use `ig_001` from captions_variations.json
- **Hook:** "Gila... aku baru nemu rahasia yang bikin kaget! 😱"
- **Hashtags:** #cashbackviral #doublecashback #mova #belanjahemat #saveuangeveryday #hacksbelanja #onlinecashback #duitbaliklagi #edukasifinansial #tipskeuangan #viralhack (#10 hashtags)
- **CTA:** "Link di bio, cek sekarang sebelum tutup!"
- **Tracking Link:** https://lynk.id/jendralbot/kkjk0mv1vg7o?utm_source=postbridge&utm_campaign=mova_cashback_march2026&utm_medium=instagram&utm_content=carousel
- **Scheduled Time:** 2026-03-05 13:45 (randomized)

**Post 4: Facebook - Long Form Post (Video)**
- **Asset:** `/videos/tiktok/tt_before_after_001.mp4` (same video, different platform)
- **Caption:** Use `fb_001` from captions_variations.json
- **Hook:** "Kalau kamu masih pakai cara lama, kamu rugi besar..."
- **Hashtags:** #Mova #DoubleCashback #CashbackOnline #HematBelanja #TipsHemat #EdukasiFinansial #CaraHematUang #AplikasiCashback #BelanjaCerdas #Hacks (#10 hashtags)
- **CTA:** "Klik link ini sekarang: https://lynk.id/jendralbot/kkjk0mv1vg7o"
- **Scheduled Time:** 2026-03-05 13:30 (randomized)

#### Evening (7:00 - 8:00 PM) - ±30min randomization

**Post 5: TikTok - Video Concept 2 (Secret Hack)**
- **Asset:** `/videos/tiktok/tt_secret_hack_002.mp4`
- **Caption:** Use `tt_002` from captions_variations.json
- **Hook:** "Kalau kamu masih pakai cara lama, kamu rugi besar..."
- **Hashtags:** #cashback #mova #doublecashback #fyp
- **CTA:** "Link di bio, cek sekarang!"
- **Tracking Link:** https://lynk.id/jendralbot/kkjk0mv1vg7o?utm_source=postbridge&utm_campaign=mova_cashback_march2026&utm_medium=tiktok&utm_content=video_002
- **Scheduled Time:** 2026-03-05 19:20 (randomized)

**Post 6: YouTube Shorts - Video Concept 1**
- **Asset:** `/videos/youtube/yt_shorts_001.mp4`
- **Caption:** Use `yt_001` from captions_variations.json
- **Hook:** "Cuma butuh 10 detik dan masalah ini langsung selesai!"
- **SEO Keywords:** Cara Dapat Double Cashback, Cashback Online Terbaik 2026, Cara Hemat Uang Belanja, MOVA Cashback Review, Tips Hemat Belanja Online
- **Hashtags:** #doublecashback #mova #cashback #hematbelanja #belanjaonline #tipskeuangan #carahemat #edithemat #viral #fyp
- **Tracking Link:** https://lynk.id/jendralbot/kkjk0mv1vg7o?utm_source=postbridge&utm_campaign=mova_cashback_march2026&utm_medium=youtube&utm_content=shorts
- **Scheduled Time:** 2026-03-05 19:45 (randomized)

---

### Day 2 (2026-03-06)

#### Morning (9:00 - 10:00 AM) - ±30min randomization

**Post 7: Twitter/X - Viral Tweet**
- **Asset:** `/images/ads/tw_ad_urgency.jpg` (single image)
- **Caption:** Use `tw_001` from captions_variations.json
- **Hook:** "Aku kira ini scam… ternyata hasilnya bikin kaget. 🤯"
- **Hashtags:** #DoubleCashback #Mova #Hacks #FYP
- **CTA:** "Link: https://lynk.id/jendralbot/kkjk0mv1vg7o"
- **Tracking Link:** https://lynk.id/jendralbot/kkjk0mv1vg7o?utm_source=postbridge&utm_campaign=mova_cashback_march2026&utm_medium=twitter&utm_content=tweet_001
- **Scheduled Time:** 2026-03-06 09:15 (randomized)

**Post 8: Instagram Story - Carousel Slide 3-4**
- **Asset:** `/carousels/instagram/ig_carousel_001_slide3.jpg` + slide4
- **Caption:** "Swipe untuk lihat benefits! 👉"
- **Hashtags:** #mova #doublecashback
- **CTA:** "Swipe up - Link in bio"
- **Scheduled Time:** 2026-03-06 09:30 (randomized)

#### Night (9:00 - 10:00 PM) - ±30min randomization

**Post 9: TikTok - Video Concept 3 (UGC Testimonial)**
- **Asset:** `/videos/tiktok/tt_ugc_testimonial_003.mp4`
- **Caption:** Use `tt_003` from captions_variations.json
- **Hook:** "Aku kira ini scam… ternyata hasilnya bikin kaget."
- **Hashtags:** #mova #cashback #doublecashback #fyp #viral
- **CTA:** "Cek panduan gratis di link bio!"
- **Tracking Link:** https://lynk.id/jendralbot/kkjk0mv1vg7o?utm_source=postbridge&utm_campaign=mova_cashback_march2026&utm_medium=tiktok&utm_content=video_003
- **Scheduled Time:** 2026-03-06 21:20 (randomized)

**Post 10: Instagram Reel - Video Concept 1 (Repost as Reel)**
- **Asset:** `/videos/instagram/ig_reel_001.mp4`
- **Caption:** Use `ig_002` from captions_variations.json
- **Hook:** "Kalau kamu masih pakai cara lama, kamu rugi besar... 💔"
- **Hashtags:** #doublecashback #mova #cashbackonline #hematbelanja #tipskeuangan #carahemat #belanjacerdas #edukasifinansial #hacksbelanja #viral (#10 hashtags)
- **CTA:** "Link di bio sekarang sebelum kuota habis!"
- **Tracking Link:** https://lynk.id/jendralbot/kkjk0mv1vg7o?utm_source=postbridge&utm_campaign=mova_cashback_march2026&utm_medium=instagram&utm_content=reel
- **Scheduled Time:** 2026-03-06 21:45 (randomized)

---

## Phase 4: Campaign Activation

### Step 4.1: Final Review Checklist
Before activating, verify:
- [ ] All 10 posts scheduled (2 platforms × 5 posts each platform mix)
- [ ] Content type balanced: 40% video, 30% carousel, 30% image
- [ ] No duplicate content across platforms
- [ ] All captions platform-specific
- [ ] All tracking links functional
- [ ] UTM parameters correct
- [ ] Scheduled times randomized (±30min)
- [ ] Mobile preview checked for all posts
- [ ] CTAs clear and compelling
- [ ] Hashtag counts correct per platform

### Step 4.2: Activate Campaign
1. Review all scheduled posts in PostBridge dashboard
2. Click "Activate Campaign"
3. Monitor first 24 hours:
   - Check if all posts published on time
   - Review initial engagement metrics
   - Verify tracking links are working
   - Check for any errors/issues

---

## Phase 5: Monitoring & Optimization

### Daily Monitoring Tasks
**Morning:**
- Check overnight posts engagement
- Review click-through rates (CTR)
- Monitor conversions (WhatsApp sign-ups)
- Respond to comments/questions

**Afternoon:**
- Check mid-day posts performance
- Identify top-performing content
- Adjust scheduling for remaining posts if needed
- Engage with audience comments

**Evening:**
- Review all posts published that day
- Aggregate metrics
- Prepare daily performance report

### Key Metrics to Track

#### Vanity Metrics (Engagement):
- TikTok: Views, Likes, Shares, Comments
- Instagram: Likes, Shares, Saves, Comments, Reach
- Facebook: Reactions, Shares, Comments
- Twitter/X: Likes, Retweets, Replies
- YouTube Shorts: Views, Likes, Comments

#### Conversion Metrics (Business Impact):
- Click-through rate (CTR) to LYNK link
- WhatsApp sign-ups (via unique phone numbers if possible)
- Group join requests
- Actual MOVA registrations

 Attribution by UTM parameters to see which platform/content type performs best.

### Optimization Strategies

**If CTR is low (<2%):**
- Test different hooks
- Modify CTAs (more urgent/exciting)
- Adjust thumbnail/cover image
- Change posting times
- A/B test different content formats

**If Engagement is low:**
- Test different hook patterns
- Adjust caption style (shorter/longer)
- Try different visual styles
- Respond more actively to comments
- Add more social proof

**If Conversion is low (high CTR, low sign-ups):**
- Clarify CTA directions
- Simplify sign-up process
- Add more benefits
- Include more social proof/testimonials
- Address objections directly

---

## Emergency Plan

### If Posts Fail to Publish:
1. Check PostBridge status page
2. Verify social media API credentials
3. Manually repost if automation fails
4. Adjust schedule to avoid double postings

### If Engagement Drops Suddenly:
1. Pause remaining scheduled posts
2. Audit recent performance
3. Identify potential issues (shadowban, algorithm change)
4. Adjust strategy or content style
5. Restart when ready

### If Negative Feedback Spikes:
1. Monitor comments closely
2. Address legitimate concerns
3. Pause campaign if serious issues
4. Revise messaging if needed

---

## Success Metrics (7-Day Campaign)

**Minimum Success:**
- 50K+ total impressions across all platforms
- 5K+ clicks to LYNK link (10% CTR minimum)
- 500+ WhatsApp sign-ups
- 100+ new group joins

**Target Success:**
- 100K+ total impressions
- 10K+ clicks to LYNK link (10% CTR)
- 1,000+ WhatsApp sign-ups
- 200+ new group joins

**Outstanding Success:**
- 150K+ total impressions
- 15K+ clicks to LYNK link (10% CTR)
- 1,500+ WhatsApp sign-ups
- 300+ new group joins

---

## Post-Campaign Analysis

**Report to Prepare:**
1. Aggregate performance by platform
2. Top-performing content types
3. Best hooks/CTAs
4. Best posting times
5. ROI calculation (if tracking actual revenue)
6. Lessons learned
7. Recommendations for next campaign

**Date to Generate Report:** 2026-03-13 (after campaign ends)

---

## Team Communication

**Contact Person:** Veris (BerkahKarya)
**WhatsApp:** 628551180009
**Support Script:** "Halo Admin saya sudah baca panduan dan ingin join Grup Edukasi MOVA dengan Mak Niluh"

**Daily Updates:**
- Morning: "Yesterday's performance: [metrics]"
- Afternoon: "Today's posts: [platforms/content types]"
- Evening: "Daily summary: [impressions, clicks, conversions]"

---

**Execution Plan Generated:** 2026-03-04
**Campaign Start:** 2026-03-05
**Campaign End:** 2026-03-11
**Total Scheduled Posts:** 10 posts across 5 platforms
**Review & Report:** 2026-03-13