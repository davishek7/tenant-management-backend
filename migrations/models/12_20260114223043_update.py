from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "adjustments" DROP COLUMN "added_on";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "adjustments" ADD "added_on" DATE NOT NULL;"""


MODELS_STATE = (
    "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"
    "0Y+5bA7ZxA0ZC5pdYFAvxqP518uP/wNfnCEq"
)
