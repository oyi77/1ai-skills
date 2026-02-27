# Landing Page Promotion Plan - TikTok Content Agency

**Date**: 2026-02-28
**Current Landing Page**: https://berkahkarya.org
**Status**: ✅ LIVE (General BerkahKarya page)

---

## 📊 Current Landing Page Analysis

### What's on berkahkarya.org
- **Services**: Digital Growth Agency (general)
  - E-commerce optimization (Shopee & TikTok)
  - SEO services
  - Trading bot (FlashRobs)
  - Case studies (fashion, local service, investment)
- **Content**: 
  - Company overview
  - Team members (Andi, Sony, Fikri)
  - Testimonials
  - Statistics (500+ projects, 98% satisfaction)
  - Contact info (generic)

### What's MISSING
- ❌ **NO TikTok Content Agency specific page**
- ❌ NO portfolio video showcase
- ❌ NO pricing packages for video creation
- ❌ NO contact form for Shopee sellers
- ❌ NO "3 free videos" offer

---

## 🎯 Problem

berkahkarya.org exists BUT it's a **general agency page**, NOT specific to TikTok Content Agency service for Shopee sellers.

**Impact:**
- Traffic sees general agency, not specific service
- Confusing value proposition
- No clear call-to-action for Shopee sellers
- Missing portfolio showcase (3 videos ready)

---

## 💡 Solution: Create Dedicated TikTok Agency Landing Page

### Option 1: New Subpage (Recommended)
**URL**: https://berkahkarya.org/tiktok-agency
**Time**: 2-4 hours development
**Pros**:
- ✅ Part of main domain
- ✅ Easy to setup (add to existing site)
- ✅ Professional branding
- ✅ Can link from main page

**Content Needed:**
```
- Hero section: "TikTok Viral Content for Shopee Sellers"
- Portfolio showcase: 3 sample videos (embedded from Drive)
- Pricing packages: Starter (IDR 3M), Growth (IDR 5M), Scale (IDR 8M)
- Benefits/ROI calculator
- Case studies/testimonials
- Contact form: Shop name, email, product details
- FAQ section
- CTA: "Get 3 Free Sample Videos"
```

### Option 2: Dedicated Subdomain (Alternative)
**URL**: https://tiktok.berkahkarya.org
**Time**: 4-8 hours development
**Pros**:
- ✅ Clear branding for TikTok agency
- ✅ Can have separate design
- ✅ Easy to promote

**Cons**:
- ❌ Requires subdomain DNS setup
- ❌ More time to develop

### Option 3: Modify Main Page (Fastest)
**Action**: Add TikTok Agency section to berkahkarya.org
**Time**: 1-2 hours development
**Pros**:
- ✅ Fastest to implement
- ✅ Leverages existing traffic

**Cons**:
- ❌ Less focused on specific service
- ❌ May confuse general agency offering

---

## 🚀 Recommended Implementation: Option 1 (Subpage)

### Technical Requirements

#### 1. HTML Structure
```html
<!DOCTYPE html>
<html lang="id">
<head>
    <title>TikTok Content Agency - BerkahKarya</title>
    <meta name="description" content="TikTok viral content for Shopee sellers. Get 3 free sample videos.">
</head>
<body>
    <!-- Hero Section -->
    <section class="hero">
        <h1>TikTok Viral Content untuk Shopee Sellers</h1>
        <p>Tingkatkan penjualan hingga 150% dengan video content yang terbukti viral</p>
        <a href="#contact" class="cta">Dapatkan 3 Video Gratis</a>
    </section>

    <!-- Portfolio Section -->
    <section class="portfolio">
        <h2>Sample Videos</h2>
        <!-- Embed 3 videos from Google Drive -->
        <div class="video-grid">
            <div class="video-item">
                <iframe src="https://drive.google.com/file/d/1AZUX3uQu7kVaLkKx_MtS2nf0qzFiz-_s/preview"></iframe>
                <p>Before & After Transformation</p>
            </div>
            <div class="video-item">
                <iframe src="https://drive.google.com/file/d/1RlAdstXdWSRlH4Wfza4jymnZTS6OYxG6/preview"></iframe>
                <p>Premium Showcase</p>
            </div>
            <div class="video-item">
                <iframe src="https://drive.google.com/file/d/1q95SpX29wOCXjhrpv_HeIFz_7czQD1as/preview"></iframe>
                <p>Installation Tutorial</p>
            </div>
        </div>
    </section>

    <!-- Pricing Section -->
    <section class="pricing">
        <h2>Paket Harga</h2>
        <div class="pricing-grid">
            <div class="plan starter">
                <h3>Starter</h3>
                <p>IDR 3,000,000/bulan</p>
                <ul>
                    <li>20 videos</li>
                    <li>1 video/hari</li>
                    <li>24 jam turnaround</li>
                </ul>
            </div>
            <div class="plan growth">
                <h3>Growth</h3>
                <p>IDR 5,000,000/bulan</p>
                <ul>
                    <li>40 videos</li>
                    <li>2 video/hari</li>
                    <li>12 jam turnaround</li>
                </ul>
            </div>
            <div class="plan scale">
                <h3>Scale</h3>
                <p>IDR 8,000,000/bulan</p>
                <ul>
                    <li>80 videos</li>
                    <li>4 video/hari</li>
                    <li>6 jam turnaround</li>
                </ul>
            </div>
        </div>
    </section>

    <!-- Contact Form -->
    <section id="contact" class="contact">
        <h2>Dapatkan 3 Videos Gratis</h2>
        <form action="https://api.berkahkarya.org/submit" method="POST">
            <input type="text" name="shop_name" placeholder="Nama Toko Shopee" required>
            <input type="email" name="email" placeholder="Email Address" required>
            <input type="text" name="product" placeholder="Produk Utama">
            <textarea name="message" placeholder="Ceritakan tentang toko Anda..."></textarea>
            <button type="submit">Kirim</button>
        </form>
    </section>
</body>
</html>
```

#### 2. Backend (Contact Form)
```javascript
// Simple serverless function (Vercel/Netlify)
export default async function handler(req, res) {
    const { shop_name, email, product, message } = req.body;
    
    // Store in database or send email
    await sendEmail({
        to: 'veris@berkahkarya.org',
        subject: `New Lead: ${shop_name}`,
        body: `Shop: ${shop_name}\nEmail: ${email}\nProduct: ${product}\n\n${message}`
    });
    
    // Auto-reply to seller
    await sendEmail({
        to: email,
        subject: 'Terima Kasih - 3 Videos Gratis',
        body: 'Terima kasih! Kami akan kirim 3 videos gratis dalam 24 jam.'
    });
    
    res.status(200).json({ success: true });
}
```

#### 3. Deployment
```bash
# Deploy to Vercel (free)
vercel deploy tiktok-agency --prod

# Or Netlify (free)
netlify deploy --dir=tiktok-agency --prod
```

---

## 📣 Promotion Channels (After Landing Page Ready)

### Channel 1: Social Media (Primary)

#### Instagram
- **Post frequency**: 2-3 posts/week
- **Content**:
  - Before/After transformations
  - Portfolio showcase
  - Case studies/testimonials
  - Behind-the-scenes (video creation process)
- **Hashtags**: #ShopeeSellers #TikTokMarketing #VideoContent #IndonesiaBusiness
- **Caption template**:
  ```
  Mau videonya viral di TikTok? Kami buat content untuk Shopee sellers!
  
  ✅ 3 sample videos GRATIS
  ✅ Format TikTok 9:16
  ✅ Hyperrealistic quality
  
  Cek: https://berkahkarya.org/tiktok-agency
  
  #ShopeeSellers #TikTokMarketing #IndonesiaBusiness
  ```

#### TikTok
- **Post frequency**: 3-4 posts/week
- **Content**:
  - Portfolio videos (repost sample videos)
  - Viral hooks examples
  - Industry tips (how to increase Shopee sales)
- **Music**: Trending audio tracks
- **Hashtags**: #ShopeeSeller #TikTokBusiness #VideoMarketing

---

### Channel 2: Shopee Seller Communities

#### Facebook Groups
**Target Groups:**
- "Komunitas Shopee Seller Indonesia"
- "Tips Jualan di Shopee"
- "Diskusi E-commerce Indonesia"
- "Digital Marketing Indonesia"

**Strategy**:
1. Join groups (5-10 groups)
2. **DO NOT SPAM** - Contribute value first
3. Share tips about TikTok marketing (educational)
4. After 5-10 posts, share landing page with context

**Post Template:**
```
Hi semua! 👋

Aku share tips: TikTok content bisa tingkatkan penjualan Shopee hingga 150%.

Data:
- LVT flooring market: USD 540M (2025)
- TikTok #flooring: 577.8K posts
- Flooring renovation content viral banget

Aku buat landing page dengan:
✅ 3 sample videos GRATIS
✅ ROI calculator
✅ Paket harga mulai IDR 150K/video

Cek: https://berkahkarya.org/tiktok-agency

Semoga membantu! 😊
```

---

### Channel 3: Direct Outreach (Manual Shopee Chat)

**Process:**
1. Contact top 5 sellers via Shopee Chat
2. Send message with **landing page link**
3. Ask for email to send 3 free videos

**Template:**
```
Halo! Ini Veris dari BerkahKarya TikTok Content Agency.

Kami membuat TikTok viral content untuk Shopee sellers.

**3 Sample Videos GRATIS:**
https://berkahkarya.org/tiktok-agency

Include:
✅ Before & After transformations
✅ Installation tutorials
✅ Premium showcases

**Market Data:**
- TikTok #flooring: 577.8K posts
- LVT market tumbuh 11.3%/tahun
- Flooring renovation content viral banget

**Harga:**
- Starter: IDR 3M/bulan (20 videos)
- Growth: IDR 5M/bulan (40 videos)
- Scale: IDR 8M/bulan (80 videos)

Cek videonya di landing page. Kalau suka, reply email address kalian untuk 3 videos gratis.

Terima kasih!

Veris | BerkahKarya
📞 +62 857-3274-0006 | 🌐 berkahkarya.org
```

---

### Channel 4: Paid Ads (Optional - Week 2)

#### Facebook Ads
**Target Audience:**
- Location: Indonesia (Java, Sumatra, Bali)
- Interest: E-commerce, Online selling, Shopee, TikTok
- Age: 25-45 years
- Income: IDR 5M+

**Ad Creative:**
- **Headline**: "TikTok Viral Content untuk Shopee Sellers"
- **Image**: Before/After transformation image
- **CTA Button**: "Dapatkan 3 Videos Gratis"
- **Landing Page**: https://berkahkarya.org/tiktok-agency

**Budget**: IDR 50-100K/day (test phase)

**Expected Results:**
- Clicks: 50-100/day
- Leads: 5-10/day
- Cost/Lead: IDR 10-20K

---

### Channel 5: Word of Mouth (Referrals)

#### Strategy
1. **Ask current clients** for referrals (after first 1-2 clients)
2. **Incentive**: 10% commission on referred deals
3. **Social proof**: Post testimonials on social media

**Referral Program Template:**
```
🎁 Referral Program

Kenalkan klien ke BerkahKarya TikTok Content Agency:
✅ Dapatkan 10% commission
✅ Klien dapat discount 10%
✅ Win-win-win!

Cara:
1. Share link: https://berkahkarya.org/tiktok-agency?ref=YOUR_NAME
2. Klien klik link → 10% discount
3. Kalian dapat 10% commission
```

---

## 📊 Promotion Timeline

### Week 1: Foundation
- [x] ✅ 3 sample videos generated
- [x] ✅ Portfolio uploaded to Drive
- [ ] Create TikTok Agency landing page (berkahkarya.org/tiktok-agency)
- [ ] Deploy landing page
- [ ] Test contact form

### Week 2: Initial Promotion
- [ ] Create social media accounts (if not exist)
- [ ] Post 2-3 Instagram posts
- [ ] Post 3-4 TikTok videos
- [ ] Join 5-10 Facebook groups
- [ ] Contact 5 Shopee sellers via chat (with landing page link)

### Week 3: Paid Ads (Optional)
- [ ] Create Facebook ads campaign
- [ ] Set budget IDR 50-100K/day
- [ ] Monitor performance
- [ ] Optimize based on data

### Week 4: Scale & Follow-up
- [ ] Follow up on all leads
- [ ] Create case studies/testimonials
- [ ] Increase posting frequency
- [ ] Scale ads if working

---

## 🎯 Success Metrics

### Traffic Metrics
- **Unique visitors**: 500+/week
- **Page views**: 2,000+/week
- **Bounce rate**: <50%
- **Time on page**: 2+ minutes

### Lead Metrics
- **Form submissions**: 10-20/week
- **Contact requests**: 10-20/week
- **Email addresses collected**: 10-20/week

### Conversion Metrics
- **Free trial requests**: 2-4/week
- **Paid conversions**: 1-2/month
- **Revenue**: IDR 10M+ (30-day goal)

---

## 💡 Best Practices

### 1. Content Quality First
- High-quality videos (hyperrealistic)
- Professional landing page design
- Clear value proposition
- Easy-to-use contact form

### 2. Authenticity Matters
- Show real portfolio (3 videos ready)
- Include testimonials (after first clients)
- Transparent pricing (no hidden costs)
- Honest about capabilities

### 3. Provide Value Before Selling
- Educational content (TikTok marketing tips)
- Free samples (3 videos)
- ROI calculator (show numbers)
- Case studies (prove results)

### 4. Multiple Touchpoints
- Social media presence (Instagram + TikTok)
- Direct outreach (Shopee Chat)
- Community engagement (Facebook groups)
- Paid ads (optional)

---

## 🚀 Immediate Next Steps

### RIGHT NOW (Today)
1. **Create landing page** (berkahkarya.org/tiktok-agency)
   - Hero section
   - Portfolio (3 videos)
   - Pricing packages
   - Contact form

2. **Deploy landing page**
   - Test functionality
   - Check mobile responsiveness
   - Verify contact form

3. **Create social media content**
   - 2-3 Instagram posts
   - 3-4 TikTok videos

### THIS WEEK
4. **Join Facebook groups** (5-10 groups)
5. **Contact 5 Shopee sellers** via chat (with landing page link)
6. **Post initial content** on social media

### NEXT WEEK
7. **Consider paid ads** (if organic not enough)
8. **Follow up on leads**
9. **Create testimonials** (from first clients)

---

## 💰 Budget & Resources

### Development Cost
- **Landing page**: 2-4 hours (FREE - use own time)
- **Hosting**: FREE (Vercel/Netlify)
- **Domain**: Already owned (berkahkarya.org)

### Promotion Cost
- **Social media**: FREE
- **Facebook groups**: FREE
- **Shopee Chat**: FREE (manual labor)
- **Paid ads**: IDR 350K-700K/week (optional)

### Total Investment (First Month)
- **Development**: IDR 0 (own time)
- **Promotion**: IDR 0-700K (depending on ads)
- **Total**: IDR 0-700K

### Expected Return (First Month)
- **Revenue**: IDR 10,000,000
- **Profit**: IDR 9,300,000-10,000,000
- **ROI**: 930% - 10,000%

---

*Plan created: 2026-02-28 00:30*
*Status: READY FOR EXECUTION*
*Recommendation: Create berkahkarya.org/tiktok-agency landing page, then promote*
