#!/usr/bin/env node
/**
 * skill-router-prompt.js — UserPromptSubmit hook.
 *
 * Deterministic corporate intent router + fuzzy skill_router fallback.
 * Every owner/company prompt that expresses a corporate event (idea,
 * incident, legal, HR, vendor, PR, launch, escalation) MUST reach
 * a named role skill before the agent acts.
 *
 * Output contract (Claude Code UserPromptSubmit):
 *   {"systemMessage": "..."}   — non-empty => shown to agent before acting
 *   {}                         — silent (no suggestion)
 *
 * Safety: bounded runtime (5s), never throws, never blocks the prompt.
 */
'use strict';

const { execFileSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const REPO = '/home/openclaw/projects/1ai-skills';
const ROUTER = path.join(REPO, 'scripts', 'skill_router.py');
const SKILLS_JSON = path.join(REPO, 'SKILLS.json');

// ── Read prompt from stdin ───────────────────────────────────────────────
function readPrompt() {
  const maxBytes = 65536;
  const buf = Buffer.alloc(maxBytes);
  let total = 0;
  try {
    while (total < maxBytes) {
      const n = fs.readSync(0, buf, total, maxBytes - total, null);
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
    if (parsed && typeof parsed.prompt === 'string') return parsed.prompt;
    return raw;
  } catch {
    return raw;
  }
}

// ── Registry ─────────────────────────────────────────────────────────────
function loadAnchorMap() {
  const map = {};
  try {
    const data = JSON.parse(fs.readFileSync(SKILLS_JSON, 'utf8'));
    for (const s of data.skills || []) {
      if (s.name && s.name.startsWith('role-') && s.roles && s.roles.length) {
        map[s.name] = s;
      }
    }
  } catch {
    // silent
  }
  return map;
}

// ── Deterministic corporate intent ───────────────────────────────────────
// Priority is intentional: explicit crisis/incident language beats generic
// "I have an idea" for the same prompt.
const CORPORATE_INTENT = [
  {
    role: 'role-incident-commander',
    keywords: [
      'production down', 'production outage', 'server down', 'service down',
      'system down', 'can\'t login', 'cannot login', '500 error', '500 errors',
      '5xx', 'database down', 'database error', 'database is returning',
      'api error', 'api errors', 'api is returning', 'api returning',
      'errors for', 'returning errors', 'error rate', 'payment failing',
      'payment gateway is failing', 'revenue blocked', 'checkout broken',
      'got hacked', 'we got hacked', 'hacked', 'breach', 'data breach',
      'data exfiltration', 'security incident', 'unauthorized access',
      'intrusion', 'sev1', 'sev2', 'sev3', 'sev4', 'p0', 'p1', 'p2',
      'critical incident', 'declare incident', 'data loss', 'data corruption',
      'service degraded', 'incident commander', 'war room'
    ]
  },
  {
    role: 'role-crisis-communications',
    keywords: [
      'journalist', 'media inquiry', 'press inquiry', 'press release',
      'press conference', 'negative reviews', 'negative review', 'viral',
      'trending on twitter', 'going viral', 'controversial', 'offensive',
      'insensitive', 'backlash', 'boycott', 'public apology',
      'public statement', 'public response', 'crisis response',
      'brand reputation', 'brand crisis', 'pr crisis', 'privacy scandal',
      'data leak', 'data spill', 'exposed data', 'exposed on social',
      'media is covering', 'media coverage', 'statement to press',
      'ceo made a', 'ceo said', 'ceo tweeted'
    ]
  },
  {
    role: 'role-legal-counsel',
    keywords: [
      'gdpr', 'ccpa', 'hipaa', 'sox ', 'pci ', 'ferpa', 'coppa',
      'patent', 'trademark', 'copyright', 'ip infringement', 'ip dispute',
      'sue ', 'suing ', 'lawsuit', 'litigation', 'legal action',
      'cease and desist', 'nda', 'non-disclosure', 'confidentiality agreement',
      'data export', 'export their data', 'export the data', 'export my data',
      'export user data', 'export customer data', 'want to export',
      'data portability', 'right to be forgotten',
      'data deletion', 'privacy obligation', 'privacy policy',
      'data retention', 'regulatory obligation', 'compliance audit',
      'compliance review', 'regulatory audit', 'regulatory review',
      'outside counsel', 'legal opinion', 'legal advice', 'legal consultation',
      'terms of service', 'contract terms', 'contract review'
    ]
  },
  {
    role: 'role-people-operations',
    keywords: [
      'resignation', 'resign', 'wants to leave', 'leaving the company',
      'leaving us', 'team conflict', 'team disagreement', 'interpersonal',
      'conflict between', 'in conflict', 'dispute between', 'not getting along',
      'underperformance', 'underperforming', 'performance concern',
      'performance review', 'performance plan', 'improvement plan',
      'hire ', 'hiring ', 'new hire', 'role change', 'compensation ',
      'equity ', 'restructure', 're-org', 'reorg', 'org change',
      'team restructure', 'layoffs', 'layoff', 'let go', 'firing',
      'terminate', 'termination', 'hr ', 'people ops', 'onboarding',
      'offboarding', 'exit interview', 'talent', 'recruit', 'headcount',
      'capacity plan', 'employee', 'employees', 'staff'
    ]
  },
  {
    role: 'role-vendor-and-partnerships',
    keywords: [
      'vendor', 'vendors', 'procurement', 'saas agreement', 'saas contract',
      'aws ', 'azure ', 'gcp ', 'cloud provider', 'cloud migration',
      'price hike', 'price increase', 'renewal', 'renew ', 'contract renewal',
      'exclusive ', 'exclusivity', 'distribution rights', 'strategic partner',
      'due diligence', 'm&a', 'acquisition', 'acquire', 'buyout',
      'investment in', 'partnership', 'co-marketing', 'joint venture',
      'integration partner', 'announce the partnership', 'announce partnership',
      'partner wants', 'partner contract'
    ]
  },
  {
    role: 'role-owner-idea-intake',
    keywords: [
      'i have an idea', 'what if we', 'how if we', 'should we build',
      'new product idea', 'competitor reference', 'as reference:',
      'like tradoor', 'like notion', 'like figma', 'like stripe',
      'crypto payment', 'payment option', 'market expansion', 'expand to',
      'expanding to', 'explore ', 'ai agents for', 'pivot to', 'pivot into',
      'strategic pivot', 'new product line', 'new market', 'new opportunity',
      'strategic direction', 'ready to launch', 'go-to-market',
      'launch strategy', 'launch v', 'launch version', 'product roadmap',
      'build something like', 'make this application like',
      'make an app like', 'should we add', 'could we add',
      'let\'s add', 'let us add', 'i want to build', 'i want to create',
      'owner idea', 'idea from owner'
    ]
  },
  {
    role: 'role-owner-decision-log',
    keywords: [
      'log the decision', 'decision log', 'record the idea outcome',
      'owner decision', 'audit trail', 'write up the verdict',
      'record the decision', 'decision matrix', 'decision record'
    ]
  },
  {
    role: 'role-multi-department-brainstorm',
    keywords: [
      'multi-department review', 'cross-functional debate',
      'stakeholder discussion', 'brainstorm across teams',
      'who should weigh in', 'department perspectives',
      'all departments discuss', 'department heads discuss'
    ]
  }
];

// Coding fallback: when no corporate intent matched, ensure implementation
// tasks still reach the software-engineer role anchor.
const CODING_KEYWORDS = [
  'fix ', 'debug', 'implement', 'write code', 'build feature', 'add test',
  'refactor', 'code review', 'review code', 'python ', '.py',
  'function ', 'class ', 'async ', 'import ', 'def ',
  'const ', 'let ', 'var ', 'function(', 'def(', 'class(', 'import(',
  'from ', 'require(', 'npm ', 'pip ', 'bug ', 'error ', 'exception ',
  'traceback', 'stack trace', 'lint ', 'format ', 'prettier', 'eslint',
  'pylint', 'mypy ', 'typescript', 'javascript', 'node ', 'deno ', 'bun ',
  'docker ', 'dockerfile', 'kubernetes', 'k8s', 'ci/cd', 'ci cd',
  'github action', 'gitlab ci', 'pipeline', 'deploy ', 'deploy:',
  'test ', 'pytest', 'jest', 'vitest', 'playwright', 'cypress',
  'mock ', 'stub ', 'fixture', 'fixture(', '@pytest', '@test',
  'expect(', 'assert(', 'assert.', 'describe(', 'it(', 'test(',
  'unit test', 'unit tests', 'integration test', 'e2e test', 'write test',
  'code coverage', 'test coverage', 'tdd', 'red green refactor', 'write tests',
  'benchmark', 'profile ', 'compile ', 'build ', 'make ', 'cargo ',
  'go build', 'go test', 'go run', 'go get', 'go mod', 'package.json',
  'requirements.txt', 'pyproject.toml', 'cargo.toml', 'go.mod',
  'setup.py', 'setup.cfg', 'makefile', 'cmake', 'gradle', 'maven', 'sbt'
];

function normalized(prompt) {
  return ' ' + prompt.toLowerCase().replace(/[^a-z0-9&'\-]+/g, ' ') + ' ';
}

function matchKeywords(prompt, keywords) {
  const q = normalized(prompt);
  return keywords.filter(kw => q.includes(kw.toLowerCase()));
}

function deterministicRole(prompt) {
  for (const intent of CORPORATE_INTENT) {
    const hits = matchKeywords(prompt, intent.keywords);
    if (hits.length) {
      return { role: intent.role, hits };
    }
  }
  if (matchKeywords(prompt, CODING_KEYWORDS).length) {
    return { role: 'role-software-engineer', hits: ['coding keyword'] };
  }
  return null;
}

// ── Router fallback ──────────────────────────────────────────────────────
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

  const anchors = loadAnchorMap();
  const decision = deterministicRole(prompt);

  let name = null;
  let scoreLabel = '';

  if (decision && anchors[decision.role]) {
    // Deterministic intent layer wins: corporate events must not be
    // misrouted by fuzzy skill-name scoring (data breach ≠ data-engineer).
    name = decision.role;
    scoreLabel = `intent:${decision.hits[0]}`;
  } else {
    const hit = detectRole(prompt);
    if (hit && hit.name.startsWith('role-') && hit.score >= 30.0 && anchors[hit.name]) {
      name = hit.name;
      scoreLabel = `score ${hit.score}`;
    } else if (hit && hit.name.startsWith('role-') && hit.score >= 30.0) {
      name = hit.name;
      scoreLabel = `score ${hit.score}`;
    }
  }

  if (!name) {
    process.stdout.write('{}');
    return;
  }

  const anchor = anchors[name];
  const personaName = anchor && anchor.persona ? anchor.persona.name : null;
  const personaTitle = anchor && anchor.persona ? anchor.persona.title : null;
  const roleLabel = name.replace(/^role-/, '').replace(/-/g, ' ');

  let msg = `1ai-skills role detected: "${roleLabel}" (${scoreLabel}).`;
  if (personaName) {
    msg += ` Persona: ${personaName}`;
    if (personaTitle) msg += ` — ${personaTitle}`;
  }
  msg += ` Load skill: ~/.agents/skills/${name}/SKILL.md to follow its workflow.`;

  process.stdout.write(JSON.stringify({ systemMessage: msg }));
}

try {
  main();
} catch {
  process.stdout.write('{}');
}
