from tortoise import fields
from .base import BaseModel
from .enums import UtilityType


class UtilityBill(BaseModel):
    tenant = fields.ForeignKeyField(
        "models.Tenant",
        related_name="utility_bills",
        index=True,
    )
    unit = fields.ForeignKeyField(
        "models.Unit",
        index=True,
    )
    property = fields.ForeignKeyField(
        "models.Property",
        index=True,
    )
    user = fields.ForeignKeyField(
        "models.User",
        index=True,
    )

    utility_type = fields.CharEnumField(
        UtilityType,
        max_length=20,
    )

    period = fields.DateField()  # YYYY-MM-01
    amount = fields.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        table = "utility_bills"
        unique_together = ("tenant", "utility_type", "period")
