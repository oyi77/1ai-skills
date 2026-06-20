---
name: dagster-pipelines
description: Dagster data orchestration — software-defined assets, ops, jobs, schedules, sensors, IO managers
domain: data
tags:
- analytics
- dagster
- data-analysis
- pipelines
- visualization
---


## Overview

Dagster is a modern data orchestrator that treats data assets as first-class citizens. It uses software-defined assets to declare what data to produce, with built-in testing, type checking, and observability through the Dagit UI.

## Capabilities

- Define software-defined assets with @asset decorator
- Build jobs from asset selections
- Schedule and trigger jobs with schedules and sensors
- Manage data I/O with IO managers
- Partition assets by time, category, or custom dimensions
- Test pipelines locally before deployment
- Monitor runs via Dagit web UI

## When to Use

- Building asset-centric data pipelines
- Needing strong typing and testing for data workflows
- Wanting local development and testing before production
- Managing incremental/partitioned data processing
- Coordinating dbt models with Python transformations

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The dagster-pipelines workflow follows a standard pipeline pattern.

Core flow:
```
# dagster-pipelines primary flow
input = prepare(raw_data)
result = process(input, config={assets, dagster, data, defined, jobs})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Software-Defined Asset

```python
from dagster import asset, MaterializeResult
import pandas as pd

@asset
def raw_orders() -> pd.DataFrame:
    """Load raw orders from source database."""
    return pd.read_sql("SELECT * FROM orders", con=engine)

@asset
def cleaned_orders(raw_orders: pd.DataFrame) -> pd.DataFrame:
    """Clean and validate orders."""
    df = raw_orders.dropna(subset=['customer_id'])
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

@asset
def daily_summary(cleaned_orders: pd.DataFrame) -> pd.DataFrame:
    """Aggregate daily order summary."""
    return cleaned_orders.groupby('order_date').agg(
        total_orders=('order_id', 'count'),
        total_revenue=('amount', 'sum'),
    ).reset_index()
```

### Asset with Partitions

```python
from dagster import asset, DailyPartitionsDefinition

daily_partitions = DailyPartitionsDefinition(start_date="2025-01-01")

@asset(partitions_def=daily_partitions)
def daily_events(context) -> pd.DataFrame:
    """Load events for a specific partition date."""
    partition_date = context.partition_key
    return pd.read_sql(
        f"SELECT * FROM events WHERE date = '{partition_date}'",
        con=engine,
    )
```

### Asset with Metadata

```python
@asset
def enriched_customers(cleaned_orders: pd.DataFrame) -> pd.DataFrame:
    """Enrich customer data with order history."""
    df = cleaned_orders.merge(customers, on='customer_id')
    return MaterializeResult(
        value=df,
        metadata={
            "row_count": len(df),
            "columns": list(df.columns),
            "null_counts": df.isnull().sum().to_dict(),
        },
    )
```

### IO Manager

```python
from dagster import ConfigurableIOManager
import pandas as pd

class S3ParquetIOManager(ConfigurableIOManager):
    bucket: str

    def handle_output(self, context, obj):
        path = f"s3://{self.bucket}/{context.asset_key.path[-1]}.parquet"
        obj.to_parquet(path)

    def load_input(self, context):
        path = f"s3://{self.bucket}/{context.asset_key.path[-1]}.parquet"
        return pd.read_parquet(path)
```

### Job and Schedule

```python
from dagster import define_asset_job, schedule, ScheduleDefinition

# Job: materialize specific assets
daily_etl_job = define_asset_job(
    name="daily_etl",
    selection=["raw_orders", "cleaned_orders", "daily_summary"],
)

# Schedule
daily_schedule = ScheduleDefinition(
    job=daily_etl_job,
    cron_schedule="0 6 * * *",
)
```

### Sensor

```python
from dagster import sensor, RunRequest, SkipReason
import os

@sensor(job=daily_etl_job)
def new_file_sensor(context):
    path = "/data/incoming/"
    files = [f for f in os.listdir(path) if f.endswith('.csv')]
    if not files:
        return SkipReason("No new files")
    return RunRequest(
        run_key=files[0],
        run_config={"ops": {"raw_orders": {"config": {"filename": files[0]}}}},
    )
```

### dbt Integration

```python
from dagster_dbt import DbtCliClient, dbt_assets, DbtProject

@dbt_assets(manifest=DbtProject(project_dir="/dbt").manifest_path())
def my_dbt_assets(context, dbt: DbtCliClient):
    yield from dbt.cli(["build"], context=context).stream()
```

## Common Patterns

| Pattern | When to Use |
|---------|------------|
| `@asset` | Define a data asset |
| `@asset(partitions_def=...)` | Partitioned incremental processing |
| `IOManager` | Custom data storage/retrieval |
| `define_asset_job` | Select assets for a job |
| `ScheduleDefinition` | Cron-based scheduling |
| `@sensor` | Event-driven triggers |
| `MaterializeResult` | Return metadata with asset output |
| `@dbt_assets` | Integrate dbt models |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `DagsterInvalidDefinitionError` | Circular dependency or missing input | Check asset dependency graph in Dagit |
| Asset materialization failed | Runtime error in asset function | Check Dagit run logs for traceback |
| Partition missing | Partition not yet materialized | Run backfill or check partition mapping |
| IO manager error | Storage connection issue | Verify credentials and bucket/path |

## How to Use

1. Define data sources, sinks, and transformation requirements
2. Implement extraction with error handling and schema validation
3. Add transformation logic with idempotency guarantees
4. Configure loading with conflict resolution (upsert/append)
5. Set up monitoring for pipeline health and data freshness
6. Test with representative sample data before production

## Red Flags

- **Data pipeline has no error handling**: Silent failures corrupt downstream datasets
- **No data validation at boundaries**: Bad input propagates through entire pipeline
- **Missing monitoring for data freshness**: Stale data causes wrong business decisions
- **No rollback on failed transforms**: Failed transforms without rollback require manual recovery
- **Hardcoded connection strings**: Credentials in code get committed to version control

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
