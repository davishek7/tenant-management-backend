from fastapi import APIRouter, Depends
from uuid import UUID
from app.core.dependencies import get_adjustment_service
from app.security.dependencies import get_current_user_id
from app.schemas import AdjustmentIn, AdjustmentOut


router = APIRouter()


@router.post("/tenant/{tenant_id}/adjustment", response_model=AdjustmentOut)
async def create_adjustment(
    adjustment_schema: AdjustmentIn,
    tenant_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    adjustment_service=Depends(get_adjustment_service),
):
    return await adjustment_service.create_adjustment(
        tenant_id, user_id, adjustment_schema
    )


@router.get("/adjustment/{adjustment_id}", response_model=AdjustmentOut)
async def get_adjustment(
    adjustment_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    adjustment_service=Depends(get_adjustment_service),
):
    return await adjustment_service.get_adjustment(adjustment_id, user_id)
