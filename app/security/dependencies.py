from fastapi import Security, status
from fastapi_jwt import JwtAuthorizationCredentials
from uuid import UUID
from .jwt import access_security
from app.exceptions.custom_exception import AppException


async def get_current_user_id(
    credentials: JwtAuthorizationCredentials = Security(access_security),
) -> UUID:
    try:
        return credentials.subject["user_id"]
    except KeyError:
        raise AppException("Invalid authentication token", status.HTTP_401_UNAUTHORIZED)
