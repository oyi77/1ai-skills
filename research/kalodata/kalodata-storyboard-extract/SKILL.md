---
name: kalodata-storyboard-extract
description: Use when extracting AI-generated storyboards from viral TikTok Shop videos, including scene breakdowns, visual descriptions, camera work analysis, and auto-generating content ideas for replication.
---

# Kalodata Storyboard Extract

Extract AI-generated storyboards from viral videos to understand what made them successful and generate content ideas for replication.

## Quick Start

### Extract Storyboard from Video
```typescript
import { StoryboardExtractor } from '../../src/kalodata/storyboard-extract.js';

const extractor = new StoryboardExtractor({
  cookies: 'SESSION=xxx; cf_clearance=yyy; ...',
});
// Or: export KALODATA_COOKIES="your_cookies"

const result = await extractor.extractStoryboard({
  videoId: '7600772739623914770',
  dateRange: { start: '2026-01-20', end: '2026-02-18' },
});

console.log(result.keyToSuccess);
console.log(result.contentIdeas);
```

## Use This Skill When

- **Analyze Viral Videos**: Understand what made a video successful
- **Extract Scene Breakdowns**: Get detailed scene-by-scene analysis
- **Camera Work Analysis**: Understand camera techniques used
- **Content Ideation**: Auto-generate 5 content ideas from any video
- **Competitor Research**: Study winning video structures for your category
- **Creative Direction**: Get visual descriptions for product showcases

## Do Not Use This Skill When

- Need real-time video metrics (use Video Analysis skill)
- Need product data (use Product Research skill)
- Need creator/influencer analytics (use Kalodata creator endpoints)

## Core Features

### 1. Storyboard Extraction
Trigger AI analysis of any video and get complete scene breakdown:

```typescript
const result = await extractor.extractStoryboard({
  videoId: '7600772739623914770',
  dateRange: { start: '2026-01-20', end: '2026-02-18' },
});
```

Returns:
- `keyToSuccess`: What made the video viral
- `cameraWork`: Camera techniques used
- `scenes`: Detailed scene breakdown
- `contentIdeas`: 5 auto-generated content angles

### 2. Key Success Factors
Extract what made the video viral:

```typescript
// Returns array of success factors
result.keyToSuccess.forEach(factor => {
  console.log(factor);
});

// Example output:
// [
//   "Menampilkan setelan pakaian modis dan tertutup (modest fashion)...",
//   "Model secara aktif berpose dan berputar...",
//   "Branding 'FashionByDea' terlihat jelas...",
//   ...
// ]
```

### 3. Camera Work Analysis
Get camera techniques used in the video:

```typescript
console.log(result.cameraWork);
// "Video ini menggunakan teknik pengambilan gambar statis..."
```

### 4. Scene Breakdown
Detailed per-scene analysis:

```typescript
result.scenes.forEach(scene => {
  console.log(`${scene.name}: ${scene.shotScale}`);
  console.log(`  ${scene.visualDescription}`);
});

// Example output:
// Product Information: Full Shot
//   Seorang wanita berhijab mengenakan setelan tunik...
// Product Selling Points: Full Shot
//   Wanita itu berputar perlahan untuk menunjukkan...
```

### 5. Auto-Generated Content Ideas
Automatically generate 5 content angles for replication:

```typescript
result.contentIdeas.forEach((idea, i) => {
  console.log(`${i + 1}. ${idea.title}`);
  console.log(`   Angle: ${idea.angle}`);
  console.log(`   ${idea.description}`);
});
```

## API Reference

### StoryboardExtractor Class

```typescript
class StoryboardExtractor {
  constructor(options: ClientOptions);
  
  // Main extraction method
  extractStoryboard(options: ExtractStoryboardOptions): Promise<StoryboardResult>;
  
  // Analysis helpers
  analyzeStoryboard(storyboard: GetVideoScriptResponse): StoryboardAnalysis;
  generateContentIdeas(storyboard: GetVideoScriptResponse): ContentIdea[];
  
  // Credentials
  updateCredentials(session: string, cfClearance: string): void;
  getConfig(): Readonly<KalodataConfig>;
}
```

### ExtractStoryboardOptions

```typescript
interface ExtractStoryboardOptions {
  videoId: string;
  dateRange: { start: string; end: string };
  translate?: boolean;
  maxAttempts?: number;
  pollIntervalMs?: number;
}
```

### StoryboardResult

```typescript
interface StoryboardResult {
  videoId: string;
  language: string;
  gender: string;
  keyToSuccess: string[];
  cameraWork: string;
  scenes: Scene[];
  contentIdeas: ContentIdea[];
  metadata: {
    extractedAt: string;
    totalDuration: number;
    sceneCount: number;
  };
}
```

### Scene

```typescript
interface Scene {
  name: string;
  startTime: number;
  endTime: number;
  duration: number;
  shotScale: string;
  visualDescription: string;
}
```

### ContentIdea

```typescript
interface ContentIdea {
  title: string;
  description: string;
  angle: 'demonstration' | 'transformation' | 'lifestyle' | 'problem-solution' | 'emotional';
  keyScene: string;
  hook: string;
}
```

## Content Idea Angles

| Angle | Description | Best For |
|-------|-------------|----------|
| **demonstration** | Show product directly with information | Educational products, new launches |
| **transformation** | Show 360° views, different angles | Fashion, beauty, accessories |
| **lifestyle** | Real experience with natural poses | All products, authenticity |
| **problem-solution** | Show product in action | Functional products, tools |
| **emotional** | Build connection, CTA at end | Engagement, conversions |

## Example Workflow

### Full Analysis Example
```typescript
import { StoryboardExtractor } from '../../src/kalodata/storyboard-extract.js';

async function analyzeViralVideo(videoId: string) {
  const extractor = new StoryboardExtractor({
    session: process.env.KALODATA_SESSION!,
    cfClearance: process.env.KALODATA_CF_CLEARANCE!,
  });

  const result = await extractor.extractStoryboard({
    videoId,
    dateRange: { start: '2026-01-20', end: '2026-02-18' },
  });

  // Print key success factors
  console.log('=== KEY SUCCESS FACTORS ===');
  result.keyToSuccess.forEach((factor, i) => {
    console.log(`${i + 1}. ${factor}\n`);
  });

  // Print camera work analysis
  console.log('=== CAMERA WORK ===');
  console.log(result.cameraWork + '\n');

  // Print scene breakdown
  console.log('=== SCENE BREAKDOWN ===');
  result.scenes.forEach(scene => {
    console.log(`[${scene.startTime}s - ${scene.endTime}s] ${scene.shotScale}: ${scene.name}`);
    console.log(`  ${scene.visualDescription}\n`);
  });

  // Print content ideas
  console.log('=== CONTENT IDEAS ===');
  result.contentIdeas.forEach((idea, i) => {
    console.log(`${i + 1}. ${idea.title} (${idea.angle})`);
    console.log(`   Hook: ${idea.hook}`);
    console.log(`   ${idea.description}\n`);
  });

  return result;
}

// Usage
analyzeViralVideo('7600772739623914770');
```

## Integration with Product Research

```typescript
import { ProductResearcher } from '../../src/kalodata/product-research.js';
import { StoryboardExtractor } from '../../src/kalodata/storyboard-extract.js';

async function researchTopProductVideos() {
  const productResearcher = new ProductResearcher({
    session: process.env.KALODATA_SESSION!,
    cfClearance: process.env.KALODATA_CF_CLEARANCE!,
  });

  const storyboardExtractor = new StoryboardExtractor({
    session: process.env.KALODATA_SESSION!,
    cfClearance: process.env.KALODATA_CF_CLEARANCE!,
  });

  // Find top products
  const products = await productResearcher.queryByGoal({
    goal: 'find stable winners',
    categoryId: '600138989',
    dateRange: { start: '2026-01-20', end: '2026-02-18' },
  });

  // Get videos for top product
  const topProduct = products[0];
  console.log(`Analyzing: ${topProduct.title}`);

  // Extract storyboard from top video
  const storyboard = await storyboardExtractor.extractStoryboard({
    videoId: topProduct.videos?.[0]?.id || '',
    dateRange: { start: '2026-01-20', end: '2026-02-18' },
  });

  return storyboard;
}
```

## Error Handling

```typescript
try {
  const result = await extractor.extractStoryboard(options);
} catch (error) {
  if (error instanceof AuthenticationError) {
    console.log('Invalid credentials - update session/cf_clearance');
  } else if (error instanceof TaskNotCompleteError) {
    console.log('Video analysis taking too long - try increasing maxAttempts');
  } else if (error.message.includes('timed out')) {
    console.log('Request timed out - video may not exist');
  }
}
```

## Environment Variables

```bash
KALODATA_SESSION=your_session_cookie
KALODATA_CF_CFLEARANCE=your_cf_clearance_token
```

## Best Practices

1. **Date Range**: Use 30-day range for accurate analysis
2. **Timeout**: Increase `maxAttempts` for complex videos (default: 30)
3. **Polling Interval**: Decrease for faster videos, increase for slower (default: 2000ms)
4. **Content Ideas**: Use as starting points - customize for your product
5. **Scene Timing**: Use `startTime` and `endTime` to replicate exact structure

## Related Skills

- [Kalodata Product Research](./kalodata-product-research.md) - Product intelligence
- [Kalodata Video Analysis](./kalodata-video-analysis.md) - Video metrics
- [Kalodata API Client](../src/kalodata/client.ts) - Core client
