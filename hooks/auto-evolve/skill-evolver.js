#!/usr/bin/env node
/**
 * skill-evolver.js — SessionEnd hook / manual trigger
 * Reads metrics, identifies underperforming skills, rewrites SKILL.md
 * Run: node ~/.claude/hooks/skill-evolver.js [--dry-run]
 */

const fs = require('fs');
const path = require('path');

const METRICS_DIR = path.join(process.env.HOME, '.1ai-skills');
const STATS_FILE = path.join(METRICS_DIR, 'stats.json');
const EVOLVE_LOG = path.join(METRICS_DIR, 'evolve-log.jsonl');
const CONFIG_FILE = path.join(METRICS_DIR, 'evolve-config.json');

const DRY_RUN = process.argv.includes('--dry-run');

// Default config
const DEFAULT_CONFIG = {
  min_invocations: 5,        // Need at least 5 uses before evolving
  success_threshold: 70,     // Below 70% = needs improvement
  evolve_cooldown_hours: 24, // Don't evolve same skill within 24h
  max_evolves_per_run: 3,    // Max skills to evolve per session
  auto_push: false,
  target_repo: '',
  skill_dirs: [
    path.join(process.env.HOME, '.claude', 'skills'),
  ],
};

function loadConfig() {
  try { return { ...DEFAULT_CONFIG, ...JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8')) }; }
  catch (e) { return DEFAULT_CONFIG; }
}

function loadStats() {
  try { return JSON.parse(fs.readFileSync(STATS_FILE, 'utf8')); }
  catch (e) { return {}; }
}

function loadEvolveLog() {
  try {
    return fs.readFileSync(EVOLVE_LOG, 'utf8').trim().split('\n').map(l => JSON.parse(l));
  }
  catch (e) { return []; }
}

function findSkillPath(skillName, dirs) {
  for (const dir of dirs) {
    const p = path.join(dir, skillName, 'SKILL.md');
    if (fs.existsSync(p)) return p;
  }
  return null;
}

function identifyCandidates(stats, config, evolveLog) {
  const candidates = [];
  const now = Date.now();

  for (const [skill, data] of Object.entries(stats)) {
    // Skip if not enough invocations
    if (data.invocations < config.min_invocations) continue;

    // Skip if already successful
    if (data.success_rate >= config.success_threshold) continue;

    // Check cooldown
    const lastEvolve = evolveLog
      .filter(e => e.skill === skill)
      .sort((a, b) => new Date(b.ts) - new Date(a.ts))[0];

    if (lastEvolve) {
      const hoursSince = (now - new Date(lastEvolve.ts).getTime()) / (1000 * 60 * 60);
      if (hoursSince < config.evolve_cooldown_hours) continue;
    }

    candidates.push({
      skill,
      success_rate: data.success_rate,
      invocations: data.invocations,
      failures: data.failures,
      avg_tokens: data.avg_tokens,
      priority: (100 - data.success_rate) * Math.log(data.invocations),
    });
  }

  return candidates.sort((a, b) => b.priority - a.priority).slice(0, config.max_evolves_per_run);
}

function analyzeFailures(skillName) {
  const metricsFile = path.join(METRICS_DIR, 'metrics.jsonl');
  if (!fs.existsSync(metricsFile)) return [];

  const lines = fs.readFileSync(metricsFile, 'utf8').trim().split('\n');
  const failures = [];

  for (const line of lines) {
    try {
      const entry = JSON.parse(line);
      if (entry.skill === skillName && !entry.success) {
        failures.push({
          error: entry.error,
          args: entry.args,
          ts: entry.ts,
        });
      }
    } catch (e) { /* ignore */ }
  }

  return failures.slice(-10); // Last 10 failures
}

function generateImprovementPrompt(skillName, skillContent, failures, stats) {
  const errorSummary = failures.map(f => `- ${f.error || 'unknown error'}`).join('\n');

  return `You are improving a Claude Code skill that has been underperforming.

## Skill: ${skillName}
## Current success rate: ${stats.success_rate}% over ${stats.invocations} invocations

## Recent failures:
${errorSummary || '- No specific errors captured'}

## Current SKILL.md content:
${skillContent}

## Task:
1. Analyze the failure patterns
2. Improve the SKILL.md to handle these failure cases
3. Keep the core purpose intact
4. Add better error handling, clearer instructions, or edge case coverage
5. Output ONLY the improved SKILL.md content, nothing else

Focus on:
- Making instructions more specific and unambiguous
- Adding error recovery steps
- Handling common failure modes
- Keeping token usage efficient`;
}

function evolveSkill(skillPath, skillName, failures, stats, config) {
  const content = fs.readFileSync(skillPath, 'utf8');

  // Generate evolution record
  const evolveRecord = {
    ts: new Date().toISOString(),
    skill: skillName,
    action: 'evolve_triggered',
    success_rate: stats.success_rate,
    invocations: stats.invocations,
    failure_count: failures.length,
    skill_path: skillPath,
    improvement_prompt: generateImprovementPrompt(skillName, content, failures, stats),
  };

  if (DRY_RUN) {
    console.log(`[DRY RUN] Would evolve: ${skillName} (${stats.success_rate}% success, ${stats.invocations} uses)`);
    console.log(`  Failures: ${failures.length}`);
    console.log(`  Path: ${skillPath}`);
    return evolveRecord;
  }

  // Write evolution request to queue (consumed by Claude session)
  const queueFile = path.join(METRICS_DIR, 'evolve-queue.jsonl');
  fs.appendFileSync(queueFile, JSON.stringify(evolveRecord) + '\n');

  return evolveRecord;
}

// Main
const config = loadConfig();
const stats = loadStats();
const evolveLog = loadEvolveLog();
const candidates = identifyCandidates(stats, config, evolveLog);

if (candidates.length === 0) {
  console.log('No skills need evolution right now.');
  process.exit(0);
}

console.log(`Found ${candidates.length} skill(s) to evolve:`);

let evolved = 0;
for (const candidate of candidates) {
  const skillPath = findSkillPath(candidate.skill, config.skill_dirs);
  if (!skillPath) {
    console.log(`  ${candidate.skill}: SKILL.md not found, skipping`);
    continue;
  }

  const failures = analyzeFailures(candidate.skill);
  const record = evolveSkill(skillPath, candidate.skill, failures, candidate, config);

  // Log evolution
  fs.appendFileSync(EVOLVE_LOG, JSON.stringify(record) + '\n');
  evolved++;

  console.log(`  ${candidate.skill}: ${candidate.success_rate}% success, ${candidate.failures} failures`);
}

console.log(`\n${evolved} skill(s) queued for evolution.`);
if (DRY_RUN) console.log('(dry run — no changes made)');

if (config.auto_push && evolved > 0 && !DRY_RUN) {
  console.log('Auto-push enabled — commit hook will handle git push.');
}
