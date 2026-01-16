from tortoise import fields
from .base import BaseModel


class Property(BaseModel):
    owner = fields.ForeignKeyField("models.User", related_name="properties")
    name = fields.CharField(max_length=100)
    address = fields.TextField()

    class Meta:
        table = "properties"
