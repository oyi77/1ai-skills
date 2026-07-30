#!/usr/bin/env python3
"""
Generate doc/STRUCTURE.md from SKILLS.json — human-facing domain index.

Produces a hierarchical listing of all skill categories and their skills
with descriptions, count aggregates, and links to _index.md files.

Usage:
    python3 scripts/generate-structure.py
"""

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent.parent
SKILLS_JSON = ROOT / 'SKILLS.json'
OUTPUT = ROOT / 'doc' / 'STRUCTURE.md'

from config import SKILL_DIRS  # shared category definitions


def load_skills():
    """Load skills from SKILLS.json."""
    with open(SKILLS_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('skills', [])


def build_name_path_map():
    """Build name → relative path mapping by scanning filesystem.

    The canonical `name` in frontmatter may differ from the directory
    basename after path deduplication (e.g. name=kalodata-dashboard
    lives at integrations/kalodata/dashboard/).
    """
    import re
    name_path = {}
    for md in ROOT.rglob('SKILL.md'):
        if '.git' in md.parts:
            continue
        try:
            text = md.read_text(encoding='utf-8')
            m = re.search(r'^name:\s*(.+)$', text[:500], re.MULTILINE)
            if m:
                name = m.group(1).strip().strip("'\"").strip()
                rel = str(md.parent.relative_to(ROOT))
                name_path[name] = rel
        except Exception:
            pass
    return name_path


def skill_sort_key(skill):
    """Sort skills: name."""
    return skill.get('name', '').lower()


def fmt_desc(desc, max_len=100):
    """Truncate description to max_len with ellipsis."""
    if len(desc) > max_len:
        return desc[:max_len - 3] + '...'
    return desc


def generate():
    """Generate the STRUCTURE.md file."""
    skills = load_skills()
    name_path = build_name_path_map()
    output = ROOT / 'doc' / 'STRUCTURE.md'

    # Group by category
    grouped = {}
    for s in skills:
        cat = s.get('category', 'uncategorized')
        grouped.setdefault(cat, []).append(s)

    lines = [
        '# 1ai-skills Structure',
        '',
        'Auto-generated from `SKILLS.json`. Last generated: `python3 scripts/generate-structure.py`',
        '',
        '---',
        '',
        '## Overview',
        '',
        f'**{len(skills)} skills** across **{len(grouped)} categories**.',
        '',
        '---',
        '',
    ]

    # Table of Contents
    lines.append('## Category Index')
    lines.append('')
    for cat in SKILL_DIRS:
        if cat in grouped:
            n = len(grouped[cat])
            lines.append(f'- [{cat}](/{cat}/_index.md) — {n} skills')
    lines.append('')
    lines.append('---')
    lines.append('')

    # Detailed per-category listing
    lines.append('## Skills by Category')
    lines.append('')

    for cat in SKILL_DIRS:
        if cat not in grouped:
            continue
        cat_skills = grouped[cat]
        title = cat.replace('-', ' ').title()
        lines.append(f'### {title} ({cat}/)')
        lines.append('')
        lines.append(f'_Total: {len(cat_skills)} skills_')
        lines.append('')
        lines.append(f'Browse in [`{cat}/_index.md`](/{cat}/_index.md).')
        lines.append('')

        for s in sorted(cat_skills, key=skill_sort_key):
            name = s.get('name', '?')
            desc = s.get('description', '')
            tags = s.get('tags', [])
            tag_str = ' '.join(f'`{t}`' for t in tags[:5]) if tags else ''
            skill_rel = name_path.get(name)
            if skill_rel:
                lines.append(f'- [{name}](/{skill_rel}/) — {desc}')
            else:
                lines.append(f'- **{name}** — {desc} _(path not found)_')
            if tag_str:
                lines.append(f'  {tag_str}')
            lines.append('')

    # Footer
    lines.append('---')
    lines.append(f'_Generated from {len(skills)} skills across {len(grouped)} categories._')
    lines.append('')

    content = '\n'.join(lines)

    # Ensure doc/ exists
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding='utf-8')
    print(f'✓ {output.relative_to(ROOT)}')
    print(f'  {len(skills)} skills, {len(grouped)} categories')
    return 0


if __name__ == '__main__':
    sys.exit(generate())
