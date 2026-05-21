#!/usr/bin/env node
/**
 * skill-feedback-capture.js — PostToolUse hook (matcher: Skill)
 * Detects when user gives feedback during/after skill use
 * Queues feedback for skill improvement
 *
 * How it works:
 * 1. Tracks which skill is currently active
 * 2. After skill invocation, watches for user messages containing feedback signals
 * 3. Logs feedback to skill's feedback.jsonl for the evolver to consume
 */

const fs = require('fs');
const path = require('path');

const METRICS_DIR = path.join(process.env.HOME, '.1ai-skills');
const FEEDBACK_FILE = path.join(METRICS_DIR, 'feedback.jsonl');
const STATE_FILE = path.join(METRICS_DIR, '.active-skill.json');

// Feedback signals — phrases that indicate user is improving the skill
const FEEDBACK_SIGNALS = [
  // Corrections
  'don\'t do', 'stop doing', 'never', 'always', 'instead of',
  'wrong', 'incorrect', 'fix this', 'change this', 'no not',
  'not that', 'that\'s wrong', 'bad', 'terrible',

  // Improvements
  'better', 'good', 'perfect', 'nice', 'great', 'exactly',
  'that\'s it', 'yes', 'correct', 'right', 'do this instead',
  'use this', 'try this', 'add this', 'include',

  // Preferences
  'prefer', 'want', 'need', 'should', 'must', 'make it',
  'i like', 'i want', 'please', 'can you',

  // Patterns
  'next time', 'from now on', 'always do', 'remember',
  'when this happens', 'if this then', 'pattern',
];

function loadState() {
  try { return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8')); }
  catch (e) { return {}; }
}

function saveState(state) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(state));
}

function detectFeedback(message) {
  const lower = message.toLowerCase();
  const signals = FEEDBACK_SIGNALS.filter(s => lower.includes(s));
  return signals.length > 0 ? signals : null;
}

function extractInsight(message) {
  // Try to extract the actionable part
  const lines = message.split('\n').filter(l => l.trim());
  // Look for imperative sentences
  const imperatives = lines.filter(l =>
    /^(use|add|change|fix|do|don't|stop|always|never|make|try|include|remove|replace)/i.test(l.trim())
  );
  return imperatives.length > 0 ? imperatives.join('; ') : message.slice(0, 500);
}

// Main
let input = '';
process.stdin.on('data', chunk => input += chunk);
process.stdin.on('end', () => {
  try {
    const data = JSON.parse(input);

    // Track skill invocations
    if (data.tool_name === 'Skill') {
      const skillName = data.tool_input?.skill || 'unknown';
      saveState({
        active_skill: skillName,
        invoked_at: new Date().toISOString(),
        user_message: data.user_message || '',
      });
      return;
    }

    // Check if user message contains feedback about active skill
    const state = loadState();
    if (!state.active_skill) return;

    const userMessage = data.user_message || '';
    if (!userMessage) return;

    const signals = detectFeedback(userMessage);
    if (!signals) return;

    // Record feedback
    const entry = {
      ts: new Date().toISOString(),
      skill: state.active_skill,
      feedback_signals: signals,
      insight: extractInsight(userMessage),
      raw_message: userMessage.slice(0, 1000),
    };

    fs.appendFileSync(FEEDBACK_FILE, JSON.stringify(entry) + '\n');

    // Also update stats with feedback count
    const statsFile = path.join(METRICS_DIR, 'stats.json');
    try {
      const stats = JSON.parse(fs.readFileSync(statsFile, 'utf8'));
      if (stats[state.active_skill]) {
        stats[state.active_skill].feedback_count = (stats[state.active_skill].feedback_count || 0) + 1;
        stats[state.active_skill].last_feedback = new Date().toISOString();
        fs.writeFileSync(statsFile, JSON.stringify(stats, null, 2));
      }
    } catch (e) { /* stats not yet created */ }

  } catch (e) { /* silent fail */ }
});
