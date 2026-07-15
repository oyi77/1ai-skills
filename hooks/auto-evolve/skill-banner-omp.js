#!/usr/bin/env node
/**
 * skill-banner-omp.js — OMP PostToolUse hook.
 *
 * Detects `read` tool calls where the resolved path contains a SKILL.md
 * and prepends an activation banner to the tool output.
 *
 * Uses tool-result content modification (not pi.sendMessage) because
 * sendMessage during streaming feeds the LLM via steer() without
 * emitting a message_start event — the TUI never renders it.
 *
 * Depends on the shared core at hooks/shared/skill-banner-core.js.
 *
 * Usage: install.sh copies this to ~/.omp/agent/hooks/post/
 */

var core = require('./shared/skill-banner-core.js');

module.exports = function skillBannerOmp(pi) {
  pi.on("tool_result", function (event) {
    // Only for successful read tool calls
    if (event.type !== "tool_result") return;
    if (event.toolName !== "read") return;
    if (event.isError) return;

    // Extract skill name from the tool input path
    var inputPath = event.input && event.input.path;
    if (typeof inputPath !== "string") return;

    var skillName = core.skillNameFromPath(inputPath);
    if (!skillName) return;

    // Dedup: only show banner once per skill per session
    if (core.isAlreadyWelcomed(skillName)) return;

    // Build banner and strip ANSI codes for plain-text output
    var meta = core.resolveSkillMeta(skillName);
    var ansiBanner = core.buildBanner(skillName, meta);
    var plainBanner = core.stripAnsi(ansiBanner);

    // Prepend banner to the FIRST text block in the tool result
    var content = event.content;
    if (!content || !content.length) return;

    // Find the first text content block
    for (var i = 0; i < content.length; i++) {
      var block = content[i];
      if (block && block.type === "text") {
        // Prepend banner + separator to the existing text
        var modified = {};
        // Copy enumerable own properties to make a new object
        for (var k in block) {
          if (Object.prototype.hasOwnProperty.call(block, k)) {
            modified[k] = block[k];
          }
        }
        modified.text = '\n' + plainBanner + '\n\n───\n\n' + modified.text;
        content[i] = modified;
        break;
      }
    }

    // Return modified content — OMP will replace the tool result with it
    return { content: content };
  });
};
