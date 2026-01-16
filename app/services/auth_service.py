from fastapi import status
from pydantic import EmailStr
from app.security.jwt import generate_and_set_auth_tokens, logout_and_remove_auth_tokens
from app.security.password import hash_password, verify_password, get_dummy_password
from app.exceptions.custom_exception import AppException
from app.utils.responses import success_response


class AuthService:
    def __init__(self, model):
        self.model = model

    async def _authenticate(self, email: EmailStr, password: str):
        user = await self.model.filter(email=email).first()
        password_hash = user.password if user else get_dummy_password()
        if not user or not verify_password(password, password_hash):
            raise AppException(
                "Invalid email or password", status.HTTP_401_UNAUTHORIZED
            )
        return {"user_id": str(user.id), "email": user.email}

    async def login(self, response, login_data):
        data = login_data.model_dump()
        sub = await self._authenticate(data.get("email"), data.get("password"))
        return await generate_and_set_auth_tokens(response, sub)

    async def register(self, register_data):
        data = register_data.model_dump()
        data["password"] = hash_password(data["password"])
        return await self.model.create(**data)

    async def refresh(self, response, sub):
        return await generate_and_set_auth_tokens(response, sub)

    async def logout(self, response):
        return await logout_and_remove_auth_tokens(response)
