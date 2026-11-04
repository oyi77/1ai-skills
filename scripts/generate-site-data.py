#!/usr/bin/env python3
"""Generate docs/site-data.json from skill files."""
import json, os, re, sys
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAT_DIRS = ['content', 'core', 'development', 'integrations', 'marketing',
            'meta', 'mindset', 'operations', 'productivity', 'research',
            'sales', 'trading', 'data', 'devops', 'cybersecurity',
            'automation', 'financial', 'mcp', 'agents']

def get_fm(content):
    m = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not m: return {}
    fm = {}
    for line in m.group(1).split('\n'):
        if ':' in line:
            k, _, v = line.partition(':')
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm

cats, skills = {}, []
for root, dirs, files in os.walk(REPO):
    if '.git' in root: continue
    for f in files:
        if f != 'SKILL.md': continue
        path = os.path.join(root, f)
        rel = os.path.relpath(path, REPO)
        parts = rel.split(os.sep)
        cat = parts[0] if parts and parts[0] in CAT_DIRS else 'other'
        with open(path) as fh: content = fh.read()
        fm = get_fm(content)
        name = fm.get('name', os.path.basename(os.path.dirname(path)))
        desc = fm.get('description', '').strip().strip('>').strip()[:160]
        cats[cat] = cats.get(cat, 0) + 1
        skills.append({'name': name, 'description': desc, 'category': cat})

sorted_cats = sorted(cats.items(), key=lambda x: -x[1])
skills.sort(key=lambda x: x['name'])

data = {
    'generated': datetime.now(timezone.utc).isoformat(),
    'total': len(skills),
    'categories': [{'name': c, 'count': n} for c, n in sorted_cats],
    'categoryCount': len(sorted_cats),
    'featured': skills[:18],
    'allSkills': [{'name': s['name'], 'category': s['category']} for s in skills],
}

output_path = os.path.join(REPO, 'docs', 'site-data.json')
try:
    with open(output_path, 'r') as fh:
        old = json.load(fh)
    if {k: v for k, v in old.items() if k != 'generated'} == {k: v for k, v in data.items() if k != 'generated'}:
        print(f'OK: {data["total"]} skills, {data["categoryCount"]} categories (unchanged)')
        sys.exit(0)
except (OSError, ValueError):
    pass

with open(output_path, 'w') as fh:
    json.dump(data, fh, indent=2)
print(f'OK: {data["total"]} skills, {data["categoryCount"]} categories (updated)')
