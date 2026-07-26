#!/usr/bin/env python3
"""
Fix compliance gaps in 1ai-skills SKILL.md frontmatter:

1. Tag-format fix: convert `- [tag1\n- tag2]` → proper block list
2. Category fix: repair non-standard category/domain values
3. Duplicate tag fix: remove duplicate entries in tags arrays

Usage: python3 scripts/fix-skill-compliance.py
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

class FixResult:
    def __init__(self):
        self.tag_format = []
        self.category = []
        self.dup_tag = []
        self.errors = []

    def ok(self, fix_type, path, detail):
        getattr(self, fix_type).append((str(path), detail))

    def err(self, path, msg):
        self.errors.append((str(path), msg))

    def report(self):
        total = len(self.tag_format) + len(self.category) + len(self.dup_tag)
        print(f"\n{'='*60}")
        print(f"Fix Report: {total} files fixed ({len(self.errors)} errors)")
        print(f"  Tag-format fixes: {len(self.tag_format)}")
        print(f"  Category fixes:   {len(self.category)}")
        print(f"  Duplicate tag:    {len(self.dup_tag)}")
        if self.errors:
            print(f"\n  ERRORS:")
            for p, m in self.errors:
                print(f"    ! {p}: {m}")
        print(f"{'='*60}\n")

fix = FixResult()


# ──────────────────────────────────────────────
# 1. Category fixes — 9 skills
# ──────────────────────────────────────────────
# Mapping: relative SKILL.md path → list of (field, old_value, new_value)
category_fixes = {
    "automation/scrapers/agent-reach-channels/SKILL.md": [
        ("category", "automation/scrapers", "automation"),
    ],
    "content/video/auto-clipper/SKILL.md": [
        ("domain", "video", "content"),
    ],
    "content/video/faceless-youtube/SKILL.md": [
        ("domain", "video", "content"),
    ],
    "content/writing/SKILL.md": [
        ("domain", "content/writing", "content"),
    ],
    "data/analysis/SKILL.md": [
        ("domain", "data/analysis", "data"),
    ],
    "devops/docker/SKILL.md": [
        ("domain", "devops/docker", "devops"),
    ],
    "finance/investment-bottleneck/SKILL.md": [
        ("category", "investment", "finance"),
    ],
    "finance/investment-industry/SKILL.md": [
        ("category", "investment", "finance"),
    ],
    "finance/investment-earnings/SKILL.md": [
        ("category", "investment", "finance"),
    ],
}

for rel_path, ops in category_fixes.items():
    path = ROOT / rel_path
    if not path.exists():
        fix.err(path, "File not found")
        continue
    text = path.read_text()
    # Extract frontmatter (between first two --- separators)
    m = re.match(r'^(-{3,})\n(.*?)\n\1', text, re.DOTALL)
    if not m:
        fix.err(path, "No valid YAML frontmatter found")
        continue
    fm_raw = m.group(2)
    result = text
    for field, old_val, new_val in ops:
        # Replace `field: old_val` with `field: new_val` in frontmatter
        pattern = rf'^{re.escape(field)}:\s*{re.escape(old_val)}\s*$'
        new_line = f"{field}: {new_val}"
        if re.search(pattern, fm_raw, re.MULTILINE):
            result = re.sub(pattern, new_line, result, flags=re.MULTILINE)
            fix.ok("category", path, f"{field}: {old_val} → {new_val}")
        else:
            fix.err(path, f"Pattern '{field}: {old_val}' not found in frontmatter")
    path.write_text(result)


# ──────────────────────────────────────────────
# 2. Tag-format fixes — 15 skills
# ──────────────────────────────────────────────
tag_format_skills = [
    "core/agent-harness-optimizer/SKILL.md",
    "core/agent-security-scanner/SKILL.md",
    "core/karpathy-coding-principles/SKILL.md",
    "core/ai-engineering-curriculum/SKILL.md",
    "development/agentic-quality-engineering/SKILL.md",
    "development/automated-test-generator/SKILL.md",
    "development/engineering-hard-rules/SKILL.md",
    "development/free-dev-resources/SKILL.md",
    "development/qa-review-fix-loop/SKILL.md",
    "devops/free-cloud-infrastructure/SKILL.md",
    "integrations/free-saas-toolkit/SKILL.md",
    "meta/skill-evolution-engine/SKILL.md",
    "productivity/career-ops/SKILL.md",
    "productivity/focus-time-management/SKILL.md",
    "productivity/meeting-management/SKILL.md",
]

for rel_path in tag_format_skills:
    path = ROOT / rel_path
    if not path.exists():
        fix.err(path, "File not found")
        continue
    text = path.read_text()

    # Pattern: `tags: \n- [tag1\n- tag2\n- ...tagN]`
    # This is YAML: a block sequence with one element — a flow sequence [tag1, tag2, ...]
    # The closing ] may be on the last tag line.
    # Fix: rewrite as `tags:\n  - tag1\n  - tag2\n  - ...\n`

    # Find the tags block and the closing ]
    tags_match = re.search(
        r'^tags:\s*\n((?:\s*-\s*\[?(?:[^\n\[\]]+))+(?:\])?\s*)',
        text, re.MULTILINE
    )
    if not tags_match:
        fix.err(path, "Could not find tags block in expected format")
        continue

    tags_block = tags_match.group(1)
    # Extract tag names (stuff after - and optional [)
    tags = re.findall(r'-\s*\[?(.+?)(?:\])?$', tags_block, re.MULTILINE)
    tags = [t.strip() for t in tags if t.strip()]

    if not tags:
        fix.err(path, "No tags extracted")
        continue

    # Build the replacement
    indentation = "  "  # 2-space indent
    new_tags_block = "\n".join(f"{indentation}- {t}" for t in tags)

    # Replace the tags block
    new_text = text[:tags_match.start(1)] + new_tags_block + text[tags_match.end(1):]

    # Handle case where tags section had more indented lines after the tags
    # (e.g., persona, expertise fields after tags in agent-harness-optimizer)
    path.write_text(new_text)
    fix.ok("tag_format", path, f"{len(tags)} tags: {', '.join(tags[:5])}...")


# ──────────────────────────────────────────────
# 3. Duplicate tag fix — clay-art-video-generator
# ──────────────────────────────────────────────
path = ROOT / "content/video/clay-art-video-generator/SKILL.md"
if path.exists():
    text = path.read_text()
    # Also fix domain: video → domain: content here
    text = re.sub(r'^domain:\s*video\s*$', 'domain: content', text, flags=re.MULTILINE)

    # Fix the tags to remove duplicate 'video'
    # The frontmatter has: tags: [clay, art, video, generator, video]
    m = re.match(r'^(-{3,})\n(.*?)\n\1', text, re.DOTALL)
    if m:
        fm_raw = m.group(2)
        # Find the tags line
        tags_line_match = re.search(r'^tags:\s*\[(.+?)\]\s*$', fm_raw, re.MULTILINE)
        if tags_line_match:
            tag_str = tags_line_match.group(1)
            tag_list = [t.strip() for t in tag_str.split(',')]
            # Remove duplicates while preserving order
            seen = set()
            deduped = []
            for t in tag_list:
                if t not in seen:
                    seen.add(t)
                    deduped.append(t)
            if len(deduped) < len(tag_list):
                new_tag_str = ', '.join(deduped)
                text = text.replace(f'[{tag_str}]', f'[{new_tag_str}]')
                fix.ok("dup_tag", path, f"Removed dupes: {set(tag_list) - seen}")
            else:
                fix.err(path, "No duplicate tags found in flow sequence")
        else:
            fix.err(path, "Could not find tags flow sequence")
    path.write_text(text)

fix.report()
