#!/usr/bin/env node
'use strict';

/**
 * skill-banner.js — PostToolUse hook
 * Displays an ASCII art activation banner when a 1ai-skill is loaded.
 * Input: JSON on stdin with tool_name, tool_input, tool_output, etc.
 */

const fs = require('fs');
const path = require('path');

const HOME = process.env.HOME || process.env.USERPROFILE;

// ANSI
const R = '\x1b[0m', B = '\x1b[1m', D = '\x1b[2m';
const CN = '\x1b[36m', GN = '\x1b[32m', YL = '\x1b[33m', MG = '\x1b[35m';

const W = 56; // inner width

// --- Skill resolution ---

function getCategoryDirs() {
  const roots = [path.join(HOME, 'projects', '1ai-skills'), path.join(HOME, '.1ai-skills', 'repo')];
  const cats = ['agents','automation','content','core','cybersecurity','data','development','devops',
    'financial','integrations','marketing','mcp','meta','mindset','operations','productivity','research','sales','trading'];
  const d = [];
  for (const r of roots) for (const c of cats) d.push(path.join(r, c));
  return d;
}

const SEARCH = [...getCategoryDirs(), path.join(HOME, '.claude', 'skills'),
  path.join(HOME, '.claude', 'plugins', 'marketplaces', 'omc', 'skills')];

function findSkill(n) {
  // 1. Flat lookup (category/name)
  for (const d of SEARCH) { const f = path.join(d, n, 'SKILL.md'); if (fs.existsSync(f)) return f; }
  // 2. Recursive lookup (category/subdir/name)
  for (const d of SEARCH) {
    if (!fs.existsSync(d)) continue;
    try {
      const walk = (dir, depth) => {
        if (depth > 3) return null;
        for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
          if (!e.isDirectory()) continue;
          const p = path.join(dir, e.name);
          if (e.name === n && fs.existsSync(path.join(p, 'SKILL.md'))) return path.join(p, 'SKILL.md');
          const r = walk(p, depth + 1);
          if (r) return r;
        }
        return null;
      };
      const found = walk(d, 0);
      if (found) return found;
    } catch {}
  }
  return null;
}

function parseFM(content) {
  const m = content.match(/^---\n([\s\S]*?)\n---/);
  if (!m) return {};
  const y = m[1], meta = {};
  let x;
  if ((x = y.match(/^name:\s*(.+)$/m))) meta.name = x[1].trim();
  if ((x = y.match(/^description:\s*(.+)$/m))) meta.description = x[1].trim();
  if ((x = y.match(/^domain:\s*(.+)$/m))) meta.domain = x[1].trim();
  if ((x = y.match(/^tags:\s*\n((?:\s*-\s*.+\n?)+)/m)))
    meta.tags = x[1].split('\n').map(l => l.replace(/^\s*-\s*/, '').trim()).filter(Boolean);
  const wM = content.match(/## When to Use\s*\n([\s\S]*?)(?=\n## )/);
  if (wM) meta.whenToUse = wM[1].split('\n').filter(l => l.match(/^\s*-\s+/)).slice(0, 3).map(l => l.replace(/^\s*-\s*/, '').trim());
  return meta;
}

// Visible width (strip ANSI, emoji=2)
function vw(s) {
  const t = s.replace(/\x1b\[[0-9;]*m/g, '');
  let w = 0;
  for (const ch of t) {
    const c = ch.codePointAt(0);
    w += (c >= 0x1F000 && c <= 0x1FFFF) || (c >= 0x2600 && c <= 0x27BF) ||
         (c >= 0x2300 && c <= 0x23FF) || (c >= 0x4E00 && c <= 0x9FFF) ||
         (c >= 0x3000 && c <= 0x30FF) ? 2 : 1;
  }
  return w;
}

function pad(s, n) { return s + ' '.repeat(Math.max(0, n - vw(s))); }

function row(text) {
  return `${CN}║${R} ${pad(text, W - 1)}${CN}║${R}`;
}

function center(text, width) {
  const diff = Math.max(0, width - vw(text));
  const left = Math.floor(diff / 2);
  return ' '.repeat(left) + text;
}

function wrap(text, max) {
  if (!text) return [];
  const words = text.split(' '), lines = [];
  let cur = '';
  for (const w of words) {
    const t = cur ? cur + ' ' + w : w;
    if (vw(t) > max && cur) { lines.push(cur); cur = w; } else cur = t;
  }
  if (cur) lines.push(cur);
  return lines;
}

// --- Banner generator ---

function banner(skillName, meta) {
  const name = meta.name || skillName;
  const domain = meta.domain || 'general';
  const desc = meta.description || 'No description available.';
  const tags = (meta.tags || []).slice(0, 3);
  const triggers = meta.whenToUse || [];

  // ASCII art for "1AI SKILLS" — block letters, no special chars
  const art = [
    ' ___   ___ ___    _ _  __ ___',
    '|_  ) / __|_  )  (_) |/  |_  )',
    ' / /  \\__ \\/ /   | |   <  / /',
    '/___| |___/___|  |_|_|\\_\\/___|',
    '              S K I L L S     ',
  ];

  const L = [];
  L.push(`${CN}╔${'═'.repeat(W)}╗${R}`);
  for (const a of art) L.push(row(`${MG}${a}${R}`));
  L.push(`${CN}╠${'═'.repeat(W)}╣${R}`);

  // ACTIVATED line
  const act = `${B}${YL}⚡ ${name} ACTIVATED!${R}`;
  L.push(`${CN}║${R} ${pad(center(act, W - 1), W - 1)}${CN}║${R}`);

  L.push(`${CN}╠${'─'.repeat(W)}╣${R}`);

  // Domain & tags
  L.push(row(`${B}Domain:${R}  ${GN}📂 ${domain}${R}`));
  if (tags.length) L.push(row(`${B}Tags:${R}    ${D}🏷️  ${tags.join(', ')}${R}`));

  L.push(`${CN}╠${'─'.repeat(W)}╣${R}`);

  // Summary
  L.push(row(`${B}Summary:${R}`));
  for (const dl of wrap(desc, W - 6).slice(0, 3))
    L.push(row(`  ${CN}▸ ${dl}${R}`));

  // Triggers
  if (triggers.length) {
    L.push(`${CN}╠${'─'.repeat(W)}╣${R}`);
    L.push(row(`${B}Triggers:${R}`));
    for (const t of triggers) L.push(row(`  ${YL}▸ ${t}${R}`));
  }

  L.push(`${CN}╚${'═'.repeat(W)}╝${R}`);
  return L.join('\n');
}

// --- Main ---

let input = '';
process.stdin.on('data', chunk => input += chunk);
process.stdin.on('end', () => {
  try {
    const data = JSON.parse(input);
    if (data.tool_name !== 'Skill') return;
    const skillName = data.tool_input?.skill || data.tool_input?.name || '';
    if (!skillName) return;

    const fp = findSkill(skillName);
    let meta = {};
    if (fp) try { meta = parseFM(fs.readFileSync(fp, 'utf8')); } catch {}
    if (!meta.name && data.tool_output) {
      const m = parseFM(data.tool_output);
      if (m.name) meta = m;
    }

    process.stderr.write(banner(skillName, meta) + '\n');
  } catch { /* silent */ }
});
