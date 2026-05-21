#!/usr/bin/env node
'use strict';

/**
 * 1ai-skills Hooks Onboarding TUI
 * Interactive guided setup with status display and config questions.
 *
 * Usage:
 *   node scripts/hooks-tui.js           # interactive mode
 *   node scripts/hooks-tui.js --yes     # non-interactive, accept all defaults
 *   node scripts/hooks-tui.js --status  # status only, no prompts
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const HOME = process.env.HOME || process.env.USERPROFILE;
const PKG_ROOT = path.resolve(__dirname, '..');
const CLAUDE_DIR = path.join(HOME, '.claude');
const CLAUDE_HOOKS_DIR = path.join(CLAUDE_DIR, 'hooks');
const SETTINGS_FILE = path.join(CLAUDE_DIR, 'settings.json');
const METRICS_DIR = path.join(HOME, '.1ai-skills');
const VERSION_FILE = path.join(METRICS_DIR, '.hooks-version');
const CONFIG_FILE = path.join(METRICS_DIR, 'evolve-config.json');

const HOOK_SCRIPTS = [
  'skill-tracker.js',
  'skill-evolver.js',
  'skill-committer.js',
  'skill-feedback-capture.js'
];

// --- Colors (ANSI, safe for all terminals) ---

const c = {
  reset: '\x1b[0m',
  bold: '\x1b[1m',
  dim: '\x1b[2m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  red: '\x1b[31m',
  cyan: '\x1b[36m',
  white: '\x1b[37m',
  bgGreen: '\x1b[42m',
  bgYellow: '\x1b[43m',
  bgRed: '\x1b[41m',
};

function colorize(color, text) {
  if (!process.stdout.isTTY) return text;
  return `${color}${text}${c.reset}`;
}

// --- Box drawing ---

function box(lines, width) {
  const w = width || Math.max(...lines.map(l => stripAnsi(l).length)) + 4;
  const top = `\u256d${'─'.repeat(w)}\u256e`;
  const bot = `\u2570${'─'.repeat(w)}\u256f`;
  const padded = lines.map(l => {
    const visible = stripAnsi(l);
    const pad = Math.max(0, w - visible.length - 2);
    return `\u2502 ${l}${' '.repeat(pad)}\u2502`;
  });
  return [top, ...padded, bot].join('\n');
}

function stripAnsi(str) {
  return str.replace(/\x1b\[[0-9;]*m/g, '');
}

// --- Status check ---

function getHookStatus() {
  const status = {
    versionStamp: null,
    packageVersion: null,
    upToDate: false,
    hookEntries: 0,
    scriptsOnDisk: 0,
    configExists: false,
    metricsSize: {},
  };

  // Version stamp
  if (fs.existsSync(VERSION_FILE)) {
    status.versionStamp = fs.readFileSync(VERSION_FILE, 'utf8').trim();
  }

  // Package version
  try {
    status.packageVersion = require(path.join(PKG_ROOT, 'package.json')).version;
  } catch {}

  status.upToDate = status.versionStamp === status.packageVersion;

  // Hook entries
  try {
    const settings = JSON.parse(fs.readFileSync(SETTINGS_FILE, 'utf8'));
    if (settings.hooks) {
      for (const entries of Object.values(settings.hooks)) {
        if (!Array.isArray(entries)) continue;
        status.hookEntries += entries.filter(e =>
          e.hooks && e.hooks.some(h =>
            h.command && (
              h.command.includes('skill-tracker') ||
              h.command.includes('skill-evolver') ||
              h.command.includes('skill-committer') ||
              h.command.includes('skill-feedback-capture')
            )
          )
        ).length;
      }
    }
  } catch {}

  // Scripts on disk
  for (const script of HOOK_SCRIPTS) {
    if (fs.existsSync(path.join(CLAUDE_HOOKS_DIR, script))) status.scriptsOnDisk++;
  }

  // Config
  status.configExists = fs.existsSync(CONFIG_FILE);

  // Metrics
  for (const f of ['metrics.jsonl', 'feedback.jsonl']) {
    const fp = path.join(METRICS_DIR, f);
    if (fs.existsSync(fp)) {
      status.metricsSize[f] = fs.statSync(fp).size;
    }
  }

  return status;
}

function loadConfig() {
  if (!fs.existsSync(CONFIG_FILE)) {
    return {
      min_invocations: 5,
      success_threshold: 70,
      evolve_cooldown_hours: 24,
      max_evolves_per_run: 3,
      auto_push: false,
      target_repo: '',
      skill_dirs: [path.join(HOME, '.claude', 'skills')],
      repo_dir: PKG_ROOT,
      commit_prefix: 'evolve',
      tracking_enabled: true,
      evolve_enabled: true,
    };
  }
  try { return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8')); }
  catch { return {}; }
}

function saveConfig(config) {
  if (!fs.existsSync(METRICS_DIR)) fs.mkdirSync(METRICS_DIR, { recursive: true });
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2) + '\n');
}

// --- Display ---

function renderStatus(status) {
  const lines = [];

  lines.push(colorize(c.bold + c.cyan, '  1ai-skills Hooks'));

  // Version
  if (status.versionStamp) {
    const icon = status.upToDate
      ? colorize(c.green, '\u2713')
      : colorize(c.yellow, '!');
    const verText = status.upToDate
      ? colorize(c.green, `${status.versionStamp} (up to date)`)
      : colorize(c.yellow, `${status.versionStamp} -> ${status.packageVersion} (outdated)`);
    lines.push(`  ${icon} Version: ${verText}`);
  } else {
    lines.push(`  ${colorize(c.red, '\u2717')} Version: ${colorize(c.red, 'not installed')}`);
  }

  // Hook entries
  const entryIcon = status.hookEntries >= 4
    ? colorize(c.green, '\u2713')
    : colorize(c.yellow, '!');
  lines.push(`  ${entryIcon} Hooks:   ${status.hookEntries} entries in settings.json`);

  // Scripts
  const scriptIcon = status.scriptsOnDisk >= 4
    ? colorize(c.green, '\u2713')
    : colorize(c.yellow, '!');
  lines.push(`  ${scriptIcon} Scripts: ${status.scriptsOnDisk}/${HOOK_SCRIPTS.length} on disk`);

  // Config
  const configIcon = status.configExists
    ? colorize(c.green, '\u2713')
    : colorize(c.yellow, '!');
  lines.push(`  ${configIcon} Config:  ${status.configExists ? 'present' : 'missing'}`);

  // Metrics
  const metricsTotal = Object.values(status.metricsSize).reduce((a, b) => a + b, 0);
  if (metricsTotal > 0) {
    lines.push(`  ${colorize(c.dim, '\u2022')} Metrics: ${formatBytes(metricsTotal)}`);
  }

  console.log(box(lines, 52));
}

function formatBytes(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function renderConfig(config) {
  const lines = [];
  lines.push(colorize(c.bold + c.cyan, '  Evolve Config'));
  lines.push(`  ${colorize(c.dim, 'auto_push:')}           ${config.auto_push ? colorize(c.green, 'on') : colorize(c.dim, 'off')}`);
  lines.push(`  ${colorize(c.dim, 'target_repo:')}         ${config.target_repo || colorize(c.dim, '(not set)')}`);
  lines.push(`  ${colorize(c.dim, 'success_threshold:')}   ${config.success_threshold}%`);
  lines.push(`  ${colorize(c.dim, 'min_invocations:')}     ${config.min_invocations}`);
  lines.push(`  ${colorize(c.dim, 'cooldown:')}            ${config.evolve_cooldown_hours}h`);
  lines.push(`  ${colorize(c.dim, 'tracking:')}            ${config.tracking_enabled ? colorize(c.green, 'on') : colorize(c.red, 'off')}`);
  lines.push(`  ${colorize(c.dim, 'evolve:')}              ${config.evolve_enabled ? colorize(c.green, 'on') : colorize(c.red, 'off')}`);
  console.log(box(lines, 52));
}

// --- Interactive prompts ---

function ask(rl, question, defaultVal) {
  return new Promise(resolve => {
    const suffix = defaultVal !== undefined ? ` ${colorize(c.dim, `[${defaultVal}]`)} ` : ' ';
    rl.question(`${colorize(c.cyan, '?')} ${question}${suffix}`, answer => {
      resolve(answer.trim() || defaultVal);
    });
  });
}

function confirm(rl, question, defaultYes) {
  return new Promise(resolve => {
    const hint = defaultYes ? 'Y/n' : 'y/N';
    rl.question(`${colorize(c.cyan, '?')} ${question} ${colorize(c.dim, `[${hint}]`)} `, answer => {
      const a = answer.trim().toLowerCase();
      if (a === '') resolve(defaultYes);
      else resolve(a === 'y' || a === 'yes');
    });
  });
}

async function interactiveSetup(rl) {
  const config = loadConfig();

  console.log();
  console.log(colorize(c.bold, '  Auto-Evolve Configuration'));
  console.log(colorize(c.dim, '  Skills below success threshold get auto-improved.'));
  console.log();

  // Auto-push
  config.auto_push = await confirm(rl, 'Auto-push evolved skills to GitHub?', config.auto_push);

  if (config.auto_push) {
    config.target_repo = await ask(rl, 'Target repo (e.g. oyi77/1ai-skills):', config.target_repo || '');
  }

  // Thresholds
  const threshold = await ask(rl, 'Success threshold % (skills below this get evolved):', String(config.success_threshold));
  config.success_threshold = parseInt(threshold, 10) || 70;

  const minInv = await ask(rl, 'Min invocations before evolving:', String(config.min_invocations));
  config.min_invocations = parseInt(minInv, 10) || 5;

  const cooldown = await ask(rl, 'Cooldown between evolve cycles (hours):', String(config.evolve_cooldown_hours));
  config.evolve_cooldown_hours = parseInt(cooldown, 10) || 24;

  // Toggle features
  config.tracking_enabled = await confirm(rl, 'Enable skill tracking?', config.tracking_enabled);
  config.evolve_enabled = await confirm(rl, 'Enable auto-evolution?', config.evolve_enabled);

  return config;
}

// --- Main ---

async function main() {
  const args = process.argv.slice(2);
  const isYes = args.includes('--yes') || args.includes('-y');
  const isStatus = args.includes('--status');

  const status = getHookStatus();

  console.log();
  renderStatus(status);

  if (isStatus) {
    if (status.configExists) {
      console.log();
      renderConfig(loadConfig());
    }
    console.log();
    return;
  }

  // Check if needs install
  const needsInstall = !status.versionStamp || !status.upToDate || status.scriptsOnDisk < 4;

  if (needsInstall) {
    console.log();
    const doInstall = isYes || await new Promise(resolve => {
      const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
      confirm(rl, 'Install hooks now?', true).then(r => { rl.close(); resolve(r); });
    });

    if (doInstall) {
      console.log();
      require('./install-hooks.js');
      console.log();
    } else {
      console.log(colorize(c.dim, '  Skipped. Run `npm run hooks install` later.'));
      console.log();
      return;
    }
  }

  // Config questions (interactive only)
  if (!isYes) {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

    console.log();
    const configure = await confirm(rl, 'Configure auto-evolve settings?', false);

    if (configure) {
      const config = await interactiveSetup(rl);
      saveConfig(config);
      console.log();
      console.log(colorize(c.green, '  \u2713 Config saved.'));
      console.log();
      renderConfig(config);
    }

    rl.close();
  }

  console.log();
  console.log(colorize(c.dim, '  Commands:'));
  console.log(colorize(c.dim, '    npm run hooks status    — view status'));
  console.log(colorize(c.dim, '    npm run hooks install   — reinstall hooks'));
  console.log(colorize(c.dim, '    npm run hooks uninstall — remove hooks'));
  console.log();
}

main().catch(err => {
  console.error(`[1ai-skills] Error: ${err.message}`);
  process.exit(1);
});
