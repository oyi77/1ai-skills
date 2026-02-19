---
name: kalodata-video-analysis
description: Get videos associated with products, extract video metadata, get downloadable video URLs, and identify top-performing videos for competitive analysis. Use when analyzing video marketing strategies, finding best-performing creative assets, or building video intelligence reports.
---

# Kalodata Video Analysis

Get videos associated with products, extract downloadable video URLs, and identify top-performing videos for competitive analysis.

## Quick Start

### Basic Video Analysis
```typescript
import { VideoAnalyzer } from '../../src/kalodata/video-analysis.js';

const analyzer = new VideoAnalyzer({
  cookies: 'SESSION=xxx; cf_clearance=yyy; ...',
});

// Or use environment variable: export KALODATA_COOKIES="your_cookies"

// Get videos for products
const productIds = ['1732844308471449032', '1730004337700932599'];
const videos = await analyzer.getVideosForProducts(productIds);
```

### Get Download URLs
```typescript
// Get downloadable URL for a single video
const url = await analyzer.getVideoUrl('7600772739623914770');

// Get URLs for multiple videos
const urls = await analyzer.getVideoUrls(['7600772739623914770', '7601457368899030279']);
```

### Analyze Products for Top Videos
```typescript
// Analyze products and find top-performing videos
const analysis = await analyzer.analyzeWithSummary(products, {
  dateRange: { start: '2026-01-01', end: '2026-02-19' },
  includeDownloadUrls: true,
});

console.log(analysis.summary);
console.log(analysis.products[0].topPerformer);
```

## Use This Skill When

- **Video Discovery**: Find videos associated with products
- **Competitive Analysis**: Identify top-performing videos for products
- **Creative Research**: Get downloadable video URLs for analysis
- **Content Strategy**: Understand video patterns in a category

## Do Not Use This Skill When

- Need real-time video streaming (use TikTok API directly)
- Need video engagement metrics (use Kalodata's analytics)
- Need creator information (use Kalodata's creator endpoints)

## Core Features

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
- [Product Research Skill](./kalodata-product-research.md) - Product intelligence
