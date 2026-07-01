---
name: temporal-workflows
description: Temporal durable workflows — workflow/activity definitions, retries, signals, queries, versioning
domain: data
tags:
- analytics
- data-analysis
- temporal
- visualization
- workflow
- workflows
---


## Overview

Temporal is a durable execution platform for building reliable, fault-tolerant workflows. Workflows survive process crashes, network failures, and deployments. Activities handle side effects with automatic retries.

## Capabilities

- Define deterministic workflows with automatic replay
- Execute side effects in activities with retry policies
- Send signals to running workflows
- Query workflow state without side effects
- Use child workflows for composition
- Handle long-running operations (hours, days, months)
- Version workflows for safe deployments

## When to Use
**Trigger phrases:**
- "temporal workflows"
- "Temporal durable workflows — workflow/activity definitions, retries, signals, qu"


- Building reliable multi-step business processes
- Needing workflows that survive failures and restarts
- Managing long-running operations (order fulfillment, onboarding)
- Coordinating microservices with saga patterns
- Handling human-in-the-loop workflows

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The temporal-workflows workflow follows a standard pipeline pattern.

Core flow:
```
# temporal-workflows primary flow
input = prepare(raw_data)
result = process(input, config={activity, definitions, durable, queries, retries})
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


### Workflow Definition (Python)

```python
from temporalio import workflow
from datetime import timedelta

@workflow.defn
class OrderWorkflow:
    @workflow.run
    async def run(self, order: dict) -> str:
        # Validate
        await workflow.execute_activity(
            validate_order,
            order,
            start_to_close_timeout=timedelta(seconds=30),
        )

        # Process payment
        payment_result = await workflow.execute_activity(
            process_payment,
            order,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
                initial_interval=timedelta(seconds=1),
                backoff_coefficient=2.0,
            ),
        )

        # Ship
        await workflow.execute_activity(
            ship_order,
            order,
            start_to_close_timeout=timedelta(minutes=5),
        )

        return f"Order {order['id']} completed"
```

### Activity Definition

```python
from temporalio import activity

@activity.defn
async def validate_order(order: dict) -> bool:
    if not order.get('items'):
        raise ApplicationError("Empty order", non_retryable=True)
    return True

@activity.defn
async def process_payment(order: dict) -> dict:
    # Call payment gateway
    result = await payment_client.charge(order['total'])
    return {"transaction_id": result['id'], "status": "charged"}

@activity.defn
async def ship_order(order: dict) -> str:
    tracking = await shipping_client.create_shipment(order)
    return tracking['tracking_number']
```

### Signals and Queries

```python
@workflow.defn
class ApprovalWorkflow:
    def __init__(self):
        self._approved = False
        self._reason = ""

    @workflow.signal
    async def approve(self, approved: bool, reason: str = ""):
        self._approved = approved
        self._reason = reason

    @workflow.query
    def status(self) -> dict:
        return {"approved": self._approved, "reason": self._reason}

    @workflow.run
    async def run(self, request: dict) -> str:
        # Wait for approval signal
        await workflow.wait_condition(lambda: self._approved is not None)
        if self._approved:
            await workflow.execute_activity(process_request, request)
            return "Approved and processed"
        return f"Rejected: {self._reason}"
```

### Child Workflows

```python
@workflow.defn
class ParentWorkflow:
    @workflow.run
    async def run(self, items: list) -> list:
        results = []
        for item in items:
            result = await workflow.execute_child_workflow(
                ProcessItemWorkflow.run,
                item,
                id=f"process-{item['id']}",
            )
            results.append(result)
        return results
```

### Continue-As-New (Long-Running)

```python
@workflow.defn
class MonitoringWorkflow:
    @workflow.run
    async def run(self, state: dict):
        # Do work
        new_state = await workflow.execute_activity(check_status, state)

        # Sleep
        await workflow.sleep(timedelta(minutes=5))

        # Continue as new to avoid unbounded history
        workflow.continue_as_new(new_state)
```

### Workflow Client

```python
from temporalio.client import Client

async def main():
    client = await Client.connect("localhost:7233")

    # Start workflow
    handle = await client.start_workflow(
        OrderWorkflow.run,
        {"id": "123", "items": [...], "total": 99.99},
        id="order-123",
        task_queue="orders",
    )

    # Send signal
    await handle.signal(ApprovalWorkflow.approve, True, "Looks good")

    # Query
    status = await handle.query(ApprovalWorkflow.status)

    # Wait for result
    result = await handle.result()
```

## Common Patterns

| Pattern | When to Use |
|---------|------------|
| `execute_activity` | Side effects (DB, API, file I/O) |
| `RetryPolicy` | Transient failure handling |
| `workflow.signal` | External events (human input, webhooks) |
| `workflow.query` | Read state without side effects |
| `execute_child_workflow` | Compose workflows |
| `continue_as_new` | Long-running workflows (unbounded history) |
| `workflow.wait_condition` | Wait for state change |
| `workflow.sleep` | Timed delays |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `ActivityError` | Activity failed after retries | Check activity logs, adjust retry policy |
| `WorkflowReplayError` | Non-deterministic code in workflow | Move side effects to activities |
| `NonRetryableError` | Business logic error | Raise `ApplicationError(non_retryable=True)` |
| History too large | Long-running workflow | Use `continue_as_new` |

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