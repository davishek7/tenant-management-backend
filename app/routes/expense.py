from fastapi import APIRouter, Depends
from uuid import UUID
from typing import List
from app.schemas import ExpenseIn, ExpenseOut, ExpensePatch
from app.core.dependencies import get_expense_service
from app.security.dependencies import get_current_user_id


router = APIRouter()


@router.post("/property/{property_id}/expense", response_model=ExpenseOut)
async def add_property_expense(
    expense_schema: ExpenseIn,
    property_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    expense_service=Depends(get_expense_service),
):
    return await expense_service.add_property_expense(
        property_id, user_id, expense_schema
    )


@router.get("/property/{property_id}/expense", response_model=List[ExpenseOut])
async def get_property_expenses(
    property_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    expense_service=Depends(get_expense_service),
):
    return await expense_service.get_property_expenses(property_id, user_id)


@router.get("/expense/{expense_id}", response_model=ExpenseOut)
async def get_expense(
    expense_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    expense_service=Depends(get_expense_service),
):
    return await expense_service.get_expense(expense_id, user_id)


@router.patch("/expense/{expense_id}", response_model=ExpenseOut)
async def update_expense(
    expense_schema: ExpensePatch,
    expense_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    expense_service=Depends(get_expense_service),
):
    return await expense_service.update_expense(expense_id, user_id, expense_schema)


@router.delete("/expense/{expense_id}", response_model=ExpenseOut)
async def delete_expense(
    expense_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    expense_service=Depends(get_expense_service),
):
    return await expense_service.delete_expense(expense_id, user_id)
