#!/usr/bin/env node
/**
 * 1ai-evolve — Universal skill evolution daemon
 * Works with: Claude Code, OpenClaw, OpenCode, Hermes, any AI assistant
 *
 * Usage:
 *   1ai-evolve start          # Start file watcher + HTTP API
 *   1ai-evolve stop           # Stop daemon
 *   1ai-evolve track <skill> [success|fail] [tokens]
 *   1ai-evolve feedback <skill> <message>
 *   1ai-evolve status         # Show skill stats
 *   1ai-evolve evolve         # Run evolution cycle now
 *   1ai-evolve install        # Install as systemd service
 *
 * API (when daemon running):
 *   POST http://localhost:9847/track   {skill, success, tokens}
 *   POST http://localhost:9847/feedback {skill, message}
 *   GET  http://localhost:9847/stats
 *   GET  http://localhost:9847/stats/:skill
 */

const fs = require('fs');
const path = require('path');
const http = require('http');
const { execSync } = require('child_process');

const METRICS_DIR = path.join(process.env.HOME, '.1ai-skills');
const CONFIG_FILE = path.join(METRICS_DIR, 'evolve-config.json');
const METRICS_FILE = path.join(METRICS_DIR, 'metrics.jsonl');
const FEEDBACK_FILE = path.join(METRICS_DIR, 'feedback.jsonl');
const STATS_FILE = path.join(METRICS_DIR, 'stats.json');
const PID_FILE = path.join(METRICS_DIR, '.daemon.pid');
const LOG_FILE = path.join(METRICS_DIR, 'daemon.log');
const PORT = 9847;

const FEEDBACK_SIGNALS = [
  'don\'t do', 'stop doing', 'never', 'always', 'instead of',
  'wrong', 'incorrect', 'fix this', 'change this', 'no not',
  'better', 'good', 'perfect', 'nice', 'great', 'exactly',
  'that\'s it', 'yes', 'correct', 'right', 'do this instead',
  'prefer', 'want', 'need', 'should', 'must', 'make it',
  'next time', 'from now on', 'always do', 'remember',
];

// Ensure dirs
if (!fs.existsSync(METRICS_DIR)) fs.mkdirSync(METRICS_DIR, { recursive: true });

function loadConfig() {
  const defaults = {
    min_invocations: 5,
    success_threshold: 70,
    evolve_cooldown_hours: 24,
    max_evolves_per_run: 3,
    auto_push: false,
    target_repo: '',
    skill_dirs: [path.join(process.env.HOME, '.claude', 'skills')],
    repo_dir: '',
    commit_prefix: 'evolve',
    watch_enabled: true,
    api_enabled: true,
  };
  try { return { ...defaults, ...JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8')) }; }
  catch (e) { return defaults; }
}

function loadStats() {
  try { return JSON.parse(fs.readFileSync(STATS_FILE, 'utf8')); }
  catch (e) { return {}; }
}

function saveStats(stats) {
  fs.writeFileSync(STATS_FILE, JSON.stringify(stats, null, 2));
}

function log(msg) {
  const line = `[${new Date().toISOString()}] ${msg}\n`;
  fs.appendFileSync(LOG_FILE, line);
  if (process.argv[2] !== 'start') process.stdout.write(line);
}

// === TRACK ===
function trackSkill(skill, success, tokens = 0, source = 'cli') {
  const entry = {
    ts: new Date().toISOString(),
    skill,
    success: success !== 'fail',
    tokens: parseInt(tokens) || 0,
    source,
  };
  fs.appendFileSync(METRICS_FILE, JSON.stringify(entry) + '\n');

  const stats = loadStats();
  if (!stats[skill]) {
    stats[skill] = { invocations: 0, successes: 0, failures: 0, total_tokens: 0, feedback_count: 0, first_seen: entry.ts };
  }
  const s = stats[skill];
  s.invocations++;
  if (entry.success) s.successes++; else s.failures++;
  s.total_tokens += entry.tokens;
  s.last_seen = entry.ts;
  s.success_rate = Math.round((s.successes / s.invocations) * 100);
  s.avg_tokens = Math.round(s.total_tokens / s.invocations);
  saveStats(stats);

  return { tracked: true, skill, success_rate: s.success_rate };
}

// === FEEDBACK ===
function captureFeedback(skill, message) {
  const lower = message.toLowerCase();
  const signals = FEEDBACK_SIGNALS.filter(s => lower.includes(s));
  if (signals.length === 0) return { captured: false, reason: 'no feedback signals detected' };

  const entry = {
    ts: new Date().toISOString(),
    skill,
    signals,
    insight: message.slice(0, 500),
  };
  fs.appendFileSync(FEEDBACK_FILE, JSON.stringify(entry) + '\n');

  const stats = loadStats();
  if (stats[skill]) {
    stats[skill].feedback_count = (stats[skill].feedback_count || 0) + 1;
    stats[skill].last_feedback = entry.ts;
    saveStats(stats);
  }

  return { captured: true, skill, signals };
}

// === EVOLVE ===
function runEvolve() {
  const config = loadConfig();
  const stats = loadStats();
  const evolved = [];

  for (const [skill, data] of Object.entries(stats)) {
    if (data.invocations < config.min_invocations) continue;
    if (data.success_rate >= config.success_threshold) continue;

    const skillDir = findSkillDir(skill, config.skill_dirs);
    if (!skillDir) continue;

    const feedback = loadFeedback(skill);
    const entry = {
      ts: new Date().toISOString(),
      skill,
      action: 'evolve_triggered',
      success_rate: data.success_rate,
      feedback_count: feedback.length,
      skill_path: skillDir,
    };

    const queueFile = path.join(METRICS_DIR, 'evolve-queue.jsonl');
    fs.appendFileSync(queueFile, JSON.stringify(entry) + '\n');
    evolved.push({ skill, success_rate: data.success_rate, feedback: feedback.length });
  }

  return { evolved };
}

function findSkillDir(skillName, dirs) {
  for (const dir of dirs) {
    const p = path.join(dir, skillName, 'SKILL.md');
    if (fs.existsSync(p)) return p;
  }
  return null;
}

function loadFeedback(skill) {
  try {
    return fs.readFileSync(FEEDBACK_FILE, 'utf8').trim().split('\n')
      .map(l => { try { return JSON.parse(l); } catch { return null; } })
      .filter(e => e && e.skill === skill);
  }
  catch (e) { return []; }
}

// === FILE WATCHER ===
function startWatcher(config) {
  if (!config.watch_enabled) return;

  const watchDirs = config.skill_dirs.filter(d => fs.existsSync(d));
  for (const dir of watchDirs) {
    try {
      fs.watch(dir, { recursive: true }, (eventType, filename) => {
        if (!filename || (!filename.endsWith('.md') && !filename.endsWith('.json'))) return;
        log(`File changed: ${filename} (${eventType})`);
        // Auto-commit if repo configured
        if (config.repo_dir && config.auto_push) {
          autoCommit(config);
        }
      });
      log(`Watching: ${dir}`);
    } catch (e) {
      log(`Watch error on ${dir}: ${e.message}`);
    }
  }
}

function autoCommit(config) {
  try {
    execSync(`cd "${config.repo_dir}" && git add -A`, { timeout: 5000 });
    const status = execSync(`cd "${config.repo_dir}" && git status --porcelain`, { timeout: 5000 }).toString().trim();
    if (!status) return;

    const timestamp = new Date().toISOString().slice(0, 19).replace('T', ' ');
    execSync(`cd "${config.repo_dir}" && git commit -m "${config.commit_prefix}: auto-evolve [${timestamp}]"`, { timeout: 10000 });
    execSync(`cd "${config.repo_dir}" && git push origin main --force-with-lease 2>&1 || git push origin HEAD 2>&1`, { timeout: 30000 });
    log('Auto-committed and pushed');
  } catch (e) {
    log(`Auto-commit error: ${e.message.slice(0, 200)}`);
  }
}

// === HTTP API ===
function startAPI() {
  const server = http.createServer((req, res) => {
    const url = new URL(req.url, `http://localhost:${PORT}`);

    if (req.method === 'POST' && url.pathname === '/track') {
      let body = '';
      req.on('data', c => body += c);
      req.on('end', () => {
        try {
          const { skill, success, tokens } = JSON.parse(body);
          const result = trackSkill(skill, success, tokens, 'api');
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify(result));
        } catch (e) {
          res.writeHead(400); res.end(JSON.stringify({ error: e.message }));
        }
      });
      return;
    }

    if (req.method === 'POST' && url.pathname === '/feedback') {
      let body = '';
      req.on('data', c => body += c);
      req.on('end', () => {
        try {
          const { skill, message } = JSON.parse(body);
          const result = captureFeedback(skill, message);
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify(result));
        } catch (e) {
          res.writeHead(400); res.end(JSON.stringify({ error: e.message }));
        }
      });
      return;
    }

    if (req.method === 'GET' && url.pathname === '/stats') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(loadStats()));
      return;
    }

    if (req.method === 'GET' && url.pathname.startsWith('/stats/')) {
      const skill = url.pathname.split('/')[2];
      const stats = loadStats();
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(stats[skill] || { error: 'not found' }));
      return;
    }

    res.writeHead(404); res.end('Not found');
  });

  server.listen(PORT, '127.0.0.1', () => {
    log(`API listening on http://127.0.0.1:${PORT}`);
  });
}

// === CLI ===
const cmd = process.argv[2];
const args = process.argv.slice(3);

switch (cmd) {
  case 'track':
    if (!args[0]) { console.error('Usage: 1ai-evolve track <skill> [success|fail] [tokens]'); process.exit(1); }
    console.log(JSON.stringify(trackSkill(args[0], args[1] || 'success', args[2])));
    break;

  case 'feedback':
    if (!args[0] || !args[1]) { console.error('Usage: 1ai-evolve feedback <skill> <message>'); process.exit(1); }
    console.log(JSON.stringify(captureFeedback(args[0], args.slice(1).join(' '))));
    break;

  case 'stats':
    const stats = loadStats();
    if (args[0]) {
      console.log(JSON.stringify(stats[args[0]] || { error: 'not found' }, null, 2));
    } else {
      console.log(JSON.stringify(stats, null, 2));
    }
    break;

  case 'evolve':
    console.log(JSON.stringify(runEvolve(), null, 2));
    break;

  case 'start':
    const config = loadConfig();
    log('Daemon starting...');
    startWatcher(config);
    startAPI();
    fs.writeFileSync(PID_FILE, process.pid.toString());
    log(`PID: ${process.pid}`);
    // Keep alive
    process.on('SIGTERM', () => { log('Daemon stopping'); fs.unlinkSync(PID_FILE); process.exit(0); });
    break;

  case 'stop':
    try {
      const pid = fs.readFileSync(PID_FILE, 'utf8').trim();
      process.kill(parseInt(pid), 'SIGTERM');
      fs.unlinkSync(PID_FILE);
      console.log(`Stopped daemon (PID ${pid})`);
    } catch (e) {
      console.log('No daemon running');
    }
    break;

  case 'install':
    console.log('Installing as systemd service...');
    const service = `[Unit]
Description=1ai-skills Auto-Evolve Daemon
After=network.target

[Service]
Type=simple
ExecStart=${process.execPath} ${path.resolve(__filename)} start
Restart=on-failure
RestartSec=10
User=${process.env.USER}

[Install]
WantedBy=default.target`;
    const servicePath = path.join(process.env.HOME, '.config', 'systemd', 'user', '1ai-evolve.service');
    fs.mkdirSync(path.dirname(servicePath), { recursive: true });
    fs.writeFileSync(servicePath, service);
    try { execSync('systemctl --user daemon-reload', { timeout: 5000 }); } catch {}
    try { execSync('systemctl --user enable 1ai-evolve', { timeout: 5000 }); } catch {}
    try { execSync('systemctl --user start 1ai-evolve', { timeout: 5000 }); } catch {}
    console.log('✅ Service installed and started');
    console.log(`   Config: ${CONFIG_FILE}`);
    console.log(`   Logs: ${LOG_FILE}`);
    console.log(`   API: http://127.0.0.1:${PORT}`);
    break;

  default:
    console.log(`
1ai-evolve — Universal skill evolution daemon

Commands:
  start                    Start daemon (file watcher + API)
  stop                     Stop daemon
  track <skill> [s|f] [t]  Track skill invocation
  feedback <skill> <msg>   Capture feedback
  status                   Show all skill stats
  evolve                   Run evolution cycle
  install                  Install as systemd service

API (when daemon running):
  POST /track    {"skill":"name","success":true,"tokens":100}
  POST /feedback {"skill":"name","message":"always do X"}
  GET  /stats
  GET  /stats/:skill

Works with: Claude Code, OpenClaw, OpenCode, Hermes, any AI assistant
`);
}
