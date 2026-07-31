---
name: debt
description: Use when harvest ponytail shortcut comments into one debt ledger so deferrals get tracked instead of forgotten.
domain: mindset
author: oyi77
license: Apache-2.0
subdomain: mindset
tags:
  - debt
  - mindset
  - ponytail
  - tracking
version: 1.0.0
---


# Debt — Shortcut Deferral Ledger

## Quick Reference

Every `ponytail:` shortcut comment in the codebase gets harvested into one tracked ledger. Deferrals cannot quietly become permanent. One-shot report anytime.

## Overview

Debt mode finds every `ponytail:` annotation in source files, collects them into a structured ledger, and tracks each deferral with a ceiling (when it breaks) and an upgrade path (what fixes it). Unlike TODOs that drift into noise, the debt ledger is a living document you review weekly. If a ceiling is approaching, you fix it before it breaks.

Scope: `ponytail:` comments in codebase. Output: ledger of all deferrals. Best outcome: no forgotten shortcut.

## Quick Start

1. **Scan**: `ponytail debt --scan` — harvests every `ponytail:` comment into `.ponytail/debt.md`
2. **Review ledger**: read the ranked entries by directory — highest density means biggest risk area
3. **Prioritize 3 entries**: fix the ones whose ceiling is closest to being breached

## Key Command

```bash
ponytail debt --scan --output .ponytail/debt.md && grep -c "TODO|FIXME|HACK|ponytail:" .ponytail/debt.md
```

## Code Example: Debt Scanner

```bash
#!/bin/bash
# Collect every ponytail: comment into a structured ledger
SEARCH_DIR="${1:-.}"
OUTPUT="${2:-.ponytail/debt.md}"
mkdir -p "$(dirname "$OUTPUT")"

echo "# Ponytail Debt Ledger" > "$OUTPUT"
echo "Generated: $(date)" >> "$OUTPUT"

grep -rn "ponytail:" "$SEARCH_DIR" --include="*.py" --include="*.ts" \
    --include="*.js" --include="*.go" --include="*.rs" \
    | grep -v ".ponytail/" | sort > /tmp/ponytail-comments.txt

# Count by directory
echo "## By Directory" >> "$OUTPUT"
awk -F: '{print $1}' /tmp/ponytail-comments.txt \
    | xargs -I{} dirname {} | sort | uniq -c | sort -rn >> "$OUTPUT"

echo "## All Entries" >> "$OUTPUT"
while IFS=: read -r file line rest; do
    echo "- **$file:$line** — $rest" >> "$OUTPUT"
done < /tmp/ponytail-comments.txt
echo "Total: $(wc -l < /tmp/ponytail-comments.txt) entries"
```

## Debt Checklist

- [ ] All `ponytail:` comments collected into single ledger file
- [ ] Every entry has a ceiling (when this breaks) and upgrade path
- [ ] Entries grouped by directory to surface high-risk areas
- [ ] Weekly review scheduled to prevent forgotten deferrals
- [ ] Top 3 entries by ceiling urgency have fix tickets assigned

## When to Use

Use when harvest ponytail shortcut comments into one debt ledger so deferrals get tracked instead of forgotten.

## Workflow

Execute these steps sequentially:

1. **Scan**: `ponytail debt --scan` — harvests every `ponytail:` comment into `.ponytail/debt.md`
2. **Review ledger**: read the ranked entries by directory — highest density means biggest risk area
3. **Prioritize 3 entries**: fix the ones whose ceiling is closest to being breached

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll remember to fix this later" | You won't. Without a ledger, every temporary hack is permanent. Write the ceiling and upgrade path now |
| "Tracking debt is overhead" | One weekly 5-minute scan prevents one production incident per quarter. The ROI is 100:1 |
| "My TODO comments are enough" | TODOs have no ceiling, no upgrade path, and no accountability. Debt ledger forces structure |
