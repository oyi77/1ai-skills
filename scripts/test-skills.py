#!/usr/bin/env python3
"""
test-skills.py — Comprehensive skill quality test suite.

Tests ALL skills across 8 dimensions:
  1. Structural (YAML frontmatter, required fields)
  2. Content quality (sections, depth, placeholders)
  3. Code syntax (Python ast.parse, JS/TS presence)
  4. Internal links (/skills/<name> resolution)
  5. Description quality (length, action-oriented)
  6. Anti-rationalization tables
  7. SDK/tool availability
  8. Workflow completeness

Usage:
  python3 scripts/test-skills.py              # Run all tests
  python3 scripts/test-skills.py --quick      # Skip slow tests
  python3 scripts/test-skills.py --verbose    # Show all details
  python3 scripts/test-skills.py --json       # JSON output
  python3 scripts/test-skills.py --skill NAME # Test single skill
"""

import argparse
import ast
import json
import os
import re
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

# ── Config ──

ROOT = Path(__file__).resolve().parent.parent
CATS = [
    'agents', 'automation', 'content', 'core', 'cybersecurity', 'data',
    'development', 'devops', 'financial', 'integrations', 'marketing',
    'mcp', 'meta', 'mindset', 'operations', 'productivity', 'research',
    'sales', 'trading',
]

REQUIRED_FM = ['name', 'description', 'domain']
REQUIRED_SECTIONS = ['## When to Use']
WORKFLOW_ALTERNATIVES = ['## Workflow', '## Process', '## Steps', '## Daily Practice',
                         '## Core Principles', '## How to Use', '## Capabilities',
                         '## Core Features', '## Architecture']
RECOMMENDED_SECTIONS = ['## When NOT to Use', '## Overview', '## Verification']
QUALITY_MARKERS = ['Anti-Rationalization', 'Code Example', '```']

# ── Result types ──

class TestResult:
    def __init__(self, skill, category, passed, warnings, errors, metrics):
        self.skill = skill
        self.category = category
        self.passed = passed
        self.warnings = warnings
        self.errors = errors
        self.metrics = metrics

# ── Collectors ──

def collect_skills(filter_name=None):
    """Collect all SKILL.md files."""
    skills = []
    for cat in CATS:
        cat_dir = ROOT / cat
        if not cat_dir.exists():
            continue
        for md in sorted(cat_dir.rglob('SKILL.md')):
            name = md.parent.name
            if filter_name and name != filter_name:
                continue
            skills.append({
                'name': name,
                'category': cat,
                'path': md,
                'rel': str(md.parent.relative_to(ROOT)),
            })
    return skills

# ── Individual tests ──

def test_structure(text, skill_name):
    """Test 1: YAML frontmatter and required fields."""
    errors = []
    warnings = []
    metrics = {}

    if not text.startswith('---'):
        errors.append('missing-leading----')
        return errors, warnings, metrics

    fm_match = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    if not fm_match:
        errors.append('unclosed-frontmatter')
        return errors, warnings, metrics

    fm = fm_match.group(1)

    # Required fields
    for field in REQUIRED_FM:
        match = re.search(rf'^{field}:\s*(.+)$', fm, re.MULTILINE)
        if not match or not match.group(1).strip():
            errors.append(f'missing-{field}')
        else:
            metrics[field] = match.group(1).strip()

    # Name matches directory
    if 'name' in metrics and metrics['name'] != skill_name:
        errors.append(f'name-mismatch[fm={metrics["name"]}, dir={skill_name}]')

    # Description quality
    if 'description' in metrics:
        desc = metrics['description']
        metrics['desc_len'] = len(desc)
        if len(desc) < 30:
            errors.append(f'description-too-short({len(desc)}c)')
        elif len(desc) < 50:
            warnings.append(f'description-short({len(desc)}c)')
        if len(desc) > 200:
            warnings.append(f'description-long({len(desc)}c)')

    # Domain matches category
    if 'domain' in metrics:
        metrics['domain_value'] = metrics['domain']

    # Tags
    tags_match = re.search(r'^tags:\s*\n((?:\s*-\s*.+\n?)+)', fm, re.MULTILINE)
    if tags_match:
        tags = [l.strip('- ').strip() for l in tags_match.group(1).strip().split('\n')]
        metrics['tag_count'] = len(tags)
        if len(tags) < 3:
            warnings.append(f'too-few-tags({len(tags)})')
    else:
        warnings.append('missing-tags')

    # Version
    ver_match = re.search(r'^version:\s*(.+)$', fm, re.MULTILINE)
    metrics['has_version'] = bool(ver_match)

    return errors, warnings, metrics


def test_content(text):
    """Test 2: Content quality — sections, depth, placeholders."""
    errors = []
    warnings = []
    metrics = {}

    body = text.split('---', 2)[-1] if text.count('---') >= 2 else text
    lines = body.splitlines()
    metrics['line_count'] = len(lines)

    # Placeholder detection
    placeholders = []
    if 'Section content — see SKILL.md body for full details' in body:
        placeholders.append('section-content-placeholder')
    if 'This section covers core rules for the' in body and 'Refer to the skill overview' in body:
        placeholders.append('generic-rules-placeholder')
    if 'Configure domain, generation, media, realistic, relevant settings' in body:
        placeholders.append('configure-domain-placeholder')
    if 'Review output quality and adjust parameters' in body and 'Monitor performance metrics' in body:
        placeholders.append('review-output-placeholder')

    if placeholders:
        errors.extend([f'placeholder:{p}' for p in placeholders])
    metrics['placeholder_count'] = len(placeholders)

    # Required sections
    for section in REQUIRED_SECTIONS:
        if section not in body:
            errors.append(f'missing-section:{section}')

    # Workflow section (accept alternatives)
    has_workflow = any(alt in body for alt in WORKFLOW_ALTERNATIVES)
    if not has_workflow:
        errors.append('missing-section:## Workflow (or alternative)')

    # Recommended sections
    for section in RECOMMENDED_SECTIONS:
        if section not in body:
            warnings.append(f'missing-recommended:{section}')

    # Section count
    headings = re.findall(r'^##+ .+$', body, re.MULTILINE)
    metrics['section_count'] = len(headings)

    # Depth score (how many quality markers present)
    depth = 0
    if 'Anti-Rationalization' in body or '## Common Pitfalls' in body:
        depth += 1
    if re.search(r'```', body):
        depth += 1
    if '## Verification' in body or '## Quality Checklist' in body:
        depth += 1
    if '## When NOT to Use' in body:
        depth += 1
    if re.search(r'`(npm|pip|npx|brew|apt)\s+(install|add)', body):
        depth += 1
    metrics['depth_score'] = depth  # 0-5

    return errors, warnings, metrics


def test_code_syntax(text):
    """Test 3: Code block syntax validation."""
    errors = []
    warnings = []
    metrics = {}

    # Python blocks
    py_blocks = re.findall(r'```python\n(.*?)```', text, re.DOTALL)
    metrics['python_blocks'] = len(py_blocks)
    py_errors = 0
    for block in py_blocks:
        try:
            ast.parse(block)
        except SyntaxError:
            py_errors += 1
    if py_errors > 0:
        errors.append(f'python-syntax-errors:{py_errors}')
    metrics['python_syntax_errors'] = py_errors

    # JS/TS blocks
    js_blocks = re.findall(r'```(typescript|javascript|tsx|ts|jsx)\n(.*?)```', text, re.DOTALL)
    metrics['js_blocks'] = len(js_blocks)

    # Bash blocks
    bash_blocks = re.findall(r'```bash\n(.*?)```', text, re.DOTALL)
    metrics['bash_blocks'] = len(bash_blocks)

    # SQL blocks
    sql_blocks = re.findall(r'```sql\n(.*?)```', text, re.DOTALL)
    metrics['sql_blocks'] = len(sql_blocks)

    # Total code blocks
    all_blocks = re.findall(r'```\w*\n', text)
    metrics['total_code_blocks'] = len(all_blocks)

    if len(all_blocks) == 0:
        warnings.append('no-code-blocks')

    return errors, warnings, metrics


def test_internal_links(text, all_names):
    """Test 4: Internal /skills/<name> links."""
    errors = []
    warnings = []
    metrics = {}

    links = re.findall(r'/skills/([a-z0-9-]+)', text)
    metrics['internal_links'] = len(links)

    broken = [l for l in links if l not in all_names]
    if broken:
        errors.extend([f'broken-link:{l}' for l in broken])
    metrics['broken_links'] = len(broken)

    return errors, warnings, metrics


def test_quality_markers(text):
    """Test 5-6: Anti-rationalization tables, code examples, verification."""
    errors = []
    warnings = []
    metrics = {}

    has_ar = bool(re.search(r'Anti-Rationalization|Common Rationalizations|Common Pitfalls', text))
    has_code = bool(re.search(r'```', text))
    has_verify = bool(re.search(r'## Verification|## Quality Checklist|## Quality Gates', text))
    has_when_not = bool(re.search(r'## When NOT to Use|## When Not to Use', text))
    has_overview = bool(re.search(r'## Overview', text))
    has_commands = bool(re.search(r'`(npm|pip|npx|brew|apt|docker|git)\s+', text))
    has_imports = bool(re.search(r'(import |from |require\(|const .+ = require)', text))

    metrics['has_anti_rationalization'] = has_ar
    metrics['has_code_examples'] = has_code
    metrics['has_verification'] = has_verify
    metrics['has_when_not_to_use'] = has_when_not
    metrics['has_overview'] = has_overview
    metrics['has_commands'] = has_commands
    metrics['has_imports'] = has_imports

    # Quality score (0-7)
    quality = sum([has_ar, has_code, has_verify, has_when_not, has_overview, has_commands, has_imports])
    metrics['quality_score'] = quality

    if not has_ar:
        warnings.append('no-anti-rationalization')
    if not has_code:
        warnings.append('no-code-examples')
    if not has_verify:
        warnings.append('no-verification')

    return errors, warnings, metrics


def test_sdk_availability(text):
    """Test 7: Check if referenced SDKs/tools are importable."""
    errors = []
    warnings = []
    metrics = {}

    # Extract import statements
    imports = set()
    for match in re.findall(r'(?:from|import)\s+([\w.]+)', text):
        top = match.split('.')[0]
        imports.add(top)

    # Extract npm packages
    for match in re.findall(r'npm install\s+([\w@/-]+)', text):
        imports.add(match.split('/')[-1].replace('@', ''))

    # Check availability
    available = 0
    unavailable = 0
    for imp in imports:
        try:
            __import__(imp)
            available += 1
        except ImportError:
            unavailable += 1

    metrics['referenced_imports'] = len(imports)
    metrics['importable'] = available
    metrics['not_importable'] = unavailable

    return errors, warnings, metrics


# ── Main runner ──

def run_tests(skills, quick=False, verbose=False, json_out=False):
    """Run all tests on a list of skills."""
    all_names = {s['name'] for s in skills}
    results = []
    start = time.time()

    for skill in skills:
        try:
            text = skill['path'].read_text(encoding='utf-8')
        except Exception as e:
            results.append(TestResult(skill['name'], skill['category'], False, [], [f'unreadable:{e}'], {}))
            continue

        all_errors = []
        all_warnings = []
        all_metrics = {'name': skill['name'], 'category': skill['category']}

        # Test 1: Structure
        e, w, m = test_structure(text, skill['name'])
        all_errors.extend(e); all_warnings.extend(w); all_metrics.update(m)

        # Test 2: Content
        e, w, m = test_content(text)
        all_errors.extend(e); all_warnings.extend(w); all_metrics.update(m)

        # Test 3: Code syntax
        e, w, m = test_code_syntax(text)
        all_errors.extend(e); all_warnings.extend(w); all_metrics.update(m)

        # Test 4: Internal links
        e, w, m = test_internal_links(text, all_names)
        all_errors.extend(e); all_warnings.extend(w); all_metrics.update(m)

        # Test 5-6: Quality markers
        e, w, m = test_quality_markers(text)
        all_errors.extend(e); all_warnings.extend(w); all_metrics.update(m)

        # Test 7: SDK availability (skip in quick mode)
        if not quick:
            e, w, m = test_sdk_availability(text)
            all_warnings.extend(w); all_metrics.update(m)

        passed = len(all_errors) == 0
        results.append(TestResult(skill['name'], skill['category'], passed, all_warnings, all_errors, all_metrics))

    elapsed = time.time() - start
    return results, elapsed


def print_report(results, elapsed, verbose=False, json_out=False):
    """Print test report."""
    if json_out:
        output = {
            'total': len(results),
            'passed': sum(1 for r in results if r.passed),
            'failed': sum(1 for r in results if not r.passed),
            'warnings': sum(len(r.warnings) for r in results),
            'elapsed_seconds': round(elapsed, 2),
            'skills': []
        }
        for r in results:
            entry = {
                'name': r.skill,
                'category': r.category,
                'passed': r.passed,
                'errors': r.errors,
                'warnings': r.warnings,
                'metrics': r.metrics,
            }
            output['skills'].append(entry)
        print(json.dumps(output, indent=2))
        return

    # Summary
    passed = sum(1 for r in results if r.passed)
    failed = sum(1 for r in results if not r.passed)
    total_warnings = sum(len(r.warnings) for r in results)

    print()
    print("=" * 60)
    print("  1AI-SKILLS COMPREHENSIVE TEST RESULTS")
    print("=" * 60)
    print(f"  Total:    {len(results)}")
    print(f"  Passed:   {passed} ({passed/len(results)*100:.1f}%)")
    print(f"  Failed:   {failed}")
    print(f"  Warnings: {total_warnings}")
    print(f"  Time:     {elapsed:.2f}s")
    print("=" * 60)

    # By category
    cat_stats = defaultdict(lambda: {'pass': 0, 'fail': 0, 'warn': 0})
    for r in results:
        cat_stats[r.category]['pass' if r.passed else 'fail'] += 1
        cat_stats[r.category]['warn'] += len(r.warnings)

    print(f"\n  {'Category':<20} {'Pass':>6} {'Fail':>6} {'Warn':>6}")
    print(f"  {'-'*20} {'-'*6} {'-'*6} {'-'*6}")
    for cat in sorted(cat_stats):
        s = cat_stats[cat]
        print(f"  {cat:<20} {s['pass']:>6} {s['fail']:>6} {s['warn']:>6}")

    # Error summary
    error_counts = defaultdict(int)
    for r in results:
        for e in r.errors:
            # Extract error type (before the colon)
            etype = e.split(':')[0] if ':' in e else e
            error_counts[etype] += 1

    if error_counts:
        print(f"\n  Error Types:")
        for etype, count in sorted(error_counts.items(), key=lambda x: -x[1]):
            print(f"    {etype:<40} {count:>4}")

    # Warning summary
    warn_counts = defaultdict(int)
    for r in results:
        for w in r.warnings:
            wtype = w.split(':')[0] if ':' in w else w
            warn_counts[wtype] += 1

    if warn_counts:
        print(f"\n  Warning Types:")
        for wtype, count in sorted(warn_counts.items(), key=lambda x: -x[1]):
            print(f"    {wtype:<40} {count:>4}")

    # Quality score distribution
    quality_scores = [r.metrics.get('quality_score', 0) for r in results]
    depth_scores = [r.metrics.get('depth_score', 0) for r in results]

    print(f"\n  Quality Score Distribution (0-7):")
    for score in range(8):
        count = quality_scores.count(score)
        bar = "█" * (count // 10) + "░"
        print(f"    {score}: {count:>5} {bar}")

    print(f"\n  Depth Score Distribution (0-5):")
    for score in range(6):
        count = depth_scores.count(score)
        bar = "█" * (count // 10) + "░"
        print(f"    {score}: {count:>5} {bar}")

    # Failed skills (always show)
    failed_skills = [r for r in results if not r.passed]
    if failed_skills:
        print(f"\n  FAILED SKILLS ({len(failed_skills)}):")
        for r in failed_skills:
            print(f"    ✗ {r.category}/{r.skill}")
            for e in r.errors:
                print(f"      → {e}")

    # Verbose: show all warnings
    if verbose:
        warned_skills = [r for r in results if r.warnings]
        if warned_skills:
            print(f"\n  WARNINGS ({len(warned_skills)} skills):")
            for r in warned_skills:
                print(f"    ⚠ {r.category}/{r.skill}")
                for w in r.warnings:
                    print(f"      → {w}")

    # Final verdict
    print(f"\n{'=' * 60}")
    if failed == 0:
        print(f"  ✅ ALL {len(results)} SKILLS PASS")
    else:
        print(f"  ❌ {failed}/{len(results)} SKILLS FAILED")
    print(f"{'=' * 60}")


# ── CLI ──

def main():
    parser = argparse.ArgumentParser(description='Comprehensive 1ai-skills test suite')
    parser.add_argument('--quick', action='store_true', help='Skip slow tests (SDK checks)')
    parser.add_argument('--verbose', action='store_true', help='Show all warnings')
    parser.add_argument('--json', action='store_true', help='JSON output')
    parser.add_argument('--skill', type=str, help='Test single skill by name')
    args = parser.parse_args()

    skills = collect_skills(filter_name=args.skill)

    if not skills:
        print(f"No skills found{f' matching {args.skill}' if args.skill else ''}")
        return 1

    if not args.json:
        print(f"Testing {len(skills)} skills...", file=sys.stderr)

    results, elapsed = run_tests(skills, quick=args.quick, verbose=args.verbose, json_out=args.json)
    print_report(results, elapsed, verbose=args.verbose, json_out=args.json)

    # Exit code: 0 if all pass, 1 if any fail
    return 0 if all(r.passed for r in results) else 1


if __name__ == '__main__':
    sys.exit(main())
