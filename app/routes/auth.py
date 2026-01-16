from fastapi import APIRouter, Depends, Security, Response
from fastapi_jwt import JwtAuthorizationCredentials
from app.schemas import LoginSchema, RegisterSchema
from app.core.dependencies import get_auth_service
from app.security.jwt import access_security, refresh_security


router = APIRouter()


@router.post("/login")
async def login(
    response: Response,
    login_schema: LoginSchema,
    auth_service=Depends(get_auth_service),
):
    await auth_service.login(response, login_schema)
    return {"message": "Login successful"}


@router.post("/register")
async def register(
    register_schema: RegisterSchema, auth_service=Depends(get_auth_service)
):
    return await auth_service.register(register_schema)


@router.post("/refresh")
async def refresh(
    response: Response,
    auth_service=Depends(get_auth_service),
    credentials: JwtAuthorizationCredentials = Security(refresh_security),
):
    sub = credentials.subject
    return await auth_service.refresh(response, sub)


@router.post("/logout")
async def logout(
    response: Response,
    auth_service=Depends(get_auth_service),
):
    await auth_service.logout(response)
    return {"message": "Logged out"}
