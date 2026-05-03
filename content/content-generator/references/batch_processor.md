# BatchProcessor Class

Processor for handling multiple video generation jobs with concurrency control.

## Overview

```python
from scripts.batch_processor import BatchProcessor, BatchJob, JobStatus
```

Allows processing multiple prompts concurrently with configurable limits.

---

## Enums

### JobStatus

Status of a batch job.

```python
class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
```

---

## Dataclasses

### BatchJob

Represents a single job in a batch.

```python
@dataclass
class BatchJob:
    job_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    prompt: str = ""
    status: JobStatus = JobStatus.PENDING
    result: Optional[Any] = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
```

**Attributes:**
- `job_id` - Unique job identifier
- `prompt` - The prompt for this job
- `status` - Current job status
- `result` - Job result (if completed)
- `error` - Error message (if failed)
- `created_at` - When job was created
- `started_at` - When job started processing
- `completed_at` - When job completed

#### to_dict()

Convert job to dictionary.

```python
def to_dict(self) -> dict
```

---

## BatchProcessor Class

```python
class BatchProcessor:
    def __init__(
        self,
        max_concurrent: int = 3,
        process_func: Optional[Callable[[str], Any]] = None,
    ):
```

**Constructor Parameters:**
- `max_concurrent` - Maximum number of concurrent jobs (default: 3)
- `process_func` - Function to call for processing each prompt

---

## Methods

### create_job()

Create a new batch job.

```python
def create_job(self, prompt: str) -> BatchJob
```

**Parameters:**
- `prompt` - The prompt for the job

**Returns:** Created BatchJob object

---

### create_jobs()

Create multiple batch jobs from prompts.

```python
def create_jobs(self, prompts: list[str]) -> list[BatchJob]
```

**Parameters:**
- `prompts` - List of prompts

**Returns:** List of created BatchJob objects

---

### process_batch()

Process multiple prompts with concurrency control.

```python
async def process_batch(
    self,
    prompts: list[str],
    process_func: Optional[Callable[[str], Any]] = None,
) -> list[BatchJob]
```

**Parameters:**
- `prompts` - List of prompts to process
- `process_func` - Function to call for processing each prompt (overrides the one set in __init__)

**Returns:** List of completed BatchJob objects

**Note:** Uses asyncio.Semaphore to limit concurrent jobs

---

### get_job_status()

Get the status of a specific job.

```python
def get_job_status(self, job_id: str) -> Optional[BatchJob]
```

**Parameters:**
- `job_id` - The ID of the job to check

**Returns:** BatchJob object if found, None otherwise

---

### get_all_job_statuses()

Get status of all jobs.

```python
def get_all_job_statuses(self) -> list[BatchJob]
```

**Returns:** List of all BatchJob objects

---

### get_jobs_by_status()

Get all jobs with a specific status.

```python
def get_jobs_by_status(self, status: JobStatus) -> list[BatchJob]
```

**Parameters:**
- `status` - JobStatus to filter by

**Returns:** List of matching BatchJob objects

---

### cancel_job()

Cancel a specific job if it's still pending.

```python
def cancel_job(self, job_id: str) -> bool
```

**Parameters:**
- `job_id` - The ID of the job to cancel

**Returns:** True if cancelled, False if not found or not pending

---

### get_batch_summary()

Get a summary of the batch processing status.

```python
def get_batch_summary(self) -> dict
```

**Returns:** Dictionary with counts:
- `total` - Total number of jobs
- `pending` - Number of pending jobs
- `running` - Number of running jobs
- `completed` - Number of completed jobs
- `failed` - Number of failed jobs
- `cancelled` - Number of cancelled jobs

---

## Usage Example

```python
import asyncio
from scripts.batch_processor import BatchProcessor, JobStatus

async def process_prompt(prompt: str):
    """Example processing function"""
    # Your generation logic here
    await asyncio.sleep(1)  # Simulate work
    return {"prompt": prompt, "status": "done"}

async def main():
    # Create processor with max 3 concurrent jobs
    processor = BatchProcessor(max_concurrent=3)
    
    # Define prompts to process
    prompts = [
        "Generate a video about product A",
        "Generate a video about product B",
        "Generate a video about product C",
        "Generate a video about product D",
        "Generate a video about product E",
    ]
    
    # Process batch
    jobs = await processor.process_batch(
        prompts=prompts,
        process_func=process_prompt
    )
    
    # Check results
    summary = processor.get_batch_summary()
    print(f"Summary: {summary}")
    
    # Print individual job results
    for job in jobs:
        print(f"Job {job.job_id}: {job.status.value}")
        if job.status == JobStatus.COMPLETED:
            print(f"  Result: {job.result}")
        elif job.status == JobStatus.FAILED:
            print(f"  Error: {job.error}")

asyncio.run(main())
```

---

## Sync and Async Functions

The BatchProcessor automatically detects whether the process function is async:

```python
# Async function - will be awaited
async def async_process(prompt: str):
    result = await generate_video(prompt)
    return result

# Sync function - will be called directly
def sync_process(prompt: str):
    result = generate_video(prompt)
    return result

# Both work:
await processor.process_batch(prompts, process_func=async_process)
await processor.process_batch(prompts, process_func=sync_process)
```
