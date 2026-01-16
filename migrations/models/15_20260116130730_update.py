from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "tenant_documents" RENAME COLUMN "file_url" TO "filename";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "tenant_documents" RENAME COLUMN "filename" TO "file_url";"""


MODELS_STATE = (
    "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"
)
