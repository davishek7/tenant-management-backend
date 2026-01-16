from tortoise import fields
from .base import BaseModel


class Expense(BaseModel):
    user = fields.ForeignKeyField("models.User", index=True)
    property = fields.ForeignKeyField("models.Property", related_name="expenses")
    title = fields.CharField(max_length=100)
    amount = fields.DecimalField(max_digits=10, decimal_places=2)
    expense_date = fields.DateField()
    remarks = fields.TextField(null=True)

    class Meta:
        table = "expenses"
