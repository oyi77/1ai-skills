#!/usr/bin/env node
/**
 * skill-router-prompt.js — UserPromptSubmit hook.
 *
 * Runs the 1ai-skills skill router on every user prompt and injects a
 * systemMessage that names the matching role anchor (if any). This is the
 * orchestration trigger: it turns "CEO / CTO / CMO / CFO / COO / CCO"
 * strategic intent into an automatic role-skill suggestion, without
 * requiring the agent to remember to call the router itself.
 *
 * Output contract (Claude Code UserPromptSubmit):
 *   {"systemMessage": "..."}   — non-empty => shown to agent before acting
 *   {}                         — silent (no suggestion)
 *
 * Safety: bounded runtime (5s timeout), never throws, never blocks the
 * prompt. A router failure degrades to silent — the agent still works.
 */
'use strict';

const { execFileSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const REPO = '/home/openclaw/projects/1ai-skills';
const ROUTER = path.join(REPO, 'scripts', 'skill_router.py');
const SKILLS_JSON = path.join(REPO, 'SKILLS.json');

// ── Read prompt from stdin (Claude Code passes it as JSON) ──────────────
function readPrompt() {
  // Node streams are async — a synchronous `for...of process.stdin` returns
  // nothing and the hook silently degrades. Read the fd directly instead.
  const maxBytes = 65536;
  const buf = Buffer.alloc(maxBytes);
  let total = 0;
  try {
    const fd = 0;
    while (total < maxBytes) {
      const n = fs.readSync(fd, buf, total, maxBytes - total, null);
      if (n <= 0) break;
      total += n;
    }
  } catch {
    // EAGAIN / no stdin — fall through with whatever was read
  }
  const raw = buf.subarray(0, total).toString('utf8').trim();
  if (!raw) return '';
  try {
    const parsed = JSON.parse(raw);
    // Claude Code passes {"prompt": "..."} on UserPromptSubmit
    if (parsed && typeof parsed.prompt === 'string') return parsed.prompt;
    return raw;
  } catch {
    return raw;
  }
}

// ── Load registry for anchor lookup ──────────────────────────────────────
function loadAnchorMap() {
  try {
    const data = JSON.parse(fs.readFileSync(SKILLS_JSON, 'utf8'));
    const map = {};
    for (const s of data.skills || []) {
      if (s.name && s.name.startsWith('role-') && s.roles && s.roles.length) {
        map[s.name] = s;
      }
    }
    return map;
  } catch {
    return {};
  }
}

// ── Detect role intent via router ────────────────────────────────────────
function detectRole(prompt) {
  if (!prompt || prompt.length < 4) return null;
  try {
    const out = execFileSync('python3', [ROUTER, prompt, '--top', '3', '--json'], {
      timeout: 4000,
      maxBuffer: 64 * 1024,
      cwd: REPO,
      stdio: ['ignore', 'pipe', 'pipe'],
    }).toString('utf8');
    const parsed = JSON.parse(out);
    const results = parsed.results || parsed;
    if (!Array.isArray(results) || results.length === 0) return null;
    const top = results[0];
    if (!top || !top.name) return null;
    return { name: top.name, score: top.score, category: top.category };
  } catch {
    return null;
  }
}

// ── Main ────────────────────────────────────────────────────────────────
function main() {
  const prompt = readPrompt();
  if (!prompt) {
    process.stdout.write('{}');
    return;
  }

  const hit = detectRole(prompt);
  if (!hit) {
    process.stdout.write('{}');
    return;
  }

  // Only suggest when the top hit is a role anchor (role-* prefix).
  // This prevents noise: implementation tasks route to functional skills,
  // strategic tasks route to corporate anchors.
  if (!hit.name.startsWith('role-')) {
    process.stdout.write('{}');
    return;
  }

  const anchors = loadAnchorMap();
  const anchor = anchors[hit.name];
  const personaName = anchor && anchor.persona ? anchor.persona.name : null;
  const personaTitle = anchor && anchor.persona ? anchor.persona.title : null;
  const roleLabel = hit.name.replace(/^role-/, '').replace(/-/g, ' ');

  let msg = `1ai-skills role detected: "${roleLabel}" (score ${hit.score}).`;
  if (personaName) {
    msg += ` Persona: ${personaName}`;
    if (personaTitle) msg += ` — ${personaTitle}`;
  }
  msg += ` Load skill: ~/.agents/skills/${hit.name}/SKILL.md to follow its workflow.`;

  process.stdout.write(JSON.stringify({ systemMessage: msg }));
}

try {
  main();
} catch {
  // Never block the prompt; degrade silently.
  process.stdout.write('{}');
}