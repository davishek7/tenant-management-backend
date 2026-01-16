from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class UserProfile(BaseModel):
    id: UUID
    name: str
    phone: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserPatch(BaseModel):
    name: str | None = None
    phone: str | None = None
