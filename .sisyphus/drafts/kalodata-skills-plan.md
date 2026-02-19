# Draft: Kalodata Research Skills Plan

## Objective
Create detailed skills that can automate TikTok Shop product research using Kalodata API.

## Research Data from Draft

### API Endpoints Documented:
1. **Product Query** - `POST https://www.kalodata.com/product/queryList`
   - Filters: category, date range, price, sales channel, strategy, affiliate type, creator count
   - Returns: product info, revenue, sales, creators, trends

2. **Product Enrichment (Videos)** - `POST https://www.kalodata.com/product/enrich`
   - Input: product IDs
   - Returns: video IDs associated with products

3. **AI Usage Check** - `GET https://www.kalodata.com/benefit/checkAiUse`
   - Input: video ID, type (videoScript)
   - Returns: AI usage status and quota

4. **Video URL** - `GET https://www.kalodata.com/video/detail/getVideoUrl`
   - Input: video ID
   - Returns: MP4 download URL

5. **Script/Storyboard Export** - `POST https://www.kalodata.com/aiTask/startAiTask`
   - Input: video ID, type (video_script), date range
   - Returns: task status (processing/complete)

6. **Get Storyboard** - `POST https://www.kalodata.com/aiTask/video/getVideoScript`
   - Input: video ID, date range
   - Returns: scene breakdown, visual descriptions, audio scripts

7. **Product Count** - `POST https://www.kalodata.com/product/count`
   - Returns: total products matching filters

## Key Requirements:
- Authentication via cookies (SESSION, cf_clearance)
- Country/currency/language headers (ID context)
- Date range filtering capability
- Category filtering (e.g., 601152 = Fashion)
- Pagination support

## Skills to Build:
1. **kalodata-product-research** - Search products by criteria
2. **kalodata-video-analysis** - Get videos for products
3. **kalodata-storyboard-extract** - Extract AI-generated storyboards
4. **kalodata-research-automation** - End-to-end research workflow

## Scope:
- IN: Build skills that can call Kalodata APIs
- OUT: Building a full dashboard (just the skills)
