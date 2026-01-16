from pydantic import BaseModel
from uuid import UUID
from app.models.enums import TenantDocType


class DocumentOut(BaseModel):
    id: UUID
    tenant_id: UUID
    doc_type: TenantDocType
    file_url: str


class DocumentPatch(BaseModel):
    doc_type: TenantDocType | None = None
