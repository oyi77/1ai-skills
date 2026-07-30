"""Bulk-fix description-long warnings in SKILL.md files.

Scans all SKILL.md files, finds descriptions with yaml-parsed length >200 chars,
and truncates them to ~197 chars while maintaining valid YAML.

Usage: python3 scripts/fix-descriptions.py [--dry-run]
"""
import os
import re
import sys
import yaml

SKILL_DIRS = [
    'core', 'development', 'devops', 'automation', 'content',
    'marketing', 'mindset', 'integrations', 'trading', 'operations',
    'research', 'data', 'agents', 'mcp', 'meta', 'financial',
    'sales', 'productivity', 'cybersecurity',
]

MAX_DESC = 197
MAX_WARN = 200

dry_run = '--dry-run' in sys.argv

fixed = 0
skipped = []
total_over_200 = 0

for cat in SKILL_DIRS:
    base = os.path.join(cat)
    if not os.path.isdir(base):
        continue
    for entry in os.listdir(base):
        skill_path = os.path.join(base, entry, 'SKILL.md')
        if not os.path.isfile(skill_path):
            continue

        text = open(skill_path).read()
        if not text.startswith('---'):
            continue

        # Extract frontmatter
        fm_match = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
        if not fm_match:
            continue

        fm = fm_match.group(1)
        fm_span = fm_match.span()

        # Parse with yaml
        try:
            parsed = yaml.load(fm, Loader=getattr(yaml, 'CSafeLoader', yaml.SafeLoader))
        except yaml.YAMLError:
            skipped.append(f'{cat}/{entry} (yaml error)')
            continue

        if not isinstance(parsed, dict):
            skipped.append(f'{cat}/{entry} (non-dict)')
            continue

        desc = parsed.get('description')
        if desc is None or not isinstance(desc, str):
            continue

        desc = desc.strip()
        if len(desc) <= MAX_WARN:
            continue

        total_over_200 += 1

        # Truncate
        if len(desc) <= MAX_DESC:
            continue  # already short enough after strip

        short = desc[:MAX_DESC]
        short = short.rstrip()
        # Add ellipsis
        short = short + '...'

        # Need to write it back as a valid YAML single line
        # If description contains special chars, quote it
        if any(c in short for c in [':', '#', '{', '}', '[', ']', ',', '&', '*', '?', '|', '-', '<', '>', '=', '!', '%', '@', '`']):
            # Use double quotes, escape any existing quotes or backslashes
            escaped = short.replace('\\', '\\\\').replace('"', '\\"')
            new_desc_line = f'description: "{escaped}"'
        else:
            new_desc_line = f'description: {short}'

        # The old regex just captured one line. The yaml continuation lines
        # are indented. We need to replace the description line AND remove
        # any continuation lines.

        # Split frontmatter into lines
        fm_lines = fm.split('\n')

        # Find the description line
        desc_idx = None
        for i, line in enumerate(fm_lines):
            if line.startswith('description:'):
                desc_idx = i
                break

        if desc_idx is None:
            skipped.append(f'{cat}/{entry} (no desc line)')
            continue

        # Find the end of the description block (next non-indented line or end)
        # Continuation lines are indented with 2 spaces
        end_idx = desc_idx + 1
        while end_idx < len(fm_lines) and (fm_lines[end_idx].startswith('  ') or fm_lines[end_idx] == ''):
            end_idx += 1

        # Replace lines desc_idx..end_idx-1 with the new single line
        old_desc_block = '\n'.join(fm_lines[desc_idx:end_idx])
        fm_lines[desc_idx:end_idx] = [new_desc_line]
        new_fm = '\n'.join(fm_lines)

        # Rebuild the file
        before_fm = text[:fm_span[0]]
        after_fm = text[fm_span[1]:]
        new_text = before_fm + '---\n' + new_fm + '\n---' + after_fm

        if dry_run:
            print(f'  WOULD FIX {cat}/{entry}: {len(desc)}c -> {len(short)}c')
        else:
            with open(skill_path, 'w') as f:
                f.write(new_text)
            fixed += 1

print(f'\nSummary:')
print(f'  Descriptions >200 chars: {total_over_200}')
print(f'  Fixed: {fixed}')
print(f'  Skipped: {len(skipped)}')
if skipped:
    for s in skipped[:10]:
        print(f'    {s}')
    if len(skipped) > 10:
        print(f'    ... and {len(skipped)-10} more')
