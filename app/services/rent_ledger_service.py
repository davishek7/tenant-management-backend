from decimal import Decimal
from datetime import date
from tortoise.transactions import in_transaction
from app.models.enums import LedgerEntryType
from app.core.authorization import get_tenant_owned_by_user


class RentLedgerService:
    def __init__(self, model, tenant_model):
        self.model = model
        self.tenant_model = tenant_model

    async def generate_monthly_rent(self, user_id):
        period = date.today().replace(day=1)

        tenants = await self.tenant_model.filter(
            user_id=user_id, is_active=True
        ).select_related("unit")

        created = skipped = 0

        for tenant in tenants:
            ledger_exists = await self.model.filter(
                tenant_id=tenant.id, user_id=user_id, period=period
            ).exists()

            if ledger_exists:
                skipped += 1
                continue

            async with in_transaction():
                last_ledger = (
                    await self.model.filter(tenant_id=tenant.id)
                    .order_by("-created_at")
                    .first()
                )

                prev_balance = last_ledger.balance if last_ledger else Decimal("0")

                await self.model.create(
                    tenant_id=tenant.id,
                    unit_id=tenant.unit_id,
                    property_id=tenant.property_id,
                    user_id=user_id,
                    period=period,
                    entry_type=LedgerEntryType.RENT,
                    amount=tenant.unit.monthly_rent,
                    balance=prev_balance + tenant.unit.monthly_rent,
                )

                created += 1
        return {"period": str(period), "created": created, "skipped": skipped}

    async def get_all_rent_ledgers(self, user_id):
        tenants = await self.tenant_model.filter(
            user_id=user_id, is_active=True
        ).select_related("unit")

        result = []

        for tenant in tenants:
            last_ledger = (
                await self.model.filter(tenant_id=tenant.id)
                .order_by("-created_at")
                .first()
            )

            result.append(
                {
                    "tenant_id": tenant.id,
                    "tenant_name": tenant.name,
                    "unit_id": tenant.unit_id,
                    "balance": last_ledger.balance if last_ledger else 0,
                    "last_activity": last_ledger.created_at if last_ledger else None,
                }
            )
        return result

    async def get_tenant_rent_ledgers(self, tenant_id, user_id):
        tenant = await self.tenant_model.filter(id=tenant_id, user_id=user_id).first()
        rent_ledgers = await self.model.filter(
            tenant_id=tenant.id, user_id=user_id
        ).order_by("-created_at")
        return rent_ledgers
