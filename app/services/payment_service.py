from fastapi import status
from decimal import Decimal
from datetime import datetime, timezone
from tortoise.transactions import in_transaction
from app.exceptions.custom_exception import AppException
from app.core.authorization import get_tenant_owned_by_user, get_payment_owned_by_user
from app.models.enums import LedgerEntryType


class PaymentService:
    def __init__(self, model, tenant_model, ledger_model):
        self.model = model
        self.tenant_model = tenant_model
        self.ledger_model = ledger_model

    async def create_payment(self, tenant_id, user_id, payment_schema):
        tenant = await get_tenant_owned_by_user(self.tenant_model, tenant_id, user_id)
        data = payment_schema.model_dump()
        data.update(
            {
                "tenant_id": tenant.id,
                "unit_id": tenant.unit_id,
                "property_id": tenant.property_id,
                "user_id": user_id,
            }
        )

        async with in_transaction():
            payment = await self.model.create(**data)

            payment_date = payment.paid_on
            period = payment_date.replace(day=1)
            ledger_amount = abs(payment.amount)

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
                period=period,
                entry_type=LedgerEntryType.PAYMENT,
                amount=-ledger_amount,
                balance=prev_balance - payment.amount,
                reference_id=payment.id,
            )
        return payment

    async def get_payment(self, payment_id, user_id):
        payment = await get_payment_owned_by_user(self.model, payment_id, user_id)
        return payment

    async def reverse_payment(self, payment_id, user_id):
        payment = await get_payment_owned_by_user(self.model, payment_id, user_id)

        last_ledger = (
            await self.ledger_model.filter(tenant_id=payment.tenant_id, user_id=user_id)
            .order_by("-created_at")
            .first()
        )

        prev_balance = last_ledger.balance if last_ledger else Decimal("0")
        period = datetime.now(timezone.utc).date().replace(day=1)

        async with in_transaction():
            await self.model.filter(id=payment_id).update(
                is_reversed=True, reversed_on=datetime.now(timezone.utc)
            )

            await self.ledger_model.create(
                tenant_id=payment.tenant_id,
                unit_id=payment.unit_id,
                property_id=payment.property_id,
                user_id=user_id,
                period=period,
                entry_type=LedgerEntryType.ADJUSTMENT,
                amount=payment.amount,
                balance=prev_balance + payment.amount,
                reference_id=payment.id,
            )
