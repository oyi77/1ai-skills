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
        timeout: def.type === 'PostToolUse' && def.matcher === 'Write|Edit' ? 35 : 5
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
    const config = {
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
      evolve_enabled: true
    };
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2) + '\n');
    console.log('[1ai-skills] Created evolve-config.json');
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
}

install();
