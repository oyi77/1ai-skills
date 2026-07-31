---
name: help
description: Use when quick reference for ponytail modes, skills, and commands. One-shot display.
domain: mindset
author: oyi77
license: Apache-2.0
subdomain: mindset
tags:
  - help
  - mindset
  - ponytail
  - reference
version: 1.0.0
---


# Help — Quick Reference Card for Ponytail Modes

## Quick Reference

One-shot display of ponytail modes, key commands, and skill discovery. Never changes mode, writes files, or persists anything. Pure reference.

## Overview

Help mode prints a concise reference card covering all four ponytail modes (audit, debt, review, help) and their commands, options, and output formats. It is the fastest way to learn the tools without reading the full parent skill. Designed for the moment you know what you want to do but cannot remember the exact flag.

Scope: session only. Output: reference card. Best outcome: developer finds the answer in 5 seconds.

## Quick Start

1. **Show help**: `ponytail help` — prints the full reference card
2. **Filter by mode**: `ponytail help --mode audit` — shows only audit commands
3. **Show examples**: `ponytail help --examples` — includes usage examples for each mode

## Key Command

```bash
ponytail help          # full reference card
ponytail help audit    # specific mode details
ponytail help --json   # machine-readable output for tooling
```

## Reference Card Output

```
~ ponytail commands ~
  audit    — Ranked list of what to delete/simplify repo-wide
  debt     — Collect ponytail: comments into a tracked ledger
  help     — This reference card
  review   — One-line-per-finding diff over-engineering check

Options:
  --path <dir>      Scope to directory
  --diff <text>     Diff text for review
  --output <file>   Write results to file
  --stdin           Read input from stdin
  --scan            Scan mode for debt
  --rank-by-impact  Sort audit findings by LOC savings
  --require-no-findings  Fail review if any issues found
```

## Help Checklist

- [ ] Reference card displays all four modes with correct descriptions
- [ ] All command options are listed and accurate
- [ ] Mode filtering works (show only one mode's commands)
- [ ] Examples are up-to-date with current tool behavior
- [ ] Output is parseable (plain text or --json)

## When to Use

Use when quick reference for ponytail modes, skills, and commands. One-shot display.

## Workflow

Execute these steps sequentially:

1. **Show help**: `ponytail help` — prints the full reference card
2. **Filter by mode**: `ponytail help --mode audit` — shows only audit commands
3. **Show examples**: `ponytail help --examples` — includes usage examples for each mode

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll just read the source" | Help is faster than grepping source. It is the single entry point — use it first |
| "I already know the commands" | Flags change, options get added. A 5-second help check prevents stale assumptions |
| "I can guess the flag names" | `--rank-by-impact` vs `--sort-by-size` — guessing wastes more time than reading help once |
