from fastapi import APIRouter, Depends
from uuid import UUID
from typing import List
from app.schemas import UnitIn, UnitOut, UnitPatch
from app.core.dependencies import get_unit_service
from app.security.dependencies import get_current_user_id


router = APIRouter()


@router.post("/property/{property_id}/unit", response_model=UnitOut)
async def create_unit(
    property_id: UUID,
    unit_schema: UnitIn,
    user_id: UUID = Depends(get_current_user_id),
    unit_service=Depends(get_unit_service),
):
    return await unit_service.create_unit(property_id, user_id, unit_schema)


@router.get("/property/{property_id}/unit", response_model=List[UnitOut])
async def get_units(
    property_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    unit_service=Depends(get_unit_service),
):
    return await unit_service.get_units(property_id, user_id)


@router.get("/unit/{unit_id}", response_model=UnitOut)
async def get_unit(
    unit_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    unit_service=Depends(get_unit_service),
):
    return await unit_service.get_unit(unit_id, user_id)


@router.patch("/unit/{unit_id}", response_model=UnitOut)
async def update_unit(
    unit_id: UUID,
    unit_schema: UnitPatch,
    user_id: UUID = Depends(get_current_user_id),
    unit_service=Depends(get_unit_service),
):
    return await unit_service.update_unit(unit_id, user_id, unit_schema)


@router.delete("/unit/{unit_id}")
async def delete_unit(
    unit_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    unit_service=Depends(get_unit_service),
):
    return await unit_service.delete_unit(unit_id, user_id)
