#!/usr/bin/env python3
"""
add-triggers.py — Batch add trigger phrases to skills missing them.

Reads skill name + description from SKILL.md frontmatter, generates natural
language trigger phrases, and inserts them into the When to Use section.

Usage:
    python3 scripts/add-triggers.py              # Dry run (preview)
    python3 scripts/add-triggers.py --apply      # Apply changes
    python3 scripts/add-triggers.py --limit 50   # Process max 50 skills
"""

import re, os, sys

DRY_RUN = "--apply" not in sys.argv
LIMIT = None
for i, arg in enumerate(sys.argv):
    if arg == "--limit" and i + 1 < len(sys.argv):
        LIMIT = int(sys.argv[i + 1])

def slug_to_phrases(name: str, desc: str, category: str) -> list[str]:
    """Generate trigger phrases from skill name and description."""
    phrases = []
    
    # From name: convert slug to natural phrases
    clean = name.replace("-", " ").replace("_", " ")
    phrases.append(f'"{clean}"')
    
    # Split name into meaningful parts
    parts = name.split("-")
    
    # If name has verb-noun pattern, generate "verb the noun" variant
    if len(parts) >= 2:
        # Common verb patterns
        verbs = ["help", "create", "build", "make", "generate", "set up", "configure",
                 "analyze", "detect", "implement", "perform", "conduct", "test",
                 "scan", "hunt", "exploit", "reverse", "deploy", "audit", "fix",
                 "optimize", "automate", "manage", "design", "develop", "write"]
        
        first = parts[0].lower()
        if first in verbs:
            rest = " ".join(parts[1:])
            phrases.append(f'"{first} {rest}"')
            phrases.append(f'"{first}ing {rest}"')
    
    # From description: extract key phrases
    if desc:
        # Get first sentence
        first_sent = desc.split(".")[0][:80]
        if first_sent and first_sent != clean:
            phrases.append(f'"{first_sent}"')
    
    # Category-specific patterns
    cat_triggers = {
        "cybersecurity": ["security", "pentest", "vulnerability"],
        "marketing": ["marketing", "campaign", "growth"],
        "trading": ["trading", "strategy", "market"],
        "development": ["coding", "debug", "refactor"],
    }
    if category in cat_triggers:
        for t in cat_triggers[category]:
            if t in name.lower() or (desc and t in desc.lower()):
                phrases.append(f'"{t} {clean}"')
                break
    
    # Deduplicate, limit to 4
    seen = set()
    unique = []
    for p in phrases:
        p_lower = p.lower()
        if p_lower not in seen:
            seen.add(p_lower)
            unique.append(p)
    
    return unique[:4]


def get_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter."""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}
    
    fm = {}
    for line in match.group(1).split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm


def has_trigger_section(content: str) -> bool:
    """Check if skill already has trigger phrases."""
    return bool(re.search(r'(Trigger phrases|Use when|trigger)', content[:3000], re.IGNORECASE))


def insert_triggers(content: str, name: str, phrases: list[str]) -> str:
    """Insert trigger phrases into the When to Use section."""
    
    # Find "## When to Use" section
    when_match = re.search(r'(## When to Use\n)', content)
    if when_match:
        insert_pos = when_match.end()
        trigger_block = "**Trigger phrases:**\n"
        for p in phrases:
            trigger_block += f"- {p}\n"
        trigger_block += "\n"
        return content[:insert_pos] + trigger_block + content[insert_pos:]
    
    # If no "## When to Use", add after frontmatter
    fm_match = re.match(r'(---\n.*?\n---\n)', content, re.DOTALL)
    if fm_match:
        insert_pos = fm_match.end()
        trigger_block = f"\n## When to Use\n\n**Trigger phrases:**\n"
        for p in phrases:
            trigger_block += f"- {p}\n"
        trigger_block += "\n"
        return content[:insert_pos] + trigger_block + content[insert_pos:]
    
    return content


# Main
processed = 0
skipped = 0
errors = 0

for root, dirs, files in sorted(os.walk(".")):
    if ".git" in root: continue
    for f in sorted(files):
        if f != "SKILL.md": continue
        path = os.path.join(root, f)
        
        with open(path) as fh:
            content = fh.read()
        
        if has_trigger_section(content):
            skipped += 1
            continue
        
        if LIMIT and processed >= LIMIT:
            break
        
        # Extract metadata
        fm = get_frontmatter(content)
        name = fm.get("name", os.path.basename(os.path.dirname(path)))
        desc = fm.get("description", "").strip().strip(">")
        
        # Determine category from path
        parts = root.split("/")
        category = parts[2] if len(parts) > 2 else "root"
        
        # Generate phrases
        phrases = slug_to_phrases(name, desc, category)
        
        if not phrases:
            errors += 1
            continue
        
        # Insert
        new_content = insert_triggers(content, name, phrases)
        
        if DRY_RUN:
            print(f"  [DRY] {name}: {', '.join(phrases)}")
        else:
            with open(path, "w") as fh:
                fh.write(new_content)
            print(f"  ✓ {name}: {', '.join(phrases)}")
        
        processed += 1

print(f"\n{'Would process' if DRY_RUN else 'Processed'}: {processed}")
print(f"Skipped (already has triggers): {skipped}")
print(f"Errors (no phrases generated): {errors}")
if DRY_RUN:
    print("\nRun with --apply to make changes.")
