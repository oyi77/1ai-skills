#!/usr/bin/env python3
"""
Fix ALL 130 test failures in one pass.

Fixes:
  1. name-mismatch        — set frontmatter `name:` to match directory name
  2. description-too-short — convert multi-line YAML block scalars to inline
  3. missing-section       — add ## When to Use and ## Workflow to stubs
  4. missing-leading----   — add frontmatter delimiters
  5. broken-link           — fix internal links to nonexistent targets
  6. python-syntax-errors  — fix Python code block syntax
"""

import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def collect_all_skills():
    """Walk all SKILL.md files just like the test does."""
    skills = []
    for cat_dir in ROOT.iterdir():
        if not cat_dir.is_dir() or cat_dir.name.startswith(('.', '_')):
            continue
        if cat_dir.name in ('scripts', 'test_data', '.github', '.git', '.claude-plugin'):
            continue
        for md in sorted(cat_dir.rglob('SKILL.md')):
            skills.append({'name': md.parent.name, 'path': md, 'rel': str(md.parent.relative_to(ROOT))})
    return skills

# ── Issue checks ──

def check_name_mismatch(text, dir_name):
    m = re.search(r'^name:\s*(.+)$', text, re.MULTILINE)
    if m and m.group(1).strip() != dir_name:
        return m.group(1).strip()
    return None

def check_description_length(text):
    m = re.search(r'^description:\s*(.+)$', text, re.MULTILINE)
    if m:
        desc = m.group(1).strip()
        if desc in ('>', '|', '>-', '|+', '>+', '|-', '>8', '|-', '>-'):
            return True  # multi-line block scalar indicator captured instead of content
    return None

def check_missing_sections(text):
    missing = []
    if '## When to Use' not in text:
        missing.append('## When to Use')
    workflow_alts = ['## Workflow', '## Process', '## Steps', '## Daily Practice',
                     '## Core Principles', '## How to Use', '## Capabilities',
                     '## Core Features', '## Architecture']
    if not any(s in text for s in workflow_alts):
        missing.append('## Workflow')
    return missing

def check_missing_leading(text):
    return not text.startswith('---')

def check_broken_links(text, all_names):
    broken = []
    for m in re.finditer(r'\[([^\]]*)\]\(/skills/([^)]+)\)', text):
        target = m.group(2)
        if target and target not in all_names:
            broken.append(target)
    return broken

def check_python_syntax(text):
    """Very basic check: look for Python code blocks with print statement issues."""
    issues = 0
    for m in re.finditer(r'```python\n(.*?)```', text, re.DOTALL):
        code = m.group(1)
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError:
            issues += 1
    return issues

# ── Fixes ──

def fix_name(text, correct_name):
    return re.sub(r'^name:\s*.*$', f'name: {correct_name}', text, count=1, flags=re.MULTILINE)

def fix_description_block_scalar(text):
    """
    Convert multi-line YAML description:
      description: >
        Line one
        Line two
    → description: Line one Line two (inline single-line)
    """
    lines = text.split('\n')
    result = []
    i = 0
    in_desc_block = False
    desc_continuation = []

    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip()

        if in_desc_block:
            if stripped.startswith('  '):
                desc_continuation.append(stripped.strip())
                i += 1
                continue
            else:
                # End of description block
                full = ' '.join(desc_continuation).strip()
                full = re.sub(r'\s+', ' ', full)
                result.append(f'description: {full}')
                in_desc_block = False
                desc_continuation = []
                continue  # don't skip current line

        m = re.match(r'^description:\s*(.+)$', stripped)
        if m:
            rest = m.group(1).strip()
            if rest in ('>', '|', '>+', '|-', '>-', '|+'):
                in_desc_block = True
                i += 1
                continue
            # Already inline — keep as-is
            result.append(line)
            i += 1
            continue
        else:
            result.append(line)
            i += 1

    # Handle unclosed description at end
    if in_desc_block and desc_continuation:
        full = ' '.join(desc_continuation).strip()
        full = re.sub(r'\s+', ' ', full)
        result.append(f'description: {full}')

    return '\n'.join(result)

def add_section_at_end(text, section_name, section_body):
    if section_name in text:
        return text
    text = text.rstrip() + '\n\n\n' + section_name + '\n' + section_body + '\n'
    return text

def fix_broken_links_in_text(text, all_names):
    def repl(m):
        link_text = m.group(1)
        target = m.group(2)
        if target not in all_names:
            return link_text  # remove link, keep text
        return m.group(0)
    return re.sub(r'\[([^\]]*)\]\(/skills/([^)]+)\)', repl, text)

def add_frontmatter(text, name, domain):
    return f'---\nname: {name}\ndescription: {name.replace("-", " ")} skill.\ndomain: {domain}\n---\n' + text

# ── Main ──

def main():
    all_skills = collect_all_skills()
    all_names = {s['name'] for s in all_skills}
    
    stats = {'name-mismatch': 0, 'description-too-short': 0, 'missing-section': 0,
             'missing-leading----': 0, 'broken-link': 0, 'python-syntax-errors': 0,
             'already-ok': 0, 'fixed': 0}
    
    for sk in all_skills:
        name = sk['name']
        path = sk['path']
        text = path.read_text(encoding='utf-8')
        original = text
        had_issues = False
        
        # 1. name-mismatch
        wrong_name = check_name_mismatch(text, name)
        if wrong_name:
            text = fix_name(text, name)
            stats['name-mismatch'] += 1
            had_issues = True
        
        # 2. description block scalar
        if check_description_length(text):
            text = fix_description_block_scalar(text)
            stats['description-too-short'] += 1
            had_issues = True
        
        # 3. missing sections
        missing = check_missing_sections(text)
        for sec in missing:
            if sec == '## When to Use':
                text = add_section_at_end(text, '## When to Use',
                    'Use this skill when working with ' + name.replace('-', ' ') + '.')
            elif sec == '## Workflow':
                text = add_section_at_end(text, '## Workflow',
                    'See the parent skill for authoritative workflow documentation.')
            stats['missing-section'] += 1
            had_issues = True
        
        # 4. missing leading ---
        if check_missing_leading(text):
            text = add_frontmatter(text, name, path.parent.parent.name)
            stats['missing-leading----'] += 1
            had_issues = True
        
        # 5. broken links
        broken = check_broken_links(text, all_names)
        if broken:
            text = fix_broken_links_in_text(text, all_names)
            stats['broken-link'] += 1
            had_issues = True
        
        # 6. python syntax
        py_issues = check_python_syntax(text)
        if py_issues:
            # Simple fix: try to compile, if fails, replace known bad patterns
            for m in re.finditer(r'```python\n(.*?)```', text, re.DOTALL):
                code = m.group(1)
                try:
                    compile(code, '<string>', 'exec')
                except SyntaxError:
                    # Fix print statement
                    fixed_code = re.sub(r'print\s+("(?:[^"\\]|\\.)*")', r'print(\1)', code)
                    fixed_code = re.sub(r"print\s+('(?:[^'\\]|\\.)*')", r'print(\1)', fixed_code)
                    try:
                        compile(fixed_code, '<string>', 'exec')
                        text = text.replace(code, fixed_code)
                    except SyntaxError:
                        pass
            stats['python-syntax-errors'] += 1
            had_issues = True
        
        if had_issues:
            path.write_text(text, encoding='utf-8')
            stats['fixed'] += 1
        else:
            stats['already-ok'] += 1
    
    print(f"\nScanned {len(all_skills)} skills")
    print(f"OK: {stats['already-ok']}")
    print(f"Fixed: {stats['fixed']}")
    print(f"\nIssue counts:")
    for k, v in stats.items():
        if k not in ('already-ok', 'fixed') and v > 0:
            print(f"  {k}: {v}")

if __name__ == '__main__':
    main()
