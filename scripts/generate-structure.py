#!/usr/bin/env python3
"""
Generate STRUCTURE.md and _index.md files from SKILLS.json.

Produces:
  - doc/STRUCTURE.md — cross-category human-facing domain index
  - {cat}/_index.md — per-category landing pages with clickable links
  - {subdir}/_index.md — sub-group landing pages (content/video/, etc.)

Usage:
    python3 scripts/generate-structure.py
"""

from pathlib import Path
import json
import os
import sys

ROOT = Path(__file__).resolve().parent.parent
SKILLS_JSON = ROOT / 'SKILLS.json'
OUTPUT_STRUCTURE = ROOT / 'doc' / 'STRUCTURE.md'

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
    """Generate STRUCTURE.md and all _index.md files."""
    skills = load_skills()
    name_path = build_name_path_map()

    # Generate _index.md files
    generate_index_files(skills, name_path)

    # Generate STRUCTURE.md
    print('\n--- STRUCTURE.md ---')

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
            lines.append(f'- [{cat}](../{cat}/_index.md) — {n} skills')
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
        lines.append(f'Browse in [`{cat}/_index.md`](../{cat}/_index.md).')
        lines.append('')

        for s in sorted(cat_skills, key=skill_sort_key):
            name = s.get('name', '?')
            desc = s.get('description', '')
            tags = s.get('tags', [])
            tag_str = ' '.join(f'`{t}`' for t in tags[:5]) if tags else ''
            skill_rel = name_path.get(name)
            if skill_rel:
                lines.append(f'- [{name}](../{skill_rel}/) — {desc}')
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
    OUTPUT_STRUCTURE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_STRUCTURE.write_text(content, encoding='utf-8')
    print(f'  \u2713 {OUTPUT_STRUCTURE.relative_to(ROOT)}')
    print(f'  {len(skills)} skills, {len(grouped)} categories')
    return 0


def _write_index(dir_path, title, skill_entries, name_path, root_rel=None):
    """Write an _index.md with clickable links to skills.

    Args:
        dir_path: Path to the directory where _index.md will be written
        title: Display title (e.g. "Content", "Video")
        skill_entries: List of (name, description, tags) tuples, sorted
        name_path: name → relative-path map for link resolution
        root_rel: str path of dir_path relative to ROOT (for link calculation)
    """
    if root_rel is None:
        root_rel = str(dir_path.relative_to(ROOT))

    lines = [
        f'# {title}',
        '',
        f'## Skills in {title}',
        '',
        f'_Total: {len(skill_entries)}_',
        '',
    ]

    for name, desc, tags in skill_entries:
        skill_rel = name_path.get(name)
        if skill_rel:
            # Relative path from _index.md dir to skill dir
            try:
                rel_link = os.path.relpath(skill_rel, root_rel)
                if not rel_link.startswith('.'):
                    rel_link = './' + rel_link
                # Ensure trailing slash for directory links
                if not rel_link.endswith('/'):
                    rel_link += '/'
                lines.append(f'- [{name}]({rel_link}) — {fmt_desc(desc)}')
            except ValueError:
                lines.append(f'- **{name}** — {fmt_desc(desc)}')
        else:
            lines.append(f'- **{name}** — {fmt_desc(desc)} _(path not found)_')

        if tags:
            tag_str = ' '.join(f'`{t}`' for t in tags[:5])
            lines.append(f'  {tag_str}')
        lines.append('')

    lines.append('---')
    lines.append(f'*Category: {dir_path}*')
    lines.append('')

    content = '\n'.join(lines)
    index_path = dir_path / '_index.md'
    index_path.write_text(content, encoding='utf-8')
    print(f'  ✓ {index_path.relative_to(ROOT)}')


def generate_index_files(skills, name_path):
    """Generate _index.md files for all category and sub-group directories."""
    # Build name → skill lookup
    skill_by_name = {s.get('name'): s for s in skills}

    # Group skills by category from SKILLS.json
    grouped = {}
    for s in skills:
        cat = s.get('category', 'uncategorized')
        grouped.setdefault(cat, []).append(s)

    print('\n--- _index.md files ---')

    # ── Category-level _index.md ──
    for cat in SKILL_DIRS:
        cat_dir = ROOT / cat
        if not cat_dir.is_dir():
            continue
        cat_skills = grouped.get(cat, [])
        entries = []
        for s in sorted(cat_skills, key=skill_sort_key):
            name = s.get('name', '?')
            desc = s.get('description', '')
            tags = s.get('tags', [])
            entries.append((name, desc, tags))
        title = cat.replace('-', ' ').title()
        _write_index(cat_dir, title, entries, name_path)

    # ── Sub-group _index.md ──
    # Find directories with existing _index.md that aren't categories
    for idx_path in sorted(ROOT.rglob('_index.md')):
        if '.git' in idx_path.parts:
            continue
        rel = idx_path.parent.relative_to(ROOT)
        if str(rel) in SKILL_DIRS:
            continue  # category-level, already handled
        sub_dir = idx_path.parent
        sub_rel = str(rel)

        # Find all SKILL.md files under this subdirectory
        skill_mds = sorted(sub_dir.rglob('SKILL.md'))
        skill_mds = [m for m in skill_mds if '.git' not in m.parts]

        # Map to canonical names via name_path (invert: rel_path → name list)
        path_to_names = {}
        for n, p in name_path.items():
            path_to_names.setdefault(p, []).append(n)

        entries = []
        for md in skill_mds:
            md_rel = str(md.parent.relative_to(ROOT))
            for n in path_to_names.get(md_rel, []):
                sk = skill_by_name.get(n, {})
                desc = sk.get('description', '')
                tags = sk.get('tags', [])
                entries.append((n, desc, tags))

        entries.sort(key=lambda x: x[0].lower())
        title = sub_rel.replace('/', ' / ').replace('-', ' ').title()
        _write_index(sub_dir, title, entries, name_path, root_rel=sub_rel)


if __name__ == '__main__':
    import sys
    sys.exit(generate())
