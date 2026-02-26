/**
 * Kalodata API TypeScript Types
 * Based on research draft at research/kalodata/kalodata-research.md
 */

// ============================================================================
// Shared Types
// ============================================================================

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message: string | null;
  cached: boolean | null;
  code: string | null;
}

export interface KalodataConfig {
  /** Base URL for Kalodata API */
  baseUrl: string;
  /** Raw cookies string - will be parsed to extract SESSION and cf_clearance */
  cookies?: string;
  /** SESSION cookie value (auto-extracted from cookies if not provided) */
  session?: string;
  /** Cloudflare clearance token (auto-extracted from cookies if not provided) */
  cfClearance?: string;
  /** Country code (default: ID) */
  country?: string;
  /** Currency code (default: IDR) */
  currency?: string;
  /** Language code (default: id-ID) */
  language?: string;
  /** Request timeout in ms (default: 30000) */
  timeout?: number;
  /** Max retries for failed requests (default: 3) */
  maxRetries?: number;
  /** Base delay for exponential backoff in ms (default: 1000) */
  retryDelay?: number;
}

// ============================================================================
// Product API Types
// ============================================================================

export interface ProductQueryRequest {
  country: string;
  startDate: string;
  endDate: string;
  cateIds: string[];
  showCateIds: string[];
  pageNo: number;
  pageSize: number;
  sort: Array<{ field: string; type: 'ASC' | 'DESC' }>;
  'product.filter.sales_channel'?: string[];
  'product.filter.strategy'?: string;
  'product.filter.unit_price'?: string;
  'product.filter.affiliate_type'?: string;
  'product.filter.creator'?: string;
}

export interface Product {
  sec_cate_id: number;
  is_full_service: number;
  ter_cate_id: number;
  is_overseas: number;
  gmv_A: number;
  creator_conversion_ratio: number;
  unit_price: string;
  gmv_B: number;
  product_title: string;
  is_tokopedia: number;
  revenue: string;
  sale: number;
  creator_num: number;
  revenue_trend: number[];
  min_real_price: string;
  delivery_type: string;
  revenue_grouping_rate: string;
  pri_cate_id: number;
  max_real_price: string;
  commission_rate: string;
  id: string;
  launch_date: string;
  product_rating: number;
}

export type ProductQueryResponse = ApiResponse<Product[]>;

export interface ProductEnrichRequest {
  ids: string[];
  country: string;
  startDate: string;
  endDate: string;
  cateIds: string[];
}

export interface ProductVideo {
  id: string;
  videos: Array<{
    id: string;
    contentType: string;
  }>;
}

export type ProductEnrichResponse = ApiResponse<ProductVideo[]>;

export interface ProductCountRequest {
  country: string;
  startDate: string;
  endDate: string;
  cateIds: string[];
  showCateIds: string[];
  pageNo: number;
  pageSize: number;
  sort: Array<{ field: string; type: 'ASC' | 'DESC' }>;
  'product.filter.sales_channel'?: string[];
  'product.filter.strategy'?: string;
  'product.filter.unit_price'?: string;
  'product.filter.affiliate_type'?: string;
  'product.filter.creator'?: string;
}

export type ProductCountResponse = ApiResponse<number>;

// ============================================================================
// Video API Types
// ============================================================================

export interface VideoUrlRequest {
  videoId: string;
}

export interface VideoUrlResponse {
  url: string;
}

export type GetVideoUrlResponse = ApiResponse<VideoUrlResponse>;

// ============================================================================
// AI Task API Types
// ============================================================================

export interface CheckAiUseRequest {
  id: string;
  type: 'videoScript' | string;
}

export interface ProgressInfo {
  total: number;
  used: number;
  remain: number;
  full: boolean;
}

export interface CheckAiUseData {
  used: boolean;
  progressInfo: ProgressInfo;
}

export type CheckAiUseResponse = ApiResponse<CheckAiUseData>;

export interface StartAiTaskRequest {
  id: string;
  type: 'video_script';
  partitionDayStart: string;
  partitionDayEnd: string;
  uuid: string;
}

export interface StartAiTaskData {
  code: 1 | 2; // 1 = processing, 2 = completed
}

export type StartAiTaskResponse = ApiResponse<StartAiTaskData>;

export interface GetVideoScriptRequest {
  id: string;
  partitionDayStart: string;
  partitionDayEnd: string;
  translate: boolean;
}

export interface VideoScript {
  scene: string;
  translate_scene: string | null;
  start_time: number;
  end_time: number;
  shot_scale: string;
  translate_shot_scale: string | null;
  visual_description: string;
  translate_visual_description: string | null;
  audio_script: string[];
}

export interface GetVideoScriptData {
  gender: string;
  translate_gender: string | null;
  language: string;
  language_code: string;
  translate_language: string | null;
  camera_work: string;
  translate_camera_work: string | null;
  key_to_success: string;
  key_to_success_list: string[];
  translate_key_to_success: string | null;
  translate_key_to_success_list: string[] | null;
  video_scripts: VideoScript[];
}

export type GetVideoScriptResponse = ApiResponse<GetVideoScriptData>;

// ============================================================================
// Client Options
// ============================================================================

export interface ClientOptions extends Partial<KalodataConfig> {
  /** Override default headers */
  headers?: Record<string, string>;
}

// ============================================================================
// Error Types
// ============================================================================

export class KalodataError extends Error {
  constructor(
    message: string,
    public code?: string,
    public statusCode?: number
  ) {
    super(message);
    this.name = 'KalodataError';
  }
}

export class AuthenticationError extends KalodataError {
  constructor(message = 'Authentication failed') {
    super(message, 'AUTH_ERROR', 401);
    this.name = 'AuthenticationError';
  }
}

export class RateLimitError extends KalodataError {
  constructor(message = 'Rate limit exceeded') {
    super(message, 'RATE_LIMIT', 429);
    this.name = 'RateLimitError';
  }
}

export class TaskNotCompleteError extends KalodataError {
  constructor(message = 'AI task is still processing') {
    super(message, 'TASK_NOT_COMPLETE', 202);
    this.name = 'TaskNotCompleteError';
  }
}
