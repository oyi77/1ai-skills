/**
 * Kalodata Dashboard Module
 * 
 * CLI-based visual reports with ASCII charts, product cards,
 * interactive dashboards, and markdown exports.
 * 
 * Works with ProcessedProduct data from kalodata module.
 */

import { type ProcessedProduct } from '../lib/product-research.js';

// ============================================================================
// Types
// ============================================================================

export interface ChartOptions {
  width?: number;
  height?: number;
  showLabels?: boolean;
  color?: boolean;
  title?: string;
}

export interface DashboardConfig {
  products: ProcessedProduct[];
  title?: string;
  sortBy?: 'revenue' | 'sales' | 'creators' | 'conversionRate' | 'rating';
  limit?: number;
}

// ============================================================================
// ANSI Colors
// ============================================================================

const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
  white: '\x1b[37m',
  gray: '\x1b[90m',
  bold: '\x1b[1m',
};

function supportsColor(): boolean {
  return process.stdout.isTTY && !process.env.NO_COLOR;
}

// ============================================================================
// Chart Rendering Functions
// ============================================================================

/**
 * Render ASCII line chart from revenue trend array
 */
export function renderTrendChart(
  trend: number[],
  options: ChartOptions = {}
): string {
  const { width = 50, height = 10, color = supportsColor() } = options;
  
  if (!trend || trend.length === 0) {
    return 'No trend data available';
  }
  
  const maxVal = Math.max(...trend);
  const minVal = Math.min(...trend);
  const range = maxVal - minVal || 1;
  
  // Sample points to fit width
  const step = Math.max(1, Math.floor(trend.length / width));
  const sampled: number[] = [];
  for (let i = 0; i < trend.length; i += step) {
    sampled.push(trend[i]);
  }
  
  // Add last point if not included
  if (sampled[sampled.length - 1] !== trend[trend.length - 1]) {
    sampled.push(trend[trend.length - 1]);
  }
  
  const chart: string[] = [];
  const filled = color ? colors.cyan : '';
  
  for (let row = height - 1; row >= 0; row--) {
    let line = '';
    const threshold = minVal + (range * row / height);
    let lastWasFilled = false;
    
    for (let i = 0; i < sampled.length; i++) {
      const val = sampled[i];
      if (val >= threshold) {
        // Check if this is a peak
        const prev = sampled[i - 1] ?? val;
        const next = sampled[i + 1] ?? val;
        
        if (val >= prev && val >= next && val > threshold + range / height * 0.5) {
          line += filled + '▲' + colors.reset;
        } else if (val === maxVal && row === height - 1) {
          line += filled + '●' + colors.reset;
        } else {
          line += filled + '█' + colors.reset;
        }
        lastWasFilled = true;
      } else {
        line += ' ';
        lastWasFilled = false;
      }
    }
    chart.push(line);
  }
  
  // Add x-axis labels
  const xAxis = '─'.repeat(Math.min(sampled.length, width));
  chart.push(xAxis);
  
  // Add time labels
  const labels = trend.length > width 
    ? `${formatNumber(trend[0])} → ${formatNumber(trend[trend.length - 1])}`
    : '';
  if (labels) {
    chart.push(`  ${labels}`);
  }
  
  return chart.join('\n');
}

/**
 * Render horizontal bar chart for comparing values
 */
export function renderBarChart(
  data: { label: string; value: number }[],
  options: ChartOptions = {}
): string {
  const { width = 40, color = supportsColor() } = options;
  
  if (!data || data.length === 0) {
    return 'No data available';
  }
  
  const maxValue = Math.max(...data.map(d => d.value));
  const barChar = color ? colors.green + '█' + colors.reset : '█';
  const rows: string[] = [];
  
  for (const item of data) {
    const barLength = Math.round((item.value / maxValue) * width);
    const bar = barChar.repeat(barLength);
    const label = item.label.slice(0, 20).padEnd(20);
    const value = formatNumber(item.value);
    
    rows.push(`${label} │${bar} ${value}`);
  }
  
  return rows.join('\n');
}

/**
 * Render sparkline (single line, no axes)
 */
export function renderSparkline(trend: number[]): string {
  if (!trend || trend.length === 0) return '';
  
  const max = Math.max(...trend);
  const min = Math.min(...trend);
  const range = max - min || 1;
  
  const chars = ' ▁▂▃▄▅▆▇█';
  let sparkline = '';
  
  for (const val of trend) {
    const idx = Math.min(Math.floor(((val - min) / range) * (chars.length - 1)), chars.length - 1);
    sparkline += chars[idx];
  }
  
  return sparkline;
}

/**
 * Render mini trend for product cards
 */
export function renderMiniTrend(trend: number[], width = 30): string {
  if (!trend || trend.length === 0) return '';
  
  const step = Math.max(1, Math.floor(trend.length / width));
  const sampled: number[] = [];
  for (let i = 0; i < trend.length; i += step) {
    sampled.push(trend[i]);
  }
  if (sampled[sampled.length - 1] !== trend[trend.length - 1]) {
    sampled.push(trend[trend.length - 1]);
  }
  
  const max = Math.max(...sampled);
  const min = Math.min(...sampled);
  const range = max - min || 1;
  
  let result = '';
  for (const val of sampled) {
    const pct = (val - min) / range;
    if (pct > 0.8) result += '█';
    else if (pct > 0.6) result += '▓';
    else if (pct > 0.4) result += '▒';
    else if (pct > 0.2) result += '░';
    else result += ' ';
  }
  
  return result;
}

// ============================================================================
// Product Card Functions
// ============================================================================

/**
 * Get trend direction emoji
 */
function getTrendEmoji(direction: 'rising' | 'stable' | 'declining'): string {
  switch (direction) {
    case 'rising': return '📈';
    case 'declining': return '📉';
    default: return '➡️';
  }
}

/**
 * Get trend direction color
 */
function getTrendColor(direction: 'rising' | 'stable' | 'declining'): string {
  switch (direction) {
    case 'rising': return colors.green;
    case 'declining': return colors.red;
    default: return colors.yellow;
  }
}

/**
 * Render a single product card
 */
export function renderProductCard(product: ProcessedProduct, options: { color?: boolean } = {}): string {
  const { color = supportsColor() } = options;
  
  const trendEmoji = getTrendEmoji(product.trendDirection);
  const trendColor = color ? getTrendColor(product.trendDirection) : '';
  const reset = color ? colors.reset : '';
  
  const miniTrend = renderMiniTrend(product.revenueTrend);
  const trendLine = `│ ${trendEmoji} Trend: ${trendColor}${product.trendDirection.toUpperCase()}${reset}`;
  
  const title = product.title.length > 44 
    ? product.title.slice(0, 41) + '...' 
    : product.title;
  
  const lines = [
    '┌──────────────────────────────────────────────┐',
    `│ ${title.padEnd(46)}│`,
    '├──────────────────────────────────────────────┤',
    `│ 💰 Revenue: ${product.revenueFormatted.padEnd(30)}│`,
    `│ 📊 Sales: ${product.sales.toLocaleString().padEnd(15)}│`,
    `│ 👥 Creators: ${product.creators.toString().padEnd(30)}│`,
    `│ ⭐ Rating: ${product.rating.toFixed(1)}`.padEnd(37) + '│',
    `│ 📈 Conversion: ${(product.conversionRate * 100).toFixed(1)}%`.padEnd(32) + '│',
    `│ 🏷️ Commission: ${product.commissionRate.padEnd(30)}│`,
    `│ 📅 Launch: ${product.launchDate.padEnd(33)}│`,
    trendLine.padEnd(48) + '│',
    '├──────────────────────────────────────────────┤',
    `│ ${miniTrend} │`,
    '└──────────────────────────────────────────────┘',
  ];
  
  return lines.join('\n');
}

/**
 * Render multiple product cards in a grid
 */
export function renderProductGrid(products: ProcessedProduct[], columns = 2): string {
  if (products.length === 0) return 'No products to display';
  
  const cards = products.map(p => renderProductCard(p).split('\n'));
  const maxRows = Math.max(...cards.map(c => c.length));
  
  const grid: string[] = [];
  
  for (let row = 0; row < maxRows; row++) {
    let line = '';
    for (let col = 0; col < columns; col++) {
      const cardIndex = col;
      if (cardIndex < cards.length) {
        const cell = cards[col][row] || '';
        line += cell.padEnd(48) + '  ';
      }
    }
    grid.push(line);
  }
  
  return grid.join('\n');
}

// ============================================================================
// Table Rendering
// ============================================================================

/**
 * Render a data table
 */
export function renderTable(
  products: ProcessedProduct[],
  columns: (keyof ProcessedProduct)[] = ['title', 'revenueFormatted', 'sales', 'creators', 'rating']
): string {
  if (products.length === 0) return 'No data';
  
  const headers: Record<string, string> = {
    title: 'Product',
    revenueFormatted: 'Revenue',
    sales: 'Sales',
    creators: 'Creators',
    conversionRate: 'Conv %',
    rating: 'Rating',
    commissionRate: 'Commission',
    launchDate: 'Launch',
    trendDirection: 'Trend',
  };
  
  const colWidths: Record<string, number> = {};
  for (const col of columns) {
    const header = headers[col] || col;
    colWidths[col] = Math.max(
      header.length,
      ...products.map(p => String(p[col as keyof ProcessedProduct] || '').length)
    );
  }
  
  // Header
  let headerLine = '│';
  for (const col of columns) {
    const header = headers[col] || col;
    headerLine += ' ' + header.padEnd(colWidths[col]) + ' │';
  }
  
  const separator = '─'.repeat(headerLine.length - 2);
  const topBorder = '┌' + separator.replace(/─/g, '─').split('').join('─') + '┐';
  const midBorder = '├' + separator.replace(/─/g, '─').split('').join('─') + '┤';
  const botBorder = '└' + separator.replace(/─/g, '─').split('').join('─') + '┘';
  
  const rows: string[] = [topBorder, headerLine, midBorder];
  
  for (const product of products) {
    let row = '│';
    for (const col of columns) {
      let val = String(product[col as keyof ProcessedProduct] || '');
      
      // Format specific columns
      if (col === 'conversionRate') {
        val = (product.conversionRate * 100).toFixed(1) + '%';
      }
      if (col === 'title') {
        val = val.length > colWidths[col] - 1 ? val.slice(0, colWidths[col] - 4) + '...' : val;
      }
      
      row += ' ' + val.padEnd(colWidths[col]) + ' │';
    }
    rows.push(row);
  }
  
  rows.push(botBorder);
  
  return rows.join('\n');
}

// ============================================================================
// Summary Statistics
// ============================================================================

/**
 * Calculate summary statistics
 */
export function calculateSummary(products: ProcessedProduct[]): {
  totalRevenue: number;
  totalSales: number;
  avgConversion: number;
  avgRating: number;
  topCategory: string;
  risingCount: number;
  decliningCount: number;
} {
  const totalRevenue = products.reduce((sum, p) => sum + p.revenue, 0);
  const totalSales = products.reduce((sum, p) => sum + p.sales, 0);
  const avgConversion = products.reduce((sum, p) => sum + p.conversionRate, 0) / products.length;
  const avgRating = products.reduce((sum, p) => sum + p.rating, 0) / products.length;
  
  const trendCounts = products.reduce((acc, p) => {
    acc[p.trendDirection] = (acc[p.trendDirection] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);
  
  return {
    totalRevenue,
    totalSales,
    avgConversion,
    avgRating,
    topCategory: 'Fashion', // Would need category data
    risingCount: trendCounts.rising || 0,
    decliningCount: trendCounts.declining || 0,
  };
}

/**
 * Render summary box
 */
export function renderSummary(products: ProcessedProduct[]): string {
  const stats = calculateSummary(products);
  const color = supportsColor();
  
  const lines = [
    '┌──────────────────────────────────────────────┐',
    '│              📊 SUMMARY STATISTICS           │',
    '├──────────────────────────────────────────────┤',
    `│ 💰 Total Revenue: ${formatCurrency(stats.totalRevenue).padEnd(27)}│`,
    `│ 📦 Total Sales: ${stats.totalSales.toLocaleString().padEnd(30)}│`,
    `│ 📈 Avg Conversion: ${(stats.avgConversion * 100).toFixed(1)}%`.padEnd(29) + '│',
    `│ ⭐ Avg Rating: ${stats.avgRating.toFixed(2)}`.padEnd(33) + '│',
    `│ 📈 Rising: ${color ? colors.green : ''}${stats.risingCount}${color ? colors.reset : ''}  │`,
    `│ 📉 Declining: ${color ? colors.red : ''}${stats.decliningCount}${color ? colors.reset : ''}`.padEnd(32) + '│',
    '└──────────────────────────────────────────────┘',
  ];
  
  return lines.join('\n');
}

// ============================================================================
// Dashboard Rendering
// ============================================================================

/**
 * Render full dashboard
 */
export function renderDashboard(config: DashboardConfig): string {
  const { 
    products, 
    title = '📊 KALODATA DASHBOARD',
    sortBy = 'revenue',
    limit = 10 
  } = config;
  
  // Sort products
  const sorted = [...products].sort((a, b) => {
    switch (sortBy) {
      case 'revenue': return b.revenue - a.revenue;
      case 'sales': return b.sales - a.sales;
      case 'creators': return b.creators - a.creators;
      case 'conversionRate': return b.conversionRate - a.conversionRate;
      case 'rating': return b.rating - a.rating;
      default: return 0;
    }
  }).slice(0, limit);
  
  const sections: string[] = [];
  
  // Title
  sections.push(`\n${title}\n${'='.repeat(46)}\n`);
  
  // Summary
  sections.push(renderSummary(sorted));
  sections.push('');
  
  // Top Products Table
  sections.push('Top Products by ' + sortBy + ':\n');
  sections.push(renderTable(sorted, [
    'title', 
    'revenueFormatted', 
    'sales', 
    'creators',
    'trendDirection'
  ]));
  sections.push('');
  
  // Product Cards (top 3)
  sections.push('Top 3 Product Details:\n');
  sections.push(renderProductGrid(sorted.slice(0, 3)));
  
  return sections.join('\n');
}

// ============================================================================
// Markdown Export
// ============================================================================

/**
 * Export products to markdown format
 */
export function exportToMarkdown(
  products: ProcessedProduct[],
  options: { title?: string; includeCards?: boolean } = {}
): string {
  const { title = 'Kalodata Product Report', includeCards = true } = options;
  
  const stats = calculateSummary(products);
  const date = new Date().toISOString().split('T')[0];
  
  let md = `# ${title}\n\n`;
  md += `**Generated:** ${date}\n`;
  md += `**Products:** ${products.length}\n\n`;
  
  // Summary
  md += `## Summary\n\n`;
  md += `| Metric | Value |\n`;
  md += `|--------|-------|\n`;
  md += `| Total Revenue | ${formatCurrency(stats.totalRevenue)} |\n`;
  md += `| Total Sales | ${stats.totalSales.toLocaleString()} |\n`;
  md += `| Avg Conversion | ${(stats.avgConversion * 100).toFixed(1)}% |\n`;
  md += `| Avg Rating | ${stats.avgRating.toFixed(1)} |\n`;
  md += `| Rising Trends | ${stats.risingCount} |\n`;
  md += `| Declining Trends | ${stats.decliningCount} |\n\n`;
  
  // Products table
  md += `## Products\n\n`;
  md += `| # | Product | Revenue | Sales | Creators | Rating | Trend |\n`;
  md += `|---|---------|---------|-------|----------|--------|-------|\n`;
  
  products.slice(0, 20).forEach((p, i) => {
    const productName = p.title.length > 30 ? p.title.slice(0, 27) + '...' : p.title;
    md += `| ${i + 1} | ${productName} | ${p.revenueFormatted} | ${p.sales.toLocaleString()} | ${p.creators} | ${p.rating} | ${p.trendDirection} |\n`;
  });
  
  // Detailed cards
  if (includeCards) {
    md += `\n## Product Details\n\n`;
    
    products.slice(0, 10).forEach((p, i) => {
      md += `### ${i + 1}. ${p.title}\n\n`;
      md += `- **Revenue:** ${p.revenueFormatted}\n`;
      md += `- **Sales:** ${p.sales.toLocaleString()}\n`;
      md += `- **Creators:** ${p.creators}\n`;
      md += `- **Rating:** ${p.rating}\n`;
      md += `- **Commission:** ${p.commissionRate}\n`;
      md += `- **Launch Date:** ${p.launchDate}\n`;
      md += `- **Trend:** ${p.trendDirection}\n`;
      md += `- **Price Range:** ${p.price.formatted}\n\n`;
    });
  }
  
  return md;
}

/**
 * Save markdown to file
 */
export async function saveMarkdown(
  products: ProcessedProduct[],
  filePath: string,
  options?: { title?: string; includeCards?: boolean }
): Promise<void> {
  const md = exportToMarkdown(products, options);
  
  // Using dynamic import for ES modules
  const { writeFile } = await import('fs/promises');
  await writeFile(filePath, md, 'utf-8');
}

// ============================================================================
// Utility Functions
// ============================================================================

/**
 * Format number with locale
 */
export function formatNumber(num: number): string {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M';
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K';
  }
  return num.toFixed(0);
}

/**
 * Format currency (IDR)
 */
export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}

// ============================================================================
// Interactive Dashboard (Stub - requires readline)
// ============================================================================

/**
 * Interactive dashboard - requires terminal input
 * Note: Full implementation would use readline for key handling
 */
export async function runInteractiveDashboard(
  products: ProcessedProduct[]
): Promise<void> {
  console.clear();
  console.log(renderDashboard({ products, limit: products.length }));
  
  console.log('\nPress Enter to exit...');
  
  // Simple wait for enter
  const readline = await import('readline');
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  
  await new Promise<void>(resolve => {
    rl.question('', () => {
      rl.close();
      resolve();
    });
  });
}

// ============================================================================
// Main Export
// ============================================================================

export default {
  renderTrendChart,
  renderBarChart,
  renderSparkline,
  renderMiniTrend,
  renderProductCard,
  renderProductGrid,
  renderTable,
  renderSummary,
  renderDashboard,
  exportToMarkdown,
  saveMarkdown,
  formatNumber,
  formatCurrency,
  runInteractiveDashboard,
};
