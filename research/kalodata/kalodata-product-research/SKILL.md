---
name: kalodata-product-research
description: Query and analyze TikTok Shop products by category with intelligent filtering, sorting, and AI-powered research goal detection. Use when researching trending products, finding emerging winners, analyzing competition, or building product intelligence reports.
---

# Kalodata Product Research

Query and analyze TikTok Shop products using Kalodata's product intelligence API with intelligent filtering and research goal detection.

## Quick Start

### Basic Product Query
```typescript
import { ProductResearcher, parseCookies } from '../../src/kalodata/product-research.js';

// Just provide raw cookies - we'll extract what we need
const researcher = new ProductResearcher({
  cookies: 'SESSION=xxx; cf_clearance=yyy; ...',
});

// Or use environment variable
// export KALODATA_COOKIES="your_full_cookie_string"
const researcher2 = new ProductResearcher(); // reads from KALODATA_COOKIES

// Query products in a category
const products = await researcher.queryByCategory({
  categoryId: '600138989',
  dateRange: { start: '2026-01-01', end: '2026-02-19' },
});
```

### Alternative: Direct from Browser
Just copy all cookies from Kalodata.com and paste:
```typescript
const researcher = new ProductResearcher({
  cookies: 'paste_all_cookies_here',
});
```

### Research Goal Query (AI Filter Intelligence)
```typescript
// Auto-adjusts filters based on research goal
const emerging = await researcher.queryByGoal({
  goal: 'find emerging products',
  categoryId: '600138989',
  dateRange: { start: '2026-01-01', end: '2026-02-19' },
});

const winners = await researcher.queryByGoal({
  goal: 'find stable winners',
  categoryId: '600138989',
  dateRange: { start: '2026-01-01', end: '2026-02-19' },
});
```

## Use This Skill When

- **Product Discovery**: Find trending or emerging products in any TikTok Shop category
- **Competitive Analysis**: Analyze creator count, pricing, and revenue patterns
- **Market Research**: Understand category performance and trends
- **Trend Identification**: Spot products with rising revenue trends
- **Opportunity Finding**: Discover low-competition niches

## Do Not Use This Skill When

- Need real-time inventory or pricing (use TikTok Shop API directly)
- Need creator/influencer data (use Kalodata's creator endpoints)
- Need video performance data (use Kalodata's video endpoints)

## Core Features

### 1. Category-Based Queries
Query products by primary or secondary category ID:
- `cateIds`: Main category filter
- `showCateIds`: Display category for results

### 2. Flexible Filters
| Filter | API Key | Description |
|--------|---------|-------------|
| Date Range | `startDate`, `endDate` | Analysis period |
| Price Range | `product.filter.unit_price` | Min-Max price (e.g., "10000-50000") |
| Revenue Range | Custom | Filter by revenue |
| Creator Count | `product.filter.creator` | Number of creators (e.g., "1-10", "10-100") |
| Sales Channel | `product.filter.sales_channel` | "online", "offline", "all" |
| Strategy | `product.filter.strategy` | "affiliate", "self-operated", "all" |
| Affiliate Type | `product.filter.affiliate_type` | Commission type |

### 3. Sorting Options
| Field | Description |
|-------|-------------|
| `revenue` | Total revenue |
| `gmv_A` | GMV Volume A |
| `gmv_B` | GMV Volume B |
| `sale` | Number of sales |
| `creator_num` | Number of creators |
| `revenue_trend` | Revenue trend (array-based) |

### 4. AI Filter Intelligence

Automatically adjusts filters based on research goals:

| Research Goal | Auto-Adjusted Filters |
|--------------|----------------------|
| **Find emerging products** | `sort: revenue_trend ASC`, recent `launch_date`, low-mid `creator_num` |
| **Find stable winners** | `sort: revenue DESC`, high `creator_num`, established `launch_date` |
| **Find quick wins** | `sort: gmv_B ASC` (fastest growth) |
| **Low competition** | `creator_num: 1-10`, `sort: revenue DESC` |
| **High margin** | Sort by `commission_rate DESC` |
| **Trending now** | `sort: revenue_trend DESC`, recent `dateRange` |

### 5. Pagination
- Automatic pagination via `pageNo` and `pageSize`
- Built-in `paginate()` helper for bulk retrieval
- `getTotalCount()` for estimating total results

### 6. Structured Insights

Returns processed data with business-ready insights:

```typescript
interface ProcessedProduct {
  id: string;
  title: string;
  price: { min: number; max: number };
  revenue: number;
  revenueTrend: number[];
  sales: number;
  creators: number;
  conversionRate: number;
  launchDate: string;
  rating: number;
  isOverseas: boolean;
  isFullService: boolean;
  insights: {
    trendDirection: 'rising' | 'stable' | 'declining';
    competitionLevel: 'low' | 'medium' | 'high';
    opportunityScore: number;
  };
}
```

## API Reference

### ProductResearcher Class

```typescript
class ProductResearcher {
  constructor(options: ClientOptions);
  
  // Query methods
  queryByCategory(params: QueryParams): Promise<ProcessedProduct[]>;
  queryByGoal(params: GoalQueryParams): Promise<ProcessedProduct[]>;
  
  // Pagination
  paginate(params: QueryParams, maxPages?: number): AsyncGenerator<ProcessedProduct[]>;
  
  // Utilities
  getTotalCount(params: QueryParams): Promise<number>;
  getCategories(): Promise<Category[]>;
}
```

### QueryParams Interface

```typescript
interface QueryParams {
  categoryId: string;
  dateRange: { start: string; end: string };
  filters?: {
    priceMin?: number;
    priceMax?: number;
    revenueMin?: number;
    revenueMax?: number;
    creatorMin?: number;
    creatorMax?: number;
    salesChannel?: 'online' | 'offline' | 'all';
    strategy?: 'affiliate' | 'self-operated' | 'all';
  };
  sort?: { field: string; type: 'ASC' | 'DESC' }[];
  pageSize?: number;
  pageNo?: number;
}
```

### GoalQueryParams Interface

```typescript
interface GoalQueryParams {
  goal: string;
  categoryId: string;
  dateRange: { start: string; end: string };
  filters?: Partial<QueryParams['filters']>;
  pageSize?: number;
}
```

## Research Goal Patterns

### Finding Emerging Products
```
Goal: "find emerging products", "new products", "rising stars", "just launched"
Filters Applied:
- sort: revenue_trend ASC
- launch_date: within last 30 days
- creator_num: 10-100 (some traction but not saturated)
```

### Finding Stable Winners
```
Goal: "stable winners", "best sellers", "proven products", "market leaders"
Filters Applied:
- sort: revenue DESC
- creator_num: >100 (wide creator adoption)
- launch_date: >60 days ago
```

### Finding Quick Wins
```
Goal: "quick wins", "fast growers", "trending now", "viral products"
Filters Applied:
- sort: gmv_B ASC (growth rate)
- revenue_trend: trending up
- dateRange: last 7-14 days
```

### Finding Low Competition
```
Goal: "low competition", "niche products", "underserved markets", "easy to rank"
Filters Applied:
- creator_num: 1-10
- sort: revenue DESC
- exclude: saturated categories
```

## Error Handling

```typescript
try {
  const products = await researcher.queryByCategory(params);
} catch (error) {
  if (error instanceof AuthenticationError) {
    // Invalid credentials - prompt for new session/cf_clearance
  } else if (error instanceof RateLimitError) {
    // Wait and retry with backoff
  } else {
    // Handle other errors
  }
}
```

## Environment Variables

```bash
# Required
KALODATA_SESSION=your_session_cookie
KALODATA_CF_CFLEARANCE=your_cf_clearance_token

# Optional
KALODATA_COUNTRY=ID
KALODATA_CURRENCY=IDR
KALODATA_LANGUAGE=id-ID
```

## Common Category IDs (TikTok Shop Indonesia)

| Category | ID |
|----------|-----|
| Fashion | 600138989 |
| Electronics | 600136323 |
| Beauty | 600137235 |
| Home & Living | 600138081 |
| Food & Beverage | 600138171 |
| Mother & Baby | 600138251 |
| Sports | 600138431 |
| Toys & Games | 600138621 |
| Books | 600138761 |

## Integration Example

```typescript
// Complete research workflow
import { ProductResearcher } from '../../src/kalodata/product-research.js';

async function researchCategory(categoryId: string) {
  const researcher = new ProductResearcher({
    session: process.env.KALODATA_SESSION!,
    cfClearance: process.env.KALODATA_CF_CLEARANCE!,
  });

  // Get overview with emerging products
  const emerging = await researcher.queryByGoal({
    goal: 'find emerging products',
    categoryId,
    dateRange: { start: '2026-01-01', end: '2026-02-19' },
  });

  // Get stable winners
  const winners = await researcher.queryByGoal({
    goal: 'find stable winners',
    categoryId,
    dateRange: { start: '2026-01-01', end: '2026-02-19' },
  });

  // Generate report
  return {
    emerging: emerging.slice(0, 10),
    winners: winners.slice(0, 10),
    insights: {
      totalEmerging: emerging.length,
      totalWinners: winners.length,
    }
  };
}
```

## Best Practices

1. **Date Range**: Use 30-90 day ranges for trend analysis
2. **Pagination**: Always paginate for comprehensive data
3. **Caching**: Don't cache video URLs (they expire)
4. **Rate Limiting**: Add delays between requests
5. **Error Handling**: Always handle auth errors gracefully

## See Also

- [Kalodata API Client](../src/kalodata/client.ts) - Core API client
- [Kalodata Types](../src/kalodata/types.ts) - TypeScript definitions
- [Video Research Skill](./kalodata-video-research.md) - Video content analysis
