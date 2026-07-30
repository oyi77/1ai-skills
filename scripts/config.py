"""
Shared configuration for 1ai-skills tooling.

Single source of truth for category/skill directories.
Both lint-skills.py and test-skills.py import from here.
"""

# ── Skill categories ─────────────────────────────────────────────────────
# Each directory under project root that contains SKILL.md files.
# Must be kept in sync with actual on-disk category directories.
SKILL_DIRS = [
    "agents", "automation", "content", "core", "cybersecurity", "data",
    "development", "devops", "financial", "integrations",
    "marketing", "mcp", "meta", "mindset", "operations", "productivity",
    "research", "sales", "trading",
]
