from pydantic import BaseModel, condecimal
from uuid import UUID
from decimal import Decimal
from datetime import date, datetime


class ExpenseIn(BaseModel):
    title: str
    amount: condecimal(max_digits=10, decimal_places=2)
    expense_date: date
    remarks: str


class ExpenseOut(BaseModel):
    id: UUID
    property_id: UUID
    title: str
    amount: Decimal
    expense_date: date
    remarks: str


class ExpensePatch(BaseModel):
    title: str | None = None
    amount: Decimal | None = None
    expense_date: date | None = None
    remarks: str | None = None
