from tortoise import fields
from .base import BaseModel
from .enums import LedgerEntryType


class RentLedger(BaseModel):
    tenant = fields.ForeignKeyField(
        "models.Tenant",
        related_name="ledgers",
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

    period = fields.DateField()  # first day of month (YYYY-MM-01)

    entry_type = fields.CharEnumField(
        LedgerEntryType,
        max_length=20,
    )

    amount = fields.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    balance = fields.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    reference_id = fields.UUIDField(
        null=True,
    )  # payment_id / utility_id / adjustment_id

    class Meta:
        table = "rent_ledgers"
        indexes = [
            ("tenant", "period"),
            ("tenant", "entry_type"),
        ]
