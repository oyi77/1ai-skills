---
name: review
description: Use when reviewing a diff for over-engineering. Finds what to delete
  — reinvented stdlib, needless deps, speculative abstractions.
domain: mindset
author: oyi77
license: Apache-2.0
subdomain: mindset
tags:
- review
- mindset
- ponytail
- simplification
version: 1.0.0
category: mindset
---



# Review — Diff Over-Engineering Detection

## Quick Reference

Review a diff for over-engineering. One line per finding: location, what to cut, what replaces it. The diff's best outcome is getting shorter.

## Overview

Review mode analyzes a diff (from a PR, staged changes, or any before/after text) and flags over-engineering patterns: unnecessary abstractions, new dependencies that duplicate stdlib, speculative code paths, and comments that explain the obvious. Each finding is a single line — location, pattern type, and a concrete fix suggestion. The goal is measurable: the diff should be shorter after review than before.

Scope: single diff. Output: one line per finding. Best outcome: diff gets shorter after review (net removal).

## Quick Start

1. **Stage your changes**: `git add -A` then run review on the staged diff
2. **Run review**: `ponytail review --diff "$(git diff --cached)"` — scans for over-engineering
3. **Apply cuts**: for each finding, decide: delete or keep. Aim for cutting 50% of added lines

## Key Command

```bash
# Review staged changes
git diff --cached | ponytail review --stdin --require-no-findings

# Review against main
ponytail review --diff "$(git diff main...HEAD)"
```

## Code Example: Review Script

```bash
#!/bin/bash
# Analyze a diff for over-engineering patterns
DIFF="${1}"

echo "# Red Flags"
# Flag new abstractions with few callers
echo "$DIFF" | grep "^+" | grep -iE "(interface|abstract class|factory|singleton|visitor)" \
    | while IFS= read -r line; do echo "- ABSTRACTION: $line"; done

# Flag new deps that are not in common allowlist
echo "$DIFF" | grep "^+" | grep -E "(from|import|require)" \
    | grep -vE "(react|vue|lodash|express|stdlib)" \
    | while IFS= read -r line; do echo "- NEW DEP: $line"; done

# Count net
added=$(echo "$DIFF" | grep "^+" | grep -v "^+++" | wc -l)
removed=$(echo "$DIFF" | grep "^-" | grep -v "^---" | wc -l)
echo "Net: +$((added - removed)) lines — aim to cut $((added / 2))"
```

## Review Checklist

- [ ] All unnecessary abstractions flagged (interfaces with one impl, single-use factories)
- [ ] New dependencies checked against stdlib alternatives
- [ ] Speculative code paths identified (unused branches, future-proofing)
- [ ] Comment-to-code ratio evaluated (self-documenting code preferred)
- [ ] Net line count calculated; recommended cuts documented

## When to Use

Use when review a diff for over-engineering. Finds what to delete — reinvented stdlib, needless deps, speculative abstractions.

## Workflow

Execute these steps sequentially:

1. **Stage your changes**: `git add -A` then run review on the staged diff
2. **Run review**: `ponytail review --diff "$(git diff --cached)"` — scans for over-engineering
3. **Apply cuts**: for each finding, decide: delete or keep. Aim for cutting 50% of added lines

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "This interface will be useful later" | The interface is a bet. Until there are two implementations, it costs more (indirection, boilerplate) than it saves |
| "One more dependency doesn't matter" | Every dependency is a supply chain risk, API surface, and version lock. Prove stdlib cannot do it first |
| "It's just a few comments" | Comments that restate the code are noise. Delete them and make the code self-documenting |
