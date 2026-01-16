from typing import List
from app.models import TenantDocument


def serialize_documents(docs: List[TenantDocument], get_presigned_url) -> List[dict]:
    return [
        {
            "id": doc.id,
            "tenant_id": doc.tenant_id,
            "doc_type": doc.doc_type,
            "file_url": get_presigned_url(doc.filename),
        }
        for doc in docs
    ]


def serialize_document(doc: TenantDocument, get_presigned_url) -> dict:
    return {
        "id": doc.id,
        "tenant_id": doc.tenant_id,
        "doc_type": doc.doc_type,
        "file_url": get_presigned_url(doc.filename),
    }
