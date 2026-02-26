import { KalodataClient } from './client.js';
import type { ClientOptions, GetVideoScriptResponse } from './types.js';

/**
 * Storyboard extraction result with structured insights
 */
export interface StoryboardResult {
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

/**
 * Individual scene from storyboard
 */
export interface Scene {
  name: string;
  startTime: number;
  endTime: number;
  duration: number;
  shotScale: string;
  visualDescription: string;
}

/**
 * Auto-generated content idea from storyboard analysis
 */
export interface ContentIdea {
  title: string;
  description: string;
  angle: 'demonstration' | 'transformation' | 'lifestyle' | 'problem-solution' | 'emotional';
  keyScene: string;
  hook: string;
}

/**
 * Options for storyboard extraction
 */
export interface ExtractStoryboardOptions {
  videoId: string;
  dateRange: {
    start: string;
    end: string;
  };
  translate?: boolean;
  maxAttempts?: number;
  pollIntervalMs?: number;
}

/**
 * Storyboard Extractor - Extract AI-generated storyboards from viral videos
 * 
 * Provides scene breakdowns, visual descriptions, camera work analysis,
 * and auto-generates content ideas for replication.
 */
export class StoryboardExtractor {
  private client: KalodataClient;

  constructor(options: ClientOptions) {
    this.client = new KalodataClient(options);
  }

  /**
   * Extract storyboard from a video
   * Triggers AI analysis and polls for completion
   */
  async extractStoryboard(options: ExtractStoryboardOptions): Promise<StoryboardResult> {
    const { videoId, dateRange, translate = false, maxAttempts = 30, pollIntervalMs = 2000 } = options;

    // Generate unique ID for the task
    const uuid = `${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;

    // Start AI task for storyboard generation
    await this.client.startAiTask({
      id: videoId,
      type: 'video_script',
      partitionDayStart: dateRange.start,
      partitionDayEnd: dateRange.end,
      uuid,
    });

    // Wait for completion with polling
    const storyboard = await this.client.waitForVideoScript(
      {
        id: videoId,
        partitionDayStart: dateRange.start,
        partitionDayEnd: dateRange.end,
        translate,
      },
      maxAttempts,
      pollIntervalMs
    );

    // Process and transform the response
    return this.processStoryboard(videoId, storyboard);
  }

  /**
   * Analyze storyboard and extract key insights
   */
  analyzeStoryboard(storyboard: GetVideoScriptResponse): StoryboardAnalysis {
    const data = storyboard.data;
    
    return {
      keyToSuccess: this.parseKeyToSuccess(data.key_to_success),
      cameraWork: data.camera_work || '',
      gender: data.gender || 'unknown',
      language: data.language || 'unknown',
      sceneCount: data.video_scripts?.length || 0,
      totalDuration: this.calculateTotalDuration(data.video_scripts || []),
    };
  }

  /**
   * Generate 5 content ideas from storyboard analysis
   */
  generateContentIdeas(storyboard: GetVideoScriptResponse): ContentIdea[] {
    const data = storyboard.data;
    const ideas: ContentIdea[] = [];
    
    if (!data.video_scripts || data.video_scripts.length === 0) {
      return ideas;
    }

    // Extract scenes for content angles
    const scenes = data.video_scripts.map(s => ({
      name: s.scene,
      visualDescription: s.visual_description,
      shotScale: s.shot_scale,
    }));

    // Generate 5 diverse content ideas
    
    // 1. Demonstration-focused idea
    ideas.push({
      title: 'Produk Dimulai dengan Informasi',
      description: 'Mulai video dengan menampilkan produk secara langsung dan informatif. Tunjukkan tampilan lengkap produk di awal video.',
      angle: 'demonstration',
      keyScene: scenes.find(s => s.name.includes('Information'))?.name || scenes[0]?.name || '',
      hook: 'Lihat produk ini...',
    });

    // 2. Transformation/Showcase idea
    ideas.push({
      title: 'Putaran 360 Derajat',
      description: 'Fokus pada showing different angles dengan berputar untuk menunjukkan detail produk dari berbagai sisi.',
      angle: 'transformation',
      keyScene: scenes.find(s => s.name.includes('Selling'))?.name || scenes[1]?.name || '',
      hook: 'Lihat bagaimana produk ini terlihat dari semua sisi...',
    });

    // 3. Lifestyle/Experience idea  
    ideas.push({
      title: 'Pengalaman Nyata',
      description: 'Tunjukkan produk dalam penggunaan nyata dengan pose dan ekspresi alami yang menampilkan kepercayaan diri.',
      angle: 'lifestyle',
      keyScene: scenes.find(s => s.name.includes('Experience'))?.name || scenes[2]?.name || '',
      hook: 'Begini rasanya ketika memakai produk ini...',
    });

    // 4. Problem-Solution idea
    ideas.push({
      title: 'Skenario Penggunaan',
      description: '展示了产品在实际使用中的表现，通过动作演示产品的功能和特点。',
      angle: 'problem-solution',
      keyScene: scenes.find(s => s.name.includes('Usage'))?.name || scenes[3]?.name || '',
      hook: 'Mau tahu cara menggunakan produk ini?...',
    });

    // 5. Emotional/CTA idea
    ideas.push({
      title: 'Ajak Interaksi',
      description: 'Akhiri dengan CTA yang menarik dan interaksi positif untuk membangun engagement.',
      angle: 'emotional',
      keyScene: scenes.find(s => s.name.includes('Action'))?.name || scenes[scenes.length - 1]?.name || '',
      hook: 'Siap mencoba?...',
    });

    return ideas;
  }

  /**
   * Process raw API response into structured result
   */
  private processStoryboard(videoId: string, storyboard: GetVideoScriptResponse): StoryboardResult {
    const data = storyboard.data;
    
    const scenes: Scene[] = (data.video_scripts || []).map(s => ({
      name: s.scene,
      startTime: s.start_time,
      endTime: s.end_time,
      duration: s.end_time - s.start_time,
      shotScale: s.shot_scale,
      visualDescription: s.visual_description,
    }));

    const contentIdeas = this.generateContentIdeas(storyboard);

    return {
      videoId,
      language: data.language || 'unknown',
      gender: data.gender || 'unknown',
      keyToSuccess: this.parseKeyToSuccess(data.key_to_success),
      cameraWork: data.camera_work || '',
      scenes,
      contentIdeas,
      metadata: {
        extractedAt: new Date().toISOString(),
        totalDuration: this.calculateTotalDuration(data.video_scripts || []),
        sceneCount: scenes.length,
      },
    };
  }

  /**
   * Parse key_to_success string into array of factors
   */
  private parseKeyToSuccess(keyToSuccess: string | undefined): string[] {
    if (!keyToSuccess) return [];
    
    // Split by numbered items (1., 2., etc.) or newlines
    const factors = keyToSuccess
      .split(/\d+\.\s*/)
      .map(f => f.trim())
      .filter(f => f.length > 0);
    
    return factors.length > 0 ? factors : [keyToSuccess];
  }

  /**
   * Calculate total video duration from scenes
   */
  private calculateTotalDuration(scenes: Array<{ start_time: number; end_time: number }>): number {
    if (scenes.length === 0) return 0;
    const lastScene = scenes[scenes.length - 1];
    return lastScene.end_time;
  }

  /**
   * Update client credentials
   */
  updateCredentials(session: string, cfClearance: string): void {
    this.client.updateCredentials(session, cfClearance);
  }

  /**
   * Get current config
   */
  getConfig() {
    return this.client.getConfig();
  }
}

/**
 * Analysis result structure
 */
export interface StoryboardAnalysis {
  keyToSuccess: string[];
  cameraWork: string;
  gender: string;
  language: string;
  sceneCount: number;
  totalDuration: number;
}

/**
 * Factory function to create StoryboardExtractor
 */
export function createStoryboardExtractor(options: ClientOptions): StoryboardExtractor {
  return new StoryboardExtractor(options);
}
