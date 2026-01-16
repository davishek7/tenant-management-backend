from tortoise import fields
from .base import BaseModel


class Tenant(BaseModel):
    user = fields.ForeignKeyField("models.User", related_name="tenants", index=True)
    unit = fields.ForeignKeyField("models.Unit", related_name="tenants", index=True)
    property = fields.ForeignKeyField(
        "models.Property", related_name="tenants", index=True
    )
    name = fields.CharField(max_length=100)
    phone = fields.CharField(max_length=15)
    move_in_date = fields.DateField()
    deposit_amount = fields.DecimalField(max_digits=10, decimal_places=2)
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "tenants"
