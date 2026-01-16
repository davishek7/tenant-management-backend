from pydantic import BaseModel, condecimal
from decimal import Decimal
from uuid import UUID
from datetime import datetime


class TenantIn(BaseModel):
    name: str
    phone: str
    move_in_date: datetime
    deposit_amount: condecimal(max_digits=10, decimal_places=2)


class TenantOut(BaseModel):
    id: UUID
    unit_id: UUID
    property_id: UUID
    user_id: UUID
    name: str
    phone: str
    deposit_amount: Decimal
    is_active: bool
    created_at: datetime
    updated_at: datetime


class TenantPatch(BaseModel):
    name: str | None = None
    phone: str | None = None
    deposit_amount: condecimal(max_digits=10, decimal_places=2) | None = None
