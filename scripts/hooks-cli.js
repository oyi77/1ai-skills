#!/usr/bin/env node
'use strict';

/**
 * 1ai-skills Hooks CLI
 * Commands: install, uninstall, status
 *
 * Usage: node scripts/hooks-cli.js <command>
 *        npm run hooks -- <command>
 *        npx 1ai-skills-hooks <command>
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const HOME = process.env.HOME || process.env.USERPROFILE;
const PKG_ROOT = path.resolve(__dirname, '..');
const CLAUDE_HOOKS_DIR = path.join(HOME, '.claude', 'hooks');
const SETTINGS_FILE = path.join(HOME, '.claude', 'settings.json');
const METRICS_DIR = path.join(HOME, '.1ai-skills');
const VERSION_FILE = path.join(METRICS_DIR, '.hooks-version');

const HOOK_SCRIPTS = [
  'skill-tracker.js',
  'skill-evolver.js',
  'skill-committer.js',
  'skill-feedback-capture.js'
];

function loadSettings() {
  if (!fs.existsSync(SETTINGS_FILE)) return {};
  try { return JSON.parse(fs.readFileSync(SETTINGS_FILE, 'utf8')); }
  catch { return {}; }
}

function saveSettings(settings) {
  const dir = path.dirname(SETTINGS_FILE);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(SETTINGS_FILE, JSON.stringify(settings, null, 2) + '\n');
}

// --- Commands ---

function cmdInstall() {
  const installer = path.join(__dirname, 'install-hooks.js');
  execSync(`node "${installer}"`, { stdio: 'inherit' });
}

function cmdUninstall() {
  console.log('[1ai-skills] Uninstalling hooks...');

  // 1. Remove hook entries from settings.json
  const settings = loadSettings();
  let removed = 0;

  if (settings.hooks) {
    for (const [hookType, entries] of Object.entries(settings.hooks)) {
      if (!Array.isArray(entries)) continue;
      const before = entries.length;
      settings.hooks[hookType] = entries.filter(e => {
        if (!e.hooks) return true;
        return !e.hooks.some(h =>
          h.command && (
            h.command.includes('skill-tracker') ||
            h.command.includes('skill-evolver') ||
            h.command.includes('skill-committer') ||
            h.command.includes('skill-feedback-capture')
          )
        );
      });
      removed += before - settings.hooks[hookType].length;
      if (settings.hooks[hookType].length === 0) {
        delete settings.hooks[hookType];
      }
    }
  }

  if (removed > 0) {
    saveSettings(settings);
    console.log(`[1ai-skills] Removed ${removed} hook entry/entries from settings.json`);
  } else {
    console.log('[1ai-skills] No hook entries found in settings.json');
  }

  // 2. Remove copied hook scripts
  for (const script of HOOK_SCRIPTS) {
    const fp = path.join(CLAUDE_HOOKS_DIR, script);
    if (fs.existsSync(fp)) {
      fs.unlinkSync(fp);
      console.log(`[1ai-skills] Removed ${script}`);
    }
  }

  // 3. Remove version stamp
  if (fs.existsSync(VERSION_FILE)) {
    fs.unlinkSync(VERSION_FILE);
    console.log('[1ai-skills] Removed version stamp');
  }

  console.log('[1ai-skills] Hooks uninstalled');
}

function cmdStatus() {
  console.log('[1ai-skills] Hooks Status');
  console.log('='.repeat(40));

  // Version stamp
  if (fs.existsSync(VERSION_FILE)) {
    const installed = fs.readFileSync(VERSION_FILE, 'utf8').trim();
    const current = require(path.join(PKG_ROOT, 'package.json')).version;
    const upToDate = installed === current;
    console.log(`Installed version: ${installed}`);
    console.log(`Package version:   ${current}`);
    console.log(`Status:            ${upToDate ? 'Up to date' : 'OUTDATED — run: node scripts/install-hooks.js'}`);
  } else {
    console.log('Installed version: NOT INSTALLED');
    console.log('Run: node scripts/install-hooks.js');
  }

  // Hook entries in settings.json
  const settings = loadSettings();
  let hookCount = 0;
  if (settings.hooks) {
    for (const entries of Object.values(settings.hooks)) {
      if (!Array.isArray(entries)) continue;
      hookCount += entries.filter(e =>
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
  console.log(`Hook entries:      ${hookCount} in settings.json`);

  // Hook scripts on disk
  let scriptsOnDisk = 0;
  for (const script of HOOK_SCRIPTS) {
    if (fs.existsSync(path.join(CLAUDE_HOOKS_DIR, script))) scriptsOnDisk++;
  }
  console.log(`Scripts on disk:   ${scriptsOnDisk}/${HOOK_SCRIPTS.length} in ${CLAUDE_HOOKS_DIR}`);

  // Config
  const configPath = path.join(METRICS_DIR, 'evolve-config.json');
  console.log(`Config:            ${fs.existsSync(configPath) ? 'Present' : 'Missing'}`);

  // Metrics
  for (const f of ['metrics.jsonl', 'feedback.jsonl']) {
    const fp = path.join(METRICS_DIR, f);
    if (fs.existsSync(fp)) {
      const size = fs.statSync(fp).size;
      console.log(`${f}:   ${size} bytes`);
    }
  }
}

// --- Main ---

function cmdSetup() {
  const tui = path.join(__dirname, 'hooks-tui.js');
  execSync(`node "${tui}"`, { stdio: 'inherit' });
}

// --- Main ---

const cmd = process.argv[2];
switch (cmd) {
  case 'install':
    cmdInstall();
    break;
  case 'uninstall':
    cmdUninstall();
    break;
  case 'status':
    cmdStatus();
    break;
  case 'setup':
    cmdSetup();
    break;
  default:
    console.log('Usage: node scripts/hooks-cli.js <install|uninstall|status|setup>');
    process.exit(1);
}
