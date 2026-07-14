#!/usr/bin/env node
'use strict';

/**
 * skill-banner.js — Claude Code PostToolUse hook.
 *
 * Detects Skill tool invocations and prints an activation banner.
 * Depends on the shared core at hooks/shared/skill-banner-core.js.
 */

var core = require('./shared/skill-banner-core.js');

var input = '';
process.stdin.on('data', function (chunk) { input += chunk; });
process.stdin.on('end', function () {
  try {
    var data = JSON.parse(input);
    if (data.tool_name !== 'Skill') return;

    var skillName = data.tool_input && (data.tool_input.skill || data.tool_input.name);
    if (!skillName) return;

    if (core.isAlreadyWelcomed(skillName)) return;

    var meta = core.resolveSkillMeta(skillName);

    // Fallback: parse frontmatter from tool output if filesystem/index didn't have it
    if (!meta || !meta.name) {
      meta = parseInlineMeta(data.tool_output) || meta;
    }

    process.stderr.write(core.buildBanner(skillName, meta) + '\n');
  } catch (e) {
    // Silent — don't break skill loading
  }
});

function parseInlineMeta(output) {
  if (typeof output !== 'string') return null;
  var m = output.match(/^---\n([\s\S]*?)\n---/);
  if (!m) return null;
  var y = m[1], meta = {}, x;
  if ((x = y.match(/^name:\s*(.+)$/m))) meta.name = x[1].trim();
  if ((x = y.match(/^description:\s*(.+)$/m))) meta.description = x[1].trim();
  if ((x = y.match(/^domain:\s*(.+)$/m))) meta.domain = x[1].trim();
  return meta.name ? meta : null;
}
