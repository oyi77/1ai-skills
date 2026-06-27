---
name: spark-processing
description: Apache Spark distributed processing — DataFrames, SQL, streaming, MLlib, cluster management
domain: data
tags:
- analytics
- data-analysis
- machine-learning
- processing
- spark
- visualization
---


## Overview

Apache Spark is a unified analytics engine for large-scale data processing. It provides DataFrame APIs, SQL queries, streaming, and machine learning, running on YARN, Kubernetes, or standalone clusters.

## Capabilities

- Process petabyte-scale data with DataFrame API
- Run SQL queries on distributed data
- Handle real-time data with Structured Streaming
- Build ML pipelines with MLlib
- Optimize joins, shuffles, and partitioning
- Manage clusters on YARN, K8s, or standalone
- Use Delta Lake for ACID transactions

## When to Use

- Processing datasets too large for single-machine tools
- Running SQL analytics on data lakes
- Building real-time streaming pipelines
- Training ML models on distributed data
- ETL from multiple sources to data warehouse

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The spark-processing workflow follows a standard pipeline pattern.

Core flow:
```
# spark-processing primary flow
input = prepare(raw_data)
result = process(input, config={apache, cluster, dataframes, distributed, management})
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


### SparkSession Setup

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("ETL Pipeline") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .getOrCreate()
```

### DataFrame Operations

```python
# Read
df = spark.read.parquet("s3://bucket/data/")
df = spark.read.csv("path/to/file.csv", header=True, inferSchema=True)
df = spark.read.format("delta").load("s3://bucket/delta-table/")

# Transform
from pyspark.sql import functions as F

result = df \
    .filter(F.col("status") == "active") \
    .withColumn("year", F.year("order_date")) \
    .withColumn("amount_usd", F.col("amount") * F.lit(1.1)) \
    .groupBy("customer_id", "year") \
    .agg(
        F.count("*").alias("order_count"),
        F.sum("amount_usd").alias("total_spent"),
        F.avg("amount_usd").alias("avg_order"),
    )

# Write
result.write.mode("overwrite").parquet("s3://bucket/output/")
result.write.mode("append").format("delta").save("s3://bucket/delta-output/")
```

### Spark SQL

```python
# Register as temp view
df.createOrReplaceTempView("orders")

# Run SQL
result = spark.sql("""
    SELECT
        customer_id,
        YEAR(order_date) as year,
        COUNT(*) as order_count,
        SUM(amount) as total_spent
    FROM orders
    WHERE status = 'active'
    GROUP BY customer_id, YEAR(order_date)
    HAVING COUNT(*) > 5
    ORDER BY total_spent DESC
""")
```

### Joins and Optimization

```python
# Broadcast join (small table fits in memory)
from pyspark.sql.functions import broadcast

result = orders_df.join(broadcast(customers_df), "customer_id")

# Partition pruning (read only needed partitions)
df = spark.read.parquet("s3://bucket/data/") \
    .filter(F.col("date") == "2025-01-15")

# Repartition for downstream performance
df = df.repartition(200, "customer_id")

# Coalesce to reduce output files
df.coalesce(10).write.parquet("output/")
```

### Structured Streaming

```python
# Read stream from Kafka
stream_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:9092") \
    .option("subscribe", "events") \
    .load()

# Parse and transform
parsed = stream_df \
    .selectExpr("CAST(value AS STRING)") \
    .select(F.from_json(F.col("value"), schema).alias("data")) \
    .select("data.*")

# Windowed aggregation
windowed = parsed \
    .withWatermark("event_time", "10 minutes") \
    .groupBy(
        F.window("event_time", "5 minutes"),
        "event_type",
    ) \
    .count()

# Write stream
query = windowed.writeStream \
    .outputMode("update") \
    .format("delta") \
    .option("checkpointLocation", "s3://checkpoints/events/") \
    .start("s3://bucket/stream-output/")
```

### Delta Lake

```python
from delta.tables import DeltaTable

# MERGE (upsert)
delta_table = DeltaTable.forPath(spark, "s3://bucket/delta-table/")

delta_table.alias("target").merge(
    updates_df.alias("source"),
    "target.id = source.id",
) \
    .whenMatchedUpdate(set={"status": "source.status", "amount": "source.amount"}) \
    .whenNotMatchedInsertAll() \
    .execute()

# Time travel
df_v1 = spark.read.format("delta").option("versionAsOf", 1).load("path")
df_ts = spark.read.format("delta").option("timestampAsOf", "2025-01-15").load("path")
```

### MLlib Pipeline

```python
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.classification import RandomForestClassifier

# Feature engineering
indexer = StringIndexer(inputCol="category", outputCol="category_idx")
assembler = VectorAssembler(
    inputCols=["amount", "quantity", "category_idx"],
    outputCol="features",
)
rf = RandomForestClassifier(labelCol="label", featuresCol="features")

# Pipeline
pipeline = Pipeline(stages=[indexer, assembler, rf])
model = pipeline.fit(train_df)
predictions = model.transform(test_df)
```

## Common Patterns

| Pattern | When to Use |
|---------|------------|
| `broadcast(small_df)` | Join with small dimension table |
| `repartition(N, col)` | Optimize downstream shuffle |
| `coalesce(N)` | Reduce output file count |
| `cache()` / `persist()` | Reuse DataFrame across operations |
| `withWatermark()` | Handle late data in streaming |
| Delta MERGE | Upsert into target table |
| Delta Time Travel | Audit, rollback, historical queries |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `OutOfMemoryError` | Data skew or large shuffle | Increase executor memory, repartition |
| `AnalysisException` | Column not found or type mismatch | Check schema with `df.printSchema()` |
| `ShuffleFetchFailed` | Executor died during shuffle | Check cluster health, increase retries |
| Streaming lag | Processing slower than ingestion | Scale cluster, optimize transformations |

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