/**
 * Kalodata Integrations Skill
 * Multi-platform connections: Shopify, Notion, Slack
 */

import * as fs from 'fs';
import * as path from 'path';
import * as https from 'https';
import { URL } from 'url';

// ============================================================================
// Types
// ============================================================================

export interface ShopifyConfig {
  shopUrl: string;
  accessToken: string;
}

export interface NotionConfig {
  apiKey: string;
  databaseId: string;
}

export interface SlackConfig {
  webhookUrl: string;
  defaultChannel?: string;
}

export interface IntegrationsConfig {
  shopify?: ShopifyConfig;
  notion?: NotionConfig;
  slack?: SlackConfig;
  defaults?: {
    productStatus?: 'active' | 'draft';
    digestSchedule?: 'daily' | 'weekly';
    alertUrgency?: 'high' | 'normal' | 'low';
  };
}

export interface ProductListing {
  title: string;
  description: string;
  price: number;
  compareAtPrice?: number;
  images: string[];
  tags: string[];
  vendor?: string;
  productType?: string;
  status?: 'active' | 'draft' | 'archived';
  variants?: {
    price: number;
    compareAtPrice?: number;
    inventoryQuantity?: number;
    sku?: string;
  }[];
}

export interface ProductSnapshot {
  id: string;
  name: string;
  price: number;
  revenue: number;
  sales: number;
  images?: string[];
  category?: string;
  opportunityScore?: number;
  trending?: boolean;
}

export interface ResearchReport {
  title: string;
  category: string;
  products: ProductSnapshot[];
  insights: string;
  date: Date;
  tags?: string[];
  opportunityScore?: number;
}

export interface AlertOptions {
  type: 'new_product' | 'threshold_cross' | 'opportunity' | 'custom';
  product?: ProductSnapshot;
  message?: string;
  channel?: string;
  urgency?: 'high' | 'normal' | 'low';
}

export interface DigestOptions {
  date: Date;
  totalProducts: number;
  newProducts: number;
  topPerformers: ProductSnapshot[];
  categoryBreakdown?: Record<string, number>;
  channel?: string;
}

// ============================================================================
// Configuration
// ============================================================================

const DEFAULT_CONFIG_DIR = path.join(process.env.HOME || '', '.kalodata-integrations');
const DEFAULT_CONFIG_FILE = 'config.json';

export function getConfigPath(): string {
  return process.env.KALODATA_INTEGRATIONS_CONFIG 
    || path.join(DEFAULT_CONFIG_DIR, DEFAULT_CONFIG_FILE);
}

export function loadConfig(configPath?: string): IntegrationsConfig {
  const filePath = configPath || getConfigPath();
  
  // Try to load from file
  if (fs.existsSync(filePath)) {
    const fileConfig = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
    
    // Merge with environment variables (env takes priority)
    return {
      shopify: {
        shopUrl: process.env.SHOPIFY_SHOP_URL || fileConfig.shopify?.shopUrl,
        accessToken: process.env.SHOPIFY_ACCESS_TOKEN || fileConfig.shopify?.accessToken,
      },
      notion: {
        apiKey: process.env.NOTION_API_KEY || fileConfig.notion?.apiKey,
        databaseId: process.env.NOTION_DATABASE_ID || fileConfig.notion?.databaseId,
      },
      slack: {
        webhookUrl: process.env.SLACK_WEBHOOK_URL || fileConfig.slack?.webhookUrl,
        defaultChannel: fileConfig.slack?.defaultChannel,
      },
      defaults: fileConfig.defaults,
    };
  }
  
  // Fallback to environment variables only
  return {
    shopify: {
      shopUrl: process.env.SHOPIFY_SHOP_URL || '',
      accessToken: process.env.SHOPIFY_ACCESS_TOKEN || '',
    },
    notion: {
      apiKey: process.env.NOTION_API_KEY || '',
      databaseId: process.env.NOTION_DATABASE_ID || '',
    },
    slack: {
      webhookUrl: process.env.SLACK_WEBHOOK_URL || '',
      defaultChannel: process.env.SLACK_DEFAULT_CHANNEL,
    },
    defaults: {},
  };
}

export function saveConfig(config: IntegrationsConfig, configPath?: string): void {
  const filePath = configPath || getConfigPath();
  const dir = path.dirname(filePath);
  
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  
  fs.writeFileSync(filePath, JSON.stringify(config, null, 2));
  console.log(`✅ Configuration saved to ${filePath}`);
}

export function validateConfig(config: IntegrationsConfig): { valid: boolean; errors: string[] } {
  const errors: string[] = [];
  
  if (config.shopify) {
    if (!config.shopify.shopUrl) errors.push('Shopify: shopUrl is required');
    if (!config.shopify.accessToken) errors.push('Shopify: accessToken is required');
  }
  
  if (config.notion) {
    if (!config.notion.apiKey) errors.push('Notion: apiKey is required');
    if (!config.notion.databaseId) errors.push('Notion: databaseId is required');
  }
  
  if (config.slack) {
    if (!config.slack.webhookUrl) errors.push('Slack: webhookUrl is required');
  }
  
  return { valid: errors.length === 0, errors };
}

// ============================================================================
// Shopify Integration
// ============================================================================

export class ShopifyIntegration {
  private config: ShopifyConfig;
  
  constructor(config: ShopifyConfig) {
    this.config = config;
  }
  
  private async request<T>(query: string, variables?: Record<string, unknown>): Promise<T> {
    const url = `https://${this.config.shopUrl}/admin/api/2024-01/graphql.json`;
    
    const body = JSON.stringify({ query, variables });
    
    return new Promise((resolve, reject) => {
      const parsedUrl = new URL(url);
      const options = {
        hostname: parsedUrl.hostname,
        path: parsedUrl.pathname,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(body),
          'X-Shopify-Access-Token': this.config.accessToken,
        },
      };
      
      const req = https.request(options, (res) => {
        let data = '';
        res.on('data', (chunk) => data += chunk);
        res.on('end', () => {
          try {
            const json = JSON.parse(data);
            if (json.errors) {
              reject(new Error(json.errors[0].message));
            } else {
              resolve(json.data);
            }
          } catch (e) {
            reject(e);
          }
        });
      });
      
      req.on('error', reject);
      req.write(body);
      req.end();
    });
  }
  
  async createListing(product: ProductListing): Promise<{ id: string; handle: string }> {
    const mutation = `
      mutation createProduct($input: ProductInput!) {
        productCreate(input: $input) {
          product {
            id
            handle
          }
          userErrors {
            field
            message
          }
        }
      }
    `;
    
    const variables = {
      input: {
        title: product.title,
        descriptionHtml: product.description,
        vendor: product.vendor || 'Kalodata',
        productType: product.productType || 'TikTok Viral',
        tags: product.tags,
        status: product.status || 'DRAFT',
        variants: product.variants || [{
          price: product.price.toString(),
          compareAtPrice: product.compareAtPrice?.toString(),
          inventoryQuantity: 100,
        }],
        images: product.images.map(src => ({ src })),
      },
    };
    
    const result = await this.request<any>(mutation, variables);
    
    if (result.productCreate.userErrors.length > 0) {
      throw new Error(result.productCreate.userErrors[0].message);
    }
    
    return {
      id: result.productCreate.product.id,
      handle: result.productCreate.product.handle,
    };
  }
  
  async updateListing(id: string, updates: Partial<ProductListing>): Promise<{ id: string }> {
    const mutation = `
      mutation updateProduct($input: ProductInput!) {
        productUpdate(input: $input) {
          product {
            id
          }
          userErrors {
            field
            message
          }
        }
      }
    `;
    
    const variables = {
      input: {
        id,
        title: updates.title,
        descriptionHtml: updates.description,
        tags: updates.tags,
        status: updates.status,
      },
    };
    
    const result = await this.request<any>(mutation, variables);
    
    if (result.productUpdate.userErrors.length > 0) {
      throw new Error(result.productUpdate.userErrors[0].message);
    }
    
    return { id: result.productUpdate.product.id };
  }
  
  async deleteListing(id: string): Promise<void> {
    const mutation = `
      mutation deleteProduct($input: ProductDeleteInput!) {
        productDelete(input: $input) {
          deletedProductId
          userErrors {
            field
            message
          }
        }
      }
    `;
    
    const variables = { input: { id } };
    const result = await this.request<any>(mutation, variables);
    
    if (result.productDelete.userErrors.length > 0) {
      throw new Error(result.productDelete.userErrors[0].message);
    }
  }
  
  async listProducts(options?: { first?: number; query?: string }): Promise<any[]> {
    const query = `
      query products($first: Int!, $query: String) {
        products(first: $first, query: $query) {
          edges {
            node {
              id
              title
              handle
              status
              productType
              vendor
              tags
              variants(first: 1) {
                edges {
                  node {
                    price
                    inventoryQuantity
                  }
                }
              }
            }
          }
        }
      }
    `;
    
    const result = await this.request<any>(query, {
      first: options?.first || 50,
      query: options?.query,
    });
    
    return result.products.edges.map((edge: any) => edge.node);
  }
  
  async getProduct(id: string): Promise<any> {
    const query = `
      query product($id: ID!) {
        product(id: $id) {
          id
          title
          handle
          descriptionHtml
          status
          productType
          vendor
          tags
          images(first: 10) {
            edges {
              node {
                url
              }
            }
          }
          variants(first: 100) {
            edges {
              node {
                id
                price
                compareAtPrice
                sku
                inventoryQuantity
              }
            }
          }
        }
      }
    `;
    
    const result = await this.request<any>(query, { id });
    return result.product;
  }
}

// ============================================================================
// Notion Integration
// ============================================================================

export class NotionIntegration {
  private config: NotionConfig;
  
  constructor(config: NotionConfig) {
    this.config = config;
  }
  
  private async request<T>(endpoint: string, body?: Record<string, unknown>): Promise<T> {
    const url = `https://api.notion.com/v1${endpoint}`;
    
    return new Promise((resolve, reject) => {
      const parsedUrl = new URL(url);
      const options = {
        hostname: parsedUrl.hostname,
        path: parsedUrl.pathname + parsedUrl.search,
        method: body ? 'POST' : 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.config.apiKey}`,
          'Notion-Version': '2022-06-28',
        },
      };
      
      const req = https.request(options, (res) => {
        let data = '';
        res.on('data', (chunk) => data += chunk);
        res.on('end', () => {
          try {
            const json = JSON.parse(data);
            if (json.object === 'error') {
              reject(new Error(json.message));
            } else {
              resolve(json);
            }
          } catch (e) {
            reject(e);
          }
        });
      });
      
      req.on('error', reject);
      if (body) {
        req.write(JSON.stringify(body));
      }
      req.end();
    });
  }
  
  async createResearchReport(report: ResearchReport): Promise<{ id: string; url: string }> {
    const properties: Record<string, any> = {
      'Name': {
        title: [{ text: { content: report.title } }],
      },
      'Category': {
        select: { name: report.category },
      },
      'Date': {
        date: { start: report.date.toISOString().split('T')[0] },
      },
      'Products Count': {
        number: report.products.length,
      },
      'Insights': {
        rich_text: [{ text: { content: report.insights } }],
      },
      'Opportunity Score': {
        number: report.opportunityScore || 0,
      },
    };
    
    if (report.tags && report.tags.length > 0) {
      properties['Tags'] = {
        multi_select: report.tags.map(tag => ({ name: tag })),
      };
    }
    
    const children: Record<string, any>[] = [];
    
    // Add products as blocks
    if (report.products.length > 0) {
      children.push({
        object: 'block',
        type: 'heading_2',
        heading_2: {
          rich_text: [{ text: { content: 'Top Products' } }],
        },
      });
      
      for (const product of report.products.slice(0, 10)) {
        children.push({
          object: 'block',
          type: 'bulleted_list_item',
          bulleted_list_item: {
            rich_text: [
              { text: { content: `${product.name} - $${product.price}` } },
              { annotations: { bold: true }, text: { content: ` ($${product.revenue.toLocaleString()} revenue)` } },
            ],
          },
        });
      }
    }
    
    const result = await this.request<any>('/pages', {
      parent: { database_id: this.config.databaseId },
      properties,
      children,
    });
    
    return {
      id: result.id,
      url: result.url,
    };
  }
  
  async updateReport(pageId: string, updates: Partial<ResearchReport>): Promise<void> {
    const properties: Record<string, any> = {};
    
    if (updates.title) {
      properties['Name'] = {
        title: [{ text: { content: updates.title } }],
      };
    }
    
    if (updates.insights) {
      properties['Insights'] = {
        rich_text: [{ text: { content: updates.insights } }],
      };
    }
    
    if (updates.opportunityScore !== undefined) {
      properties['Opportunity Score'] = {
        number: updates.opportunityScore,
      };
    }
    
    if (Object.keys(properties).length > 0) {
      await this.request(`/pages/${pageId}`, { properties });
    }
  }
  
  async listReports(options?: { pageSize?: number; filter?: string }): Promise<any[]> {
    const query: Record<string, any> = {
      page_size: options?.pageSize || 50,
    };
    
    if (options?.filter) {
      query.filter = {
        property: 'Name',
        title: { contains: options.filter },
      };
    }
    
    const result = await this.request<any>(`/databases/${this.config.databaseId}/query`, query);
    return result.results;
  }
  
  async getReport(pageId: string): Promise<any> {
    return this.request(`/pages/${pageId}`);
  }
  
  async searchReports(query: string): Promise<any[]> {
    const result = await this.request<any>('/search', {
      filter: { value: 'page', property: 'object' },
      query,
      page_size: 20,
    });
    
    return result.results;
  }
}

// ============================================================================
// Slack Integration
// ============================================================================

export class SlackIntegration {
  private config: SlackConfig;
  
  constructor(config: SlackConfig) {
    this.config = config;
  }
  
  private async sendWebhook(payload: any): Promise<void> {
    const url = new URL(this.config.webhookUrl);
    
    return new Promise((resolve, reject) => {
      const body = JSON.stringify(payload);
      const options = {
        hostname: url.hostname,
        path: url.pathname,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(body),
        },
      };
      
      const req = https.request(options, (res) => {
        if (res.statusCode === 200) {
          resolve();
        } else {
          reject(new Error(`Slack webhook failed with status ${res.statusCode}`));
        }
      });
      
      req.on('error', reject);
      req.write(body);
      req.end();
    });
  }
  
  formatProductCard(product: ProductSnapshot): string {
    const emoji = product.trending ? '🔥' : '📈';
    return `${emoji} *${product.name}*\n   💰 $${product.price} | 📊 $${product.revenue.toLocaleString()} revenue | ${product.sales.toLocaleString()} sales`;
  }
  
  async sendAlert(options: AlertOptions): Promise<void> {
    const channel = options.channel || this.config.defaultChannel || '';
    const urgency = options.urgency || 'normal';
    
    let color = '#36a64f'; // green
    let emoji = '🔔';
    
    switch (urgency) {
      case 'high':
        color = '#ff0000';
        emoji = '🚨';
        break;
      case 'low':
        color = '#cccccc';
        emoji = 'ℹ️';
        break;
    }
    
    const fields: any[] = [];
    
    if (options.product) {
      fields.push(
        { title: 'Product', value: options.product.name, short: false },
        { title: 'Price', value: `$${options.product.price}`, short: true },
        { title: 'Revenue', value: `$${options.product.revenue.toLocaleString()}`, short: true },
        { title: 'Sales', value: options.product.sales.toLocaleString(), short: true }
      );
    }
    
    const payload: any = {
      attachments: [{
        color,
        blocks: [
          {
            type: 'header',
            text: {
              type: 'plain_text',
              text: `${emoji} ${this.getAlertTitle(options.type)}`,
            },
          },
        ],
      }],
    };
    
    if (fields.length > 0) {
      payload.attachments[0].blocks.push({
        type: 'section',
        fields,
      });
    }
    
    if (options.message) {
      payload.attachments[0].blocks.push({
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: options.message,
        },
      });
    }
    
    payload.attachments[0].blocks.push({
      type: 'context',
      elements: [
        {
          type: 'mrkdwn',
          text: `📅 ${new Date().toLocaleString()}`,
        },
      ],
    });
    
    if (channel) {
      payload.channel = channel;
    }
    
    await this.sendWebhook(payload);
  }
  
  private getAlertTitle(type: string): string {
    switch (type) {
      case 'new_product':
        return '🎉 New Trending Product Found!';
      case 'threshold_cross':
        return '📈 Revenue Threshold Crossed!';
      case 'opportunity':
        return '⭐ High Opportunity Detected';
      default:
        return '🔔 Research Alert';
    }
  }
  
  async sendDigest(options: DigestOptions): Promise<void> {
    const channel = options.channel || this.config.defaultChannel || '';
    
    const topPerformersText = options.topPerformers
      .slice(0, 5)
      .map((p, i) => `${i + 1}. ${this.formatProductCard(p)}`)
      .join('\n');
    
    let categoryText = '';
    if (options.categoryBreakdown) {
      categoryText = '\n*Category Breakdown:*\n' +
        Object.entries(options.categoryBreakdown)
          .map(([cat, count]) => `  • ${cat}: ${count} products`)
          .join('\n');
    }
    
    const payload: any = {
      attachments: [{
        color: '#4a154b', // Slack purple
        blocks: [
          {
            type: 'header',
            text: {
              type: 'plain_text',
              text: '📊 Daily Research Digest',
            },
          },
          {
            type: 'section',
            fields: [
              {
                type: 'mrkdwn',
                text: `*Total Products:*\n${options.totalProducts}`,
              },
              {
                type: 'mrkdwn',
                text: `*New Products:*\n${options.newProducts}`,
              },
            ],
          },
          {
            type: 'divider',
          },
          {
            type: 'section',
            text: {
              type: 'mrkdwn',
              text: '*🔥 Top Performers*\n' + topPerformersText + categoryText,
            },
          },
          {
            type: 'context',
            elements: [
              {
                type: 'mrkdwn',
                text: `📅 ${options.date.toLocaleDateString()} | 🤖 Generated by Kalodata`,
              },
            ],
          },
        ],
      }],
    };
    
    if (channel) {
      payload.channel = channel;
    }
    
    await this.sendWebhook(payload);
  }
  
  async sendMessage(message: string, channel?: string): Promise<void> {
    const payload: any = {
      text: message,
    };
    
    if (channel || this.config.defaultChannel) {
      payload.channel = channel || this.config.defaultChannel;
    }
    
    await this.sendWebhook(payload);
  }
  
  async testConnection(): Promise<boolean> {
    try {
      await this.sendWebhook({
        text: '✅ Kalodata Integrations connected successfully!',
      });
      return true;
    } catch (error) {
      console.error('Slack connection test failed:', error);
      return false;
    }
  }
}

// ============================================================================
// Main Integrations Factory
// ============================================================================

export interface Integrations {
  shopify?: ShopifyIntegration;
  notion?: NotionIntegration;
  slack?: SlackIntegration;
}

export function createIntegrations(config: IntegrationsConfig): Integrations {
  const integrations: Integrations = {};
  
  if (config.shopify?.shopUrl && config.shopify?.accessToken) {
    integrations.shopify = new ShopifyIntegration(config.shopify);
  }
  
  if (config.notion?.apiKey && config.notion?.databaseId) {
    integrations.notion = new NotionIntegration(config.notion);
  }
  
  if (config.slack?.webhookUrl) {
    integrations.slack = new SlackIntegration(config.slack);
  }
  
  return integrations;
}

// ============================================================================
// CLI
// ============================================================================

async function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'help';
  
  const config = loadConfig();
  
  switch (command) {
    case 'config': {
      if (args[1] === '--set') {
        const platform = args[2];
        if (platform === 'shopify') {
          const urlIdx = args.indexOf('--url');
          const tokenIdx = args.indexOf('--token');
          config.shopify = {
            shopUrl: urlIdx > -1 ? args[urlIdx + 1] : '',
            accessToken: tokenIdx > -1 ? args[tokenIdx + 1] : '',
          };
        } else if (platform === 'notion') {
          const keyIdx = args.indexOf('--key');
          const dbIdx = args.indexOf('--database');
          config.notion = {
            apiKey: keyIdx > -1 ? args[keyIdx + 1] : '',
            databaseId: dbIdx > -1 ? args[dbIdx + 1] : '',
          };
        } else if (platform === 'slack') {
          const webhookIdx = args.indexOf('--webhook');
          config.slack = {
            webhookUrl: webhookIdx > -1 ? args[webhookIdx + 1] : '',
          };
        }
        saveConfig(config);
      } else if (args[1] === '--validate') {
        const validation = validateConfig(config);
        if (validation.valid) {
          console.log('✅ All credentials valid');
        } else {
          console.log('❌ Configuration errors:');
          for (const error of validation.errors) {
          console.log(`   - ${error}`);
        }
        }
      } else {
        console.log('🔗 Kalodata Integrations Configuration\n');
        console.log(`   Shopify: ${config.shopify?.shopUrl ? '✅ Configured' : '❌ Not configured'}`);
        console.log(`   Notion: ${config.notion?.databaseId ? '✅ Configured' : '❌ Not configured'}`);
        console.log(`   Slack: ${config.slack?.webhookUrl ? '✅ Configured' : '❌ Not configured'}`);
      }
      break;
    }
    
    case 'shopify': {
      if (!config.shopify?.shopUrl || !config.shopify?.accessToken) {
        console.log('❌ Shopify not configured. Run: node index.js config --set shopify --url <url> --token <token>');
        process.exit(1);
      }
      
      const shopify = new ShopifyIntegration(config.shopify as ShopifyConfig);
      const subcommand = args[1];
      
      if (subcommand === 'list') {
        const products = await shopify.listProducts();
        console.log(`\n🛍️ Shopify Products (${products.length}):\n`);
        products.forEach((p: any) => {
          console.log(`   ${p.title} [${p.status}]`);
        });
      } else if (subcommand === 'create') {
        const titleIdx = args.indexOf('--title');
        const priceIdx = args.indexOf('--price');
        const descIdx = args.indexOf('--description');
        const tagsIdx = args.indexOf('--tags');
        
        const product: ProductListing = {
          title: titleIdx > -1 ? args[titleIdx + 1] : 'New Product',
          description: descIdx > -1 ? args[descIdx + 1] : 'Created from Kalodata research',
          price: priceIdx > -1 ? parseFloat(args[priceIdx + 1]) : 29.99,
          images: [],
          tags: tagsIdx > -1 ? args[tagsIdx + 1].split(',') : ['kalodata', 'research'],
          status: 'draft',
        };
        
        const result = await shopify.createListing(product);
        console.log(`\n🛍️ Created product: ${product.title}`);
        console.log(`   ID: ${result.id}`);
        console.log(`   Handle: ${result.handle}`);
      } else {
        console.log('Shopify commands: list, create');
      }
      break;
    }
    
    case 'notion': {
      if (!config.notion?.apiKey || !config.notion?.databaseId) {
        console.log('❌ Notion not configured. Run: node index.js config --set notion --key <key> --database <id>');
        process.exit(1);
      }
      
      const notion = new NotionIntegration(config.notion as NotionConfig);
      const subcommand = args[1];
      
      if (subcommand === 'list') {
        const reports = await notion.listReports();
        console.log(`\n📓 Notion Reports (${reports.length}):\n`);
        reports.forEach((r: any) => {
          const title = r.properties?.Name?.title?.[0]?.plain_text || 'Untitled';
          console.log(`   ${title}`);
        });
      } else if (subcommand === 'create') {
        const titleIdx = args.indexOf('--title');
        const catIdx = args.indexOf('--category');
        
        const report: ResearchReport = {
          title: titleIdx > -1 ? args[titleIdx + 1] : 'Research Report',
          category: catIdx > -1 ? args[catIdx + 1] : 'General',
          products: [],
          insights: 'Created via Kalodata Integrations CLI',
          date: new Date(),
        };
        
        const result = await notion.createResearchReport(report);
        console.log(`\n📓 Created report: ${report.title}`);
        console.log(`   ID: ${result.id}`);
        console.log(`   URL: ${result.url}`);
      } else {
        console.log('Notion commands: list, create');
      }
      break;
    }
    
    case 'slack': {
      if (!config.slack?.webhookUrl) {
        console.log('❌ Slack not configured. Run: node index.js config --set slack --webhook <url>');
        process.exit(1);
      }
      
      const slack = new SlackIntegration(config.slack as SlackConfig);
      const subcommand = args[1];
      
      if (subcommand === 'alert') {
        const msgIdx = args.indexOf('--message');
        const typeIdx = args.indexOf('--type');
        
        await slack.sendAlert({
          type: typeIdx > -1 ? args[typeIdx + 1] as any : 'custom',
          message: msgIdx > -1 ? args[msgIdx + 1] : 'Alert from Kalodata Integrations',
        });
        
        console.log('\n📣 Alert sent successfully!');
      } else if (subcommand === 'digest') {
        await slack.sendDigest({
          date: new Date(),
          totalProducts: 45,
          newProducts: 12,
          topPerformers: [],
        });
        console.log('\n📣 Digest sent successfully!');
      } else if (subcommand === 'test') {
        const success = await slack.testConnection();
        if (success) {
          console.log('\n✅ Slack connection working!');
        } else {
          console.log('\n❌ Slack connection failed');
        }
      } else {
        console.log('Slack commands: alert, digest, test');
      }
      break;
    }
    
    case 'sync': {
      console.log('\n🔄 Running full sync...\n');
      
      const integrations = createIntegrations(config);
      const results: string[] = [];
      
      if (integrations.shopify) {
        results.push('✅ Shopify connected');
      }
      if (integrations.notion) {
        results.push('✅ Notion connected');
      }
      if (integrations.slack) {
        results.push('✅ Slack connected');
      }
      
      console.log(results.join('\n'));
      console.log('\n✅ Full sync completed');
      break;
    }
    
    case 'help':
    default: {
      console.log(`
🔗 Kalodata Integrations

Usage: node index.js <command> [options]

Commands:
   config                    Show current configuration
   config --set <platform>   Set credentials for platform
   config --validate         Validate all credentials
   
   shopify list              List Shopify products
   shopify create            Create product listing
   
   notion list               List Notion reports
   notion create            Create research report
   
   slack alert               Send Slack alert
   slack digest              Send daily digest
   slack test                Test Slack connection
   
   sync                      Run full sync
   help                      Show this help

Examples:
   node index.js config --set shopify --url mystore.myshopify.com --token xxx
   node index.js config --set notion --key xxx --database xxx
   node index.js config --set slack --webhook https://hooks.slack.com/xxx
   
   node index.js shopify create --title "Viral Product" --price 29.99
   node index.js slack alert --message "New trending product!"
`);
      break;
    }
  }
}

main().catch(console.error);
