from fastapi import APIRouter, Depends, Form, Body, File, UploadFile
from uuid import UUID
from typing import List
from app.schemas import DocumentOut, DocumentPatch
from app.core.dependencies import get_document_service
from app.security.dependencies import get_current_user_id
from app.models.enums import TenantDocType


router = APIRouter()


@router.post("/tenant/{tenant_id}/document", response_model=DocumentOut)
async def add_tenant_document(
    tenant_id: UUID,
    file: UploadFile = File(...),
    doc_type: TenantDocType = Form(...),
    user_id: UUID = Depends(get_current_user_id),
    document_service=Depends(get_document_service),
):
    return await document_service.add_tenant_document(
        tenant_id, user_id, file, doc_type
    )


@router.get("/tenant/{tenant_id}/document", response_model=List[DocumentOut])
async def get_tenant_documents(
    tenant_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    document_service=Depends(get_document_service),
):
    return await document_service.get_tenant_documents(tenant_id, user_id)


@router.get("/document/{document_id}", response_model=DocumentOut)
async def get_document(
    document_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    document_service=Depends(get_document_service),
):
    return await document_service.get_document(document_id, user_id)


@router.patch("/document/{document_id}", response_model=DocumentOut)
async def update_document(
    document_schema: DocumentPatch,
    document_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    document_service=Depends(get_document_service),
):
    return await document_service.update_document(document_id, user_id, document_schema)


@router.delete("/document/{document_id}")
async def delete_document(
    document_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    document_service=Depends(get_document_service),
):
    return await document_service.delete_document(document_id, user_id)
