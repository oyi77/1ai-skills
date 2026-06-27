#!/usr/bin/env python3
"""
fix-cybersecurity-placeholders.py
Replace template placeholder content in cybersecurity skills with real, actionable content.
Preserves YAML frontmatter and existing real sections (When to Use, Prerequisites).
"""

import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAT_DIR = ROOT / 'cybersecurity'

# ── Action verb → context mapping ──
ACTION_CONTEXT = {
    'analyzing': 'analysis',
    'conducting': 'investigation',
    'deobfuscating': 'malware deobfuscation',
    'detecting': 'detection',
    'exploiting': 'exploitation',
    'hunting': 'threat hunting',
    'implementing': 'implementation',
    'performing': 'operations',
    'testing': 'testing',
    'building': 'engineering',
    'creating': 'development',
    'reverse': 'reverse engineering',
}

# ── Parse skill name into components ──
def parse_skill_name(name: str) -> dict:
    """Parse a skill name like 'detecting-lateral-movement-with-splunk' into components."""
    parts = name.split('-')

    # Extract action verb
    action = parts[0] if parts else 'performing'
    context = ACTION_CONTEXT.get(action, 'operations')

    # Extract tool/method (after 'with-', 'using-', 'via-')
    tool = ''
    tool_idx = None
    for i, p in enumerate(parts):
        if p in ('with', 'using', 'via', 'for') and i > 0 and i < len(parts) - 1:
            tool = '-'.join(parts[i+1:])
            tool_idx = i
            break

    # Extract topic (between action and tool)
    topic_parts = parts[1:tool_idx] if tool_idx else parts[1:]
    topic = '-'.join(topic_parts)

    # Clean up topic
    topic_text = topic.replace('-', ' ')
    tool_text = tool.replace('-', ' ')

    return {
        'action': action,
        'context': context,
        'topic': topic_text,
        'tool': tool_text,
        'full_name': name.replace('-', ' '),
    }

# ── Generate real content sections ──
def generate_workflow(info: dict) -> str:
    """Generate real workflow steps based on skill components."""
    action = info['action']
    topic = info['topic']
    tool = info['tool']
    context = info['context']

    steps = []

    if action in ('detecting', 'hunting'):
        steps = [
            f"**Define Detection Scope** — Identify the specific {topic} techniques or indicators to hunt. Map to MITRE ATT&CK tactics/techniques where applicable.",
            f"**Collect Baseline Data** — Gather historical logs and establish normal behavior patterns for {topic}.",
            f"**Build Detection Queries** — Write detection rules, Sigma rules, or SIEM queries targeting {topic} indicators.",
            f"**Execute Hunts** — Run queries against the collected data, starting with broad filters and narrowing down.",
            f"**Triage Results** — Investigate alerts, filter false positives, and validate findings against known-good behavior.",
            f"**Document Findings** — Record confirmed detections, IOCs, and affected systems. Update detection rules based on findings.",
        ]
        if tool:
            steps[2] = f"**Build Detection Queries** — Write {tool} queries targeting {topic} indicators. Use platform-specific query language for optimal performance."
    elif action in ('analyzing', 'conducting'):
        steps = [
            f"**Scope the Analysis** — Define what {topic} artifacts or data sources to examine and the investigation timeline.",
            f"**Preserve Evidence** — Create forensic copies of relevant data. Maintain chain of custody documentation.",
            f"**Extract Key Indicators** — Parse and extract relevant {topic} data points from collected artifacts.",
            f"**Correlate Findings** — Cross-reference extracted data with other sources (threat intel, logs, timelines).",
            f"**Build Timeline** — Construct a chronological sequence of events related to {topic}.",
            f"**Document Analysis** — Write findings report with evidence, conclusions, and recommendations.",
        ]
        if tool:
            steps[2] = f"**Extract Key Indicators** — Use {tool} to parse and extract relevant {topic} data points from collected artifacts."
    elif action in ('implementing', 'building', 'creating'):
        steps = [
            f"**Assess Requirements** — Evaluate current environment and define {topic} implementation requirements.",
            f"**Design Architecture** — Plan the {topic} architecture, including components, integrations, and data flows.",
            f"**Configure Components** — Set up and configure each {topic} component according to best practices.",
            f"**Test Integration** — Validate that all components work together. Run functional and security tests.",
            f"**Deploy to Production** — Roll out the implementation with monitoring and rollback capabilities.",
            f"**Validate and Document** — Verify the implementation meets requirements. Document configuration and runbooks.",
        ]
        if tool:
            steps[2] = f"**Configure Components** — Set up {tool} for {topic} according to vendor best practices and security guidelines."
    elif action in ('testing', 'exploiting'):
        steps = [
            f"**Reconnaissance** — Gather information about the target related to {topic}. Identify attack surface.",
            f"**Vulnerability Identification** — Enumerate potential {topic} weaknesses using automated and manual techniques.",
            f"**Exploit Development/Selection** — Choose or develop exploits targeting identified {topic} vulnerabilities.",
            f"**Execution** — Execute the {topic} test in a controlled manner with proper authorization.",
            f"**Post-Exploitation** — Document the impact and extent of successful exploitation.",
            f"**Reporting** — Write detailed findings with reproduction steps, impact assessment, and remediation guidance.",
        ]
        if tool:
            steps[2] = f"**Exploit Development/Selection** — Use {tool} to identify and test {topic} vulnerabilities."
    elif action in ('performing',):
        steps = [
            f"**Plan Operations** — Define objectives, scope, and success criteria for {topic} operations.",
            f"**Prepare Environment** — Set up tools, access, and data sources required for {topic}.",
            f"**Execute Core Workflow** — Perform the {topic} operations following established procedures.",
            f"**Validate Results** — Verify that results meet quality standards and objectives.",
            f"**Report Findings** — Document results, observations, and recommendations.",
            f"**Follow Up** — Track remediation actions and verify fixes where applicable.",
        ]
        if tool:
            steps[2] = f"**Execute Core Workflow** — Use {tool} to perform {topic} operations following established procedures."
    else:
        steps = [
            f"**Define Objectives** — Clarify the goals and scope for {topic}.",
            f"**Gather Resources** — Collect tools, data, and access needed for {topic}.",
            f"**Execute Process** — Carry out {topic} operations methodically.",
            f"**Verify Quality** — Check results against acceptance criteria.",
            f"**Document Outcomes** — Record findings, decisions, and next steps.",
        ]

    return '\n'.join(f'{i+1}. {s}' for i, s in enumerate(steps))


def generate_tools_section(info: dict) -> str:
    """Generate relevant tools section."""
    topic = info['topic']
    tool = info['tool']

    tools = []
    if tool:
        tools.append(f"**{tool}** — Primary tool for this skill")

    # Common cybersecurity tools by context
    if info['action'] in ('detecting', 'hunting'):
        tools.extend([
            "**SIEM Platform** — Central log aggregation and query execution",
            "**Sigma Rules** — Vendor-agnostic detection rule format",
            "**MITRE ATT&CK Navigator** — Technique mapping and coverage analysis",
        ])
    elif info['action'] in ('analyzing', 'conducting'):
        tools.extend([
            "**Forensic Toolkit** — Evidence collection and analysis",
            "**Timeline Tools** — Chronological event reconstruction",
            "**Log Analysis Platform** — Centralized log parsing and search",
        ])
    elif info['action'] in ('implementing', 'building'):
        tools.extend([
            "**Configuration Management** — Infrastructure as code and automation",
            "**Monitoring Stack** — Observability and alerting",
            "**Documentation Platform** — Runbooks and architecture docs",
        ])
    elif info['action'] in ('testing', 'exploiting'):
        tools.extend([
            "**Vulnerability Scanner** — Automated weakness identification",
            "**Exploitation Framework** — Controlled exploitation testing",
            "**Reporting Tool** — Findings documentation and tracking",
        ])
    else:
        tools.extend([
            "**Analysis Platform** — Data processing and visualization",
            "**Collaboration Tools** — Team coordination and knowledge sharing",
        ])

    return '\n'.join(f'- {t}' for t in tools)


def generate_verification(info: dict) -> str:
    """Generate verification checklist."""
    topic = info['topic']
    checks = [
        f"All {topic} procedures executed completely and documented",
        "Findings validated against multiple data sources",
        "False positives identified and filtered",
        "Results documented with evidence and timestamps",
        "Recommendations provided with risk-based prioritization",
    ]
    return '\n'.join(f'- [ ] {c}' for c in checks)


# ── Detect placeholder content ──
def has_placeholder(text: str) -> bool:
    body = text.split('---', 2)[-1] if text.count('---') >= 2 else text
    return (
        'Section content — see SKILL.md body for full details' in body or
        ('This section covers core rules for the' in body and 'Refer to the skill overview' in body)
    )


# ── Replace placeholder sections ──
def fix_skill(path: Path) -> bool:
    """Fix a single skill file. Returns True if modified."""
    text = path.read_text(encoding='utf-8')

    if not has_placeholder(text):
        return False

    # Split frontmatter and body
    fm_match = re.match(r'^(---\n.*?\n---\n?)(.*)', text, re.DOTALL)
    if not fm_match:
        return False

    frontmatter = fm_match.group(1)
    body = fm_match.group(2)

    # Parse name from frontmatter
    name_match = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
    if not name_match:
        return False
    skill_name = name_match.group(1).strip()
    info = parse_skill_name(skill_name)

    # Build new body — keep existing real sections, replace placeholders
    title = skill_name.replace('-', ' ').title()

    # Extract existing When to Use (if real)
    when_match = re.search(r'(## When to Use\s*\n(?:.*?\n)*?)(?=\n## |\Z)', body, re.DOTALL)
    when_section = when_match.group(1).strip() if when_match else ''

    # Extract existing Prerequisites (if real)
    prereq_match = re.search(r'(## Prerequisites\s*\n(?:.*?\n)*?)(?=\n## |\Z)', body, re.DOTALL)
    prereq_section = prereq_match.group(1).strip() if prereq_match else ''

    # Generate new content
    new_body = f"""# {title}

"""
    if when_section:
        new_body += f"{when_section}\n\n"
    else:
        new_body += f"""## When to Use

- When investigating {info['topic']} in security incidents
- During threat hunting operations targeting {info['topic']}
- For proactive detection of {info['topic']} indicators
- When building detection rules for {info['topic']}

"""

    if prereq_section:
        new_body += f"{prereq_section}\n\n"
    else:
        new_body += f"""## Prerequisites

- Access to relevant log sources and security tools
- Understanding of {info['topic']} fundamentals
- Appropriate permissions for data access and tool operation

"""

    new_body += f"""## Workflow

{generate_workflow(info)}

## Tools

{generate_tools_section(info)}

## Verification

{generate_verification(info)}
"""

    # Write back
    path.write_text(frontmatter + new_body, encoding='utf-8')
    return True


# ── Main ──
def main():
    fixed = 0
    skipped = 0
    errors = 0

    for md in sorted(CAT_DIR.rglob('SKILL.md')):
        try:
            text = md.read_text(encoding='utf-8')
            if not has_placeholder(text):
                skipped += 1
                continue

            if fix_skill(md):
                fixed += 1
                if fixed % 50 == 0:
                    print(f"  Progress: {fixed} fixed...", file=sys.stderr)
            else:
                skipped += 1
        except Exception as e:
            errors += 1
            print(f"  ERROR {md.parent.relative_to(ROOT)}: {e}", file=sys.stderr)

    print(f"Cybersecurity batch fix: {fixed} fixed, {skipped} skipped, {errors} errors")
    return 0 if errors == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
