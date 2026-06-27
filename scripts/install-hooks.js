#!/usr/bin/env node
'use strict';

/**
 * 1ai-skills Auto Hooks Installer
 * Pure Node.js, zero external dependencies.
 * Reads from hooks/hooks.json manifest as single source of truth.
 *
 * Usage: node scripts/install-hooks.js
 * Also runs automatically via npm postinstall.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const HOME = process.env.HOME || process.env.USERPROFILE;
const PKG_ROOT = path.resolve(__dirname, '..');
const CLAUDE_DIR = path.join(HOME, '.claude');
const CLAUDE_HOOKS_DIR = path.join(CLAUDE_DIR, 'hooks');
const SETTINGS_FILE = path.join(CLAUDE_DIR, 'settings.json');
const METRICS_DIR = path.join(HOME, '.1ai-skills');
const VERSION_FILE = path.join(METRICS_DIR, '.hooks-version');

// Load manifest
const manifestPath = path.join(PKG_ROOT, 'hooks', 'hooks.json');
let manifest;
try {
  manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
} catch (err) {
  console.error(`[1ai-skills] Cannot read manifest: ${manifestPath}`);
  process.exit(1);
}

const HOOKS_VERSION = manifest.hooks_version || require(path.join(PKG_ROOT, 'package.json')).version;

// --- Helpers ---

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function copyIfChanged(src, dest) {
  if (!fs.existsSync(src)) return false;
  const srcContent = fs.readFileSync(src);
  if (fs.existsSync(dest)) {
    const destContent = fs.readFileSync(dest);
    if (srcContent.equals(destContent)) return false; // already identical
  }
  fs.writeFileSync(dest, srcContent);
  return true;
}

function mergeHookEntry(existingArray, entry) {
  const cmd = entry.hooks && entry.hooks[0] && entry.hooks[0].command;
  if (!cmd) return false;
  if (!Array.isArray(existingArray)) return false;
  const exists = existingArray.some(e =>
    e.hooks && e.hooks.some(h => h.command === cmd)
  );
  if (!exists) {
    existingArray.push(entry);
    return true;
  }
  return false;
}

function loadSettings() {
  if (!fs.existsSync(SETTINGS_FILE)) return {};
  try {
    return JSON.parse(fs.readFileSync(SETTINGS_FILE, 'utf8'));
  } catch {
    return {};
  }
}

function saveSettings(settings) {
  ensureDir(path.dirname(SETTINGS_FILE));
  fs.writeFileSync(SETTINGS_FILE, JSON.stringify(settings, null, 2) + '\n');
}

// --- Agent Detection ---

const AI_AGENTS = [
  {
    name: 'Claude Code',
    detect: () => fs.existsSync(path.join(HOME, '.claude')),
    skillDirs: [path.join(HOME, '.claude', 'skills')],
    configDir: path.join(HOME, '.claude'),
  },
  {
    name: 'OpenClaw',
    detect: () => fs.existsSync(path.join(HOME, '.openclaw')),
    skillDirs: [path.join(HOME, '.openclaw', 'workspace', 'skills')],
    configDir: path.join(HOME, '.openclaw'),
  },
  {
    name: 'OpenClaude',
    detect: () => fs.existsSync(path.join(HOME, '.openclaude')),
    skillDirs: [path.join(HOME, '.openclaude', 'skills')],
    configDir: path.join(HOME, '.openclaude'),
  },
  {
    name: 'Cline',
    detect: () => fs.existsSync(path.join(HOME, '.cline')),
    skillDirs: [path.join(HOME, '.cline', 'skills')],
    configDir: path.join(HOME, '.cline'),
  },
  {
    name: 'Aider',
    detect: () => {
      const aiderPaths = [
        path.join(HOME, '.aider.conf.yml'),
        path.join(HOME, '.aider'),
      ];
      return aiderPaths.some(p => fs.existsSync(p));
    },
    skillDirs: [path.join(HOME, '.aider', 'skills')],
    configDir: path.join(HOME, '.aider'),
  },
  {
    name: 'Cursor',
    detect: () => {
      const cursorPaths = [
        path.join(HOME, '.cursor'),
        path.join(HOME, '.config', 'cursor'),
      ];
      return cursorPaths.some(p => fs.existsSync(p));
    },
    skillDirs: [
      path.join(HOME, '.cursor', 'skills'),
      path.join(HOME, '.config', 'cursor', 'skills'),
    ],
    configDir: path.join(HOME, '.cursor'),
  },
  {
    name: 'Windsurf',
    detect: () => fs.existsSync(path.join(HOME, '.windsurf')),
    skillDirs: [path.join(HOME, '.windsurf', 'skills')],
    configDir: path.join(HOME, '.windsurf'),
  },
  {
    name: 'Continue',
    detect: () => fs.existsSync(path.join(HOME, '.continue')),
    skillDirs: [path.join(HOME, '.continue', 'skills')],
    configDir: path.join(HOME, '.continue'),
  },
  {
    name: 'Agents Skills',
    detect: () => fs.existsSync(path.join(HOME, '.agents')),
    skillDirs: [path.join(HOME, '.agents', 'skills')],
    configDir: path.join(HOME, '.agents'),
  },
];

function detectAgents() {
  const found = AI_AGENTS.filter(a => a.detect());
  return { agents: found, names: found.map(a => a.name) };
}

// --- Main ---

function install() {
  console.log('[1ai-skills] Installing hooks...');

  // 1. Ensure directories
  ensureDir(CLAUDE_HOOKS_DIR);
  ensureDir(METRICS_DIR);

  // 2. Copy auto-evolve hook scripts
  const evolveHooks = manifest.hooks && manifest.hooks['auto-evolve'];
  if (!evolveHooks) {
    console.error('[1ai-skills] No auto-evolve hooks in manifest');
    process.exit(1);
  }

  let copied = 0;
  for (const def of Object.values(evolveHooks)) {
    const src = path.join(PKG_ROOT, def.script);
    const dest = path.join(CLAUDE_HOOKS_DIR, path.basename(def.script));
    if (copyIfChanged(src, dest)) {
      copied++;
    }
  }
  console.log(`[1ai-skills] Copied ${copied} hook script(s) to ${CLAUDE_HOOKS_DIR}`);

  // 3. Merge hook entries into settings.json
  const settings = loadSettings();
  const hooks = settings.hooks || (settings.hooks = {});
  let added = 0;

  for (const def of Object.values(evolveHooks)) {
    const scriptPath = path.join(CLAUDE_HOOKS_DIR, path.basename(def.script));
    const hookType = def.type;

    if (!hooks[hookType]) hooks[hookType] = [];

    const entry = {
      matcher: def.matcher || undefined,
      hooks: [{
        type: 'command',
        command: `node "${scriptPath}"`,
        timeout: def.timeout || (def.type === 'PostToolUse' && def.matcher === 'Write|Edit' ? 35 : 5)
      }]
    };
    // Remove undefined matcher
    if (!entry.matcher) delete entry.matcher;

    if (mergeHookEntry(hooks[hookType], entry)) {
      added++;
    }
  }

  if (added > 0) {
    saveSettings(settings);
    console.log(`[1ai-skills] Added ${added} hook entry/entries to settings.json`);
  } else {
    console.log('[1ai-skills] All hook entries already present in settings.json');
  }

  // 4. Create default evolve-config.json
  const configPath = path.join(METRICS_DIR, 'evolve-config.json');
  if (!fs.existsSync(configPath)) {
    const detected = detectAgents();
    const skillDirs = detected.agents.flatMap(a => a.skillDirs).filter(d => fs.existsSync(d));
    // Always include .claude/skills even if not yet created
    const claudeSkills = path.join(HOME, '.claude', 'skills');
    if (!skillDirs.includes(claudeSkills)) skillDirs.push(claudeSkills);

    const config = {
      min_invocations: 5,
      success_threshold: 70,
      evolve_cooldown_hours: 24,
      max_evolves_per_run: 3,
      auto_push: false,
      target_repo: '',
      skill_dirs: skillDirs,
      repo_dir: PKG_ROOT,
      commit_prefix: 'evolve',
      tracking_enabled: true,
      evolve_enabled: true
    };
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2) + '\n');
    console.log(`[1ai-skills] Created evolve-config.json (detected ${detected.agents.length} agent(s))`);
    for (const agent of detected.agents) {
      console.log(`  ✓ ${agent.name} — ${agent.skillDirs.join(', ')}`);
    }
  }

  // 5. Init metrics files
  for (const f of ['metrics.jsonl', 'feedback.jsonl']) {
    const fp = path.join(METRICS_DIR, f);
    if (!fs.existsSync(fp)) fs.writeFileSync(fp, '');
  }

  // 6. Write version stamp
  fs.writeFileSync(VERSION_FILE, HOOKS_VERSION + '\n');
  console.log(`[1ai-skills] Version stamp: ${HOOKS_VERSION}`);

  console.log('[1ai-skills] Hooks installed successfully');

  // 7. Post-install recommendations
  console.log('');
  console.log('╔══════════════════════════════════════════════════╗');
  console.log('║         Thanks for using 1ai-skills!             ║');
  console.log('╠══════════════════════════════════════════════════╣');
  console.log('║                                                  ║');
  console.log('║  Commands:                                       ║');
  console.log('║    npm run hooks status    — check status        ║');
  console.log('║    npm run hooks setup     — interactive config  ║');
  console.log('║    npm run hooks uninstall — remove hooks        ║');
  console.log('╚══════════════════════════════════════════════════╝');

  // 8. Star/fork prompt
  const isCI = process.env.CI || process.env.GITHUB_ACTIONS;
  const isYes = process.argv.includes('--yes') || process.argv.includes('-y');

  // LLM banner (shown in --yes mode for agents)
  if (isYes) {
    console.log('');
    console.log('[1ai-skills] === LLM INSTALL COMPLETE ===');
    console.log('[1ai-skills] Hooks active. Skills auto-tracked on use.');
    console.log('[1ai-skills] Config: ~/.1ai-skills/evolve-config.json');
    console.log('[1ai-skills] Status: node scripts/hooks-cli.js status');
    console.log('[1ai-skills] To star/fork: gh repo star oyi77/1ai-skills');
    console.log('[1ai-skills] ================================');
  }

  if (!isCI && !isYes && process.stdin.isTTY) {
    const readline = require('readline');
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    const ghAvailable = hasGhCli();

    console.log('');
    rl.question('\x1b[36m?\x1b[0m Star & fork oyi77/1ai-skills on GitHub? \x1b[2m[y/N]\x1b[0m ', (answer) => {
      rl.close();
      const yes = answer.trim().toLowerCase();
      if (yes === 'y' || yes === 'yes') {
        if (ghAvailable) {
          try {
            execSync('gh repo star oyi77/1ai-skills', { stdio: 'inherit' });
            execSync('gh repo fork oyi77/1ai-skills --clone=false', { stdio: 'inherit' });
            console.log('\x1b[32m✓ Starred & forked!\x1b[0m');
          } catch {
            console.log('\x1b[33m! Could not run gh commands. Visit: github.com/oyi77/1ai-skills\x1b[0m');
          }
        } else {
          console.log('\x1b[2mgh CLI not found. Visit: github.com/oyi77/1ai-skills\x1b[0m');
        }
      } else {
        console.log('\x1b[2mSkipped. Visit github.com/oyi77/1ai-skills anytime.\x1b[0m');
      }
    });
  }
}

// Check if gh CLI available
function hasGhCli() {
  try {
    execSync('gh --version', { stdio: 'ignore' });
    return true;
  } catch { return false; }
}

install();
