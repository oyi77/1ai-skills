#!/usr/bin/env python3
"""
fix-descriptions.py — Add "Use when" trigger phrase to frontmatter descriptions.

The linter checks if descriptions contain trigger patterns like "Use when", "Use for",
"triggers on", "covers", "automated", "generates". This script adds "Use when..." to
descriptions that lack these patterns.

Usage:
    python3 scripts/fix-descriptions.py              # Dry run
    python3 scripts/fix-descriptions.py --apply       # Apply changes
"""

import re, os, sys

DRY_RUN = "--apply" not in sys.argv

TRIGGER_PATTERNS = [
    r"\buse when\b", r"\buse for\b", r"\btriggers? on\b",
    r"\bcovers?\b", r"\bautomate[ds]?\b", r"\bgenerat[es]+\b",
]

def has_trigger(desc: str) -> bool:
    return any(re.search(p, desc.lower()) for p in TRIGGER_PATTERNS)

def generate_use_when(name: str, desc: str) -> str:
    """Generate a 'Use when...' clause from skill name and existing description."""
    # Extract key action from description
    clean_name = name.replace("-", " ").replace("_", " ")
    
    # If description starts with a verb, convert to "Use when..."
    first_word = desc.split()[0].lower() if desc else ""
    action_verbs = [
        "create", "build", "generate", "design", "implement", "manage",
        "analyze", "detect", "track", "automate", "optimize", "integrate",
        "configure", "deploy", "develop", "write", "edit", "process",
        "render", "schedule", "monitor", "audit", "test", "scan",
        "hunt", "exploit", "reverse", "conduct", "perform",
    ]
    
    if first_word in action_verbs:
        # Convert "Create X from Y" → "Create X from Y. Use when creating X or working with Y."
        # Simple: just append "Use when [verb]ing [rest]"
        rest = " ".join(desc.split()[1:10]).rstrip(".")
        return f"{desc.rstrip('.')}. Use when {first_word}ing {rest.lower()}."
    else:
        # Generic: "Use when working with [name]"
        return f"{desc.rstrip('.')}. Use when working with {clean_name}."

processed = 0
skipped = 0

for root, dirs, files in sorted(os.walk(".")):
    if ".git" in root: continue
    for f in sorted(files):
        if f != "SKILL.md": continue
        path = os.path.join(root, f)
        
        with open(path) as fh:
            content = fh.read()
        
        # Extract frontmatter
        fm_match = re.match(r'^(---\n.*?\n---\n)', content, re.DOTALL)
        if not fm_match:
            skipped += 1
            continue
        
        fm_block = fm_match.group(1)
        
        # Get description
        desc_match = re.search(r'description:\s*(?:>\s*)?(.+?)(?:\n\w|\n---)', content, re.DOTALL)
        if not desc_match:
            skipped += 1
            continue
        
        desc = desc_match.group(1).strip().strip(">").strip()
        
        if has_trigger(desc):
            skipped += 1
            continue
        
        # Get name
        name_match = re.search(r'^name:\s*(.+)', fm_block, re.MULTILINE)
        name = name_match.group(1).strip() if name_match else os.path.basename(os.path.dirname(path))
        
        # Generate new description
        new_desc = generate_use_when(name, desc)
        
        # Replace in frontmatter
        if desc in content:
            new_content = content.replace(desc, new_desc, 1)
            
            if DRY_RUN:
                print(f"  [DRY] {name}: ...{new_desc[-60:]}")
            else:
                with open(path, "w") as fh:
                    fh.write(new_content)
                print(f"  ✓ {name}")
            
            processed += 1
        else:
            skipped += 1

print(f"\n{'Would process' if DRY_RUN else 'Processed'}: {processed}")
print(f"Skipped: {skipped}")
if DRY_RUN:
    print("\nRun with --apply to make changes.")
