from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "refresh_tokens" (
    "id" UUID NOT NULL PRIMARY KEY,
    "revoked" BOOL NOT NULL DEFAULT False,
    "expires_at" TIMESTAMPTZ NOT NULL,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "refresh_tokens";"""


MODELS_STATE = (
    "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"
)
