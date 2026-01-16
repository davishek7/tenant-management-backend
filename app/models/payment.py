from tortoise import fields
from .base import BaseModel
from .enums import PaymentMode


class Payment(BaseModel):
    tenant = fields.ForeignKeyField(
        "models.Tenant",
        related_name="payments",
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

    amount = fields.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = fields.CharEnumField(PaymentMode, max_length=20)
    paid_on = fields.DateField()
    is_reversed = fields.BooleanField(default=False)
    reversed_on = fields.DatetimeField(null=True)

    class Meta:
        table = "payments"
