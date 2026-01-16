from app.utils.responses import success_response
from app.core.authorization import get_property_owned_by_user


class PropertyService:
    def __init__(self, model):
        self.model = model

    async def get_list(self, user_id):
        properties = await self.model.filter(owner=user_id)
        return properties

    async def get(self, id, user_id):
        property = await get_property_owned_by_user(self.model, id, user_id)
        return property

    async def create(self, property_schema, user_id):
        data = property_schema.model_dump()
        data["owner_id"] = user_id
        return await self.model.create(**data)

    async def update(self, property_schema, id, user_id):
        property = await get_property_owned_by_user(self.model, id, user_id)
        data = property_schema.model_dump(exclude_unset=True)
        if not data:
            return await self.model.filter(id=property.id, owner=user_id).first()
        await self.model.filter(id=property.id, owner=user_id).update(**data)
        return await self.model.filter(id=property.id).first()

    async def delete(self, id, user_id):
        property = await get_property_owned_by_user(self.model, id, user_id)
        await self.model.filter(id=property.id, owner_id=user_id).delete()
        return success_response("Property deleted successfully")
