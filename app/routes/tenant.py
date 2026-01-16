from fastapi import APIRouter, Depends
from typing import List
from uuid import UUID
from app.core.dependencies import get_tenant_service
from app.security.dependencies import get_current_user_id
from app.schemas import TenantIn, TenantOut, TenantPatch


router = APIRouter()


@router.post("/unit/{unit_id}/tenant", response_model=TenantOut)
async def create_tenant(
    tenant_schema: TenantIn,
    unit_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    tenant_service=Depends(get_tenant_service),
):
    return await tenant_service.create_tenant(unit_id, user_id, tenant_schema)


@router.get("/unit/{unit_id}/tenant", response_model=TenantOut)
async def get_active_tenant_of_unit(
    unit_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    tenant_service=Depends(get_tenant_service),
):
    return await tenant_service.get_active_tenant_of_unit(unit_id, user_id)


@router.get("/tenant/{tenant_id}", response_model=TenantOut)
async def get_tenant(
    tenant_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    tenant_service=Depends(get_tenant_service),
):
    return await tenant_service.get_tenant(tenant_id, user_id)


@router.patch("/tenant/{tenant_id}", response_model=TenantOut)
async def update_tenant(
    tenant_schema: TenantPatch,
    tenant_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    tenant_service=Depends(get_tenant_service),
):
    return await tenant_service.update_tenant(tenant_id, user_id, tenant_schema)


@router.patch("/tenant/{tenant_id}/vacate")
async def vacate_tenant(
    tenant_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    tenant_service=Depends(get_tenant_service),
):
    return await tenant_service.vacate_tenant(tenant_id, user_id)
