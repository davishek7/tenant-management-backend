from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "adjustments" ADD "added_on" DATE NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "adjustments" DROP COLUMN "added_on";"""


MODELS_STATE = (
    "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"
)
