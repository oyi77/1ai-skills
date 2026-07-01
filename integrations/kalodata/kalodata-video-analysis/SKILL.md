---
name: kalodata-video-analysis
description: Get videos associated with products, extract video metadata, get downloadable video URLs, and identify top-performing
  videos for competitive analysis. Use when analyzing video marketing strategies, finding best-performing creative assets,
  or building video intelligence reports.
domain: integrations
tags:
- api
- integrations
- kalodata
- third-party
- video
---

# Kalodata Video Analysis

Get videos associated with products, extract downloadable video URLs, and identify top-performing videos for competitive analysis.

## Overview

Enables getting videos associated with products, extracting downloadable video URLs, and identifying top-performing videos for competitive analysis. Provides video discovery, top performer identification, and downloadable URL extraction.

## When to Use

- **Video Discovery**: Find videos associated with products
- **Competitive Analysis**: Identify top-performing videos for products
- **Creative Research**: Get downloadable video URLs for analysis
- **Content Strategy**: Understand video patterns in a category

## The Process

1. **Identify products** – Select products for video analysis
2. **Get videos for products** – Extract video IDs using the analyzer
3. **Find top performers** – Identify best-performing videos
4. **Get download URLs** – Extract downloadable video URLs
5. **Analyze and act** – Review video content strategy

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- Trying to access videos without valid Kalodata cookies
- Expecting real-time video data (this skill provides historical analysis)
- Not checking URL expiration times (download URLs are temporary)
- Ignoring product video association issues

## Verification

- Videos are correctly associated with products in results
- Top-performing videos match expected metrics (views, engagement)
- Downloadable URLs are valid MP4 links
- Video metadata includes accurate duration, likes, comments
- Analysis summary provides actionable insights

## Do Not Use This Skill When

- Need real-time video streaming (use TikTok API directly)
- Need video engagement metrics (use Kalodata's analytics)
- Need creator information (use Kalodata's creator endpoints)

## Core Features
- Core operation execution with comprehensive error handling
- Input validation and output quality assurance
- Integration with existing workflows and toolchains
- Detailed logging for debugging and audit trails


### 1. Get Videos for Products
Uses `POST /product/enrich` endpoint to retrieve video IDs for products.

```typescript
const videos = await analyzer.getVideosForProducts(productIds, {
  start: '2026-01-01',
  end: '2026-02-19',
});
```

### 2. Get Downloadable URLs
Uses `GET /video/detail/getVideoUrl` to get MP4 download URLs.

```typescript
const url = await analyzer.getVideoUrl(videoId);
// Returns: https://live.kalocdn.com/video/7600772739623914770.mp4?key=...
```

**Note**: URLs expire - do not cache long-term.

### 3. Top-Performing Video Identification
Automatically identifies the best video based on:
- Original video content (preferred over autocut)
- First in list (most prominent/recent)

```typescript
const topVideo = analysis.products[0].topPerformer;
// {
//   videoId: '7600772739623914770',
//   contentType: 'video',
//   downloadUrl: 'https://...',
//   reason: 'Original video content - typically has higher engagement than autocut'
// }
```

### 4. Batch Processing
Process multiple products efficiently with batch operations.

```typescript
const analysis = await analyzer.analyzeVideos(products, {
  includeDownloadUrls: true,
  maxVideosPerProduct: 10,
});
```

### 5. Structured Results
Returns business-ready data, not raw API responses.

```typescript
interface ProductVideoAnalysis {
  productId: string;
  productTitle: string;
  videos: VideoInfo[];
  topPerformer: TopPerformingVideo | null;
  totalVideos: number;
  hasAutocut: boolean;
}
```

## API Reference
| Endpoint/Method | Description |
|----------------|-------------|
| `GET /status` | Check service health and availability |
| `POST /execute` | Run the primary operation |
| `GET /results` | Retrieve operation results |
| `DELETE /cache` | Clear cached data |


### VideoAnalyzer Class

```typescript
class VideoAnalyzer {
  constructor(options: ClientOptions);
  
  // Video retrieval
  getVideosForProducts(productIds: string[], dateRange?: DateRange): Promise<ProductVideos[]>;
  getVideoUrl(videoId: string): Promise<string | null>;
  getVideoUrls(videoIds: string[]): Promise<Map<string, string | null>>;
  
  // Analysis
  analyzeVideos(products: Product[], options?: AnalysisOptions): Promise<ProductVideoAnalysis[]>;
  analyzeWithSummary(products: Product[], options?: AnalysisOptions): Promise<VideoAnalysisResult>;
  getProductVideos(productId: string, options?: ProductVideoOptions): Promise<ProductVideoAnalysis | null>;
  
  // Utilities
  updateCredentials(session: string, cfClearance: string): void;
}
```

### AnalysisOptions Interface

```typescript
interface AnalysisOptions {
  dateRange?: { start: string; end: string };
  includeDownloadUrls?: boolean;
  maxVideosPerProduct?: number;
}
```

### VideoInfo Interface

```typescript
interface VideoInfo {
  id: string;
  contentType: 'video' | 'autocut' | string;
  downloadUrl?: string;
  urlExpiry?: string;
}
```

### TopPerformingVideo Interface

```typescript
interface TopPerformingVideo {
  videoId: string;
  contentType: string;
  downloadUrl?: string;
  reason: string;
}
```

### VideoAnalysisResult Interface

```typescript
interface VideoAnalysisResult {
  products: ProductVideoAnalysis[];
  summary: {
    totalProducts: number;
    totalVideos: number;
    productsWithVideos: number;
    productsWithoutVideos: number;
  };
  metadata: {
    queryTime: string;
    dateRange: { start: string; end: string };
  };
}
```

## Video Content Types

| Type | Description |
|------|-------------|
| `video` | Original video content - typically higher engagement |
| `autocut` | Auto-generated highlight video - lower production value |

## Integration Example

```typescript
import { ProductResearcher } from '../../src/kalodata/product-research.js';
import { VideoAnalyzer } from '../../src/kalodata/video-analysis.js';

async function analyzeCategoryVideos(categoryId: string) {
  const researcher = new ProductResearcher({
    session: process.env.KALODATA_SESSION!,
    cfClearance: process.env.KALODATA_CF_CLEARANCE!,
  });
  
  const analyzer = new VideoAnalyzer({
    session: process.env.KALODATA_SESSION!,
    cfClearance: process.env.KALODATA_CF_CLEARANCE!,
  });
  
  // Get top products in category
  const products = await researcher.queryByCategory({
    categoryId,
    dateRange: { start: '2026-01-01', end: '2026-02-19' },
    pageSize: 20,
  });
  
  // Analyze videos for these products
  const analysis = await analyzer.analyzeWithSummary(products, {
    includeDownloadUrls: true,
  });
  
  // Report top performers
  for (const product of analysis.products) {
    if (product.topPerformer) {
      console.log(`${product.productTitle}: ${product.topPerformer.videoId}`);
      console.log(`  Reason: ${product.topPerformer.reason}`);
    }
  }
  
  return analysis;
}
```

## Best Practices

1. **URL Expiry**: Video URLs expire - use immediately or re-fetch
2. **Batch Processing**: Use batch methods for multiple videos
3. **Rate Limiting**: Add delays between bulk requests
4. **Content Type**: Prefer original videos over autocut for analysis
5. **Date Range**: Use consistent date ranges for comparative analysis

## Environment Variables

```bash
# Required
KALODATA_SESSION=your_session_cookie
KALODATA_CF_CLEARANCE=your_cf_clearance_token

# Optional
KALODATA_COUNTRY=ID
KALODATA_CURRENCY=IDR
KALODATA_LANGUAGE=id-ID
```

## Error Handling

```typescript
try {
  const videos = await analyzer.getVideosForProducts(productIds);
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

## See Also

- [Kalodata API Client](../src/kalodata/client.ts) - Core API client
- [Kalodata Types](../src/kalodata/types.ts) - TypeScript definitions
- Product Research Skill - Product intelligence

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I will handle auth later" | Retrofitting auth is 10x harder. Build it from day one. |
| "APIs do not change" | APIs change. Version your integrations and handle deprecations. |
| "Webhooks are optional" | Without webhooks, you miss real-time events. They are essential. |