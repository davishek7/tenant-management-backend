from fastapi import status
from decimal import Decimal
from datetime import date
from tortoise.transactions import in_transaction
from app.exceptions.custom_exception import AppException
from app.core.authorization import get_tenant_owned_by_user, get_payment_owned_by_user
from app.models.enums import LedgerEntryType, UtilityType


class UtilityService:
    def __init__(self, model, tenant_model, ledger_model):
        self.model = model
        self.tenant_model = tenant_model
        self.ledger_model = ledger_model

    async def create_utility(self, tenant_id, user_id, utility_schema):
        tenant = await get_tenant_owned_by_user(self.tenant_model, tenant_id, user_id)
        data = utility_schema.model_dump()

        period = date.today().replace(day=1)

        data.update(
            {
                "tenant_id": tenant.id,
                "unit_id": tenant.unit_id,
                "property_id": tenant.property_id,
                "user_id": user_id,
                "period": period,
            }
        )

        async with in_transaction():
            utility = await self.model.create(**data)

            ledger_exists = (
                await self.ledger_model.filter(tenant_id=tenant.id, user_id=user_id)
                .order_by("-created_at")
                .first()
            )
            prev_balance = ledger_exists.balance if ledger_exists else Decimal("0")

            await self.ledger_model.create(
                tenant_id=tenant.id,
                unit_id=tenant.unit_id,
                property_id=tenant.property_id,
                user_id=user_id,
                period=utility.period,
                entry_type=LedgerEntryType.UTILITY,
                amount=utility.amount,
                balance=prev_balance + utility.amount,
                reference_id=utility.id,
            )
        return utility

    async def get_utility_bill(self, utility_id, user_id):
        utility_bill = await self.model.filter(id=utility_id, user_id=user_id).first()
        if not utility_bill:
            raise AppException("Utility bill not found", status.HTTP_404_NOT_FOUND)
        return utility_bill
