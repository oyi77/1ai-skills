#!/usr/bin/env node
/**
 * OpenClaw Command Center - Server
 * BerkahKarya / Vilona AI Operations Dashboard
 * 
 * Security: localhost only, no external calls, no secrets in UI
 * Architecture: Pure Node.js, no build step, no npm install required
 * 
 * Usage: node server.js [--port 3337] [--host 127.0.0.1]
 */

'use strict';

const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');
const { exec, execSync, spawn } = require('child_process');
const os = require('os');
const readline = require('readline');

// ─── Config ───────────────────────────────────────────────────────────────────
const DEFAULT_PORT = 3337;
const DEFAULT_HOST = '127.0.0.1';
const WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.join(os.homedir(), '.openclaw', 'workspace');
const SERVER_VERSION = '1.0.0';
const REFRESH_INTERVAL_MS = 5000; // 5s SSE push

// Parse CLI args
const args = process.argv.slice(2);
const PORT = parseInt(args[args.indexOf('--port') + 1] || DEFAULT_PORT, 10);
const HOST = args[args.indexOf('--host') + 1] || DEFAULT_HOST;

// Privacy: topics to hide in screenshot mode
const PRIVATE_TOPICS = [
  'trading', 'credential', 'token', 'password', 'secret', 'api_key',
  'bank', 'finance', 'cashflow', 'salary', 'revenue',
];

// ─── State ────────────────────────────────────────────────────────────────────
let sseClients = [];
let cachedData = {
  sessions: [],
  system: {},
  crons: [],
  llmQuotas: {},
  subagents: [],
  recentLogs: [],
  lastUpdate: null,
};
let screenshotMode = false;

// ─── Utilities ────────────────────────────────────────────────────────────────
function log(msg) {
  const ts = new Date().toISOString().replace('T', ' ').slice(0, 19);
  process.stdout.write(`[${ts}] ${msg}\n`);
}

function safeExec(cmd, opts = {}) {
  return new Promise((resolve) => {
    exec(cmd, { timeout: 10000, ...opts }, (err, stdout, stderr) => {
      if (err) resolve({ ok: false, err: err.message, stdout: '', stderr });
      else resolve({ ok: true, stdout: stdout.trim(), stderr: stderr.trim() });
    });
  });
}

function sanitizeForPrivacy(text) {
  if (!screenshotMode) return text;
  let out = text;
  PRIVATE_TOPICS.forEach(topic => {
    const re = new RegExp(topic, 'gi');
    out = out.replace(re, '***');
  });
  return out;
}

function jsonResponse(res, data, status = 200) {
  const body = JSON.stringify(data, null, 2);
  res.writeHead(status, {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Cache-Control': 'no-cache',
  });
  res.end(body);
}

function sseResponse(res) {
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Access-Control-Allow-Origin': '*',
    'X-Accel-Buffering': 'no',
  });
  res.write('retry: 3000\n\n');
  return res;
}

// ─── System Vitals ────────────────────────────────────────────────────────────
async function getSystemVitals() {
  const vitals = {
    hostname: os.hostname(),
    platform: os.platform(),
    arch: os.arch(),
    uptime: os.uptime(),
    uptimeHuman: formatUptime(os.uptime()),
    loadAvg: os.loadavg(),
    cpuCount: os.cpus().length,
    cpuModel: os.cpus()[0]?.model || 'Unknown',
    memory: {
      total: os.totalmem(),
      free: os.freemem(),
      used: os.totalmem() - os.freemem(),
      usedPct: Math.round(((os.totalmem() - os.freemem()) / os.totalmem()) * 100),
      totalHuman: formatBytes(os.totalmem()),
      freeHuman: formatBytes(os.freemem()),
      usedHuman: formatBytes(os.totalmem() - os.freemem()),
    },
    disk: {},
    nodeVersion: process.version,
    pid: process.pid,
    timestamp: Date.now(),
  };

  // CPU usage via /proc/stat
  try {
    vitals.cpuUsage = await getCpuUsage();
  } catch (e) {
    vitals.cpuUsage = vitals.loadAvg[0] * 10; // fallback estimate
  }

  // Disk usage
  try {
    const diskResult = await safeExec('df -h / --output=size,used,avail,pcent 2>/dev/null | tail -1');
    if (diskResult.ok) {
      const [size, used, avail, pct] = diskResult.stdout.trim().split(/\s+/);
      vitals.disk = { size, used, avail, pct: parseInt(pct, 10) || 0 };
    }
  } catch (e) {}

  // Workspace disk usage
  try {
    const wsResult = await safeExec(`du -sh "${WORKSPACE}" 2>/dev/null`);
    if (wsResult.ok) {
      vitals.workspaceDisk = wsResult.stdout.split('\t')[0];
    }
  } catch (e) {}

  // Network connections count
  try {
    const netResult = await safeExec('ss -tn 2>/dev/null | wc -l');
    if (netResult.ok) vitals.tcpConnections = parseInt(netResult.stdout, 10) || 0;
  } catch (e) {}

  return vitals;
}

function getCpuUsage() {
  return new Promise((resolve, reject) => {
    try {
      const stat1 = readProcStat();
      setTimeout(() => {
        try {
          const stat2 = readProcStat();
          const idle1 = stat1.idle + stat1.iowait;
          const total1 = Object.values(stat1).reduce((a, b) => a + b, 0);
          const idle2 = stat2.idle + stat2.iowait;
          const total2 = Object.values(stat2).reduce((a, b) => a + b, 0);
          const usage = Math.round((1 - (idle2 - idle1) / (total2 - total1)) * 100);
          resolve(Math.max(0, Math.min(100, usage)));
        } catch (e) { reject(e); }
      }, 200);
    } catch (e) { reject(e); }
  });
}

function readProcStat() {
  const line = fs.readFileSync('/proc/stat', 'utf8').split('\n')[0];
  const parts = line.replace('cpu', '').trim().split(/\s+/).map(Number);
  return {
    user: parts[0] || 0, nice: parts[1] || 0, system: parts[2] || 0,
    idle: parts[3] || 0, iowait: parts[4] || 0, irq: parts[5] || 0,
    softirq: parts[6] || 0, steal: parts[7] || 0,
  };
}

function formatBytes(bytes) {
  if (bytes < 1024) return bytes + ' B';
  const units = ['KB', 'MB', 'GB', 'TB'];
  let i = -1, n = bytes;
  while (n >= 1024 && i < units.length - 1) { n /= 1024; i++; }
  return n.toFixed(1) + ' ' + units[i];
}

function formatUptime(secs) {
  const d = Math.floor(secs / 86400);
  const h = Math.floor((secs % 86400) / 3600);
  const m = Math.floor((secs % 3600) / 60);
  const parts = [];
  if (d > 0) parts.push(d + 'd');
  if (h > 0) parts.push(h + 'h');
  parts.push(m + 'm');
  return parts.join(' ');
}

// ─── OpenClaw Sessions ────────────────────────────────────────────────────────
async function getOCLSessions() {
  try {
    // Try openclaw sessions list
    const result = await safeExec('openclaw sessions list --json 2>/dev/null');
    if (result.ok && result.stdout) {
      try {
        const parsed = JSON.parse(result.stdout);
        return Array.isArray(parsed) ? parsed : parsed.sessions || [];
      } catch (e) {}
    }
    
    // Fallback: parse from workspace/memory
    return await getSessionsFromFiles();
  } catch (e) {
    return await getSessionsFromFiles();
  }
}

async function getSessionsFromFiles() {
  // Build session list from memory/log files
  const sessions = [];
  try {
    const today = new Date().toISOString().slice(0, 10);
    const yesterday = new Date(Date.now() - 86400000).toISOString().slice(0, 10);
    
    for (const date of [today, yesterday]) {
      const memFile = path.join(WORKSPACE, 'memory', `${date}.md`);
      if (fs.existsSync(memFile)) {
        const content = fs.readFileSync(memFile, 'utf8');
        const lines = content.split('\n').slice(0, 50);
        sessions.push({
          id: `mem-${date}`,
          label: `Memory ${date}`,
          status: date === today ? 'active' : 'completed',
          channel: 'local',
          model: 'unknown',
          lastUpdate: fs.statSync(memFile).mtime.toISOString(),
          preview: lines.slice(0, 3).join(' ').slice(0, 100),
        });
      }
    }
  } catch (e) {}
  return sessions;
}

async function getSubagents() {
  try {
    const result = await safeExec('openclaw subagents list --json 2>/dev/null');
    if (result.ok && result.stdout) {
      try { return JSON.parse(result.stdout); } catch (e) {}
    }
  } catch (e) {}
  return [];
}

// ─── Cron Jobs ────────────────────────────────────────────────────────────────
async function getCronJobs() {
  const jobs = [];
  
  try {
    // Current user crontab
    const result = await safeExec('crontab -l 2>/dev/null');
    if (result.ok && result.stdout) {
      const lines = result.stdout.split('\n');
      let i = 1;
      for (const line of lines) {
        const trimmed = line.trim();
        if (trimmed && !trimmed.startsWith('#')) {
          const parts = trimmed.split(/\s+/);
          if (parts.length >= 6) {
            const schedule = parts.slice(0, 5).join(' ');
            const command = parts.slice(5).join(' ');
            jobs.push({
              id: `cron-${i++}`,
              schedule,
              command: screenshotMode ? sanitizeForPrivacy(command) : command,
              scheduleHuman: cronToHuman(schedule),
              nextRun: getNextRun(schedule),
              source: 'crontab',
              status: 'active',
            });
          }
        }
      }
    }
  } catch (e) {}

  // Check workspace cron files
  try {
    const cronFile = path.join(WORKSPACE, 'crontab.txt');
    if (fs.existsSync(cronFile)) {
      const content = fs.readFileSync(cronFile, 'utf8');
      const lines = content.split('\n');
      let i = 100;
      for (const line of lines) {
        const trimmed = line.trim();
        if (trimmed && !trimmed.startsWith('#')) {
          const parts = trimmed.split(/\s+/);
          if (parts.length >= 6) {
            const schedule = parts.slice(0, 5).join(' ');
            const command = parts.slice(5).join(' ');
            // Avoid duplicates
            const exists = jobs.some(j => j.command === command);
            if (!exists) {
              jobs.push({
                id: `file-${i++}`,
                schedule,
                command: screenshotMode ? sanitizeForPrivacy(command) : command,
                scheduleHuman: cronToHuman(schedule),
                source: 'workspace/crontab.txt',
                status: 'file',
              });
            }
          }
        }
      }
    }
  } catch (e) {}

  // Check unified_schedule.cron
  try {
    const uFile = path.join(WORKSPACE, 'unified_schedule.cron');
    if (fs.existsSync(uFile)) {
      const content = fs.readFileSync(uFile, 'utf8');
      const lines = content.split('\n');
      for (const line of lines) {
        const trimmed = line.trim();
        if (trimmed && !trimmed.startsWith('#')) {
          const parts = trimmed.split(/\s+/);
          if (parts.length >= 6) {
            const schedule = parts.slice(0, 5).join(' ');
            const command = parts.slice(5).join(' ');
            const exists = jobs.some(j => j.command === command);
            if (!exists) {
              jobs.push({
                id: `unified-${jobs.length}`,
                schedule,
                command: screenshotMode ? sanitizeForPrivacy(command) : command,
                scheduleHuman: cronToHuman(schedule),
                source: 'unified_schedule.cron',
                status: 'file',
              });
            }
          }
        }
      }
    }
  } catch (e) {}

  return jobs;
}

function cronToHuman(expr) {
  const parts = expr.split(/\s+/);
  if (parts.length !== 5) return expr;
  const [min, hour, dom, month, dow] = parts;
  
  if (expr === '* * * * *') return 'Every minute';
  if (min === '*/5' && hour === '*') return 'Every 5 minutes';
  if (min === '*/10' && hour === '*') return 'Every 10 minutes';
  if (min === '*/15' && hour === '*') return 'Every 15 minutes';
  if (min === '*/30' && hour === '*') return 'Every 30 minutes';
  if (hour === '*/2' && min === '0') return 'Every 2 hours';
  if (hour === '*/4' && min === '0') return 'Every 4 hours';
  if (hour === '*/6' && min === '0') return 'Every 6 hours';
  if (hour === '*' && min !== '*') return `Every hour at :${min.padStart(2,'0')}`;
  if (dom === '*' && month === '*' && dow === '*') {
    if (hour !== '*' && min !== '*') return `Daily at ${hour.padStart(2,'0')}:${min.padStart(2,'0')}`;
  }
  if (dow !== '*') {
    const days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
    const day = days[parseInt(dow)] || dow;
    return `Weekly ${day} at ${hour.padStart(2,'0')}:${min.padStart(2,'0')}`;
  }
  return expr;
}

function getNextRun(expr) {
  // Simple next-run estimate
  try {
    const now = new Date();
    const parts = expr.split(/\s+/);
    if (parts[0] === '*/5') return new Date(Math.ceil(now.getTime() / 300000) * 300000).toISOString();
    if (parts[0] === '*/10') return new Date(Math.ceil(now.getTime() / 600000) * 600000).toISOString();
    if (parts[0] === '*/30') return new Date(Math.ceil(now.getTime() / 1800000) * 1800000).toISOString();
    if (parts[1] === '*/2' && parts[0] === '0') {
      const next = new Date(now);
      next.setMinutes(0, 0, 0);
      next.setHours(Math.ceil(now.getHours() / 2) * 2);
      return next.toISOString();
    }
  } catch (e) {}
  return null;
}

// ─── LLM Quotas ───────────────────────────────────────────────────────────────
async function getLLMQuotas() {
  const quotas = {};

  // Check CLAWHUB token
  try {
    const clawToken = path.join(WORKSPACE, 'CLAWHUB_TOKEN.json');
    if (fs.existsSync(clawToken)) {
      const data = JSON.parse(fs.readFileSync(clawToken, 'utf8'));
      quotas.clawhub = {
        name: 'ClawHub',
        status: data.token ? 'configured' : 'missing',
        token: data.token ? '***' + data.token.slice(-4) : null,
      };
    }
  } catch (e) {}

  // Check LLM.md config
  try {
    const llmFile = path.join(WORKSPACE, 'LLM.md');
    if (fs.existsSync(llmFile)) {
      const content = fs.readFileSync(llmFile, 'utf8');
      quotas.llmConfig = {
        name: 'LLM Config',
        status: 'present',
        providers: extractProvidersFromMd(content),
      };
    }
  } catch (e) {}

  // Check config files for API keys (masked)
  try {
    const configDir = path.join(WORKSPACE, 'config');
    if (fs.existsSync(configDir)) {
      const files = fs.readdirSync(configDir);
      quotas.configFiles = files.map(f => ({
        file: f,
        size: fs.statSync(path.join(configDir, f)).size,
      }));
    }
  } catch (e) {}

  // Check OpenClaw config (openclaw.json)
  try {
    const oclConfig = path.join(os.homedir(), '.openclaw', 'openclaw.json');
    if (fs.existsSync(oclConfig)) {
      const data = JSON.parse(fs.readFileSync(oclConfig, 'utf8'));
      const providers = [];
      
      // Parse providers
      const modelProviders = data.models?.providers || {};
      Object.keys(modelProviders).forEach(k => {
        providers.push({
          name: k,
          configured: true,
          model: modelProviders[k]?.baseUrl || '?',
          type: 'provider',
        });
      });
      
      // Parse agent defaults (agents.defaults.model.primary)
      const agentDefaults = data.agents?.defaults || {};
      const modelCfg = agentDefaults.model || {};
      if (modelCfg.primary) {
        quotas.defaultModel = modelCfg.primary;
      }
      if (modelCfg.fallbacks) {
        quotas.fallbackModels = modelCfg.fallbacks.slice(0, 10);
      }
      // All configured models
      const allModels = agentDefaults.models || {};
      quotas.allConfiguredModels = Object.keys(allModels).slice(0, 20);
      
      quotas.openclawModels = providers;
      quotas.openclawAgents = Object.keys(data.agents || {}).filter(k => k !== 'defaults');
    }
    
    // Also check config.json
    const oclConfig2 = path.join(os.homedir(), '.openclaw', 'config.json');
    if (fs.existsSync(oclConfig2)) {
      const data = JSON.parse(fs.readFileSync(oclConfig2, 'utf8'));
      if (!quotas.defaultModel && (data.defaultModel || data.model)) {
        quotas.defaultModel = data.defaultModel || data.model;
      }
    }
  } catch (e) {}

  return quotas;
}

function extractProvidersFromMd(content) {
  const providers = [];
  const lines = content.split('\n');
  for (const line of lines) {
    if (line.includes('anthropic') || line.includes('claude')) providers.push('Anthropic/Claude');
    if (line.includes('openai') || line.includes('gpt')) providers.push('OpenAI/GPT');
    if (line.includes('gemini')) providers.push('Google/Gemini');
    if (line.includes('deepseek')) providers.push('DeepSeek');
    if (line.includes('glm') || line.includes('zhipu')) providers.push('ZhipuAI/GLM');
  }
  return [...new Set(providers)];
}

// ─── Recent Logs ──────────────────────────────────────────────────────────────
async function getRecentLogs() {
  const logs = [];

  // Today's memory file
  try {
    const today = new Date().toISOString().slice(0, 10);
    const memFile = path.join(WORKSPACE, 'memory', `${today}.md`);
    if (fs.existsSync(memFile)) {
      const content = fs.readFileSync(memFile, 'utf8');
      const lines = content.split('\n').filter(l => l.trim()).slice(-20);
      logs.push({
        source: 'daily-memory',
        date: today,
        entries: lines.map(l => screenshotMode ? sanitizeForPrivacy(l) : l),
      });
    }
  } catch (e) {}

  // Workspace logs dir
  try {
    const logsDir = path.join(WORKSPACE, 'logs');
    if (fs.existsSync(logsDir)) {
      const files = fs.readdirSync(logsDir)
        .filter(f => f.endsWith('.log'))
        .map(f => ({
          name: f,
          mtime: fs.statSync(path.join(logsDir, f)).mtime,
          size: fs.statSync(path.join(logsDir, f)).size,
        }))
        .sort((a, b) => b.mtime - a.mtime)
        .slice(0, 5);
      
      for (const file of files) {
        try {
          const content = fs.readFileSync(path.join(logsDir, file.name), 'utf8');
          const lines = content.split('\n').filter(l => l.trim()).slice(-10);
          logs.push({
            source: file.name,
            date: file.mtime.toISOString(),
            size: formatBytes(file.size),
            entries: lines.map(l => screenshotMode ? sanitizeForPrivacy(l) : l),
          });
        } catch (e) {}
      }
    }
  } catch (e) {}

  return logs;
}

// ─── Revenue Stats (from workspace files) ─────────────────────────────────────
async function getRevenueStats() {
  if (screenshotMode) return { hidden: true, reason: 'Privacy mode active' };
  
  const stats = { sources: [], totalEstimate: null };
  
  try {
    // Check cashflow tracker
    const cashFile = path.join(WORKSPACE, 'cashflow_tracker.md');
    if (fs.existsSync(cashFile)) {
      const content = fs.readFileSync(cashFile, 'utf8');
      stats.cashflowPresent = true;
      stats.cashflowSize = formatBytes(fs.statSync(cashFile).size);
      stats.cashflowLastUpdate = fs.statSync(cashFile).mtime.toISOString();
      
      // Extract IDR numbers
      const idrMatches = content.match(/IDR\s*([\d.,]+)/g);
      if (idrMatches) {
        stats.idrMentions = idrMatches.slice(0, 5);
      }
    }
  } catch (e) {}

  try {
    // Check LYNK status
    const lynkFile = path.join(WORKSPACE, 'LYNK_SKILL_CREATED.md');
    if (fs.existsSync(lynkFile)) {
      stats.sources.push({ name: 'LYNK Affiliate', status: 'active', url: 'https://lynk.id/jendralbot' });
    }
  } catch (e) {}

  return stats;
}

// ─── Processes Monitor ────────────────────────────────────────────────────────
async function getRunningProcesses() {
  const procs = [];
  
  try {
    // Python processes in workspace
    const result = await safeExec("ps aux | grep -E '(python|node|openclaw|postbridge)' | grep -v grep | awk '{print $1,$2,$3,$4,$11}' | head -20");
    if (result.ok && result.stdout) {
      result.stdout.split('\n').forEach((line, i) => {
        const parts = line.trim().split(/\s+/);
        if (parts.length >= 5) {
          procs.push({
            id: i,
            user: parts[0],
            pid: parts[1],
            cpu: parts[2] + '%',
            mem: parts[3] + '%',
            cmd: parts.slice(4).join(' ').slice(0, 80),
          });
        }
      });
    }
  } catch (e) {}
  
  return procs;
}

// ─── Data Aggregator ──────────────────────────────────────────────────────────
async function refreshAllData() {
  try {
    const [system, crons, llmQuotas, recentLogs, revenue, processes] = await Promise.all([
      getSystemVitals(),
      getCronJobs(),
      getLLMQuotas(),
      getRecentLogs(),
      getRevenueStats(),
      getRunningProcesses(),
    ]);

    // Sessions are lightweight, do separately
    const sessions = await getOCLSessions();
    const subagents = await getSubagents();

    cachedData = {
      sessions,
      subagents,
      system,
      crons,
      llmQuotas,
      recentLogs,
      revenue,
      processes,
      screenshotMode,
      serverVersion: SERVER_VERSION,
      lastUpdate: new Date().toISOString(),
    };

    return cachedData;
  } catch (e) {
    log('Error refreshing data: ' + e.message);
    return cachedData;
  }
}

// ─── SSE Broadcast ────────────────────────────────────────────────────────────
function broadcastSSE(event, data) {
  const msg = `event: ${event}\ndata: ${JSON.stringify(data)}\n\n`;
  sseClients = sseClients.filter(client => !client.destroyed);
  sseClients.forEach(client => {
    try { client.write(msg); } catch (e) {}
  });
}

// ─── HTTP Router ──────────────────────────────────────────────────────────────
async function handleRequest(req, res) {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const pathname = url.pathname;
  const method = req.method;

  // CORS preflight
  if (method === 'OPTIONS') {
    res.writeHead(204, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST',
      'Access-Control-Allow-Headers': 'Content-Type',
    });
    return res.end();
  }

  // ── SSE Stream ──
  if (pathname === '/events') {
    const client = sseResponse(res);
    sseClients.push(client);
    
    // Send current data immediately
    client.write(`event: init\ndata: ${JSON.stringify(cachedData)}\n\n`);
    
    // Cleanup on disconnect
    req.on('close', () => {
      const idx = sseClients.indexOf(client);
      if (idx !== -1) sseClients.splice(idx, 1);
    });
    return;
  }

  // ── API Routes ──
  if (pathname.startsWith('/api/')) {
    // Unified endpoint
    if (pathname === '/api/all') {
      return jsonResponse(res, await refreshAllData());
    }
    
    if (pathname === '/api/system') {
      return jsonResponse(res, await getSystemVitals());
    }
    
    if (pathname === '/api/sessions') {
      return jsonResponse(res, await getOCLSessions());
    }
    
    if (pathname === '/api/crons') {
      return jsonResponse(res, await getCronJobs());
    }
    
    if (pathname === '/api/quotas') {
      return jsonResponse(res, await getLLMQuotas());
    }
    
    if (pathname === '/api/logs') {
      return jsonResponse(res, await getRecentLogs());
    }
    
    if (pathname === '/api/processes') {
      return jsonResponse(res, await getRunningProcesses());
    }
    
    if (pathname === '/api/revenue') {
      return jsonResponse(res, await getRevenueStats());
    }
    
    if (pathname === '/api/status') {
      return jsonResponse(res, {
        ok: true,
        version: SERVER_VERSION,
        uptime: process.uptime(),
        clients: sseClients.length,
        screenshotMode,
        lastUpdate: cachedData.lastUpdate,
        workspace: WORKSPACE,
      });
    }
    
    // Privacy toggle
    if (pathname === '/api/privacy' && method === 'POST') {
      screenshotMode = !screenshotMode;
      log(`Screenshot/privacy mode: ${screenshotMode ? 'ON' : 'OFF'}`);
      broadcastSSE('privacy', { screenshotMode });
      return jsonResponse(res, { ok: true, screenshotMode });
    }
    
    // Manual refresh
    if (pathname === '/api/refresh' && method === 'POST') {
      const data = await refreshAllData();
      broadcastSSE('refresh', data);
      return jsonResponse(res, { ok: true, lastUpdate: data.lastUpdate });
    }
    
    // Execute openclaw command (safe, read-only)
    if (pathname === '/api/exec' && method === 'POST') {
      let body = '';
      req.on('data', d => body += d);
      req.on('end', async () => {
        try {
          const { cmd } = JSON.parse(body);
          // Whitelist safe commands only
          const allowed = ['openclaw sessions list', 'openclaw subagents list', 'crontab -l'];
          const safe = allowed.some(a => cmd && cmd.startsWith(a));
          if (!safe) {
            return jsonResponse(res, { ok: false, error: 'Command not in whitelist' }, 403);
          }
          const result = await safeExec(cmd);
          return jsonResponse(res, result);
        } catch (e) {
          return jsonResponse(res, { ok: false, error: e.message }, 400);
        }
      });
      return;
    }

    return jsonResponse(res, { ok: false, error: 'Not found' }, 404);
  }

  // ── Dashboard HTML ──
  if (pathname === '/' || pathname === '/index.html') {
    const dashboardFile = path.join(__dirname, 'dashboard.html');
    if (fs.existsSync(dashboardFile)) {
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      return res.end(fs.readFileSync(dashboardFile));
    }
    res.writeHead(404);
    return res.end('Dashboard not found. Run from command-center directory.');
  }

  // ── Static files ──
  if (pathname.endsWith('.css') || pathname.endsWith('.js') || pathname.endsWith('.ico')) {
    const filePath = path.join(__dirname, pathname);
    if (fs.existsSync(filePath)) {
      const ext = path.extname(filePath);
      const mime = { '.css': 'text/css', '.js': 'application/javascript', '.ico': 'image/x-icon' };
      res.writeHead(200, { 'Content-Type': mime[ext] || 'text/plain' });
      return res.end(fs.readFileSync(filePath));
    }
  }

  res.writeHead(404);
  res.end('Not found');
}

// ─── Background Refresh Loop ──────────────────────────────────────────────────
let refreshTimer = null;

function startRefreshLoop() {
  async function tick() {
    const data = await refreshAllData();
    broadcastSSE('update', data);
    refreshTimer = setTimeout(tick, REFRESH_INTERVAL_MS);
  }
  // Initial load
  refreshAllData().then(data => {
    log(`Initial data loaded. Sessions: ${data.sessions?.length || 0}, Crons: ${data.crons?.length || 0}`);
    refreshTimer = setTimeout(tick, REFRESH_INTERVAL_MS);
  });
}

// ─── Main ─────────────────────────────────────────────────────────────────────
const server = http.createServer(handleRequest);

server.listen(PORT, HOST, () => {
  log(`╔══════════════════════════════════════════════════════════╗`);
  log(`║   OpenClaw Command Center v${SERVER_VERSION} — BerkahKarya          ║`);
  log(`╠══════════════════════════════════════════════════════════╣`);
  log(`║   Dashboard: http://${HOST}:${PORT}/                        ║`);
  log(`║   API:       http://${HOST}:${PORT}/api/all                 ║`);
  log(`║   SSE:       http://${HOST}:${PORT}/events                  ║`);
  log(`║   Workspace: ${WORKSPACE.slice(0, 44)}  ║`);
  log(`╚══════════════════════════════════════════════════════════╝`);
  startRefreshLoop();
});

server.on('error', (e) => {
  if (e.code === 'EADDRINUSE') {
    log(`Port ${PORT} in use. Try: node server.js --port 3338`);
    process.exit(1);
  }
  log('Server error: ' + e.message);
});

process.on('SIGINT', () => {
  log('Shutting down...');
  if (refreshTimer) clearTimeout(refreshTimer);
  sseClients.forEach(c => { try { c.end(); } catch (e) {} });
  server.close(() => process.exit(0));
});

process.on('SIGTERM', () => process.emit('SIGINT'));

// ============ FINANCIAL STATUS ENDPOINT ============
// NOTE: Financial API integrated into main request handler (server uses raw http, not express)
// To add: handle '/api/financial' in the main requestListener above
// const { getFinancialStatus } = require('./financial-api.js');
log('[INIT] Command Center ready');
