from pydantic import BaseModel, condecimal
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID
from app.models.enums import PaymentMode


class PaymentIn(BaseModel):
    amount: condecimal(max_digits=10, decimal_places=2)
    payment_mode: PaymentMode
    paid_on: date


class PaymentOut(BaseModel):
    id: UUID
    amount: Decimal
    payment_mode: PaymentMode
    paid_on: date
    created_at: datetime
