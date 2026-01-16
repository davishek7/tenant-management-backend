from fastapi import status
from calendar import monthrange
from decimal import Decimal, ROUND_HALF_UP
from tortoise.transactions import in_transaction
from app.exceptions.custom_exception import AppException
from app.core.authorization import get_unit_owned_by_user, get_tenant_owned_by_user
from app.models.enums import LedgerEntryType
from app.utils.responses import success_response


class TenantService:
    def __init__(self, model, unit_model, ledger_model):
        self.model = model
        self.unit_model = unit_model
        self.ledger_model = ledger_model

    async def create_tenant(self, unit_id, user_id, tenant_schema):
        unit = await get_unit_owned_by_user(self.unit_model, unit_id, user_id)
        active_exists = await self.model.filter(
            unit_id=unit.id, is_active=True
        ).exists()
        if active_exists:
            raise AppException(
                "Unit already has an active tenant",
                status.HTTP_409_CONFLICT,
            )
        data = tenant_schema.model_dump()
        data.update(
            {"property_id": unit.property_id, "unit_id": unit.id, "user_id": user_id}
        )

        move_in = data["move_in_date"]
        period = move_in.replace(day=1)

        monthly_rent = Decimal(unit.monthly_rent)
        days_in_month = monthrange(move_in.year, move_in.month)[1]

        if move_in.day == 1:
            rent_amount = monthly_rent
        else:
            daily = monthly_rent / days_in_month
            days = days_in_month - move_in.day + 1
            rent_amount = (daily * days).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )

        async with in_transaction():
            tenant = await self.model.create(**data)

            await self.ledger_model.create(
                tenant_id=tenant.id,
                unit_id=unit.id,
                property_id=tenant.property_id,
                user_id=user_id,
                period=period,
                entry_type=LedgerEntryType.RENT,
                amount=rent_amount,
                balance=rent_amount,
            )

            await self.unit_model.filter(id=unit.id).update(is_occupied=True)

        return tenant

    async def get_active_tenant_of_unit(self, unit_id, user_id):
        unit = await self.unit_model.filter(
            id=unit_id, property__owner_id=user_id, is_occupied=True
        ).first()
        if not unit:
            raise AppException("Unit with tenant not found", status.HTTP_404_NOT_FOUND)
        tenant = await self.model.filter(
            unit_id=unit.id, user_id=user_id, is_active=True
        )
        return tenant

    async def get_tenant(self, tenant_id, user_id):
        tenant = await get_tenant_owned_by_user(self.model, tenant_id, user_id)
        return tenant

    async def update_tenant(self, tenant_id, user_id, tenant_schema):
        tenant = await get_tenant_owned_by_user(self.model, tenant_id, user_id)
        data = tenant_schema.model_dump(exclude_unset=True)
        if not data:
            return await self.model.get(id=tenant.id, user_id=user_id)
        await self.model.filter(id=tenant.id).update(**data)
        return await self.model.filter(id=tenant.id, user_id=user_id).first()

    async def vacate_tenant(self, tenant_id, user_id):
        tenant = (
            await self.model.filter(id=tenant_id, user_id=user_id, is_active=True)
            .select_related("unit")
            .first()
        )
        if not tenant:
            raise AppException("Active tenant not found", status.HTTP_404_NOT_FOUND)
        async with in_transaction():
            await self.model.filter(id=tenant.id).update(is_active=False)
            await self.unit_model.filter(id=tenant.unit_id).update(is_occupied=False)
        return success_response("Tenant vacated successfully")
