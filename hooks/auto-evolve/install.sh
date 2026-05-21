#!/bin/bash
# 1ai-skills Auto-Evolve Installer
# Installs hooks into Claude Code for self-improving skills
#
# Usage: bash hooks/auto-evolve/install.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
HOOKS_DIR="$CLAUDE_DIR/hooks"
METRICS_DIR="$HOME/.1ai-skills"
SETTINGS_FILE="$CLAUDE_DIR/settings.json"

echo "🧠 1ai-skills Auto-Evolve Installer"
echo "===================================="

# 1. Create directories
mkdir -p "$HOOKS_DIR" "$METRICS_DIR"
echo "✅ Directories created"

# 2. Copy hook scripts
for hook in skill-tracker.js skill-evolver.js skill-committer.js skill-feedback-capture.js; do
  src="$SCRIPT_DIR/$hook"
  if [ -f "$src" ]; then
    cp "$src" "$HOOKS_DIR/$hook"
    echo "✅ Installed $hook"
  else
    echo "⚠️  $hook not found in $SCRIPT_DIR, skipping"
  fi
done

# 3. Create default config if not exists
if [ ! -f "$METRICS_DIR/evolve-config.json" ]; then
  # Detect repo dir (where this script lives's parent)
  REPO_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

  cat > "$METRICS_DIR/evolve-config.json" << EOCONF
{
  "min_invocations": 5,
  "success_threshold": 70,
  "evolve_cooldown_hours": 24,
  "max_evolves_per_run": 3,
  "auto_push": false,
  "target_repo": "",
  "skill_dirs": [
    "$HOME/.claude/skills"
  ],
  "repo_dir": "$REPO_DIR",
  "commit_prefix": "evolve",
  "tracking_enabled": true,
  "evolve_enabled": true
}
EOCONF
  echo "✅ Config created at $METRICS_DIR/evolve-config.json"
  echo "   ℹ️  Edit auto_push and target_repo to enable auto-push to GitHub"
else
  echo "ℹ️  Config already exists, skipping"
fi

# 4. Wire hooks into settings.json
if [ ! -f "$SETTINGS_FILE" ]; then
  echo '{"hooks":{}}' > "$SETTINGS_FILE"
fi

# Use python3 to merge hooks (safe for existing config)
python3 << 'PYEOF'
import json, sys, os

settings_file = os.path.expanduser("~/.claude/settings.json")
hooks_dir = os.path.expanduser("~/.claude/hooks")

with open(settings_file) as f:
    settings = json.load(f)

hooks = settings.setdefault("hooks", {})

# PostToolUse: tracker + committer
post_tool = hooks.setdefault("PostToolUse", [])

# Add skill-tracker (matcher: Skill)
tracker_entry = {
    "matcher": "Skill",
    "hooks": [{"type": "command", "command": f'node "{hooks_dir}/skill-tracker.js"', "timeout": 5}]
}
if not any(h.get("matcher") == "Skill" for h in post_tool):
    post_tool.append(tracker_entry)

# Add skill-committer (matcher: Write|Edit)
committer_entry = {
    "matcher": "Write|Edit",
    "hooks": [{"type": "command", "command": f'node "{hooks_dir}/skill-committer.js"', "timeout": 35}]
}
if not any(h.get("matcher") == "Write|Edit" and "committer" in str(h) for h in post_tool):
    post_tool.append(committer_entry)

# UserPromptSubmit: feedback capture
user_submit = hooks.setdefault("UserPromptSubmit", [])
feedback_entry = {
    "hooks": [{"type": "command", "command": f'node "{hooks_dir}/skill-feedback-capture.js"', "timeout": 5}]
}
if not any("feedback-capture" in str(h) for h in user_submit):
    user_submit.append(feedback_entry)

# SessionEnd: evolver
session_end = hooks.setdefault("SessionEnd", [])
evolver_entry = {
    "hooks": [{"type": "command", "command": f'node "{hooks_dir}/skill-evolver.js"', "timeout": 30}]
}
if not any("evolver" in str(h) for h in session_end):
    session_end.append(evolver_entry)

with open(settings_file, "w") as f:
    json.dump(settings, f, indent=2)

print("✅ Hooks wired into settings.json")
PYEOF

# 5. Init metrics files
touch "$METRICS_DIR/metrics.jsonl"
touch "$METRICS_DIR/feedback.jsonl"
echo "✅ Metrics files initialized"

echo ""
echo "🎉 Auto-Evolve installed!"
echo ""
echo "Next steps:"
echo "  1. Edit ~/.1ai-skills/evolve-config.json"
echo "     - Set 'auto_push: true' to auto-commit improvements"
echo "     - Set 'target_repo' to your GitHub repo (e.g. 'you/1ai-skills')"
echo "  2. Start using skills — they'll improve automatically"
echo "  3. Check ~/.1ai-skills/stats.json for skill health"
