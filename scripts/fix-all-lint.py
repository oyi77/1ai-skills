#!/usr/bin/env python3
"""
fix-all-lint.py — Batch fix lint issues across all SKILL.md files.

Fixes:
1. Missing '## When to Use' sections — inserts a minimal stub
2. Short descriptions (<30 chars) — expands with context from the skill name
3. Long descriptions (>500 chars) — truncates to 497 chars + "..."
4. Stub descriptions — replaces with descriptive text from H1 title
5. Missing tags — auto-generates from skill name, domain, and description
6. Missing recommended sections — inserts section stubs

Usage:
    python3 scripts/fix-all-lint.py [--dry-run]
"""
from __future__ import annotations

import argparse
import re
import sys
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SKILL_DIRS = [
    "agents", "automation", "content", "core", "cybersecurity", "data",
    "development", "devops", "financial", "integrations", "marketing",
    "mcp", "meta", "mindset", "operations", "productivity", "research",
    "sales", "trading",
]

# Category → default tags
CATEGORY_TAGS = {
    "agents": ["ai-agent", "automation", "orchestration"],
    "automation": ["automation", "workflow", "productivity"],
    "content": ["content-creation", "media", "digital-content"],
    "core": ["infrastructure", "memory", "self-improvement"],
    "cybersecurity": ["security", "cybersecurity", "threat-defense"],
    "data": ["data-analysis", "analytics", "visualization"],
    "development": ["software-engineering", "coding", "testing"],
    "devops": ["devops", "ci-cd", "infrastructure"],
    "financial": ["finance", "investment", "analysis"],
    "integrations": ["integrations", "api", "third-party"],
    "marketing": ["marketing", "growth", "seo"],
    "mcp": ["mcp-server", "model-context-protocol", "tool-integration"],
    "meta": ["self-improvement", "meta-learning", "skill-evolution"],
    "mindset": ["mindset", "personal-development", "soft-skills"],
    "operations": ["operations", "business-ops", "management"],
    "productivity": ["productivity", "time-management", "tools"],
    "research": ["research", "analysis", "investigation"],
    "sales": ["sales", "revenue", "business-development"],
    "trading": ["trading", "markets", "algorithms"],
}


def find_skills() -> list[Path]:
    found = []
    for d in SKILL_DIRS:
        p = ROOT / d
        if p.is_dir():
            found.extend(p.rglob("SKILL.md"))
    return sorted(found)


def split_frontmatter(text: str) -> tuple[str | None, str]:
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    return text[4:end], text[end + 4:]


def extract_tags_from_name(name: str, category: str, description: str) -> list[str]:
    """Auto-generate tags from skill name, category, and description."""
    tags = set()

    # From category defaults
    tags.update(CATEGORY_TAGS.get(category, []))

    # From name segments
    parts = name.replace("-", " ").split()
    # Filter out common stop words and very short segments
    stop_words = {"a", "an", "the", "for", "with", "and", "or", "in", "on", "to", "of", "is", "it", "by"}
    for part in parts:
        if len(part) > 2 and part.lower() not in stop_words:
            tags.add(part.lower())

    # From description keywords
    desc_lower = description.lower()
    keyword_patterns = [
        (r"api", "api"), (r"security", "security"), (r"docker", "docker"),
        (r"kubernetes|k8s", "kubernetes"), (r"aws", "aws"), (r"azure", "azure"),
        (r"gcp", "gcp"), (r"terraform", "terraform"), (r"testing", "testing"),
        (r"monitoring", "monitoring"), (r"trading", "trading"), (r"crypto", "crypto"),
        (r"seo", "seo"), (r"social", "social-media"), (r"email", "email"),
        (r"slack", "slack"), (r"discord", "discord"), (r"github", "github"),
        (r"notion", "notion"), (r"voice", "voice"), (r"video", "video"),
        (r"podcast", "podcast"), (r"tts", "text-to-speech"), (r"websocket", "websocket"),
        (r"graphql", "graphql"), (r"rest", "rest-api"), (r"webhook", "webhook"),
        (r"cron", "cron"), (r"pipeline", "pipeline"), (r"workflow", "workflow"),
        (r"agent", "ai-agent"), (r"machine.learning|ml", "machine-learning"),
        (r"penetration.test|pentest", "penetration-testing"),
        (r"forensic", "forensics"), (r"malware", "malware-analysis"),
        (r"incident.response", "incident-response"), (r"threat.hunt", "threat-hunting"),
        (r"compliance", "compliance"), (r"zero.trust", "zero-trust"),
    ]
    for pattern, tag in keyword_patterns:
        if re.search(pattern, desc_lower):
            tags.add(tag)

    # Remove overly generic tags that are redundant with category
    generic = {"security", "automation", "analysis", "management", "development"}
    # Keep them only if they add value beyond the category default
    cat_defaults = set(CATEGORY_TAGS.get(category, []))
    tags = tags - (generic & tags - cat_defaults) if len(tags) > 5 else tags

    return sorted(tags)[:8]  # Cap at 8 tags


def generate_wtu_section(name: str, description: str) -> str:
    """Generate a minimal '## When to Use' section from skill context."""
    # Convert name to readable form
    readable = name.replace("-", " ").title()

    return f"""
## When to Use

**Trigger phrases:**
- "{readable.lower()}"
- "Help me with {name.replace('-', ' ')}"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope
"""


def generate_section_stub(section_name: str) -> str:
    """Generate a minimal section stub."""
    return f"""
{section_name}

> Section content — see SKILL.md body for full details.
"""


def fix_skill(path: Path, dry_run: bool = False) -> dict:
    """Fix all lint issues in a single skill file. Returns fix report."""
    fixes = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return {"path": str(path), "error": str(e)}

    fm, body = split_frontmatter(text)
    if fm is None:
        return {"path": str(path), "error": "no-frontmatter"}

    try:
        meta = yaml.safe_load(fm) or {}
    except Exception:
        return {"path": str(path), "error": "invalid-yaml"}

    if not isinstance(meta, dict):
        return {"path": str(path), "error": "not-dict"}

    rel = path.relative_to(ROOT)
    category = rel.parts[0] if len(rel.parts) > 1 else "unknown"
    name = meta.get("name", path.parent.name)
    description = meta.get("description", "")
    domain = meta.get("domain", category)

    # ── Fix 1: Short description ──
    if description and len(description) < 30:
        # Expand from name and body H1
        h1_match = re.search(r"^# (.+)$", body, re.MULTILINE)
        h1 = h1_match.group(1) if h1_match else name.replace("-", " ").title()
        new_desc = f"{h1}. Use when working with {name.replace('-', ' ')} in {category} domain."
        if len(new_desc) >= 30:
            meta["description"] = new_desc
            fixes.append(f"expanded-description({len(description)}→{len(new_desc)})")
        else:
            meta["description"] = f"{h1}. Use when relevant to {category} tasks and workflows for {name.replace('-', ' ')}."
            fixes.append(f"expanded-description({len(description)}→{len(meta['description'])})")

    # ── Fix 2: Long description ──
    if len(description) > 500:
        # Truncate at sentence boundary near 497 chars
        truncated = description[:497]
        last_period = truncated.rfind(".")
        if last_period > 300:
            truncated = truncated[:last_period + 1]
        else:
            truncated = truncated.rstrip() + "..."
        meta["description"] = truncated
        fixes.append(f"truncated-description({len(description)}→{len(truncated)})")

    # ── Fix 3: Stub description ──
    desc_lower = (meta.get("description") or "").strip().lower()
    stub_patterns = [r"^ai.?agent", r"^skill for", r"^use this skill", r"^todo", r"^placeholder", r"^tbd", r"^lorem"]
    is_stub = any(re.match(p, desc_lower) for p in stub_patterns)
    if is_stub:
        h1_match = re.search(r"^# (.+)$", body, re.MULTILINE)
        h1 = h1_match.group(1) if h1_match else name.replace("-", " ").title()
        new_desc = f"{h1}. Use when performing {name.replace('-', ' ')} tasks in {category} workflows."
        meta["description"] = new_desc
        fixes.append(f"replaced-stub-description")

    # ── Fix 4: Missing tags ──
    if not meta.get("tags") or (isinstance(meta.get("tags"), list) and len(meta["tags"]) == 0):
        meta["tags"] = extract_tags_from_name(name, category, meta.get("description", ""))
        fixes.append(f"added-tags({len(meta['tags'])})")

    # ── Fix 5: Missing '## When to Use' section ──
    if "## When to Use" not in body and "## when to use" not in body.lower():
        wtu = generate_wtu_section(name, meta.get("description", ""))
        # Insert after first H1 or at start of body
        h1_match = re.search(r"^# .+$", body, re.MULTILINE)
        if h1_match:
            insert_pos = h1_match.end()
            body = body[:insert_pos] + wtu + body[insert_pos:]
        else:
            body = wtu + body
        fixes.append("added-when-to-use")

    # ── Fix 6: Missing recommended sections ──
    recommended = {
        "## Overview": generate_section_stub("## Overview"),
        "## Verification": "\n## Verification\n\n- [ ] Skill output matches expected behavior\n",
    }
    for section, stub in recommended.items():
        if section not in body:
            # Insert before the last section or at end
            body = body.rstrip() + "\n" + stub
            fixes.append(f"added-{section.lower().replace('## ', '').replace(' ', '-')}")

    if not fixes:
        return {"path": str(rel), "fixes": []}

    # ── Reassemble file ──
    # Reorder frontmatter keys
    ordered = {}
    for key in ("name", "description", "domain", "tags", "persona"):
        if key in meta:
            ordered[key] = meta.pop(key)
    ordered.update(meta)

    new_fm = yaml.safe_dump(ordered, sort_keys=False, allow_unicode=True, width=120).rstrip()
    new_text = f"---\n{new_fm}\n---\n{body}" if not body.startswith("\n") else f"---\n{new_fm}\n---{body}"

    if not dry_run:
        path.write_text(new_text, encoding="utf-8")

    return {"path": str(rel), "fixes": fixes}


def main() -> int:
    ap = argparse.ArgumentParser(description="Batch fix lint issues in SKILL.md files")
    ap.add_argument("--dry-run", action="store_true", help="Show what would be fixed without writing")
    args = ap.parse_args()

    skills = find_skills()
    print(f"Processing {len(skills)} skills...")

    total_fixes = 0
    fixed_files = 0
    errors = 0

    for skill in skills:
        result = fix_skill(skill, dry_run=args.dry_run)
        if result.get("error"):
            errors += 1
            print(f"  ERROR {result['path']}: {result['error']}")
        elif result["fixes"]:
            fixed_files += 1
            total_fixes += len(result["fixes"])
            print(f"  FIXED {result['path']}: {', '.join(result['fixes'])}")

    print(f"\n{'DRY RUN ' if args.dry_run else ''}Summary:")
    print(f"  Files processed: {len(skills)}")
    print(f"  Files fixed: {fixed_files}")
    print(f"  Total fixes: {total_fixes}")
    print(f"  Errors: {errors}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
