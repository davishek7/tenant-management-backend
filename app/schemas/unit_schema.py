from pydantic import BaseModel, condecimal
from decimal import Decimal
from uuid import UUID
from datetime import datetime, date


class UnitIn(BaseModel):
    unit_number: str
    monthly_rent: condecimal(max_digits=10, decimal_places=2)


class UnitOut(BaseModel):
    id: UUID
    property_id: UUID
    unit_number: str
    monthly_rent: Decimal
    is_occupied: bool
    created_at: datetime
    updated_at: datetime


class UnitPatch(BaseModel):
    unit_number: str | None = None
    monthly_rent: condecimal(max_digits=10, decimal_places=2) | None = None
