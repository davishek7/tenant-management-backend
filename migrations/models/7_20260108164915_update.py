from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "tenants" DROP CONSTRAINT IF EXISTS "fk_tenants_users_560883bf";
        ALTER TABLE "tenants" RENAME COLUMN "property_owner_id" TO "user_id";
        ALTER TABLE "tenants" ADD CONSTRAINT "fk_tenants_users_0039fabe" FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "tenants" DROP CONSTRAINT IF EXISTS "fk_tenants_users_0039fabe";
        ALTER TABLE "tenants" RENAME COLUMN "user_id" TO "property_owner_id";
        ALTER TABLE "tenants" ADD CONSTRAINT "fk_tenants_users_560883bf" FOREIGN KEY ("property_owner_id") REFERENCES "users" ("id") ON DELETE CASCADE;"""


MODELS_STATE = (
    "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"
    "Iyp2PEgzDCc5leYFguvFz94+Xpf+SLwx4="
)
