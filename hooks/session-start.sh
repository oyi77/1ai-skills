#!/bin/bash
PROJECT_DIR="${1:-.}"
SKILL_BASE="${HOME}/.claude/skills/1ai-skills"

echo "[hooks] Session start: detecting project type in $PROJECT_DIR"

if [ -f "$PROJECT_DIR/package.json" ]; then
  echo "[hooks] Node.js project detected"
  echo "[hooks] Available: development/systematic-debugging, development/test-driven-development"
fi

if [ -f "$PROJECT_DIR/requirements.txt" ] || [ -f "$PROJECT_DIR/pyproject.toml" ]; then
  echo "[hooks] Python project detected"
  echo "[hooks] Available: research/comprehensive_research, research/feynman-science"
fi

if [ -f "$PROJECT_DIR/Cargo.toml" ]; then
  echo "[hooks] Rust project detected"
  echo "[hooks] Available: development/code-reviewer, development/systematic-debugging"
fi

if grep -q "next\|react\|vue\|svelte" "$PROJECT_DIR/package.json" 2>/dev/null; then
  echo "[hooks] Frontend project detected"
  echo "[hooks] Available: development/frontend-ui-engineering, content/minimalist-design"
fi

if [ -f "$PROJECT_DIR/seo-config.json" ] || grep -q "seo\|meta.*tag\|open.*graph" "$PROJECT_DIR"/*.html 2>/dev/null; then
  echo "[hooks] SEO project detected"
  echo "[hooks] Available: marketing/seo-optimizer, marketing/content-marketing"
fi

if curl -s http://localhost:9099/brain/status > /dev/null 2>&1; then
  echo "[hooks] bk-hub brain detected — loading session-brain skill"
fi

# Auto-detect hooks health
if command -v node &> /dev/null; then
  node "$(dirname "$0")/session-start-detect.js" 2>/dev/null || true
fi

echo "[hooks] Session start complete. Use /find-skills to discover more capabilities."
