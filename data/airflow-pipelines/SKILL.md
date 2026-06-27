---
name: airflow-pipelines
description: Apache Airflow workflow orchestration — DAGs, operators, sensors, XComs, pools, scheduling
domain: data
tags:
- airflow
- analytics
- data-analysis
- pipelines
- visualization
- workflow
---


## Overview

Apache Airflow is the industry standard for programmatically authoring, scheduling, and monitoring data pipelines. This skill covers DAG design, operator selection, sensor patterns, XCom data passing, and production-ready pipeline patterns.

## Capabilities

- Define DAGs with tasks, dependencies, and scheduling
- Use Python, Bash, and Kubernetes operators for diverse workloads
- Implement sensors for event-driven triggers (file, API, database)
- Pass data between tasks with XComs
- Manage concurrency with pools and priority weights
- Handle backfills, retries, and alerting for production reliability
- Use Airflow Connections and Variables for configuration management

## When to Use

- Building scheduled data pipelines (ETL/ELT)
- Orchestrating multi-step workflows across systems
- Needing retry logic, alerting, and monitoring for batch jobs
- Coordinating tasks across databases, APIs, cloud services
- Managing backfills and historical data processing

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The airflow-pipelines workflow follows a standard pipeline pattern.

Core flow:
```
# airflow-pipelines primary flow
input = prepare(raw_data)
result = process(input, config={airflow, apache, dags, operators, orchestration})
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


### DAG Definition

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'email_on_failure': True,
    'email': ['alerts@company.com'],
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='etl_pipeline',
    default_args=default_args,
    description='Daily ETL pipeline',
    schedule_interval='0 6 * * *',  # 6 AM daily
    start_date=datetime(2025, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=['etl', 'production'],
) as dag:

    # Wait for input file
    wait_for_file = FileSensor(
        task_id='wait_for_input',
        filepath='/data/input/{{ ds }}/orders.csv',
        poke_interval=30,
        timeout=3600,
        mode='reschedule',  # Free up worker slot while waiting
    )

    # Extract data
    def extract(**context):
        import pandas as pd
        df = pd.read_csv(f'/data/input/{context["ds"]}/orders.csv')
        # Push to XCom (limit size; use S3/DB for large data)
        context['ti'].xcom_push(key='row_count', value=len(df))
        df.to_parquet(f'/tmp/extracted/{context["ds"]}.parquet')

    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract,
    )

    # Transform with bash
    transform_task = BashOperator(
        task_id='transform_data',
        bash_command='python /scripts/transform.py --date {{ ds }}',
    )

    # Load
    def load(**context):
        row_count = context['ti'].xcom_pull(task_ids='extract_data', key='row_count')
        print(f"Loading {row_count} rows")
        # Load to warehouse...

    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load,
    )

    wait_for_file >> extract_task >> transform_task >> load_task
```

### XCom Data Passing

```python
# Push data (small payloads only — use external storage for large data)
def push_data(**context):
    context['ti'].xcom_push(key='api_response', value={'status': 'ok', 'count': 42})

# Pull data
def consume_data(**context):
    data = context['ti'].xcom_pull(task_ids='api_call', key='api_response')
    print(f"Got {data['count']} records")
```

### Sensor with Poke vs Reschedule

```python
# poke: holds worker slot while waiting (good for short waits)
sensor = FileSensor(
    task_id='wait_short',
    filepath='/data/file.csv',
    poke_interval=10,
    timeout=300,
    mode='poke',
)

# reschedule: frees worker slot between checks (good for long waits)
sensor = FileSensor(
    task_id='wait_long',
    filepath='/data/file.csv',
    poke_interval=60,
    timeout=3600,
    mode='reschedule',
)
```

### Pool for Resource Limiting

```python
# Create pool: airflow pools set api_pool 2 "Limit API calls to 2 concurrent"
api_call = PythonOperator(
    task_id='call_api',
    python_callable=make_api_call,
    pool='api_pool',        # Use this pool
    pool_slots=1,           # Consume 1 slot
    priority_weight=10,     # Higher = scheduled first
)
```

### Branching

```python
from airflow.operators.python import BranchPythonOperator

def choose_branch(**context):
    date = context['ds']
    if datetime.strptime(date, '%Y-%m-%d').weekday() >= 5:
        return 'weekend_task'
    return 'weekday_task'

branch = BranchPythonOperator(
    task_id='branch_on_day',
    python_callable=choose_branch,
)

branch >> [weekday_task, weekend_task]
```

### TaskGroup for Organization

```python
from airflow.utils.task_group import TaskGroup

with TaskGroup(group_id='validation') as validate:
    check_schema = PythonOperator(task_id='check_schema', python_callable=validate_schema)
    check_nulls = PythonOperator(task_id='check_nulls', python_callable=validate_nulls)
    check_schema >> check_nulls
```

## Common Patterns

| Pattern | When to Use |
|---------|------------|
| `FileSensor` | Wait for upstream file delivery |
| `HttpSensor` | Wait for API endpoint to be ready |
| `ExternalTaskSensor` | Wait for another DAG's task to complete |
| `TriggerDagRunOperator` | Kick off another DAG |
| `BranchPythonOperator` | Conditional execution paths |
| `SubDagOperator` / TaskGroup | Group related tasks |
| `DummyOperator` | Dependency junction points |
| `PythonOperator` | Custom Python logic |
| `BashOperator` | Shell scripts, CLI tools |
| `KubernetesPodOperator` | Isolated containerized tasks |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| Task stuck in `upstream_failed` | Parent task failed | Fix upstream or set `trigger_rule='all_done'` |
| XCom value too large | Large data in XCom | Use S3/GCS path instead, push only reference |
| DAG not appearing | Import error or syntax issue | Check `airflow dags test <dag_id>` |
| Sensor timeout | Resource not available | Increase timeout or use `mode='reschedule'` |
| Max active runs reached | Concurrent DAG limit | Set `max_active_runs=1` or increase |

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

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "CSV is fine for everything" | Structured databases enable queries, integrity, and scale. |
| "I will add data validation later" | Bad data propagates silently. Validate at ingestion. |
| "Small datasets do not need optimization" | Even small datasets benefit from proper indexing and schema design. |