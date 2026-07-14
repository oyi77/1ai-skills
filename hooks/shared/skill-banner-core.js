#!/usr/bin/env node
'use strict';

/**
 * skill-banner-core.js — Shared core for 1ai-skills activation banner.
 *
 * Provides skill resolution (SKILLS.json index + filesystem fallback),
 * ANSI banner builder, dedup tracking, and URI helpers.
 *
 * Used by:
 *   - Claude Code hook  (hooks/auto-evolve/skill-banner.js)
 *   - OMP hook          (hooks/auto-evolve/skill-banner-omp.js)
 *   - OpenCode plugin   (hooks/auto-evolve/skill-banner-opencode.ts)
 */

const fs = require('fs');
const path = require('path');

const HOME = process.env.HOME || process.env.USERPROFILE;

// ── Dedup ─────────────────────────────────────────────────────────────────

const welcomed = new Set();

exports.isAlreadyWelcomed = function (name) {
  if (welcomed.has(name)) return true;
  welcomed.add(name);
  return false;
};

// ── Skill resolution via SKILLS.json index ────────────────────────────────

function findSkillsJson() {
  const candidates = [
    path.join(HOME, 'projects', '1ai-skills', 'SKILLS.json'),
    path.join(HOME, '.1ai-skills', 'repo', 'SKILLS.json'),
  ];
  return candidates.find(function (p) { return fs.existsSync(p); }) || null;
}

function loadIndex() {
  var p = findSkillsJson();
  if (!p) return null;
  try { return JSON.parse(fs.readFileSync(p, 'utf-8')); }
  catch { return null; }
}

function lookupInIndex(name, index) {
  if (!index || !index.skills) return null;
  return index.skills.find(function (s) { return s.name === name; }) || null;
}

// ── Skill resolution via filesystem (SKILL.md frontmatter) ────────────────

var SEARCH_DIRS = null;

function getSearchDirs() {
  if (SEARCH_DIRS) return SEARCH_DIRS;
  var roots = [
    path.join(HOME, 'projects', '1ai-skills'),
    path.join(HOME, '.1ai-skills', 'repo'),
  ];
  var cats = [
    'agents', 'automation', 'content', 'core', 'cybersecurity', 'data',
    'development', 'devops', 'financial', 'integrations', 'marketing', 'mcp',
    'meta', 'mindset', 'operations', 'productivity', 'research', 'sales', 'trading',
  ];
  var dirs = [];
  for (var ri = 0; ri < roots.length; ri++) {
    for (var ci = 0; ci < cats.length; ci++) {
      dirs.push(path.join(roots[ri], cats[ci]));
    }
  }
  dirs.push(path.join(HOME, '.claude', 'skills'));
  dirs.push(path.join(HOME, '.claude', 'plugins', 'marketplaces', 'omc', 'skills'));
  SEARCH_DIRS = dirs;
  return dirs;
}

function findSkillMd(name) {
  var dirs = getSearchDirs();

  // Flat lookup: category/name/SKILL.md
  for (var i = 0; i < dirs.length; i++) {
    var f = path.join(dirs[i], name, 'SKILL.md');
    if (fs.existsSync(f)) return f;
  }

  // Recursive lookup (subdirectory nesting)
  for (var j = 0; j < dirs.length; j++) {
    var d = dirs[j];
    if (!fs.existsSync(d)) continue;
    try {
      var found = walkDir(d, name, 0);
      if (found) return found;
    } catch {}
  }
  return null;
}

function walkDir(dir, name, depth) {
  if (depth > 3) return null;
  var entries;
  try { entries = fs.readdirSync(dir, { withFileTypes: true }); }
  catch { return null; }
  for (var i = 0; i < entries.length; i++) {
    var e = entries[i];
    if (!e.isDirectory()) continue;
    var p = path.join(dir, e.name);
    if (e.name === name && fs.existsSync(path.join(p, 'SKILL.md'))) return path.join(p, 'SKILL.md');
    var r = walkDir(p, name, depth + 1);
    if (r) return r;
  }
  return null;
}

function parseFM(content) {
  var m = content.match(/^---\n([\s\S]*?)\n---/);
  if (!m) return {};
  var y = m[1], meta = {}, x;
  if ((x = y.match(/^name:\s*(.+)$/m))) meta.name = x[1].trim();
  if ((x = y.match(/^description:\s*(.+)$/m))) meta.description = x[1].trim();
  if ((x = y.match(/^domain:\s*(.+)$/m))) meta.domain = x[1].trim();
  if ((x = y.match(/^tags:\s*\n((?:\s*-\s*.+\n?)+)/m)))
    meta.tags = x[1].split('\n').map(function (l) { return l.replace(/^\s*-\s*/, '').trim(); }).filter(Boolean);
  var wM = content.match(/## When to Use\s*\n([\s\S]*?)(?=\n## )/);
  if (wM)
    meta.whenToUse = wM[1].split('\n').filter(function (l) { return l.match(/^\s*-\s+/); }).slice(0, 3)
      .map(function (l) { return l.replace(/^\s*-\s*/, '').trim(); });
  return meta;
}

exports.resolveSkillMeta = function (name) {
  // Try SKILLS.json first (fast)
  var index = loadIndex();
  if (index) {
    var meta = lookupInIndex(name, index);
    if (meta) return meta;
  }
  // Fallback: filesystem SKILL.md frontmatter
  var mdPath = findSkillMd(name);
  if (mdPath) {
    try { return parseFM(fs.readFileSync(mdPath, 'utf-8')); }
    catch {}
  }
  return null;
};

// ── URI helpers ───────────────────────────────────────────────────────────

exports.skillNameFromUri = function (uri) {
  var m = uri.match(/^skill:\/\/(.+)/);
  if (!m) return null;
  return m[1].split('/')[0];
};

// ── Filesystem path detection (hooks receive resolved paths) ───────────

var SKILL_BASES = null;

function findSkillBase() {
  if (SKILL_BASES) return SKILL_BASES;
  var candidates = [
    path.join(HOME, '.agents', 'skills'),
    path.join(HOME, '.opencode', 'skills'),
    path.join(HOME, '.claude', 'skills'),
    path.join(HOME, '.claude', 'plugins', 'marketplaces', 'omc', 'skills'),
  ];
  SKILL_BASES = [];
  for (var i = 0; i < candidates.length; i++) {
    if (fs.existsSync(candidates[i])) SKILL_BASES.push(candidates[i]);
  }
  return SKILL_BASES;
}

exports.skillNameFromPath = function (inputPath) {
  if (typeof inputPath !== 'string') return null;
  // Handle skill:// URIs too (belt-and-suspenders)
  if (inputPath.startsWith('skill://')) {
    return exports.skillNameFromUri(inputPath);
  }
  var bases = findSkillBase();
  for (var i = 0; i < bases.length; i++) {
    var base = bases[i];
    var prefix = base + '/';
    if (inputPath.startsWith(prefix)) {
      var rel = inputPath.slice(prefix.length).split('/')[0];
      if (rel && rel.length > 0 && !rel.startsWith('.')) return rel;
    }
  }
  return null;
};

// ── ANSI constants ────────────────────────────────────────────────────────

var R = '\x1b[0m', B = '\x1b[1m', D = '\x1b[2m';
var CN = '\x1b[36m', GN = '\x1b[32m', YL = '\x1b[33m', MG = '\x1b[35m';
var W = 56; // inner box width

function vw(s) {
  var t = s.replace(/\x1b\[[0-9;]*m/g, '');
  var w = 0;
  for (var i = 0; i < t.length; i++) {
    var c = t.charCodeAt(i);
    w += (c >= 0x1F000 && c <= 0x1FFFF) || (c >= 0x2600 && c <= 0x27BF) ||
         (c >= 0x2300 && c <= 0x23FF) || (c >= 0x4E00 && c <= 0x9FFF) ||
         (c >= 0x3000 && c <= 0x30FF) ? 2 : 1;
  }
  return w;
}

function pad(s, n) { return s + ' '.repeat(Math.max(0, n - vw(s))); }

function center(s, width) {
  var diff = Math.max(0, width - vw(s));
  return ' '.repeat(Math.floor(diff / 2)) + s;
}

function wrap(text, max) {
  if (!text) return [];
  var words = text.split(' '), lines = [], cur = '';
  for (var i = 0; i < words.length; i++) {
    var w = words[i];
    var t = cur ? cur + ' ' + w : w;
    if (vw(t) > max && cur) { lines.push(cur); cur = w; } else cur = t;
  }
  if (cur) lines.push(cur);
  return lines;
}

function row(text) {
  return CN + '║' + R + ' ' + pad(text, W - 1) + CN + '║' + R;
}

// ── Banner builder ────────────────────────────────────────────────────────

exports.buildBanner = function (skillName, meta) {
  var name = (meta && meta.name) || skillName;
  var domain = (meta && meta.domain) || 'general';
  var desc = (meta && meta.description) || 'No description available.';
  var tags = (meta && meta.tags) || [];
  tags = tags.slice(0, 3);
  var triggers = (meta && meta.whenToUse) || [];

  var art = [
    ' ___   ___ ___    _ _  __ ___',
    '|_  ) / __|_  )  (_) |/  |_  )',
    ' / /  \\__ \\/ /   | |   <  / /',
    '/___| |___/___|  |_|_|\\_\\/___|',
    '              S K I L L S     ',
  ];

  var L = [];
  L.push(CN + '╔' + '═'.repeat(W) + '╗' + R);
  for (var ai = 0; ai < art.length; ai++) L.push(row(MG + art[ai] + R));
  L.push(CN + '╠' + '═'.repeat(W) + '╣' + R);

  var act = B + YL + '⚡ ' + name + ' ACTIVATED!' + R;
  L.push(CN + '║' + R + ' ' + pad(center(act, W - 1), W - 1) + CN + '║' + R);

  L.push(CN + '╠' + '─'.repeat(W) + '╣' + R);

  L.push(row(B + 'Domain:' + R + '  ' + GN + '📂 ' + domain + R));
  if (tags.length) L.push(row(B + 'Tags:' + R + '    ' + D + '🏷️  ' + tags.join(', ') + R));

  L.push(CN + '╠' + '─'.repeat(W) + '╣' + R);

  L.push(row(B + 'Summary:' + R));
  var descLines = wrap(desc, W - 6).slice(0, 3);
  for (var di = 0; di < descLines.length; di++)
    L.push(row('  ' + CN + '▸ ' + descLines[di] + R));

  if (triggers.length) {
    L.push(CN + '╠' + '─'.repeat(W) + '╣' + R);
    L.push(row(B + 'Triggers:' + R));
    for (var ti = 0; ti < triggers.length; ti++)
      L.push(row('  ' + YL + '▸ ' + triggers[ti] + R));
  }

  L.push(CN + '╚' + '═'.repeat(W) + '╝' + R);
  return L.join('\n');
};
