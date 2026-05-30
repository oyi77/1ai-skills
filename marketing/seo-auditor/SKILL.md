---
name: seo-auditor
description: SEO analysis and optimization automation for websites. Use when conducting technical SEO audits, tracking keyword rankings, analyzing competitor SEO, monitoring backlink profiles, optimizing existing content, improving local SEO visibility, generating SEO reports for clients, or automating website health checks.
---


# SEO Auditor Skill 🔍

**Production-ready** automation untuk website SEO analysis & optimization.

## Overview

SEO Auditor provides comprehensive website optimization capabilities including technical SEO audits, keyword ranking tracking, competitor analysis, backlink monitoring, content optimization suggestions, local SEO improvements, and automated reporting. It serves as a complete SEO management solution that automate the audit process, track performance over time, identify actionable improvements, and generate client-ready reports in various formats including PDF and Excel.

## When to Use

- **Technical SEO audit**: Identifying crawl errors, speed issues, and mobile-friendliness problems
- **Keyword tracking**: Monitoring rankings for target keywords over time
- **Competitor analysis**: Comparing against competitors' SEO performance
- **Backlink monitoring**: Tracking new, lost, and toxic backlinks
- **Content optimization**: Suggesting improvements for existing content
- **Local SEO**: Google My Business optimization and local citations
- **Report generation**: Creating PDF and Excel reports for clients
- **Scheduled audits**: Automated regular website health checks

## The Process

- Configure analysis, analyzing, auditor, audits, automating settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Step 1: Target Configuration

**Configuration File Setup**:
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

### Step 2: Full SEO Audit

**Run Complete Audit**:
```bash
./script.sh --target "Client Website" --full
```

**Audit Categories**:
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

### Step 3: Rank Tracking

**Monitor Keyword Rankings**:
```bash
./script.sh --target "Client Website" --ranks
```

**Setup Tracking**:
1. Add target keywords in config
2. Schedule daily tracking
3. Monitor position changes
4. Set alerts for significant moves

### Step 4: Backlink Analysis

**Track Backlink Profile**:
```bash
./script.sh --target "Client Website" --backlinks
```

**Metrics Tracked**:
- New backlinks from last check
- Lost backlinks
- Toxic score changes
- Referring domains count

### Step 5: Competitor Comparison

**Analyze Competitors**:
```bash
./script.sh --target "Client Website" --competitors
```

**Comparison Points**:
- Top ranking keywords
- Link profiles
- Content structure
- Page speed
- Mobile optimization

### Step 6: Report Generation

**Generate SEO Report**:
```bash
./script.sh --target "Client Website" --report
```

**Report Contents**:
- Overall SEO score
- Strengths and weaknesses
- Priority issues to fix
- Recommendation list
- Ranking history charts
- Backlink summary

### Step 7: Scheduled Automation

**Setup Regular Audits**:
```bash
# Weekly full audit (add to cron)
0 0 * * 0 ./script.sh --target "Client Website" --full --report

# Daily rank tracking
0 6 * * * ./script.sh --target "Client Website" --ranks
```

## Common Patterns

**Weekly SEO Workflow**:
```bash
# Monday morning routine
./script.sh --target "Client Website" --full
./script.sh --target "Client Website" --report
./script.sh --target "Client Website" --ranks
```

**Campaign-Based Audits**:
```bash
# Before marketing campaign
./script.sh --target "Client Website" --full --before

# After campaign
./script.sh --target "Client Website" --full --after
```

**Emergency Health Check**:
```bash
# After site changes
./script.sh --target "Client Website" --quick
```

## When NOT to Use

- Task is about sales, not marketing (use sales skills)
- Task is about product development (use product skills)
- You need to analyze marketing data (use analytics skills)
- Task is about customer support (use support skills)
- You don't have marketing assets
- Task requires legal review (consult legal)


## Red Flags

- **❌ API quota exceeded**: Google Search Console or PageSpeed API limits hit - implement rate limiting
- **❌ Audit incomplete**: Missing data from specific categories - check API connectivity
- **❌ Backlink tracking stops**: Backlink API connection failure or API key expired
- **❌ Report generation fails**: Template or formatting issues - verify template file path
- **❌ Keyword rankings show null/: Check search volume or query issues
- **❌ Speed scores inconsistent**: Device-specific checks (desktop vs mobile) not matched
- **❌ Crawl errors missing**: Configuration issue or site blocked crawler access

## Verification

**Connection Tests**:
```bash
# Test API connections
curl -H "Authorization: Bearer $GSC_ACCESS_TOKEN" \
  "https://searchconsole.googleapis.com/v1/sites/$SITE_URL"

# Test PageSpeed API
curl "https://pagespeedonline.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://example.com"
```

**Functional Verification**:

1. **Audit Complete Test**:
   ```bash
   ./script.sh --target "Test Site" --full
   
   # Verify all audit categories completed
   # Output: Technical: OK, On-page: OK, Off-page: OK, Local: OK
   ```

2. **Rank Tracking Test**:
   ```bash
   ./script.sh --target "Test Site" --keywords "test keyword"
   
   # Verify ranking recorded in database
   # Should show position and change from last check
   ```

3. **Report Generation Test**:
   ```bash
   ./script.sh --target "Test Site" --report
   
   # Verify output file exists and is valid
   # Check file size > 100KB (indicates content)
   ```

**API Endpoint Verification**:
```bash
# Verify all API connections work
./script.sh --verify-apis

# Expected:
# ✓ Google Search Console - Connected
# ✓ Google PageSpeed Insights - Connected
# ✓ Google Analytics - Connected
# ✓ Custom Crawler - Ready
```

**Data Quality Checks**:
- [ ] Audit data matches manual spot-checks
- [ ] Rankings trend logically (no random jumps)
- [ ] Backlink counts are reasonably accurate
- [ ] Speed scores correlate with actual load times
- [ ] Crawl errors match site robots.txt and server logs

**Output Verification**:
```bash
# After report generation
ls -la reports/client-website-2026-02-18.pdf

# Verify file properties
file reports/client-website-2026-02-18.pdf
# Should output: PDF document, version 1.4 or higher
```

**Quick Health Check**:
```bash
echo "SEO Auditor Status"
echo "=================="
echo "API Status: $(./script.sh --verify-apis 2>&1 | grep -c 'Connected')/4 OK"
echo "Last Audit: $(ls -t reports/ 2>/dev/null | head -1 || echo 'Never')"
echo "Target Sites: $(cat config.json | jq '.targets | length')"
echo "Keyword Trackers: $(cat config.json | jq '.targets[0].keywords | length')"
```
