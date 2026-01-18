from fastapi import status, Request
from app.security.jwt import decode_token
from uuid import UUID
from app.exceptions.custom_exception import AppException


async def get_current_user_id(request: Request) -> UUID:
    access_token = request.cookies.get("access_token")

    if not access_token:
        raise AppException("Not authenticated", status.HTTP_401_UNAUTHORIZED)

    payload = decode_token(access_token)
    return payload["sub"]
