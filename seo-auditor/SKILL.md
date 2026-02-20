# SEO Auditor Skill 🔍

**Production-ready** automation untuk website SEO analysis & optimization.

## 🎯 Features

- **Technical SEO audit** - Crawl errors, speed, mobile-friendliness
- **Keyword tracking** - Monitor rankings for target keywords
- **Competitor analysis** - Compare against competitors
- **Backlink monitoring** - Track new/lost backlinks
- **Content optimization** - Suggest improvements for existing content
- **Local SEO** - Google My Business optimization
- **Report generation** - PDF/Excel reports for clients

## 📦 Files

```
seo-auditor/
├── SKILL.md              # This file
├── script.sh             # Main audit script (cross-platform)
├── script.ps1            # Windows PowerShell version
├── config.json           # Configuration (targets, keywords)
├── templates/            # Report templates
└── reports/              # Generated reports
```

## 🔧 Setup

### 1. Configure Targets

Edit `config.json`:
```json
{
  "targets": [
    {
      "name": "Client Website",
      "url": "https://example.com",
      "keywords": ["keyword1", "keyword2", "keyword3"],
      "competitors": ["https://competitor1.com", "https://competitor2.com"]
    }
  ],
  "schedule": {
    "fullAudit": "weekly",
    "rankTracking": "daily",
    "backlinkCheck": "weekly"
  },
  "reporting": {
    "format": "pdf",
    "email": "client@example.com",
    "branding": {
      "logo": "assets/logo.png",
      "colors": {"primary": "#007bff"}
    }
  }
}
```

### 2. Run the Skill

```bash
# Full SEO audit (Linux/macOS)
./script.sh --target "Client Website" --full

# Quick rank check
./script.sh --target "Client Website" --ranks

# Competitor analysis
./script.sh --target "Client Website" --competitors

# Generate report
./script.sh --target "Client Website" --report
```

**Windows (PowerShell):**
```powershell
.\script.ps1 -Target "Client Website" -Full
```

## 🔄 How It Works

### Audit Categories:

1. **Technical SEO**
   - Crawlability & indexation
   - Site speed (Core Web Vitals)
   - Mobile-friendliness
   - HTTPS & security
   - Structured data

2. **On-Page SEO**
   - Title tags & meta descriptions
   - Header structure (H1-H6)
   - Content quality & length
   - Keyword optimization
   - Internal linking

3. **Off-Page SEO**
   - Backlink profile analysis
   - Domain authority
   - Social signals
   - Brand mentions

4. **Local SEO** (if applicable)
   - Google My Business optimization
   - NAP consistency
   - Local citations
   - Reviews management

## 📊 Metrics Tracked

- **Organic traffic** (Google Analytics integration)
- **Keyword rankings** (top 100 positions)
- **Backlinks** (new, lost, toxic)
- **Page speed** (LCP, FID, CLS)
- **Crawl errors** (404, 500, redirect chains)
- **Index coverage** (indexed vs excluded pages)

## 🛠️ Tools & APIs

- **Google Search Console API** - Performance data, index coverage
- **Google PageSpeed Insights API** - Speed metrics
- **Google Analytics API** - Traffic data
- **Custom crawler** - Site audit (based on Puppeteer/Playwright)
- **Backlink API** (optional: Ahrefs, SEMrush, Moz)

## 📈 Sample Report Sections

```
SEO Audit Report - example.com
Generated: 2026-02-18

📊 Overall Score: 78/100

✅ Strengths:
- Fast page load (1.2s)
- Mobile-friendly design
- Good internal linking

⚠️ Issues Found:
- 3 pages with missing meta descriptions
- 2 broken internal links (404)
- 5 images without alt text
- H1 missing on homepage

🎯 Recommendations:
1. Add meta descriptions to product pages
2. Fix broken links to /old-page
3. Add alt text to all images
4. Add H1 tag to homepage

📈 Keyword Rankings:
- "keyword1": #3 (↑2)
- "keyword2": #7 (↓1)
- "keyword3": #12 (new)
```

## ⚠️ Warnings

- **API Quotas**: Google APIs have daily limits
- **Rate Limiting**: Don't crawl too aggressively
- **Data Accuracy**: Rankings vary by location/device

## 🚀 Next Steps

Planned improvements:
- [ ] AI-powered content suggestions
- [ ] Automated fix implementation
- [ ] Multi-language support
- [ ] E-commerce specific audits
- [ ] Integration with CMS (WordPress, Shopify)

---
**Berkah Karya** ⚡ | Part of 1ai-skills collection
