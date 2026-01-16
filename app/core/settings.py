import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class GeneralSettings(BaseSettings):
    APP_NAME: str = "Tenant Management App REST API"
    TIMEZONE: str = "Asia/Kolkata"
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_TIMEDELTA: str = os.environ.get("ACCESS_TOKEN_EXPIRE_TIMEDELTA")
    REFRESH_TOKEN_EXPIRE_TIMEDELTA: str = os.environ.get(
        "REFRESH_TOKEN_EXPIRE_TIMEDELTA"
    )
    FRONTEND_URL: str = os.environ.get("FRONTEND_URL")


class DatabaseSettings(BaseSettings):
    DATABASE_URL: str = os.environ.get("DATABASE_URL")


class MediaStorageSettings(BaseSettings):
    DOCUMENT_FOLDER: str = os.environ.get("DOCUMENT_FOLDER")


class CloudinarySettings(BaseSettings):
    CLOUD_NAME: str = os.environ.get("CLOUD_NAME")
    API_KEY: str = os.environ.get("API_KEY")
    API_SECRET: str = os.environ.get("API_SECRET")


class CloudflareR2Settings(BaseSettings):
    R2_ACCESS_KEY_ID: str = os.environ.get("R2_ACCESS_KEY_ID")
    R2_SECRET_ACCESS_KEY: str = os.environ.get("R2_SECRET_ACCESS_KEY")
    R2_ENDPOINT_URL: str = os.environ.get("R2_ENDPOINT_URL")


class Settings(
    GeneralSettings,
    DatabaseSettings,
    CloudinarySettings,
    CloudflareR2Settings,
    MediaStorageSettings,
):
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
