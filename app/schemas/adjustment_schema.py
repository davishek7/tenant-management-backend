from pydantic import BaseModel, condecimal
from decimal import Decimal
from datetime import date, datetime
from uuid import UUID
from app.models.enums import AdjustmentReason


class AdjustmentIn(BaseModel):
    amount: condecimal(max_digits=10, decimal_places=2)
    reason: AdjustmentReason
    note: str


class AdjustmentOut(BaseModel):
    id: UUID
    amount: Decimal
    reason: AdjustmentReason
    note: str
    created_at: datetime
