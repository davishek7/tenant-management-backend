import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class GeneralSettings(BaseSettings):
    APP_NAME: str = "Tenant Management App REST API"
    TIMEZONE: str = "Asia/Kolkata"
    SECRET_KEY: str
    FRONTEND_URL: str


class DatabaseSettings(BaseSettings):
    DATABASE_URL: str


class JWTSettings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_TIMEDELTA: int
    REFRESH_TOKEN_EXPIRE_TIMEDELTA: int
    ALGO: str


class MediaStorageSettings(BaseSettings):
    DOCUMENT_FOLDER: str


class CloudinarySettings(BaseSettings):
    CLOUD_NAME: str
    API_KEY: str
    API_SECRET: str


class CloudflareR2Settings(BaseSettings):
    R2_ACCESS_KEY_ID: str
    R2_SECRET_ACCESS_KEY: str
    R2_ENDPOINT_URL: str


class Settings(
    GeneralSettings,
    DatabaseSettings,
    JWTSettings,
    CloudinarySettings,
    CloudflareR2Settings,
    MediaStorageSettings,
):
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
