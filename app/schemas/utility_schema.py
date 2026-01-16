from pydantic import BaseModel, condecimal
from decimal import Decimal
from uuid import UUID
from datetime import date, datetime
from app.models.enums import UtilityType


class UtilityIn(BaseModel):
    utility_type: UtilityType
    period: date
    amount: condecimal(max_digits=10, decimal_places=2)


class UtilityOut(BaseModel):
    id: UUID
    utility_type: UtilityType
    period: date
    amount: Decimal
    created_at: datetime
