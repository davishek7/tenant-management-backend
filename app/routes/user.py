from fastapi import APIRouter, Depends
from app.schemas.user_schema import UserProfile, UserPatch
from app.core.dependencies import get_user_service
from app.security.dependencies import get_current_user_id
from uuid import UUID


router = APIRouter()


@router.get("/me", response_model=UserProfile)
async def get_profile(
    user_id: UUID = Depends(get_current_user_id),
    user_service=Depends(get_user_service),
):
    return await user_service.get(user_id)


@router.patch("/me", response_model=UserProfile)
async def update_profile(
    user_schema: UserPatch,
    user_id: UUID = Depends(get_current_user_id),
    user_service=Depends(get_user_service),
):
    return await user_service.update(user_id, user_schema)
