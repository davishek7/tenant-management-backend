from app.core.authorization import get_property_owned_by_user, get_expense_owned_by_user
from app.utils.responses import success_response


class ExpenseService:
    def __init__(self, model, property_model):
        self.model = model
        self.property_model = property_model

    async def add_property_expense(self, property_id, user_id, expense_schema):
        property = await get_property_owned_by_user(
            self.property_model, property_id, user_id
        )
        data = expense_schema.model_dump()
        data.update({"property_id": property.id, "user_id": user_id})
        expense = await self.model.create(**data)
        return expense

    async def get_property_expenses(self, property_id, user_id):
        property = await get_property_owned_by_user(
            self.property_model, property_id, user_id
        )
        expenses = await self.model.filter(property_id=property.id, user_id=user_id)
        return expenses

    async def get_expense(self, expense_id, user_id):
        expense = await get_expense_owned_by_user(self.model, expense_id, user_id)
        return expense

    async def update_expense(self, expense_id, user_id, expense_schema):
        expense = await get_expense_owned_by_user(self.model, expense_id, user_id)
        data = expense_schema.model_dump(exclude_unset=True)
        if not data:
            return self.model.filter(id=expense.id, user_id=user_id).first()
        await self.model.filter(id=expense.id).update(**data)
        return await self.model.filter(id=expense.id, user_id=user_id).first()

    async def delete_expense(self, expense_id, user_id):
        expense = await get_expense_owned_by_user(self.model, expense_id, user_id)
        await self.model.filter(id=expense.id, user_id=user_id).delete()
        return success_response("Expense deleted successfully")
