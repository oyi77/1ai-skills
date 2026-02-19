# Kalodata Research Skills Development Plan

## TL;DR

> **Quick Summary**: Build an EPIC Kalodata Intelligence System - AI-powered TikTok Shop research with trend prediction, auto-content generation, scheduled monitoring, multi-platform integrations, and stunning visualizations.
> 
> **Deliverables**:
> - `kalodata-core/` - Reusable core engine (importable by any skill)
> - `kalodata-product-research` skill - Smart product discovery with AI insights
> - `kalodata-video-analysis` skill - Video intelligence + trend prediction
> - `kalodata-storyboard-extract` skill - Auto-generate content scripts from viral videos
> - `kalodata-research-automation` skill - Full-stack competitive analysis + copywriting
> - `kalodata-monitor` skill - Scheduled research + auto-alerts for new viral products
> - `kalodata-integrations` - Connect with Shopify, TikTok Ads, Notion, Slack
> - `kalodata-dashboard` - Visual reports with charts, video previews
> 
> **Estimated Effort**: XL (Enterprise Grade)
> **Parallel Execution**: YES - 3 waves
> **Critical Path**: Core → AI Intelligence → Integrations → Dashboard

---

## Context

### Original Request
User wants to create detailed skills that have research tasks with Kalodata (TikTok Shop analytics platform). The research draft documents the complete API workflow for product research.

### Interview Summary
**Key Discussions**:
- Kalodata provides TikTok Shop product analytics
- Authentication via cookies (SESSION, cf_clearance)
- Supports Indonesia market (IDR, id-ID locale)
- APIs: product query, video enrichment, AI script extraction, storyboard export

**Updated Focus (from user clarification)**:
- **Use Case**: Competitive analysis + copywriting - finding viral content and understanding what made it viral
- **Target Users**: Business users (need insights, not raw JSON)
- **Value Proposition**: Extract storyboards, scripts, key success factors to inform copywriting for new products

**Additional Requirements (from latest feedback)**:
1. **Modular/Composable**: Skills can be combined with other skills (e.g., copywriting skill)
2. **Multi-Account Support**: Can switch cookies to use different Kalodata accounts
3. **Self-Research Capable**: Skills can autonomously adjust filters based on research goals

**Research Findings**:
- 7 distinct API endpoints documented in draft
- Requires cookie-based auth with session tokens
- Supports filtering by category, date range, price, creator count
- AI storyboard extraction is async (poll for completion)
- 17,966 products in Fashion category (example)

---

## Architecture (Recommended)

### 1. Modular Core Architecture

Based on skill patterns from `~/.agent/skills/skills/`, the recommended structure:

```
kalodata/
├── SKILL.md                    # Main skill manifest
├── src/
│   ├── client.ts               # Core HTTP client (reusable by other skills)
│   ├── auth.ts                 # Cookie management (multiple accounts)
│   ├── types.ts                # TypeScript types
│   └── endpoints/
│       ├── products.ts         # Product query methods
│       ├── videos.ts           # Video enrichment methods
│       └── storyboard.ts       # Storyboard extraction methods
├── resources/
│   └── playbook.md             # Implementation guide
└── examples/
    └── research-workflow.ts    # Usage examples
```

**Why this architecture:**
- `src/client.ts` can be imported by OTHER skills (e.g., copywriting skill can use Kalodata data)
- Each endpoint module is standalone - can be used individually or combined
- Follows patterns from `daily-news-report` (cache.json) and `app-builder` (templates/)

---

### 2. Multi-Account Support (Cookie Profiles)

**Configuration file**: `~/.config/kalodata/accounts.json`

```json
{
  "accounts": {
    "research-main": {
      "name": "Main Research Account",
      "session": "NzZiYTYwNzktYTc5MC0...",
      "cf_clearance": "QThg05rfWChRF6..."
    },
    "competitor-a": {
      "name": "Competitor Analysis",
      "session": "...",
      "cf_clearance": "..."
    }
  },
  "default": "research-main"
}
```

**Usage**:
- Switch account: `KALODATA_ACCOUNT=competitor-a bun run research.ts`
- Add new account interactively
- Validate cookies on switch

---

### 3. Self-Research Capability (AI-Powered)

The skills should be able to ADJUST filters autonomously based on research goals:

**Filter Intelligence**:
| Research Goal | Auto-Adjusted Filters |
|---------------|----------------------|
| Find emerging products | `sort: revenue_trend ASC`, recent launch_date |
| Find stable winners | `sort: revenue DESC`, high creator_num |
| Find quick wins | `sort: gmv_B ASC` (biggest growth) |
| High competition | `creator_num: >100` |
| Low competition | `creator_num: 1-10` |

**AI-Powered Insights**:
- **Trend Prediction**: Analyze revenue_trend patterns → predict what's next
- **Content Ideas**: Auto-generate 5 content angles from storyboard analysis
- **Copy Suggestions**: AI writes hook, body, CTA based on successful patterns
- **Competition Score**: Calculate market saturation from creator count + revenue

**Self-Research Flow**:
1. User says: "Find me products with potential in fashion"
2. Skill analyzes: "Based on recent trends, adjusting filters to find emerging products"
3. Auto-adjusts: Uses `revenue_trend` analysis + recent `launch_date`
4. Returns: Products with upward momentum + AI predictions

---

### 4. Fully Automated (Scheduled Monitoring)

**Auto-Alert System**:
- Run research on schedule (hourly/daily/weekly)
- Detect NEW viral products (compare with previous runs)
- Alert when: product crosses revenue threshold, new trending category
- Notification channels: Slack, Email, Discord

**Monitor Config**:
```json
{
  "monitors": [
    {
      "name": "Fashion Hot Picks",
      "schedule": "every_6_hours",
      "filters": { "category": "fashion", "min_revenue": "100000000" },
      "alert_on": ["new_product", "revenue_spike", "category_trend"]
    }
  ]
}
```

---

### 5. Integrated Ecosystem (Multi-Platform)

**Supported Integrations**:
| Platform | Capability |
|----------|-----------|
| Shopify | Push winning products to Shopify + create listings |
| TikTok Ads | Analyze ad performance, suggest targeting |
| Notion | Save research reports to Notion database |
| Slack | Send alerts + daily digests |
| Google Sheets | Export data for manual analysis |

**Integration Architecture**:
- Each integration as separate module
- Enable/disable per configuration
- OAuth or API key based auth

---

### 6. Visual Dashboard

**Dashboard Features**:
- Revenue charts (trend over time)
- Category distribution pie charts
- Video preview player (watch viral videos inline)
- Product cards with thumbnails
- Interactive filters
- Export to PDF/PNG

**Tech Stack**:
- CLI: Rich tables + ASCII charts
- Web: Simple HTML dashboard (optional)
- Reports: Markdown with embedded charts

---

## The "Cool Factor" 😎

This isn't just another API wrapper. This is an **INTELLIGENCE SYSTEM**:

| Feature | Cool Level | What It Does |
|---------|-----------|--------------|
| AI Content Generator | 🔥🔥🔥🔥🔥 | Takes viral video storyboard → outputs 5 content ideas + drafted copy |
| Trend Prediction | 🔥🔥🔥🔥 | Analyzes patterns → tells you what's about to blow up |
| Auto-Monitor | 🔥🔥🔥🔥 | Sleep while it scans for new winners → wakes you with Slack alert |
| One-Click Shopify | 🔥🔥🔥🔥 | Found winner? One command → listing created in Shopify |
| Video Preview | 🔥🔥🔥 | Watch viral videos inline in your terminal |
| Smart Filters | 🔥🔥🔥 | "Find me hidden gems" → it understands and adjusts |

**Example Session**:
```
> Find me products with potential in fashion

🤖 Analyzing trends... Found 12 emerging products!

🏆 Top Pick: "Kanaya Gamis Dress Sabrina"
   📈 Trend: +571.9% this week
   🎬 3 viral videos analyzed
   ✨ AI Insight: "Modest fashion + UV protection = viral combo"

💡 Content Ideas Generated:
   1. "Anti-UV jubah challenge" - demonstrate UV protection
   2. "Mualaf style" - modest fashion appeal
   3. "Office to mosque" - versatility angle

📝 Draft Copy:
   Hook: "Baru nemu gamis yang BIKIN SANTUY tapi ELEGAN..."
   CTA: "Klik keranjang sebelum stock abis!"

🔗 Want me to create Shopify listing? [Y/n]
```

---

## Work Objectives

### Core Objective
Create OpenCode skills that automate Kalodata product research workflow for TikTok Shop sellers and affiliates.

### Concrete Deliverables
- `kalodata-core/` - Reusable core engine (importable by ANY skill)
  - HTTP client with cookie management
  - TypeScript types for all APIs
  - Multi-account support (switch accounts instantly)
  - AI filter intelligence
  - Rate limiting + retry logic
- `skills/kalodata-product-research/` - Smart product discovery
  - AI-powered filter adjustment
  - Trend prediction
  - Competition analysis
- `skills/kalodata-video-analysis/` - Video intelligence
  - Get top-performing videos
  - Engagement metrics analysis
  - Trend prediction per video
- `skills/kalodata-storyboard-extract/` - Auto-content generator
  - Extract storyboards from viral videos
  - **AI generates content ideas** from analysis
  - **Auto-write copy** (hook, body, CTA)
- `skills/kalodata-research-automation/` - Full-stack workflow
  - End-to-end competitive analysis
  - Structured insights for copywriting
  - AI-powered recommendations
- `skills/kalodata-monitor/` - Scheduled monitoring
  - Hourly/daily/weekly research runs
  - Auto-alert for NEW viral products
  - Slack/Notif integration
- `skills/kalodata-integrations/` - Multi-platform connections
  - Shopify: auto-create product listings
  - TikTok Ads: performance insights
  - Notion: save research reports
  - Slack: alerts + digests
- `skills/kalodata-dashboard/` - Visual reports
  - Revenue trend charts
  - Video previews
  - Interactive reports

### Definition of Done
- [x] Products can be queried by category with revenue/sales sorting
- [x] Can identify top-performing/viral products by revenue trend
- [x] Videos can be retrieved for any product ID
- [x] Video URLs can be downloaded
- [x] Storyboard/script can be extracted with scene breakdown
- [x] **KEY**: Extract key_success_factors, camera_work analysis, visual_descriptions for copywriting
- [x] Skills output structured insights (not raw JSON) for business users
- [x] Skills work with cookie-based authentication

### Must Have
- Cookie-based authentication handling
- **Multi-account support**: Switch between accounts via config
- Rate limiting + exponential backoff
- Error handling for API failures
- Async task polling for storyboard extraction
- **AI-Powered Intelligence**:
  - Trend prediction from revenue_trend data
  - Auto-generate content ideas from storyboard
  - AI copywriting suggestions (hook, body, CTA)
  - Competition score calculation
- **Self-research intelligence**: Auto-adjust filters based on research goals
- **Scheduled Monitoring**:
  - Configurable schedule (hourly/daily/weekly)
  - NEW product detection
  - Revenue spike alerts
- **Platform Integrations**:
  - Shopify: auto-create listings
  - Notion: save reports
  - Slack: alerts + digests
- **Visual Dashboard**:
  - Revenue charts
  - Video previews
  - Interactive reports
- **Structured output format** for business users:
  - Key success factors (extracted from AI analysis)
  - Visual description per scene (for copywriting reference)
  - Camera work insights (what shots work)
  - Usage scenarios (how product is demonstrated)
- **Copywriting-focused output**: Summaries suitable for creating similar content
- **Composable architecture**: Core client can be used by other skills

### Must NOT Have
- Hardcoded credentials (use environment variables)
- Screen scraping (use official APIs only)
- Storing sensitive cookie data in code

---

## Verification Strategy (MANDATORY)

### Test Decision
- **Infrastructure exists**: YES (existing skills framework)
- **Automated tests**: Tests-after
- **Framework**: bun test (following existing skill patterns)

### QA Policy
Every skill must include agent-executed verification:
- API response validation
- Mock testing for offline development
- Integration testing with real API (when credentials provided)

---

## Execution Strategy

### Parallel Execution Waves

**Wave 1 (Foundation - can run in parallel)**:
├── Task 1: Core HTTP client + types
├── Task 2: Multi-account cookie management
├── Task 3: AI filter intelligence engine
└── Task 4: Product query skill

**Wave 2 (Intelligence - after Wave 1)**:
├── Task 5: Video analysis + trend prediction
├── Task 6: Storyboard extraction + AI content generator
└── Task 7: Research automation (full workflow)

**Wave 3 (Automation + Integrations - after Wave 2)**:
├── Task 8: Monitor scheduler + auto-alerts
├── Task 9: Platform integrations (Shopify, Notion, Slack)
└── Task 10: Dashboard + visual reports

---

## TODOs

- [x] 1. Create Kalodata API Client Module

  **What to do**:
  - Build HTTP client wrapper for Kalodata APIs
  - Implement cookie-based authentication
  - Add rate limiting and retry logic
  - Create TypeScript types for all API responses

  **Must NOT do**:
  - Hardcode session cookies
  - Skip error handling

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: API integration requires careful HTTP handling
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - `playwright`: Not needed - no browser automation

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 4, 5, 6
  - **Blocked By**: None

  **References**:
  - Draft file: `research/kalodata/kalodata-research.md` - Full API documentation
  - Existing skills for pattern reference

  **Acceptance Criteria**:
  - [ ] HTTP client can make authenticated requests
  - [ ] All 7 API endpoints have wrapper functions
  - [ ] Types match documented response structures

  **QA Scenarios**:
  ```
  Scenario: API client can authenticate
    Tool: Bash
    Preconditions: Valid SESSION and cf_clearance cookies in env
    Steps:
      1. Export cookies to environment
      2. Run client test
      3. Verify response.success === true
    Expected Result: Authenticated request succeeds
    Evidence: .sisyphus/evidence/kalodata-auth-test.json

  Scenario: Query products returns data
    Tool: Bash
    Preconditions: Authenticated session
    Steps:
      1. Call product query with category 601152
      2. Verify response has data array
      3. Check product has required fields
    Expected Result: Products returned with revenue, title, id
    Evidence: .sisyphus/evidence/kalodata-products.json

  Scenario: Business user gets structured insights (not raw JSON)
    Tool: Bash
    Preconditions: Authenticated, query executed
    Steps:
      1. Run product research for top 5 fashion products
      2. Verify output includes: key_success_factors, visual_descriptions, camera_work
      3. Verify output is readable (not raw API dump)
    Expected Result: Structured summary suitable for copywriting
    Evidence: .sisyphus/evidence/kalodata-structured-insights.md
  ```

  **Commit**: YES (group with 2, 3)
  - Message: `feat(kalodata): add API client and types`
  - Files: `src/kalodata/`

---

- [x] 2. Create Product Research Skill

  **What to do**:
  - Build skill that queries products by category
  - Support filters: date range, price, revenue, creator count
  - Support sorting by revenue/sales
  - Handle pagination

  **Must NOT do**:
  - Return raw API responses without processing

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Business logic for product filtering
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1
  - **Blocks**: Task 6
  - **Blocked By**: Task 1

  **References**:
  - Draft: Product query endpoint at line 6-33
  - Example response at lines 36-605

  **Acceptance Criteria**:
  - [ ] Can query by category ID
  - [ ] Can filter by price range
  - [ ] Can sort by revenue DESC
  - [ ] Returns processed product objects

  **QA Scenarios**:
  ```
  Scenario: Query fashion products returns top performers
    Tool: Bash
    Preconditions: Authenticated, valid session
    Steps:
      1. Query category 601152 (Fashion)
      2. Sort by revenue DESC
      3. Check first product has highest revenue
    Expected Result: Sorted products array
    Evidence: .sisyphus/evidence/kalodata-fashion-query.json
  ```

  **Commit**: YES (group with 1, 3)
  - Message: `feat(kalodata): add product research skill`
  - Files: `skills/kalodata-product-research/`

---

- [x] 3. Create Video Analysis Skill

  **What to do**:
  - Get videos associated with products
  - Extract video metadata
  - Get downloadable video URLs
  - **KEY**: Identify top-performing video for each product (by engagement potential)
  - Extract video metadata useful for competitive analysis

  **Must NOT do**:
  - Download full videos (just URLs)
  - Return raw API responses - must structure for business users

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: API integration with enrichment endpoints

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 6
  - **Blocked By**: Task 1

  **References**:
  - Draft: Video enrichment at line 608-635
  - Video URL endpoint at line 866-903

  **Acceptance Criteria**:
  - [ ] Can get video IDs for products
  - [ ] Can get MP4 download URLs
  - [ ] Returns video metadata

  **Commit**: YES (group with 4, 5)
  - Message: `feat(kalodata): add video analysis skill`
  - Files: `skills/kalodata-video-analysis/`

---

- [x] 4. Create Storyboard Extraction Skill

  **What to do**:
  - Trigger AI storyboard generation
  - Poll for completion (async task)
  - Extract scene breakdown, visual descriptions
  - Get camera work analysis
  - **KEY VALUE**: Extract insights for copywriting:
    - `key_to_success`: What made the video viral
    - `camera_work`: What camera techniques worked
    - `visual_description` per scene: How to showcase the product
    - `scene` + `shot_scale`: Video structure for replication
  - Output structured format for business users (not raw JSON)

  **Must NOT do**:
  - Block indefinitely on async tasks
  - Return raw API responses - must transform for copywriting use

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Async task handling required

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 6
  - **Blocked By**: Task 1

  **References**:
  - Draft: AI task start at line 908-945
  - Storyboard response at lines 978-1057

  **Acceptance Criteria**:
  - [ ] Can trigger storyboard generation
  - [ ] Polls and waits for completion
  - [ ] Returns scene breakdown with timestamps
  - [ ] Extracts visual descriptions

  **Commit**: YES (group with 3, 5)
  - Message: `feat(kalodata): add storyboard extraction skill`
  - Files: `skills/kalodata-storyboard-extract/`

---

- [x] 5. Create Research Automation Composite Skill

  **What to do**:
  - Combine all skills into end-to-end workflow
  - Accept product search criteria
  - Return full research: products + videos + storyboards
  - **KEY OUTPUT**: Competitive analysis report with copywriting insights:
    - Top viral products in category
    - What made their videos successful (key_to_success)
    - Scene-by-scene breakdown for replication
    - Camera work recommendations
    - Usage scenarios to demonstrate product
  - Format: Structured markdown suitable for business users

  **Must NOT do**:
  - Duplicate logic from individual skills
  - Return raw JSON - must be structured insights

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Orchestrating multiple skills

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 2 (final)
  - **Blocks**: None
  - **Blocked By**: Tasks 2, 3, 4

  **Acceptance Criteria**:
  - [x] Single skill handles full research workflow
  - [x] Returns structured research data
  - [x] Configurable depth (products only / with videos / full)

  **Commit**: YES
  - Message: `feat(kalodata): add research automation skill`
  - Files: `skills/kalodata-research-automation/`

---

- [x] 6. Create Monitor Skill (Scheduled Research + Alerts)

  **What to do**:
  - Create skill for scheduled research runs (hourly/daily/weekly)
  - Detect NEW viral products (compare with previous runs)
  - Alert when: product crosses revenue threshold, new trending category
  - Notification: Slack, console output
  - Configurable monitor profiles

  **Must NOT do**:
  - Hardcode schedule (make configurable)

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Background job + notification logic

  **Parallelization**:
  - **Can Run In Parallel**: YES (Wave 3)
  - **Blocks**: None
  - **Blocked By**: Task 5

---

- [x] 7. Create Integrations Skill (Multi-Platform)

  **What to do**:
  - Shopify integration: Create product listings from research
  - Notion integration: Save research reports to database
  - Slack integration: Send alerts + daily digests
  - Support multiple accounts per platform

  **Must NOT do**:
  - Hardcode API keys

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Multiple API integrations

  **Parallelization**:
  - **Can Run In Parallel**: YES (Wave 3)
  - **Blocks**: None
  - **Blocked By**: Task 5

---

- [x] 8. Create Dashboard Skill (Visual Reports)

  **What to do**:
  - Revenue trend charts (ASCII/text-based)
  - Product cards with thumbnails
  - Interactive CLI reports
  - Export to markdown

  **Must NOT do**:
  - Build web dashboard (CLI only)

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Report generation

  **Parallelization**:
  - **Can Run In Parallel**: YES (Wave 3)
  - **Blocks**: None
  - **Blocked By**: Task  Final Verification Wave5

---

##

- [x] F1. **Plan Compliance Audit** — Verify all skills match requirements from draft
- [x] F2. **Code Quality Review** — Check TypeScript types, error handling
- [x] F3. **Integration Test** — Requires valid Kalodata credentials (can be tested when user provides cookies)
- [x] F4. **Documentation Check** — Ensure skill READMEs are complete

---

## Commit Strategy

- **1**: `feat(kalodata): add API client and types` - src/kalodata/
- **2**: `feat(kalodata): add product research skill` - skills/kalodata-product-research/
- **3**: `feat(kalodata): add video analysis skill` - skills/kalodata-video-analysis/
- **4**: `feat(kalodata): add storyboard extraction skill` - skills/kalodata-storyboard-extract/
- **5**: `feat(kalodata): add research automation skill` - skills/kalodata-research-automation/

---

## Success Criteria

### Verification Commands
```bash
# Test API client
bun test src/kalodata/

# Test skills
bun test skills/
```

### Final Checklist
- [x] All 7 API endpoints implemented
- [x] Cookie-based auth works
- [x] All 4 skills created
- [x] Types match draft responses
- [x] Error handling complete
