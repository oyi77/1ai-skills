#!/usr/bin/env python3
"""
Phase 3b: Bulk Anti-Rationalization Table normalization.

Fixes three classes of issues across all SKILL.md files:
1. Rename `## Anti-Rationalization` → `## Anti-Rationalization Table` (1130 files)
2. Split concatenated `## Anti-Rationalization Table| Rationalization | Reality | |---|---` into proper format (2 files)
3. Add `## Anti-Rationalization Table` section to files missing it entirely (201 files)

Usage: python3 scripts/bulk-fix-ar-table.py [--dry-run] [--verify]
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Generic AR table template for files that have none
AR_TABLE_TEMPLATE = """\
## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll figure it out as I go" | A structured approach saves time and reduces errors. Follow the workflow in this skill rather than improvising. |
| "I already know this topic" | Familiarity breeds shortcuts. Use the checklist to verify you haven't missed critical steps. |
| "This doesn't apply to my situation" | The patterns here generalize across contexts. Adapt, don't skip — the underlying principles hold. |
| "One more tool will fix it" | Adding complexity rarely solves process gaps. Master the core workflow first. |
"""


def fix_ar_header(text: str) -> str:
    """
    Normalize Anti-Rationalization headers in a SKILL.md body.
    
    Cases handled:
    1. `## Anti-Rationalization` (no "Table") → `## Anti-Rationalization Table`
    2. `## Anti-Rationalization Table| Rationalization | Reality | |---` → split into proper format
    """
    # Case 2: Concatenated header - line looks like:
    # ## Anti-Rationalization Table| Rationalization | Reality | |---
    # Replace just the leading header part, keeping the table content on next lines
    text = re.sub(
        r'^## Anti-Rationalization Table\|.*',
        '## Anti-Rationalization Table\n\n| Rationalization | Reality |\n|---|---|',
        text,
        flags=re.MULTILINE
    )
    # Clean up duplicate `\n|---|---|\n|---\n` left when the original
    # concatenated line was followed by `\n|---\n` (the next line was a separator)
    text = re.sub(r'(\|-{3,}\|)\n\|-{3,}\n', r'\1\n', text)
    
    
    # Case 1: Plain old-format header
    # Replace `## Anti-Rationalization` (NOT followed by ` Table` already)
    text = re.sub(
        r'^## Anti-Rationalization(?! Table)',
        '## Anti-Rationalization Table',
        text,
        flags=re.MULTILINE
    )
    
    return text


def has_ar_section(text: str) -> bool:
    """Check if any form of Anti-Rationalization section exists."""
    return bool(re.search(r'## Anti-Rationalization', text))


def has_when_to_use(text: str) -> bool:
    """Check if When to Use section exists."""
    return bool(re.search(r'^## When to Use', text, re.MULTILINE))


def add_ar_table_section(text: str) -> str:
    """
    Add a basic Anti-Rationalization Table section to a file that lacks one.
    Inserts before `## When to Use` if present, otherwise appends at end.
    """
    # Check if there's a When to Use section to insert before
    match = re.search(r'^## When to Use', text, re.MULTILINE)
    if match:
        pos = match.start()
        # Add a blank line before the new section if needed
        prefix = '\n' if pos > 0 and text[pos-1] != '\n' else ''
        return text[:pos] + prefix + '\n' + AR_TABLE_TEMPLATE + '\n' + text[pos:]
    else:
        # Append to end
        if text.endswith('\n'):
            return text + '\n' + AR_TABLE_TEMPLATE
        else:
            return text + '\n\n' + AR_TABLE_TEMPLATE


def main():
    dry_run = '--dry-run' in sys.argv
    
    skill_files = sorted(ROOT.rglob('SKILL.md'))
    # Filter out hidden dirs and node_modules
    skill_files = [
        f for f in skill_files
        if not any(p.startswith('.') for p in f.relative_to(ROOT).parts)
        and 'node_modules' not in f.parts
    ]
    
    rename_count = 0       # Case 1: old header → new header
    concat_count = 0       # Case 2: concatenated → proper format
    add_count = 0          # Case 3: no AR section → add template
    unchanged = 0          # Already has proper AR Table
    no_change_needed = 0   # Files needing no fix (already correct)
    errors = []
    
    for fpath in skill_files:
        rel = fpath.relative_to(ROOT)
        try:
            text = fpath.read_text()
        except Exception as e:
            errors.append(f"Cannot read {rel}: {e}")
            continue
        
        original = text
        
        # Check cases
        needs_rename = bool(re.search(r'^## Anti-Rationalization(?! Table)', text, re.MULTILINE))
        needs_concat_fix = bool(re.search(r'^## Anti-Rationalization Table\|', text, re.MULTILINE))
        needs_add = not has_ar_section(text)
        
        if needs_concat_fix:
            text = fix_ar_header(text)
            concat_count += 1
            # After fixing concatenated, check if it also needs rename
            # (unlikely but handle)
            needs_rename = bool(re.search(r'^## Anti-Rationalization(?! Table)', text, re.MULTILINE))
        
        if needs_rename:
            text = fix_ar_header(text)
            rename_count += 1
        
        if needs_add:
            text = add_ar_table_section(text)
            add_count += 1
        
        if text == original:
            no_change_needed += 1
            continue
        
        if dry_run:
            print(f"[DRY-RUN] Would fix: {rel}")
            if needs_concat_fix:
                print(f"         Reason: concatenated header")
            if needs_rename:
                print(f"         Reason: old-format header")
            if needs_add:
                print(f"         Reason: missing AR section")
        else:
            try:
                fpath.write_text(text)
                flags = []
                if needs_concat_fix: flags.append("concat")
                if needs_rename: flags.append("rename")
                if needs_add: flags.append("add")
                print(f"  Fixed: {rel}  [{','.join(flags)}]")
            except Exception as e:
                errors.append(f"Cannot write {rel}: {e}")
                continue
    
    print(f"\n--- Summary ---")
    print(f"Total SKILL.md files scanned: {len(skill_files)}")
    print(f"Renamed headers (old→Table): {rename_count}")
    print(f"Fixed concatenated headers: {concat_count}")
    print(f"Added AR Table sections: {add_count}")
    print(f"Already correct (unchanged): {no_change_needed}")
    if dry_run:
        print(f"DRY RUN — no files were modified")
    else:
        print(f"Files modified: {rename_count + concat_count + add_count}")
    
    if errors:
        print(f"\nERRORS ({len(errors)}):")
        for e in errors:
            print(f"  {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
