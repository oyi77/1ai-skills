# 1ai-skills Evaluation System

A lightweight evaluation framework for verifying skill quality and correctness.
Each eval case tests that a skill's content meets specific quality checks.

## Directory Structure

```
evals/
  README.md          — This file
  cases/             — Eval case definitions (one JSON per skill)
    development/
    devops/
    core/
    cybersecurity/
    ...
  reports/           — Generated eval results (optional, gitignored)
```

## Writing an Eval Case

Create a JSON file in `evals/cases/<category>/<skill-name>.json`:

```json
{
  "skill": "skill-name",
  "category": "development",
  "name": "Descriptive eval name",
  "description": "What this eval verifies",
  "checks": [
    {"type": "contains", "pattern": "required phrase"},
    {"type": "section_exists", "pattern": "When to Use"},
    {"type": "frontmatter_field", "field": "version"},
    {"type": "code_block_count", "min": 1},
    {"type": "anti_rat_table": true},
    {"type": "has_workflow_section"}
  ]
}
```

## Running Evals

```bash
# Run all evals
python3 scripts/run-evals.py

# List available eval cases
python3 scripts/run-evals.py --list

# Run evals for a specific skill
python3 scripts/run-evals.py --skill test-driven-development

# Run evals for a category
python3 scripts/run-evals.py --category development

# JSON output for CI/automation
python3 scripts/run-evals.py --json

# Verbose mode (show passing checks too)
python3 scripts/run-evals.py --verbose
```

## Check Types

| Type | Description | Parameters |
|------|-------------|------------|
| `contains` | SKILL.md body contains regex pattern | `pattern` (str) |
| `not_contains` | SKILL.md body does NOT contain pattern | `pattern` (str) |
| `section_exists` | Has markdown section heading matching regex | `pattern` (str) |
| `frontmatter_field` | Frontmatter field has expected value | `field` (str), `value` (str, optional) |
| `frontmatter_field_exists` | Frontmatter field exists (any value) | `field` (str) |
| `anti_rat_table` | Has anti-rationalization table | `true` |
| `code_block_count` | Fenced code blocks within count range | `min` (int, default 0), `max` (int, optional) |
| `has_workflow_section` | Has a workflow/process section | `true` |
| `trigger_phrase` | Description starts with "Use when" | `true` |
| `skill_depth` | SKILL.md is at least N lines | `min_lines` (int) |
| `has_code_example` | Has at least one fenced code block with language | `language` (str, optional) |

## Scope

Evals are NOT a replacement for `test-skills.py` (structural validation) or
`lint-skills.py` (quality linting). They verify higher-level behavioral and
content correctness — that a skill actually delivers what it promises.
