#!/usr/bin/env node
/**
 * skill-tracker.js — PostToolUse hook
 * Logs every Skill tool invocation to ~/.1ai-skills/metrics.jsonl
 * Input: JSON on stdin with tool_name, tool_input, tool_output, duration, etc.
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const METRICS_DIR = path.join(process.env.HOME, '.1ai-skills');
const METRICS_FILE = path.join(METRICS_DIR, 'metrics.jsonl');
const CONFIG_FILE = path.join(METRICS_DIR, 'evolve-config.json');

// Ensure dir exists
if (!fs.existsSync(METRICS_DIR)) fs.mkdirSync(METRICS_DIR, { recursive: true });

let input = '';
process.stdin.on('data', chunk => input += chunk);
process.stdin.on('end', () => {
  try {
    const data = JSON.parse(input);

    // Only track Skill tool invocations
    if (data.tool_name !== 'Skill') return;

    const skillName = data.tool_input?.skill || 'unknown';
    const args = data.tool_input?.args || '';
    const output = data.tool_output || '';
    const isError = data.is_error || false;
    const duration = data.duration_ms || 0;

    // Extract token usage from output if available
    const tokenMatch = output.match(/(\d+)\s*tokens?/i);
    const tokens = tokenMatch ? parseInt(tokenMatch[1]) : 0;

    // Determine success/fail
    const success = !isError && !output.toLowerCase().includes('error');

    // Skill content hash (for change detection)
    const skillPaths = [
      path.join(process.env.HOME, '.claude', 'skills', skillName, 'SKILL.md'),
      path.join(process.env.HOME, '.claude', 'plugins', 'marketplaces', 'omc', 'skills', skillName, 'SKILL.md'),
    ];
    let contentHash = '';
    for (const sp of skillPaths) {
      if (fs.existsSync(sp)) {
        contentHash = crypto.createHash('sha256').update(fs.readFileSync(sp)).digest('hex').slice(0, 12);
        break;
      }
    }

    const entry = {
      ts: new Date().toISOString(),
      skill: skillName,
      args: args.slice(0, 200),
      success,
      tokens,
      duration_ms: duration,
      hash: contentHash,
      error: isError ? output.slice(0, 300) : null,
    };

    fs.appendFileSync(METRICS_FILE, JSON.stringify(entry) + '\n');

    // Update aggregate stats
    updateStats(skillName, success, tokens, duration);

  } catch (e) {
    // Silent fail — hooks must not break the session
  }
});

function updateStats(skill, success, tokens, duration) {
  const statsFile = path.join(METRICS_DIR, 'stats.json');
  let stats = {};
  try { stats = JSON.parse(fs.readFileSync(statsFile, 'utf8')); } catch {}

  if (!stats[skill]) {
    stats[skill] = { invocations: 0, successes: 0, failures: 0, total_tokens: 0, total_ms: 0, first_seen: new Date().toISOString() };
  }

  const s = stats[skill];
  s.invocations++;
  if (success) s.successes++; else s.failures++;
  s.total_tokens += tokens;
  s.total_ms += duration;
  s.last_seen = new Date().toISOString();
  s.success_rate = Math.round((s.successes / s.invocations) * 100);
  s.avg_tokens = Math.round(s.total_tokens / s.invocations);

  fs.writeFileSync(statsFile, JSON.stringify(stats, null, 2));
}
