---
name: data-cleaner
description: Use when preparing raw datasets for analysis — handling missing values, removing duplicates, standardizing types, and generating cleaning reports.
domain: data
tags: [analytics, data, cleaning, preprocessing]
version: 1.0.0
---

# Data Cleaner

> **Redirect stub — full documentation at parent [data/analysis](../SKILL.md). This page is a quick reference for standalone use.**

## Quick Reference

Data cleaning is the highest-leverage phase of any analysis engagement — clients pay for confidence in their data, not for charts. This skill implements a **config-driven cleaning pipeline** that handles duplicates, missing values (median/mode/zero/forward-fill), high-missingness column removal, and type coercion in one pass, plus a human-readable cleaning report.

The parent skill covers the full pipeline (clean → detect → report → visualize) with money-making protocol for pricing cleaning-only engagements.

### Quick Start

1. **Profile first** — Run `profile_dataset(df)` to inventory missing values, duplicates, and dtypes before cleaning
2. **Configure strategy** — Build a fill_strategy dict per column: `{"age": "median", "category": "mode", "revenue": "zero"}`
3. **Execute & report** — Call `clean_dataset(df, config)` then `cleaning_report(before, after)` for a client-ready summary

### Focused Code Example

```python
import pandas as pd

df = pd.read_csv("client_data.csv")
before = df.copy()

# Config-driven cleaning
config = {
    "drop_duplicates": True,
    "fill_strategy": {
        "age": "median",
        "category": "mode",
        "revenue": "zero",
        "notes": "forward",
    },
    "drop_high_missing": 80,      # drop columns >80% null
    "type_coercions": {
        "date": "datetime64[ns]",
        "price": "float64",
    },
}

result = df.copy()

if config.get("drop_duplicates"):
    result = result.drop_duplicates()

for col, strat in config.get("fill_strategy", {}).items():
    if col in result.columns:
        if strat == "median" and result[col].dtype.kind in "fc":
            result[col] = result[col].fillna(result[col].median())
        elif strat == "mode":
            result[col] = result[col].fillna(result[col].mode().iloc[0] if not result[col].mode().empty else "")
        elif strat == "zero":
            result[col] = result[col].fillna(0)
        elif strat == "forward":
            result[col] = result[col].ffill()

# Cleaning report
print(f"Rows: {len(before)} → {len(result)} ({len(before)-len(result)} removed)")
print(f"Columns: {len(before.columns)} → {len(result.columns)}")
```

### Verification Checklist

- [ ] Duplicates dropped and count documented in cleaning report
- [ ] Missing values handled per-column with appropriate strategy (not one-size-fits-all)
- [ ] Columns with >80% missingness removed (or documented if kept intentionally)
- [ ] Type coercions verified — date columns parse, numeric columns are float/int, strings are object
- [ ] Cleaning report generated showing before/after state for every change
- [ ] No hardcoded paths or client data in reusable pipeline code
- [ ] Cleaned dataset exported as CSV/Parquet alongside raw copy

### Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Cleaning is not billable" | Cleaning IS the value. Clients pay for confidence in their data, not for charts. Bill $200–$800 for cleaning-only engagements. |
| "One fill strategy works for all columns" | Median for skewed numeric, mode for categorical, zero for revenue/quantity, forward-fill for time series — each column needs its own strategy documented in the report. |
| "Drop all rows with nulls" | Aggressive dropping destroys sample size and introduces bias. Only drop when missingness is random and <1% of rows. |
| "Cleaning happens in Excel before I get the data" | You will never receive clean data. Expect and charge for cleaning — it's 40% of every engagement. |

## When to Use
Use this skill when preparing raw datasets for analysis — handling missing values, removing duplicates, standardizing types, and generating cleaning reports that document every transformation.

## Workflow
See the parent skill for authoritative workflow documentation.
