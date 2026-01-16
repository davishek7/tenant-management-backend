from datetime import timedelta
from fastapi import Response
from app.core.settings import settings
from fastapi_jwt import JwtAccessCookie, JwtRefreshCookie


access_security = JwtAccessCookie(
    settings.SECRET_KEY,
    auto_error=True,
    access_expires_delta=timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_TIMEDELTA)),
)

refresh_security = JwtRefreshCookie(
    settings.SECRET_KEY,
    auto_error=True,
    refresh_expires_delta=timedelta(days=int(settings.REFRESH_TOKEN_EXPIRE_TIMEDELTA)),
)


async def generate_and_set_auth_tokens(response: Response, sub: dict) -> None:
    access_token = access_security.create_access_token(sub)
    refresh_token = refresh_security.create_refresh_token(sub)
    access_security.set_access_cookie(response, access_token)
    refresh_security.set_refresh_cookie(response, refresh_token)


async def logout_and_remove_auth_tokens(response: Response) -> None:
    access_security.unset_access_cookie(response)
    refresh_security.unset_refresh_cookie(response)
