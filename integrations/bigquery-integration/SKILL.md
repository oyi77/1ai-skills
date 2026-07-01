---
name: bigquery-integration
description: Integrate Google BigQuery for large-scale data analytics. Write SQL queries, manage datasets, export results, and build data pipelines.
domain: integrations
tags:
- bigquery
- google-cloud
- sql
- analytics
- data-warehouse
- etl
---

# Bigquery Integration

## When to Use
**Trigger phrases:**
- "bigquery integration"
- "Integrate Google BigQuery for large-scale data analytics"


- When querying large datasets (TB-scale) with SQL
- When building data warehouses or analytics pipelines
- When exporting BigQuery results to applications
- When managing BigQuery datasets, tables, and permissions

## When NOT to Use

- For small datasets (use PostgreSQL or SQLite)
- For real-time transactional data (use OLTP databases)

## Overview

Google BigQuery integration for serverless, scalable data analytics. Supports SQL queries, data loading, export, and dataset management.

## Workflow

1. **Set up auth** - Service account or ADC
2. **Install SDK** - `@google-cloud/bigquery` or `google-cloud-bigquery`
3. **Manage datasets** - Create, list, delete datasets and tables
4. **Load data** - CSV, JSON, Avro, Parquet from GCS or local
5. **Run queries** - SQL queries with parameterization
6. **Export results** - To DataFrames, CSV, or streaming inserts

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "SELECT * is fine" | BigQuery charges per bytes scanned - always select specific columns |
| "I do not need partitions" | Partitioned tables reduce query costs by 90%+ |

## Code Example (Python)

```python
from google.cloud import bigquery

client = bigquery.Client()

query = '''
    SELECT name, SUM(amount) as total
    FROM `project.dataset.transactions`
    WHERE date >= @start_date
    GROUP BY name
    ORDER BY total DESC
    LIMIT 10
'''
job_config = bigquery.QueryJobConfig(
    query_parameters=[bigquery.ScalarQueryParameter('start_date', 'DATE', '2026-01-01')]
)

results = client.query(query, job_config=job_config).to_dataframe()
```

## Verification

- [ ] Auth configured and working
- [ ] Queries return correct results
- [ ] Parameterized queries prevent injection
- [ ] Costs tracked per query

