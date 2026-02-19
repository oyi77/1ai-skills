"""Batch processor for processing multiple video generation prompts."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional
import asyncio
import uuid
from datetime import datetime


class JobStatus(Enum):
    """Status of a batch job."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class BatchJob:
    """Represents a single job in a batch."""

    job_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    prompt: str = ""
    status: JobStatus = JobStatus.PENDING
    result: Optional[Any] = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """Convert job to dictionary."""
        return {
            "job_id": self.job_id,
            "prompt": self.prompt,
            "status": self.status.value,
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat()
            if self.completed_at
            else None,
        }


class BatchProcessor:
    """Processor for handling multiple video generation jobs with concurrency control."""

    def __init__(
        self,
        max_concurrent: int = 3,
        process_func: Optional[Callable[[str], Any]] = None,
    ):
        """
        Initialize the batch processor.

        Args:
            max_concurrent: Maximum number of concurrent jobs (default: 3)
            process_func: Function to call for processing each prompt
        """
        self.max_concurrent = max_concurrent
        self.process_func = process_func
        self.jobs: dict[str, BatchJob] = {}
        self._semaphore: Optional[asyncio.Semaphore] = None

    def create_job(self, prompt: str) -> BatchJob:
        """Create a new batch job."""
        job = BatchJob(prompt=prompt)
        self.jobs[job.job_id] = job
        return job

    def create_jobs(self, prompts: list[str]) -> list[BatchJob]:
        """Create multiple batch jobs from prompts."""
        return [self.create_job(prompt) for prompt in prompts]

    async def process_batch(
        self,
        prompts: list[str],
        process_func: Optional[Callable[[str], Any]] = None,
    ) -> list[BatchJob]:
        """
        Process multiple prompts with concurrency control.

        Args:
            prompts: List of prompts to process
            process_func: Function to call for processing each prompt
                         (overrides the one set in __init__)

        Returns:
            List of completed BatchJob objects
        """
        func = process_func or self.process_func
        if func is None:
            raise ValueError("No process_func provided")

        jobs = self.create_jobs(prompts)
        self._semaphore = asyncio.Semaphore(self.max_concurrent)

        async def process_job(job: BatchJob):
            async with self._semaphore:
                job.status = JobStatus.RUNNING
                job.started_at = datetime.now()
                try:
                    if asyncio.iscoroutinefunction(func):
                        job.result = await func(job.prompt)
                    else:
                        job.result = func(job.prompt)
                    job.status = JobStatus.COMPLETED
                except Exception as e:
                    job.status = JobStatus.FAILED
                    job.error = str(e)
                finally:
                    job.completed_at = datetime.now()

        await asyncio.gather(
            *[process_job(job) for job in jobs], return_exceptions=True
        )
        return jobs

    def get_job_status(self, job_id: str) -> Optional[BatchJob]:
        """
        Get the status of a specific job.

        Args:
            job_id: The ID of the job to check

        Returns:
            BatchJob object if found, None otherwise
        """
        return self.jobs.get(job_id)

    def get_all_job_statuses(self) -> list[BatchJob]:
        """Get status of all jobs."""
        return list(self.jobs.values())

    def get_jobs_by_status(self, status: JobStatus) -> list[BatchJob]:
        """Get all jobs with a specific status."""
        return [job for job in self.jobs.values() if job.status == status]

    def cancel_job(self, job_id: str) -> bool:
        """Cancel a specific job if it's still pending."""
        job = self.jobs.get(job_id)
        if job and job.status == JobStatus.PENDING:
            job.status = JobStatus.CANCELLED
            job.completed_at = datetime.now()
            return True
        return False

    def get_batch_summary(self) -> dict:
        """Get a summary of the batch processing status."""
        return {
            "total": len(self.jobs),
            "pending": len(self.get_jobs_by_status(JobStatus.PENDING)),
            "running": len(self.get_jobs_by_status(JobStatus.RUNNING)),
            "completed": len(self.get_jobs_by_status(JobStatus.COMPLETED)),
            "failed": len(self.get_jobs_by_status(JobStatus.FAILED)),
            "cancelled": len(self.get_jobs_by_status(JobStatus.CANCELLED)),
        }
