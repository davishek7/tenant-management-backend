from tortoise import fields
from .base import BaseModel


class Unit(BaseModel):
    property = fields.ForeignKeyField("models.Property", related_name="units")
    unit_number = fields.CharField(max_length=50)
    monthly_rent = fields.DecimalField(max_digits=10, decimal_places=2)
    is_occupied = fields.BooleanField(default=False)

    class Meta:
        table = "units"
        unique_together = ("property", "unit_number")
