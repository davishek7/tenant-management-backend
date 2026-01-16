from fastapi import status
from app.core.authorization import get_property_owned_by_user, get_unit_owned_by_user


class UnitService:
    def __init__(self, model, property_model):
        self.model = model
        self.property_model = property_model

    async def create_unit(self, property_id, user_id, unit_schema):
        property = await get_property_owned_by_user(
            self.property_model, id=property_id, owner=user_id
        )
        data = unit_schema.model_dump()
        data.update({property: property})
        return await self.model.create(**data)

    async def get_units(self, property_id, user_id):
        property = await get_property_owned_by_user(
            self.property_model, property_id=property_id, user_id=user_id
        )
        units = await self.model.filter(property_id=property.id)
        return units

    async def get_unit(self, unit_id, user_id):
        unit = await get_unit_owned_by_user(
            self.model, id=unit_id, property__owner_id=user_id
        )
        return unit

    async def update_unit(self, unit_id, user_id, unit_schema):
        unit = await get_unit_owned_by_user(
            self.model, id=unit_id, property__owner_id=user_id
        )
        data = unit_schema.model_dump(exclude_unset=True)
        if not data:
            return await self.model.filter(
                id=unit.id, property__owner_id=user_id
            ).first()
        await self.model.filter(id=unit.id).update(**data)
        return await self.model.filter(id=unit.id, property__owner_id=user_id).first()

    async def delete_unit(self, unit_id, user_id):
        unit = await get_unit_owned_by_user(self.model, unit_id, user_id)
        return await self.model.filter(id=unit.id, property__owner_id=user_id).delete()
