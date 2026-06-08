---
name: digital-real-estate
description: Build and manage a portfolio of niche content sites generating affiliate
  and AdSense revenue with AI handling research, writing, SEO, and updates
domain: content
---



## Overview

Build, scale, and monetize a portfolio of niche content websites. Solo operators run 5-20 sites simultaneously with AI handling research, writing, internal linking, technical SEO, and content updates. Revenue comes from affiliate programs (Amazon Associates, ShareASale, Impact) and display ads (AdSense, Mediavine, AdThrive). Target: $1K-$10K/month per site after 6-12 months.

## Required Tools

- **CMS**: WordPress (with WP-CLI) or Next.js (static generation)
- **Keyword Research**: Ahrefs API, SEMrush API, or free alternatives (Google Keyword Planner, Ubersuggest)
- **Content Generation**: Claude API or OpenAI API
- **SEO**: Screaming Frog CLI, Google Search Console API, sitemap generators
- **Hosting**: Vercel (Next.js), Cloudways/SiteGround (WordPress), or VPS
- **Affiliate Networks**: Amazon Associates, ShareASale, Impact, CJ Affiliate
- **Analytics**: Google Analytics 4, Plausible (privacy-friendly)
- **Node.js 18+** for automation scripts

## Capabilities

- Research profitable niches with low competition
- Generate SEO-optimized long-form content (2000-5000 words)
- Build internal linking structures automatically
- Manage multiple sites from a single dashboard
- Track rankings, traffic, and revenue across portfolio
- Auto-update outdated content with fresh information
- A/B test headlines, meta descriptions, and CTAs
- Scale from 1 site to 20+ with consistent quality

## When to Use

- Building passive income through content sites
- Expanding existing portfolio to new niches
- Automating content production for established sites
- Refreshing outdated content to recover rankings
- Starting affiliate marketing with minimal investment
- Creating assets that compound in value over time

## When NOT to Use

- Task is about content strategy, not creation (use strategy skills)
- Task is about content distribution (use distribution skills)
- You need to analyze content performance (use analytics skills)
- Task is about content moderation (use moderation tools)
- You don't have content guidelines
- Task requires domain expertise (consult experts)


## Pseudo Code

The digital-real-estate workflow follows a standard pipeline pattern.

Core flow:
```
# digital-real-estate primary flow
input = prepare(raw_data)
result = process(input, config={adsense, affiliate, build, content, digital})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Core Workflow
```
# digital-real-estate primary flow
input = prepare(raw_data)
result = process(input, config={adsense, affiliate, build, content, digital})
validate(result)
deliver(result)
```

### Error Handling
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Niche Research & Selection

```bash
# Evaluate niche potential
evaluate_niche() {
  NICHE=$1

  # Check search volume and competition
  ahrefs_keyword_difficulty "$NICHE" --min-volume 1000 --max-kd 30

  # Check monetization potential
  # Target: $10+ RPM (revenue per 1000 impressions)
  check_affiliate_programs "$NICHE"  # Amazon, ShareASale, etc.
  check_ad_network_rpm "$NICHE"      # Mediavine requires 50K sessions/mo

  # Competition analysis
  # Look for weak SERPs: forums, thin content, outdated articles in top 10
  serp_analysis "$NICHE" --top-urls 10

  # Score: volume * RPM / competition = opportunity score
  # Target score > 50
}

# Ideal niche criteria:
# - 500+ keywords with 1K-10K monthly volume
# - KD (keyword difficulty) < 30
# - RPM > $10
# - Multiple affiliate programs available
# - Evergreen topic (not seasonal/fad)
# - You can produce 100+ articles
```

### Site Setup (WordPress)

```bash
# Automated WordPress setup
SITE_DOMAIN="myniche.com"

# Provision hosting
wp-cli core download --path=/var/www/$SITE_DOMAIN
wp-cli config create --dbname=${SITE_DOMAIN}_db --dbuser=root --dbpass=$DB_PASS
wp-cli core install --url=$SITE_DOMAIN --title="My Niche Site" --admin_user=admin

# Install essential plugins
wp-cli plugin install wordpress-seo --activate           # Yoast SEO
wp-cli plugin install wp-rocket                           # Caching
wp-cli plugin install shortpixel-adaptive-images          # Image optimization
wp-cli plugin install tablepress                          # Comparison tables
wp-cli plugin install wp-schema-pro                       # Structured data

# Set up theme (Astra or GeneratePress - lightweight, fast)
wp-cli theme install astra --activate

# Configure SEO defaults
wp-cli option update blogdescription "Expert reviews and guides"
wp-cli option update permalink_structure "/%postname%/"

# Submit sitemap to Search Console
curl -X POST "https://www.google.com/ping?sitemap=https://$SITE_DOMAIN/sitemap.xml"
```

### Content Pipeline

```python
# Generate cluster of related articles
def generate_content_cluster(main_keyword, site_config):
    # Step 1: Keyword clustering
    keywords = research_keywords(main_keyword)
    clusters = cluster_by_intent(keywords)  # informational, commercial, transactional

    for cluster in clusters:
        # Step 2: Generate pillar article (3000-5000 words)
        pillar = generate_article(
            keyword=cluster.main_keyword,
            word_count=4000,
            style="comprehensive_guide",
            include_table=True,
            include_faq=True,
            site_config=site_config
        )

        # Step 3: Generate supporting articles (1500-2500 words)
        for kw in cluster.supporting_keywords:
            article = generate_article(
                keyword=kw,
                word_count=2000,
                style="focused_guide",
                internal_links_to=[pillar.url],
                site_config=site_config
            )

        # Step 4: Internal linking
        auto_internal_link(cluster.all_articles)

        # Step 5: Schema markup
        add_schema_markup(cluster.all_articles, types=["Article", "FAQ", "HowTo"])

    return clusters
```

### Internal Linking Automation

```python
def auto_internal_link(articles):
    """Automatically build internal links between related articles."""
    for article in articles:
        # Find related articles by keyword overlap
        related = find_related_articles(article, all_articles, max_links=5)

        for target in related:
            # Find natural anchor text opportunities
            anchor_text = find_anchor_opportunity(article.content, target.keyword)

            if anchor_text:
                # Insert link naturally within content
                article.content = insert_link(
                    article.content,
                    anchor_text,
                    target.url,
                    position="contextual"  # Not footer or sidebar
                )

        # Update article with new links
        update_article(article)
```

### Technical SEO Checklist

```bash
# Run technical SEO audit on each site
technical_seo_audit() {
  SITE=$1

  # Core Web Vitals
  curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=$SITE&strategy=mobile" \
    | jq '.lighthouseResult.categories'

  # Check for common issues
  screaming-frog --crawl $SITE --output-seo-issues \
    --check "missing_title,duplicate_content,broken_links,missing_alt,thin_content"

  # Generate sitemap
  wp-cli sitemap generate --post_type=post --format=xml

  # Submit to search engines
  curl -X POST "https://www.google.com/ping?sitemap=$SITE/sitemap.xml"
  curl -X POST "https://www.bing.com/indexnow?url=$SITE&key=$INDEXNOW_KEY"

  # Check robots.txt
  curl "$SITE/robots.txt"
}
```

### Portfolio Scaling

```bash
# Manage multiple sites from single config
cat > portfolio.json << 'EOF'
{
  "sites": [
    {
      "domain": "bestcoffeemakers.com",
      "niche": "coffee equipment",
      "status": "active",
      "monthly_traffic": 45000,
      "monthly_revenue": 2800,
      "articles": 87,
      "last_update": "2026-05-01"
    },
    {
      "domain": "homeofficeguide.com",
      "niche": "home office setup",
      "status": "growing",
      "monthly_traffic": 12000,
      "monthly_revenue": 650,
      "articles": 34,
      "last_update": "2026-05-15"
    }
  ]
}
EOF

# Weekly maintenance routine
for site in $(jq -r '.sites[].domain' portfolio.json); do
  echo "=== $site ==="
  # Check rankings
  check_rankings $site --alert-if-drop > 10
  # Update outdated content
  find_outdated_articles $site --older-than 90days
  # Check for broken links
  check_broken_links $site
  # Generate weekly report
  generate_report $site --period weekly
done
```

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| `CONTENT_DUPLICATE` | AI generated similar content to existing | Run plagiarism check, rewrite unique sections |
| `RANKING_DROP` | Algorithm update or competitor outranked | Audit content quality, update with fresh data |
| `AFFILIATE_BAN` | Violated affiliate program terms | Review compliance, apply to alternative programs |
| `HOSTING_DOWNTIME` | Server issues | Monitor with UptimeRobot, switch to reliable host |
| `INDEXING_ISSUE` | Google not indexing new content | Check Search Console, request indexing, fix technical issues |
| `THIN_CONTENT_FLAG` | AI content detected as low quality | Add unique insights, expert quotes, original research |

## Common Patterns

- **Batch processing**: Process multiple items in parallel for throughput
- **Retry with backoff**: Handle transient failures gracefully
- **Rate limiting**: Respect API limits with configurable delays
- **Logging**: Structured logging for debugging and audit trails


### Revenue Stacking
- Primary: Affiliate commissions (Amazon 1-10%, other programs 5-30%)
- Secondary: Display ads (AdSense $5-15 RPM, Mediavine $20-40 RPM)
- Tertiary: Sponsored posts ($200-$2000 per post)
- Target: $30+ RPM across all revenue streams

### Content Refresh Cycle
- Monthly: Update statistics, prices, and product availability
- Quarterly: Refresh top 20% of traffic-driving articles
- Annually: Complete rewrite of underperforming cornerstone content
- Trigger: Any article dropping >20% in traffic gets immediate refresh

### Exit Strategy
- Sites sell for 30-40x monthly revenue on Flippia, Empire Flippers, Motion Invest
- A site earning $3K/month = $90K-$120K sale price
- Clean up content, document processes, transfer hosting before listing

## How to Use

1. Define content goal (traffic, engagement, conversion, brand awareness)
2. Research target audience pain points and search intent
3. Generate content using appropriate AI tools
4. Edit and humanize output for authenticity
5. Optimize for target platform (SEO, hashtags, format)
6. Schedule and distribute across channels
7. Measure performance and iterate

## Red Flags

- **AI-generated content sounds robotic**: Always run through humanizer before publishing
- **Engagement dropping week-over-week**: Content fatigue or algorithm change — vary formats
- **Duplicate content across platforms**: Adapt content per platform, don't just cross-post
- **No content calendar**: Sporadic posting kills audience retention
- **Ignoring analytics**: Content without measurement is just publishing, not marketing
