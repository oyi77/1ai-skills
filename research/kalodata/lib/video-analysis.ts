/**
 * Kalodata Video Analysis Module
 * 
 * Provides video intelligence capabilities for products including:
 * - Getting videos associated with products
 * - Extracting downloadable video URLs
 * - Identifying top-performing videos for competitive analysis
 * - Structured video metadata for business users
 * 
 * Features:
 * - Batch video retrieval for multiple products
 * - Download URL extraction (not full video download)
 * - Top-performing video identification
 * - Competitive analysis insights
 */

import {
  KalodataClient,
  createClient,
  type ClientOptions,
  type Product,
  type ProductVideo,
} from '../kalodata/index.js';

// ============================================================================
// Types
// ============================================================================

export interface VideoInfo {
  id: string;
  contentType: 'video' | 'autocut' | string;
  downloadUrl?: string;
  urlExpiry?: string;
}

export interface ProductVideos {
  productId: string;
  videos: VideoInfo[];
  videoCount: number;
}

export interface TopPerformingVideo {
  videoId: string;
  contentType: string;
  downloadUrl?: string;
  reason: string;
}

export interface ProductVideoAnalysis {
  productId: string;
  productTitle: string;
  videos: VideoInfo[];
  topPerformer: TopPerformingVideo | null;
  totalVideos: number;
  hasAutocut: boolean;
}

export interface VideoAnalysisResult {
  products: ProductVideoAnalysis[];
  summary: {
    totalProducts: number;
    totalVideos: number;
    productsWithVideos: number;
    productsWithoutVideos: number;
  };
  metadata: {
    queryTime: string;
    dateRange: {
      start: string;
      end: string;
    };
  };
}

// ============================================================================
// VideoAnalysis Class
// ============================================================================

export class VideoAnalyzer {
  private client: KalodataClient;
  private defaultDateRange: { start: string; end: string };
  private defaultCountry: string;
  
  constructor(options: ClientOptions = {}) {
    this.client = createClient(options);
    this.defaultCountry = options.country ?? 'ID';
    
    const end = new Date();
    const start = new Date();
    start.setDate(start.getDate() - 30);
    
    this.defaultDateRange = {
      start: start.toISOString().split('T')[0],
      end: end.toISOString().split('T')[0],
    };
  }
  
  async getVideosForProducts(
    productIds: string[],
    dateRange?: { start: string; end: string }
  ): Promise<ProductVideos[]> {
    if (productIds.length === 0) {
      return [];
    }
    
    const response = await this.client.enrichProducts({
      ids: productIds,
      country: this.defaultCountry,
      startDate: dateRange?.start ?? this.defaultDateRange.start,
      endDate: dateRange?.end ?? this.defaultDateRange.end,
      cateIds: [],
    });
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to get product videos');
    }
    
    return response.data.map((productVideo: ProductVideo) => ({
      productId: productVideo.id,
      videos: productVideo.videos.map(v => ({
        id: v.id,
        contentType: v.contentType,
      })),
      videoCount: productVideo.videos.length,
    }));
  }
  
  async getVideoUrl(videoId: string): Promise<string | null> {
    try {
      const response = await this.client.getVideoUrl({ videoId });
      
      if (!response.success || !response.data?.url) {
        return null;
      }
      
      return response.data.url;
    } catch (error) {
      console.error(`Failed to get URL for video ${videoId}:`, error);
      return null;
    }
  }
  
  async getVideoUrls(videoIds: string[]): Promise<Map<string, string | null>> {
    const results = new Map<string, string | null>();
    
    const batchSize = 10;
    
    for (let i = 0; i < videoIds.length; i += batchSize) {
      const batch = videoIds.slice(i, i + batchSize);
      const promises = batch.map(async (videoId) => {
        const url = await this.getVideoUrl(videoId);
        return { videoId, url };
      });
      
      const batchResults = await Promise.all(promises);
      for (const { videoId, url } of batchResults) {
        results.set(videoId, url);
      }
      
      if (i + batchSize < videoIds.length) {
        await new Promise(resolve => setTimeout(resolve, 100));
      }
    }
    
    return results;
  }
  
  async analyzeVideos(
    products: Product[],
    options: {
      dateRange?: { start: string; end: string };
      includeDownloadUrls?: boolean;
      maxVideosPerProduct?: number;
    } = {}
  ): Promise<ProductVideoAnalysis[]> {
    const { 
      dateRange, 
      includeDownloadUrls = false,
      maxVideosPerProduct = 10,
    } = options;
    
    if (products.length === 0) {
      return [];
    }
    
    const productIds = products.map(p => p.id);
    
    const productVideos = await this.getVideosForProducts(productIds, dateRange);
    
    const productVideoMap = new Map<string, VideoInfo[]>();
    const allVideoIds: string[] = [];
    
    for (const pv of productVideos) {
      const videos = pv.videos.slice(0, maxVideosPerProduct);
      productVideoMap.set(pv.productId, videos);
      for (const v of videos) {
        allVideoIds.push(v.id);
      }
    }
    
    let videoUrlMap: Map<string, string | null> | undefined;
    if (includeDownloadUrls && allVideoIds.length > 0) {
      videoUrlMap = await this.getVideoUrls(allVideoIds);
    }
    
    const results: ProductVideoAnalysis[] = [];
    
    for (const product of products) {
      const videos = productVideoMap.get(product.id) || [];
      
      const videosWithUrls: VideoInfo[] = videos.map(video => ({
        ...video,
        downloadUrl: videoUrlMap?.get(video.id) || undefined,
        urlExpiry: videoUrlMap?.get(video.id) ? 'URLs expire - use immediately' : undefined,
      }));
      
      const topPerformer = this.identifyTopPerformer(videosWithUrls);
      
      results.push({
        productId: product.id,
        productTitle: product.product_title,
        videos: videosWithUrls,
        topPerformer,
        totalVideos: videosWithUrls.length,
        hasAutocut: videos.some(v => v.contentType === 'autocut'),
      });
    }
    
    return results;
  }
  
  async analyzeWithSummary(
    products: Product[],
    options?: {
      dateRange?: { start: string; end: string };
      includeDownloadUrls?: boolean;
    }
  ): Promise<VideoAnalysisResult> {
    const analyses = await this.analyzeVideos(products, options);
    
    const productsWithVideos = analyses.filter(a => a.totalVideos > 0).length;
    const productsWithoutVideos = analyses.length - productsWithVideos;
    const totalVideos = analyses.reduce((sum, a) => sum + a.totalVideos, 0);
    
    return {
      products: analyses,
      summary: {
        totalProducts: analyses.length,
        totalVideos,
        productsWithVideos,
        productsWithoutVideos,
      },
      metadata: {
        queryTime: new Date().toISOString(),
        dateRange: options?.dateRange ?? this.defaultDateRange,
      },
    };
  }
  
  private identifyTopPerformer(videos: VideoInfo[]): TopPerformingVideo | null {
    if (videos.length === 0) {
      return null;
    }
    
    const originalVideo = videos.find(v => v.contentType === 'video');
    
    if (originalVideo) {
      return {
        videoId: originalVideo.id,
        contentType: originalVideo.contentType,
        downloadUrl: originalVideo.downloadUrl,
        reason: 'Original video content - typically has higher engagement than autocut',
      };
    }
    
    const firstVideo = videos[0];
    return {
      videoId: firstVideo.id,
      contentType: firstVideo.contentType,
      downloadUrl: firstVideo.downloadUrl,
      reason: 'First video in list - most prominent or recently added',
    };
  }
  
  async getProductVideos(
    productId: string,
    options: {
      dateRange?: { start: string; end: string };
      includeDownloadUrls?: boolean;
    } = {}
  ): Promise<ProductVideoAnalysis | null> {
    const productVideos = await this.getVideosForProducts([productId], options.dateRange);
    
    if (productVideos.length === 0) {
      return null;
    }
    
    const pv = productVideos[0];
    
    let videos = pv.videos;
    
    if (options.includeDownloadUrls && videos.length > 0) {
      const videoIds = videos.map(v => v.id);
      const urlMap = await this.getVideoUrls(videoIds);
      
      videos = videos.map(video => ({
        ...video,
        downloadUrl: urlMap.get(video.id) || undefined,
      }));
    }
    
    const topPerformer = this.identifyTopPerformer(videos);
    
    return {
      productId: pv.productId,
      productTitle: 'Product ID: ' + pv.productId,
      videos,
      topPerformer,
      totalVideos: videos.length,
      hasAutocut: videos.some(v => v.contentType === 'autocut'),
    };
  }
  
  updateCredentials(session: string, cfClearance: string): void {
    this.client.updateCredentials(session, cfClearance);
  }
}

export function createVideoAnalyzer(options?: ClientOptions): VideoAnalyzer {
  return new VideoAnalyzer(options);
}

export default VideoAnalyzer;
