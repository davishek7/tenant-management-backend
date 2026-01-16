import boto3
import requests
from botocore.config import Config
from app.core.settings import settings
from app.core.authorization import get_tenant_owned_by_user


class CloudflareService:
    def __init__(self, document_model, tenant_model):
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.R2_ENDPOINT_URL,
            aws_access_key_id=settings.R2_ACCESS_KEY_ID,
            aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
            config=Config(signature_version="s3v4"),
            region_name="auto",
        )
        self.bucket = settings.DOCUMENT_FOLDER
        self.document_model = document_model
        self.tenant_model = tenant_model

    def get_presigned_url(self, filename: str):
        return self.client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": self.bucket, "Key": filename},
            ExpiresIn=3600,
        )

    async def upload_document(self, tenant_id, user_id, file):
        await get_tenant_owned_by_user(self.tenant_model, tenant_id, user_id)

        content = await file.read()

        result = self.client.put_object(
            Bucket=self.bucket,
            Key=file.filename,
            Body=content,
            ContentType=file.content_type,
        )

        if result:
            return file.filename

    async def delete_document(self, filename):
        return self.client.delete_object(Bucket=self.bucket, Key=filename)
