from fastapi import APIRouter, Depends, Request, Response, Security
from app.schemas import LoginSchema, RegisterSchema
from app.core.dependencies import get_auth_service


router = APIRouter()


@router.post("/login")
async def login(
    response: Response,
    login_schema: LoginSchema,
    auth_service=Depends(get_auth_service),
):
    return await auth_service.login(response, login_schema)


@router.post("/register")
async def register(
    register_schema: RegisterSchema, auth_service=Depends(get_auth_service)
):
    return await auth_service.register(register_schema)


@router.post("/refresh")
async def refresh(
    request: Request,
    response: Response,
    auth_service=Depends(get_auth_service),
):
    return await auth_service.refresh(request, response)


@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    auth_service=Depends(get_auth_service),
):
    return await auth_service.logout(request, response)
