from fastapi import APIRouter, Depends
from uuid import UUID
from app.core.dependencies import get_payment_service
from app.security.dependencies import get_current_user_id
from app.schemas import PaymentIn, PaymentOut


router = APIRouter()


@router.post("/tenant/{tenant_id}/payment", response_model=PaymentOut)
async def create_payment(
    payment_schema: PaymentIn,
    tenant_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    payment_service=Depends(get_payment_service),
):
    return await payment_service.create_payment(tenant_id, user_id, payment_schema)


@router.get("/payment/{payment_id}", response_model=PaymentOut)
async def get_payment(
    payment_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    payment_service=Depends(get_payment_service),
):
    return await payment_service.get_payment(payment_id, user_id)


@router.post("/payment/{payment_id}/reverse")
async def reverse_payment(
    payment_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    payment_service=Depends(get_payment_service),
):
    await payment_service.reverse_payment(payment_id, user_id)
    return {"message": "Payment reversed successfully"}
