/**
 * Kalodata Monitor Skill
 * 
 * Scheduled research runs with auto-alerts for NEW viral products.
 * - Runs research on schedule (configurable: hourly/daily/weekly)
 * - Detects NEW products (compares with previous run)
 * - Alerts on revenue threshold crossing
 * - Sends notifications via Slack webhook
 * - Stores previous run data for comparison
 */

import {
  createProductResearcher,
  type ProcessedProduct,
  type DateRange,
} from '../../src/kalodata/product-research.js';

// @ts-ignore - Node.js types expected at runtime
import * as fs from 'fs';
// @ts-ignore
import * as path from 'path';
// @ts-ignore
import * as https from 'https';
// @ts-ignore
import * as http from 'http';

// ============================================================================
// Types
// ============================================================================

export type ScheduleInterval = 'hourly' | 'daily' | 'weekly';

export interface AlertCondition {
  /** Revenue threshold in absolute value */
  revenueMin?: number;
  /** Revenue threshold as multiple of previous run */
  revenueGrowthMultiplier?: number;
  /** Minimum opportunity score (0-100) */
  opportunityScoreMin?: number;
  /** Alert when product crosses this revenue in new run */
  revenueCrosses?: number;
}

export interface MonitorProfile {
  /** Unique profile identifier */
  id: string;
  /** Profile name */
  name: string;
  /** Product category name or ID */
  category: string;
  /** Research goal */
  goal: string;
  /** Schedule interval */
  schedule: ScheduleInterval;
  /** Alert conditions */
  alerts: AlertCondition;
  /** Number of products to track */
  topProducts?: number;
  /** Date range for research */
  dateRange?: DateRange;
  /** Enabled status */
  enabled?: boolean;
  /** Last run timestamp */
  lastRun?: string;
  /** Slack webhook URL for notifications */
  slackWebhook?: string;
}

export interface MonitorConfig {
  /** Data directory for storing run history */
  dataDir: string;
  /** Default Kalodata credentials */
  credentials: {
    session: string;
    cfClearance: string;
  };
  /** Monitor profiles */
  profiles: MonitorProfile[];
  /** Default Slack webhook (used if profile doesn't have one) */
  defaultSlackWebhook?: string;
}

export interface ProductSnapshot {
  id: string;
  title: string;
  revenue: number;
  revenueFormatted: string;
  creators: number;
  sales: number;
  opportunityScore: number;
  competitionLevel: string;
  trendDirection: string;
  launchDate: string;
  price: { min: number; max: number; formatted: string };
  capturedAt: string;
}

export interface RunResult {
  profileId: string;
  profileName: string;
  category: string;
  goal: string;
  executedAt: string;
  products: ProductSnapshot[];
  newProducts: ProductSnapshot[];
  crossedThreshold: ProductSnapshot[];
  alerts: Alert[];
}

export interface Alert {
  type: 'new_product' | 'revenue_threshold' | 'opportunity';
  productId: string;
  productTitle: string;
  message: string;
  details?: Record<string, unknown>;
}

// ============================================================================
// Monitor Class
// ============================================================================

export class KalodataMonitor {
  private config: MonitorConfig;
  private researcher: ReturnType<typeof createProductResearcher>;
  private defaultDateRange: DateRange;

  constructor(config: MonitorConfig) {
    this.config = config;
    this.researcher = createProductResearcher({
      session: config.credentials.session,
      cfClearance: config.credentials.cfClearance,
    });

    // Default date range: last 30 days
    const end = new Date();
    const start = new Date();
    start.setDate(start.getDate() - 30);
    this.defaultDateRange = {
      start: start.toISOString().split('T')[0],
      end: end.toISOString().split('T')[0],
    };
  }

  /**
   * Get all profiles
   */
  getProfiles(): MonitorProfile[] {
    return this.config.profiles;
  }

  /**
   * Get a specific profile by ID
   */
  getProfile(id: string): MonitorProfile | undefined {
    return this.config.profiles.find(p => p.id === id);
  }

  /**
   * Add or update a monitor profile
   */
  saveProfile(profile: MonitorProfile): void {
    const existingIndex = this.config.profiles.findIndex(p => p.id === profile.id);
    if (existingIndex >= 0) {
      this.config.profiles[existingIndex] = profile;
    } else {
      this.config.profiles.push(profile);
    }
    this.persistConfig();
  }

  /**
   * Remove a profile
   */
  removeProfile(id: string): void {
    this.config.profiles = this.config.profiles.filter(p => p.id !== id);
    this.persistConfig();
  }

  /**
   * Run research for a specific profile
   */
  async runProfile(profileId: string): Promise<RunResult> {
    const profile = this.getProfile(profileId);
    if (!profile) {
      throw new Error(`Profile not found: ${profileId}`);
    }

    console.log(`\n📊 Running monitor: ${profile.name} (${profile.category} - ${profile.goal})`);

    // Resolve category ID
    const categoryId = await this.resolveCategoryId(profile.category);

    // Run research
    const products = await this.researcher.queryByGoal({
      categoryId,
      goal: profile.goal,
      dateRange: profile.dateRange || this.defaultDateRange,
      pageSize: profile.topProducts || 20,
    });

    // Convert to snapshots
    const snapshots = products.map(p => this.productToSnapshot(p));

    // Load previous run data
    const previousData = this.loadPreviousRun(profileId);

    // Compare and find new products
    const newProducts = this.findNewProducts(snapshots, previousData);

    // Find products crossing revenue thresholds
    const crossedThreshold = this.findThresholdCrossings(snapshots, previousData, profile.alerts);

    // Generate alerts
    const alerts = this.generateAlerts(profile, snapshots, newProducts, crossedThreshold);

    // Create run result
    const result: RunResult = {
      profileId: profile.id,
      profileName: profile.name,
      category: profile.category,
      goal: profile.goal,
      executedAt: new Date().toISOString(),
      products: snapshots,
      newProducts,
      crossedThreshold,
      alerts,
    };

    // Save current run
    this.saveRunResult(profileId, snapshots);

    // Update profile last run time
    profile.lastRun = result.executedAt;
    this.saveProfile(profile);

    // Send notifications
    if (alerts.length > 0) {
      const webhookUrl = profile.slackWebhook || this.config.defaultSlackWebhook;
      if (webhookUrl) {
        await this.sendSlackNotification(webhookUrl, result);
      }
    }

    return result;
  }

  /**
   * Run all enabled profiles
   */
  async runAll(): Promise<RunResult[]> {
    const enabledProfiles = this.config.profiles.filter(p => p.enabled !== false);
    const results: RunResult[] = [];

    for (const profile of enabledProfiles) {
      try {
        const result = await this.runProfile(profile.id);
        results.push(result);
      } catch (error) {
        console.error(`Error running profile ${profile.name}:`, error);
      }
    }

    return results;
  }

  /**
   * Run profiles due for their schedule
   */
  async runScheduled(): Promise<RunResult[]> {
    const now = new Date();
    const results: RunResult[] = [];

    for (const profile of this.config.profiles) {
      if (profile.enabled === false) continue;
      if (!profile.schedule) continue;

      const shouldRun = this.shouldRunNow(profile, now);
      if (shouldRun) {
        try {
          const result = await this.runProfile(profile.id);
          results.push(result);
        } catch (error) {
          console.error(`Error running scheduled profile ${profile.name}:`, error);
        }
      }
    }

    return results;
  }

  /**
   * Get comparison report between current and previous run
   */
  getComparison(profileId: string): { current: ProductSnapshot[]; previous: ProductSnapshot[]; changes: ComparisonChange[] } | null {
    const previous = this.loadPreviousRun(profileId);
    if (!previous) return null;

    const profile = this.getProfile(profileId);
    if (!profile) return null;

    // Run quick research for current data
    // Note: In real usage, you'd cache this from the last run
    return {
      current: [],
      previous,
      changes: [],
    };
  }

  /**
   * Export profile configuration
   */
  exportConfig(): string {
    return JSON.stringify(this.config, null, 2);
  }

  // ============================================================================
  // Private Methods
  // ============================================================================

  private productToSnapshot(product: ProcessedProduct): ProductSnapshot {
    return {
      id: product.id,
      title: product.title,
      revenue: product.revenue,
      revenueFormatted: product.revenueFormatted,
      creators: product.creators,
      sales: product.sales,
      opportunityScore: product.opportunityScore,
      competitionLevel: product.competitionLevel,
      trendDirection: product.trendDirection,
      launchDate: product.launchDate,
      price: product.price,
      capturedAt: new Date().toISOString(),
    };
  }

  private findNewProducts(current: ProductSnapshot[], previous: ProductSnapshot[] | null): ProductSnapshot[] {
    if (!previous || previous.length === 0) {
      // First run - all products are "new"
      return current.slice(0, 10);
    }

    const previousIds = new Set(previous.map(p => p.id));
    return current.filter(p => !previousIds.has(p.id));
  }

  private findThresholdCrossings(
    current: ProductSnapshot[],
    previous: ProductSnapshot[] | null,
    alerts: AlertCondition
  ): ProductSnapshot[] {
    if (!previous || previous.length === 0 || !alerts) return [];

    const crossed: ProductSnapshot[] = [];
    const previousMap = new Map(previous.map(p => [p.id, p]));

    for (const product of current) {
      const prev = previousMap.get(product.id);
      if (!prev) continue;

      // Check revenue crosses threshold
      if (alerts.revenueCrosses && prev.revenue < alerts.revenueCrosses && product.revenue >= alerts.revenueCrosses) {
        crossed.push(product);
        continue;
      }

      // Check revenue growth multiplier
      if (alerts.revenueGrowthMultiplier && prev.revenue > 0) {
        const multiplier = product.revenue / prev.revenue;
        if (multiplier >= alerts.revenueGrowthMultiplier) {
          crossed.push(product);
        }
      }
    }

    return crossed;
  }

  private generateAlerts(
    profile: MonitorProfile,
    products: ProductSnapshot[],
    newProducts: ProductSnapshot[],
    crossedThreshold: ProductSnapshot[]
  ): Alert[] {
    const alerts: Alert[] = [];

    // New products alert
    if (newProducts.length > 0) {
      alerts.push({
        type: 'new_product',
        productId: 'multiple',
        productTitle: `${newProducts.length} new products`,
        message: `Found ${newProducts.length} new products in ${profile.category} (${profile.goal})`,
        details: {
          products: newProducts.slice(0, 5).map(p => ({
            id: p.id,
            title: p.title,
            revenue: p.revenueFormatted,
          })),
        },
      });
    }

    // Revenue threshold alerts
    for (const product of crossedThreshold) {
      alerts.push({
        type: 'revenue_threshold',
        productId: product.id,
        productTitle: product.title,
        message: `${product.title} crossed revenue threshold: ${product.revenueFormatted}`,
        details: {
          revenue: product.revenue,
          opportunityScore: product.opportunityScore,
        },
      });
    }

    // High opportunity score alerts
    if (profile.alerts.opportunityScoreMin) {
      const highOpportunity = products.filter(p => p.opportunityScore >= profile.alerts.opportunityScoreMin!);
      if (highOpportunity.length > 0) {
        alerts.push({
          type: 'opportunity',
          productId: 'multiple',
          productTitle: `${highOpportunity.length} high-opportunity products`,
          message: `${highOpportunity.length} products with opportunity score >= ${profile.alerts.opportunityScoreMin}`,
          details: {
            products: highOpportunity.slice(0, 5).map(p => ({
              title: p.title,
              score: p.opportunityScore,
              revenue: p.revenueFormatted,
            })),
          },
        });
      }
    }

    return alerts;
  }

  private shouldRunNow(profile: MonitorProfile, now: Date): boolean {
    if (!profile.lastRun) return true;

    const lastRun = new Date(profile.lastRun);
    const hoursSinceLastRun = (now.getTime() - lastRun.getTime()) / (1000 * 60 * 60);

    switch (profile.schedule) {
      case 'hourly':
        return hoursSinceLastRun >= 1;
      case 'daily':
        return hoursSinceLastRun >= 24;
      case 'weekly':
        return hoursSinceLastRun >= 24 * 7;
      default:
        return false;
    }
  }

  private async resolveCategoryId(category: string): Promise<string> {
    const categories = await this.researcher.getCategories();
    const found = categories.find(
      c => c.name.toLowerCase() === category.toLowerCase() || c.id === category
    );
    if (found) {
      return found.id;
    }
    // Default to Beauty if not found
    return '600137235';
  }

  private getDataPath(profileId: string): string {
    return path.join(this.config.dataDir, `${profileId}.json`);
  }

  private loadPreviousRun(profileId: string): ProductSnapshot[] | null {
    const filePath = this.getDataPath(profileId);
    try {
      if (fs.existsSync(filePath)) {
        const data = fs.readFileSync(filePath, 'utf-8');
        return JSON.parse(data);
      }
    } catch (error) {
      console.error(`Error loading previous run for ${profileId}:`, error);
    }
    return null;
  }

  private saveRunResult(profileId: string, products: ProductSnapshot[]): void {
    const filePath = this.getDataPath(profileId);
    try {
      if (!fs.existsSync(this.config.dataDir)) {
        fs.mkdirSync(this.config.dataDir, { recursive: true });
      }
      fs.writeFileSync(filePath, JSON.stringify(products, null, 2));
    } catch (error) {
      console.error(`Error saving run result for ${profileId}:`, error);
    }
  }

  private persistConfig(): void {
    const configPath = path.join(this.config.dataDir, 'config.json');
    try {
      fs.writeFileSync(configPath, JSON.stringify(this.config, null, 2));
    } catch (error) {
      console.error('Error saving config:', error);
    }
  }

  private async sendSlackNotification(webhookUrl: string, result: RunResult): Promise<void> {
    if (!result.alerts || result.alerts.length === 0) return;

    const blocks = this.buildSlackBlocks(result);

    const payload = JSON.stringify({ blocks });

    return new Promise((resolve, reject) => {
      const url = new URL(webhookUrl);
      const protocol = url.protocol === 'https:' ? https : http;

      const req = protocol.request({
        hostname: url.hostname,
        port: url.port,
        path: url.pathname,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // @ts-ignore - Buffer is a Node.js global
          'Content-Length': Buffer.byteLength(payload),
        },
      }, (res: http.IncomingMessage) => {
        if (res.statusCode && res.statusCode >= 200 && res.statusCode < 300) {
          console.log('✅ Slack notification sent successfully');
          resolve();
        } else {
          reject(new Error(`Slack webhook failed with status: ${res.statusCode}`));
        }
      });

      req.on('error', reject);
      req.write(payload);
      req.end();
    });
  }

  private buildSlackBlocks(result: RunResult): SlackBlock[] {
    const blocks: SlackBlock[] = [];

    // Header
    blocks.push({
      type: 'header',
      text: {
        type: 'plain_text',
        text: `📊 Kalodata Monitor: ${result.profileName}`,
        emoji: true,
      },
    });

    // Summary
    const newCount = result.newProducts.length;
    const crossedCount = result.crossedThreshold.length;

    let summaryText = `*Category:* ${result.category} (${result.goal})\n`;
    summaryText += `*Run Time:* <!date^${Math.floor(new Date(result.executedAt).getTime() / 1000)}^{date_short} at {time}|${result.executedAt}>\n`;
    summaryText += `*New Products:* ${newCount}\n`;
    summaryText += `*Threshold Crossings:* ${crossedCount}`;

    blocks.push({
      type: 'section',
      text: {
        type: 'mrkdwn',
        text: summaryText,
      },
    });

    // Divider
    blocks.push({ type: 'divider' });

    // New Products
    if (result.newProducts.length > 0) {
      blocks.push({
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: `*🆕 New Products (${result.newProducts.length})*`,
        },
      });

      for (const product of result.newProducts.slice(0, 5)) {
        blocks.push({
          type: 'section',
          text: {
            type: 'mrkdwn',
            text: `• *${product.title}*\n  💰 ${product.revenueFormatted} | 👥 ${product.creators} creators | 📈 ${product.trendDirection}`,
          },
        });
      }

      blocks.push({ type: 'divider' });
    }

    // Threshold Crossings
    if (result.crossedThreshold.length > 0) {
      blocks.push({
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: `*⚡ Revenue Threshold Crossings (${result.crossedThreshold.length})*`,
        },
      });

      for (const product of result.crossedThreshold.slice(0, 5)) {
        blocks.push({
          type: 'section',
          text: {
            type: 'mrkdwn',
            text: `• *${product.title}*\n  💰 ${product.revenueFormatted} | Score: ${product.opportunityScore}/100`,
          },
        });
      }
    }

    // Footer
    blocks.push({
      type: 'context',
      elements: [
        {
          type: 'mrkdwn',
          text: `Kalodata Monitor • ${result.products.length} products tracked`,
        },
      ],
    });

    return blocks;
  }
}

// ============================================================================
// Slack Types
// ============================================================================

interface SlackBlock {
  type: 'header' | 'section' | 'divider' | 'context';
  text?: {
    type: 'plain_text' | 'mrkdwn';
    text: string;
    emoji?: boolean;
  };
  elements?: Array<{
    type: 'mrkdwn';
    text: string;
  }>;
}

interface ComparisonChange {
  productId: string;
  productTitle: string;
  change: 'new' | 'revenue_up' | 'revenue_down' | 'score_up' | 'score_down';
  previousValue?: number;
  currentValue?: number;
}

// ============================================================================
// Factory Functions
// ============================================================================

export function createMonitor(config: MonitorConfig): KalodataMonitor {
  return new KalodataMonitor(config);
}

export function loadMonitorConfig(dataDir: string): MonitorConfig {
  const configPath = path.join(dataDir, 'config.json');

  // Ensure data directory exists
  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
  }

  // Load existing config or create default
  if (fs.existsSync(configPath)) {
    const configData = fs.readFileSync(configPath, 'utf-8');
    return JSON.parse(configData);
  }

  // Return default config structure
  const defaultConfig: MonitorConfig = {
    dataDir,
    credentials: {
      // @ts-ignore - process.env is a Node.js global
      session: process.env.KALODATA_SESSION || '',
      // @ts-ignore
      cfClearance: process.env.KALODATA_CF_CLEARANCE || '',
    },
    profiles: [],
  };

  fs.writeFileSync(configPath, JSON.stringify(defaultConfig, null, 2));
  return defaultConfig;
}

export function createProfile(params: {
  id: string;
  name: string;
  category: string;
  goal: string;
  schedule: ScheduleInterval;
  alerts?: AlertCondition;
  slackWebhook?: string;
}): MonitorProfile {
  return {
    id: params.id,
    name: params.name,
    category: params.category,
    goal: params.goal,
    schedule: params.schedule,
    alerts: params.alerts || {},
    topProducts: 20,
    enabled: true,
    slackWebhook: params.slackWebhook,
  };
}

// ============================================================================
// CLI Interface
// ============================================================================

export async function runCLI(args: string[]): Promise<void> {
  // @ts-ignore - process.cwd() is a Node.js global
  const dataDir = path.join(process.cwd(), '.kalodata-monitor');
  const config = loadMonitorConfig(dataDir);

  // Check for credentials
  if (!config.credentials.session || !config.credentials.cfClearance) {
    console.error('❌ Missing credentials. Set KALODATA_SESSION and KALODATA_CF_CLEARANCE environment variables.');
    // @ts-ignore - process.exit() is a Node.js global
    process.exit(1);
  }

  const monitor = createMonitor(config);
  const command = args[2];

  switch (command) {
    case 'list':
    case 'ls': {
      console.log('\n📋 Monitor Profiles:\n');
      const profiles = monitor.getProfiles();
      if (profiles.length === 0) {
        console.log('  No profiles configured. Use "add" to create one.\n');
      } else {
        for (const p of profiles) {
          const status = p.enabled !== false ? '✅' : '❌';
          const lastRun = p.lastRun ? new Date(p.lastRun).toLocaleString() : 'Never';
          console.log(`  ${status} ${p.name}`);
          console.log(`     Category: ${p.category} | Goal: ${p.goal} | Schedule: ${p.schedule}`);
          console.log(`     Last run: ${lastRun}`);
          console.log('');
        }
      }
      break;
    }

    case 'add': {
      if (!args[3]) {
        console.log('Usage: monitor add <name> <category> <goal> <schedule> [slack-webhook]');
        console.log('  schedule: hourly, daily, weekly');
        break;
      }
      const name = args[3];
      const category = args[4] || 'Beauty';
      const goal = args[5] || 'trending';
      const schedule = (args[6] || 'daily') as ScheduleInterval;
      const webhook = args[7] || config.defaultSlackWebhook;

      const newProfile = createProfile({
        id: `profile-${Date.now()}`,
        name,
        category,
        goal,
        schedule,
        alerts: {
          revenueCrosses: 10000000,
          opportunityScoreMin: 70,
        },
        slackWebhook: webhook,
      });

      monitor.saveProfile(newProfile);
      console.log(`✅ Profile "${name}" created successfully!`);
      break;
    }

    case 'run': {
      const profileId = args[3];
      if (profileId) {
        const result = await monitor.runProfile(profileId);
        console.log('\n📊 Run Results:');
        console.log(`  New products: ${result.newProducts.length}`);
        console.log(`  Threshold crossings: ${result.crossedThreshold.length}`);
        console.log(`  Alerts: ${result.alerts.length}`);
      } else {
        console.log('\n🚀 Running all enabled profiles...');
        const results = await monitor.runAll();
        console.log(`\n✅ Completed ${results.length} profiles`);
      }
      break;
    }

    case 'scheduled':
    case 'schedule': {
      console.log('\n⏰ Running scheduled profiles...');
      const scheduledResults = await monitor.runScheduled();
      console.log(`\n✅ Completed ${scheduledResults.length} scheduled profiles`);
      break;
    }

    case 'remove':
    case 'rm': {
      if (!args[3]) {
        console.log('Usage: monitor remove <profile-id>');
        break;
      }
      monitor.removeProfile(args[3]);
      console.log(`✅ Profile removed`);
      break;
    }

    case 'enable': {
      if (!args[3]) {
        console.log('Usage: monitor enable <profile-id>');
        break;
      }
      const enableProfile = monitor.getProfile(args[3]);
      if (enableProfile) {
        enableProfile.enabled = true;
        monitor.saveProfile(enableProfile);
        console.log(`✅ Profile enabled`);
      } else {
        console.log(`❌ Profile not found: ${args[3]}`);
      }
      break;
    }

    case 'disable': {
      if (!args[3]) {
        console.log('Usage: monitor disable <profile-id>');
        break;
      }
      const disableProfile = monitor.getProfile(args[3]);
      if (disableProfile) {
        disableProfile.enabled = false;
        monitor.saveProfile(disableProfile);
        console.log(`✅ Profile disabled`);
      } else {
        console.log(`❌ Profile not found: ${args[3]}`);
      }
      break;
    }

    case 'config': {
      console.log('\n⚙️ Current Configuration:\n');
      console.log(monitor.exportConfig());
      break;
    }

    case 'help':
    default: {
      console.log(`
📊 Kalodata Monitor - CLI Usage

  list, ls              List all monitor profiles
  add <name> <category> <goal> <schedule> [webhook]
                        Add a new monitor profile
  run [profile-id]      Run a specific profile or all profiles
  scheduled             Run profiles due for their schedule
  remove <profile-id>   Remove a monitor profile
  enable <profile-id>   Enable a profile
  disable <profile-id>  Disable a profile
  config                Show full configuration

Examples:
  monitor add "Beauty Trending" Beauty trending daily
  monitor add "Weekly Fashion" Fashion emerging weekly https://hooks.slack.com/...
  monitor run
  monitor run profile-1234567890

Environment Variables:
  KALODATA_SESSION      Your Kalodata session cookie
  KALODATA_CF_CLEARANCE Your Cloudflare clearance token
`);
      break;
    }
  }
}

// ============================================================================
// Main Entry Point
// ============================================================================

// @ts-ignore - import.meta and process.argv are Node.js globals
if (import.meta.url === `file://${process.argv[1]}`) {
  // @ts-ignore
  runCLI(process.argv).catch(console.error);
}

export default KalodataMonitor;
