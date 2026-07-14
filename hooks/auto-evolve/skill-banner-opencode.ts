/// <reference types="bun" />
/**
 * skill-banner-opencode.ts — OpenCode plugin.
 *
 * Shows an ASCII activation banner when an agent reads a skill URI
 * or a resolved skill filesystem path. Handles both skill:// and
 * resolved FS paths that OpenCode may pass to the hook.
 * Depends on shared core at hooks/shared/skill-banner-core.js.
 *
 * Install: copied to ~/.opencode/plugins/ by install.sh
 */

const core = import.meta.require("./shared/skill-banner-core.js");

export const SkillBannerPlugin = async () => {
  return {
    "tool.execute.after": async (input: { tool?: string; args?: Record<string, unknown> }) => {
      if (input.tool !== "read") return;

      const pathVal = input.args?.path;
      if (typeof pathVal !== "string" || pathVal.length === 0) return;

      // Handles both skill:// URIs AND resolved FS paths (OpenCode
      // resolves before passing to tools)
      const skillName = core.skillNameFromPath(pathVal);
      if (!skillName || core.isAlreadyWelcomed(skillName)) return;

      const meta = core.resolveSkillMeta(skillName);
      const banner = core.buildBanner(skillName, meta);
      console.error(banner);
    },
  };
};
