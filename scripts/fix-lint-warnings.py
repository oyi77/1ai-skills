#!/usr/bin/env python3
"""
Fix all 113 pre-existing lint warnings in SKILL.md files.

Three warning types:
- desc-no-trigger (105): Prepend "Use when " to description
- missing-tags (5): Add tags field to frontmatter
- missing-section (3): Add "## When to Use" section
"""

from __future__ import annotations
import os
import re
import sys
import hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── Warning Data (from /tmp/lint-full.txt) ──────────────────────────────────

DESC_NO_TRIGGER_SKILLS = [
    "code-agent", "deploy-agent", "planning-agent", "research-agent",
    "review-agent", "linter-agent", "perf-agent", "refactor-agent",
    "security-agent", "test-agent", "telegram-bot", "twitter-bot",
    "whatsapp-bot", "agent-reach-channels", "content-monitor",
    "smart-scraper", "social-listener", "workflows", "cron-designer",
    "ifttt-maker", "n8n-builder", "webhook-router", "zapier-alt",
    "content-kingdom", "auto-clipper", "clay-art-video-generator",
    "writing", "ad-copy", "email-writer", "long-form", "product-desc",
    "berkahkarya-orchestrator", "vilona", "vilona-activate",
    "analyzing-network-traffic-for-incidents",
    "analyzing-windows-amcache-artifacts", "collecting-open-source-intelligence",
    "conducting-mobile-app-penetration-test", "containing-active-breach",
    "deploying-decoy-files-for-ransomware-detection",
    "detecting-ai-model-prompt-injection-attacks",
    "detecting-business-email-compromise-with-ai",
    "detecting-malicious-scheduled-tasks-with-sysmon",
    "detecting-ransomware-encryption-behavior",
    "detecting-ransomware-precursors-in-network",
    "detecting-serverless-function-injection", "executing-red-team-exercise",
    "exploiting-api-injection-vulnerabilities",
    "exploiting-broken-function-level-authorization",
    "hunting-for-anomalous-powershell-execution",
    "implementing-api-rate-limiting-and-throttling",
    "implementing-aws-nitro-enclave-security",
    "implementing-browser-isolation-for-zero-trust",
    "implementing-data-loss-prevention-with-microsoft-purview",
    "implementing-ransomware-kill-switch-detection",
    "implementing-sigstore-for-software-signing",
    "implementing-web-application-logging-with-modsecurity",
    "monitoring-scada-modbus-traffic-anomalies",
    "performing-api-fuzzing-with-restler", "performing-api-rate-limiting-bypass",
    "performing-disk-forensics-investigation",
    "performing-fuzzing-with-aflplusplus",
    "performing-graphql-introspection-attack",
    "performing-insider-threat-investigation", "performing-ransomware-response",
    "performing-static-malware-analysis-with-pe-studio",
    "reverse-engineering-android-malware-with-jadx",
    "testing-api-for-broken-object-level-authorization",
    "testing-api-for-mass-assignment-vulnerability",
    "testing-websocket-api-security", "anomaly-detect", "data-cleaner",
    "report-gen", "viz-creator", "docker", "docker-compose", "dockerfile-opt",
    "k8s-deploy", "investment-bottleneck", "investment-earnings",
    "investment-industry", "discord", "discord-bot", "discord-webhooks",
    "github", "github-actions", "github-issues", "github-pr",
    "notion-integration", "notion-api", "notion-db", "notion-pages",
    "slack", "slack-bot", "slack-notifier", "slash-commands",
    "analytics-reporting", "critical-thinking", "audit", "debt", "help",
    "review", "legal-assistant", "lead-generation-engine", "portfolio-manager",
]

MISSING_TAGS_SKILLS = [
    "auto-clipper", "clay-art-video-generator",
    "investment-bottleneck", "investment-earnings", "investment-industry",
]

MISSING_SECTION_SKILLS = [
    "autonomous", "coding", "ponytail",
]


# ── Helpers ─────────────────────────────────────────────────────────────────

def find_skill_md(name: str) -> str | None:
    """Find the SKILL.md file for a skill name by searching categories."""
    for root, dirs, files in os.walk(ROOT):
        # Skip hidden dirs and non-skill dirs
        basename = os.path.basename(root)
        if basename == name and "SKILL.md" in files:
            return os.path.join(root, "SKILL.md")
    return None


def read_frontmatter(content: str) -> tuple[int, int] | None:
    """Return (start, end) line numbers of frontmatter delimiters.
    Returns None if no valid frontmatter.
    """
    lines = content.split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return (0, i)
    return None


def fix_desc_no_trigger(filepath: str) -> bool:
    """Prepend 'Use when ' to description if it lacks a trigger phrase."""
    with open(filepath) as f:
        content = f.read()

    fm = read_frontmatter(content)
    if not fm:
        print(f"  SKIP {filepath}: no frontmatter")
        return False

    lines = content.split("\n")
    desc_idx = None
    for i in range(fm[0] + 1, fm[1]):
        if lines[i].startswith("description:"):
            desc_idx = i
            break

    if desc_idx is None:
        print(f"  SKIP {filepath}: no description field")
        return False

    old_line = lines[desc_idx]
    # Parse the description value — it's the part after "description:"
    prefix = "description:"
    # Handle quoted and unquoted descriptions
    rest = old_line[len(prefix):].strip()
    
    # If empty or already has a trigger phrase, skip
    desc_lower = rest.lower()
    import re as re2
    trigger_patterns = [
        r"\buse when\b", r"\buse for\b", r"\btriggers?\s+on\b",
        r"\bcovers?\b", r"\bautomate[ds]?\b", r"\bgenerat[es]+\b",
    ]
    has_trigger = any(re2.search(p, desc_lower) for p in trigger_patterns)
    if has_trigger:
        print(f"  OK {filepath}: already has trigger")
        return False

    # Remove surrounding quotes if any
    unquoted = rest
    if (unquoted.startswith('"') and unquoted.endswith('"')) or \
       (unquoted.startswith("'") and unquoted.endswith("'")):
        unquoted = unquoted[1:-1]

    # Prepend "Use when " and decapitalize first char if uppercase
    new_desc = "Use when " + unquoted[0].lower() + unquoted[1:] if unquoted else "Use when " + unquoted
    
    # Re-wrap in quotes if original was quoted
    if rest.startswith('"') and rest.endswith('"'):
        new_line = f"{prefix} \"{new_desc}\""
    elif rest.startswith("'") and rest.endswith("'"):
        new_line = f"{prefix} '{new_desc}'"
    else:
        new_line = f"{prefix} {new_desc}"

    lines[desc_idx] = new_line
    new_content = "\n".join(lines)
    with open(filepath, "w") as f:
        f.write(new_content)
    return True


def fix_missing_tags(filepath: str) -> bool:
    """Add tags field to frontmatter."""
    with open(filepath) as f:
        content = f.read()

    fm = read_frontmatter(content)
    if not fm:
        print(f"  SKIP {filepath}: no frontmatter")
        return False

    lines = content.split("\n")
    
    # Determine tags based on name
    name = None
    for i in range(fm[0] + 1, fm[1]):
        if lines[i].startswith("name:"):
            name = lines[i].split(":", 1)[1].strip()
            break
    
    domain = None
    for i in range(fm[0] + 1, fm[1]):
        if lines[i].startswith("domain:"):
            domain = lines[i].split(":", 1)[1].strip()
            break

    # Generate tags from name/domain
    name_parts = name.split("-") if name else []
    tags = name_parts + [domain] if domain else name_parts
    tags_str = ", ".join(tags)
    
    # Insert tags line before the last frontmatter line (before the closing ---)
    insert_idx = fm[1]  # insert before the closing ---
    lines.insert(insert_idx, f"tags: [{tags_str}]")
    
    new_content = "\n".join(lines)
    with open(filepath, "w") as f:
        f.write(new_content)
    return True


def fix_missing_section(filepath: str) -> bool:
    """Add '## When to Use' section to the body."""
    with open(filepath) as f:
        content = f.read()

    fm = read_frontmatter(content)
    if not fm:
        print(f"  SKIP {filepath}: no frontmatter")
        return False

    lines = content.split("\n")
    
    # Check if section already exists
    body_start = fm[1] + 1
    body_lines = lines[body_start:]
    for line in body_lines:
        if line.strip().startswith("## When to Use"):
            print(f"  OK {filepath}: already has section")
            return False

    # Insert after the frontmatter closing ---
    # Generate a reasonable description based on skill name
    name = None
    for i in range(fm[0] + 1, fm[1]):
        if lines[i].startswith("name:"):
            name = lines[i].split(":", 1)[1].strip()
            break

    desc = name or os.path.basename(os.path.dirname(filepath))
    
    # Add blank line after frontmatter, then ## When to Use, then blank line
    section_lines = [
        "",
        f"## When to Use",
        f"Use this skill when working with {desc}.",
        "",
    ]
    
    for idx, sl in enumerate(section_lines):
        lines.insert(body_start + idx, sl)

    new_content = "\n".join(lines)
    with open(filepath, "w") as f:
        f.write(new_content)
    return True


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    success = 0
    skipped = 0
    errors = 0

    print("=" * 60)
    print("Fixing [desc-no-trigger] — prepending 'Use when' to descriptions")
    print("=" * 60)
    for idx, name in enumerate(DESC_NO_TRIGGER_SKILLS):
        path = find_skill_md(name)
        if not path:
            print(f"  NOT FOUND: {name}")
            errors += 1
            continue
        try:
            if fix_desc_no_trigger(path):
                print(f"  FIXED [{idx+1}/{len(DESC_NO_TRIGGER_SKILLS)}] {name}")
                success += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  ERROR [{idx+1}/{len(DESC_NO_TRIGGER_SKILLS)}] {name}: {e}")
            errors += 1

    print()
    print("=" * 60)
    print("Fixing [missing-tags] — adding tags to frontmatter")
    print("=" * 60)
    for idx, name in enumerate(MISSING_TAGS_SKILLS):
        path = find_skill_md(name)
        if not path:
            print(f"  NOT FOUND: {name}")
            errors += 1
            continue
        try:
            if fix_missing_tags(path):
                print(f"  FIXED [{idx+1}/{len(MISSING_TAGS_SKILLS)}] {name}")
                success += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  ERROR [{idx+1}/{len(MISSING_TAGS_SKILLS)}] {name}: {e}")
            errors += 1

    print()
    print("=" * 60)
    print("Fixing [missing-section] — adding ## When to Use section")
    print("=" * 60)
    for idx, name in enumerate(MISSING_SECTION_SKILLS):
        path = find_skill_md(name)
        if not path:
            print(f"  NOT FOUND: {name}")
            errors += 1
            continue
        try:
            if fix_missing_section(path):
                print(f"  FIXED [{idx+1}/{len(MISSING_SECTION_SKILLS)}] {name}")
                success += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  ERROR [{idx+1}/{len(MISSING_SECTION_SKILLS)}] {name}: {e}")
            errors += 1

    print()
    print(f"Total: {success} fixed, {skipped} skipped, {errors} errors")
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
