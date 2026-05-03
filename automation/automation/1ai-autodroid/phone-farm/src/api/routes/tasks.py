"""Task management routes."""

from fastapi import APIRouter, Depends, HTTPException, Request

from src.api.models.task import TaskCreate, TaskResponse
from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories.task_repo import TaskRepository

router = APIRouter(prefix="/tasks", tags=["tasks"])


async def get_task_repo(request: Request):
    async for db in get_db():
        yield TaskRepository(db)


@router.get("", response_model=list[TaskResponse])
async def list_tasks(
    request: Request,
    repo: TaskRepository = Depends(get_task_repo),
    limit: int = 100,
    offset: int = 0,
):
    tenant_id = getattr(request.state, "tenant_id", None)
    return await repo.list_all(tenant_id=tenant_id, limit=limit, offset=offset)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    request: Request,
    repo: TaskRepository = Depends(get_task_repo),
):
    tenant_id = getattr(request.state, "tenant_id", None)
    task = await repo.get_by_id(task_id, tenant_id=tenant_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(
    data: TaskCreate,
    request: Request,
    repo: TaskRepository = Depends(get_task_repo),
):
    tenant_id = getattr(request.state, "tenant_id", "default")
    row_data = {
        "serial": data.serial,
        "task_type": data.task_type,
        "tenant_id": tenant_id,
        "status": "pending",
    }
    task_id = await repo.create(row_data)
    return await repo.get_by_id(task_id, tenant_id=tenant_id)


@router.put("/{task_id}/status", response_model=TaskResponse)
async def update_task_status(
    task_id: int,
    status: str,
    request: Request,
    repo: TaskRepository = Depends(get_task_repo),
):
    tenant_id = getattr(request.state, "tenant_id", None)
    existing = await repo.get_by_id(task_id, tenant_id=tenant_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Task not found")
    await repo.update_status(task_id, status, tenant_id=tenant_id)
    return await repo.get_by_id(task_id, tenant_id=tenant_id)
