#!/usr/bin/env node
/**
 * skill-banner-omp.js — OMP PostToolUse hook.
 *
 * Detects `read` tool calls where the resolved path contains a SKILL.md
 * and prints an activation banner via the OMP message bus.
 * Depends on the shared core at hooks/shared/skill-banner-core.js.
 *
 * Usage: install.sh copies this to ~/.omp/agent/hooks/post/
 */

var core = require('./shared/skill-banner-core.js');

module.exports = function skillBannerOmp(pi) {
  pi.on("tool_result", function (event) {
    if (event.type !== "tool_result") return;
    if (event.toolName !== "read") return;
    if (event.isError) return;

    var inputPath = event.input && event.input.path;
    if (typeof inputPath !== "string") return;

    var skillName = core.skillNameFromPath(inputPath);
    if (!skillName) return;

    if (core.isAlreadyWelcomed(skillName)) return;

    var meta = core.resolveSkillMeta(skillName);
    var bannerText = core.buildBanner(skillName, meta);

    pi.sendMessage({
      customType: "skill-banner",
      content: "[Skill Activated] " + skillName,
      display: bannerText,
    });
  });
};
