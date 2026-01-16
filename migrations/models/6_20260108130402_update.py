from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "tenants" DROP CONSTRAINT IF EXISTS "fk_tenants_users_0039fabe";
        ALTER TABLE "tenants" RENAME COLUMN "user_id" TO "property_owner_id";
        ALTER TABLE "tenants" ADD CONSTRAINT "fk_tenants_users_560883bf" FOREIGN KEY ("property_owner_id") REFERENCES "users" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "tenants" DROP CONSTRAINT IF EXISTS "fk_tenants_users_560883bf";
        ALTER TABLE "tenants" RENAME COLUMN "property_owner_id" TO "user_id";
        ALTER TABLE "tenants" ADD CONSTRAINT "fk_tenants_users_0039fabe" FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON DELETE CASCADE;"""


MODELS_STATE = (
    "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"
    "M5HSMehBGey/QCw2Lh5eofL0//A9O61F4="
)
