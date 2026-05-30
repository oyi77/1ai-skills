---
name: lakefs-versioning
description: LakeFS data versioning — Git-like branching for data lakes, atomic commits, time travel, CI/CD
---

## Overview

LakeFS brings Git-like version control to data lakes. It enables branching, committing, merging, and reverting data changes — supporting atomic operations, isolated experimentation, and CI/CD for data.

## Capabilities

- Create branches for isolated data experiments
- Commit atomic changes to data
- Merge branches with conflict detection
- Time travel to any previous data state
- Run pre-commit and pre-merge hooks (CI/CD)
- Works with S3, Azure Blob, GCS as storage backends
- Compatible with Spark, Presto, Trino, Hive, dbt

## When to Use

- Needing reproducible data pipelines
- Experimenting with data changes without risk
- Implementing CI/CD for data quality
- Rolling back failed data updates
- Supporting multi-tenant data isolation

## When NOT to Use

- Task is about data processing, not versioning
- You need real-time data streaming (use streaming tools)
- Task is about data storage, not version control
- You don't have data pipeline infrastructure
- Task is about database migrations (use migration tools)
- You need data warehousing, not versioning

## Pseudo Code

Implementation patterns for common use cases with this skill.


### Installation

```bash
# Docker
docker run -p 8000:8000 treeverse/lakefs:latest

# Access at http://localhost:8000
# Default credentials: admin / admin
```

### CLI Operations

```bash
# Install lakectl
brew install lakefs/tap/lakectl

# Configure
lakectl config
# Endpoint: http://localhost:8000
# Access Key: AKIAIOSFODNN7EXAMPLE
# Secret Key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

# Repository operations
lakectl repo create my-repo s3://my-bucket
lakectl branch create my-repo/main-branch

# Branch
lakectl branch create my-repo/experiment-1 --source my-repo/main

# Upload data
lakectl fs upload s3://my-repo/experiment-1/data/file.parquet --source ./file.parquet

# Commit
lakectl commit my-repo/experiment-1 -m "Add new data"

# Merge
lakectl merge my-repo/experiment-1 my-repo/main

# Diff
lakectl diff my-repo/main my-repo/experiment-1

# Time travel
lakectl fs ls my-repo/main@commit-abc123/data/
```

### Python SDK

```python
import lakefs

# Connect
repo = lakefs.repository("my-repo")

# Create branch
branch = repo.branch("experiment-1").create(source_reference="main")

# Upload object
obj = branch.object("data/new_file.parquet")
obj.upload(data=open("file.parquet", "rb"))

# Commit
branch.commit(message="Add new data", metadata={"author": "etl-pipeline"})

# Merge
branch.merge_into("main", message="Merge experiment results")

# List objects
for obj in branch.objects(prefix="data/"):
    print(obj.path, obj.size_bytes)

# Time travel
main_branch = repo.branch("main")
for obj in main_branch.objects(prefix="data/", ref="commit-abc123"):
    print(obj.path)
```

### Spark Integration

```python
# S3 gateway endpoint
spark.conf.set("spark.hadoop.fs.s3a.endpoint", "http://localhost:8000")
spark.conf.set("spark.hadoop.fs.s3a.access.key", "AKIAIOSFODNN7EXAMPLE")
spark.conf.set("spark.hadoop.fs.s3a.secret.key", "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY")

# Read from branch
df = spark.read.parquet("s3a://my-repo/experiment-1/data/")

# Write to branch
df.write.parquet("s3a://my-repo/experiment-1/output/")
```

### Hooks (CI/CD)

```yaml
# .lakefs.yaml
pre_commit:
  - name: check_format
    type: lua
    properties:
      script: |
        for _, obj in ipairs(objects) do
          if not string.match(obj.path, "%.parquet$") then
            error("Only parquet files allowed: " .. obj.path)
          end
        end

pre_merge:
  - name: validate_schema
    type: lua
    properties:
      script: |
        -- Run schema validation before merge
        -- Reject if breaking changes detected
```

### Garbage Collection

```bash
# Configure retention policy
lakectl gc set-config my-repo --from-file gc-config.yaml
```

```yaml
# gc-config.yaml
default_retention_days: 30
branches:
  - branch: main
    retention_days: 90
  - branch: experiment-*
    retention_days: 7
```

## Common Patterns

| Pattern | When to Use |
|---------|------------|
| Branch → Experiment → Merge | Safe data changes |
| Commit with metadata | Track data lineage |
| Pre-merge hooks | Data quality gates |
| Time travel | Audit and rollback |
| Garbage collection | Clean up old versions |
| Multi-branch | Isolated dev/staging/prod |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| Merge conflict | Same file modified on both branches | Resolve manually or use strategy |
| Branch not found | Typo or deleted branch | Check `lakectl branch list` |
| Storage error | S3/GCS credentials | Verify storage config |
| Hook rejected | Pre-commit/merge check failed | Fix data or hook logic |

## Red Flags

- Claiming completion without running verification
- Skipping the analysis phase and jumping to implementation
- Ignoring existing codebase patterns and conventions

## Verification

- [ ] Output matches the original requirements
- [ ] All code or content runs without errors
- [ ] Edge cases have been considered and handled
- [ ] No placeholder content or TODOs remain