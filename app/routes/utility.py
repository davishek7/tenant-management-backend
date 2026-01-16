from fastapi import APIRouter, Depends
from uuid import UUID
from app.schemas import UtilityIn, UtilityOut
from app.security.dependencies import get_current_user_id
from app.core.dependencies import get_utility_service


router = APIRouter()


@router.post("/tenant/{tenant_id}/utility", response_model=UtilityOut)
async def create_utility(
    tenant_id: UUID,
    utility_schema: UtilityIn,
    user_id: UUID = Depends(get_current_user_id),
    utility_service=Depends(get_utility_service),
):
    return await utility_service.create_utility(tenant_id, user_id, utility_schema)


@router.get("/utility/{utility_id}", response_model=UtilityOut)
async def get_utility_bill(
    utility_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    utility_service=Depends(get_utility_service),
):
    return await utility_service.get_utility_bill(utility_id, user_id)
