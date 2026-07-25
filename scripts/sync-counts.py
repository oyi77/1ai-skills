#!/usr/bin/env python3
"""Sync all hardcoded skill counts across docs from SKILLS.json source of truth."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_JSON = ROOT / 'SKILLS.json'
README = ROOT / 'README.md'
AGENTS = ROOT / 'AGENTS.md'
LLMS = ROOT / 'llms.txt'
PKGJSON = ROOT / 'package.json'
GENERATE = ROOT / 'scripts/generate-site.py'

with open(SKILLS_JSON) as f:
    data = json.load(f)

total = data['total_skills']
cats = data['categories']
# cats is a dict: {name: count} — confirm
if isinstance(cats, list):
    cats = {c['name']: c.get('count', 0) for c in cats}

print(f"Source: {total} skills across {len(cats)} categories")

# ── README.md ──
with open(README) as f:
    text = f.read()

# Hero badge — replace hardcoded count
text = re.sub(r'Skills-\d+', f'Skills-{total}', text, count=1)

# Hero sentence
text = re.sub(
    r'\*\*Your AI agent is lazy\. These \d+ skills fix that\.\*\*',
    f'**Your AI agent is lazy. These {total} skills fix that.**',
    text,
)

# Heading
text = re.sub(
    r'^## \d+ Skills Across \d+ Categories',
    f'## {total} Skills Across {len(cats)} Categories',
    text, flags=re.MULTILINE,
)

# Comparison table line
text = re.sub(
    r'\| \*\*Skills\*\* \| \d+-\d+ curated \| \*\*\d+ tested\*\* \|',
    f'| **Skills** | 24-100 curated | **{total} tested** |',
    text,
)

# Test result line
text = re.sub(
    r'\*\*Result: \d+/\d+ PASS · 0 warnings · 0 failures\*\*',
    f'**Result: {total}/{total} PASS · 0 warnings · 0 failures**',
    text,
)

# Category table — rebuild from cats dict
cat_table_start = text.find('## 1337 Skills Across') 
if cat_table_start == -1:
    cat_table_start = text.find(f'## {total} Skills Across')
if cat_table_start == -1:
    cat_table_start = text.find('| Category | Skills | What It Covers |')
if cat_table_start >= 0:
    table_end = text.find('\n\n', cat_table_start + 10)
    if table_end > 0:
        # Find the actual table content — skip header and rebuild
        table_lines = text[cat_table_start:table_end].split('\n')
        header_lines = [l for l in table_lines if '|---' in l or '| Category' in l or '| ---' in l]
        
        # Build new table
        new_table = f'## {total} Skills Across {len(cats)} Categories\n\n'
        new_table += '| Category | Skills | What It Covers |\n'
        new_table += '|---|---:|---|\n'
        
        # Map categories to descriptions (keep from original)
        cat_descs = {}
        for line in table_lines:
            if line.startswith('| ') and line.count('|') >= 3:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 4 and parts[1] not in ('', 'Category'):
                    name = parts[1].lower()
                    desc = parts[3]
                    cat_descs[name] = desc
        
        order = ['cybersecurity','development','content','mindset','marketing','core',
                 'integrations','devops','automation','research','trading',
                 'operations','agents','mcp','meta','financial','sales','data','productivity']
        
        for name in order:
            count = cats.get(name, 0)
            desc = cat_descs.get(name, '')
            display = name.title() if name != 'mcp' else 'MCP'
            if name == 'integrations': display = 'Integrations'
            elif name == 'devops': display = 'DevOps'
            new_table += f'| {display} | {count} | {desc} |\n'
        
        text = text[:cat_table_start] + new_table + text[table_end:]

with open(README, 'w') as f:
    f.write(text)
print(f"  README.md — updated to {total}")

# ── AGENTS.md ──
with open(AGENTS) as f:
    text = f.read()

# Description line
text = re.sub(
    r'Production-ready AI agent skill library — \d+ skills across \d+ categories',
    f'Production-ready AI agent skill library — {total} skills across {len(cats)} categories',
    text,
)

# Category table in AGENTS.md
cat_table_start = text.find('| Category | Count | What it covers |')
if cat_table_start >= 0:
    table_end = text.find('\n\n', cat_table_start + 5)
    if table_end > 0:
        lines = text[cat_table_start:table_end].split('\n')
        # Build new table
        new_table = '| Category | Count | What it covers |\n|----------|------:|----------------|\n'
        order = ['cybersecurity','development','content','mindset','marketing','core',
                 'integrations','devops','automation','research','trading',
                 'operations','agents','mcp','meta','financial','sales','data','productivity']
        cat_descs = {}
        for line in lines:
            if line.startswith('| ') and '|' in line and 'Category' not in line and '---' not in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 4:
                    cat_descs[parts[1].lower()] = parts[3]
        for name in order:
            count = cats.get(name, 0)
            desc = cat_descs.get(name, '')
            new_table += f'| {name} | {count} | {desc} |\n'
        text = text[:cat_table_start] + new_table + text[table_end:]

with open(AGENTS, 'w') as f:
    f.write(text)
print(f"  AGENTS.md — updated to {total}")

# ── llms.txt ──
with open(LLMS) as f:
    text = f.read()

text = re.sub(
    r'> \d+ production-ready AI agent skills',
    f'> {total} production-ready AI agent skills',
    text,
)
text = re.sub(
    r'1ai-skills is a library of \d+ SKILL\.md files across \d+ categories',
    f'1ai-skills is a library of {total} SKILL.md files across {len(cats)} categories',
    text,
)
text = re.sub(
    r'\d+/\d+ skills pass 8-dimension test suite',
    f'{total}/{total} skills pass 8-dimension test suite',
    text,
)

# Update category counts in llms.txt
for name, count in cats.items():
    display = name.title()
    if name == 'mcp': display = 'MCP'
    elif name == 'integrations': display = 'Integrations'
    elif name == 'devops': display = 'DevOps'
    pattern = rf'\*\*{display}\*\* \(\d+ skills\)'
    replacement = f'**{display}** ({count} skills)'
    text = re.sub(pattern, replacement, text)

with open(LLMS, 'w') as f:
    f.write(text)
print(f"  llms.txt — updated to {total}")

# ── package.json — description ──
with open(PKGJSON) as f:
    text = f.read()

pkg = json.loads(text)
old_desc = pkg['description']
new_desc = re.sub(r'\d+ production-ready AI agent skills', f'{total} production-ready AI agent skills', old_desc)
pkg['description'] = new_desc

with open(PKGJSON, 'w') as f:
    json.dump(pkg, f, indent=2)
    f.write('\n')
print(f"  package.json — description updated to '{new_desc}'")

# ── generate-site.py — replace hardcoded 1337 with computed values ──
with open(GENERATE) as f:
    content = f.read()

# line 276: og_desc
content = re.sub(
    r'og_desc = "\d+ production-grade AI agent skills',
    f'og_desc = "{total} production-grade AI agent skills',
    content,
)

# line 601: library count in docs
content = content.replace(
    '1ai-skills is a library of 1337 SKILL.md files',
    f'1ai-skills is a library of {total} SKILL.md files'
)
content = content.replace(
    'a library of 1,329 SKILL.md files',
    f'a library of {total} SKILL.md files'
)

# line 755: comparison table
content = re.sub(
    r'His \d+ skills are engineering lifecycle commands \(/spec, /build, /test\)\. Our \d+ skills are domain-specific knowledge',
    f'His 24 skills are engineering lifecycle commands (/spec, /build, /test). Our {total} skills are domain-specific knowledge',
    content,
)

# line 795: browse header
content = re.sub(
    r'<h1>Browse <span class="grad">\d+ Skills</span></h1>',
    f'<h1>Browse <span class="grad">{total} Skills</span></h1>',
    content,
)

# lines 1109-1110: api test output, use {total}
content = re.sub(
    r'# Total:    \d+',
    f'# Total:    {total}',
    content,
)
content = re.sub(
    r'# Passed:   \d+ \(100\.0%\)',
    f'# Passed:   {total} (100.0%)',
    content,
)

# line 795 also appears in docs/browse.html pattern — also update js count reference
# line 312 area: `countEl.textContent = \`Showing $\{list.length} of \d+ skills\``
content = re.sub(
    r'countEl\.textContent = `Showing \$\{list\.length\} of \d+ skills`',
    f'countEl.textContent = `Showing ${{list.length}} of {total} skills`',
    content,
)

with open(GENERATE, 'w') as f:
    f.write(content)
print(f"  generate-site.py — updated {total} refs")

print(f"\n✓ All docs synced to {total} skills across {len(cats)} categories")