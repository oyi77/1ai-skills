#!/usr/bin/env node
'use strict';

/**
 * Session-start hooks health detection.
 * Silent when healthy. Prints suggestion when hooks missing/outdated/removed.
 *
 * Called by hooks/session-start.sh at end of session start.
 */

const fs = require('fs');
const path = require('path');

const HOME = process.env.HOME || process.env.USERPROFILE;
const PKG_ROOT = path.resolve(__dirname, '..');
const SETTINGS_FILE = path.join(HOME, '.claude', 'settings.json');
const VERSION_FILE = path.join(HOME, '.1ai-skills', '.hooks-version');

function getPackageVersion() {
  try {
    return require(path.join(PKG_ROOT, 'package.json')).version;
  } catch {
    return null;
  }
}

function check() {
  // Check 1: Version stamp exists?
  if (!fs.existsSync(VERSION_FILE)) {
    console.log('[1ai-skills] Hooks not installed. Say "install hooks" or run: node scripts/hooks-tui.js');
    return;
  }

  // Check 2: Version matches?
  const installed = fs.readFileSync(VERSION_FILE, 'utf8').trim();
  const current = getPackageVersion();
  if (current && installed !== current) {
    console.log(`[1ai-skills] Hooks outdated (${installed} -> ${current}). Say "setup hooks" or run: node scripts/hooks-tui.js`);
    return;
  }

  // Check 3: Settings.json still has our hooks?
  try {
    const settings = JSON.parse(fs.readFileSync(SETTINGS_FILE, 'utf8'));
    const settingsStr = JSON.stringify(settings);
    if (!settingsStr.includes('skill-tracker')) {
      console.log('[1ai-skills] Hooks removed from settings. Say "install hooks" or run: node scripts/hooks-tui.js');
      return;
    }
  } catch {
    // Can't read settings — don't spam, just skip
    return;
  }

  // All healthy — silent
}

check();
