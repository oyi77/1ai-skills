"""Device CRUD routes."""

from fastapi import APIRouter, Depends, HTTPException, Request
from httpx import AsyncClient

from src.api.models.device import DeviceCreate, DeviceUpdate, DeviceResponse
from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories.device_repo import DeviceRepository

router = APIRouter(prefix="/devices", tags=["devices"])


async def get_device_repo(request: Request):
    async for db in get_db():
        yield DeviceRepository(db)


@router.get("", response_model=list[DeviceResponse])
async def list_devices(
    request: Request,
    repo: DeviceRepository = Depends(get_device_repo),
    limit: int = 100,
    offset: int = 0,
):
    tenant_id = getattr(request.state, "tenant_id", None)
    return await repo.list_all(tenant_id=tenant_id, limit=limit, offset=offset)


@router.get("/{serial}", response_model=DeviceResponse)
async def get_device(
    serial: str,
    request: Request,
    repo: DeviceRepository = Depends(get_device_repo),
):
    tenant_id = getattr(request.state, "tenant_id", None)
    device = await repo.get_by_serial(serial, tenant_id=tenant_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.post("", response_model=DeviceResponse, status_code=201)
async def create_device(
    data: DeviceCreate,
    request: Request,
    repo: DeviceRepository = Depends(get_device_repo),
):
    from src.domain.entities.device import Device, DeviceStatus

    tenant_id = getattr(request.state, "tenant_id", "default")
    device = Device(
        serial=data.serial,
        name=data.name,
        status=DeviceStatus.UNKNOWN,
        enabled=data.enabled,
        config_json=data.config_json,
        tenant_id=tenant_id,
    )
    row_data = repo.from_entity(device)
    await repo.create(row_data)
    return await repo.get_by_serial(data.serial, tenant_id=tenant_id)


@router.put("/{serial}", response_model=DeviceResponse)
async def update_device(
    serial: str,
    data: DeviceUpdate,
    request: Request,
    repo: DeviceRepository = Depends(get_device_repo),
):
    tenant_id = getattr(request.state, "tenant_id", None)
    existing = await repo.get_by_serial(serial, tenant_id=tenant_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Device not found")

    update_data = data.model_dump(exclude_unset=True)
    if update_data:
        await repo.update(serial, update_data)

    return await repo.get_by_serial(serial, tenant_id=tenant_id)


@router.delete("/{serial}", status_code=204)
async def delete_device(
    serial: str,
    request: Request,
    repo: DeviceRepository = Depends(get_device_repo),
):
    tenant_id = getattr(request.state, "tenant_id", None)
    existing = await repo.get_by_serial(serial, tenant_id=tenant_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Device not found")
    await repo.delete(serial)
