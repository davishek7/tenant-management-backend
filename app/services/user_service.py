from uuid import UUID
from fastapi import status
from app.exceptions.custom_exception import AppException


class UserService:
    def __init__(self, model):
        self.model = model

    async def get(self, user_id):
        return await self.model.filter(id=user_id).first()

    async def update(self, user_id, user_schema):
        data = user_schema.model_dump(exclude_unset=True)
        if not data:
            return await self.model.filter(id=user_id).first()
        updated = await self.model.filter(id=user_id).update(**data)
        if not updated:
            raise AppException("User not found", status.HTTP_404_NOT_FOUND)
        return await self.model.filter(id=user_id).first()
