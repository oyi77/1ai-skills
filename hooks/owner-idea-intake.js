#!/usr/bin/env node
/**
 * owner-idea-intake.js — UserPromptSubmit hook.
 *
 * Detects owner-originated idea language and injects the corporate intake
 * protocol before the agent acts. It does not decide or build; it forces
 * Vilona triage: strategic fit, company/ecosystem value, then CEO escalation.
 *
 * Conservative trigger policy: only explicit ideation/competitor language.
 * Ordinary coding, research, and status prompts remain silent.
 */
'use strict';

const fs = require('fs');

const MAX_BYTES = 65536;
const IDEA_PATTERNS = [
  /\bi have an idea\b/i,
  /\bwhat if we (?:build|make|launch|create|turn|develop)\b/i,
  /\bhow if we (?:build|make|launch|create|turn|develop)\b/i,
  /\bshould we (?:build|make|launch|create|turn|develop)\b/i,
  /\b(?:build|make|launch|create) (?:this|it) (?:like|similar to|based on)\b/i,
  /\bas reference\s*:/i,
  /\bcompetitor reference\b/i,
  /\bnew product idea\b/i,
  /\bshould we build this\b/i,
];

function readPrompt() {
  const buffer = Buffer.alloc(MAX_BYTES);
  let total = 0;
  try {
    while (total < MAX_BYTES) {
      const n = fs.readSync(0, buffer, total, MAX_BYTES - total, null);
      if (n <= 0) break;
      total += n;
    }
  } catch {
    // Empty or unavailable stdin: silent fallback.
  }
  const raw = buffer.subarray(0, total).toString('utf8').trim();
  if (!raw) return '';
  try {
    const data = JSON.parse(raw);
    return typeof data.prompt === 'string' ? data.prompt : raw;
  } catch {
    return raw;
  }
}

function main() {
  const prompt = readPrompt();
  if (!prompt || !IDEA_PATTERNS.some((pattern) => pattern.test(prompt))) {
    process.stdout.write('{}');
    return;
  }
  process.stdout.write(JSON.stringify({
    systemMessage: [
      '1ai corporate intake required: owner-originated idea detected.',
      'Load ~/.agents/skills/role-owner-idea-intake/SKILL.md before evaluating or building.',
      'Vilona must classify the idea, check existing skills/brain, score company benefit, ecosystem benefit, feasibility, cost, and risk, then route promising ideas to role-ceo.',
      'Do not implement directly. Record build/research/archive decision and escalate through CEO → relevant C-suite → multi-department review.',
    ].join(' '),
  }));
}

try {
  main();
} catch {
  process.stdout.write('{}');
}