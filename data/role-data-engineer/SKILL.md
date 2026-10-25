---
name: role-data-engineer
description: Use when orchestrating data engineering pipelines, batch/streaming ETL,
  dbt data modeling, Airflow DAG orchestration, database query optimization, and warehouse
  warehousing.
domain: data
author: oyi77
version: 1.0.0
category: data
tags:
- data
- data-engineering
- etl
- dbt
- airflow
- spark
- kafka
- bigquery
- postgres
license: MIT
subdomain: data-engineering
---

## Overview

The `role-data-engineer` skill directs enterprise data platform architecture, ingestion pipeline orchestration, transformation modeling, and warehouse performance optimization. Rather than building fragile one-off extract scripts or unmonitored cron jobs, this role coordinates idempotent ETL/ELT pipelines, declarative data transformations via dbt, resilient DAG workflow scheduling with Apache Airflow, distributed batch/streaming computation (Spark, Kafka), and high-throughput query optimization across relational and cloud columnar warehouses (PostgreSQL, BigQuery).

```
[Phase 1: Ingestion & Schema Modeling] ──► [Phase 2: Stream/Batch Transport] ──► [Phase 3: dbt Transformation & Lineage]
                                                                                               │
                   [Phase 5: Quality & SLA Monitoring] ◄── [Phase 4: Warehouse Optimization] ◄─┘
```

The data engineer enforces data quality contracts, idempotent backfills, schema evolution guarantees, and least-privilege data access across all analytics assets.

## When to Use

- When building, repairing, or scaling multi-source batch or streaming ETL/ELT pipelines.
- When orchestrating scheduled data workflows, sensors, and dependency graphs with Apache Airflow.
- When creating modular, testable, and documented data transformation models using dbt.
- When optimizing slow SQL queries, database indexing strategies, and connection pool behavior in PostgreSQL.
- When processing large-scale distributed datasets using Apache Spark or streaming events via Apache Kafka.
- When managing analytics data warehouses, partitioning schemes, and cost optimization in Google BigQuery.

## When NOT to Use

- When building web application frontend UI components or design tokens (use `content/role-ui-ux-designer`).
- When implementing application business logic or REST API endpoints (use `development/role-software-engineer`).
- When conducting qualitative market research or web OSINT reconnaissance (use `research/role-research-analyst`).
- When managing general Kubernetes cluster infrastructure or Docker daemon configurations (use `devops/role-devops-sre-engineer`).

## Deterministic Dispatch Matrix

| Data Engineering Scope / Platform Objective | Delegated Child Skill | Primary Data Artifact |
|---|---|---|
| End-to-end multi-source ETL pipeline construction and telemetry | `research/data-pipeline-engine` | Operational pipeline DAG and data flow telemetry report |
| Declarative SQL transformations, data lineage, and schema tests | `data/dbt-transform` | Versioned dbt models, schema tests, and documentation |
| Scheduling, sensors, retries, and task dependency DAG management | `data/airflow-pipelines` | Production Airflow DAGs with idempotent execution hooks |
| Query plan optimization, indexing strategies, and lock mitigation | `development/postgres-queries` | Optimized SQL queries, EXPLAIN ANALYZE plan receipts |
| Cloud columnar warehouse schema modeling, partitioning, clustering | `integrations/bigquery-integration` | BigQuery partition/cluster schemas and cost budget guards |
| Distributed large-scale data processing and DataFrame operations | `data/spark-processing` | Spark PySpark/Scala jobs with tuned executor allocations |
| High-throughput distributed event streaming, topic partitioning | `development/kafka-patterns` | Kafka producer/consumer configs with dead-letter topics |

## Workflow

### Phase 1: Source Ingestion & Schema Contracts

1. Ingest structured and unstructured data from transactional DBs, APIs, and logs using `research/data-pipeline-engine`.
2. Define explicit schema contracts (Avro, Protobuf, JSON Schema) to prevent unexpected upstream breaking changes.
3. Enforce append-only or idempotent upsert mechanisms (`MERGE` statements on primary keys).

### Phase 2: Streaming & Batch Transport Layer

1. For real-time event ingestion, configure topics, partitions, and consumer groups via `development/kafka-patterns`.
2. For large batch datasets, distribute processing across compute nodes using `data/spark-processing`.
3. Implement dead-letter queues (DLQ) for corrupted or malformed payloads.

### Phase 3: Declarative Transformation with dbt

1. Structure transformation models following the medallion architecture (Bronze/Raw -> Silver/Cleaned -> Gold/Aggregated) via `data/dbt-transform`.
2. Write automated data quality tests (`unique`, `not_null`, `relationships`, `accepted_values`).
3. Document table and column descriptions directly in schema YAML files.

### Phase 4: Workflow Orchestration & Dependency Scheduling

1. Codify data pipelines into Directed Acyclic Graphs (DAGs) using `data/airflow-pipelines`.
2. Enforce idempotent task execution: rerunning a DAG for a past `execution_date` must produce the exact same deterministic dataset without duplicating rows.
3. Configure retry backoffs and failure alert webhooks.

### Phase 5: Storage Optimization & Quality Verification

1. Optimize PostgreSQL relational stores with targeted partial/composite indexes and VACUUM maintenance via `development/postgres-queries`.
2. In Google BigQuery, partition tables by date/timestamp and cluster by high-cardinality query keys using `integrations/bigquery-integration`.
3. Assert that data freshness, row counts, and transformation SLAs are monitored continuously.

## Anti-Rationalization

| Data Engineering Excuse | Flawed Rationalization | Required Data Platform Discipline |
|---|---|---|
| "Cron jobs are simpler than setting up Airflow" | "A single cron script in crontab is fast to write." | Cron lacks dependency tracking, backfills, retries, and failure visibility. Orchestrate pipelines with Airflow DAGs. |
| "We will clean up the dirty data in the dashboard" | "Tableau or BI tools can filter out nulls and duplicates." | Pushing data cleaning to BI layers causes conflicting metrics across teams. Transform and validate data at the dbt modeling layer. |
| "Writing dbt schema tests takes too much time" | "The raw tables come from production, so data is clean." | Upstream databases frequently have unexpected nulls, migrations, or bugs. Enforce automated schema tests on every model. |
| "Full table scans in BigQuery are fast enough" | "BigQuery handles petabytes easily, no need to partition." | Unpartitioned queries burn cloud budgets and fail to scale. Partition by event date and cluster by lookup keys. |
| "Just re-run the pipeline and ignore duplicate rows" | "Analytics only looks at rough trends anyway." | Non-idempotent pipelines poison financial and operational reporting. Enforce primary keys and idempotent upserts (`MERGE`). |

## Implementation Examples

### Idempotent Database Upsert Pipeline (Python/SQL)

```python
import psycopg2
from psycopg2.extras import execute_values
from typing import List, Tuple

def idempotent_upsert(conn, records: List[Tuple]):
    """Executes an idempotent batch upsert into PostgreSQL using ON CONFLICT."""
    query = """
    INSERT INTO analytics.daily_user_metrics (user_id, metric_date, session_count, revenue_cents)
    VALUES %s
    ON CONFLICT (user_id, metric_date) DO UPDATE SET
        session_count = EXCLUDED.session_count,
        revenue_cents = EXCLUDED.revenue_cents,
        updated_at = NOW();
    """
    with conn.cursor() as cur:
        execute_values(cur, query, records, page_size=1000)
    conn.commit()
    print(f"SUCCESS: Idempotently upserted {len(records)} records.")

if __name__ == "__main__":
    print("Idempotent data upsert framework initialized.")
```

### dbt Model & Test Verification (Bash)

```bash
#!/usr/bin/env bash
set -euo pipefail

MODEL_TARGET="core_orders"

echo "=== Step 1: Compiling and Running dbt Model: $MODEL_TARGET ==="
dbt run --select "$MODEL_TARGET"

echo "=== Step 2: Executing dbt Schema Tests ==="
dbt test --select "$MODEL_TARGET"

echo "SUCCESS: dbt model and data contract tests verified cleanly."
```

## Verification Checklist

- [ ] Ingestion pipelines enforce schema contracts and dead-letter queue isolation.
- [ ] Transformation models adhere to medallion layers (raw, clean, mart) in dbt.
- [ ] Airflow DAGs execute idempotently with deterministic backfill capabilities.
- [ ] Database query plans optimized using EXPLAIN ANALYZE with targeted indexing.
- [ ] BigQuery tables partitioned and clustered to minimize scan costs.
- [ ] Automated schema tests (`unique`, `not_null`, `relationships`) pass with zero defects.

## Sub-Skills & Specialized Playbooks

| Sub-skill | File | Use when |
|---|---|---|
| airflow-pipelines | [SKILL.md](../airflow-pipelines/SKILL.md) | Developing Apache Airflow DAGs, operators, sensors, and schedules. |
| dagster-pipelines | [SKILL.md](../dagster-pipelines/SKILL.md) | Building Dagster software-defined assets, resources, and jobs. |
| prefect-flows | [SKILL.md](../prefect-flows/SKILL.md) | Orchestrating Prefect flows, tasks, deployments, and work pools. |
| temporal-workflows | [SKILL.md](../temporal-workflows/SKILL.md) | Implementing durable Temporal workflows, retries, signals, and queries. |
| spark-processing | [SKILL.md](../spark-processing/SKILL.md) | Processing distributed data with Spark SQL, streaming, and MLlib. |
| lakefs-versioning | [SKILL.md](../../automation/lakefs-versioning/SKILL.md) | Versioning data lakes with lakeFS branches, commits, and time travel. |
