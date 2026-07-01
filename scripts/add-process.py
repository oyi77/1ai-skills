#!/usr/bin/env python3
"""
add-process.py — Add ## Process sections to skills missing them.

Generates a basic 3-step process from the skill's name, description, and existing content.

Usage:
    python3 scripts/add-process.py              # Dry run
    python3 scripts/add-process.py --apply       # Apply changes
    python3 scripts/add-process.py --limit 50    # Process max 50
"""

import re, os, sys

DRY_RUN = "--apply" not in sys.argv
LIMIT = None
for i, arg in enumerate(sys.argv):
    if arg == "--limit" and i + 1 < len(sys.argv):
        LIMIT = int(sys.argv[i + 1])

def extract_sections(content: str) -> dict:
    """Extract section headers and their content."""
    sections = {}
    current = None
    lines = []
    for line in content.split("\n"):
        if line.startswith("## "):
            if current:
                sections[current] = "\n".join(lines)
            current = line[3:].strip()
            lines = []
        elif current:
            lines.append(line)
    if current:
        sections[current] = "\n".join(lines)
    return sections

def generate_process(name: str, desc: str, sections: dict) -> str:
    """Generate a Process section based on skill context."""
    clean_name = name.replace("-", " ").replace("_", " ")
    
    # Detect category from content patterns
    is_cyber = any(k in name.lower() for k in ["exploit", "hack", "pentest", "vuln", "malware", "forensic", "detect", "hunt", "attack", "security", "phishing", "breach", "incident"])
    is_dev = any(k in name.lower() for k in ["api", "pattern", "framework", "deploy", "config", "build", "test", "debug", "code", "orm", "database"])
    is_content = any(k in name.lower() for k in ["video", "content", "blog", "seo", "marketing", "social", "email", "campaign"])
    is_ops = any(k in name.lower() for k in ["deploy", "ci-cd", "kubernetes", "docker", "terraform", "monitor", "infra"])
    is_research = any(k in name.lower() for k in ["research", "analyz", "intelligence", "market", "competitor"])
    
    # Extract key verbs from description
    first_word = desc.split()[0].lower() if desc else ""
    
    # Build process steps
    steps = []
    
    if is_cyber:
        steps = [
            "**Reconnaissance** — Gather target information, identify attack surface, enumerate services",
            "**Analysis/Exploitation** — Execute the technique, analyze results, document findings",
            "**Reporting** — Document IOCs, write findings, provide remediation recommendations",
        ]
    elif is_dev:
        steps = [
            "**Design** — Define interface, identify patterns, plan implementation",
            "**Implement** — Write code following existing conventions, add tests",
            "**Verify** — Run tests, check integration, validate behavior",
        ]
    elif is_content:
        steps = [
            "**Research** — Analyze target audience, competitors, and trending topics",
            "**Create** — Generate content following brand guidelines and best practices",
            "**Publish & Optimize** — Distribute to target platforms, track performance, iterate",
        ]
    elif is_ops:
        steps = [
            "**Plan** — Define infrastructure requirements, security constraints, rollback strategy",
            "**Implement** — Configure resources, apply security best practices, test in staging",
            "**Deploy & Monitor** — Roll out to production, verify health checks, set up alerting",
        ]
    elif is_research:
        steps = [
            "**Scope** — Define research questions, identify data sources, set time boundaries",
            "**Gather** — Collect data from primary sources, APIs, and public records",
            "**Synthesize** — Analyze findings, identify patterns, produce actionable report",
        ]
    else:
        # Generic 3-step process
        steps = [
            f"**Prepare** — Gather requirements, verify prerequisites, set up environment",
            f"**Execute** — Run {clean_name} workflow with configured parameters",
            f"**Verify** — Validate output meets requirements, document results",
        ]
    
    process = "\n".join(f"1. {s}" for s in steps)
    return f"\n## Process\n\n{process}\n"

def insert_process(content: str, process_block: str) -> str:
    """Insert Process section before ## Verification or ## Anti-Rationalization or at end."""
    # Try to insert before Verification
    for anchor in ["## Verification", "## Anti-Rationalization", "## Quality Checklist", "## Red Flags"]:
        idx = content.find(anchor)
        if idx > 0:
            return content[:idx] + process_block + "\n" + content[idx:]
    
    # Append at end
    return content.rstrip() + "\n" + process_block

processed = 0
skipped = 0

for root, dirs, files in sorted(os.walk(".")):
    if ".git" in root: continue
    for f in sorted(files):
        if f != "SKILL.md": continue
        path = os.path.join(root, f)
        
        with open(path) as fh:
            content = fh.read()
        
        if "## Process" in content:
            skipped += 1
            continue
        
        if LIMIT and processed >= LIMIT:
            break
        
        # Extract metadata
        name_match = re.search(r'^name:\s*(.+)', content, re.MULTILINE)
        name = name_match.group(1).strip() if name_match else os.path.basename(os.path.dirname(path))
        
        desc_match = re.search(r'description:\s*(?:>\s*)?(.+?)(?:\n\w|\n---)', content, re.DOTALL)
        desc = desc_match.group(1).strip().strip(">").strip() if desc_match else ""
        
        sections = extract_sections(content)
        process_block = generate_process(name, desc, sections)
        new_content = insert_process(content, process_block)
        
        if DRY_RUN:
            print(f"  [DRY] {name}")
        else:
            with open(path, "w") as fh:
                fh.write(new_content)
            print(f"  ✓ {name}")
        
        processed += 1

print(f"\n{'Would process' if DRY_RUN else 'Processed'}: {processed}")
print(f"Skipped (already has Process): {skipped}")
if DRY_RUN:
    print("\nRun with --apply to make changes.")
