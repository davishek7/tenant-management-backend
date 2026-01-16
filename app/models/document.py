from tortoise import fields
from .base import BaseModel
from .enums import TenantDocType


class TenantDocument(BaseModel):
    tenant = fields.ForeignKeyField("models.Tenant", related_name="documents")
    doc_type = fields.CharEnumField(TenantDocType, max_length=50)
    filename = fields.TextField()

    class Meta:
        table = "tenant_documents"
