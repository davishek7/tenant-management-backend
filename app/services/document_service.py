from app.core.authorization import get_tenant_owned_by_user, get_document_owned_by_user
from app.serializers.document_serializer import serialize_documents, serialize_document
from app.utils.responses import success_response


class DocumentService:
    def __init__(self, cloudflare_service, model, tenant_model):
        self.model = model
        self.tenant_model = tenant_model
        self.cloudflare_service = cloudflare_service

    async def add_tenant_document(self, tenant_id, user_id, file, doc_type):
        tenant = await get_tenant_owned_by_user(self.tenant_model, tenant_id, user_id)
        uploaded_document_filename = await self.cloudflare_service.upload_document(
            tenant.id, user_id, file
        )
        document = await self.model.create(
            tenant_id=tenant.id, doc_type=doc_type, filename=uploaded_document_filename
        )
        return serialize_document(document, self.cloudflare_service.get_presigned_url)

    async def get_tenant_documents(self, tenant_id, user_id):
        tenant = await get_tenant_owned_by_user(self.tenant_model, tenant_id, user_id)
        documents = await self.model.filter(
            tenant_id=tenant.id, tenant__user_id=user_id
        )
        return serialize_documents(documents, self.cloudflare_service.get_presigned_url)

    async def get_document(self, document_id, user_id):
        document = await get_document_owned_by_user(self.model, document_id, user_id)
        return serialize_document(document, self.cloudflare_service.get_presigned_url)

    async def update_document(self, document_id, user_id, document_schema):
        document = await get_document_owned_by_user(self.model, document_id, user_id)
        data = document_schema.model_dump(exclude_unset=True)
        if not data:
            return serialize_document(
                document, self.cloudflare_service.get_presigned_url
            )
        await self.model.filter(id=document.id).update(**data)
        updated_document = await self.model.filter(id=document.id).first()
        return serialize_document(
            updated_document, self.cloudflare_service.get_presigned_url
        )

    async def delete_document(self, document_id, user_id):
        document = await get_document_owned_by_user(self.model, document_id, user_id)
        await self.cloudflare_service.delete_document(document.filename)
        await self.model.filter(id=document_id).delete()
        return success_response("Document deleted successfully")
