/**
 * Financial Status API
 * Reads real financial data from memory files
 */

const fs = require('fs');
const path = require('path');

function getFinancialStatus() {
  try {
    const filePath = path.join(process.env.HOME || '/home/openclaw', '.openclaw/workspace/memory/2026-03-12-financial-status.json');
    
    if (fs.existsSync(filePath)) {
      const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
      return {
        ok: true,
        data: data,
        source: 'financial-status.json'
      };
    }
    
    return {
      ok: false,
      error: 'File not found',
      fallback: {
        bank_balance: 'UNKNOWN',
        daily_revenue: 'UNKNOWN',
        runway_days: 0,
        campaign_status: 'UNKNOWN'
      }
    };
  } catch (err) {
    return {
      ok: false,
      error: err.message,
      fallback: {
        bank_balance: 'ERROR',
        daily_revenue: 'ERROR',
        runway_days: 0
      }
    };
  }
}

module.exports = {
  getFinancialStatus
};
