from fastapi import status, Request, Response
from pydantic import EmailStr
from datetime import datetime, timezone, timedelta
from app.core.settings import settings
from app.security.password import hash_password, verify_password, get_dummy_password
from app.exceptions.custom_exception import AppException
from app.security.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
    new_jti,
    COOKIE_BASE,
)


class AuthService:
    def __init__(self, model, refresh_token_model):
        self.model = model
        self.refresh_token_model = refresh_token_model

    async def authenticate(self, email: EmailStr, password: str):
        user = await self.model.filter(email=email).first()
        password_hash = user.password if user else get_dummy_password()
        if not user or not verify_password(password, password_hash):
            raise AppException(
                "Invalid email or password", status.HTTP_401_UNAUTHORIZED
            )
        return user

    async def login(self, response: Response, login_data):
        data = login_data.model_dump()
        user = await self.authenticate(data.get("email"), data.get("password"))

        jti = new_jti()
        access = create_access_token(str(user.id))
        refresh = create_refresh_token(str(user.id), jti)

        await self.refresh_token_model.create(
            id=jti,
            user=user,
            expires_at=datetime.now(timezone.utc)
            + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_TIMEDELTA),
        )

        response.set_cookie("access_token", access, **COOKIE_BASE)
        response.set_cookie("refresh_token", refresh, **COOKIE_BASE)

        return {"message": "Login successful"}

    async def register(self, register_data):
        data = register_data.model_dump()
        data["password"] = hash_password(data["password"])
        return await self.model.create(**data)

    async def refresh(self, request: Request, response: Response):
        refresh_token = request.cookies.get("refresh_token")

        if not refresh_token:
            raise AppException("Invalid refresh token", status.HTTP_401_UNAUTHORIZED)

        payload = decode_token(refresh_token)
        if payload["type"] != "refresh":
            raise AppException(
                "Provided token is not refresh token", status.HTTP_401_UNAUTHORIZED
            )

        record = await self.refresh_token_model.filter(
            id=payload["jti"], revoked=False
        ).first()
        if not record:
            raise AppException("Refresh token is expired or revoked")

        # revoke token
        await self.refresh_token_model.filter(id=payload["jti"]).update(revoked=True)

        jti = new_jti()
        await self.refresh_token_model.create(
            id=jti,
            user_id=payload["sub"],
            expires_at=datetime.now(timezone.utc)
            + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_TIMEDELTA),
        )

        new_access = create_access_token(payload["sub"])
        new_refresh = create_refresh_token(payload["sub"], jti)

        response.set_cookie("access_token", new_access, **COOKIE_BASE)
        response.set_cookie("refresh_token", new_refresh, **COOKIE_BASE)

        return {"message": "Tokens refreshed successfully"}

    async def logout(self, request: Request, response: Response):
        refresh_token = request.cookies.get("refresh_token")
        payload = decode_token(refresh_token)

        await self.refresh_token_model.filter(id=payload["jti"]).update(revoked=True)

        response.delete_cookie("access_token", path="/")
        response.delete_cookie("refresh_token", path="/")

        return {"message": "Logged out"}
