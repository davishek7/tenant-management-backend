from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, date
from decimal import Decimal
from app.models.enums import LedgerEntryType


class RentLedgerOut(BaseModel):
    tenant_id: UUID
    unit_id: UUID
    period: date
    entry_type: LedgerEntryType
    amount: Decimal
    balance: Decimal
    created_at: datetime


class RentLedgerSummaryOut(BaseModel):
    tenant_id: UUID
    tenant_name: str
    unit_id: UUID
    balance: Decimal
    last_activity: datetime | None
