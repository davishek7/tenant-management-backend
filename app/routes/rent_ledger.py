from fastapi import APIRouter, Depends
from uuid import UUID
from typing import List
from app.core.dependencies import get_rent_ledger_service
from app.security.dependencies import get_current_user_id
from app.schemas import RentLedgerOut, RentLedgerSummaryOut


router = APIRouter()


@router.post("/generate")
async def generate_rent_ledger(
    user_id: UUID = Depends(get_current_user_id),
    rent_ledger_service=Depends(get_rent_ledger_service),
):
    return await rent_ledger_service.generate_monthly_rent(user_id)


@router.get("/", response_model=List[RentLedgerSummaryOut])
async def get_all_rent_ledgers(
    user_id: UUID = Depends(get_current_user_id),
    rent_ledger_service=Depends(get_rent_ledger_service),
):
    return await rent_ledger_service.get_all_rent_ledgers(user_id)


@router.get("/tenant/{tenant_id}", response_model=List[RentLedgerOut])
async def get_tenant_rent_ledgers(
    tenant_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    rent_ledger_service=Depends(get_rent_ledger_service),
):
    return await rent_ledger_service.get_tenant_rent_ledgers(tenant_id, user_id)
