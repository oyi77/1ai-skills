/**
 * Kalodata Research Automation - Composite Skill
 * 
 * End-to-end competitive analysis that combines:
 * - Product Research: Discover products by category and goal
 * - Video Analysis: Get viral videos for top products
 * - Storyboard Extraction: Scene breakdowns for content replication
 * 
 * Returns structured markdown report for business users.
 */

import {
  KalodataClient,
  createClient,
  type ClientOptions,
  type Product,
} from '../lib/index.js';

import {
  ProductResearcher,
  createProductResearcher,
  type ProcessedProduct,
  type GoalAnalysis,
  type DateRange as ProductDateRange,
} from '../lib/product-research.js';

import {
  VideoAnalyzer,
  createVideoAnalyzer,
  type ProductVideoAnalysis,
} from '../lib/video-analysis.js';

import {
  StoryboardExtractor,
  createStoryboardExtractor,
  type StoryboardResult,
  type ContentIdea,
} from '../lib/storyboard-extract.js';

// ============================================================================
// Types
// ============================================================================

export type AnalysisDepth = 'products' | 'videos' | 'full';

export interface ResearchParams {
  category: string;
  goal: string;
  dateRange?: ProductDateRange;
  depth?: AnalysisDepth;
  topProducts?: number;
}

export interface ResearchData {
  products: ProcessedProduct[];
  videos: Map<string, ProductVideoAnalysis>;
  storyboards: Map<string, StoryboardResult>;
  goalAnalysis: GoalAnalysis;
  metadata: {
    category: string;
    goal: string;
    depth: AnalysisDepth;
    dateRange: ProductDateRange;
    analyzedAt: string;
  };
}

export interface ResearchAutomationOptions extends ClientOptions {
  session: string;
  cfClearance: string;
}

// ============================================================================
// ResearchAutomation Class
// ============================================================================

export class ResearchAutomation {
  private productResearcher: ProductResearcher;
  private videoAnalyzer: VideoAnalyzer;
  private storyboardExtractor: StoryboardExtractor;
  private defaultDateRange: ProductDateRange;
  
  constructor(options: ResearchAutomationOptions) {
    // Initialize all three modules with same credentials
    this.productResearcher = createProductResearcher({
      session: options.session,
      cfClearance: options.cfClearance,
      baseUrl: options.baseUrl,
      country: options.country ?? 'ID',
      currency: options.currency ?? 'IDR',
      timeout: options.timeout,
      maxRetries: options.maxRetries,
    });
    
    this.videoAnalyzer = createVideoAnalyzer({
      session: options.session,
      cfClearance: options.cfClearance,
      baseUrl: options.baseUrl,
      country: options.country ?? 'ID',
      timeout: options.timeout,
      maxRetries: options.maxRetries,
    });
    
    this.storyboardExtractor = createStoryboardExtractor({
      session: options.session,
      cfClearance: options.cfClearance,
      baseUrl: options.baseUrl,
      country: options.country ?? 'ID',
      timeout: options.timeout,
      maxRetries: options.maxRetries,
    });
    
    // Set default date range (last 30 days)
    const end = new Date();
    const start = new Date();
    start.setDate(start.getDate() - 30);
    this.defaultDateRange = {
      start: start.toISOString().split('T')[0],
      end: end.toISOString().split('T')[0],
    };
  }
  
  /**
   * Run comprehensive research based on parameters
   */
  async runResearch(params: ResearchParams): Promise<ResearchData> {
    const {
      category,
      goal,
      dateRange = this.defaultDateRange,
      depth = 'full',
      topProducts = 5,
    } = params;
    
    // Step 1: Get category ID
    const categoryId = await this.resolveCategoryId(category);
    
    // Step 2: Run product research
    const products = await this.productResearcher.queryByGoal({
      categoryId,
      goal,
      dateRange,
      pageSize: topProducts,
    });
    
    // Sort by opportunity score and take top N
    const topProductsList = products
      .sort((a, b) => b.opportunityScore - a.opportunityScore)
      .slice(0, topProducts);
    
    const goalAnalysis = this.productResearcher.analyzeGoal(goal);
    
    const result: ResearchData = {
      products: topProductsList,
      videos: new Map(),
      storyboards: new Map(),
      goalAnalysis,
      metadata: {
        category,
        goal,
        depth,
        dateRange,
        analyzedAt: new Date().toISOString(),
      },
    };
    
    // Step 3: Video analysis (if depth is videos or full)
    if (depth === 'videos' || depth === 'full') {
      const rawProducts = topProductsList.map(p => ({
        id: p.id,
        product_title: p.title,
        revenue: p.revenue.toString(),
        revenue_trend: p.revenueTrend,
        creator_num: p.creators,
        commission_rate: p.commissionRate,
        product_rating: p.rating,
        is_overseas: p.isOverseas ? 1 : 0,
        is_full_service: p.isFullService ? 1 : 0,
        launch_date: p.launchDate,
        min_real_price: p.price.min.toString(),
        max_real_price: p.price.max.toString(),
        sale: p.sales,
        creator_conversion_ratio: p.conversionRate,
        gmv_A: p.gmvA,
        gmv_B: p.gmvB,
      } as Product));
      
      const videoResults = await this.videoAnalyzer.analyzeWithSummary(
        rawProducts,
        { dateRange, includeDownloadUrls: depth === 'full' }
      );
      
      for (const analysis of videoResults.products) {
        result.videos.set(analysis.productId, analysis);
      }
    }
    
    // Step 4: Storyboard extraction (if depth is full)
    if (depth === 'full') {
      for (const [productId, videoAnalysis] of result.videos) {
        if (videoAnalysis.topPerformer?.downloadUrl) {
          try {
            const storyboard = await this.storyboardExtractor.extractStoryboard({
              videoId: videoAnalysis.topPerformer.videoId,
              dateRange,
            });
            result.storyboards.set(productId, storyboard);
          } catch (error) {
            console.error(`Failed to extract storyboard for ${productId}:`, error);
          }
        }
      }
    }
    
    return result;
  }
  
  /**
   * Generate structured markdown report from research data
   */
  generateReport(data: ResearchData): string {
    const lines: string[] = [];
    
    // Header
    lines.push(`# Competitive Analysis Report`);
    lines.push('');
    lines.push(`**Category:** ${data.metadata.category}`);
    lines.push(`**Research Goal:** ${data.metadata.goal}`);
    lines.push(`**Date Range:** ${data.metadata.dateRange.start} to ${data.metadata.dateRange.end}`);
    lines.push(`**Analyzed:** ${new Date(data.metadata.analyzedAt).toLocaleDateString()}`);
    lines.push('');
    lines.push('---');
    lines.push('');
    
    // Executive Summary
    lines.push('## Executive Summary');
    lines.push('');
    const top3 = data.products.slice(0, 3);
    for (let i = 0; i < top3.length; i++) {
      const p = top3[i];
      lines.push(`${i + 1}. **${p.title}**`);
      lines.push(`   - Revenue: ${p.revenueFormatted}`);
      lines.push(`   - Opportunity Score: ${p.opportunityScore}/100`);
      lines.push(`   - Competition: ${p.competitionLevel}`);
      lines.push(`   - Trend: ${p.trendDirection}`);
      lines.push('');
    }
    lines.push('');
    
    // Product Analysis
    lines.push('## Product Analysis');
    lines.push('');
    for (const product of data.products) {
      lines.push(`### ${product.title}`);
      lines.push('');
      lines.push(`| Metric | Value |`);
      lines.push(`|--------|-------|`);
      lines.push(`| Price | ${product.price.formatted} |`);
      lines.push(`| Revenue | ${product.revenueFormatted} |`);
      lines.push(`| Sales | ${product.sales.toLocaleString()} |`);
      lines.push(`| Creators | ${product.creators} |`);
      lines.push(`| Conversion Rate | ${(product.conversionRate * 100).toFixed(1)}% |`);
      lines.push(`| Rating | ${product.rating} |`);
      lines.push(`| Commission | ${product.commissionRate} |`);
      lines.push(`| Competition | ${product.competitionLevel} |`);
      lines.push(`| Trend | ${product.trendDirection} |`);
      lines.push(`| Opportunity Score | ${product.opportunityScore}/100 |`);
      lines.push('');
      
      // Video section
      const videoAnalysis = data.videos.get(product.id);
      if (videoAnalysis) {
        lines.push('### Video Performance');
        lines.push('');
        lines.push(`**Total Videos:** ${videoAnalysis.totalVideos}`);
        if (videoAnalysis.topPerformer) {
          lines.push(`**Top Video ID:** ${videoAnalysis.topPerformer.videoId}`);
          lines.push(`**Content Type:** ${videoAnalysis.topPerformer.contentType}`);
          lines.push(`**Why It Works:** ${videoAnalysis.topPerformer.reason}`);
        }
        lines.push('');
      }
      
      // Storyboard section
      const storyboard = data.storyboards.get(product.id);
      if (storyboard) {
        // Key to Success
        if (storyboard.keyToSuccess.length > 0) {
          lines.push('### What Made This Video Successful');
          lines.push('');
          for (const factor of storyboard.keyToSuccess) {
            lines.push(`- ${factor}`);
          }
          lines.push('');
        }
        
        // Camera Work
        if (storyboard.cameraWork) {
          lines.push('### Camera Work Recommendations');
          lines.push('');
          lines.push(storyboard.cameraWork);
          lines.push('');
        }
        
        // Scene Breakdown
        if (storyboard.scenes.length > 0) {
          lines.push('### Scene-by-Scene Breakdown');
          lines.push('');
          lines.push('| Scene | Time | Shot | Description |');
          lines.push('|-------|------|------|-------------|');
          for (const scene of storyboard.scenes) {
            lines.push(`| ${scene.name} | ${scene.startTime}s - ${scene.endTime}s | ${scene.shotScale} | ${scene.visualDescription.substring(0, 60)}... |`);
          }
          lines.push('');
        }
        
        // Usage Scenarios
        lines.push('### Usage Scenarios to Demonstrate');
        lines.push('');
        const scenarios = this.extractUsageScenarios(storyboard);
        for (const scenario of scenarios) {
          lines.push(`- ${scenario}`);
        }
        lines.push('');
        
        // Content Ideas
        if (storyboard.contentIdeas.length > 0) {
          lines.push('### Auto-Generated Content Ideas');
          lines.push('');
          for (const idea of storyboard.contentIdeas) {
            lines.push(`#### ${idea.title}`);
            lines.push(`**Angle:** ${idea.angle}`);
            lines.push(`**Hook:** ${idea.hook}`);
            lines.push(`**Description:** ${idea.description}`);
            lines.push('');
          }
        }
      }
      
      lines.push('---');
      lines.push('');
    }
    
    // Recommendations
    lines.push('## Recommendations');
    lines.push('');
    const recommendations = this.generateRecommendations(data);
    for (const rec of recommendations) {
      lines.push(`- ${rec}`);
    }
    lines.push('');
    
    return lines.join('\n');
  }
  
  /**
   * Update credentials for all modules
   */
  updateCredentials(session: string, cfClearance: string): void {
    this.productResearcher.updateCredentials(session, cfClearance);
    this.videoAnalyzer.updateCredentials(session, cfClearance);
    this.storyboardExtractor.updateCredentials(session, cfClearance);
  }
  
  /**
   * Resolve category name to ID
   */
  private async resolveCategoryId(category: string): Promise<string> {
    const categories = await this.productResearcher.getCategories();
    const found = categories.find(
      c => c.name.toLowerCase() === category.toLowerCase() || c.id === category
    );
    if (found) {
      return found.id;
    }
    // Default to Beauty if not found
    return '600137235';
  }
  
  /**
   * Extract usage scenarios from storyboard
   */
  private extractUsageScenarios(storyboard: StoryboardResult): string[] {
    const scenarios: string[] = [];
    
    // Extract from scenes
    for (const scene of storyboard.scenes) {
      if (scene.visualDescription && scenarios.length < 5) {
        const desc = scene.visualDescription.toLowerCase();
        if (desc.includes('use') || desc.includes('apply') || desc.includes('try')) {
          scenarios.push(scene.visualDescription.substring(0, 100));
        }
      }
    }
    
    // Add defaults if not enough
    if (scenarios.length < 3) {
      scenarios.push('Show product in everyday use');
      scenarios.push('Demonstrate key features');
      scenarios.push('Show before/after (if applicable)');
    }
    
    return scenarios.slice(0, 5);
  }
  
  /**
   * Generate strategic recommendations
   */
  private generateRecommendations(data: ResearchData): string[] {
    const recs: string[] = [];
    
    // Analyze top products
    const topProduct = data.products[0];
    if (topProduct) {
      recs.push(`Focus on "${topProduct.title}" - highest opportunity score (${topProduct.opportunityScore}/100)`);
    }
    
    // Competition analysis
    const lowComp = data.products.filter(p => p.competitionLevel === 'low');
    if (lowComp.length > 0) {
      recs.push(`${lowComp.length} products have low competition - good for new creators`);
    }
    
    // Trend analysis
    const rising = data.products.filter(p => p.trendDirection === 'rising');
    if (rising.length > 0) {
      recs.push(`${rising.length} products showing rising trends - capture early`);
    }
    
    // Video insights
    const productsWithVideos = data.videos.size;
    if (productsWithVideos > 0) {
      recs.push(`${productsWithVideos} products have viral videos to analyze`);
    }
    
    // Storyboard insights
    if (data.storyboards.size > 0) {
      const storyboard = Array.from(data.storyboards.values())[0];
      if (storyboard?.keyToSuccess.length > 0) {
        recs.push(`Top success factor: ${storyboard.keyToSuccess[0]}`);
      }
    }
    
    return recs;
  }
}

// ============================================================================
// Factory Function
// ============================================================================

export function createResearchAutomation(
  options: ResearchAutomationOptions
): ResearchAutomation {
  return new ResearchAutomation(options);
}

// ============================================================================
// Utility Functions
// ============================================================================

export { createProductResearcher } from '../lib/product-research.js';
export { createVideoAnalyzer } from '../lib/video-analysis.js';
export { createStoryboardExtractor } from '../lib/storyboard-extract.js';

export type {
  ProcessedProduct,
  GoalAnalysis,
  ProductVideoAnalysis,
  StoryboardResult,
  ContentIdea,
  DateRange as ProductDateRange,
} from '../lib/index.js';

export default ResearchAutomation;
