# Kalodata Skills - Learnings

## Session Log

### Session 1 - 2026-02-19
- Started building Kalodata Intelligence System
- Wave 1: Foundation (API Client, Auth, Product Skill)

## Conventions
- All API calls require cookies (SESSION, cf_clearance)
- Use environment variables for credentials
- Output structured insights for business users (not raw JSON)
- Support multi-account switching via config

## Gotchas
- Storyboard extraction is async - must poll for completion
- Cookie authentication requires proper headers
- Video URLs expire - don't cache long-term

## Implementation Notes

### API Client Module (src/kalodata/)
Created 4 core files:
- `types.ts` - TypeScript interfaces for all 7 API endpoints
- `auth.ts` - Cookie-based authentication utilities
- `client.ts` - HTTP client with retry logic and exponential backoff
- `index.ts` - Public exports

### API Endpoints Implemented
1. POST /product/queryList - Query products
2. POST /product/enrich - Get videos for products
3. GET /benefit/checkAiUse - Check AI usage
4. GET /video/detail/getVideoUrl - Get video download URL
5. POST /aiTask/startAiTask - Start storyboard generation (async)
6. POST /aiTask/video/getVideoScript - Get storyboard
7. POST /product/count - Get product count

### Key Design Decisions
- Used `setEnvGetter` pattern for environment variables (avoids Node.js dependency)
- Exponential backoff with configurable delay
- `waitForVideoScript` helper for async polling
- All error types extend KalodataError for consistent error handling

### Environment Variables
- KALODATA_SESSION
- KALODATA_CF_CLEARANCE

### Default Configuration
- baseUrl: https://www.kalodata.com
- country: ID, currency: IDR, language: id-ID
- timeout: 30000ms, maxRetries: 3, retryDelay: 1000ms

### Product Research Skill (Wave 1 Extension)
Created `src/kalodata/product-research.ts` with:

#### Features
- Category-based product queries with flexible filters
- AI Filter Intelligence for research goal detection
- Pagination support with async generator
- Structured insights (trend direction, competition level, opportunity score)

#### AI Filter Intelligence Patterns
| Goal Pattern | Filters Applied |
|-------------|-----------------|
| emerging/new/rising | sort: revenue_trend ASC, recent launch_date, creator_num: 10-100 |
| stable/bestsellers/proven | sort: revenue DESC, creator_num: >100 |
| quick wins/fast growers/trending | sort: gmv_B ASC |
| low competition/niche | creator_num: 1-10 |
| high margin | sort: commission_rate DESC |

#### Key Insight Calculations
- **Trend Direction**: Compares recent 7-day avg vs older avg (rising/stable/declining)
- **Competition Level**: Based on creator_num (low: 1-10, medium: 11-100, high: 100+)
- **Opportunity Score**: Composite score combining competition, trend, commission, price

#### Exports
- `ProductResearcher` class - main research interface
- `createProductResearcher` factory function
- `queryByGoal()` - AI-powered goal-based queries
- `queryByCategory()` - standard category queries
- `paginate()` - async generator for bulk retrieval

#### Skill Manifest
- Created `skills/kalodata-product-research/SKILL.md`
- Follows standard skill pattern with YAML frontmatter
- Includes usage examples, API reference, and research goal patterns

### Video Analysis Skill (Wave 1 Extension)
Created `src/kalodata/video-analysis.ts` with:

#### Features
- `getVideosForProducts()` - Get video IDs for products via `/product/enrich`
- `getVideoUrl()` - Get downloadable MP4 URL via `/video/detail/getVideoUrl`
- `getVideoUrls()` - Batch get URLs for multiple videos
- `analyzeVideos()` - Find top-performing videos per product
- `analyzeWithSummary()` - Full analysis with summary statistics
- `getProductVideos()` - Single product video analysis

#### Top Performer Detection
- Prefers original `video` content over `autocut`
- Falls back to first video in list (most prominent/recent)
- Includes reasoning for why video was selected

#### Key Design Decisions
- URLs expire - module includes warning, no long-term caching
- Batch processing with configurable delays
- Returns structured data (not raw API responses)
- Content type detection (video vs autocut)

#### Exports
- `VideoAnalyzer` class - main analysis interface
- `createVideoAnalyzer` factory function
- TypeScript interfaces for all data structures

#### Skill Manifest
- Created `skills/kalodata-video-analysis/SKILL.md`
- Follows standard skill pattern with YAML frontmatter
- Includes usage examples, API reference, and content type guide

### Storyboard Extraction Skill (Wave 1 Extension)
Created `src/kalodata/storyboard-extract.ts` with:

#### Features
- `extractStoryboard()` - Trigger and wait for AI storyboard generation via `/aiTask/startAiTask`
- `analyzeStoryboard()` - Extract key insights (key_to_success, camera_work, scenes)
- `generateContentIdeas()` - Auto-generate 5 content angles from analysis
- Polling with timeout via `waitForVideoScript` helper

#### Storyboard Data Structure
From `/aiTask/video/getVideoScript` response:
- `key_to_success`: What made the video viral (array of factors)
- `camera_work`: Camera techniques used
- `video_scripts`: Array of scenes with:
  - `scene`: Scene name
  - `shot_scale`: Full Shot, Close Up, etc.
  - `visual_description`: How to showcase product
  - `start_time`, `end_time`: Timing

#### Auto-Generated Content Ideas
Generates 5 content angles:
1. **demonstration** - Show product directly with info
2. **transformation** - Show 360° views, different angles
3. **lifestyle** - Real experience with natural poses
4. **problem-solution** - Show product in action
5. **emotional** - Build connection, CTA at end

#### Exports
- `StoryboardExtractor` class - main extraction interface
- `createStoryboardExtractor` factory function
- TypeScript interfaces for all data structures

#### Skill Manifest
- Created `skills/kalodata-storyboard-extract/SKILL.md`
- Follows standard skill pattern with YAML frontmatter
- Includes usage examples, API reference, and content idea angles

### Research Automation Composite Skill (Wave 2 - Complete Integration)
Created `skills/kalodata-research-automation/` combining all three modules:

#### Features
- `runResearch(params)` - Main entry point accepting:
  - `category`: Product category (Fashion, Beauty, Electronics, etc.)
  - `goal`: Research goal (emerging, trending, bestsellers, low competition)
  - `dateRange`: Optional date range
  - `depth`: Analysis depth (products | videos | full)
  - `topProducts`: Number of products to analyze
- `generateReport(data)` - Creates structured markdown report
- `updateCredentials()` - Updates auth for all modules

#### Analysis Depth Levels
| Depth | Products | Videos | Storyboards | Use Case |
|-------|----------|--------|-------------|----------|
| products | ✓ | ✗ | ✗ | Quick market overview |
| videos | ✓ | ✓ | ✗ | Video marketing insights |
| full | ✓ | ✓ | ✓ | Complete competitive analysis |

#### Report Output Structure
1. **Executive Summary** - Top 3 product recommendations with scores
2. **Product Analysis** - Metrics table (revenue, creators, conversion, etc.)
3. **Video Performance** - Top video per product with content type
4. **What Made This Video Successful** - key_to_success factors
5. **Camera Work Recommendations** - Techniques to replicate
6. **Scene-by-Scene Breakdown** - Timing, shot scale, descriptions
7. **Usage Scenarios** - How to demonstrate the product
8. **Auto-Generated Content Ideas** - 5 angles per product
9. **Recommendations** - Strategic next steps

#### File Structure
```
skills/kalodata-research-automation/
├── SKILL.md          # Skill manifest with YAML frontmatter
└── index.ts         # Implementation combining all 3 modules
```

#### Dependencies
- ProductResearcher from product-research.ts
- VideoAnalyzer from video-analysis.ts  
- StoryboardExtractor from storyboard-extract.ts

#### Environment Variables
- KALODATA_SESSION - Session cookie
- KALODATA_CF_CLEARANCE - Cloudflare clearance

