export {
  type KalodataConfig,
  type ClientOptions,
  type ProductQueryRequest,
  type ProductQueryResponse,
  type Product,
  type ProductEnrichRequest,
  type ProductEnrichResponse,
  type ProductVideo,
  type ProductCountRequest,
  type ProductCountResponse,
  type VideoUrlRequest,
  type GetVideoUrlResponse,
  type CheckAiUseRequest,
  type CheckAiUseResponse,
  type ProgressInfo,
  type StartAiTaskRequest,
  type StartAiTaskResponse,
  type GetVideoScriptRequest,
  type GetVideoScriptResponse,
  type VideoScript,
  type GetVideoScriptData,
  type ApiResponse,
  KalodataError,
  AuthenticationError,
  RateLimitError,
  TaskNotCompleteError,
} from './types.js';

export {
  type AuthCredentials,
  getCredentialsFromEnv,
  parseCookies,
  setEnvGetter,
  buildCookieHeader,
  createHeaders,
  validateConfig,
} from './auth.js';

export { KalodataClient, createClient } from './client.js';

export {
  ProductResearcher,
  createProductResearcher,
  detectResearchGoal,
  formatCurrency,
  calculateTrendDirection,
  type QueryParams,
  type GoalQueryParams,
  type ProcessedProduct,
  type ResearchResult,
  type GoalAnalysis,
  type ProductFilters,
  type SortOption,
  type DateRange,
  type Category,
  type PriceInfo,
} from './product-research.js';

export {
  VideoAnalyzer,
  createVideoAnalyzer,
  type VideoInfo,
  type ProductVideos,
  type TopPerformingVideo,
  type ProductVideoAnalysis,
  type VideoAnalysisResult,
} from './video-analysis.js';

export {
  StoryboardExtractor,
  createStoryboardExtractor,
  type StoryboardResult,
  type Scene,
  type ContentIdea,
  type ExtractStoryboardOptions,
  type StoryboardAnalysis,
} from './storyboard-extract.js';
