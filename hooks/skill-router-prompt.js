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

// ── Coding keyword fallback ──────────────────────────────────────────────
const CODING_KEYWORDS = [
  'fix ', 'debug', 'implement', 'write code', 'build feature', 'add test',
  'refactor', 'code review', 'review code', 'debug ', 'implement ',
  'build feature', 'add test', 'refactor ', 'code review', 'review code',
  'python ', '.py', 'function ', 'class ', 'async ', 'import ',
  'def ', 'export ', 'const ', 'let ', 'var ', 'function(',
  'def(', 'class(', 'import(', 'from ', 'require(', 'npm ', 'pip ',
  'bug ', 'error ', 'exception ', 'traceback', 'stack trace',
  'lint ', 'format ', 'format:', 'prettier', 'eslint', 'pylint',
  'mypy ', 'typescript', 'javascript', 'node ', 'deno ', 'bun ',
  'docker ', 'dockerfile', 'kubernetes', 'k8s', 'ci/cd', 'ci cd',
  'github action', 'gitlab ci', 'pipeline', 'deploy ', 'deploy:',
  'test ', 'pytest', 'jest', 'vitest', 'playwright', 'cypress',
  'mock ', 'stub ', 'fixture', 'fixture(', '@pytest', '@test',
  'expect(', 'assert(', 'assert.', 'describe(', 'it(', 'test(',
  'benchmark', 'profile ', 'profile(', 'optimize ', 'optimize(',
  'compile ', 'build ', 'make ', 'cargo ', 'go build', 'go test',
  'go run', 'go get', 'go mod', 'package.json', 'requirements.txt',
  'pyproject.toml', 'cargo.toml', 'go.mod', 'setup.py', 'setup.cfg',
  'makefile', 'cmake', 'gradle', 'maven', 'sbt', 'gradle',
];

function isCodingPrompt(prompt) {
  const normalized = prompt.toLowerCase();
  return CODING_KEYWORDS.some(kw => normalized.includes(kw));
}
// ─────────────────────────────────────────────────────────────────────────
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
  const anchors = loadAnchorMap(); // available everywhere below

  if (hit && hit.name.startsWith('role-') && hit.score >= 30.0) {
    // Router hit a role anchor above threshold — use it.
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
    return;
  }

  // No router role hit above threshold. Fall back: coding keyword → software-engineer.
  // This covers BOTH cases: (a) router returned null, (b) router returned a functional
  // skill (e.g. python-indentation-error-debugging) instead of the role anchor.
  const topIsNotRole = !hit || !hit.name.startsWith('role-') || hit.score < 30.0;
  if (topIsNotRole && isCodingPrompt(prompt)) {
    const anchor = anchors['role-software-engineer'];
    if (anchor) {
      const personaName = anchor.persona ? anchor.persona.name : null;
      const personaTitle = anchor.persona ? anchor.persona.title : null;
      const msg = `1ai-skills role detected: "software-engineer" (keyword match).` +
        ` Persona: ${personaName}` +
        (personaTitle ? ` — ${personaTitle}` : '') +
        ` Load skill: ~/.agents/skills/role-software-engineer/SKILL.md to follow its workflow.`;
      process.stdout.write(JSON.stringify({ systemMessage: msg }));
      return;
    }
  }

  process.stdout.write('{}');
}

try {
  main();
} catch {
  // Never block the prompt; degrade silently.
  process.stdout.write('{}');
}