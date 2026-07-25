#!/usr/bin/env python3
"""Find stub entries and verify SKILLS.json registration."""
import sys, json, importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Load SKILLS.json
data = json.loads((ROOT / 'SKILLS.json').read_text())
json_names = {s['name'] for s in data['skills']}
json_by_name = {s['name']: s for s in data['skills']}

# Load test-skills module
sys.path.insert(0, str(ROOT / 'scripts'))
spec = importlib.util.spec_from_file_location('test_skills', str(ROOT / 'scripts/test-skills.py'))
ts = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ts)

skills = ts.collect_skills()
results, _ = ts.run_tests(skills, quick=True)

stubs = []
for r in results:
    d = r.metrics.get('depth_score', 0)
    q = r.metrics.get('quality_score', 0)
    if d == 0 and q == 0:
        in_json = r.skill in json_names
        stubs.append((r.skill, r.category, r.metrics.get('section_count', 0), r.metrics.get('line_count', 0), in_json))
        flag = "" if in_json else "  NOT IN SKILLS.JSON"
        print(f"  {r.skill:40s}  {r.category:15s}  sec={r.metrics.get('section_count',0):3d}  lines={r.metrics.get('line_count',0):4d}{flag}")

print(f"\nTotal stubs on disk (depth=0 quality=0): {len(stubs)}")

# Cross-reference: which are in SKILLS.json
in_json_stubs = [(n, c, s, l) for n, c, s, l, j in stubs if j]
not_in_json_stubs = [(n, c, s, l) for n, c, s, l, j in stubs if not j]
print(f"In SKILLS.json:      {len(in_json_stubs)}")
print(f"NOT in SKILLS.json:  {len(not_in_json_stubs)}")

if not_in_json_stubs:
    print(f"\nStubs not in SKILLS.json (already removed):")
    for n, c, s, l in not_in_json_stubs:
        print(f"  {n:40s}  {c:15s}")

if in_json_stubs:
    print(f"\nStubs TO REMOVE from SKILLS.json ({len(in_json_stubs)}):")
    cats = {}
    for n, c, s, l in in_json_stubs:
        cats.setdefault(c, []).append(n)
    for c in sorted(cats):
        print(f"  {c}:")
        for n in cats[c]:
            print(f"    - {n}")
    
    # Show category count impact
    print(f"\nCategory count changes required:")
    for c in sorted(cats):
        print(f"  {c}: -{len(cats[c])}")
    print(f"Total removal: {len(in_json_stubs)}")
    print(f"New total_skills: {data['total_skills'] - len(in_json_stubs)}")
