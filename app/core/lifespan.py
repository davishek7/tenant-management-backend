from fastapi import FastAPI
from contextlib import asynccontextmanager
from tortoise import Tortoise
from app.core.database import TORTOISE_ORM


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Tortoise.init(config=TORTOISE_ORM)
    yield
    Tortoise.close_connections
