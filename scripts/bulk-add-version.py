#!/usr/bin/env python3
"""Bulk-add `version: 1.0.0` to SKILL.md files missing it in frontmatter."""

import os
import re
import sys
import glob
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CATEGORIES = [
    "agents", "automation", "content", "core", "cybersecurity",
    "data", "development", "devops", "financial", "integrations",
    "marketing", "mcp", "meta", "mindset", "operations", "productivity",
    "research", "sales", "trading",
]

FM_PATTERN = re.compile(
    r'^---\n(?P<fm>.*?)\n^---\n',
    re.MULTILINE | re.DOTALL
)

def find_skills_missing_version():
    """Find all SKILL.md files without `version:` in frontmatter."""
    missing = []
    for cat in CATEGORIES:
        pattern = str(REPO / cat / "**" / "SKILL.md")
        for path in glob.glob(pattern, recursive=True):
            with open(path, 'r') as f:
                content = f.read()
            m = FM_PATTERN.match(content)
            if not m:
                continue
            fm = m.group('fm')
            if 'version:' not in fm:
                missing.append(path)
    return missing

def add_version(paths, dry_run=False):
    """Add `version: 1.0.0` to frontmatter of each file, before closing ---."""
    modified = 0
    for path in sorted(paths):
        with open(path, 'r') as f:
            content = f.read()
        m = FM_PATTERN.match(content)
        if not m:
            print(f"  WARN: no frontmatter in {path}")
            continue
        
        # Insert version: 1.0.0 before the closing ---\n delimiter
        # m.end(0) is past \n---\n; m.end(0)-5 = start of \n---\n
        new_content = content[:m.end(0)-5] + '\nversion: 1.0.0' + content[m.end(0)-5:]

        if dry_run:
            modified += 1
        else:
            with open(path, 'w') as f:
                f.write(new_content)
            modified += 1
            if modified % 100 == 0:
                print(f"  ... {modified} done")
    
    return modified

if __name__ == '__main__':
    dry_run = '--dry-run' in sys.argv
    
    print("Finding SKILL.md files without version field...")
    missing = find_skills_missing_version()
    print(f"Skills missing version: {len(missing)}")
    
    if not missing:
        print("Nothing to do.")
        sys.exit(0)
    
    print(f"{'DRY RUN — would modify' if dry_run else 'Modifying'} {len(missing)} files...")
    modified = add_version(missing, dry_run=dry_run)
    
    print(f"\n{'[DRY-RUN] Would modify' if dry_run else 'Modified'}: {modified} files")
    if dry_run:
        print("Run without --dry-run to apply changes.")
