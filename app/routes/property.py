from fastapi import APIRouter, Depends, Security
from uuid import UUID
from typing import List
from fastapi_jwt import JwtAuthorizationCredentials
from app.security.jwt import access_security
from app.core.dependencies import get_property_service
from app.security.dependencies import get_current_user_id
from app.schemas import PropertyIn, PropertyPatch, PropertyOut


router = APIRouter()


@router.get("/", response_model=List[PropertyOut])
async def get_list(
    user_id: UUID = Depends(get_current_user_id),
    property_service=Depends(get_property_service),
):
    return await property_service.get_list(user_id)


@router.get("/{id}", response_model=PropertyOut)
async def get(
    id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    property_service=Depends(get_property_service),
):
    return await property_service.get(id, user_id)


@router.post("/", response_model=PropertyOut)
async def create(
    property_schema: PropertyIn,
    user_id: UUID = Depends(get_current_user_id),
    property_service=Depends(get_property_service),
):
    return await property_service.create(property_schema, user_id)


@router.patch("/{id}", response_model=PropertyOut)
async def update(
    property_schema: PropertyPatch,
    id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    property_service=Depends(get_property_service),
):
    return await property_service.update(property_schema, id, user_id)


@router.delete("/{id}")
async def delete(
    id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    property_service=Depends(get_property_service),
):
    return await property_service.delete(id, user_id)
