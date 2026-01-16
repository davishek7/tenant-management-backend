from tortoise import fields
from .base import BaseModel


class User(BaseModel):
    name = fields.CharField(max_length=100)
    phone = fields.CharField(max_length=15, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255, null=True)
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "users"
