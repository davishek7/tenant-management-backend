from tortoise import fields
from .base import BaseModel
from .enums import AdjustmentReason


class Adjustment(BaseModel):
    tenant = fields.ForeignKeyField(
        "models.Tenant",
        related_name="adjustments",
        index=True,
    )
    user = fields.ForeignKeyField(
        "models.User",
        index=True,
    )

    amount = fields.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    # positive → extra charge
    # negative → discount / waiver

    reason = fields.CharEnumField(
        AdjustmentReason,
        max_length=30,
    )

    note = fields.TextField(null=True)

    class Meta:
        table = "adjustments"
