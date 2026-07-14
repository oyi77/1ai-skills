#!/usr/bin/env node
/**
 * skill-banner-omp.js — OMP PostToolUse hook.
 *
 * Detects `read` tool calls where the path falls under the skills
 * directory and prints an activation banner via the OMP message bus.
 * Depends on the shared core at hooks/shared/skill-banner-core.js.
 *
 * Usage: install.sh copies this to ~/.omp/agent/hooks/post/
 */

var core = require('./shared/skill-banner-core.js');

/** Resolve the skills base dir (e.g. ~/.agents/skills) */
function skillsDir() {
  var home = process.env.HOME || process.env.USERPROFILE;
  var dirs = [home + '/.agents/skills', home + '/projects/1ai-skills'];
  for (var i = 0; i < dirs.length; i++) {
    try {
      if (require('fs').statSync(dirs[i]).isDirectory()) return dirs[i] + '/';
    } catch (_) {}
  }
  return null;
}

module.exports = function skillBannerOmp(pi) {
  var skillsBase = skillsDir();
  if (!skillsBase) return; // no skills directory found — silently skip

  pi.on("tool_result", function (event) {
    if (event.type !== "tool_result") return;
    if (event.toolName !== "read") return;
    if (event.isError) return;

    var inputPath = event.input && event.input.path;
    if (typeof inputPath !== "string") return;

    // OMP resolves skill:// URIs to FS paths; check if it's under skillsBase
    if (!inputPath.startsWith(skillsBase)) return;

    var rel = inputPath.slice(skillsBase.length).split('/')[0];
    if (!rel) return;

    if (core.isAlreadyWelcomed(rel)) return;

    var meta = core.resolveSkillMeta(rel);
    var bannerText = core.buildBanner(rel, meta);

    pi.sendMessage({
      customType: "skill-banner",
      content: "[Skill Activated] " + rel,
      display: bannerText,
    });
  });
};
