from fastapi import Request, status
from fastapi.exceptions import RequestValidationError, HTTPException
from cloudinary.exceptions import Error as CloudinaryError
from tortoise.exceptions import DoesNotExist
from app.utils.responses import error_response
from .custom_exception import AppException


def register_exception_handlers(app):
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return error_response(exc.message, exc.status_code, exc.errors)

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        errors = [
            {
                "field": ".".join(str(loc) for loc in err["loc"][1:]),
                "message": err["msg"],
            }
            for err in exc.errors()
        ]
        return error_response(
            "Invalid data provided", status.HTTP_422_UNPROCESSABLE_ENTITY, errors
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return error_response(exc.detail, exc.status_code)

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        print(f"Unhandled error: {exc}")  # Optional: log or notify
        return error_response(
            "Internal server error", status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @app.exception_handler(CloudinaryError)
    async def handle_cloudinary_errors(request: Request, exc: CloudinaryError):
        print(exc.http_code)
        return error_response(
            f"Cloudinary Exception: {str(exc)}",
        )

    @app.exception_handler(DoesNotExist)
    async def handle_tortoise_does_not_exist_error(request: Request, exc: DoesNotExist):
        return error_response(str(exc), status.HTTP_404_NOT_FOUND)
