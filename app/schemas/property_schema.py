from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class PropertyIn(BaseModel):
    name: str
    address: str


class PropertyOut(BaseModel):
    id: UUID
    owner_id: UUID
    name: str
    address: str
    created_at: datetime
    updated_at: datetime


class PropertyPatch(BaseModel):
    name: str | None = None
    address: str | None = None
