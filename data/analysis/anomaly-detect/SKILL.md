---
name: anomaly-detect
description: Anomaly Detect. Use when working with anomaly detect in data domain.
domain: data
tags:
- analytics
- anomaly
- data-analysis
- detect
- visualization
---
# Anomaly Detect

## When to Use

**Trigger phrases:**
- "anomaly detect"
- "Help me with anomaly detect"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


## When NOT to Use

- For real-time transactional workloads (use OLTP databases)
- When the dataset fits in a spreadsheet (use simpler tools)
- When data privacy regulations prohibit cloud processing


## Overview

Anomaly Detect handles data analysis with support for multiple data formats and sources.

## Workflow

```python
# Example: Data pipeline
import pandas as pd

def pipeline(source: str):
    df = pd.read_csv(source)
    df = df.dropna()
    df = df.drop_duplicates()
    df["processed_at"] = pd.Timestamp.now()
    return df.to_parquet("output.parquet")
```

1. **Connect** — Establish connection to data sources
2. **Extract** — Pull data from source systems
3. **Transform** — Apply cleaning, normalization, and enrichment
4. **Load** — Write processed data to target destinations
5. **Validate** — Verify data quality and completeness
6. **Document** — Record schema changes and data lineage

## Data Quality Checks

- [ ] No null values in required fields
- [ ] Data types match schema definitions
- [ ] Referential integrity maintained
- [ ] Duplicate detection applied
- [ ] Outlier handling documented

## Supported Formats

- JSON, CSV, Parquet, Avro
- SQL databases (PostgreSQL, MySQL, SQLite)
- REST APIs and webhooks
- File systems (local, S3, GCS)

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "CSV is fine for everything" | Structured databases enable queries, integrity, and scale. |
| "I will add data validation later" | Bad data propagates silently. Validate at ingestion. |
| "Small datasets do not need optimization" | Even small datasets benefit from proper indexing and schema design. |


## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
1. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
1. **Reporting** — Document IOCs, write findings, provide remediation recommendations

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings