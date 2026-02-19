import {
  type KalodataConfig,
  type ClientOptions,
  type ProductQueryRequest,
  type ProductQueryResponse,
  type ProductEnrichRequest,
  type ProductEnrichResponse,
  type ProductCountRequest,
  type ProductCountResponse,
  type VideoUrlRequest,
  type GetVideoUrlResponse,
  type CheckAiUseRequest,
  type CheckAiUseResponse,
  type StartAiTaskRequest,
  type StartAiTaskResponse,
  type GetVideoScriptRequest,
  type GetVideoScriptResponse,
  KalodataError,
  AuthenticationError,
  RateLimitError,
  TaskNotCompleteError,
} from './types.js';
import { validateConfig, createHeaders } from './auth.js';

export class KalodataClient {
  private config: KalodataConfig;
  private headers: Record<string, string>;

  constructor(options: ClientOptions = {}) {
    this.config = validateConfig(options);
    this.headers = createHeaders(this.config);
  }

  private async request<T>(
    method: 'GET' | 'POST',
    endpoint: string,
    body?: unknown
  ): Promise<T> {
    const url = `${this.config.baseUrl}${endpoint}`;
    let lastError: Error | null = null;

    for (let attempt = 0; attempt <= (this.config.maxRetries ?? 3); attempt++) {
      try {
        const response = await this.executeRequest<T>(method, url, body);

        if (!response.success) {
          const errorMessage = response.message || 'API request failed';
          throw new KalodataError(errorMessage, response.code || 'UNKNOWN');
        }

        return response.data;
      } catch (error) {
        if (error instanceof KalodataError) {
          if (error instanceof AuthenticationError) {
            throw error;
          }
          if (error instanceof RateLimitError) {
            const delay = this.config.retryDelay! * Math.pow(2, attempt);
            await this.sleep(delay);
            lastError = error;
            continue;
          }
          if (error instanceof TaskNotCompleteError) {
            throw error;
          }
        }

        if (attempt < (this.config.maxRetries ?? 3)) {
          const delay = this.config.retryDelay! * Math.pow(2, attempt);
          await this.sleep(delay);
          lastError = error instanceof Error ? error : new Error(String(error));
        } else {
          throw lastError || error;
        }
      }
    }

    throw lastError || new Error('Request failed after retries');
  }

  private async executeRequest<T>(
    method: 'GET' | 'POST',
    url: string,
    body?: unknown
  ): Promise<{ success: boolean; data: T; message: string | null; code: string | null }> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.config.timeout);

    try {
      const fetchOptions: RequestInit = {
        method,
        headers: this.headers,
        signal: controller.signal,
      };

      if (body && method === 'POST') {
        fetchOptions.body = JSON.stringify(body);
      }

      const response = await fetch(url, fetchOptions);

      if (response.status === 401) {
        throw new AuthenticationError('Invalid or expired credentials');
      }

      if (response.status === 429) {
        throw new RateLimitError('Rate limit exceeded');
      }

      if (!response.ok) {
        throw new KalodataError(
          `HTTP error: ${response.status}`,
          undefined,
          response.status
        );
      }

      const data = await response.json() as { success: boolean; data: T; message: string | null; code: string | null; cached?: boolean };
      return data;
    } catch (error) {
      if (error instanceof Error && error.name === 'AbortError') {
        throw new KalodataError('Request timeout');
      }
      throw error;
    } finally {
      clearTimeout(timeoutId);
    }
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async queryProducts(request: ProductQueryRequest): Promise<ProductQueryResponse> {
    return this.request('POST', '/product/queryList', request);
  }

  async enrichProducts(request: ProductEnrichRequest): Promise<ProductEnrichResponse> {
    return this.request('POST', '/product/enrich', request);
  }

  async checkAiUse(request: CheckAiUseRequest): Promise<CheckAiUseResponse> {
    const params = new URLSearchParams({
      id: request.id,
      type: request.type,
    });
    return this.request('GET', `/benefit/checkAiUse?${params}`, undefined);
  }

  async getVideoUrl(request: VideoUrlRequest): Promise<GetVideoUrlResponse> {
    const params = new URLSearchParams({ videoId: request.videoId });
    return this.request('GET', `/video/detail/getVideoUrl?${params}`, undefined);
  }

  async startAiTask(request: StartAiTaskRequest): Promise<StartAiTaskResponse> {
    return this.request('POST', '/aiTask/startAiTask', request);
  }

  async getVideoScript(request: GetVideoScriptRequest): Promise<GetVideoScriptResponse> {
    const response = await this.request<{
      success: boolean;
      data: GetVideoScriptResponse['data'];
      message: string | null;
      code: string | null;
    }>('POST', '/aiTask/video/getVideoScript', request);

    if (!response.success && response.code === '1') {
      throw new TaskNotCompleteError('AI task is still processing');
    }

    return {
      success: response.success,
      data: response.data,
      message: response.message,
      cached: null,
      code: response.code,
    };
  }

  async getProductCount(request: ProductCountRequest): Promise<ProductCountResponse> {
    return this.request('POST', '/product/count', request);
  }

  async waitForVideoScript(
    request: GetVideoScriptRequest,
    maxAttempts = 30,
    intervalMs = 2000
  ): Promise<GetVideoScriptResponse> {
    for (let attempt = 0; attempt < maxAttempts; attempt++) {
      try {
        return await this.getVideoScript(request);
      } catch (error) {
        if (error instanceof TaskNotCompleteError) {
          await this.sleep(intervalMs);
          continue;
        }
        throw error;
      }
    }
    throw new Error('Video script generation timed out');
  }

  updateCredentials(session: string, cfClearance: string): void {
    this.config.session = session;
    this.config.cfClearance = cfClearance;
    this.headers = createHeaders(this.config);
  }

  getConfig(): Readonly<KalodataConfig> {
    return { ...this.config };
  }
}

export function createClient(options?: ClientOptions): KalodataClient {
  return new KalodataClient(options);
}
