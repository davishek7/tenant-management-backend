from fastapi import status
from decimal import Decimal
from datetime import datetime, timezone
from tortoise.transactions import in_transaction
from app.exceptions.custom_exception import AppException
from app.core.authorization import get_tenant_owned_by_user
from app.models.enums import LedgerEntryType


class AdjustmentService:
    def __init__(self, model, tenant_model, ledger_model):
        self.model = model
        self.tenant_model = tenant_model
        self.ledger_model = ledger_model

    async def create_adjustment(self, tenant_id, user_id, adjustment_schema):
        tenant = await get_tenant_owned_by_user(self.tenant_model, tenant_id, user_id)
        data = adjustment_schema.model_dump()
        data.update({"tenant_id": tenant.id, "user_id": user_id})

        ledger_exists = (
            await self.ledger_model.filter(tenant_id=tenant.id, user_id=user_id)
            .order_by("-created_at")
            .first()
        )

        prev_balance = ledger_exists.balance if ledger_exists else Decimal("0")
        period = datetime.now(timezone.utc).date().replace(day=1)

        async with in_transaction():
            adjustment = await self.model.create(**data)

            await self.ledger_model.create(
                tenant_id=tenant.id,
                unit_id=tenant.unit_id,
                property_id=tenant.property_id,
                user_id=user_id,
                period=period,
                entry_type=LedgerEntryType.ADJUSTMENT,
                amount=adjustment.amount,
                balance=prev_balance + adjustment.amount,
                reference_id=adjustment.id,
            )
        return adjustment

    async def get_adjustment(self, adjustment_id, user_id):
        adjustment = await self.model.filter(id=adjustment_id, user_id=user_id).first()
        if not adjustment:
            raise AppException("Adjustment not found", status.HTTP_404_NOT_FOUND)
        return adjustment
