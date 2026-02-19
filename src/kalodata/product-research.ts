/**
 * Kalodata Product Research Module
 * 
 * Provides intelligent product research capabilities with AI-powered
 * filter detection based on research goals.
 * 
 * Features:
 * - Category-based product queries
 * - Flexible filtering (price, revenue, creators, etc.)
 * - Multiple sort options
 * - AI Filter Intelligence for research goal detection
 * - Pagination support
 * - Structured insights generation
 */

import {
  KalodataClient,
  createClient,
  type ClientOptions,
  type Product,
  type ProductQueryRequest,
  type ProductQueryResponse,
} from '../kalodata/index.js';

// ============================================================================
// Types
// ============================================================================

export interface DateRange {
  start: string;
  end: string;
}

export interface ProductFilters {
  priceMin?: number;
  priceMax?: number;
  revenueMin?: number;
  revenueMax?: number;
  creatorMin?: number;
  creatorMax?: number;
  salesChannel?: 'online' | 'offline' | 'all';
  strategy?: 'affiliate' | 'self-operated' | 'all';
  affiliateType?: string;
}

export interface SortOption {
  field: string;
  type: 'ASC' | 'DESC';
}

export interface QueryParams {
  categoryId: string;
  dateRange: DateRange;
  filters?: ProductFilters;
  sort?: SortOption[];
  pageSize?: number;
  pageNo?: number;
}

export interface GoalQueryParams {
  goal: string;
  categoryId: string;
  dateRange: DateRange;
  filters?: Partial<ProductFilters>;
  pageSize?: number;
}

export interface PriceInfo {
  min: number;
  max: number;
  formatted: string;
}

export interface ProcessedProduct {
  id: string;
  title: string;
  price: PriceInfo;
  revenue: number;
  revenueFormatted: string;
  revenueTrend: number[];
  trendDirection: 'rising' | 'stable' | 'declining';
  sales: number;
  creators: number;
  conversionRate: number;
  launchDate: string;
  rating: number;
  isOverseas: boolean;
  isFullService: boolean;
  commissionRate: string;
  gmvA: number;
  gmvB: number;
  competitionLevel: 'low' | 'medium' | 'high';
  opportunityScore: number;
}

export interface Category {
  id: string;
  name: string;
  parentId?: string;
}

export interface ResearchResult {
  products: ProcessedProduct[];
  pagination: {
    pageNo: number;
    pageSize: number;
    hasMore: boolean;
  };
  metadata: {
    queryTime: string;
    dateRange: DateRange;
    categoryId: string;
    sortApplied: SortOption[];
    filtersApplied: ProductFilters;
  };
}

export interface GoalAnalysis {
  goal: string;
  detectedIntent: string;
  filtersApplied: Partial<ProductFilters>;
  sortApplied: SortOption[];
  reasoning: string;
}

// ============================================================================
// Research Goal Intelligence
// ============================================================================

const RESEARCH_GOAL_PATTERNS: Record<string, GoalAnalysis> = {
  'emerging': {
    goal: 'find emerging products',
    detectedIntent: 'Discover new products with rising trends',
    filtersApplied: {
      creatorMin: 10,
      creatorMax: 100,
    },
    sortApplied: [
      { field: 'revenue_trend', type: 'ASC' },
      { field: 'launch_date', type: 'DESC' },
    ],
    reasoning: 'Sorting by revenue_trend ASC finds products with growing revenue. Recent launch dates and moderate creator count indicate emerging products.',
  },
  'new products': {
    goal: 'find emerging products',
    detectedIntent: 'Discover newly launched products',
    filtersApplied: {
      creatorMin: 10,
      creatorMax: 100,
    },
    sortApplied: [
      { field: 'launch_date', type: 'DESC' },
      { field: 'revenue_trend', type: 'ASC' },
    ],
    reasoning: 'Sorting by launch_date DESC finds newest products first.',
  },
  'rising stars': {
    goal: 'find emerging products',
    detectedIntent: 'Find products with upward momentum',
    filtersApplied: {
      creatorMin: 10,
      creatorMax: 100,
    },
    sortApplied: [
      { field: 'revenue_trend', type: 'ASC' },
      { field: 'gmv_B', type: 'DESC' },
    ],
    reasoning: 'Revenue trend ascending shows growth; gmv_B shows recent volume.',
  },
  'stable winners': {
    goal: 'find stable winners',
    detectedIntent: 'Identify proven best-selling products',
    filtersApplied: {
      creatorMin: 100,
    },
    sortApplied: [
      { field: 'revenue', type: 'DESC' },
      { field: 'creator_num', type: 'DESC' },
    ],
    reasoning: 'High revenue and high creator count indicate established products with proven market fit.',
  },
  'best sellers': {
    goal: 'find stable winners',
    detectedIntent: 'Find top-performing products',
    filtersApplied: {
      creatorMin: 100,
    },
    sortApplied: [
      { field: 'revenue', type: 'DESC' },
      { field: 'sale', type: 'DESC' },
    ],
    reasoning: 'Sorting by revenue and sales volume identifies market leaders.',
  },
  'proven products': {
    goal: 'find stable winners',
    detectedIntent: 'Find products with track record',
    filtersApplied: {
      creatorMin: 100,
    },
    sortApplied: [
      { field: 'revenue', type: 'DESC' },
      { field: 'creator_num', type: 'DESC' },
    ],
    reasoning: 'Proven products have wide creator adoption and consistent revenue.',
  },
  'market leaders': {
    goal: 'find stable winners',
    detectedIntent: 'Find category leaders',
    filtersApplied: {
      creatorMin: 200,
    },
    sortApplied: [
      { field: 'revenue', type: 'DESC' },
    ],
    reasoning: 'Market leaders dominate their category with high revenue and creator count.',
  },
  'quick wins': {
    goal: 'find quick wins',
    detectedIntent: 'Find fast-growing products',
    filtersApplied: {},
    sortApplied: [
      { field: 'gmv_B', type: 'ASC' },
      { field: 'revenue_trend', type: 'ASC' },
    ],
    reasoning: 'gmv_B ascending shows products with fastest recent growth rate.',
  },
  'fast growers': {
    goal: 'find quick wins',
    detectedIntent: 'Identify rapidly growing products',
    filtersApplied: {},
    sortApplied: [
      { field: 'gmv_B', type: 'ASC' },
      { field: 'creator_num', type: 'DESC' },
    ],
    reasoning: 'Sorting by gmv_B growth rate identifies products gaining traction quickly.',
  },
  'trending now': {
    goal: 'find quick wins',
    detectedIntent: 'Find currently trending products',
    filtersApplied: {
      creatorMin: 50,
    },
    sortApplied: [
      { field: 'gmv_B', type: 'ASC' },
      { field: 'revenue_trend', type: 'DESC' },
    ],
    reasoning: 'Trending products show high recent growth (gmv_B) and upward trend.',
  },
  'viral products': {
    goal: 'find quick wins',
    detectedIntent: 'Find products with viral potential',
    filtersApplied: {
      creatorMin: 20,
      creatorMax: 200,
    },
    sortApplied: [
      { field: 'gmv_B', type: 'ASC' },
      { field: 'creator_conversion_ratio', type: 'DESC' },
    ],
    reasoning: 'Viral products have high growth and good conversion rates.',
  },
  'low competition': {
    goal: 'find low competition',
    detectedIntent: 'Find underserved product niches',
    filtersApplied: {
      creatorMin: 1,
      creatorMax: 10,
    },
    sortApplied: [
      { field: 'revenue', type: 'DESC' },
    ],
    reasoning: 'Low creator count indicates less competition - easier to capture market share.',
  },
  'niche products': {
    goal: 'find low competition',
    detectedIntent: 'Find specialized products',
    filtersApplied: {
      creatorMin: 1,
      creatorMax: 10,
    },
    sortApplied: [
      { field: 'revenue', type: 'DESC' },
      { field: 'revenue_trend', type: 'ASC' },
    ],
    reasoning: 'Niche products have few creators but steady revenue.',
  },
  'underserved markets': {
    goal: 'find low competition',
    detectedIntent: 'Find opportunities with less competition',
    filtersApplied: {
      creatorMin: 1,
      creatorMax: 10,
    },
    sortApplied: [
      { field: 'revenue', type: 'DESC' },
      { field: 'gmv_B', type: 'ASC' },
    ],
    reasoning: 'Underserved markets have low creator count with positive growth.',
  },
  'easy to rank': {
    goal: 'find low competition',
    detectedIntent: 'Find products easy to promote',
    filtersApplied: {
      creatorMin: 1,
      creatorMax: 10,
    },
    sortApplied: [
      { field: 'revenue', type: 'DESC' },
      { field: 'commission_rate', type: 'DESC' },
    ],
    reasoning: 'Low competition with high commission = easier to rank as affiliate.',
  },
  'high margin': {
    goal: 'find high margin',
    detectedIntent: 'Find products with best commission rates',
    filtersApplied: {},
    sortApplied: [
      { field: 'commission_rate', type: 'DESC' },
      { field: 'revenue', type: 'DESC' },
    ],
    reasoning: 'Sorting by commission_rate finds highest-earning affiliate products.',
  },
  'trending': {
    goal: 'find trending',
    detectedIntent: 'Find currently popular products',
    filtersApplied: {
      creatorMin: 50,
    },
    sortApplied: [
      { field: 'revenue_trend', type: 'DESC' },
      { field: 'gmv_B', type: 'DESC' },
    ],
    reasoning: 'Trending products have positive revenue trend and high recent volume.',
  },
};

// ============================================================================
// Helper Functions
// ============================================================================

function detectResearchGoal(goal: string): GoalAnalysis {
  const normalizedGoal = goal.toLowerCase();
  
  // Try exact match first
  for (const [pattern, analysis] of Object.entries(RESEARCH_GOAL_PATTERNS)) {
    if (normalizedGoal.includes(pattern)) {
      return analysis;
    }
  }
  
  // Default to stable winners if no match
  return RESEARCH_GOAL_PATTERNS['stable winners'];
}

function parsePriceRange(priceStr: string): { min: number; max: number } | null {
  const match = priceStr.match(/^(\d+)-(\d+)$/);
  if (match) {
    return {
      min: parseInt(match[1], 10),
      max: parseInt(match[2], 10),
    };
  }
  return null;
}

function formatCurrency(amount: number, currency = 'IDR'): string {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}

function calculateTrendDirection(trend: number[]): 'rising' | 'stable' | 'declining' {
  if (!trend || trend.length < 2) return 'stable';
  
  const recent = trend.slice(-7);
  const older = trend.slice(0, Math.min(7, trend.length - 7));
  
  if (recent.length === 0 || older.length === 0) return 'stable';
  
  const recentAvg = recent.reduce((a, b) => a + b, 0) / recent.length;
  const olderAvg = older.reduce((a, b) => a + b, 0) / older.length;
  
  const change = (recentAvg - olderAvg) / (olderAvg || 1);
  
  if (change > 0.1) return 'rising';
  if (change < -0.1) return 'declining';
  return 'stable';
}

function calculateCompetitionLevel(creatorNum: number): 'low' | 'medium' | 'high' {
  if (creatorNum <= 10) return 'low';
  if (creatorNum <= 100) return 'medium';
  return 'high';
}

function calculateOpportunityScore(product: ProcessedProduct): number {
  let score = 50;
  
  // Lower competition = higher opportunity
  if (product.competitionLevel === 'low') score += 30;
  else if (product.competitionLevel === 'medium') score += 15;
  
  // Rising trend = higher opportunity
  if (product.trendDirection === 'rising') score += 20;
  else if (product.trendDirection === 'stable') score += 10;
  
  // Good commission rate = higher opportunity
  const commissionRate = parseFloat(product.commissionRate) || 0;
  if (commissionRate > 20) score += 10;
  else if (commissionRate > 10) score += 5;
  
  // Reasonable price point
  if (product.price.min >= 50000 && product.price.max <= 500000) score += 5;
  
  return Math.min(100, score);
}

function processProduct(product: Product, currency = 'IDR'): ProcessedProduct {
  const trendDirection = calculateTrendDirection(product.revenue_trend);
  const competitionLevel = calculateCompetitionLevel(product.creator_num);
  
  const processed: ProcessedProduct = {
    id: product.id,
    title: product.product_title,
    price: {
      min: parseFloat(product.min_real_price) || 0,
      max: parseFloat(product.max_real_price) || 0,
      formatted: `${formatCurrency(parseFloat(product.min_real_price) || 0, currency)} - ${formatCurrency(parseFloat(product.max_real_price) || 0, currency)}`,
    },
    revenue: parseFloat(product.revenue) || 0,
    revenueFormatted: formatCurrency(parseFloat(product.revenue) || 0, currency),
    revenueTrend: product.revenue_trend || [],
    trendDirection,
    sales: product.sale || 0,
    creators: product.creator_num || 0,
    conversionRate: product.creator_conversion_ratio || 0,
    launchDate: product.launch_date,
    rating: product.product_rating || 0,
    isOverseas: product.is_overseas === 1,
    isFullService: product.is_full_service === 1,
    commissionRate: product.commission_rate || '0',
    gmvA: product.gmv_A || 0,
    gmvB: product.gmv_B || 0,
    competitionLevel,
    opportunityScore: 0, // Will be calculated after
  };
  
  processed.opportunityScore = calculateOpportunityScore(processed);
  
  return processed;
}

function buildQueryRequest(
  categoryId: string,
  dateRange: DateRange,
  options: {
    filters?: ProductFilters;
    sort?: SortOption[];
    pageSize?: number;
    pageNo?: number;
  } = {}
): ProductQueryRequest {
  const {
    filters = {},
    sort = [],
    pageSize = 20,
    pageNo = 1,
  } = options;
  
  const request: ProductQueryRequest = {
    country: 'ID',
    startDate: dateRange.start,
    endDate: dateRange.end,
    cateIds: [categoryId],
    showCateIds: [categoryId],
    pageNo,
    pageSize,
    sort: sort.length > 0 ? sort : [{ field: 'revenue', type: 'DESC' }],
  };
  
  // Apply filters
  if (filters.priceMin !== undefined || filters.priceMax !== undefined) {
    const min = filters.priceMin ?? 0;
    const max = filters.priceMax ?? Number.MAX_SAFE_INTEGER;
    request['product.filter.unit_price'] = `${min}-${max}`;
  }
  
  if (filters.salesChannel) {
    request['product.filter.sales_channel'] = [filters.salesChannel];
  }
  
  if (filters.strategy) {
    request['product.filter.strategy'] = filters.strategy;
  }
  
  if (filters.affiliateType) {
    request['product.filter.affiliate_type'] = filters.affiliateType;
  }
  
  if (filters.creatorMin !== undefined || filters.creatorMax !== undefined) {
    const min = filters.creatorMin ?? 1;
    const max = filters.creatorMax ?? Number.MAX_SAFE_INTEGER;
    request['product.filter.creator'] = `${min}-${max}`;
  }
  
  return request;
}

// ============================================================================
// ProductResearcher Class
// ============================================================================

export class ProductResearcher {
  private client: KalodataClient;
  private currency: string;
  
  constructor(options: ClientOptions = {}) {
    this.client = createClient(options);
    this.currency = options.currency ?? 'IDR';
  }
  
  /**
   * Query products by category with filters
   */
  async queryByCategory(params: QueryParams): Promise<ProcessedProduct[]> {
    const request = buildQueryRequest(
      params.categoryId,
      params.dateRange,
      {
        filters: params.filters,
        sort: params.sort,
        pageSize: params.pageSize,
        pageNo: params.pageNo,
      }
    );
    
    const response = await this.client.queryProducts(request);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to query products');
    }
    
    return response.data.map(product => processProduct(product, this.currency));
  }
  
  /**
   * Query products using AI-powered goal detection
   */
  async queryByGoal(params: GoalQueryParams): Promise<ProcessedProduct[]> {
    const goalAnalysis = detectResearchGoal(params.goal);
    
    // Merge user filters with goal-based filters
    const mergedFilters: ProductFilters = {
      ...goalAnalysis.filtersApplied,
      ...params.filters,
    };
    
    const request = buildQueryRequest(
      params.categoryId,
      params.dateRange,
      {
        filters: mergedFilters,
        sort: goalAnalysis.sortApplied,
        pageSize: params.pageSize,
        pageNo: 1,
      }
    );
    
    const response = await this.client.queryProducts(request);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to query products');
    }
    
    return response.data.map(product => processProduct(product, this.currency));
  }
  
  /**
   * Query with full result metadata
   */
  async queryWithMetadata(params: QueryParams): Promise<ResearchResult> {
    const products = await this.queryByCategory(params);
    
    return {
      products,
      pagination: {
        pageNo: params.pageNo ?? 1,
        pageSize: params.pageSize ?? 20,
        hasMore: products.length === (params.pageSize ?? 20),
      },
      metadata: {
        queryTime: new Date().toISOString(),
        dateRange: params.dateRange,
        categoryId: params.categoryId,
        sortApplied: params.sort ?? [{ field: 'revenue', type: 'DESC' }],
        filtersApplied: params.filters ?? {},
      },
    };
  }
  
  /**
   * Query by goal with metadata
   */
  async queryByGoalWithMetadata(params: GoalQueryParams): Promise<{
    products: ProcessedProduct[];
    goalAnalysis: GoalAnalysis;
  }> {
    const goalAnalysis = detectResearchGoal(params.goal);
    const products = await this.queryByGoal(params);
    
    return {
      products,
      goalAnalysis,
    };
  }
  
  /**
   * Paginate through results
   */
  async *paginate(
    params: Omit<QueryParams, 'pageNo'>,
    maxPages = 5
  ): AsyncGenerator<ProcessedProduct[]> {
    let pageNo = 1;
    let hasMore = true;
    
    while (hasMore && pageNo <= maxPages) {
      const products = await this.queryByCategory({
        ...params,
        pageNo,
      });
      
      if (products.length === 0) {
        break;
      }
      
      yield products;
      
      hasMore = products.length === (params.pageSize ?? 20);
      pageNo++;
    }
  }
  
  /**
   * Get total count of products matching filters
   */
  async getTotalCount(params: Omit<QueryParams, 'pageSize' | 'pageNo'>): Promise<number> {
    const request = buildQueryRequest(
      params.categoryId,
      params.dateRange,
      {
        filters: params.filters,
        sort: params.sort,
        pageSize: 1,
        pageNo: 1,
      }
    );
    
    const response = await this.client.getProductCount({
      country: request.country,
      startDate: request.startDate,
      endDate: request.endDate,
      cateIds: request.cateIds,
      showCateIds: request.showCateIds,
      pageNo: 1,
      pageSize: 1,
      sort: request.sort,
    });
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to get product count');
    }
    
    return response.data;
  }
  
  /**
   * Analyze research goal and return filter recommendations
   */
  analyzeGoal(goal: string): GoalAnalysis {
    return detectResearchGoal(goal);
  }
  
  /**
   * Get available categories
   */
  async getCategories(): Promise<Category[]> {
    // Common TikTok Shop Indonesia categories
    return [
      { id: '600138989', name: 'Fashion' },
      { id: '600136323', name: 'Electronics' },
      { id: '600137235', name: 'Beauty' },
      { id: '600138081', name: 'Home & Living' },
      { id: '600138171', name: 'Food & Beverage' },
      { id: '600138251', name: 'Mother & Baby' },
      { id: '600138431', name: 'Sports' },
      { id: '600138621', name: 'Toys & Games' },
      { id: '600138761', name: 'Books' },
      { id: '600138841', name: 'Automotive' },
      { id: '600139021', name: 'Health' },
      { id: '600139121', name: 'Pet Supplies' },
    ];
  }
  
  /**
   * Update client credentials
   */
  updateCredentials(session: string, cfClearance: string): void {
    this.client.updateCredentials(session, cfClearance);
  }
}

// ============================================================================
// Factory Function
// ============================================================================

export function createProductResearcher(options?: ClientOptions): ProductResearcher {
  return new ProductResearcher(options);
}

// ============================================================================
// Utility Functions
// ============================================================================

export { detectResearchGoal, formatCurrency, calculateTrendDirection };

export default ProductResearcher;
